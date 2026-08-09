"""Doc-engine domain meeting inventory (gap-average analogy, floor 98.7).

Modules still on ``domain_unclassified`` are the *debt* set. Once reclassified
to a named BC they leave that set and are no longer part of the debt inventory
— same partition idea as coverage gap-average (green files excluded).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from doc_engine.ci.test_domain_catalog import (
    DOC_ENGINE_MEETING_FLOOR,
    UNCLASSIFIED_MARKER,
)
from doc_engine.ci.test_domain_classify import classify_test_path, iter_test_modules


@dataclass(frozen=True)
class DocEngineDomainInventory:
    """Partition of ``tests/doc_engine`` modules by classification debt."""

    floor: float
    total: int
    meeting: tuple[Path, ...]
    debt: tuple[Path, ...]

    @property
    def meeting_pct(self) -> float:
        if self.total <= 0:
            return 100.0
        return 100.0 * len(self.meeting) / self.total

    @property
    def meets_floor(self) -> bool:
        return self.meeting_pct >= self.floor


def build_doc_engine_inventory(repo: Path) -> DocEngineDomainInventory:
    """Classify doc_engine tests; debt = still ``domain_unclassified``."""
    modules = [
        path
        for path in iter_test_modules(repo)
        if "doc_engine" in path.parts
    ]
    meeting: list[Path] = []
    debt: list[Path] = []
    for path in modules:
        marker = classify_test_path(repo, path)
        if marker == UNCLASSIFIED_MARKER:
            debt.append(path)
        else:
            meeting.append(path)
    return DocEngineDomainInventory(
        floor=DOC_ENGINE_MEETING_FLOOR,
        total=len(modules),
        meeting=tuple(meeting),
        debt=tuple(debt),
    )
