"""Coverage climb: mcp_tools pin/dispatch + gap_probe lineage helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.query import mcp_tools as mcp
from doc_engine.query.load import QueryError, QueryPathError
from doc_engine.scanning.gap_probe import lineage as lin

pytestmark = pytest.mark.domain_climb_sensor

def test_pin_path_and_help(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "root"
    root.mkdir()
    inside = root / "run"
    inside.mkdir()
    assert mcp._pin_path(inside, root=root) == inside.resolve()
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(QueryPathError, match="escapes"):
        mcp._pin_path(outside, root=root)
    help_ = mcp._dispatch_help()
    assert "tools" in help_ and help_["tools"]
    monkeypatch.setattr(mcp, "_server_root", lambda: root)
    assert mcp.dispatch_tool("doc_engine_help")["tools"]
    with pytest.raises(QueryError, match="unknown"):
        mcp.dispatch_tool("no_such_tool")

def test_dispatch_query_runners_mocked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "root"
    root.mkdir()
    signals = root / "signals.json"
    signals.write_text("{}", encoding="utf-8")
    facts = root / "facts.jsonl"
    facts.write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(mcp, "_server_root", lambda: root)
    seen: list[str] = []

    def fake_run(kind, **kwargs):
        seen.append(kind)
        return {"kind": kind, "ok": True}

    monkeypatch.setattr(mcp, "run_query", fake_run)
    assert mcp.dispatch_tool("query_evidence", {"signals": str(signals)})["ok"]
    assert mcp.dispatch_tool("query_facts", {"facts": str(facts)})["ok"]
    assert mcp.dispatch_tool("query_entity", {"signals": str(signals)})["ok"]
    assert mcp.dispatch_tool(
        "query_routes", {"signals": str(signals), "path_contains": "/api"}
    )["ok"]
    assert mcp.dispatch_tool(
        "query_route_trace", {"signals": str(signals)}
    )["ok"]
    assert "evidence" in seen and "facts" in seen

def test_lineage_reason_and_null_outcome() -> None:
    assert lin._lineage_reason_class(None) == "unavailable_unknown"
    assert lin._lineage_reason_class("InvalidSyntaxException here") == "dialect_or_syntax"
    assert lin._lineage_reason_class("contested mapping") == "contested_refuse"
    assert lin._lineage_reason_class("entity not found") == "entity_lookup"
    assert lin._lineage_reason_class("other") == "unavailable_other"
    assert lin._reason_mentions("Foo BAR", "bar")
    stratum, ok, failure, tax = lin._null_query_outcome(
        {"file": "a.java", "line": 1},
        query_kind="jpql",
        scoring_env=lin.SCORING_ENV_CALLABLE,
    )
    assert stratum == "null_query" and ok is False and tax == "null_query"
    assert failure["stratum"] == "null_query"
    stratum2, _, _, _ = lin._null_query_outcome(
        {"file": "a.java", "line": 1},
        query_kind="native",
        scoring_env=lin.SCORING_ENV_POOLED,
    )
    assert stratum2 == "native"
    dom = lin._dominant_failure_stratum(
        {"failure_taxonomy": {"entity_lookup": 3, "null_query": 9, "other": 1}}
    )
    assert dom is not None and dom["reason_class"] == "entity_lookup"
