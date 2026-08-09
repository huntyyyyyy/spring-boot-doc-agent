"""Coverage report domain model + Cobertura XML adapter (DIP boundary).

Gap-average and measure depend on :class:`CoverageReport`, not on a cwd-relative
``coverage.xml`` file name. The Cobertura adapter is the sole XML parser.

Usage:
    from doc_engine.ci.coverage_report import load_cobertura_report
    report = load_cobertura_report(Path("coverage.xml"))
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Sequence


@dataclass(frozen=True)
class FileCoverage:
    """Combined statement+branch coverage for one Cobertura class/file."""

    path: str
    statements: int
    missed_statements: int
    branches: int
    missed_branches: int

    @property
    def measurable(self) -> int:
        return self.statements + self.branches

    @property
    def covered(self) -> int:
        return (
            self.statements
            - self.missed_statements
            + self.branches
            - self.missed_branches
        )

    @property
    def cover_pct(self) -> float:
        if self.measurable <= 0:
            return 100.0
        return 100.0 * self.covered / self.measurable


class CoverageReport(Protocol):
    """Abstract coverage report — pluggable source for gap-average (OCP/DIP)."""

    @property
    def files(self) -> Sequence[FileCoverage]:
        """Per-file coverage rows."""

    def source_paths(self) -> list[str]:
        """Source path strings as recorded in the report."""


@dataclass(frozen=True)
class CoberturaXmlReport:
    """Adapter: coverage.py Cobertura XML → :class:`FileCoverage` rows."""

    _files: tuple[FileCoverage, ...]

    @property
    def files(self) -> Sequence[FileCoverage]:
        return self._files

    def source_paths(self) -> list[str]:
        return [f.path for f in self._files]


def _parse_condition_coverage(raw: str | None) -> tuple[int, int]:
    """Return (taken, total) branch arcs from Cobertura condition-coverage."""
    if not raw or "/" not in raw:
        return (0, 0)
    try:
        part = raw.split("(")[1].split(")")[0]
        taken_s, total_s = part.split("/")
        return (int(taken_s), int(total_s))
    except (IndexError, ValueError):
        return (0, 0)


def _line_branch_totals(lines: list) -> tuple[int, int]:
    branches = 0
    missed_branches = 0
    for line in lines:
        taken, total = _parse_condition_coverage(
            line.attrib.get("condition-coverage")
        )
        if total <= 0:
            continue
        branches += total
        missed_branches += max(0, total - taken)
    return branches, missed_branches


def parse_cobertura_files(coverage_xml: Path) -> list[FileCoverage]:
    """Parse per-file combined Cover% rows from a Cobertura coverage.xml."""
    root = ET.parse(coverage_xml).getroot()
    rows: list[FileCoverage] = []
    for cls in root.iter("class"):
        filename = cls.attrib.get("filename") or cls.attrib.get("name") or ""
        if not filename:
            continue
        lines = list(cls.iter("line"))
        if not lines:
            continue
        statements = len(lines)
        missed_statements = sum(
            1 for line in lines if line.attrib.get("hits", "0") == "0"
        )
        branches, missed_branches = _line_branch_totals(lines)
        rows.append(
            FileCoverage(
                path=filename.replace("\\", "/"),
                statements=statements,
                missed_statements=missed_statements,
                branches=branches,
                missed_branches=missed_branches,
            )
        )
    return rows


def load_cobertura_report(coverage_xml: Path) -> CoberturaXmlReport:
    """Factory helper: load XML into a :class:`CoverageReport` adapter."""
    return CoberturaXmlReport(tuple(parse_cobertura_files(coverage_xml)))
