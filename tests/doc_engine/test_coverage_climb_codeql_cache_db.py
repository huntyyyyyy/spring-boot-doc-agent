"""Coverage climb: CodeQL invoke/version/cache/database helpers."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import doc_engine.scanning.support._codeql_cache as cache_mod
import doc_engine.scanning.support._codeql_cli as cli_mod
import doc_engine.scanning.support._codeql_queries as queries_mod
from doc_engine.scanning.support import _codeql_runner as runner

pytestmark = pytest.mark.domain_climb_sensor

def test_find_codeql_rejects_missing_env_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOC_ENGINE_CODEQL", str(Path("/no/such/codeql-binary")))
    with pytest.raises(runner.CodeQLNotFoundError, match="not an existing file"):
        runner.find_codeql()

def test_resolve_codeql_exe_rejects_directory(tmp_path: Path) -> None:
    d = tmp_path / "not-a-file"
    d.mkdir()
    with pytest.raises(runner.CodeQLError, match="not a file"):
        runner._resolve_codeql_exe(d)

def test_reject_unsafe_option_empty() -> None:
    with pytest.raises(runner.CodeQLError, match="non-empty"):
        runner._reject_unsafe_option("")

def test_invoke_codeql_timeout_wraps(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")

    def _raise(*_a, **_k):
        raise subprocess.TimeoutExpired(cmd="codeql", timeout=1)

    monkeypatch.setattr(cli_mod.subprocess, "run", _raise)
    with pytest.raises(runner.CodeQLError, match="timed out"):
        runner._invoke_codeql(fake, ("--version",), timeout=1)

def test_codeql_version_nonzero_and_success(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setattr(
        cli_mod,
        "_invoke_codeql",
        lambda *a, **k: MagicMock(returncode=1, stdout="", stderr="boom"),
    )
    with pytest.raises(runner.CodeQLError, match="--version failed"):
        runner.codeql_version(fake)
    monkeypatch.setattr(
        cli_mod,
        "_invoke_codeql",
        lambda *a, **k: MagicMock(
            returncode=0,
            stdout="CodeQL command-line toolchain release 2.20.0.\n",
            stderr="",
        ),
    )
    assert runner.codeql_version(fake) == "2.20.0"

def test_version_token_no_digit_after_release() -> None:
    assert runner._version_token_from_line("release only words") is None

def test_cache_base_dir_xdg_and_fallback(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    assert runner._cache_base_dir() == tmp_path / "xdg"
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.setattr(cache_mod.sys, "platform", "linux")
    monkeypatch.setattr(cache_mod.Path, "home", classmethod(lambda cls: tmp_path / "home"))
    assert runner._cache_base_dir() == tmp_path / "home" / ".cache"

def test_hash_one_walk_file_skips_outside_and_oserror(
    tmp_path: Path, monkeypatch
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    inside = repo / "A.java"
    inside.write_text("class A {}", encoding="utf-8")
    h = MagicMock()
    runner._hash_one_walk_file(
        h, repo, str(repo.resolve()), inside, lambda *_: False
    )
    h.update.assert_not_called()

    def _boom(_self=None):
        raise OSError("io")

    monkeypatch.setattr(Path, "read_bytes", _boom)
    runner._hash_one_walk_file(
        h, repo, str(repo.resolve()), inside, lambda *_: True
    )

def test_cache_metadata_and_validity(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    db = tmp_path / "db"
    db.mkdir()
    assert runner._cache_metadata(db) is None
    runner._write_cache_metadata(db, repo, pack, "gradlew compileJava", codeql_cli_version="2.0")
    assert runner._cache_is_valid(db, repo, pack, "gradlew compileJava", codeql_cli_version="2.0")
    assert not runner._cache_is_valid(
        db, repo, pack, "gradlew compileJava", codeql_cli_version="2.1"
    )
    bad = db / "spring_signal_scan_cache.json"
    bad.write_text("{not-json", encoding="utf-8")
    assert runner._cache_metadata(db) is None

def test_results_cache_roundtrip_and_corrupt(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    rows = [{"file": "A.java", "line": 1}]
    runner._save_results_cache(
        repo, pack, "gradlew compileJava", "sv1", rows, codeql_cli_version="2.0"
    )
    loaded = runner._load_results_cache(
        repo, pack, "gradlew compileJava", "sv1", codeql_cli_version="2.0"
    )
    assert loaded == rows
    path = runner._results_cache_path(
        repo, pack, "gradlew compileJava", "sv1", codeql_cli_version="2.0"
    )
    path.write_text("[]not-json", encoding="utf-8")
    assert (
        runner._load_results_cache(
            repo, pack, "gradlew compileJava", "sv1", codeql_cli_version="2.0"
        )
        is None
    )

def test_create_database_and_install_pack_failures(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setattr(
        cli_mod,
        "_invoke_codeql",
        lambda *a, **k: MagicMock(returncode=2, stdout="out", stderr="err"),
    )
    with pytest.raises(runner.CodeQLError, match="database create failed"):
        runner.create_database(
            fake, tmp_path / "repo", tmp_path / "db", "gradlew compileJava"
        )
    with pytest.raises(runner.CodeQLError, match="pack install failed"):
        runner.install_pack(fake, tmp_path / "pack")

def test_run_query_and_decode_failures(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setattr(
        cli_mod,
        "_invoke_codeql",
        lambda *a, **k: MagicMock(returncode=3, stdout="", stderr="bad"),
    )
    with pytest.raises(runner.CodeQLError, match="query run failed"):
        runner.run_query(fake, tmp_path / "db", tmp_path / "q.ql", tmp_path / "out.bqrs")
    with pytest.raises(runner.CodeQLError, match="bqrs decode failed"):
        runner.decode_bqrs(fake, tmp_path / "out.bqrs")

def test_decode_bqrs_success(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    payload = {
        "#select": {
            "columns": [{"name": "file"}, {"kind": "String"}],
            "tuples": [["a.java", "x"]],
        }
    }
    monkeypatch.setattr(
        cli_mod,
        "_invoke_codeql",
        lambda *a, **k: MagicMock(returncode=0, stdout=json.dumps(payload), stderr=""),
    )
    rows = runner.decode_bqrs(fake, tmp_path / "out.bqrs")
    assert rows == [{"file": "a.java", "col_1": "x"}]

def test_run_all_queries_empty_and_merge(tmp_path: Path, monkeypatch) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    with pytest.raises(runner.CodeQLError, match="no .ql queries"):
        runner.run_all_queries(tmp_path / "codeql", tmp_path / "db", pack, tmp_path)
    (pack / "one.ql").write_text("// q", encoding="utf-8")
    monkeypatch.setattr(queries_mod, "run_query", lambda *a, **k: None)
    monkeypatch.setattr(
        queries_mod, "decode_bqrs", lambda *a, **k: [{"file": "a.java"}]
    )
    rows = runner.run_all_queries(tmp_path / "codeql", tmp_path / "db", pack, tmp_path)
    assert rows[0]["_query_file"] == "one.ql"
