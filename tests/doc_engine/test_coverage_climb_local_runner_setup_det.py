"""Coverage climb B2: setup + deterministic phases; Q2 witness mutmut_slice."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.pipeline.compliance import ComplianceProfile
from doc_engine.pipeline.local_runner_phases import deterministic as det
from doc_engine.pipeline.local_runner_phases import setup as setup_mod
from doc_engine.pipeline.local_runner_phases.state import LocalRunState

pytestmark = pytest.mark.domain_climb_sensor


def _base_args(repo: Path, **overrides):
    values = dict(
        repo_path=str(repo),
        out_dir=None,
        docs_in_target_repo=False,
        trust_repo_config=False,
        allow_mock=True,
        signals_file=None,
        strict_citations=False,
        keep_going=False,
        compliance_profile="certified",
        deterministic_only=False,
        until=None,
        skip_drift=True,
        prior_signals=None,
    )
    values.update(overrides)
    return SimpleNamespace(**values)


def test_require_repo_dir_and_phase_setup_errors(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "nope"
    assert setup_mod._require_repo_dir(str(missing)) == 2
    err = capsys.readouterr().err
    assert "not a directory" in err

    assert setup_mod.phase_setup(_base_args(missing)) == 2

    repo = tmp_path / "repo"
    repo.mkdir()
    out = tmp_path / "out"
    ghost = tmp_path / "ghost_signals.json"
    code = setup_mod.phase_setup(
        _base_args(repo, out_dir=str(out), signals_file=str(ghost))
    )
    assert code == 2
    assert "not found" in capsys.readouterr().err


def test_reuse_signals_sibling_error_and_deterministic_banner(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    out = tmp_path / "out"
    # JSON array fails Stage-0 sibling materialization (root must be object).
    signals = tmp_path / "signals.json"
    signals.write_text("[]", encoding="utf-8")

    code = setup_mod.phase_setup(
        _base_args(repo, out_dir=str(out), signals_file=str(signals))
    )
    assert code == 2
    assert "Stage-0 siblings" in capsys.readouterr().err

    out2 = tmp_path / "out2"
    state = setup_mod.phase_setup(
        _base_args(
            repo,
            out_dir=str(out2),
            compliance_profile="deterministic_only",
            docs_in_target_repo=True,
        )
    )
    assert isinstance(state, LocalRunState)
    assert state.profile == ComplianceProfile.DETERMINISTIC_ONLY
    assert state.docs_dir.endswith("docs")
    log_text = Path(state.log.path).read_text(encoding="utf-8")
    assert "Deterministic stages only" in log_text
    state.log.close()

    out3 = tmp_path / "out3"
    scan = setup_mod.phase_setup(
        _base_args(repo, out_dir=str(out3), compliance_profile="scan_only")
    )
    assert isinstance(scan, LocalRunState)
    scan_log = Path(scan.log.path).read_text(encoding="utf-8")
    assert "Scan-only profile" in scan_log
    scan.log.close()


def test_reuse_signals_success_copies_and_logs(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    out = tmp_path / "out"
    signals = tmp_path / "signals.json"
    payload = {
        "evidence": {},
        "file_signatures": {"A.java": {"sha256": "abc", "size": 1}},
    }
    signals.write_text(json.dumps(payload), encoding="utf-8")
    state = setup_mod.phase_setup(
        _base_args(repo, out_dir=str(out), signals_file=str(signals))
    )
    assert isinstance(state, LocalRunState)
    assert state.skip_signal_scan is True
    assert Path(state.signals_path).is_file()
    assert Path(out, "facts.jsonl").is_file() or Path(out, "covering_proof.json").is_file()
    log_text = Path(state.log.path).read_text(encoding="utf-8")
    assert "reused signals" in log_text
    assert "signal_scan skipped" in log_text
    state.log.close()


def test_phase_deterministic_only_runs_and_until_note(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls: list[str] = []

    class FakeLog:
        def rule(self, msg: str) -> None:
            calls.append(f"rule:{msg}")

        def __call__(self, msg: str = "") -> None:
            calls.append(str(msg))

    class FakeRunner:
        def run(self, name, argv, gate=False, gate_id=None, env=None):
            calls.append(name)
            return 0

    finish_kwargs: dict = {}

    def fake_finish(*_a, **kwargs):
        finish_kwargs.update(kwargs)
        calls.append("finish")
        return 0

    monkeypatch.setattr(
        det.gates,
        "run_gate_via_runner",
        lambda *a, **k: calls.append(k.get("gate_id") or "gate"),
    )
    monkeypatch.setattr(det.gates, "run_validate_all_artifacts", lambda *_a, **_k: None)
    monkeypatch.setattr(det, "_run_drift_check", lambda *_a, **_k: calls.append("drift"))
    monkeypatch.setattr(det, "_artifact_inventory", lambda *_a, **_k: calls.append("inv"))
    monkeypatch.setattr(det, "_write_certification_and_finish", fake_finish)

    # Early exit when certified + generative work remains.
    early = SimpleNamespace(
        profile=ComplianceProfile.CERTIFIED,
        generative_specs=["g"],
        log=FakeLog(),
        runner=FakeRunner(),
        args=SimpleNamespace(skip_drift=True),
        out_dir=str(tmp_path),
        manifest=str(tmp_path / "m.json"),
        signals_path=str(tmp_path / "s.json"),
        preflight_path=str(tmp_path / "p.json"),
        repo_path=str(tmp_path),
        until_stage=None,
        allow_mock=True,
    )
    assert det.phase_deterministic_only(early) is None

    state = SimpleNamespace(
        profile=ComplianceProfile.DETERMINISTIC_ONLY,
        generative_specs=["still-ignored"],
        log=FakeLog(),
        runner=FakeRunner(),
        args=SimpleNamespace(skip_drift=True, prior_signals=None),
        out_dir=str(tmp_path / "out"),
        manifest=str(tmp_path / "m.json"),
        signals_path=str(tmp_path / "s.json"),
        preflight_path=str(tmp_path / "p.json"),
        repo_path=str(tmp_path),
        until_stage="architect",
        allow_mock=False,
    )
    (tmp_path / "out").mkdir()
    assert det.phase_deterministic_only(state) == 0
    assert "validate_artifacts_all" in calls
    assert "run_manifest finalize" in calls
    assert "run_manifest summary" in calls
    assert "drift" in calls and "inv" in calls and "finish" in calls
    # until_note only for CERTIFIED profile
    assert finish_kwargs.get("success_lines")
    assert "Stopped after --until" not in finish_kwargs["success_lines"][0]

    calls.clear()
    finish_kwargs.clear()
    certified = SimpleNamespace(
        profile=ComplianceProfile.CERTIFIED,
        generative_specs=[],
        log=FakeLog(),
        runner=FakeRunner(),
        args=SimpleNamespace(skip_drift=True, prior_signals=None),
        out_dir=str(tmp_path / "out2"),
        manifest=str(tmp_path / "m2.json"),
        signals_path=str(tmp_path / "s2.json"),
        preflight_path=str(tmp_path / "p2.json"),
        repo_path=str(tmp_path),
        until_stage="gap_analysis_interview",
        allow_mock=True,
    )
    (tmp_path / "out2").mkdir()
    assert det.phase_deterministic_only(certified) == 0
    assert "Stopped after --until gap_analysis_interview" in finish_kwargs["success_lines"][0]
