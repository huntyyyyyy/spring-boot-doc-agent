"""Coverage climb: CodeQL prepare_scan / run_queries / scan cache."""

from __future__ import annotations

from pathlib import Path

import pytest

import doc_engine.scanning.support._codeql_cache as cache_mod
import doc_engine.scanning.support._codeql_database as db_mod
from doc_engine.scanning.support import _codeql_runner as runner

pytestmark = pytest.mark.domain_climb_sensor

def test_prepare_scan_targets_and_reuse(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    resolved, db, using_cache, keep = runner._prepare_scan_targets(
        repo, "gradlew compileJava", pack, None, False, None, "2.0"
    )
    assert using_cache is True
    assert keep is True
    assert resolved == pack
    assert db.parent.name == "codeql-cache"

    with pytest.raises(runner.CodeQLError, match="query pack not found"):
        runner._prepare_scan_targets(
            repo, "gradlew compileJava", tmp_path / "missing", None, False, None, "2.0"
        )

    created = []

    def _create(*a, **k):
        created.append(True)
        db.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(db_mod, "create_database", _create)
    monkeypatch.setattr(cache_mod, "_cache_is_valid", lambda *a, **k: False)
    runner._reuse_or_rebuild_cached_db(
        codeql_path=tmp_path / "codeql",
        repo_path=repo,
        db_path=db,
        pack_dir=pack,
        build_command="gradlew compileJava",
        using_cache=True,
        scan_context=None,
        cli_version="2.0",
    )
    assert created
    # Caller-provided keep path trusts existing DB.
    created.clear()
    runner._reuse_or_rebuild_cached_db(
        codeql_path=tmp_path / "codeql",
        repo_path=repo,
        db_path=db,
        pack_dir=pack,
        build_command="gradlew compileJava",
        using_cache=False,
        scan_context=None,
        cli_version="2.0",
    )
    assert not created

def test_ensure_database_create_path(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    calls = []
    monkeypatch.setattr(
        db_mod, "create_database", lambda *a, **k: calls.append("create")
    )
    monkeypatch.setattr(
        cache_mod, "_write_cache_metadata", lambda *a, **k: calls.append("meta")
    )
    db = tmp_path / "fresh-db"
    runner._ensure_codeql_database(
        codeql_path=tmp_path / "codeql",
        repo_path=repo,
        db_path=db,
        pack_dir=pack,
        build_command="gradlew compileJava",
        using_cache=True,
        keep_database=True,
        scan_context=None,
        cli_version="2.0",
    )
    assert calls == ["create", "meta"]

def test_run_queries_and_cleanup(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    monkeypatch.setattr(
        runner, "run_all_queries", lambda *a, **k: [{"file": "A.java"}]
    )
    saved = []
    monkeypatch.setattr(
        runner, "_save_results_cache", lambda *a, **k: saved.append(True)
    )
    rows = runner._run_queries_and_maybe_cache(
        codeql_path=tmp_path / "codeql",
        repo_path=repo,
        db_path=tmp_path / "db",
        pack_dir=pack,
        build_command="gradlew compileJava",
        using_cache=True,
        scanner_version="sv",
        scan_context=None,
        cli_version="2.0",
        tmp=tmp_path,
    )
    assert rows and saved
    db = tmp_path / "dbdir"
    db.mkdir()
    tmp = tmp_path / "tmpdir"
    tmp.mkdir()
    runner._cleanup_scan_temps(db, str(tmp), keep_database=False)
    assert not db.exists()
    assert not tmp.exists()

def test_scan_with_codeql_uses_results_cache(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setattr(runner, "find_codeql", lambda: fake)
    monkeypatch.setattr(runner, "codeql_version", lambda _p: "2.0")
    monkeypatch.setattr(
        runner,
        "_load_cached_scan_rows",
        lambda **k: [{"file": "A.java", "cached": True}],
    )
    rows = runner.scan_with_codeql(
        repo,
        "gradlew compileJava",
        pack_dir=pack,
        scanner_version="sv",
    )
    assert rows[0]["cached"] is True
