"""Below-floor coverage gap-average (partition, average, and present).

One concept: climb inventory over files still under the floor. Loads via
:class:`~doc_engine.ci.coverage_report.CoverageReport`, validates with
:class:`~doc_engine.ci.coverage_path_cohesion.PathCohesionGuard`.

Usage:
    doc-engine coverage-gap-average
    python -m doc_engine.ci.coverage_gap_average --coverage-xml coverage.xml \\
        --floor 98.7 --worst 15 --markdown

Exit codes: 0 ok; 2 missing / unreadable / non-cohesive coverage.xml
"""

from __future__ import annotations

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from doc_engine.ci.coverage_artifact_policy import (
    DEFAULT_FLOOR,
    refuse_climb_as_gap_inventory,
)
from doc_engine.ci.coverage_path_cohesion import PathCohesionError, PathCohesionGuard
from doc_engine.ci.coverage_report import (
    CoverageReport,
    FileCoverage,
    load_cobertura_report,
    parse_cobertura_files,
)
from doc_engine.ci.gate_tools import checkout_root

# Mutable so tests can patch the active checkout (same pattern as gate_tools).
REPO_ROOT = checkout_root()


def parse_file_coverages(coverage_xml: Path) -> list[FileCoverage]:
    """Parse Cobertura XML (compat wrapper around the report adapter)."""
    return parse_cobertura_files(coverage_xml)


@dataclass(frozen=True)
class GapAverageReport:
    """Partition + averages + presentation for files below the coverage floor."""

    floor: float
    files: tuple[FileCoverage, ...]
    meeting_floor: tuple[FileCoverage, ...]
    below_floor: tuple[FileCoverage, ...]

    @property
    def whole_repo_cover_pct(self) -> float:
        measurable = sum(f.measurable for f in self.files)
        if measurable <= 0:
            return 100.0
        return 100.0 * sum(f.covered for f in self.files) / measurable

    @property
    def below_floor_cover_pct(self) -> float:
        measurable = sum(f.measurable for f in self.below_floor)
        if measurable <= 0:
            return 100.0
        return 100.0 * sum(f.covered for f in self.below_floor) / measurable

    @property
    def below_floor_mean_file_pct(self) -> float:
        if not self.below_floor:
            return 100.0
        return sum(f.cover_pct for f in self.below_floor) / len(self.below_floor)

    def worst(self, limit: int) -> list[FileCoverage]:
        return sorted(self.below_floor, key=lambda f: (f.cover_pct, -f.measurable))[
            : max(0, limit)
        ]

    def as_text(self, *, worst: int) -> str:
        """Human-readable gap-average (stdout / CI logs)."""
        lines = [
            f"coverage gap-average (floor={self.floor:g}%)",
            f"  files total={len(self.files)}  "
            f"meeting_floor={len(self.meeting_floor)}  "
            f"below_floor={len(self.below_floor)}",
            f"  whole_repo_cover={self.whole_repo_cover_pct:.2f}%",
            f"  below_floor_cover={self.below_floor_cover_pct:.2f}%  "
            f"(weighted stmt+branch; green files excluded)",
            f"  below_floor_mean_file={self.below_floor_mean_file_pct:.2f}%  "
            f"(unweighted mean of below-floor file %)",
        ]
        if not self.below_floor:
            lines.append("  worst: (none — every measured file meets the floor)")
            return "\n".join(lines)
        lines.append(f"  worst {min(worst, len(self.below_floor))} below-floor files:")
        for row in self.worst(worst):
            lines.append(
                f"    {row.cover_pct:6.2f}%  "
                f"miss_stmt={row.missed_statements} miss_br={row.missed_branches}  "
                f"{row.path}"
            )
        return "\n".join(lines)

    def as_markdown(self, *, worst: int) -> str:
        """GitHub step-summary markdown."""
        lines = [
            "### Coverage gap-average (below-floor files only)",
            "",
            f"- Floor: **{self.floor:g}%**",
            f"- Files: total={len(self.files)}, "
            f"meeting_floor={len(self.meeting_floor)}, "
            f"below_floor={len(self.below_floor)}",
            f"- Whole-repo Cover%: **{self.whole_repo_cover_pct:.2f}%** "
            f"(fail_under SoR; includes green files)",
            f"- Below-floor Cover%: **{self.below_floor_cover_pct:.2f}%** "
            f"(weighted; climb inventory — green files excluded)",
            f"- Below-floor mean file %: **{self.below_floor_mean_file_pct:.2f}%**",
            "",
        ]
        if not self.below_floor:
            lines.append("Every measured file meets the floor.")
            return "\n".join(lines)
        lines.extend(
            ["| Cover% | miss stmt | miss br | file |", "| ---: | ---: | ---: | --- |"]
        )
        for row in self.worst(worst):
            lines.append(
                f"| {row.cover_pct:.2f} | {row.missed_statements} | "
                f"{row.missed_branches} | `{row.path}` |"
            )
        return "\n".join(lines)


