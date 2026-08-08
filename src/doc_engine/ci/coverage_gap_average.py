"""Report coverage averaged only over files still below the floor.

Whole-repo ``fail_under`` (pyproject / pytest-cov) still includes every file.
This report drops files already at or above the floor so the climb inventory is
not diluted by green modules.

Usage:
    doc-engine coverage-gap-average
    python -m doc_engine.ci.coverage_gap_average --coverage-xml coverage.xml \\
        --floor 98.7 --worst 15 --markdown

Exit codes:
    0  report written (or nothing to report)
    2  missing / unreadable coverage.xml
"""

from __future__ import annotations

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from doc_engine.ci.gate_tools import REPO_ROOT

DEFAULT_FLOOR = 98.7
DEFAULT_XML = REPO_ROOT / "coverage.xml"


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


def parse_file_coverages(coverage_xml: Path) -> list[FileCoverage]:
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


def format_text(report: GapAverageReport, *, worst: int) -> str:
    """Human-readable gap-average report (stdout / CI logs)."""
    lines = [
        f"coverage gap-average (floor={report.floor:g}%)",
        f"  files total={len(report.files)}  "
        f"meeting_floor={len(report.meeting_floor)}  "
        f"below_floor={len(report.below_floor)}",
        f"  whole_repo_cover={report.whole_repo_cover_pct:.2f}%",
        f"  below_floor_cover={report.below_floor_cover_pct:.2f}%  "
        f"(weighted stmt+branch; green files excluded)",
        f"  below_floor_mean_file={report.below_floor_mean_file_pct:.2f}%  "
        f"(unweighted mean of below-floor file %)",
    ]
    if not report.below_floor:
        lines.append("  worst: (none — every measured file meets the floor)")
        return "\n".join(lines)
    lines.append(f"  worst {min(worst, len(report.below_floor))} below-floor files:")
    for row in report.worst(worst):
        lines.append(
            f"    {row.cover_pct:6.2f}%  "
            f"miss_stmt={row.missed_statements} miss_br={row.missed_branches}  "
            f"{row.path}"
        )
    return "\n".join(lines)


def format_markdown(report: GapAverageReport, *, worst: int) -> str:
    """GitHub step-summary markdown."""
    lines = [
        "### Coverage gap-average (below-floor files only)",
        "",
        f"- Floor: **{report.floor:g}%**",
        f"- Files: total={len(report.files)}, "
        f"meeting_floor={len(report.meeting_floor)}, "
        f"below_floor={len(report.below_floor)}",
        f"- Whole-repo Cover%: **{report.whole_repo_cover_pct:.2f}%** "
        f"(fail_under SoR; includes green files)",
        f"- Below-floor Cover%: **{report.below_floor_cover_pct:.2f}%** "
        f"(weighted; climb inventory — green files excluded)",
        f"- Below-floor mean file %: **{report.below_floor_mean_file_pct:.2f}%**",
        "",
    ]
    if not report.below_floor:
        lines.append("Every measured file meets the floor.")
        return "\n".join(lines)
    lines.extend(
        [
            "| Cover% | miss stmt | miss br | file |",
            "| ---: | ---: | ---: | --- |",
        ]
    )
    for row in report.worst(worst):
        lines.append(
            f"| {row.cover_pct:.2f} | {row.missed_statements} | "
            f"{row.missed_branches} | `{row.path}` |"
        )
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--coverage-xml",
        type=Path,
        default=DEFAULT_XML,
        help="Cobertura XML path (default: ./coverage.xml)",
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
    coverage_xml = args.coverage_xml
    if not coverage_xml.is_absolute():
        coverage_xml = REPO_ROOT / coverage_xml
    if not coverage_xml.is_file():
        print(f"error: missing coverage report: {coverage_xml}", file=sys.stderr)
        return 2
    try:
        files = parse_file_coverages(coverage_xml)
    except ET.ParseError as exc:
        print(f"error: unreadable coverage.xml: {exc}", file=sys.stderr)
        return 2
    report = build_report(files, floor=args.floor)
    text = (
        format_markdown(report, worst=args.worst)
        if args.markdown
        else format_text(report, worst=args.worst)
    )
    print(text, flush=True)
    if args.append_github_summary:
        _append_github_summary(format_markdown(report, worst=args.worst))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
