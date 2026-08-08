"""Tests for doc_engine.paths."""

from pathlib import Path

import pytest

from doc_engine.paths import (
    PathValidationError,
    ast_grep_rules_path,
    checked_output_path,
    checked_path,
    codeql_dir,
    join_under,
    repo_root,
    schemas_dir,
    scripts_dir,
)


def test_repo_root_contains_pyproject():
    root = repo_root()
    assert (root / "pyproject.toml").is_file()


def test_scripts_dir_under_repo_root():
    root = repo_root()
    scripts = scripts_dir()
    assert scripts.is_dir()
    assert scripts.parent == root


def test_schemas_dir_exists():
    assert schemas_dir().is_dir()


def test_ast_grep_rules_path_exists():
    assert ast_grep_rules_path().is_file()


def test_codeql_dir_exists():
    assert codeql_dir().is_dir()


def test_checked_path_rejects_dotdot(tmp_path: Path):
    nested = tmp_path / "a" / "b"
    nested.mkdir(parents=True)
    with pytest.raises(PathValidationError, match=r"\.\."):
        checked_path(nested / ".." / ".." / "etc", want="dir")


def test_checked_path_accepts_existing_dir(tmp_path: Path):
    assert checked_path(tmp_path, want="dir") == tmp_path.resolve()


def test_join_under_rejects_escape(tmp_path: Path):
    (tmp_path / "ok.txt").write_text("x", encoding="utf-8")
    with pytest.raises(PathValidationError, match="unsafe path component"):
        join_under(tmp_path, "..", "outside.txt")


def test_join_under_keeps_nested_file(tmp_path: Path):
    nested = tmp_path / "docs"
    nested.mkdir()
    target = nested / "readme.md"
    target.write_text("# hi\n", encoding="utf-8")
    assert join_under(tmp_path, "docs", "readme.md") == target.resolve()


def test_checked_output_path_requires_parent(tmp_path: Path):
    missing_parent = tmp_path / "nope" / "out.json"
    with pytest.raises(PathValidationError, match="output parent"):
        checked_output_path(missing_parent)


def test_checked_output_path_accepts_new_file(tmp_path: Path):
    out = tmp_path / "report.json"
    assert checked_output_path(out) == out.resolve()
