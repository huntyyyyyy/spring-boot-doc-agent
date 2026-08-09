"""TDD coverage for structural adequacy sensor (E-QA1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci.adequacy.criterion_ports import SLICE_KIND_STRUCTURAL
from doc_engine.ci.adequacy.structural_summary import structural_slice

pytestmark = pytest.mark.domain_ci_meta


def test_structural_slice_missing_coverage_xml(tmp_path: Path) -> None:
    missing = tmp_path / "coverage.xml"
    slice_row = structural_slice(missing, floor_echo="98.7")
    assert slice_row.kind == SLICE_KIND_STRUCTURAL
    assert slice_row.present is False
    joined = " ".join(slice_row.body_lines)
    assert "coverage.xml missing" in joined
    assert "98.7" in joined
    assert "does not claim" in joined or "separate SoT" in joined


def test_structural_slice_present_line_rate(tmp_path: Path) -> None:
    coverage = tmp_path / "coverage.xml"
    coverage.write_text('<coverage line-rate="0.987"/>', encoding="utf-8")
    slice_row = structural_slice(coverage, floor_echo="98.7")
    assert slice_row.present is True
    joined = " ".join(slice_row.body_lines)
    assert "98.70%" in joined
    assert "sensor text only" in joined
    assert "fail_under floor 98.7%" in joined
