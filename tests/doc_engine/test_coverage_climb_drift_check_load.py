"""Coverage climb B4: spring_drift_check load / check_drift / CLI.

Q2 witness: mutmut_slice on doc_engine.tools.spring_drift_check (not Arm-1).
"""
from __future__ import annotations
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from doc_engine.tools import spring_drift_check as drift
pytestmark = pytest.mark.domain_climb_sensor
_EMPTY_REPORT = {'file_signatures_baseline': {'source': 'spring_signals.json'}, 'citations_checked': 0, 'status_counts': {}, 'file_summary': {'unchanged': [], 'changed': [], 'deleted': [], 'added': []}}

def _test_cli_validate_and_main_errors_prelude(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'a.java').write_text('class A {}', encoding='utf-8')
    signals_path = tmp_path / 'signals.json'
    signals_path.write_text(json.dumps(_signals_with_cite('a.java')), encoding='utf-8')
    out = tmp_path / 'drift.json'
    man = tmp_path / 'man.json'
    man.write_text(json.dumps({'status': 'complete', 'file_signatures': {'a.java': 'x'}, 'target_repo': {'path': str(repo)}}), encoding='utf-8')
    drift._validate_drift_cli_paths(SimpleNamespace(repo_path=str(repo), signals_path=str(signals_path), manifest=str(man)))
    monkeypatch.setattr(drift, 'check_drift', lambda *a, **k: dict(_EMPTY_REPORT))
    monkeypatch.setattr('sys.argv', ['spring_drift_check', str(repo), str(signals_path), '--out', str(out)])
    drift.main()
    assert out.is_file() and 'Citations checked' in capsys.readouterr().out
    monkeypatch.setattr(drift, 'check_drift', MagicMock(side_effect=drift.spring_signal_scan.CodeQLScannerError('cq')))
    with pytest.raises(SystemExit) as exc:
        drift.main()

def _test_cli_validate_and_main_errors_core(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    assert exc.value.code == 1 and 'cq' in capsys.readouterr().err
    monkeypatch.setattr(drift, 'check_drift', lambda *a, **k: dict(_EMPTY_REPORT))
    monkeypatch.setattr(drift, 'checked_output_path', MagicMock(side_effect=drift.PathValidationError('bad out')))
    with pytest.raises(SystemExit):
        drift.main()
    assert 'bad out' in capsys.readouterr().err

def _signals_with_cite(file_rel: str='a.java') -> dict:
    return {'schema_version': 2, 'repo_path': '/r', 'file_signatures': {file_rel: 'sig1'}, 'evidence': {'sec': [{'file': file_rel, 'line': 1, 'rule_id': 'security__secured', 'match': '@Secured'}]}, 'entity_table_map': {}, 'config_key_sets': {}, 'scanners': ['filesystem']}

def test_load_signals_and_manifest_ok(tmp_path: Path) -> None:
    signals_path = tmp_path / 'signals.json'
    signals_path.write_text(json.dumps({'schema_version': 2, 'file_signatures': {'a.java': 'x'}, 'evidence': {}}), encoding='utf-8')
    assert drift.load_signals(str(signals_path))['schema_version'] == 2
    man_path = tmp_path / 'run_manifest.json'
    man_path.write_text(json.dumps({'status': 'complete', 'file_signatures': {'a.java': 'x'}, 'target_repo': {'path': str(tmp_path)}}), encoding='utf-8')
    assert drift.load_manifest(str(man_path))['file_signatures']['a.java'] == 'x'
    with pytest.raises(SystemExit):
        drift._validate_manifest_baseline(str(man_path), {'file_signatures': {}, 'status': 'complete', 'target_repo': {'path': str(tmp_path / 'missing-repo')}})

def test_tier1_scan_walk_and_oserror(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    target = tmp_path / 'f.java'
    target.write_text('class F {}', encoding='utf-8')

    def fake_walk(_repo: str):
        yield str(target)
        yield str(tmp_path / 'gone.java')
    monkeypatch.setattr(drift.spring_signal_scan, 'dfs_walk', fake_walk)

    def fake_sig(path: str) -> str:
        if path.endswith('gone.java'):
            raise OSError('missing')
        return 'ok'
    monkeypatch.setattr(drift.spring_signal_scan, 'compute_file_signature', fake_sig)
    assert drift.tier1_scan(str(tmp_path))['f.java'] == 'ok'
    assert 'could not read' in capsys.readouterr().err

def test_check_drift_fast_path_and_full(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    java = tmp_path / 'a.java'
    java.write_text('class A {}\n', encoding='utf-8')
    signals = _signals_with_cite('a.java')
    signals['file_signatures'] = {'a.java': drift.spring_signal_scan.compute_file_signature(str(java))}
    report = drift.check_drift(str(tmp_path), signals)
    assert report['citations_checked'] == 1
    assert report['results'][0]['status'] == drift.STATUS_UNCHANGED
    signals2 = _signals_with_cite('a.java')
    signals2['file_signatures'] = {'a.java': 'stale'}
    monkeypatch.setattr(drift.spring_signal_scan, 'scan', lambda *a, **k: {'evidence': {'sec': [{'file': 'a.java', 'line': 1, 'rule_id': 'security__secured', 'match': '@Secured'}]}, 'entity_table_map': {}})
    report2 = drift.check_drift(str(tmp_path), signals2)
    assert report2['file_summary']['changed'] == ['a.java']
    assert report2['results'][0]['status'] == drift.STATUS_CONFIRMED

def test_cli_validate_and_main_errors(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    _test_cli_validate_and_main_errors_prelude(tmp_path, monkeypatch, capsys)
    _test_cli_validate_and_main_errors_core(tmp_path, monkeypatch, capsys)
