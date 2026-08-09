"""query_artifacts evidence/routes query envelopes."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from doc_engine.query.envelope import QUERY_RESULT_SCHEMA_VERSION, apply_limit
from doc_engine.query.handlers import dependents, entity, evidence, facts, routes
from doc_engine.query.load import QueryError, QueryMissingError, QueryPathError, load_json, load_jsonl
from doc_engine.query.registry import get_query_handler, run_query
from doc_engine.real_fixture import real_artifacts_dir
FIXTURE_SIGNALS = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    / "fixtures"
    / "spring_signals"
)
from tests.support.query_artifacts.factories import _signals_doc, _facts_rows

def test_apply_limit_sets_truncated_when_rows_exceed_cap() -> None:
    """Deviation: uncapped dumps blow agent context (DDIA backpressure)."""
    rows = [{"i": i} for i in range(10)]
    out, truncated = apply_limit(rows, 3)
    assert len(out) == 3
    assert truncated is True


def test_apply_limit_clamps_absurd_limit() -> None:
    """Deviation: huge --limit bypasses the hard ceiling."""
    from doc_engine.query.envelope import MAX_LIMIT

    rows = [{"i": i} for i in range(MAX_LIMIT + 50)]
    out, truncated = apply_limit(rows, 10_000_000)
    assert len(out) == MAX_LIMIT
    assert truncated is True


def test_run_query_envelope_always_has_schema_and_truncated() -> None:
    """Deviation: bare list without envelope (agents cannot tell freshness/cap)."""
    result = run_query(
        "evidence",
        signals=_signals_doc(),
        bucket="persistence",
        limit=50,
    )
    assert result["schema_version"] == QUERY_RESULT_SCHEMA_VERSION
    assert "truncated" in result
    assert "rows" in result
    assert result["kind"] == "evidence"


def test_evidence_filters_by_bucket_and_rule_id() -> None:
    """Deviation: returns every bucket when --bucket/--rule-id asked."""
    rows = evidence.query_evidence(
        _signals_doc(),
        bucket="api_surface",
        rule_id="api_surface__controller",
    )
    assert len(rows) == 1
    assert rows[0]["rule_id"] == "api_surface__controller"


def test_evidence_filters_by_file_substring() -> None:
    """Deviation: file filter ignored — agents re-read whole signals."""
    rows = evidence.query_evidence(
        _signals_doc(),
        bucket="persistence",
        file_contains="User.java",
    )
    assert len(rows) == 1
    assert "User.java" in rows[0]["file"]


def test_routes_defaults_to_api_surface_bucket() -> None:
    """Deviation: routes dumps persistence/security with api_surface."""
    rows = routes.query_routes(_signals_doc(), path_contains="/api/a")
    assert len(rows) == 1
    assert "/api/a" in (rows[0].get("match") or "")


def test_facts_filter_by_predicate_and_fqcn() -> None:
    """Deviation: facts query cannot find MAPS_TO by FQCN."""
    rows = facts.query_facts(
        _facts_rows(),
        predicate="MAPS_TO",
        fqcn="com.example.domain.User",
    )
    assert len(rows) == 1
    assert rows[0]["object"] == "users"


def test_entity_returns_contested_with_candidates() -> None:
    """Deviation: contested entity collapsed to unique or drops candidates."""
    rows = entity.query_entity(_signals_doc(), class_name="Order")
    assert len(rows) == 1
    assert rows[0]["status"] == "contested"
    assert len(rows[0]["candidates"]) == 2


def test_entity_lookup_by_table() -> None:
    """Deviation: table lookup misses unique entity_table_map entry."""
    rows = entity.query_entity(_signals_doc(), table="users")
    assert len(rows) == 1
    assert rows[0]["class_name"] == "User"


def test_dependents_finds_importers_of_type() -> None:
    """Deviation: dependents misses exact import arcs (LLM re-does the join)."""
    rows = dependents.query_dependents(
        _signals_doc(),
        target_file="src/User.java",
    )
    assert any(r.get("from") == "src/AController.java" and r.get("to") == "src/User.java" for r in rows)
    assert all(r.get("confidence") in ("exact", "package-fanout") for r in rows)


def test_route_trace_joins_api_surface_with_same_file_security() -> None:
    """Deviation: route_trace returns mappings without co-located security hits."""
    from doc_engine.query.handlers import route_trace

    rows = route_trace.query_route_trace(_signals_doc(), path_contains="/api/a")
    assert len(rows) >= 1
    row = rows[0]
    assert "guards" in row
    assert any("PreAuthorize" in (g.get("match") or "") for g in row["guards"])


def test_load_json_missing_file_raises_not_empty_success(tmp_path: Path) -> None:
    """Deviation: missing artifact returns empty rows (false absence)."""
    with pytest.raises(QueryMissingError):
        load_json(tmp_path / "nope.json", root=tmp_path)


def test_load_json_requires_root(tmp_path: Path) -> None:
    """Deviation: C1 — opt-in containment (root=None allowed)."""
    p = tmp_path / "x.json"
    p.write_text("{}", encoding="utf-8")
    with pytest.raises(QueryPathError):
        load_json(p, root=None)


def test_load_json_invalid_raises(tmp_path: Path) -> None:
    """Deviation: corrupt JSON treated as empty success."""
    p = tmp_path / "bad.json"
    p.write_text("{not-json", encoding="utf-8")
    with pytest.raises(QueryError):
        load_json(p, root=tmp_path)
