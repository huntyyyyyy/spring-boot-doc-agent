"""Coverage climb: executors and query handler hard-stops."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from doc_engine.pipeline import executor as executor_mod
from doc_engine.pipeline import local_run as local_run_mod
from doc_engine.pipeline.context import PipelineContext
from doc_engine.query import registry as query_registry
from doc_engine.query.load import QueryError, QueryMissingError
from doc_engine.scanning import java_extract as jx
from doc_engine.scanning import stage0_siblings as siblings
from doc_engine.scanning._scanner_registry import (
    get_scanner,
    resolve_scanner_names,
)
from doc_engine.tools import gap_probe as gap_probe_mod
from stf.runners import implement as implement_mod
from stf.validators import lint_tasks as lint_mod
from tests.stf.conftest import build_minimal_valid_spec, build_minimal_valid_tasks
from tests.support.coverage_climb.tier2_context import _ctx

def test_subprocess_runner_file_not_found_and_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runner = executor_mod.SubprocessStageRunner()
    ctx = _ctx(tmp_path)

    def _missing(*_a, **_k):
        raise FileNotFoundError("gone")

    monkeypatch.setattr(executor_mod.subprocess, "run", _missing)
    bad = runner.run(["nope"], ctx)
    assert bad.success is False
    assert "gone" in (bad.error or "")

    def _timeout(*_a, **_k):
        raise subprocess.TimeoutExpired(cmd="x", timeout=1)

    monkeypatch.setattr(executor_mod, "tool_timeout_seconds", lambda: 1)
    monkeypatch.setattr(executor_mod.subprocess, "run", _timeout)
    timed = runner.run(["sleep"], ctx)
    assert timed.success is False
    assert timed.error == "subprocess timed out"


def test_mock_and_http_executors(tmp_path: Path) -> None:
    ctx = _ctx(tmp_path)
    mock = executor_mod.MockStageExecutor(
        {
            "ok": lambda _c: "done",
            "boom": lambda _c: (_ for _ in ()).throw(RuntimeError("x")),
        }
    )
    assert mock.run_generative("missing", ctx).success is False
    assert mock.run_generative("ok", ctx).detail == "done"
    assert mock.run_generative("boom", ctx).success is False
    http = executor_mod.HttpLLMStageExecutor()
    assert "not implemented" in (http.run_generative("s1", ctx).error or "")


def test_local_run_delegates_to_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(local_run_mod, "main", lambda argv: 7 if argv == ["--help"] else 0)
    assert local_run_mod.run(["--help"]) == 7
    assert local_run_mod.run(None) == 0


def test_load_signals_rejects_non_object(tmp_path: Path) -> None:
    path = tmp_path / "signals.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(QueryError, match="JSON object"):
        query_registry._load_signals(None, path, tmp_path)


def test_load_facts_and_edges_from_paths(tmp_path: Path) -> None:
    facts = tmp_path / "facts.jsonl"
    facts.write_text('{"a":1}\n', encoding="utf-8")
    assert query_registry._load_facts(None, facts, tmp_path) == [{"a": 1}]
    edges = tmp_path / "edges.json"
    edges.write_text('{"n":[]}', encoding="utf-8")
    assert query_registry._load_edges(None, edges, tmp_path) == {"n": []}
    edges.write_text("[]", encoding="utf-8")
    assert query_registry._load_edges(None, edges, tmp_path) is None


def test_invoke_handlers_require_artifacts() -> None:
    with pytest.raises(QueryMissingError, match="signals"):
        query_registry._invoke_signals_handler(
            lambda *_a, **_k: [], accepts_edges=False, sig=None, ed=None, filters={}
        )
    with pytest.raises(QueryMissingError, match="facts"):
        query_registry._invoke_facts_handler(lambda *_a, **_k: [], None, {})

    spec = SimpleNamespace(
        handler=lambda **filters: [{"k": filters.get("file")}],
        requires_signals=False,
        requires_facts=False,
        accepts_edges=False,
    )
    rows = query_registry._invoke_handler(
        spec, sig=None, fr=None, ed=None, filters={"file": "a.java"}
    )
    assert rows[0]["k"] == "a.java"

    edged = SimpleNamespace(
        handler=lambda sig, edges=None, **filters: [{"edges": edges is not None}],
        requires_signals=True,
        requires_facts=False,
        accepts_edges=True,
    )
    assert query_registry._invoke_signals_handler(
        edged.handler, accepts_edges=True, sig={}, ed={"e": 1}, filters={}
    )[0]["edges"] is True


def test_extras_for_kind_hard_stops() -> None:
    dep = query_registry._extras_for_kind("dependents", False)
    assert "hard_stops" in dep
    rt = query_registry._extras_for_kind("route_trace", True)
    assert rt["nested_truncated"] is True
    assert "hard_stops" in rt


def test_scanner_registry_unknown_and_dedupe() -> None:
    with pytest.raises(ValueError, match="unknown scanner"):
        get_scanner("nope")
    with pytest.raises(ValueError, match="unknown scanner"):
        resolve_scanner_names(["filesystem", "nope"])
    assert resolve_scanner_names([]) == ["filesystem", "ast-grep"]
    assert resolve_scanner_names(["filesystem", "filesystem", "ast-grep"]) == [
        "filesystem",
        "ast-grep",
    ]
