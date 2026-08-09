"""Below-floor coverage gap-average report (climb inventory).

Refuses Cobertura reports whose source paths escape the active checkout.

Usage:
    doc-engine coverage-gap-average
    python -m doc_engine.ci.coverage_gap_average --coverage-xml coverage.xml \\
        --floor 98.7 --worst 15 --markdown

Exit codes:
    0  report written (or nothing to report)
    2  missing / unreadable / non-cohesive coverage.xml
"""

from __future__ import annotations

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from doc_engine.ci.coverage_path_cohesion import PathCohesionError, assert_paths_cohesive
from doc_engine.ci.coverage_report import (
    CoverageReport,
    FileCoverage,
    load_cobertura_report,
    parse_cobertura_files,
)
from doc_engine.ci.coverage_gap_format import format_markdown, format_text
from doc_engine.ci.gate_tools import checkout_root

# Re-export for callers/tests that import formatters from this module.
__all__ = [
    "DEFAULT_FLOOR",
    "FileCoverage",
    "GapAverageReport",
    "build_report",
    "build_report_from_coverage",
    "format_markdown",
    "format_text",
    "main",
    "parse_file_coverages",
]

DEFAULT_FLOOR = 98.7


def parse_file_coverages(coverage_xml: Path) -> list[FileCoverage]:
    """Parse Cobertura XML (compat wrapper around the report adapter)."""
    return parse_cobertura_files(coverage_xml)


@dataclass(frozen=True)
class GapAverageReport:
    """Partition + averages for files below the coverage floor."""

    floor: float
    files: tuple[FileCoverage, ...]
    meeting_floor: tuple[FileCoverage, ...]
    below_floor: tuple[FileCoverage, ...]

    @property
    def whole_repo_cover_pct(self) -> float:
        measurable = sum(f.measurable for f in self.files)
        if measurable <= 0:
            return 100.0
        covered = sum(f.covered for f in self.files)
        return 100.0 * covered / measurable

    @property
    def below_floor_cover_pct(self) -> float:
        """Weighted Cover% over below-floor files only (primary gap metric)."""
        measurable = sum(f.measurable for f in self.below_floor)
        if measurable <= 0:
            return 100.0
        covered = sum(f.covered for f in self.below_floor)
        return 100.0 * covered / measurable

    @property
    def below_floor_mean_file_pct(self) -> float:
        """Unweighted mean of per-file Cover% among below-floor files."""
        if not self.below_floor:
            return 100.0
        return sum(f.cover_pct for f in self.below_floor) / len(self.below_floor)

    def worst(self, limit: int) -> list[FileCoverage]:
        return sorted(self.below_floor, key=lambda f: (f.cover_pct, -f.measurable))[
            : max(0, limit)
        ]


def build_report(files: list[FileCoverage], *, floor: float) -> GapAverageReport:
    """Partition files at *floor* and compute gap averages."""
    meeting = tuple(f for f in files if f.cover_pct >= floor)
    below = tuple(f for f in files if f.cover_pct < floor)
    return GapAverageReport(
        floor=floor,
        files=tuple(files),
        meeting_floor=meeting,
        below_floor=below,
    )


def build_report_from_coverage(
    report: CoverageReport,
    *,
    floor: float,
    repo_root: Path | None = None,
) -> GapAverageReport:
    """Gap-average from an abstract report after path-cohesion validation."""
    root = (repo_root or checkout_root()).resolve()
    assert_paths_cohesive(report.source_paths(), root)
    return build_report(list(report.files), floor=floor)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--coverage-xml",
        type=Path,
        default=None,
        help="Cobertura XML path (default: <checkout>/coverage.xml)",
    )
    parser.add_argument(
        "--floor",
        type=float,
        default=DEFAULT_FLOOR,
        help=f"Per-file floor for partition (default: {DEFAULT_FLOOR})",
    )
    parser.add_argument(
        "--worst",
        type=int,
        default=15,
        help="How many worst below-floor files to list (default: 15)",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Emit GitHub-flavored markdown instead of plain text",
    )
    parser.add_argument(
        "--append-github-summary",
        action="store_true",
        help="Append markdown to $GITHUB_STEP_SUMMARY when set",
    )
    return parser.parse_args(argv)


def _append_github_summary(markdown: str) -> None:
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        Path(summary).open("a", encoding="utf-8").write("\n" + markdown + "\n")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = checkout_root()
    coverage_xml = args.coverage_xml or (repo_root / "coverage.xml")
    if not coverage_xml.is_absolute():
        coverage_xml = repo_root / coverage_xml
    if not coverage_xml.is_file():
        print(f"error: missing coverage report: {coverage_xml}", file=sys.stderr)
        return 2
    try:
        loaded = load_cobertura_report(coverage_xml)
        report = build_report_from_coverage(
            loaded, floor=args.floor, repo_root=repo_root
        )
    except ET.ParseError as exc:
        print(f"error: unreadable coverage.xml: {exc}", file=sys.stderr)
        return 2
    except PathCohesionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    text = (
        format_markdown(report, worst=args.worst)
        if args.markdown
        else format_text(report, worst=args.worst)
    )
    print(text, flush=True)
    if args.append_github_summary:
        _append_github_summary(format_markdown(report, worst=args.worst))
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry glue
    raise SystemExit(main())
