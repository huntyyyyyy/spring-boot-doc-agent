"""TDD coverage for hermetic mutator survivor inventory (E-QA1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci.adequacy.criterion_ports import SLICE_KIND_MUTATOR_SURVIVORS
from doc_engine.ci.adequacy.mutator_survivors import (
    load_mutator_survivor_inventory,
    mutator_survivors_slice,
    read_accepted_survivors,
    read_enforce_flag,
    registry_mutator_count,
)

pytestmark = pytest.mark.domain_ci_meta


def _write_enforce(path: Path, value: bool) -> None:
    path.write_text(f"ENFORCE = {value}\nOTHER = 1\n", encoding="utf-8")


def test_read_enforce_flag_true_and_false(tmp_path: Path) -> None:
    true_path = tmp_path / "gate.py"
    false_path = tmp_path / "assert_driver.py"
    _write_enforce(true_path, True)
    _write_enforce(false_path, False)
    assert read_enforce_flag(true_path) is True
    assert read_enforce_flag(false_path) is False


def test_read_accepted_survivors_from_tmp_baseline(tmp_path: Path) -> None:
    baseline = tmp_path / "mutation_baseline.json"
    baseline.write_text(
        '{"schema_version": 1, "accepted_survivors": '
        '{"zebra-gap": {}, "alpha-gap": {}}}\n',
        encoding="utf-8",
    )
    names = read_accepted_survivors(baseline)
    assert names == ("alpha-gap", "zebra-gap")
    assert read_accepted_survivors(tmp_path / "missing.json") == ()


def test_inventory_and_slice_with_injected_registry_count(tmp_path: Path) -> None:
    baseline = tmp_path / "mutation_baseline.json"
    baseline.write_text(
        '{"schema_version": 1, "accepted_survivors": {"gap-one": {}}}\n',
        encoding="utf-8",
    )
    gate = tmp_path / "mutate.py"
    assertion = tmp_path / "mutation_driver.py"
    _write_enforce(gate, False)
    _write_enforce(assertion, False)
    inventory = load_mutator_survivor_inventory(
        baseline_path=baseline,
        gate_mutate_path=gate,
        assertion_driver_path=assertion,
        registry_count=7,
    )
    assert inventory.registry_count == 7
    assert inventory.accepted_survivor_count == 1
    assert inventory.gate_enforce is False
    assert inventory.assertion_enforce is False
    slice_row = mutator_survivors_slice(inventory)
    assert slice_row.kind == SLICE_KIND_MUTATOR_SURVIVORS
    joined = " ".join(slice_row.body_lines)
    assert "7" in joined
    assert "`gap-one`" in joined
    assert "ENFORCE=**False**" in joined


def test_registry_mutator_count_matches_live_catalog() -> None:
    assert registry_mutator_count() >= 1
