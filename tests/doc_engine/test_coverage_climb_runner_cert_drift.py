"""Coverage climb: runner gates, certification helpers, drift."""

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
from doc_engine.pipeline.local_runner_phases.artifact_inventory import (
    artifact_inventory,
)
from doc_engine.pipeline.local_runner_phases.certification_finish import (
    certification_failure_summary,
    emit_certification_outcome,
    write_certification_and_finish,
)
from doc_engine.pipeline.local_runner_phases.drift_check_phase import run_drift_check
from doc_engine.pipeline.local_runner_phases.runner import Runner
from doc_engine.pipeline.local_runner_phases.runner_argv import py_mod
from doc_engine.pipeline.local_runner_phases.runner_log import (
    Log,
    reconfigure_stdio_utf8,
)
from doc_engine.pipeline.local_runner_phases.stage_recording import (
    classify_subprocess_status,
    gate_status_from_runner_status,
    quote,
    record_pipeline_stage_results,
)
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

def test_gate_and_subprocess_status_helpers() -> None:
    assert gate_status_from_runner_status("OK") == "ok"
    assert gate_status_from_runner_status("SKIPPED") == "skipped"
    assert gate_status_from_runner_status("FAIL") == "fail"
    assert classify_subprocess_status(0, gate=True) == "OK"
    assert classify_subprocess_status(1, gate=True) == "FAIL"
    assert classify_subprocess_status(1, gate=False) == "NONZERO"

def test_reconfigure_stdio_handles_missing_and_errors(monkeypatch) -> None:
    class _NoReconfigure:
        pass

    class _Boom:
        def reconfigure(self, **_kwargs):
            raise OSError("nope")

    monkeypatch.setattr(sys, "stdout", _NoReconfigure())
    monkeypatch.setattr(sys, "stderr", _Boom())
    reconfigure_stdio_utf8()

def test_runner_record_gate_and_abort(tmp_path: Path) -> None:
    log = Log(tmp_path / "run.log")
    try:
        runner_obj = Runner(log, keep_going=False)
        runner_obj._record_gate("g1", "label", "OK", "detail")
        assert runner_obj.gate_records[0].status == "ok"
        runner_obj._mark_critical_abort("stage0")
        assert runner_obj.aborted is True
        runner_obj.aborted = False
        runner_obj._abort_on_critical_spawn_failure(critical=True)
        assert runner_obj.aborted is True
    finally:
        log.close()

def test_runner_spawn_error_and_timeout(tmp_path: Path, monkeypatch) -> None:
    log = Log(tmp_path / "run.log")
    try:
        runner_obj = Runner(log, keep_going=False)
        runner_obj._handle_spawn_exception(
            "step",
            started=0.0,
            timeout=1.0,
            exc=subprocess.TimeoutExpired(cmd="x", timeout=1),
            gate=True,
            gate_id="g1",
            critical=True,
        )
        assert runner_obj.results[-1][1] == "ERROR"
        assert runner_obj.aborted is True

        runner_obj.aborted = False
        monkeypatch.setattr(
            runner_obj,
            "_spawn_step_process",
            lambda *a, **k: MagicMock(returncode=1, stdout="o", stderr="e"),
        )
        proc = runner_obj.run("fail-crit", ["false"], gate=True, gate_id="g2", critical=True)
        assert proc is not None
        assert runner_obj.aborted is True

        runner_obj.aborted = True
        assert runner_obj.run("skipped", ["true"]) is None
        assert runner_obj.results[-1][1] == "SKIPPED"
    finally:
        log.close()

def test_runner_mock_success_and_error(tmp_path: Path) -> None:
    log = Log(tmp_path / "run.log")
    try:
        runner_obj = Runner(log, keep_going=False)
        assert runner_obj.mock("m1", lambda: "ok-detail") == "ok-detail"
        assert runner_obj.results[-1][1] == "MOCK"
        assert runner_obj.mock("m2", lambda: (_ for _ in ()).throw(ValueError("x"))) is None
        assert runner_obj.aborted is True
        assert runner_obj.mock("m3", lambda: "never") is None
    finally:
        log.close()

