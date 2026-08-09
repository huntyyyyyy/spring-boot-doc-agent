"""Coverage climb: CodeQL exe resolve, invoke, cache, prepare/cleanup."""
from __future__ import annotations
from pathlib import Path
from types import SimpleNamespace
import pytest
from doc_engine.scanning.support import _codeql_cli as cli_mod
from doc_engine.scanning.support import _codeql_runner as runner
pytestmark = pytest.mark.domain_climb_sensor

def _test_cache_metadata_and_results_roundtrip_prelude(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv('XDG_CACHE_HOME', str(tmp_path / 'xdg'))
    pack = tmp_path / 'pack'
    pack.mkdir()
    (pack / 'a.ql').write_text('// q', encoding='utf-8')
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'A.java').write_text('class A {}', encoding='utf-8')
    db = tmp_path / 'db'
    db.mkdir()
    runner._write_cache_metadata(db, repo, pack, './gradlew compileJava', codeql_cli_version='2.0')
    assert runner._cache_is_valid(db, repo, pack, './gradlew compileJava', codeql_cli_version='2.0')
    assert not runner._cache_is_valid(db, repo, pack, './gradlew compileJava', codeql_cli_version='9.9')
    assert runner._cache_metadata(tmp_path / 'missing-db') is None
    rows = [{'file': 'A.java', 'line': 1}]
    runner._save_results_cache(repo, pack, './gradlew compileJava', 'sv1', rows, codeql_cli_version='2.0')
    loaded = runner._load_results_cache(repo, pack, './gradlew compileJava', 'sv1', codeql_cli_version='2.0')
    return loaded, rows

def _test_cache_metadata_and_results_roundtrip_core(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, loaded, rows):
    assert loaded == rows
    with pytest.raises(runner.CodeQLError, match='not a list'):
        runner._validate_cached_evidence_rows({'file': 'x'})
    with pytest.raises(runner.CodeQLError, match='missing file'):
        runner._validate_cached_evidence_rows([{'line': 1}])

def _test_prepare_scan_and_cleanup_prelude(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv('XDG_CACHE_HOME', str(tmp_path / 'xdg'))
    pack = tmp_path / 'pack'
    pack.mkdir()
    (pack / 'q.ql').write_text('//', encoding='utf-8')
    repo = tmp_path / 'repo'
    repo.mkdir()
    resolved, db, using, keep = runner._prepare_scan_targets(repo, './gradlew compileJava', pack, None, False, None, '2.0')
    assert resolved == pack
    assert using is True
    assert keep is True
    assert db.parent.is_dir()
    with pytest.raises(runner.CodeQLError, match='query pack not found'):
        runner._prepare_scan_targets(repo, './gradlew compileJava', tmp_path / 'no-pack', None, False, None, '2.0')
    db2 = tmp_path / 'explicit-db'
    db2.mkdir()
    tmp = tmp_path / 'tmp'
    return db2, pack, repo, tmp

def _test_prepare_scan_and_cleanup_core(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, db2, pack, repo, tmp):
    tmp.mkdir()
    runner._cleanup_scan_temps(db2, str(tmp), keep_database=False)
    assert not db2.exists()
    assert not tmp.exists()
    assert runner._load_cached_scan_rows(using_cache=False, scanner_version='sv', repo_path=repo, pack_dir=pack, build_command='./gradlew compileJava', scan_context=None, cli_version='2.0') is None
    assert runner._is_codeql_hash_file('build.gradle')
    assert runner._is_codeql_walk_filename('Foo.java')
    dirs = ['.git', 'src', 'build']
    runner._prune_hash_walk_dirs(dirs)
    assert dirs == ['src']

def test_reject_unsafe_and_resolve_exe(tmp_path: Path) -> None:
    with pytest.raises(runner.CodeQLError, match='non-empty'):
        runner._reject_unsafe_option('')
    with pytest.raises(runner.CodeQLError, match='single-line'):
        runner._reject_unsafe_option('bad\nopt')
    missing = tmp_path / 'nope'
    with pytest.raises(runner.CodeQLError, match='not a file'):
        runner._resolve_codeql_exe(missing)
    fake = tmp_path / 'codeql'
    fake.write_text('', encoding='utf-8')
    assert runner._resolve_codeql_exe(fake) == fake.resolve()

def test_invoke_codeql_rejects_and_timeout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake = tmp_path / 'codeql'
    fake.write_text('', encoding='utf-8')
    with pytest.raises(runner.CodeQLError, match='non-allowlisted'):
        runner._invoke_codeql(fake, ('database', 'delete'), timeout=1)
    import subprocess

    def boom(*a, **k):
        raise subprocess.TimeoutExpired(cmd='codeql', timeout=1)
    monkeypatch.setattr(cli_mod.subprocess, 'run', boom)
    with pytest.raises(runner.CodeQLError, match='timed out'):
        runner._invoke_codeql(fake, ('--version',), timeout=1)

def test_find_codeql_env_and_missing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv('DOC_ENGINE_CODEQL', raising=False)
    monkeypatch.setattr(cli_mod.shutil, 'which', lambda _n: None)
    with pytest.raises(runner.CodeQLNotFoundError):
        runner.find_codeql()
    bad = tmp_path / 'missing-bin'
    monkeypatch.setenv('DOC_ENGINE_CODEQL', str(bad))
    with pytest.raises(runner.CodeQLNotFoundError, match='not an existing'):
        runner.find_codeql()
    good = tmp_path / 'cq'
    good.write_text('', encoding='utf-8')
    monkeypatch.setenv('DOC_ENGINE_CODEQL', str(good))
    assert runner.find_codeql() == good

def test_cache_metadata_and_results_roundtrip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    loaded, rows = _test_cache_metadata_and_results_roundtrip_prelude(tmp_path, monkeypatch)
    _test_cache_metadata_and_results_roundtrip_core(tmp_path, monkeypatch, loaded, rows)

def test_prepare_scan_and_cleanup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db2, pack, repo, tmp = _test_prepare_scan_and_cleanup_prelude(tmp_path, monkeypatch)
    _test_prepare_scan_and_cleanup_core(tmp_path, monkeypatch, db2, pack, repo, tmp)

def test_ensure_regular_file_and_codeql_version(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    d = tmp_path / 'dir'
    d.mkdir()
    with pytest.raises(runner.CodeQLError, match='non-regular'):
        runner._ensure_regular_file(d)
    fake = tmp_path / 'codeql'
    fake.write_text('', encoding='utf-8')
    monkeypatch.setattr(cli_mod, '_invoke_codeql', lambda *a, **k: SimpleNamespace(returncode=0, stdout='CodeQL command-line toolchain release 2.20.0.\n'))
    assert runner.codeql_version(fake) == '2.20.0'
    monkeypatch.setattr(cli_mod, '_invoke_codeql', lambda *a, **k: SimpleNamespace(returncode=1, stderr='boom', stdout=''))
    with pytest.raises(runner.CodeQLError, match='--version failed'):
        runner.codeql_version(fake)
