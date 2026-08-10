"""Hard vacuity gate — Rust ast-grep + telemetry empty-receipt learning.

Usage::

    python3 -m doc_engine.ci.vacuity
    python3 scripts/ci/vacuous_test_gate.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from doc_engine.ci.vacuity.astgrep_engine import DEFAULT_ROOTS
from doc_engine.ci.vacuity.scan import format_report, scan_vacuity
from doc_engine.paths import repo_root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument(
        "--roots",
        nargs="*",
        default=list(DEFAULT_ROOTS),
        help="Test path prefixes under repo root",
    )
    parser.add_argument(
        "--no-ledger",
        action="store_true",
        help="Do not append .git/pre-pr-telemetry/vacuity-ledger.jsonl",
    )
    args = parser.parse_args(argv)
    root = (args.root or repo_root()).resolve()
    report = scan_vacuity(
        root,
        tuple(args.roots),
        write_ledger=not args.no_ledger,
    )
    print(format_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
