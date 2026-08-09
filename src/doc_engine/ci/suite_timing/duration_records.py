"""Immutable duration records for suite-stalking sensors (E-RUN1 / D1).

Usage:
    from doc_engine.ci.suite_timing.duration_records import CaseDuration
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class CaseDuration:
    """One pytest case wall time from a junit report."""

    node_id: str
    duration_seconds: float


@dataclass(frozen=True)
class SuiteTimingReport:
    """Sorted duration inventory for one suite run (sensor, not Cover% SoT)."""

    records: tuple[CaseDuration, ...]

    @classmethod
    def from_records(cls, records: Sequence[CaseDuration]) -> SuiteTimingReport:
        ordered = tuple(
            sorted(records, key=lambda row: row.duration_seconds, reverse=True)
        )
        return cls(records=ordered)

    def slowest(self, limit: int) -> tuple[CaseDuration, ...]:
        if limit <= 0:
            return ()
        return self.records[:limit]

    @property
    def total_seconds(self) -> float:
        return sum(row.duration_seconds for row in self.records)
