"""Coverage climb B6: adequacy sensor edges; Q2 witness mutmut_slice.

Witness: mutmut_slice on ``doc_engine.ci.adequacy`` (hermetic inventory helpers).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from doc_engine.ci.adequacy.metamorphic_vacuity import (
    count_rule_fixture_java,
    default_fixtures_dir,
    load_metamorphic_vacuity_inventory,
    metamorphic_vacuity_slice,
)
from doc_engine.ci.adequacy.mutator_survivors import (
    default_paths,
    load_mutator_survivor_inventory,
    mutator_survivors_slice,
    read_accepted_survivors,
    read_enforce_flag,
)
from doc_engine.ci.adequacy.structural_summary import structural_slice

pytestmark = pytest.mark.domain_climb_sensor


def test_metamorphic_empty_fixtures_dir_and_default_paths(tmp_path: Path) -> None:
    missing = tmp_path / "absent_fixtures"
    assert count_rule_fixture_java(missing) == 0
    inventory = load_metamorphic_vacuity_inventory(fixtures_dir=missing)
    slice_row = metamorphic_vacuity_slice(inventory)
    assert slice_row.present is False
    assert "0" in " ".join(slice_row.body_lines)
    assert default_fixtures_dir(tmp_path).name == "rule_fixtures"
    assert default_fixtures_dir(None).is_dir()


def test_mutator_survivors_missing_baseline_and_default_paths(
    tmp_path: Path,
) -> None:
    gate = tmp_path / "mutate.py"
    assertion = tmp_path / "driver.py"
    gate.write_text("ENFORCE = True\n", encoding="utf-8")
    assertion.write_text("ENFORCE = False\n", encoding="utf-8")
    assert read_enforce_flag(gate) is True
    assert read_accepted_survivors(tmp_path / "nope.json") == ()
    inventory = load_mutator_survivor_inventory(
        baseline_path=tmp_path / "nope.json",
        gate_mutate_path=gate,
        assertion_driver_path=assertion,
        registry_count=0,
    )
    assert inventory.accepted_survivor_count == 0
    assert inventory.gate_enforce is True
    joined = " ".join(mutator_survivors_slice(inventory).body_lines)
    assert "none — baseline empty or missing" in joined
    baseline, gate_path, assertion_path = default_paths(tmp_path)
    assert baseline.name == "mutation_baseline.json"
    assert gate_path.name == "mutate.py"
    assert assertion_path.name == "mutation_driver.py"
    repo_defaults = default_paths(None)
    assert repo_defaults[0].is_file()


def test_mutator_baseline_rejects_non_object_survivors(tmp_path: Path) -> None:
    bad = tmp_path / "mutation_baseline.json"
    bad.write_text(
        json.dumps({"schema_version": 1, "accepted_survivors": ["not-an-object"]}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="accepted_survivors must be an object"):
        read_accepted_survivors(bad)


def test_structural_slice_zero_line_rate(tmp_path: Path) -> None:
    coverage = tmp_path / "coverage.xml"
    coverage.write_text("<coverage/>", encoding="utf-8")
    slice_row = structural_slice(coverage, floor_echo="98.7")
    assert slice_row.present is True
    assert "0.00%" in " ".join(slice_row.body_lines)
