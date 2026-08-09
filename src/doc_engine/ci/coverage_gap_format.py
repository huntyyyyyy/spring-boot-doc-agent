"""Presentation helpers for coverage gap-average reports."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from doc_engine.ci.coverage_gap_average import GapAverageReport


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
