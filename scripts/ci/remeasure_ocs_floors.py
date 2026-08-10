#!/usr/bin/env python3
"""Remeasure OCS expectation floors via ast-grep (no Artifactory) — E-OCS0 OCS6.

Default is dry-run: print a proposal JSON. ``--write`` updates numeric
minimums in the expectations file (operator-reviewed).

Usage:
    python3 scripts/ci/remeasure_ocs_floors.py
    python3 scripts/ci/remeasure_ocs_floors.py --checkout /path/to/tree
    python3 scripts/ci/remeasure_ocs_floors.py --write
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
_HARNESS = REPO_ROOT / "spring-signals" / "harness"
if str(_HARNESS) not in sys.path:
    sys.path.insert(0, str(_HARNESS))

from plant_profile import resolve_ocs_checkout  # noqa: E402

RULES = _HARNESS / "astgrep_ocs_floors.yml"
EXPECTATIONS = _HARNESS / "expectations" / "ocs-api-service.json"
FLOOR_RULES = (
    "api_surface__controller",
    "api_surface__endpoint",
    "api_surface__path_prefix",
    "persistence__repository_marker",
)


def _scan_roots(checkout: Path) -> list[Path]:
    mains = sorted({path.resolve() for path in checkout.glob("**/src/main/java")})
    if mains:
        return mains
    return [checkout.resolve()]


def _run_astgrep(roots: Sequence[Path], rules: Path) -> Counter[str]:
    if not roots:
        return Counter()
    completed = subprocess.run(
        [
            "ast-grep",
            "scan",
            "-r",
            str(rules),
            "--json=compact",
            *[str(path) for path in roots],
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1):
        raise RuntimeError(
            (completed.stderr or completed.stdout or "ast-grep failed")[:500]
        )
    return _count_rule_ids(completed.stdout)


def _count_rule_ids(stdout: str) -> Counter[str]:
    text = (stdout or "").strip()
    if not text:
        return Counter()
    payload = json.loads(text)
    rows = payload if isinstance(payload, list) else [payload]
    return Counter(
        str(row["ruleId"])
        for row in rows
        if isinstance(row, dict) and row.get("ruleId")
    )


def _numeric_minimums(data: dict) -> dict[str, int]:
    out: dict[str, int] = {}
    for bucket in (data.get("minimums") or {}).values():
        out.update(_bucket_numeric_floors(bucket))
    return out


def _bucket_numeric_floors(bucket: object) -> dict[str, int]:
    if not isinstance(bucket, dict):
        return {}
    return {
        key: value
        for key, value in bucket.items()
        if not key.startswith("_") and isinstance(value, int)
    }


def _floor_row(rule_id: str, counts: Counter[str], minimums: dict[str, int]) -> dict:
    current = int(counts.get(rule_id, 0))
    minimum = minimums.get(rule_id)
    if minimum is None:
        return {
            "rule_id": rule_id,
            "current": current,
            "minimum": None,
            "delta": None,
            "status": "no_floor_key",
        }
    return {
        "rule_id": rule_id,
        "current": current,
        "minimum": minimum,
        "delta": current - minimum,
        "status": "ok" if current >= minimum else "below_floor",
    }


def build_proposal(
    counts: Counter[str],
    minimums: dict[str, int],
    *,
    checkout: Path,
) -> dict:
    return {
        "checkout": str(checkout),
        "rules": str(RULES.relative_to(REPO_ROOT).as_posix()),
        "floors": [_floor_row(rule_id, counts, minimums) for rule_id in FLOOR_RULES],
        "write_applied": False,
    }


def apply_write(expectations: Path, counts: Counter[str]) -> None:
    data = json.loads(expectations.read_text(encoding="utf-8"))
    for bucket in (data.get("minimums") or {}).values():
        _apply_bucket_floors(bucket, counts)
    tmp = expectations.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(data, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    tmp.replace(expectations)


def _apply_bucket_floors(bucket: object, counts: Counter[str]) -> None:
    if not isinstance(bucket, dict):
        return
    for rule_id in FLOOR_RULES:
        if rule_id in bucket and isinstance(bucket.get(rule_id), int):
            bucket[rule_id] = int(counts.get(rule_id, 0))


def _resolve_checkout(root: Path, explicit: Optional[Path]) -> Optional[Path]:
    if explicit is not None:
        return explicit if explicit.is_dir() else None
    return resolve_ocs_checkout(root)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--checkout", type=Path, default=None)
    parser.add_argument("--expectations", type=Path, default=EXPECTATIONS)
    parser.add_argument("--rules", type=Path, default=RULES)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Rewrite numeric floors in expectations (default: dry-run)",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    checkout = _resolve_checkout(root, args.checkout)
    if checkout is None:
        print(
            "error: no OCS checkout — pass --checkout or set "
            "DOC_ENGINE_REAL_REPO / local-runs/real-repo.path",
            file=sys.stderr,
        )
        return 2
    rules = args.rules if args.rules.is_absolute() else root / args.rules
    expectations = (
        args.expectations
        if args.expectations.is_absolute()
        else root / args.expectations
    )
    if not rules.is_file():
        print(f"error: rules missing: {rules}", file=sys.stderr)
        return 2
    counts = _run_astgrep(_scan_roots(checkout), rules)
    data = json.loads(expectations.read_text(encoding="utf-8"))
    proposal = build_proposal(
        counts, _numeric_minimums(data), checkout=checkout.resolve()
    )
    if args.write:
        apply_write(expectations, counts)
        proposal["write_applied"] = True
    print(json.dumps(proposal, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
