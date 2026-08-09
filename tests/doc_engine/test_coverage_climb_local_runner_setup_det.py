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

def _test_reuse_signals_sibling_error_and_deterministic_banner_prelude(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    repo = tmp_path / 'repo'
    repo.mkdir()
    out = tmp_path / 'out'
    signals = tmp_path / 'signals.json'
    signals.write_text('[]', encoding='utf-8')
    code = setup_mod.phase_setup(_base_args(repo, out_dir=str(out), signals_file=str(signals)))
    assert code == 2
    assert 'Stage-0 siblings' in capsys.readouterr().err
    out2 = tmp_path / 'out2'
    state = setup_mod.phase_setup(_base_args(repo, out_dir=str(out2), compliance_profile='deterministic_only', docs_in_target_repo=True))
    assert isinstance(state, LocalRunState)
    assert state.profile == ComplianceProfile.DETERMINISTIC_ONLY
    assert state.docs_dir.endswith('docs')
    log_text = Path(state.log.path).read_text(encoding='utf-8')
    assert 'Deterministic stages only' in log_text
    state.log.close()
    return repo

def _test_reuse_signals_sibling_error_and_deterministic_banner_core(tmp_path: Path, capsys: pytest.CaptureFixture[str], repo):
    out3 = tmp_path / 'out3'
    scan = setup_mod.phase_setup(_base_args(repo, out_dir=str(out3), compliance_profile='scan_only'))
    assert isinstance(scan, LocalRunState)
    scan_log = Path(scan.log.path).read_text(encoding='utf-8')
    assert 'Scan-only profile' in scan_log
    scan.log.close()

def _base_args(repo: Path, **overrides):
    values = dict(repo_path=str(repo), out_dir=None, docs_in_target_repo=False, trust_repo_config=False, allow_mock=True, signals_file=None, strict_citations=False, keep_going=False, compliance_profile='certified', deterministic_only=False, until=None, skip_drift=True, prior_signals=None)
    values.update(overrides)
    return SimpleNamespace(**values)

def test_require_repo_dir_and_phase_setup_errors(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    missing = tmp_path / 'nope'
    assert setup_mod._require_repo_dir(str(missing)) == 2
    err = capsys.readouterr().err
    assert 'not a directory' in err
    assert setup_mod.phase_setup(_base_args(missing)) == 2
    repo = tmp_path / 'repo'
    repo.mkdir()
    out = tmp_path / 'out'
    ghost = tmp_path / 'ghost_signals.json'
    code = setup_mod.phase_setup(_base_args(repo, out_dir=str(out), signals_file=str(ghost)))
    assert code == 2
    assert 'not found' in capsys.readouterr().err

def test_reuse_signals_sibling_error_and_deterministic_banner(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo = _test_reuse_signals_sibling_error_and_deterministic_banner_prelude(tmp_path, capsys)
    _test_reuse_signals_sibling_error_and_deterministic_banner_core(tmp_path, capsys, repo)

def test_reuse_signals_success_copies_and_logs(tmp_path: Path) -> None:
    repo = tmp_path / 'repo'
    repo.mkdir()
    out = tmp_path / 'out'
    signals = tmp_path / 'signals.json'
    payload = {'evidence': {}, 'file_signatures': {'A.java': {'sha256': 'abc', 'size': 1}}}
    signals.write_text(json.dumps(payload), encoding='utf-8')
    state = setup_mod.phase_setup(_base_args(repo, out_dir=str(out), signals_file=str(signals)))
    assert isinstance(state, LocalRunState)
    assert state.skip_signal_scan is True
    assert Path(state.signals_path).is_file()
    assert Path(out, 'facts.jsonl').is_file() or Path(out, 'covering_proof.json').is_file()
    log_text = Path(state.log.path).read_text(encoding='utf-8')
    assert 'reused signals' in log_text
    assert 'signal_scan skipped' in log_text
    state.log.close()

def test_phase_deterministic_only_early_exit(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from tests.support.coverage_climb.det_phase_fakes import make_phase_state, patch_det_phase_side_effects
    from doc_engine.pipeline.compliance import ComplianceProfile
    calls: list[str] = []; finish_kwargs: dict = {}
    patch_det_phase_side_effects(monkeypatch, calls, finish_kwargs)
    early = make_phase_state(tmp_path, profile=ComplianceProfile.CERTIFIED, generative_specs=["g"], out_name="", until_stage=None, allow_mock=True, calls=calls)
    early.args = SimpleNamespace(skip_drift=True)
    assert det.phase_deterministic_only(early) is None


def test_phase_deterministic_only_runs_and_until_note(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from tests.support.coverage_climb.det_phase_fakes import make_phase_state, patch_det_phase_side_effects
    from doc_engine.pipeline.compliance import ComplianceProfile
    calls: list[str] = []; finish_kwargs: dict = {}
    patch_det_phase_side_effects(monkeypatch, calls, finish_kwargs)
    state = make_phase_state(tmp_path, profile=ComplianceProfile.DETERMINISTIC_ONLY, generative_specs=["still-ignored"], out_name="out", until_stage="architect", allow_mock=False, calls=calls)
    (tmp_path / "out").mkdir()
    assert det.phase_deterministic_only(state) == 0
    assert "validate_artifacts_all" in calls and "finish" in calls
    assert finish_kwargs.get("success_lines")
    assert "Stopped after --until" not in finish_kwargs["success_lines"][0]
    calls.clear(); finish_kwargs.clear()
    certified = make_phase_state(tmp_path, profile=ComplianceProfile.CERTIFIED, generative_specs=[], out_name="out2", until_stage="gap_analysis_interview", allow_mock=True, calls=calls)
    (tmp_path / "out2").mkdir()
    assert det.phase_deterministic_only(certified) == 0
    assert "Stopped after --until gap_analysis_interview" in finish_kwargs["success_lines"][0]
