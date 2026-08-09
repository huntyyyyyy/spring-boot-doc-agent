"""Value objects and climb-witness kinds for adequacy sensors (E-QA1 / Q2).

Usage:
    from doc_engine.ci.adequacy.criterion_ports import (
        AdequacyReport,
        AdequacySlice,
        WITNESS_KINDS,
    )
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

# Climb Archive / adequacy witness kinds (Q2). Process checklist — not a gate.
WITNESS_KIND_INCIDENT_MUTANT: Final[str] = "incident_mutant"
WITNESS_KIND_MUTMUT_SLICE: Final[str] = "mutmut_slice"
WITNESS_KIND_METAMORPHIC: Final[str] = "metamorphic_relation"

WITNESS_KINDS: Final[frozenset[str]] = frozenset(
    {
        WITNESS_KIND_INCIDENT_MUTANT,
        WITNESS_KIND_MUTMUT_SLICE,
        WITNESS_KIND_METAMORPHIC,
    }
)

SLICE_KIND_STRUCTURAL: Final[str] = "structural"
SLICE_KIND_MUTATOR_SURVIVORS: Final[str] = "mutator_survivors"
SLICE_KIND_METAMORPHIC_VACUITY: Final[str] = "metamorphic_vacuity"


@dataclass(frozen=True)
class AdequacySlice:
    """One hermetic adequacy sensor row for the CI summary presenter."""

    kind: str
    title: str
    body_lines: tuple[str, ...]
    present: bool


@dataclass(frozen=True)
class AdequacyReport:
    """Ordered collection of adequacy sensor slices (sensors only)."""

    slices: tuple[AdequacySlice, ...]

    def slice_kinds(self) -> tuple[str, ...]:
        return tuple(item.kind for item in self.slices)
