"""Assertion-engine mutants for spring-signals/harness/check-assertions.py.

Taxonomy note: this is *not* the gate-mutator harness
(`scripts/ratchets/mutate.py`) and *not* formatting perturbations
(`java_perturbations.py`). Oracle = kill mutants in check-assertions. Not
PIT-class Java SUT mutation. See CONTRIBUTING.md “Mutation-scope taxonomies.”

Applies each named mutant to the engine in place, runs the test suite,
verifies the mutant is killed, and restores the pristine source. Run from the
repo root:  python tests/spring_signals/mutation_driver.py

ENFORCE = False -- see the CI step name, which says "non-blocking". Survivors
are reported but do not fail the job until a threshold is defended. A missing
anchor (driver stale vs. engine) still exits non-zero: that is a broken tool,
not a soft score.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "spring-signals" / "harness" / "check-assertions.py"

# Flip to True once a zero-survivor threshold is defended. Until then CI must
# name this step "non-blocking" (same honesty rule as scripts/ratchets/mutate.py).
ENFORCE = False

MUTANTS = [
    (
        "M1 minimums >= -> >",
        'rep.verdict(got >= want, name, got, f">= {want}")',
        'rep.verdict(got > want, name, got, f">= {want}")',
    ),
    (
        "M2 exact == -> >=",
        "rep.verdict(got == want, name, got, str(want))",
        "rep.verdict(got >= want, name, got, str(want))",
    ),
    (
        "M3 exact == -> <=",
        "rep.verdict(got == want, name, got, str(want))",
        "rep.verdict(got <= want, name, got, str(want))",
    ),
    (
        "M4 missing CSV returns 0 rows",
        "    if not path.exists():\n        return -1, Counter()",
        "    if not path.exists():\n        return 0, Counter()",
    ),
    (
        "M5 IDENT_RE weakened",
        'IDENT_RE = re.compile(r"^[A-Za-z]\\w*$", re.ASCII)',
        'IDENT_RE = re.compile(r".*")',
    ),
    (
        "M6 record containment removed",
        "    if not spec_path.is_relative_to(harness_dir):",
        "    if False:",
    ),
    (
        "M7 signals compared as sets",
        "        rep.verdict(actual.get(rule, []) == want_sorted,",
        "        rep.verdict(set(actual.get(rule, [])) == set(want_sorted),",
    ),
    (
        "M8 stale-CSV check removed",
        "    check_no_stale_csvs(out_dir, spec)",
        "    pass  # mutant: stale CSVs tolerated",
    ),
    (
        "M9 record shadows asserted",
        "        for key in list(entry):\n"
        "            if key in asserted.get(query, {}):\n"
        "                del entry[key]",
        "        pass  # mutant: asserted keys shadowed by recorded ones",
    ),
    (
        "M10 record merges instead of replaces",
        '    spec["snapshot"] = build_recorded_block(out_dir, asserted)',
        '    spec.setdefault("snapshot", {}).update(build_recorded_block(out_dir, asserted))',
    ),
]


def main() -> int:
    from tests.spring_signals.mutation_loop import apply_and_collect_survivors, exit_for_survivors
    pristine = ENGINE.read_text(encoding="utf-8")
    result = apply_and_collect_survivors(ENGINE, pristine, MUTANTS, REPO_ROOT)
    if isinstance(result, int):
        return result
    return exit_for_survivors(result, enforce=ENFORCE, mutant_count=len(MUTANTS))

if __name__ == "__main__":
    import sys
    sys.exit(main())
