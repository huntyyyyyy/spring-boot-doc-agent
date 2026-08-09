"""GitHub step-summary presenter for suite timing sensors (E-RUN1).

OCP: additional sinks (stdout table, JSON receipt) belong in sibling modules.

Usage:
    from doc_engine.ci.suite_timing.github_timing_summary import format_timing_markdown
"""

from __future__ import annotations

from pathlib import Path

from doc_engine.ci.github_step_summary import append_markdown
from doc_engine.ci.suite_timing.duration_records import SuiteTimingReport
from doc_engine.ci.suite_timing.junit_duration_parse import parse_junit_durations
from doc_engine.ci.suite_timing.plateau_buckets import (
    KNOWN_BUCKETS,
    plateau_totals_seconds,
)
from doc_engine.ci.suite_timing.pre_pytest_cascade import cascade_markdown


def format_timing_markdown(
    report: SuiteTimingReport,
    *,
    top_n: int,
    coverage_xml: Path,
) -> str:
    """Build markdown: cascade (if needed), slowest tests, plateau totals."""
    sections: list[str] = []
    cascade = cascade_markdown(coverage_xml=coverage_xml)
    if cascade:
        sections.append(cascade.rstrip())

    sections.append("### Suite timing (oracle cell sensor)\n")
    if not report.records:
        sections.append("No junit testcase durations found.\n")
        return "\n".join(sections)

    sections.append(f"Total recorded test time: **{report.total_seconds:.2f}s**\n")
    sections.append(f"#### Slowest {top_n} tests\n")
    for index, row in enumerate(report.slowest(top_n), start=1):
        sections.append(
            f"{index}. `{row.node_id}` — **{row.duration_seconds:.3f}s**"
        )
    sections.append("")
    sections.append("#### Plateau bucket totals (D2)\n")
    totals = plateau_totals_seconds(report.records)
    for bucket in KNOWN_BUCKETS:
        sections.append(f"- `{bucket}`: **{totals.get(bucket, 0.0):.2f}s**")
    sections.append("")
    return "\n".join(sections)


def render_from_junit(
    junit_xml: Path,
    *,
    coverage_xml: Path,
    top_n: int,
) -> str:
    """Parse junit (if present) and format the timing summary markdown."""
    if not junit_xml.is_file():
        cascade = cascade_markdown(coverage_xml=coverage_xml)
        missing = (
            "### Suite timing (oracle cell sensor)\n\n"
            f"junit xml missing at `{junit_xml}` — no duration inventory.\n"
        )
        if cascade:
            return cascade + "\n" + missing
        return missing
    report = parse_junit_durations(junit_xml)
    return format_timing_markdown(
        report, top_n=top_n, coverage_xml=coverage_xml
    )


def append_github_summary(markdown: str, summary_path: Path) -> None:
    """Append markdown to a GitHub step summary file (path-validated)."""
    append_markdown(markdown, summary_path)
