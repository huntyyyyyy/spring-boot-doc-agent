"""CLI adapter for citation_coverage."""

from __future__ import annotations

import argparse
import json
import os
import sys

from doc_engine.tools.citation_coverage_constants import DEFAULT_ANCHOR_WINDOW


def main():
    from doc_engine.tools import citation_coverage as cc

    parser = argparse.ArgumentParser(
        description=(
            "Report claims that carry no evidence tag, and citations "
            "whose line anchor does not appear to support the claim."
        )
    )
    parser.add_argument("docs_dir", help="directory of generated .md docs")
    parser.add_argument(
        "--target-repo",
        default=None,
        help="the documented repo, needed for the weak-anchor check",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=DEFAULT_ANCHOR_WINDOW,
        help=(
            f"lines each side of a citation that count as 'near' "
            f"(default {DEFAULT_ANCHOR_WINDOW})"
        ),
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="emit the raw finding objects instead of prose",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "exit 1 when there are findings. Off by default: "
            "both checks are worklists, and a run should not "
            "fail on a heuristic the way it fails on an "
            "unresolvable citation."
        ),
    )
    args = parser.parse_args()

    if not os.path.isdir(args.docs_dir):
        print(f"error: not a directory: {args.docs_dir}", file=sys.stderr)
        return 2

    report = cc.check_docs(args.docs_dir, args.target_repo, args.window)

    if args.as_json:
        print(json.dumps(report, indent=2))
    else:
        print(cc.format_report(report, args.target_repo))
        print(
            f"\n{cc.total_findings(report)} finding(s) across {len(report)} file(s)."
        )

    return 1 if (args.strict and cc.total_findings(report)) else 0
