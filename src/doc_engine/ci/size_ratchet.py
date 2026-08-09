"""Ratchet file LOC and function statement-count ceilings (must not rise).

Usage:
    doc-engine size-ratchet
    python -m doc_engine.ci.size_ratchet --update

Hard fail when a new file exceeds FILE_LOC_HARD (225), a baselined file's
LOC grows, a new function exceeds FN_STMTS_HARD (50), a baselined function's
statement count grows, or hard-offender counts rise. Soft advisories print
above FILE_LOC_SOFT (150) / FN_STMTS_SOFT (20). Measurement lives in
``size_measure``; this module owns policy, baseline persistence, and CLI.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

from doc_engine.ci.gate_tools import REPO_ROOT, checked_path_under_repo
from doc_engine.ci.size_measure import PACKAGE_ROOTS, measure_tree, statement_count

FILE_LOC_HARD = 225
FILE_LOC_SOFT = 150
FN_STMTS_HARD = 50
FN_STMTS_SOFT = 20
SCHEMA_VERSION = 2
DEFAULT_BASELINE = REPO_ROOT / "scripts" / "ratchets" / "size_baseline.json"


def hard_file_offenders(file_loc: Dict[str, int]) -> Dict[str, int]:
    return {k: v for k, v in sorted(file_loc.items()) if v > FILE_LOC_HARD}


def hard_fn_offenders(functions: Dict[str, int]) -> Dict[str, int]:
    return {k: v for k, v in sorted(functions.items()) if v > FN_STMTS_HARD}


def soft_advisories(
    file_loc: Dict[str, int], functions: Dict[str, int]
) -> List[str]:
    notes = [
        f"[advisory] file {path} has loc={loc} "
        f"(soft>{FILE_LOC_SOFT}, hard<={FILE_LOC_HARD})"
        for path, loc in sorted(file_loc.items())
        if FILE_LOC_SOFT < loc <= FILE_LOC_HARD
    ]
    notes.extend(
        f"[advisory] function {key} has statements={stmts} (soft>{FN_STMTS_SOFT})"
        for key, stmts in sorted(functions.items())
        if FN_STMTS_SOFT < stmts <= FN_STMTS_HARD
    )
    return notes


def compare_offenders(
    kind: str,
    baseline: Dict[str, int],
    current: Dict[str, int],
) -> List[str]:
    """Hard failures for new offenders or growth of baselined values."""
    issues: List[str] = []
    if len(current) > len(baseline):
        issues.append(
            f"{kind} hard-offender count rose {len(baseline)} -> {len(current)}"
        )
    for key, value in sorted(current.items()):
        prior = baseline.get(key)
        if prior is None:
            issues.append(f"new {kind} offender {key}={value}")
        elif value > prior:
            issues.append(f"{kind} offender grew: {key} {prior} -> {value}")
    return issues


def build_baseline_payload(
    file_offenders: Dict[str, int], fn_offenders: Dict[str, int]
) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "package_roots": list(PACKAGE_ROOTS),
        "file_loc_hard": FILE_LOC_HARD,
        "file_loc_soft": FILE_LOC_SOFT,
        "fn_stmts_hard": FN_STMTS_HARD,
        "fn_stmts_soft": FN_STMTS_SOFT,
        "file_offender_count": len(file_offenders),
        "fn_offender_count": len(fn_offenders),
        "files": file_offenders,
        "functions": fn_offenders,
        "note": (
            f"Hard ceilings: file LOC > {FILE_LOC_HARD}, function statements > "
            f"{FN_STMTS_HARD}. Soft advisories above {FILE_LOC_SOFT} LOC / "
            f"{FN_STMTS_SOFT} statements. Ratchet offender maps downward only. "
            "Remeasure: doc-engine size-ratchet --update"
        ),
    }


def write_baseline(
    path: Path, file_offenders: Dict[str, int], fn_offenders: Dict[str, int]
) -> None:
    path = checked_path_under_repo(path)
    path.write_text(
        json.dumps(build_baseline_payload(file_offenders, fn_offenders), indent=2)
        + "\n",
        encoding="utf-8",
    )


def load_baseline(path: Path) -> dict:
    path = checked_path_under_repo(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        print(
            f"error: baseline schema_version {data.get('schema_version')!r} "
            f"!= {SCHEMA_VERSION}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return data


def compare(baseline: dict, file_loc: Dict[str, int], functions: Dict[str, int]) -> List[str]:
    """Return hard-failure messages for size-ratchet regressions."""
    return compare_offenders(
        "file", baseline.get("files", {}), hard_file_offenders(file_loc)
    ) + compare_offenders(
        "function", baseline.get("functions", {}), hard_fn_offenders(functions)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args(argv)

    file_loc, functions = measure_tree()
    file_off = hard_file_offenders(file_loc)
    fn_off = hard_fn_offenders(functions)

    if args.update:
        write_baseline(args.baseline, file_off, fn_off)
        print(
            f"baseline written: {args.baseline} "
            f"(files={len(file_off)}, functions={len(fn_off)})"
        )
        return 0

    if not args.baseline.is_file():
        print(
            f"error: no baseline at {args.baseline}; create one with --update",
            file=sys.stderr,
        )
        return 2

    baseline = load_baseline(args.baseline)
    print(
        f"size ratchet: file_offenders={len(file_off)} "
        f"(ceiling={baseline.get('file_offender_count')}) "
        f"fn_offenders={len(fn_off)} "
        f"(ceiling={baseline.get('fn_offender_count')}) "
        f"(file_loc_hard={FILE_LOC_HARD}, fn_stmts_hard={FN_STMTS_HARD})"
    )
    advisories = soft_advisories(file_loc, functions)
    if advisories:
        print(f"size soft advisories ({len(advisories)}):")
        for note in advisories[:40]:
            print(f"  {note}")
        if len(advisories) > 40:
            print(f"  … {len(advisories) - 40} more")
    issues = compare(baseline, file_loc, functions)
    if issues:
        print(f"size ratchet failed ({len(issues)} issue(s)):", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1
    if len(file_off) < int(baseline.get("file_offender_count", 0)) or len(
        fn_off
    ) < int(baseline.get("fn_offender_count", 0)):
        print(
            "note: hard-offender count dropped; "
            "re-baseline with --update to ratchet downward"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
