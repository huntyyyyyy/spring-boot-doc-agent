"""Coverage climb: packet/freshness protocols and MCP props."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping
from unittest.mock import MagicMock
import pytest
from doc_engine.core import excludes as excludes_mod
from doc_engine.core import timeouts as timeouts_mod
from doc_engine.query import kinds as kinds_mod
from doc_engine.query.protocols import FreshnessPolicy, PacketProvider
from doc_engine.scanning import spring as spring_mod
from doc_engine.scanning._scanner_codeql import CodeQLBackend
from doc_engine.scanning.support import _codeql_runner as runner
import doc_engine.scanning.support._codeql_cache as cache_mod
import doc_engine.scanning.support._codeql_cli as cli_mod
import doc_engine.scanning.support._codeql_database as db_mod
import doc_engine.scanning.support._codeql_queries as queries_mod

pytestmark = pytest.mark.domain_climb_sensor

class _StubPacket:
    name = "stub"

    def provide(
        self,
        request: str,
        *,
        signals: Mapping[str, Any],
        facts_rows: list[Mapping[str, Any]],
        run_dir: Path,
        limit: int,
    ) -> list[dict[str, Any]]:
        return [{"path": "a.java", "reason": request, "limit": limit}]

class _StubFreshness:
    def freshness_for(self, rel_path: str | None) -> str:
        return "unknown" if not rel_path else "live"

def test_packet_provider_protocol_runtime_checkable(tmp_path: Path) -> None:
    stub = _StubPacket()
    assert isinstance(stub, PacketProvider)
    items = stub.provide(
        "need",
        signals={},
        facts_rows=[],
        run_dir=tmp_path,
        limit=3,
    )
    assert items[0]["reason"] == "need"

def test_freshness_policy_protocol_runtime_checkable() -> None:
    stub = _StubFreshness()
    assert isinstance(stub, FreshnessPolicy)
    assert stub.freshness_for(None) == "unknown"
    assert stub.freshness_for("a.java") == "live"

def test_env_seconds_rejects_non_integer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOC_ENGINE_TOOL_TIMEOUT", "not-an-int")
    with pytest.raises(ValueError, match="integer"):
        timeouts_mod.tool_timeout_seconds()

def test_env_seconds_rejects_non_positive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOC_ENGINE_CODEQL_TIMEOUT", "0")
    with pytest.raises(ValueError, match="positive"):
        timeouts_mod.codeql_database_timeout_seconds()

def test_env_seconds_blank_uses_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOC_ENGINE_TOOL_TIMEOUT", "   ")
    assert timeouts_mod.tool_timeout_seconds() == 600

def test_load_gitignore_returns_none_without_file(tmp_path: Path) -> None:
    assert excludes_mod.load_gitignore_spec(str(tmp_path)) is None

def test_load_gitignore_returns_none_when_pathspec_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".gitignore").write_text("*.class\n", encoding="utf-8")
    real_import = __import__

    def _fake_import(name, *args, **kwargs):
        if name == "pathspec":
            raise ImportError("no pathspec")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", _fake_import)
    assert excludes_mod.load_gitignore_spec(str(tmp_path)) is None

def test_mcp_input_properties_signal_fact_edge_filters() -> None:
    full = kinds_mod.QueryKindSpec(
        kind="dependents",
        handler=lambda **_: [],
        requires_signals=True,
        requires_facts=True,
        accepts_edges=True,
        filter_keys=("file", "type"),
    ).mcp_input_properties()
    assert set(full) >= {"signals", "facts", "edges", "file", "type", "limit"}
    assert full["limit"] == {"type": "integer"}

    lean = kinds_mod.QueryKindSpec(
        kind="facts",
        handler=lambda **_: [],
        requires_signals=False,
        requires_facts=True,
    ).mcp_input_properties()
    assert "signals" not in lean
    assert "facts" in lean
    assert "edges" not in lean
