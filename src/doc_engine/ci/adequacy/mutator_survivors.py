"""Hermetic gate/assertion mutator survivor inventory (E-QA1).

Reads registry count, mutation_baseline.json, and ENFORCE flags — does **not**
re-run mutate / mutation_driver.

Usage:
    from doc_engine.ci.adequacy.mutator_survivors import mutator_survivors_slice
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from doc_engine.ci.adequacy.criterion_ports import (
    SLICE_KIND_MUTATOR_SURVIVORS,
    AdequacySlice,
)
from doc_engine.paths import repo_root, scripts_dir, scripts_meta_path_entries

_ENFORCE_ASSIGN = re.compile(
    r"^ENFORCE\s*=\s*(True|False)\s*(?:#.*)?$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class MutatorSurvivorInventory:
    """Snapshot of mutator catalog + accepted survivors + ENFORCE flags."""

    registry_count: int
    accepted_survivor_names: tuple[str, ...]
    gate_enforce: bool
    assertion_enforce: bool

    @property
    def accepted_survivor_count(self) -> int:
        return len(self.accepted_survivor_names)


def read_enforce_flag(source_path: Path) -> bool:
    """Parse module-level ``ENFORCE = <bool>`` without executing the module."""
    match = _ENFORCE_ASSIGN.search(source_path.read_text(encoding="utf-8"))
    if match is None:
        raise ValueError(f"ENFORCE assignment not found in {source_path}")
    return match.group(1) == "True"


def read_accepted_survivors(baseline_path: Path) -> tuple[str, ...]:
    """Return sorted accepted survivor names from mutation_baseline.json."""
    if not baseline_path.is_file():
        return ()
    payload = json.loads(baseline_path.read_text(encoding="utf-8"))
    accepted = payload.get("accepted_survivors", {})
    if not isinstance(accepted, dict):
        raise ValueError(f"accepted_survivors must be an object in {baseline_path}")
    return tuple(sorted(str(name) for name in accepted))


def registry_mutator_count() -> int:
    """Count gate mutators via ``all_mutators()`` (path insert, no kill run)."""
    for entry in scripts_meta_path_entries():
        if entry not in sys.path:
            sys.path.insert(0, entry)
    from mutator_registry import all_mutators

    return len(all_mutators())


def load_mutator_survivor_inventory(
    *,
    baseline_path: Path,
    gate_mutate_path: Path,
    assertion_driver_path: Path,
    registry_count: int | None = None,
) -> MutatorSurvivorInventory:
    """Assemble hermetic inventory from baseline + ENFORCE sources."""
    count = registry_mutator_count() if registry_count is None else registry_count
    return MutatorSurvivorInventory(
        registry_count=count,
        accepted_survivor_names=read_accepted_survivors(baseline_path),
        gate_enforce=read_enforce_flag(gate_mutate_path),
        assertion_enforce=read_enforce_flag(assertion_driver_path),
    )


def default_paths(root: Path | None = None) -> tuple[Path, Path, Path]:
    """Return (baseline, gate mutate.py, assertion driver) under *root*."""
    base = root if root is not None else repo_root()
    baseline = scripts_dir() / "ratchets" / "mutation_baseline.json"
    if root is not None:
        baseline = base / "scripts" / "ratchets" / "mutation_baseline.json"
    gate = base / "scripts" / "ratchets" / "mutate.py"
    assertion = base / "tests" / "spring_signals" / "mutation_driver.py"
    return baseline, gate, assertion


def mutator_survivors_slice(
    inventory: MutatorSurvivorInventory,
) -> AdequacySlice:
    """Present mutator survivor inventory as an adequacy sensor slice."""
    names = inventory.accepted_survivor_names
    name_note = (
        ", ".join(f"`{name}`" for name in names)
        if names
        else "(none — baseline empty or missing)"
    )
    return AdequacySlice(
        kind=SLICE_KIND_MUTATOR_SURVIVORS,
        title="Mutator survivors (hermetic inventory)",
        body_lines=(
            f"Gate mutator registry count: **{inventory.registry_count}** "
            "(`all_mutators()`, no kill run).",
            f"Accepted survivors in baseline: **{inventory.accepted_survivor_count}** "
            f"— {name_note}.",
            f"`scripts/ratchets/mutate.py` ENFORCE=**{inventory.gate_enforce}** "
            "(measurement-first; Q8).",
            f"`tests/spring_signals/mutation_driver.py` "
            f"ENFORCE=**{inventory.assertion_enforce}** "
            "(measurement-first; Q8).",
        ),
        present=True,
    )
