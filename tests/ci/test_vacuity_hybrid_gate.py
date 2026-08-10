"""Hybrid vacuity gate: ast-grep structural hits fail closed; rg is triage only."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci.vacuity.astgrep_engine import run_astgrep_vacuity
from doc_engine.ci.vacuity.scan import scan_vacuity

pytestmark = pytest.mark.domain_ci_meta


def test_astgrep_flags_assert_true(tmp_path: Path) -> None:
    root = tmp_path / "tests" / "ci"
    root.mkdir(parents=True)
    (root / "test_plant.py").write_text(
        "def test_vacuous():\n    assert True\n",
        encoding="utf-8",
    )
    # Engine expects roots relative to repo; point repo at tmp and scan tests/ci.
    hits = run_astgrep_vacuity(tmp_path, ("tests/ci",))
    assert any(hit.rule_id == "vacuous__assert_true" for hit in hits), hits


def test_astgrep_flags_pass_only(tmp_path: Path) -> None:
    root = tmp_path / "tests" / "ci"
    root.mkdir(parents=True)
    (root / "test_plant.py").write_text(
        "def test_stub():\n    pass\n",
        encoding="utf-8",
    )
    hits = run_astgrep_vacuity(tmp_path, ("tests/ci",))
    assert any(hit.rule_id == "vacuous__test_pass_only" for hit in hits), hits


def test_scan_ok_on_clean_tree(tmp_path: Path) -> None:
    root = tmp_path / "tests" / "ci"
    root.mkdir(parents=True)
    (root / "test_ok.py").write_text(
        "def test_real():\n    assert 1 + 1 == 2\n",
        encoding="utf-8",
    )
    report = scan_vacuity(tmp_path, ("tests/ci",), write_ledger=False)
    assert report.ok, report.structural
