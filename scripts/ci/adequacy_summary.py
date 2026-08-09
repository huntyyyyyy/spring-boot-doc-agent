#!/usr/bin/env python3
"""Append adequacy sensors to GitHub step summary (E-QA1).

Thin façade over ``doc_engine.ci.adequacy`` — keeps workflow YAML free of
inline Python (policy C-A / C3). Does not claim fail_under.

Usage:
    python3 scripts/ci/adequacy_summary.py --github-summary
    python3 scripts/ci/adequacy_summary.py --github-summary --coverage-xml coverage.xml

Run with:
    python3 scripts/ci/adequacy_summary.py --github-summary
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from doc_engine.ci.adequacy.github_adequacy_summary import (
    append_github_summary,
    render_adequacy_report,
)
from doc_engine.paths import PathValidationError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--coverage-xml",
        type=Path,
        default=Path("coverage.xml"),
        help="coverage.xml path for structural sensor (default: ./coverage.xml)",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="optional repo root override for hermetic path resolution",
    )
    parser.add_argument(
        "--fixtures-dir",
        type=Path,
        default=None,
        help="optional rule_fixtures directory override",
    )
    parser.add_argument(
        "--registry-count",
        type=int,
        default=None,
        help="optional gate-mutator count override (tests); default = all_mutators()",
    )
    parser.add_argument(
        "--floor-echo",
        default="98.7",
        help="oracle floor echoed as sensor text only (default: 98.7)",
    )
    parser.add_argument(
        "--github-summary",
        action="store_true",
        required=True,
        help="append adequacy block to $GITHUB_STEP_SUMMARY",
    )
    args = parser.parse_args(argv)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary:
        print("error: GITHUB_STEP_SUMMARY is unset", file=sys.stderr)
        return 2
    markdown = render_adequacy_report(
        coverage_xml=args.coverage_xml,
        floor_echo=args.floor_echo,
        repo=args.repo_root,
        registry_count=args.registry_count,
        fixtures_dir=args.fixtures_dir,
    )
    try:
        append_github_summary(markdown, Path(summary))
    except PathValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print("adequacy summary appended")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
