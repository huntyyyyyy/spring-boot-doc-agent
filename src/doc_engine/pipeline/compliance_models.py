"""Compliance profile enums, gate IDs, and certification record models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from doc_engine._compat import StrEnum

CERTIFICATION_SCHEMA_VERSION = 1
SCAN_ONLY_GATE_ID = "validate_artifacts_spring_signals"
DETERMINISTIC_ONLY_GATE_ID = "validate_artifacts_all"

# Synthetic stage row written by live_gates derivation (not in build_stage_specs).
GENERATIVE_EXTERNAL_STAGE = "generative_external"

CERTIFIED_GATE_IDS = frozenset({
    "validate_artifacts_all",
    "pipeline_validators",
    "check_pipeline_output",
    "citation_coverage",
    "check_no_secrets_leaked",
    "test_pipeline_stages",
})


class ComplianceProfile(StrEnum):
    SCAN_ONLY = "scan_only"
    DETERMINISTIC_ONLY = "deterministic_only"
    CERTIFIED = "certified"


class GenerativeExecutor(StrEnum):
    """How generative stages were executed for this certification fold."""

    NONE = "none"
    MOCK = "mock"
    LIVE = "live"


class StageExecutorKind(StrEnum):
    """Per-stage executor stamp on StageRecord (not the StageExecutor Protocol)."""

    DETERMINISTIC = "deterministic"
    NONE = "none"
    MOCK = "mock"
    LIVE = "live"


class RecordStatus(StrEnum):
    """Normalized ok/fail/skipped on certification stage and gate rows."""

    OK = "ok"
    FAIL = "fail"
    SKIPPED = "skipped"


class StageRecord(BaseModel):
    name: str
    status: RecordStatus
    detail: str = ""
    executor: StageExecutorKind = StageExecutorKind.DETERMINISTIC


class GateRecord(BaseModel):
    id: str
    label: str
    status: RecordStatus
    required: bool = True
    detail: str = ""


class CertificationReport(BaseModel):
    schema_version: int = CERTIFICATION_SCHEMA_VERSION
    compliance_profile: str
    certified: bool
    repo_path: str
    out_dir: str
    timestamp: str
    generative_executor: GenerativeExecutor = GenerativeExecutor.NONE
    # Bare-minimum honesty: certified is a fold over recorded stage/gate rows,
    # not Stage-0 covering / gap_probe / doc-quality completeness.
    completeness_claim: Literal["fold_of_recorded_rows"] = "fold_of_recorded_rows"
    profile_gate_ids: list[str] = Field(default_factory=list)
    stages: list[StageRecord] = Field(default_factory=list)
    gates: list[GateRecord] = Field(default_factory=list)
    failures: list[str] = Field(default_factory=list)


def gates_required_for_profile(profile: ComplianceProfile) -> frozenset[str]:
    """Return stable gate IDs required for certification under a profile."""
    if profile == ComplianceProfile.SCAN_ONLY:
        return frozenset({SCAN_ONLY_GATE_ID})
    if profile == ComplianceProfile.DETERMINISTIC_ONLY:
        return frozenset({DETERMINISTIC_ONLY_GATE_ID})
    return CERTIFIED_GATE_IDS
