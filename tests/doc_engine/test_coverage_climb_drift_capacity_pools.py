"""Coverage climb: drift classify/citations, signals schema, capacity stage4 pools."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from doc_engine.scanning.support import _codeql_runner as runner
from doc_engine.scanning.support import _codeql_cli as cli_mod
from doc_engine.tools import capacity_preflight as cap
from doc_engine.tools import spring_drift_check as drift

def test_classify_and_citations_helpers() -> None:
    clf = drift.classify_files(
        {"a.java": "1", "b.java": "2", "c.java": "3"},
        {"a.java": "1", "b.java": "9", "d.java": "4"},
    )
    assert clf["unchanged"] == ["a.java"]
    assert clf["changed"] == ["b.java"]
    assert clf["deleted"] == ["c.java"]
    assert clf["added"] == ["d.java"]

    signals = {
        "evidence": {
            "persistence": [
                {"file": "a.java", "line": 1, "rule_id": "r1"},
            ]
        },
        "entity_table_map": {
            "Foo": {"file": "Foo.java", "line": 2, "table": "FOO"},
        },
        "file_signatures": {"a.java": "1"},
        "repo_path": "/r",
    }
    cites = list(drift.all_citations(signals))
    assert any(s.startswith("evidence.") for s, _ in cites)
    assert any(s.startswith("entity_table_map.") for s, _ in cites)
    by_file = drift._group_citations_by_file(signals)
    assert "a.java" in by_file
    indexed = drift._index_fresh_evidence_by_file(signals)
    assert "a.java" in indexed
    sigs, prov = drift._baseline_signatures_and_provenance(signals, None)
    assert prov["source"] == "spring_signals.json"
    assert sigs == {"a.java": "1"}
    man = {
        "file_signatures": {"x": "y"},
        "run_id": "rid",
        "target_repo": {"path": "/t", "commit_hash": "c", "dirty": False},
    }
    _, prov2 = drift._baseline_signatures_and_provenance(signals, man)
    assert prov2["source"] == "run_manifest.json"
    assert prov2["run_id"] == "rid"
    results = []
    drift._append_uniform_status(
        results, [("evidence.persistence", {"file": "a.java", "line": 1})], "unchanged"
    )
    assert results[0]["status"] == "unchanged"
    report = drift._assemble_drift_report(
        "/repo", signals, prov, clf, list(results)
    )
    assert report["citations_checked"] == 1
    assert report["schema_version"]


def test_load_signals_rejects_old_schema(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "signals.json"
    path.write_text(json.dumps({"schema_version": 1}), encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        drift.load_signals(str(path))
    assert exc.value.code == 1


def test_empty_signatures_and_manifest_validate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    data = {"target_repo": {"path": str(empty)}, "file_signatures": {}}
    monkeypatch.setattr(drift.spring_signal_scan, "dfs_walk", lambda _p: [])
    assert drift._empty_signatures_are_legitimate(data) is True
    assert drift._empty_signatures_are_legitimate({"target_repo": {}}) is False

    with pytest.raises(SystemExit):
        drift._validate_manifest_baseline(str(tmp_path / "m.json"), {"status": "ok"})
    with pytest.raises(SystemExit):
        drift._validate_manifest_baseline(
            str(tmp_path / "m.json"),
            {"file_signatures": {}, "status": "running", "target_repo": {"path": str(empty)}},
        )
    # Empty signatures + empty repo is accepted.
    drift._validate_manifest_baseline(
        str(tmp_path / "m.json"),
        {"file_signatures": {}, "status": "complete", "target_repo": {"path": str(empty)}},
    )
    assert "empty-repo baseline" in capsys.readouterr().err

    ctx = SimpleNamespace(file_signatures={"A.java": "sig"})
    assert drift.tier1_scan("/unused", scan_context=ctx) == {"A.java": "sig"}


def test_stage4_pool_helpers_and_compare() -> None:
    edges = {"groups": {"g1": {"a": 1}, "g2": {"b": list(range(50))}}}
    dist = cap.estimate_stage1_slice_tokens(edges)
    assert dist["max"] >= dist["mean"]
    assert dist["total"] >= dist["max"]
    assert cap._json_est_tokens(None) == 0
    assert cap._json_est_tokens({"k": "v"}) >= 1

    proxy = cap.estimate_stage4_shared_pool_tokens(
        {"groups": [{"est_tokens": 10}, {"est_tokens": 5}]},
        signals_data={"n": 1},
    )
    assert proxy["metric_kind"] == "partial_proxy_pre_stage4"
    assert proxy["summaries_est_tokens"] == 15
    assert proxy["signals_omitted"] is False

    measured = cap.measure_stage4_shared_pool_tokens(
        {"summaries": [1]},
        interview_answers={"q": "a"},
        signals_data=None,
    )
    assert measured["metric_kind"] == "measured_stage4_inputs"
    assert measured["interview_answers_omitted"] is False
    assert measured["signals_omitted"] is True
    with pytest.raises(ValueError):
        cap.measure_stage4_shared_pool_tokens(None)

    cmp = cap.compare_stage4_proxy_to_measured(proxy, measured)
    assert cmp["measured_over_proxy_ratio"] is not None
    fields = cap._stage4_pool_fields(measured)
    assert fields["stage4_metric_kind"] == "measured_stage4_inputs"
    warn = cap._stage4_shared_pool_warning(measured, threshold=0)
    assert warn is not None
    assert cap._stage4_shared_pool_warning(measured, threshold=10**9) is None
    fan = cap._stage_fanout_for_groups(3)
    assert fan["stage1_file_summarizer"] == 3
    assert fan["stage4_doc_writer"] == cap.STAGE4_FIXED_FANOUT
    included, omitted = cap._measured_included_omitted(True, True)
    assert "summaries" in included
    assert "interview_answers" in omitted
