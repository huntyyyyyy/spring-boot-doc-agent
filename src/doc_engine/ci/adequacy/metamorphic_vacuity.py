"""Hermetic metamorphic vacuity pointers (E-QA1).

Counts ``rule_fixtures`` ``.java`` files and points at Arm-1 / harness
vacuity tests — does not re-run the metamorphic suite.

Usage:
    from doc_engine.ci.adequacy.metamorphic_vacuity import metamorphic_vacuity_slice
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from doc_engine.ci.adequacy.criterion_ports import (
    SLICE_KIND_METAMORPHIC_VACUITY,
    AdequacySlice,
)
from doc_engine.paths import scripts_dir

HARNESS_VACUITY_POINTER: str = (
    "tests/ratchets/test_metamorphic_churn.py::HarnessIsNotVacuousTest"
)
ARM1_SUITE_POINTER: str = (
    "tests/ratchets/test_metamorphic_formatting.py "
    "+ tests/ratchets/test_metamorphic_churn.py (Arm-1 / churn)"
)


@dataclass(frozen=True)
class MetamorphicVacuityInventory:
    """Fixture corpus size + suite pointers for vacuity honesty."""

    rule_fixture_java_count: int
    harness_vacuity_pointer: str
    arm1_suite_pointer: str


def count_rule_fixture_java(fixtures_dir: Path) -> int:
    """Count ``*.java`` files under the metamorphic rule_fixtures corpus."""
    if not fixtures_dir.is_dir():
        return 0
    return sum(1 for path in fixtures_dir.glob("*.java") if path.is_file())


def load_metamorphic_vacuity_inventory(
    *,
    fixtures_dir: Path | None = None,
) -> MetamorphicVacuityInventory:
    """Assemble hermetic metamorphic vacuity inventory."""
    directory = (
        fixtures_dir
        if fixtures_dir is not None
        else scripts_dir() / "coverage" / "rule_fixtures"
    )
    return MetamorphicVacuityInventory(
        rule_fixture_java_count=count_rule_fixture_java(directory),
        harness_vacuity_pointer=HARNESS_VACUITY_POINTER,
        arm1_suite_pointer=ARM1_SUITE_POINTER,
    )


def default_fixtures_dir(root: Path | None = None) -> Path:
    """Return rule_fixtures directory under *root* (or repo scripts/)."""
    if root is None:
        return scripts_dir() / "coverage" / "rule_fixtures"
    return root / "scripts" / "coverage" / "rule_fixtures"


def metamorphic_vacuity_slice(
    inventory: MetamorphicVacuityInventory,
) -> AdequacySlice:
    """Present metamorphic vacuity pointers as an adequacy sensor slice."""
    present = inventory.rule_fixture_java_count > 0
    return AdequacySlice(
        kind=SLICE_KIND_METAMORPHIC_VACUITY,
        title="Metamorphic vacuity (hermetic pointers)",
        body_lines=(
            f"`rule_fixtures` `.java` count: "
            f"**{inventory.rule_fixture_java_count}**.",
            f"Harness vacuity: `{inventory.harness_vacuity_pointer}`.",
            f"Arm-1 suite: {inventory.arm1_suite_pointer}.",
            "Sensor only — does not re-run metamorphic relations.",
        ),
        present=present,
    )
