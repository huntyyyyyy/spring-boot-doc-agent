"""Coverage climb: query load/root/artifact/envelope path edges."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any
import pytest
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

pytestmark = pytest.mark.domain_climb_sensor

def test_require_server_root_env_and_blank(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("DOC_ENGINE_ROOT", raising=False)
    monkeypatch.delenv("DOC_ENGINE_RUN_DIR", raising=False)
    with pytest.raises(load_mod.QueryPathError, match="must be set"):
        load_mod.require_server_root()
    monkeypatch.setenv("DOC_ENGINE_ROOT", "   ")
    with pytest.raises(load_mod.QueryPathError, match="must be set"):
        load_mod.require_server_root()
    monkeypatch.setenv("DOC_ENGINE_ROOT", str(tmp_path))
    assert load_mod.require_server_root() == tmp_path.resolve()

def test_resolve_oserror_and_escape(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(load_mod.QueryPathError, match="containment root is required"):
        load_mod._resolve(tmp_path / "a.json", root=None)

    target = tmp_path / "a.json"
    target.write_text("{}", encoding="utf-8")
    real_resolve = Path.resolve

    def _boom(self, *a, **k):
        if self.name == "a.json":
            raise OSError("boom")
        return real_resolve(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", _boom)
    with pytest.raises(load_mod.QueryPathError, match="cannot resolve path"):
        load_mod._resolve(target, root=tmp_path)
    monkeypatch.setattr(Path, "resolve", real_resolve)

    outside = tmp_path.parent / "outside-artifact.json"
    outside.write_text("{}", encoding="utf-8")
    with pytest.raises(load_mod.QueryPathError, match="escapes root"):
        load_mod._resolve(outside, root=tmp_path)

def test_read_artifact_nul_and_missing(tmp_path: Path) -> None:
    nul = tmp_path / "bad.json"
    nul.write_bytes(b'{"a":1}\x00')
    with pytest.raises(load_mod.QueryError, match="NUL"):
        load_mod._read_artifact_text(nul, kind="JSON")
    missing = tmp_path / "gone.jsonl"
    with pytest.raises(load_mod.QueryMissingError):
        load_mod.load_jsonl(missing, root=tmp_path)

def test_jsonl_rejects_non_object_row(tmp_path: Path) -> None:
    path = tmp_path / "rows.jsonl"
    path.write_text("[1]\n", encoding="utf-8")
    with pytest.raises(load_mod.QueryError, match="must be object"):
        load_mod.load_jsonl(path, root=tmp_path)

def test_schema_path_unknown_and_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(load_mod.QueryError, match="unknown envelope"):
        schema_mod.schema_path("nope")
    monkeypatch.setattr(schema_mod, "_SCHEMA_DIR", tmp_path)
    with pytest.raises(load_mod.QueryError, match="schema missing"):
        schema_mod.schema_path("query_result")

def test_validate_envelope_kind_mismatches() -> None:
    with pytest.raises(load_mod.QueryError, match="context-packet"):
        schema_mod._check_kind_specific(
            "context_packet", {"kind": "wrong", "schema_version": 1}
        )
    with pytest.raises(load_mod.QueryError, match="must be a list"):
        schema_mod._check_kind_specific("query_result", {"rows": {}})

def test_list_mcp_tools_and_unknown_kind() -> None:
    names = kinds_mod.list_mcp_tool_names()
    assert "doc_engine_help" in names
    assert "query_evidence" in names
    with pytest.raises(KeyError, match="unknown query kind"):
        kinds_mod.get_query_kind_spec("not-a-kind")

def test_clamp_budget_edges() -> None:
    assert packet_mod._clamp_budget(None) == packet_mod.DEFAULT_BUDGET_TOKENS
    assert packet_mod._clamp_budget(-5) == 0
    assert packet_mod._clamp_budget(packet_mod.MAX_BUDGET_TOKENS + 99) == packet_mod.MAX_BUDGET_TOKENS

def test_resolve_run_missing_and_escape(tmp_path: Path) -> None:
    with pytest.raises(load_mod.QueryMissingError, match="missing run dir"):
        packet_mod._resolve_run_under_root(tmp_path / "nope", tmp_path)
    run = tmp_path / "run"
    run.mkdir()
    other = tmp_path / "other"
    other.mkdir()
    with pytest.raises(load_mod.QueryPathError, match="escapes root"):
        packet_mod._resolve_run_under_root(run, other)

def test_load_run_artifacts_rejects_non_object(tmp_path: Path) -> None:
    run = tmp_path / "run"
    run.mkdir()
    (run / "spring_signals.json").write_text("[]", encoding="utf-8")
    with pytest.raises(load_mod.QueryError, match="must be an object"):
        packet_mod._load_run_artifacts(run, tmp_path)
