#!/usr/bin/env python3
"""E-STK1 advisory stalker scan (G1–G6). Never rewrites fail_under/baselines.

Usage:
    python3 scripts/ci/stalker_scan.py
    python3 scripts/ci/stalker_scan.py --no-ledger
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from doc_engine.ci.stalker_sensors.scan import scan_and_write  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--no-ledger",
        action="store_true",
        help="print findings only; do not write docs/research/findings/",
    )
    args = parser.parse_args(argv)
    findings = scan_and_write(REPO_ROOT, write_ledger=not args.no_ledger)
    print(f"stalker_scan: {len(findings)} finding(s)")
    for item in findings:
        print(f"  [{item.kind}] {item.summary}")
    # Advisory: always exit 0 so pre_pr overall stays green; detail is the ledger.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
