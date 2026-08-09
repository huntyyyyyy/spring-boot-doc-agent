#!/usr/bin/env python3
"""Summarize coverage.xml for CI (GitHub step summary and/or stdout).

Replaces inline ``python <<'PY'`` heredocs in workflows (policy C-A / C3).
Missing coverage.xml is non-fatal for the summary mode (pytest may have
failed before writing); print-line-rate mode requires the file.

Usage:
    python3 scripts/ci/coverage_run_summary.py --github-summary
    python3 scripts/ci/coverage_run_summary.py --print-line-rate

Run with:
    python3 scripts/ci/coverage_run_summary.py --github-summary
"""

from __future__ import annotations

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from doc_engine.ci.github_step_summary import append_markdown_cli


def _line_rate_pct(coverage_xml: Path) -> float:
    root = ET.parse(coverage_xml).getroot()
    return 100.0 * float(root.attrib.get("line-rate", "0"))


def format_coverage_summary_markdown(
    *,
    python_version: str,
    fail_under: str,
    line_rate: float | None,
) -> str:
    """Markdown block for the oracle-cell coverage headline."""
    if line_rate is None:
        return "### Line coverage (doc_engine + stf)\n\ncoverage.xml missing\n"
    return (
        "### Line coverage (doc_engine + stf)\n\n"
        f"- Python `{python_version}`: **{line_rate:.2f}%** XML line-rate "
        f"(fail_under floor {fail_under}% "
        f"is combined stmt+branch Cover% from pytest-cov)\n"
    )


def write_github_summary(
    coverage_xml: Path,
    summary_path: Path,
    *,
    python_version: str,
    fail_under: str,
) -> int:
    """Append coverage headline to the GitHub step summary (validated path)."""
    line_rate: float | None = None
    if coverage_xml.is_file():
        line_rate = _line_rate_pct(coverage_xml)
        print(f"xml line-rate={line_rate:.2f}%")
    else:
        print("coverage.xml missing — pytest may have failed before writing it")
    markdown = format_coverage_summary_markdown(
        python_version=python_version,
        fail_under=fail_under,
        line_rate=line_rate,
    )
    return append_markdown_cli(
        markdown, summary_path, ok_message="coverage summary appended"
    )


def print_line_rate(coverage_xml: Path) -> int:
    if not coverage_xml.is_file():
        print(f"error: missing {coverage_xml}", file=sys.stderr)
        return 1
    pct = _line_rate_pct(coverage_xml)
    print(f"coverage.xml line-rate={pct:.2f}%")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--coverage-xml",
        type=Path,
        default=Path("coverage.xml"),
        help="path to coverage.xml (default: ./coverage.xml)",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--github-summary",
        action="store_true",
        help="append a coverage block to $GITHUB_STEP_SUMMARY",
    )
    mode.add_argument(
        "--print-line-rate",
        action="store_true",
        help="print line-rate and require coverage.xml to exist",
    )
    args = parser.parse_args(argv)
    if args.print_line_rate:
        return print_line_rate(args.coverage_xml)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary:
        print("error: GITHUB_STEP_SUMMARY is unset", file=sys.stderr)
        return 2
    return write_github_summary(
        args.coverage_xml,
        Path(summary),
        python_version=os.environ.get("PYTHON_VERSION", "?"),
        fail_under=os.environ.get("COV_FAIL_UNDER", "?"),
    )


if __name__ == "__main__":
    raise SystemExit(main())
