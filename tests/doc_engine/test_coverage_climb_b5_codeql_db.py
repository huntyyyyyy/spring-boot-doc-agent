"""Coverage climb B5: CodeQL database create / ensure / cache reuse."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

import doc_engine.scanning.support._codeql_cache as cache_mod
import doc_engine.scanning.support._codeql_database as db_mod

pytestmark = pytest.mark.domain_climb_sensor


def test_create_database_without_overwrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    captured: list[tuple] = []

    def _invoke(codeql_path, subcmd, *options, timeout=None):
        captured.append((subcmd, options))
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(db_mod.cli, "_invoke_codeql", _invoke)
    db_mod.create_database(
        fake,
        tmp_path / "repo",
        tmp_path / "db",
        "gradlew compileJava",
        overwrite=False,
    )
    _sub, options = captured[0]
    assert "--overwrite" not in options
    monkeypatch.setattr(
        db_mod.cli,
        "_invoke_codeql",
        lambda *a, **k: SimpleNamespace(returncode=2, stdout="", stderr="fail"),
    )
    with pytest.raises(db_mod.CodeQLError, match="pack install failed"):
        db_mod.install_pack(fake, tmp_path / "pack")


def test_ensure_reuses_existing_keep_database(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    db = tmp_path / "db"
    db.mkdir()
    reuse_calls: list[bool] = []

    def _reuse(**_kwargs):
        reuse_calls.append(True)

    monkeypatch.setattr(db_mod, "_reuse_or_rebuild_cached_db", _reuse)
    db_mod._ensure_codeql_database(
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
    assert reuse_calls == [True]


def test_ensure_writes_meta_and_valid_cache_short_circuit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    created: list[str] = []

    def _create(codeql_path, repo_path, db_path, build_command, overwrite=True):
        created.append("create")
        Path(db_path).mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(db_mod, "create_database", _create)
    fresh = tmp_path / "fresh-db"
    db_mod._ensure_codeql_database(
        codeql_path=tmp_path / "codeql",
        repo_path=repo,
        db_path=fresh,
        pack_dir=pack,
        build_command="gradlew compileJava",
        using_cache=True,
        keep_database=False,
        scan_context=None,
        cli_version="2.0",
    )
    assert created == ["create"]
    assert cache_mod._cache_is_valid(
        fresh, repo, pack, "gradlew compileJava", codeql_cli_version="2.0"
    )
    created.clear()
    db_mod._reuse_or_rebuild_cached_db(
        codeql_path=tmp_path / "codeql",
        repo_path=repo,
        db_path=fresh,
        pack_dir=pack,
        build_command="gradlew compileJava",
        using_cache=True,
        scan_context=None,
        cli_version="2.0",
    )
    assert created == []
