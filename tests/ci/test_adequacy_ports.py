"""TDD coverage for adequacy criterion ports (E-QA1)."""

from __future__ import annotations

import pytest

from doc_engine.ci.adequacy.criterion_ports import (
    SLICE_KIND_METAMORPHIC_VACUITY,
    SLICE_KIND_MUTATOR_SURVIVORS,
    SLICE_KIND_STRUCTURAL,
    WITNESS_KIND_INCIDENT_MUTANT,
    WITNESS_KIND_METAMORPHIC,
    WITNESS_KIND_MUTMUT_SLICE,
    WITNESS_KINDS,
    AdequacyReport,
    AdequacySlice,
)

pytestmark = pytest.mark.domain_ci_meta


def test_witness_kinds_are_closed_q2_set() -> None:
    assert WITNESS_KINDS == frozenset(
        {
            WITNESS_KIND_INCIDENT_MUTANT,
            WITNESS_KIND_MUTMUT_SLICE,
            WITNESS_KIND_METAMORPHIC,
        }
    )
    assert "incident_mutant" in WITNESS_KINDS
    assert "coverage_percent" not in WITNESS_KINDS


def test_adequacy_slice_and_report_are_frozen() -> None:
    slice_row = AdequacySlice(
        kind=SLICE_KIND_STRUCTURAL,
        title="Structural",
        body_lines=("line-rate sensor",),
        present=True,
    )
    report = AdequacyReport(
        slices=(
            slice_row,
            AdequacySlice(
                kind=SLICE_KIND_MUTATOR_SURVIVORS,
                title="Mutators",
                body_lines=("registry",),
                present=True,
            ),
            AdequacySlice(
                kind=SLICE_KIND_METAMORPHIC_VACUITY,
                title="Meta",
                body_lines=("fixtures",),
                present=False,
            ),
        )
    )
    assert report.slice_kinds() == (
        SLICE_KIND_STRUCTURAL,
        SLICE_KIND_MUTATOR_SURVIVORS,
        SLICE_KIND_METAMORPHIC_VACUITY,
    )
    with pytest.raises(AttributeError):
        slice_row.present = False  # type: ignore[misc]
