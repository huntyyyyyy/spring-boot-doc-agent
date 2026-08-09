"""Coverage climb B5: CodeQL scan_with_codeql facade + __main__."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

import pytest

import doc_engine.scanning.support._codeql_cli as cli_mod
import doc_engine.scanning.support._codeql_database as db_mod
import doc_engine.scanning.support._codeql_queries as queries_mod
from doc_engine.scanning.support import _codeql_runner as runner

pytestmark = pytest.mark.domain_climb_sensor


def _patch_scan_deps(
    monkeypatch: pytest.MonkeyPatch, *, fake: Path, rows: list[dict]
) -> None:
    monkeypatch.setattr(cli_mod, "find_codeql", lambda: fake)
    monkeypatch.setattr(cli_mod, "codeql_version", lambda _p: "2.0")
    monkeypatch.setattr(db_mod, "install_pack", lambda *_a, **_k: None)
    monkeypatch.setattr(db_mod, "_ensure_codeql_database", lambda **_k: None)
    monkeypatch.setattr(queries_mod, "run_all_queries", lambda *_a, **_k: rows)


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
    monkeypatch.setattr(runner, "_ensure_codeql_database", lambda **_k: None)
    monkeypatch.setattr(
        runner, "run_all_queries", lambda *_a, **_k: [{"file": "A.java"}]
    )
    rows = runner.scan_with_codeql(
        repo, "gradlew compileJava", pack_dir=pack, scanner_version="sv1"
    )
    assert rows == [{"file": "A.java"}]
    loaded = runner._load_results_cache(
        repo, pack, "gradlew compileJava", "sv1", codeql_cli_version="2.0"
    )
    assert loaded == rows


def test_validated_build_and_queries_skip_cache_without_version(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(runner.CodeQLError):
        runner._validated_build_command("rm -rf /")
    monkeypatch.setattr(
        runner, "run_all_queries", lambda *_a, **_k: [{"file": "A.java"}]
    )
    saved: list[bool] = []
    monkeypatch.setattr(
        runner, "_save_results_cache", lambda *_a, **_k: saved.append(True)
    )
    rows = runner._run_queries_and_maybe_cache(
        codeql_path=tmp_path / "codeql",
        repo_path=tmp_path / "repo",
        db_path=tmp_path / "db",
        pack_dir=tmp_path / "pack",
        build_command="gradlew compileJava",
        using_cache=True,
        scanner_version=None,
        scan_context=None,
        cli_version="2.0",
        tmp=tmp_path,
    )
    assert rows and not saved


def test_main_usage_and_scan_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
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
    _patch_scan_deps(monkeypatch, fake=fake, rows=[{"file": "Y.java"}])
    # Force pack path via prepare when db_path is explicit (using_cache False).
    monkeypatch.setattr(
        db_mod,
        "_prepare_scan_targets",
        lambda *_a, **_k: (pack, tmp_path / "db", False, True),
    )
    monkeypatch.setattr(sys, "argv", ["_codeql_runner"])
    monkeypatch.delitem(
        sys.modules, "doc_engine.scanning.support._codeql_runner", raising=False
    )
    with pytest.raises(SystemExit) as exc:
        runpy.run_module(
            "doc_engine.scanning.support._codeql_runner", run_name="__main__"
        )
    assert exc.value.code == 1
    monkeypatch.setattr(
        sys,
        "argv",
        ["_codeql_runner", str(repo), "gradlew compileJava", str(tmp_path / "db")],
    )
    monkeypatch.delitem(
        sys.modules, "doc_engine.scanning.support._codeql_runner", raising=False
    )
    runpy.run_module("doc_engine.scanning.support._codeql_runner", run_name="__main__")
    assert "row_count" in capsys.readouterr().out


def test_load_cached_scan_rows_requires_version() -> None:
    assert (
        runner._load_cached_scan_rows(
            using_cache=True,
            scanner_version=None,
            repo_path=Path("/repo"),
            pack_dir=Path("/pack"),
            build_command="gradlew compileJava",
            scan_context=None,
            cli_version="2.0",
        )
        is None
    )
