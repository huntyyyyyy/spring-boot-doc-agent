"""Coverage climb B6: scan CLI config branches; Q2 witness mutmut_slice.

Witness: mutmut_slice on ``doc_engine.cli_scan_config``.
"""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path

import pytest

from doc_engine.cli_scan_config import (
    apply_optional_scan_flags,
    scan_cli_overrides,
    scan_config,
    split_scanner_names,
)

pytestmark = pytest.mark.domain_climb_sensor


def test_split_scanner_names_strips_and_drops_empties() -> None:
    assert split_scanner_names(" filesystem , ast-grep,,codeql ") == [
        "filesystem",
        "ast-grep",
        "codeql",
    ]
    assert split_scanner_names("") == []


def test_scan_cli_overrides_optional_and_dialect(tmp_path: Path) -> None:
    empty = Namespace(
        scanners=None,
        sql_dialect="ansi",
        respect_gitignore=False,
        build_command=None,
        db_path=None,
    )
    assert scan_cli_overrides(empty) == {}

    full = Namespace(
        scanners="filesystem,ast-grep",
        sql_dialect="mysql",
        respect_gitignore=True,
        build_command="mvn -q",
        db_path="/tmp/db",
    )
    overrides = scan_cli_overrides(full)
    assert overrides["scanners"] == ["filesystem", "ast-grep"]
    assert overrides["sql_dialect"] == "mysql"
    assert overrides["respect_gitignore"] is True
    assert overrides["build_command"] == "mvn -q"
    assert overrides["db_path"] == "/tmp/db"

    partial: dict = {}
    apply_optional_scan_flags(
        Namespace(respect_gitignore=False, build_command=None, db_path=None),
        partial,
    )
    assert partial == {}


def test_scan_config_merges_without_repo_json(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    args = Namespace(
        scanners="filesystem",
        sql_dialect="ansi",
        respect_gitignore=False,
        build_command=None,
        db_path=None,
        trust_repo_config=False,
    )
    cfg = scan_config(str(repo), args)
    assert "filesystem" in cfg.scanners
