"""Characterization: quality setpoints have one concept owner (E-KNOB1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci import complexipy_ratchet, quality_gate_checks
from doc_engine.ci.adequacy import structural_summary
from doc_engine.ci.complexity_policy import COMPLEXITY_MAX, DEFAULT_BASELINE
from doc_engine.ci.coverage_artifact_policy import DEFAULT_FLOOR
from doc_engine.ci.duplication_policy import (
    DUPLICATION_MAX_PERCENT,
    DUPLICATION_MIN_LINES,
)
from doc_engine.ci.package_scope import PACKAGE_ROOTS

pytestmark = pytest.mark.domain_ci_meta


def test_cover_floor_owner_shared_by_gates_and_echo() -> None:
    assert quality_gate_checks.NEW_CODE_COVERAGE_FLOOR == DEFAULT_FLOOR
    assert structural_summary.DEFAULT_FLOOR_ECHO == f"{DEFAULT_FLOOR:g}"


def test_complexity_owner_shared_by_gate_and_ratchet() -> None:
    assert quality_gate_checks.COMPLEXITY_MAX is COMPLEXITY_MAX
    assert complexipy_ratchet.COMPLEXITY_MAX is COMPLEXITY_MAX
    assert COMPLEXITY_MAX == 5
    assert quality_gate_checks.COMPLEXITY_BASELINE == DEFAULT_BASELINE


def test_duplication_and_package_scope_owners() -> None:
    assert quality_gate_checks.DUPLICATION_MAX_PERCENT is DUPLICATION_MAX_PERCENT
    assert DUPLICATION_MIN_LINES == 5
    assert quality_gate_checks.PACKAGE_ROOTS is PACKAGE_ROOTS
    assert complexipy_ratchet.PACKAGE_ROOTS is PACKAGE_ROOTS


def test_pyproject_fail_under_mirrors_default_floor() -> None:
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    assert f"fail_under = {DEFAULT_FLOOR}" in text
