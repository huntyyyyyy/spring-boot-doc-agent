"""Load stage: show last pre_pr telemetry run (local debugger).

Usage:
    python3 scripts/ci/stalker_telemetry.py show
    python3 scripts/ci/stalker_telemetry.py show --failures-only
"""

from __future__ import annotations

import argparse
import json
import sys

from doc_engine.ci.stalker_telemetry.run_store import latest_index
from doc_engine.paths import repo_root


def _show(failures_only: bool) -> int:
    idx = latest_index(repo_root())
    if idx is None:
        print("stalker_telemetry: no .git/pre-pr-telemetry/latest index", file=sys.stderr)
        return 1
    data = json.loads(idx.read_text(encoding="utf-8"))
    print(f"telemetry: {idx}")
    print(f"sha={data.get('git_sha')} mode={data.get('mode')} at={data.get('started_at')}")
    for suite in data.get("suites") or []:
        exit_code = int(suite.get("exit_code") or 0)
        interesting = exit_code != 0 or suite.get("status") == "fail"
        if failures_only and not interesting:
            continue
        print(
            f"  {suite.get('status'):8} {suite.get('kind'):8} "
            f"exit={exit_code} {suite.get('duration_ms')}ms  {suite.get('name')}"
        )
        if interesting and suite.get("error_excerpt"):
            print("    --- excerpt ---")
            for line in str(suite["error_excerpt"]).splitlines()[:15]:
                print(f"    {line}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    show = sub.add_parser("show", help="print last telemetry index")
    show.add_argument("--failures-only", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "show":
        return _show(args.failures_only)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
