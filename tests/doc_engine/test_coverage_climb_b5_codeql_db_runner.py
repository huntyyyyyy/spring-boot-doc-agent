"""Coverage climb B5: CodeQL database reuse + scan_with_codeql facade."""

from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

import doc_engine.scanning.support._codeql_cache as cache_mod
import doc_engine.scanning.support._codeql_database as db_mod
from doc_engine.scanning.support import _codeql_runner as runner

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
    # Valid cache: reuse returns without rebuild.
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


def test_scan_with_codeql_runs_queries_and_caches(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
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
    monkeypatch.setattr(runner, "install_pack", lambda *_a, **_k: None)
    monkeypatch.setattr(
        runner,
        "_ensure_codeql_database",
        lambda **_k: None,
    )
    monkeypatch.setattr(
        runner,
        "run_all_queries",
        lambda *_a, **_k: [{"file": "A.java"}],
    )
    rows = runner.scan_with_codeql(
        repo,
        "gradlew compileJava",
        pack_dir=pack,
        scanner_version="sv1",
    )
    assert rows == [{"file": "A.java"}]
    loaded = runner._load_results_cache(
        repo, pack, "gradlew compileJava", "sv1", codeql_cli_version="2.0"
    )
    assert loaded == rows


def test_load_cached_scan_rows_requires_version_and_main(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    repo = tmp_path / "repo"
    repo.mkdir()
    assert (
        runner._load_cached_scan_rows(
            using_cache=True,
            scanner_version=None,
            repo_path=repo,
            pack_dir=pack,
            build_command="gradlew compileJava",
            scan_context=None,
            cli_version="2.0",
        )
        is None
    )
    monkeypatch.setattr(sys, "argv", ["_codeql_runner"])
    monkeypatch.delitem(
        sys.modules, "doc_engine.scanning.support._codeql_runner", raising=False
    )
    with pytest.raises(SystemExit) as exc:
        runpy.run_module(
            "doc_engine.scanning.support._codeql_runner",
            run_name="__main__",
        )
    assert exc.value.code == 1
    # Success __main__ path: exec the block with a stubbed scan (fresh module
    # namespace would ignore monkeypatch on the imported runner binding).
    monkeypatch.setattr(
        sys,
        "argv",
        ["_codeql_runner", str(repo), "gradlew compileJava"],
    )
    src = Path(runner.__file__).read_text(encoding="utf-8")
    block = src.split('if __name__ == "__main__":', 1)[1]
    exec(
        "if True:\n" + block,
        {
            "__name__": "__main__",
            "sys": sys,
            "Path": Path,
            "json": json,
            "scan_with_codeql": lambda *_a, **_k: [{"file": "X.java"}],
        },
    )
    assert "row_count" in capsys.readouterr().out
