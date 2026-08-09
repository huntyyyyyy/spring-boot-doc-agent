"""Coverage climb: STF scan prepare and build-tool runners."""

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

pytestmark = pytest.mark.domain_climb_sensor

def test_scan_prepares_and_runs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(spring_mod, "resolve_scanner_names", lambda _s: ["filesystem"])
    monkeypatch.setattr(
        spring_mod,
        "get_scanner",
        lambda _n: SimpleNamespace(name="filesystem", version_hash=lambda: "v"),
    )
    monkeypatch.setattr(
        "doc_engine.config.repo_trust.require_codeql_build_allowed",
        lambda *_a, **_k: None,
    )
    monkeypatch.setattr(
        spring_mod,
        "_run_spring_scan",
        lambda *a, **k: {"ok": True, "build": k.get("build_command")},
    )
    out = spring_mod.scan(str(tmp_path), scanners=["filesystem"], allow_codeql_build=False)
    assert out["ok"] is True

def test_tool_on_path_misses_all(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(spring_mod.shutil, "which", lambda _n: None)
    assert spring_mod._tool_on_path("gradle", "gradle.bat") is None

def test_gradle_maven_tool_requires_marker_and_binary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert spring_mod._gradle_tool_command(str(tmp_path), "g") is None
    (tmp_path / "build.gradle").write_text("//", encoding="utf-8")
    monkeypatch.setattr(spring_mod, "_tool_on_path", lambda *_n: None)
    assert spring_mod._gradle_tool_command(str(tmp_path), "g") is None
    monkeypatch.setattr(spring_mod, "_tool_on_path", lambda *_n: "C:/gradle")
    assert "gradle" in (spring_mod._gradle_tool_command(str(tmp_path), "g") or "")

    assert spring_mod._maven_tool_command(str(tmp_path), "m") is None
    (tmp_path / "pom.xml").write_text("<project/>", encoding="utf-8")
    monkeypatch.setattr(spring_mod, "_tool_on_path", lambda *_n: None)
    assert spring_mod._maven_tool_command(str(tmp_path), "m") is None
    monkeypatch.setattr(spring_mod, "_tool_on_path", lambda *_n: "C:/mvn")
    assert "mvn" in (spring_mod._maven_tool_command(str(tmp_path), "m") or "")

def test_runner_keep_going_and_quiet_paths(tmp_path: Path) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner = phase_support.Runner(log, keep_going=True)
        runner._mark_critical_abort("stage0")
        assert runner.aborted is False
        runner._log_step_header("q", ["echo", "hi there"], quiet=True)
        runner.mock("m", lambda: (_ for _ in ()).throw(RuntimeError("x")))
        assert runner.aborted is False
        assert any(r[1] == "ERROR" for r in runner.results)
        runner.results.clear()
        runner.record("x", "FAIL", 0.1, "e")
        assert len(runner.gates_failed()) == 1
        runner.table()
    finally:
        log.close()
