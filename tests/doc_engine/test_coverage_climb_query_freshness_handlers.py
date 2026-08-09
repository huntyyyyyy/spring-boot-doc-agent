"""Coverage climb: freshness policy and query handler filters."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any
import pytest
from doc_engine.pipeline.local_runner_phases import support as phase_support
from doc_engine.query import kinds as kinds_mod
from doc_engine.query import load as load_mod
from doc_engine.query import packet as packet_mod
from doc_engine.query import schema_check as schema_mod
from doc_engine.query.handlers import dependents as dep_mod
from doc_engine.query.handlers import facts as facts_mod
from doc_engine.scanning import spring as spring_mod
from stf.runners import implement as implement_mod
from stf.runners.store import TasksStore
from stf.schemas.blockers import BlockerClass
from stf.validators import lint_tasks as lint_mod
from tests.stf.conftest import build_minimal_valid_tasks

def test_file_signature_and_freshness_helpers(tmp_path: Path) -> None:
    assert packet_mod._normalized_rel_path(r"a\b.java") == "a/b.java"
    assert packet_mod._file_signature_matches(tmp_path / "missing.java", "sig") is False
    src = tmp_path / "A.java"
    src.write_text("class A {}", encoding="utf-8")
    from doc_engine.core.walk import compute_file_signature

    sig = compute_file_signature(str(src))
    assert packet_mod._file_signature_matches(src, sig) is True
    assert packet_mod._file_signature_matches(src, None) is False
    live = packet_mod._live_paths_matching_signatures(
        tmp_path, {"A.java": sig}, {"A.java", "missing.java"}
    )
    assert "A.java" in live
    assert "missing.java" not in live


def test_build_freshness_policy_assume_and_drift(tmp_path: Path) -> None:
    policy = packet_mod._build_freshness_policy(
        repo_path=None,
        signals={},
        primary=[],
        drift_report_path=None,
        root_path=tmp_path,
    )
    assert policy.__class__.__name__ == "UnknownFreshnessWhenNoRepo"
    drift = tmp_path / "drift.json"
    drift.write_text("[]", encoding="utf-8")
    wrapped = packet_mod._wrap_freshness_with_drift_report(
        SimpleNamespace(), drift, tmp_path
    )
    assert wrapped.__class__.__name__ != "DriftReportFreshness"
    report = tmp_path / "ok.json"
    report.write_text(json.dumps({"changed_files": ["a.java"]}), encoding="utf-8")
    src = tmp_path / "A.java"
    src.write_text("class A {}", encoding="utf-8")
    from doc_engine.core.walk import compute_file_signature
    from doc_engine.query.freshness import SignatureFreshness

    sig = compute_file_signature(str(src))
    inner = SignatureFreshness(
        repo_root=tmp_path, signatures={"A.java": sig}, live_paths=set()
    )
    drifted = packet_mod._wrap_freshness_with_drift_report(inner, report, tmp_path)
    assert drifted.__class__.__name__ == "DriftReportFreshness"
    labeled = packet_mod._label_items(policy, [{"path": "A.java"}, {"path": 1}])
    assert labeled[0]["freshness"] == "unknown"


def test_score_partition_and_assemble() -> None:
    scored = packet_mod._score_raw(
        "auth",
        {
            "provider": "facts",
            "path": "a.java",
            "match": "sec",
            "bucket": "security",
            "contested": True,
        },
    )
    assert scored["provider"] == "facts"
    findings, risks, rest = packet_mod._partition_by_provider(
        [
            {"provider": "facts", "score": 1},
            {"provider": "redaction", "score": 1},
            {"provider": "other", "score": 1},
        ]
    )
    assert len(findings) == 1 and len(risks) == 1 and len(rest) == 1
    packet = packet_mod._assemble_packet(
        request="r",
        budget=10,
        tokens_used=1,
        truncated=False,
        primary=[],
        related=[],
        findings=[],
        risks=[],
        providers_used=["facts"],
    )
    assert packet["empty"] is True
    assert packet["kind"] == "context-packet"


def test_build_freshness_with_repo(tmp_path: Path) -> None:
    src = tmp_path / "A.java"
    src.write_text("class A {}", encoding="utf-8")
    from doc_engine.core.walk import compute_file_signature

    sig = compute_file_signature(str(src))
    policy = packet_mod._build_freshness_policy(
        repo_path=tmp_path,
        signals={"file_signatures": {"A.java": sig, "bad": 1}},
        primary=[{"path": "A.java"}],
        drift_report_path=None,
        root_path=tmp_path,
    )
    assert policy.__class__.__name__ == "SignatureFreshness"
    # non-mapping signatures coerced to empty
    policy2 = packet_mod._build_freshness_policy(
        repo_path=tmp_path,
        signals={"file_signatures": ["nope"]},
        primary=[],
        drift_report_path=None,
        root_path=tmp_path,
    )
    assert policy2.__class__.__name__ == "SignatureFreshness"


def test_facts_filters_and_unknown_predicate() -> None:
    rows = [
        {"predicate": "MAPS_TO", "file": "a/b.java", "subject": "Foo", "qualifiers": {"fqcn": "c.Foo"}},
        {"predicate": "CUSTOM", "file": "x.java", "subject": "Bar", "qualifiers": "bad"},
        "skip-me",
    ]
    with pytest.raises(load_mod.QueryError, match="unknown facts predicate"):
        facts_mod.query_facts(rows, predicate="NOPE")
    hit = facts_mod.query_facts(
        rows,
        predicate="MAPS_TO",
        file_contains="a/",
        fqcn="c.Foo",
        subject_contains="Foo",
    )
    assert len(hit) == 1
    assert facts_mod._fqcn_of({"qualifiers": "x"}) == ""
    assert facts_mod.query_facts(rows, predicate="CUSTOM")[0]["predicate"] == "CUSTOM"


def test_dependents_want_filters_and_edges() -> None:
    assert dep_mod._normalize_want_file(None) is None
    assert dep_mod._normalize_want_file(r"a\b.java") == "a/b.java"
    assert dep_mod._matches_want_type("com.Foo", "Foo") is True
    assert dep_mod._passes_target_filters("a.java", "a.java", "x", None, None) is False
    assert dep_mod._arc_direction("a.java", "b.java", "a.java") == "outbound"
    assert dep_mod._arc_direction("a.java", "b.java", "b.java") == "inbound"
    assert dep_mod._from_edges({"groups": {}}, "missing", target_file=None) == []
    edges = {
        "groups": {
            "1": {
                "outbound": [{"from": "a.java", "to": "b.java"}, "skip"],
                "inbound": [{"from": "c.java", "to": "a.java"}],
            }
        }
    }
    rows = dep_mod._from_edges(edges, 1, target_file="a.java")
    assert {r["direction"] for r in rows} == {"outbound", "inbound"}
