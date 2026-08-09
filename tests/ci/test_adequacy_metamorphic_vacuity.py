"""TDD coverage for metamorphic vacuity sensor (E-QA1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci.adequacy.criterion_ports import SLICE_KIND_METAMORPHIC_VACUITY
from doc_engine.ci.adequacy.metamorphic_vacuity import (
    HARNESS_VACUITY_POINTER,
    count_rule_fixture_java,
    load_metamorphic_vacuity_inventory,
    metamorphic_vacuity_slice,
)

pytestmark = pytest.mark.domain_ci_meta


def test_count_rule_fixture_java_tmp_and_missing(tmp_path: Path) -> None:
    fixtures = tmp_path / "rule_fixtures"
    fixtures.mkdir()
    (fixtures / "One.java").write_text("class One {}", encoding="utf-8")
    (fixtures / "Two.java").write_text("class Two {}", encoding="utf-8")
    (fixtures / "readme.txt").write_text("skip", encoding="utf-8")
    assert count_rule_fixture_java(fixtures) == 2
    assert count_rule_fixture_java(tmp_path / "absent") == 0


def test_metamorphic_vacuity_slice_pointers(tmp_path: Path) -> None:
    fixtures = tmp_path / "rule_fixtures"
    fixtures.mkdir()
    (fixtures / "ApiSurface.java").write_text("class A {}", encoding="utf-8")
    inventory = load_metamorphic_vacuity_inventory(fixtures_dir=fixtures)
    assert inventory.rule_fixture_java_count == 1
    assert inventory.harness_vacuity_pointer == HARNESS_VACUITY_POINTER
    slice_row = metamorphic_vacuity_slice(inventory)
    assert slice_row.kind == SLICE_KIND_METAMORPHIC_VACUITY
    assert slice_row.present is True
    joined = " ".join(slice_row.body_lines)
    assert "HarnessIsNotVacuousTest" in joined
    assert "Arm-1" in joined
    assert "does not re-run" in joined


def test_repo_rule_fixtures_count_is_positive() -> None:
    inventory = load_metamorphic_vacuity_inventory()
    assert inventory.rule_fixture_java_count == 10