def format_text(report: GapAverageReport, *, worst: int) -> str:
    return report.as_text(worst=worst)


def format_markdown(report: GapAverageReport, *, worst: int) -> str:
    return report.as_markdown(worst=worst)


def build_report(files: list[FileCoverage], *, floor: float) -> GapAverageReport:
    meeting = tuple(f for f in files if f.cover_pct >= floor)
    below = tuple(f for f in files if f.cover_pct < floor)
    return GapAverageReport(
        floor=floor, files=tuple(files), meeting_floor=meeting, below_floor=below
    )


def build_report_from_coverage(
    report: CoverageReport,
    *,
    floor: float,
    repo_root: Path | None = None,
) -> GapAverageReport:
    """Gap-average from an abstract report after path-cohesion validation."""
    root = (repo_root or checkout_root()).resolve()
    PathCohesionGuard(root).assert_cohesive(report.source_paths())
    return build_report(list(report.files), floor=floor)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--coverage-xml", type=Path, default=None)
    p.add_argument("--floor", type=float, default=DEFAULT_FLOOR)
    p.add_argument("--worst", type=int, default=15)
    p.add_argument("--markdown", action="store_true")
    p.add_argument("--append-github-summary", action="store_true")
    return p.parse_args(argv)


def _resolve_coverage_xml(args: argparse.Namespace) -> Path:
    coverage_xml = args.coverage_xml or (REPO_ROOT / "coverage.xml")
    if not coverage_xml.is_absolute():
        coverage_xml = REPO_ROOT / coverage_xml
    return coverage_xml


def _append_github_summary(markdown: str) -> None:
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        Path(summary).open("a", encoding="utf-8").write("\n" + markdown + "\n")


def _print_gap_report(report: GapAverageReport, args: argparse.Namespace) -> None:
    text = (
        report.as_markdown(worst=args.worst)
        if args.markdown
        else report.as_text(worst=args.worst)
    )
    print(text, flush=True)
    if args.append_github_summary:
        _append_github_summary(report.as_markdown(worst=args.worst))


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    coverage_xml = _resolve_coverage_xml(args)
    climb_err = refuse_climb_as_gap_inventory(coverage_xml)
    if climb_err is not None:
        print(f"error: {climb_err}", file=sys.stderr)
        return 2
    if not coverage_xml.is_file():
        print(f"error: missing coverage report: {coverage_xml}", file=sys.stderr)
        return 2
    try:
        report = build_report_from_coverage(
            load_cobertura_report(coverage_xml),
            floor=args.floor,
            repo_root=REPO_ROOT,
        )
    except ET.ParseError as exc:
        print(f"error: unreadable coverage.xml: {exc}", file=sys.stderr)
        return 2
    except PathCohesionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    _print_gap_report(report, args)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
