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


def _line_rate_pct(coverage_xml: Path) -> float:
    root = ET.parse(coverage_xml).getroot()
    return 100.0 * float(root.attrib.get("line-rate", "0"))


def write_github_summary(
    coverage_xml: Path,
    summary_path: Path,
    *,
    python_version: str,
    fail_under: str,
) -> int:
    if not coverage_xml.is_file():
        print("coverage.xml missing — pytest may have failed before writing it")
        summary_path.write_text(
            "### Line coverage (doc_engine + stf)\n\ncoverage.xml missing\n",
            encoding="utf-8",
        )
        return 0
    pct = _line_rate_pct(coverage_xml)
    summary_path.write_text(
        "### Line coverage (doc_engine + stf)\n\n"
        f"- Python `{python_version}`: **{pct:.2f}%** XML line-rate "
        f"(fail_under floor {fail_under}% "
        f"is combined stmt+branch Cover% from pytest-cov)\n",
        encoding="utf-8",
    )
    print(f"xml line-rate={pct:.2f}%")
    return 0


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
