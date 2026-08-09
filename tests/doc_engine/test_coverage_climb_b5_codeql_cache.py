"""Coverage climb B5: CodeQL cache dir / metadata / results JSON edges."""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import doc_engine.scanning.support._codeql_cache as cache_mod
from doc_engine.paths import PathValidationError
from doc_engine.scanning.support import _codeql_runner as runner

pytestmark = pytest.mark.domain_climb_sensor


def test_cache_base_dir_win32_and_home_fallback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.setattr(cache_mod.sys, "platform", "win32")
    local = tmp_path / "LocalAppData"
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    assert cache_mod._cache_base_dir() == local
    monkeypatch.delenv("LOCALAPPDATA", raising=False)
    monkeypatch.setattr(cache_mod.Path, "home", classmethod(lambda cls: tmp_path / "home"))
    assert cache_mod._cache_base_dir() == tmp_path / "home" / "AppData" / "Local"


def test_refuse_broken_symlink_and_chmod_oserror(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlinks unavailable")
    link = tmp_path / "broken-cache"
    try:
        os.symlink(tmp_path / "missing-target", link)
    except OSError as exc:
        pytest.skip(f"symlink creation failed: {exc}")
    with pytest.raises(runner.CodeQLError, match="symlink"):
        cache_mod._refuse_symlink_cache_path(link)

    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    monkeypatch.setattr(
        cache_mod.os,
        "chmod",
        MagicMock(side_effect=OSError("chmod denied")),
    )
    path = cache_mod._cache_dir()
    assert path.is_dir()


def test_cache_meta_path_validation_and_metadata_none(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _boom(_base, *_parts):
        raise PathValidationError("escape")

    monkeypatch.setattr(cache_mod, "join_under", _boom)
    with pytest.raises(runner.CodeQLError, match="escape"):
        cache_mod._cache_meta_path(tmp_path / "db")
    assert cache_mod._cache_metadata(tmp_path / "db") is None


def test_load_save_results_cache_edges(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    assert (
        cache_mod._load_results_cache(
            repo, pack, "gradlew compileJava", "sv", codeql_cli_version="2.0"
        )
        is None
    )
    rows = [{"file": "A.java", "line": 1}]
    cache_mod._save_results_cache(
        repo, pack, "gradlew compileJava", "sv", rows, codeql_cli_version="2.0"
    )
    path = cache_mod._results_cache_path(
        repo, pack, "gradlew compileJava", "sv", codeql_cli_version="2.0"
    )
    assert path.is_file()
    # Second save hits exists → _ensure_regular_file; chmod OSError is soft.
    monkeypatch.setattr(
        cache_mod.os, "chmod", MagicMock(side_effect=OSError("chmod denied"))
    )
    cache_mod._save_results_cache(
        repo, pack, "gradlew compileJava", "sv", rows, codeql_cli_version="2.0"
    )
    path.write_text("not-a-list", encoding="utf-8")
    assert (
        cache_mod._load_results_cache(
            repo, pack, "gradlew compileJava", "sv", codeql_cli_version="2.0"
        )
        is None
    )


def test_cache_is_valid_none_meta_and_validate_row() -> None:
    assert (
        cache_mod._cache_is_valid(
            Path("/no/such/db"),
            Path("/repo"),
            Path("/pack"),
            "gradlew compileJava",
            codeql_cli_version="2.0",
        )
        is False
    )
    with pytest.raises(runner.CodeQLError, match="not an object"):
        cache_mod._validate_one_cached_row(0, ["not", "dict"])
    assert cache_mod._validate_one_cached_row(0, {"file": "A.java"})["file"] == "A.java"
