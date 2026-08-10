"""Structural Cover% sensor from coverage.xml (E-QA1).

Soft-missing when the XML is absent (same honesty as coverage_run_summary).
Echoes the oracle floor as sensor text only — never asserts fail_under.

Usage:
    from doc_engine.ci.adequacy.structural_summary import structural_slice
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from doc_engine.ci.adequacy.criterion_ports import (
    SLICE_KIND_STRUCTURAL,
    AdequacySlice,
)
from doc_engine.ci.coverage_artifact_policy import DEFAULT_FLOOR

DEFAULT_FLOOR_ECHO: str = f"{DEFAULT_FLOOR:g}"


def _line_rate_pct(coverage_xml: Path) -> float:
    root = ET.parse(coverage_xml).getroot()
    return 100.0 * float(root.attrib.get("line-rate", "0"))


def structural_slice(
    coverage_xml: Path,
    *,
    floor_echo: str = DEFAULT_FLOOR_ECHO,
) -> AdequacySlice:
    """Build the structural adequacy slice from Cobertura XML (or missing)."""
    title = "Structural coverage (sensor)"
    if not coverage_xml.is_file():
        return AdequacySlice(
            kind=SLICE_KIND_STRUCTURAL,
            title=title,
            body_lines=(
                f"coverage.xml missing at `{coverage_xml}` — "
                "pytest may have failed before writing it.",
                f"Oracle fail_under floor {floor_echo}% is a separate SoT "
                "(pytest-cov stmt+branch); this row does not claim it.",
            ),
            present=False,
        )
    pct = _line_rate_pct(coverage_xml)
    return AdequacySlice(
        kind=SLICE_KIND_STRUCTURAL,
        title=title,
        body_lines=(
            f"XML line-rate: **{pct:.2f}%** (Cobertura `line-rate` attribute).",
            f"Oracle fail_under floor {floor_echo}% is a separate SoT "
            "(pytest-cov stmt+branch Cover%); this row is sensor text only.",
        ),
        present=True,
    )
