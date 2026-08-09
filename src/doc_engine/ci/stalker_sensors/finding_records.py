"""Immutable stalker finding records (G1–G10)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

KIND_G1 = "ratchet_schema_skew"
KIND_G2 = "split_scope_break"
KIND_G3 = "facade_api_regress"
KIND_G4 = "collect_or_syntax"
KIND_G5 = "process_parallel_tip"
KIND_G6 = "policy_verify_incomplete"
KIND_G7 = "masked_advisory_nonzero"
KIND_G8 = "oracle_cell_posture"
KIND_G9 = "codeql_change_presence"
KIND_G10 = "workflow_suite_map"

ALL_KINDS = (
    KIND_G1,
    KIND_G2,
    KIND_G3,
    KIND_G4,
    KIND_G5,
    KIND_G6,
    KIND_G7,
    KIND_G8,
    KIND_G9,
    KIND_G10,
)


@dataclass(frozen=True)
class StalkerFinding:
    kind: str
    summary: str
    evidence: str
    backlog_pointer: str = "P15.1"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