def test_spawn_step_process_file_not_found(tmp_path: Path, monkeypatch) -> None:
    log = Log(tmp_path / "run.log")
    try:
        runner_obj = Runner(log, keep_going=True)

        def _raise(*_a, **_k):
            raise FileNotFoundError("missing")

        import doc_engine.pipeline.local_runner_phases.runner_spawn as runner_spawn

        monkeypatch.setattr(runner_spawn.subprocess, "run", _raise)
        monkeypatch.setattr(runner_spawn, "tool_timeout_seconds", lambda: 5)
        assert (
            runner_obj._spawn_step_process(
                "x",
                ["nope"],
                cwd=None,
                env=None,
                started=0.0,
                gate=False,
                gate_id=None,
                critical=False,
            )
            is None
        )
        assert runner_obj.results[-1][1] == "ERROR"
    finally:
        log.close()

def test_record_pipeline_stage_results() -> None:
    runner_obj = SimpleNamespace(results=[], aborted=False)

    def _record(label, status, seconds, detail=""):
        runner_obj.results.append((label, status, seconds, detail))

    runner_obj.record = _record
    ok = SimpleNamespace(success=True, detail="d", error=None)
    bad = SimpleNamespace(success=False, detail="", error="e")
    record_pipeline_stage_results(
        runner_obj, [("s1", ok), ("s2", bad)], ok_status="OK"
    )
    assert runner_obj.results[0][1] == "OK"
    assert runner_obj.results[1][1] == "FAIL"
    assert runner_obj.aborted is True

def test_certification_helpers(tmp_path: Path, monkeypatch) -> None:
    log = Log(tmp_path / "run.log")
    try:
        runner_obj = Runner(log, keep_going=True)
        runner_obj.record("pipeline:a", "FAIL", 0.1, "x")
        runner_obj._record_gate("g1", "gate", "FAIL", "bad")
        report = SimpleNamespace(
            certified=False,
            stages=[SimpleNamespace(name="a", status="fail")],
        )
        assert "stages:" in certification_failure_summary(runner_obj, report)
        emit_certification_outcome(log, runner_obj, report, None, None)
        good = SimpleNamespace(certified=True, stages=[])
        emit_certification_outcome(
            log, runner_obj, good, ["RESULT: ok"], ["note"]
        )
    finally:
        log.close()

def test_run_drift_check_skip_and_default(tmp_path: Path, monkeypatch) -> None:
    log = Log(tmp_path / "run.log")
    try:
        runner_obj = Runner(log, keep_going=True)
        args = SimpleNamespace(skip_drift=True, prior_signals=None)
        run_drift_check(
            log, runner_obj, str(tmp_path), "m.json", str(tmp_path), args, "sig.json"
        )
        assert runner_obj.results == []

        calls = []
        monkeypatch.setattr(
            runner_obj, "run", lambda *a, **k: calls.append(a[0]) or MagicMock()
        )
        args = SimpleNamespace(skip_drift=False, prior_signals=None)
        run_drift_check(
            log, runner_obj, str(tmp_path), "m.json", str(tmp_path), args, "sig.json"
        )
        assert calls == ["spring_drift_check"]
    finally:
        log.close()

def test_quote_and_py_mod() -> None:
    assert quote("a b") == '"a b"'
    assert quote("ab") == "ab"
    assert py_mod("pkg.mod", "--flag")[1:3] == ["-m", "pkg.mod"]

def test_artifact_inventory(tmp_path: Path) -> None:
    out = tmp_path / "out"
    out.mkdir()
    (out / "a.txt").write_text("hi", encoding="utf-8")
    log = Log(tmp_path / "run.log")
    try:
        artifact_inventory(log, str(out))
    finally:
        log.close()
