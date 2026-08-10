"""Coverage climb: STF certification finish and plan/wave gates."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any
import pytest
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

def test_emit_certification_with_notice_and_failure(tmp_path: Path) -> None:
    log = Log(tmp_path / "run.log")
    try:
        runner = Runner(log, keep_going=False)
        runner.record("pipeline:s1", "FAIL", 0.0, "boom")
        report = SimpleNamespace(
            certified=False,
            stages=[SimpleNamespace(name="s1", status="fail")],
        )
        emit_certification_outcome(
            log, runner, report, success_lines=["ok"], notice_lines=None
        )
        emit_certification_outcome(
            log,
            runner,
            SimpleNamespace(certified=True, stages=[]),
            success_lines=["done"],
            notice_lines=["note"],
        )
        summary = certification_failure_summary(runner, report)
        assert "stages:" in summary
    finally:
        log.close()

def test_write_certification_finish_uncertified(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    log = Log(tmp_path / "run.log")
    try:
        runner = Runner(log, keep_going=False)
        runner.record("pipeline:s1", "OK", 0.1, "")
        report = SimpleNamespace(certified=False, stages=[])
        monkeypatch.setattr(
            "doc_engine.pipeline.local_runner_phases.certification_finish.build_and_write_certification",
            lambda *a, **k: (report, tmp_path / "certification.json"),
        )
        code = write_certification_and_finish(
            log,
            runner,
            "certified",
            str(tmp_path),
            str(tmp_path),
            "mock",
            allow_mock=True,
            show_table=False,
            success_lines=None,
            notice_lines=["heads-up"],
        )
        assert code == 1
    finally:
        log.close()

def test_run_drift_with_prior_signals(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    log = Log(tmp_path / "run.log")
    try:
        runner = Runner(log, keep_going=True)
        called: list[Any] = []

        def _capture(label, argv, **_k):
            called.append((label, argv))
            return None

        runner.run = _capture  # type: ignore[method-assign]
        prior = tmp_path / "prior.json"
        prior.write_text("{}", encoding="utf-8")
        args = SimpleNamespace(skip_drift=False, prior_signals=str(prior))
        run_drift_check(
            log, runner, str(tmp_path), str(tmp_path / "m.json"), str(tmp_path), args, str(tmp_path / "sig.json")
        )
        assert called and called[0][0] == "spring_drift_check"
        assert str(prior.resolve()) in called[0][1]
    finally:
        log.close()

def test_finding_coverage_requires_critical_inv() -> None:
    tasks = build_minimal_valid_tasks()
    spec = SimpleNamespace(finding_ids=["C99", "N2"])
    assert implement_mod._finding_coverage(tasks, None) is True
    assert implement_mod._finding_coverage(tasks, spec) is False
    tasks.tasks[0].inputs.append({"origin": "INV-C99", "datum": "x"})
    assert implement_mod._finding_coverage(tasks, spec) is True

def test_wrapper_command_present(tmp_path: Path) -> None:
    assert spring_mod._wrapper_command(str(tmp_path), "gradlew", "build") is None
    (tmp_path / "gradlew").write_text("#!/bin/sh\n", encoding="utf-8")
    cmd = spring_mod._wrapper_command(str(tmp_path), "gradlew", "build")
    assert cmd is not None and "gradlew" in cmd
    assert spring_mod._first_wrapper_command(str(tmp_path), ("missing", "gradlew"), "g") is not None
    assert spring_mod._first_wrapper_command(str(tmp_path), ("missing",), "g") is None

def test_plan_gate_fails_on_lint(monkeypatch: pytest.MonkeyPatch) -> None:
    tasks = build_minimal_valid_tasks()
    monkeypatch.setattr(
        implement_mod,
        "lint_tasks_document",
        lambda *_a, **_k: [SimpleNamespace(level="FAIL", name="x")],
    )
    monkeypatch.setattr(
        implement_mod,
        "lint_summary",
        lambda _r: {"ok": False, "fail": 1},
    )
    with pytest.raises(implement_mod.PlanGateError, match="plan gate failed"):
        implement_mod.plan_gate(tasks, None)

def test_run_waves_and_constitution(tmp_path: Path) -> None:
    store = TasksStore(tmp_path)
    store.write_tasks(build_minimal_valid_tasks())
    dry = implement_mod.run_waves(store)
    assert "executed" in dry
    seen: list[str] = []
    store.write_tasks(build_minimal_valid_tasks())
    live = implement_mod.run_waves(store, task_fn=seen.append, max_concurrent=2)
    assert sorted(seen) == sorted(live["executed"])
    (tmp_path / "CONSTRAINTS.md").write_text("c", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("l", encoding="utf-8")
    text = implement_mod.constitution_excerpts(tmp_path, max_chars=100)
    assert "CONSTRAINTS.md" in text and "CLAUDE.md" in text

def test_append_blocker_stalls(tmp_path: Path) -> None:
    store = TasksStore(tmp_path)
    store.write_tasks(build_minimal_valid_tasks())
    blocker = implement_mod.append_blocker(
        store,
        title="blocked",
        falsified="assumption",
        evidence="e",
        class_=BlockerClass.DECISION,
        falsified_tasks=["T0"],
    )
    assert blocker.id.startswith("B")
    assert store.load_tasks().ledger.value == "stall"

def test_mutate_tasks_modes() -> None:
    tasks = build_minimal_valid_tasks()
    for mode in ("bad-dep", "no-phase", "bad-inventory", "no-acceptance", "bad-blocker", "cycle"):
        mutated = lint_mod.mutate_tasks(tasks, mode)
        assert mutated is not tasks
    with pytest.raises(ValueError, match="unknown mutate mode"):
        lint_mod.mutate_tasks(tasks, "nope")
