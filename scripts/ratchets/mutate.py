#!/usr/bin/env python3
"""Sandboxed kill harness for **gate mutators** (artifact-aware).

Usage:
    python3 scripts/ratchets/mutate.py                 # run every mutator
    python3 scripts/ratchets/mutate.py --filter grep   # only mutators whose name matches
    python3 scripts/ratchets/mutate.py --update        # rewrite the survivor baseline

ENFORCE = False -- see the CI step name, which says "non-blocking".

Gate mutators only (catalog ``gate_mutators`` → ``mutator_registry``). Oracle =
named suite fails. Not formatting perturbations (``java_perturbations``), not
assertion-engine mutants (``mutation_driver``), not PIT Java SUT mutation.
New mutators: incident-seeded only — see CONTRIBUTING.md.

WHY THIS EXISTS

A gate that cannot be shown to fail is not a gate. Catalog is OCP-open via the
registry; this file stays closed to operator churn (sandbox / score / baseline).

mutmut remains the complement for pure-Python modules; this harness is
artifact-aware (markdown / YAML / CI defects mutmut would miss).

SANDBOXED, ALWAYS — tracked-tree copy in a temp dir; never the working tree.
ONE SUITE PER MUTATION — a survivor is a test gap, not a bug in the artifact.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional

from doc_engine.paths import repo_root, scripts_dir, scripts_meta_path_entries

for _entry in scripts_meta_path_entries():
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

import suite_layout  # noqa: E402
from mutator import Mutator  # noqa: E402
from mutator_registry import all_mutators  # noqa: E402

REPO_ROOT = repo_root()
BASELINE_FILE = scripts_dir() / "ratchets" / "mutation_baseline.json"
SCHEMA_VERSION = 1

ENFORCE = False

# Backward-compatible alias: tests and callers still read mutate.MUTATORS.
MUTATORS: List[Mutator] = list(all_mutators())


class Outcome(NamedTuple):
    name: str
    status: str        # "killed" | "survived" | "misattributed" | "not-applied"
    detail: str


def tracked_files() -> List[str]:
    result = subprocess.run(["git", "-C", str(REPO_ROOT), "ls-files"],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"git ls-files failed: {result.stderr.strip()}")
    return [line for line in result.stdout.splitlines() if line.strip()]


def materialize(dest: Path) -> None:
    """Copy the tracked tree into ``dest``. Tracked-only, deliberately."""
    for rel in tracked_files():
        source = REPO_ROOT / rel
        if not source.is_file():
            continue
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    # Overlay working tests/src/scripts so sandboxes match pytest CI.
    for dirname in ("tests", "src"):
        source_dir = REPO_ROOT / dirname
        if source_dir.is_dir():
            shutil.copytree(
                source_dir, dest / dirname, dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
    scripts_root = REPO_ROOT / "scripts"
    if scripts_root.is_dir():
        shutil.copytree(
            scripts_root, dest / "scripts", dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(
                "__pycache__", "*.pyc", ".claude", ".gradle", "target",
            ),
        )


def apply_mutation(root: Path, mutator: Mutator) -> Optional[str]:
    """Apply ``mutator`` under ``root``; return error text if not applied."""
    return mutator.apply(root)


def resolve_suite_path(root: Path, suite: str) -> Path:
    """Resolve ``test_*.py`` under pyproject testpaths (recursive)."""
    name = Path(suite).name
    module = name[len("test_"):] if name.startswith("test_") else name
    found = suite_layout.suite_file_for_module(root, module)
    if found is not None:
        return found
    raise FileNotFoundError(
        f"suite {name!r} not found under "
        f"{', '.join(suite_layout.suite_roots(root))}"
    )


def run_suite(root: Path, suite: str) -> int:
    path = resolve_suite_path(root, suite)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(path), "-q", "--tb=no"],
        capture_output=True, text=True, cwd=str(root),
    )
    return result.returncode


def evaluate(mutator: Mutator, tmp_root: Path) -> Outcome:
    sandbox = tmp_root / mutator.name
    sandbox.mkdir(parents=True)
    materialize(sandbox)
    error = apply_mutation(sandbox, mutator)
    if error:
        return Outcome(mutator.name, "not-applied", error)
    if run_suite(sandbox, mutator.expected_caught_by) != 0:
        return Outcome(mutator.name, "killed",
                       f"{mutator.expected_caught_by} failed, as it should")
    return Outcome(mutator.name, "survived",
                   f"{mutator.expected_caught_by} still passed. {mutator.why}")


def load_baseline() -> Dict[str, str]:
    if not BASELINE_FILE.is_file():
        return {}
    data = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        return {}
    return dict(data.get("accepted_survivors", {}))


def write_baseline(outcomes: List[Outcome]) -> None:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "$comment": (
            "Mutations that no suite currently catches. Each entry is a test "
            "gap someone accepted, not a bug. Shrinking this file is always "
            "correct; growing it needs a reason in the PR that does it. "
            "Regenerate with: python3 scripts/ratchets/mutate.py --update"
        ),
        "accepted_survivors": {o.name: o.detail
                               for o in outcomes if o.status == "survived"},
    }
    BASELINE_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def report(outcomes: List[Outcome], accepted: Dict[str, str]) -> int:
    killed = [o for o in outcomes if o.status == "killed"]
    survived = [o for o in outcomes if o.status == "survived"]
    broken = [o for o in outcomes if o.status == "not-applied"]
    new_survivors = [o for o in survived if o.name not in accepted]

    print(f"mutation score: {len(killed)}/{len(outcomes)} killed "
          f"({len(survived)} survived, {len(broken)} not applied)")
    for outcome in outcomes:
        mark = {"killed": "  killed     ", "survived": "  SURVIVED   ",
                "not-applied": "  NOT APPLIED"}[outcome.status]
        print(f"{mark} {outcome.name}: {outcome.detail}")

    if broken:
        print("\nA mutator whose anchor no longer exists is testing nothing. "
              "Fix the anchor or delete the mutator.", file=sys.stderr)
    if new_survivors:
        print(f"\n{len(new_survivors)} new survivor(s) — a mutation nothing "
              f"caught is a gap in the tests, not a bug in the code:",
              file=sys.stderr)
        for outcome in new_survivors:
            print(f"  {outcome.name}: {outcome.detail}", file=sys.stderr)
    return 1 if (new_survivors or broken) else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--filter", default="",
                        help="only run mutators whose name contains this")
    parser.add_argument("--update", action="store_true",
                        help="rewrite the survivor baseline from this run")
    args = parser.parse_args(argv)

    catalog = list(all_mutators())
    selected = [m for m in catalog if args.filter in m.name]
    if not selected:
        print(f"error: no mutator matches {args.filter!r}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="mutate_") as tmp:
        outcomes = [evaluate(m, Path(tmp)) for m in selected]

    if args.update:
        write_baseline(outcomes)
        print(f"wrote {BASELINE_FILE.name}")
        return 0

    code = report(outcomes, load_baseline())
    if code and not ENFORCE:
        print("\n(reporting only: ENFORCE is False)", file=sys.stderr)
        return 0
    return code


if __name__ == "__main__":
    sys.exit(main())
