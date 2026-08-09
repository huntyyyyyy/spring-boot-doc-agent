"""Parse pytest ``--junitxml`` into suite timing records (E-RUN1 / D1).

Preferred machine SoT for oracle-cell durations. New report formats get a
new adapter module (OCP) — do not grow this parser with format switches.

Usage:
    from doc_engine.ci.suite_timing.junit_duration_parse import parse_junit_durations
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from doc_engine.ci.suite_timing.duration_records import (
    CaseDuration,
    SuiteTimingReport,
)


def _testcase_node_id(element: ET.Element) -> str:
    classname = (element.attrib.get("classname") or "").strip()
    name = (element.attrib.get("name") or "").strip()
    if classname and name:
        return f"{classname}::{name}"
    return name or classname or "(unknown)"


def _duration_seconds(element: ET.Element) -> float:
    raw = element.attrib.get("time", "0")
    try:
        return float(raw)
    except ValueError:
        return 0.0


def parse_junit_durations(junit_xml: Path) -> SuiteTimingReport:
    """Load all ``testcase`` rows from a junit XML path into a sorted report."""
    root = ET.parse(junit_xml).getroot()
    rows: list[CaseDuration] = []
    for element in root.iter("testcase"):
        rows.append(
            CaseDuration(
                node_id=_testcase_node_id(element),
                duration_seconds=_duration_seconds(element),
            )
        )
    return SuiteTimingReport.from_records(rows)
