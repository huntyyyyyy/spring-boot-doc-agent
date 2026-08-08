"""Second-tier coverage climb for remaining high-gap modules."""

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


def _ctx(tmp_path: Path) -> PipelineContext:
    out = tmp_path / "out"
    docs = out / "docs"
    out.mkdir(exist_ok=True)
    docs.mkdir(exist_ok=True)
    return PipelineContext(
        repo_path=tmp_path,
        out_dir=out,
        manifest_path=out / "run_manifest.json",
        docs_dir=docs,
        python="python",
        today="2026-08-08",
        respect_gitignore=False,
        max_tokens=120000,
        log=lambda _msg: None,
    )


# --- executor.py ------------------------------------------------------------


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


# --- local_run.py -----------------------------------------------------------


def test_local_run_delegates_to_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(local_run_mod, "main", lambda argv: 7 if argv == ["--help"] else 0)
    assert local_run_mod.run(["--help"]) == 7
    assert local_run_mod.run(None) == 0


# --- query/registry.py ------------------------------------------------------


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


# --- scanner registry + stage0 siblings + java_extract ----------------------


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


def test_stage0_siblings_errors_and_copy(tmp_path: Path) -> None:
    with pytest.raises(siblings.Stage0SiblingError, match="not found"):
        siblings._load_signals_mapping(tmp_path / "missing.json")
    bad = tmp_path / "signals.json"
    bad.write_text("[]", encoding="utf-8")
    with pytest.raises(siblings.Stage0SiblingError, match="JSON object"):
        siblings._load_signals_mapping(bad)

    src = tmp_path / "src"
    src.mkdir()
    signals = {
        "file_signatures": {"a.java": "sig"},
        "scanner_version": "v1",
        "evidence": {},
    }
    (src / "spring_signals.json").write_text(json.dumps(signals), encoding="utf-8")
    (src / "facts.jsonl").write_text("{}\n", encoding="utf-8")
    (src / "covering_proof.json").write_text("{}", encoding="utf-8")
    out = tmp_path / "out"
    siblings.materialize_stage0_siblings(src / "spring_signals.json", out)
    assert (out / "facts.jsonl").is_file()
    assert (out / "covering_proof.json").is_file()


def test_stage0_siblings_synthesize_when_missing(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    signals = {"file_signatures": {"a.java": "sig"}, "evidence": {}}
    (src / "spring_signals.json").write_text(json.dumps(signals), encoding="utf-8")
    out = tmp_path / "out"
    siblings.materialize_stage0_siblings(src / "spring_signals.json", out)
    assert (out / "facts.jsonl").is_file()
    proof = json.loads((out / "covering_proof.json").read_text(encoding="utf-8"))
    assert proof


def test_java_extract_edge_paths(tmp_path: Path) -> None:
    assert jx.first_line_match("") == ""
    assert jx.first_line_match("  hello\nworld") == "hello"
    assert jx.read_source_lines(str(tmp_path), "missing.java", 1) == ""
    empty = tmp_path / "Empty.java"
    empty.write_text("", encoding="utf-8")
    assert jx.read_source_lines(str(tmp_path), "Empty.java", 1) == ""
    assert jx.read_source_lines(str(tmp_path), "Empty.java", 0) == ""
    assert jx._explicit_table_name("@Table(schema=\"x\")") is None
    assert jx.extract_entity("A.java", "package com.ex;") is None
    outside = jx.normalize_repo_path(str(tmp_path / "repo"), str(tmp_path / "other" / "A.java"))
    assert outside.replace("\\", "/").endswith("other/A.java")


def test_lint_anchor_and_locate(tmp_path: Path) -> None:
    assert lint_mod._anchor_rel("plain") is None
    assert lint_mod._anchor_rel("src/foo.java") == "src/foo.java"
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "foo.java").write_text("x", encoding="utf-8")
    results: list = []
    check = lint_mod._make_check(results)
    t = SimpleNamespace(id="T1", locate="src/foo.java src/missing.py")
    lint_mod._lint_locate_anchors(t, tmp_path, check)
    assert any(r.level == "FAIL" and "missing.py" in r.name for r in results)


# --- gap_probe CLI validation -----------------------------------------------


def test_gap_probe_validate_paths(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    args = SimpleNamespace(
        repo=tmp_path,
        signals=tmp_path / "missing-signals.json",
        facts=tmp_path / "missing-facts.jsonl",
    )
    assert gap_probe_mod._validate_input_paths(args) == 2
    err = capsys.readouterr().err
    assert "reserved" in err
    assert "signals not found" in err

    signals = tmp_path / "signals.json"
    signals.write_text("{}", encoding="utf-8")
    args.signals = signals
    assert gap_probe_mod._validate_input_paths(args) == 2
    assert "facts not found" in capsys.readouterr().err

    facts = tmp_path / "facts.jsonl"
    facts.write_text("{}\n", encoding="utf-8")
    args.facts = facts
    args.repo = None
    assert gap_probe_mod._validate_input_paths(args) is None


def test_gap_probe_main_path_error(tmp_path: Path) -> None:
    rc = gap_probe_mod.main(
        [
            "--signals",
            str(tmp_path / "no.json"),
            "--facts",
            str(tmp_path / "no.jsonl"),
            "--out",
            str(tmp_path / "out"),
        ]
    )
    assert rc == 2


# --- stf implement + lint_tasks ---------------------------------------------


def test_verify_gate_dry_and_live() -> None:
    dry = implement_mod.verify_gate(verify_commands=["true", "echo hi"])
    assert dry["ok"] is True
    assert dry["results"][0]["dry_run"] is True
    with pytest.raises(implement_mod.VerifyGateError):
        implement_mod.verify_gate(
            verify_commands=["ok", "bad"],
            runner=lambda cmd: 0 if cmd == "ok" else 2,
        )
    ok = implement_mod.verify_gate(
        verify_commands=["a", "b"],
        runner=lambda _cmd: 0,
    )
    assert ok["ok"] is True


def test_plan_gate_and_finding_coverage() -> None:
    tasks = build_minimal_valid_tasks()
    spec = build_minimal_valid_spec()
    result = implement_mod.plan_gate(tasks, spec)
    assert result["ok"] is True
    assert result["finding_coverage"] is True


def test_run_wave_concurrent_and_dry() -> None:
    executed: list[str] = []
    implement_mod._run_wave_dry(["T0", "T1"], executed)
    assert executed == ["T0", "T1"]
    executed.clear()
    seen: list[str] = []

    def _fn(tid: str) -> None:
        seen.append(tid)

    implement_mod._run_wave_concurrent(
        ["T0", "T1"],
        task_fn=_fn,
        max_concurrent=2,
        executed=executed,
    )
    assert sorted(seen) == ["T0", "T1"]
    assert sorted(executed) == ["T0", "T1"]


def test_lint_one_origin_empty_skipped() -> None:
    results: list = []
    check = lint_mod._make_check(results)
    lint_mod._lint_one_origin(
        SimpleNamespace(id="T1"),
        "",
        known_tasks=set(),
        inventory=set(),
        spec=None,
        check=check,
    )
    assert results == []
