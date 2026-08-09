"""Mutant apply/run loop for spring-signals assertion-engine driver."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def apply_and_collect_survivors(
    engine: Path,
    pristine: str,
    mutants: list[tuple[str, str, str]],
    repo_root: Path,
) -> list[str] | int:
    survivors: list[str] = []
    try:
        for name, old, new in mutants:
            if old not in pristine:
                print(f"ANCHOR MISSING for {name}; driver is stale")
                return 2
            engine.write_text(pristine.replace(old, new, 1), encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/spring_signals/", "-q", "-x"],
                cwd=repo_root,
                capture_output=True,
                text=True,
            )
            status = "KILLED" if run.returncode != 0 else "SURVIVED"
            print(f"{status}: {name}")
            if run.returncode == 0:
                survivors.append(name)
    finally:
        engine.write_text(pristine, encoding="utf-8")
    return survivors


def exit_for_survivors(
    survivors: list[str], *, enforce: bool, mutant_count: int
) -> int:
    if survivors:
        print(f"\n{len(survivors)} mutant(s) survived: {survivors}")
        if not enforce:
            print("\n(reporting only: ENFORCE is False)", file=sys.stderr)
            return 0
        return 1
    print(f"\nAll {mutant_count} mutants killed; engine restored.")
    return 0
