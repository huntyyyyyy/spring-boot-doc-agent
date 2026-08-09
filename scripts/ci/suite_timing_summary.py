#!/usr/bin/env python3
"""Append suite-timing sensors to GitHub step summary (E-RUN1).

Thin façade over ``doc_engine.ci.suite_timing`` — keeps workflow YAML free of
inline Python (policy C-A / C3). Does not claim fail_under.

Usage:
    python3 scripts/ci/suite_timing_summary.py --github-summary
    python3 scripts/ci/suite_timing_summary.py --github-summary --top-n 20

Run with:
    python3 scripts/ci/suite_timing_summary.py --github-summary
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from doc_engine.ci.github_step_summary import append_markdown_cli
from doc_engine.ci.suite_timing.github_timing_summary import render_from_junit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--junit-xml",
        type=Path,
        default=Path("pytest-oracle.junit.xml"),
        help="pytest --junitxml path (default: ./pytest-oracle.junit.xml)",
    )
    parser.add_argument(
        "--coverage-xml",
        type=Path,
        default=Path("coverage.xml"),
        help="coverage.xml path used for D17 cascade (default: ./coverage.xml)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=15,
        help="how many slowest tests to list (default: 15)",
    )
    parser.add_argument(
        "--github-summary",
        action="store_true",
        required=True,
        help="append timing block to $GITHUB_STEP_SUMMARY",
    )
    args = parser.parse_args(argv)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary:
        print("error: GITHUB_STEP_SUMMARY is unset", file=sys.stderr)
        return 2
    markdown = render_from_junit(
        args.junit_xml,
        coverage_xml=args.coverage_xml,
        top_n=args.top_n,
    )
    return append_markdown_cli(
        markdown, summary, ok_message="suite timing summary appended"
    )


if __name__ == "__main__":
    raise SystemExit(main())
