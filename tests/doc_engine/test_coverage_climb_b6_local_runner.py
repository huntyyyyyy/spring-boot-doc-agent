"""Coverage climb B6: local_runner facade + stage0 abort/success.

Q2 adequacy witness: mutmut_slice on doc_engine.pipeline.local_runner and
local_runner_phases.stage0 — asserts bite setup int early-return, phase abort
certification, and CLI main argv wiring (not line-touch padding).
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.pipeline import local_runner as lr
from doc_engine.pipeline.compliance import ComplianceProfile
from doc_engine.pipeline.local_runner_phases import stage0 as stage0_mod

pytestmark = pytest.mark.domain_climb_sensor


def test_run_pipeline_setup_int_and_phase_short_circuit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(lr, "phase_setup", lambda _args: 2)
    assert lr.run_pipeline(SimpleNamespace()) == 2

    state = SimpleNamespace(token="setup-ok")
    calls: list[str] = []

    def boom(_state: object) -> int:
        calls.append("build")
        return 7

    monkeypatch.setattr(lr, "phase_setup", lambda _args: state)
    monkeypatch.setattr(lr, "phase_build_context", boom)
    monkeypatch.setattr(lr, "phase_stage0", lambda _s: calls.append("stage0") or None)
    assert lr.run_pipeline(SimpleNamespace()) == 7
    assert calls == ["build"]


def test_main_parses_argv(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[object] = []

    def fake_run(args: object) -> int:
        seen.append(args)
        return 3

    monkeypatch.setattr(lr, "run_pipeline", fake_run)
    assert lr.main([str(Path("/tmp/repo")), "--skip-drift", "--allow-mock"]) == 3
    assert seen and seen[0].skip_drift is True
    assert seen[0].allow_mock is True


def test_phase_stage0_success_and_abort(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    recorded: list[object] = []

    class FakeLog:
        def rule(self, msg: str) -> None:
            recorded.append(f"rule:{msg}")

    class FakeOuterRunner:
        def __init__(self) -> None:
            self.aborted = False

    class FakeDetRunner:
        def __init__(self, *a: object, **k: object) -> None:
            recorded.append("det_runner")

        def run(self, ctx: object) -> list[str]:
            recorded.append(ctx)
            return ["ok"]

    monkeypatch.setattr(stage0_mod, "PipelineRunner", FakeDetRunner)
    monkeypatch.setattr(
        stage0_mod,
        "record_pipeline_stage_results",
        lambda runner, results, ok_status="OK": recorded.append(
            (ok_status, list(results))
        ),
    )
    finish_calls: list[dict] = []

    def fake_finish(*_a: object, **kwargs: object) -> int:
        finish_calls.append(dict(kwargs))
        return 9

    monkeypatch.setattr(stage0_mod, "write_certification_and_finish", fake_finish)

    ok_runner = FakeOuterRunner()
    state_ok = SimpleNamespace(
        log=FakeLog(),
        runner=ok_runner,
        pipeline_ctx={"repo": str(tmp_path)},
        deterministic_specs=["signal_scan"],
        profile=ComplianceProfile.DETERMINISTIC_ONLY,
        repo_path=str(tmp_path),
        out_dir=str(tmp_path / "out"),
        allow_mock=True,
    )
    assert stage0_mod.phase_stage0(state_ok) is None
    assert any(isinstance(item, tuple) and item[0] == "OK" for item in recorded)

    abort_runner = FakeOuterRunner()
    abort_runner.aborted = True
    state_abort = SimpleNamespace(
        log=FakeLog(),
        runner=abort_runner,
        pipeline_ctx={"repo": str(tmp_path)},
        deterministic_specs=["signal_scan"],
        profile=ComplianceProfile.CERTIFIED,
        repo_path=str(tmp_path),
        out_dir=str(tmp_path / "out2"),
        allow_mock=False,
    )
    assert stage0_mod.phase_stage0(state_abort) == 9
    assert finish_calls
    assert "aborted" in finish_calls[0]["notice_lines"][0]


def test_build_arg_parser_wires_epilog() -> None:
    parser = lr.build_arg_parser()
    assert "run.log" in (parser.epilog or "")
    ns = parser.parse_args([str(Path("/tmp/repo")), "--trust-repo-config"])
    assert ns.trust_repo_config is True
