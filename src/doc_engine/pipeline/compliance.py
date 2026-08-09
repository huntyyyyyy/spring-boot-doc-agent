"""Compliance profiles, gate checklists, and certification.json emission.

``certification.json`` is a **derived view** over stage/gate facts: only
``build_certification_report`` (in ``certification_fold``) computes
``certified`` / ``failures``. ``completeness_claim`` is always
``fold_of_recorded_rows`` — the bit is not Stage-0 covering / gap
measurement / doc quality. See
``claude/research/certification-derived-view-2026-07-30.md`` and
``docs/design/ddia-north-star/deviations/dev-certification-derived-view.md``.

Concept modules: ``compliance_models``, ``compliance_profile``,
``compliance_stages``, ``certification_fold``. This façade keeps the stable
``doc_engine.pipeline.compliance`` import path.
"""

from __future__ import annotations

from doc_engine.pipeline.compliance_models import (
    CERTIFICATION_SCHEMA_VERSION,
    CERTIFIED_GATE_IDS,
    DETERMINISTIC_ONLY_GATE_ID,
    GENERATIVE_EXTERNAL_STAGE,
    SCAN_ONLY_GATE_ID,
    CertificationReport,
    ComplianceProfile,
    GateRecord,
    GenerativeExecutor,
    RecordStatus,
    StageExecutorKind,
    StageRecord,
    gates_required_for_profile,
)
from doc_engine.pipeline.compliance_profile import (
    citations_are_strict,
    deterministic_stage_names,
    generative_stage_names,
    required_stage_names_for_profile,
    resolve_compliance_profile,
    scan_only_specs as _scan_only_specs,
    specs_for_profile as _specs_for_profile,
    stages_for_profile,
    truncate_until_stage as _truncate_until_stage,
)
from doc_engine.pipeline.compliance_stages import (
    generative_stage_executor as _generative_stage_executor,
    normalize_kept_prior_stage as _normalize_kept_prior_stage,
    should_drop_prior_stage as _should_drop_prior_stage,
    skipped_stage_executor as _skipped_stage_executor,
    stage_executor_from_runner as _stage_executor_from_runner,
    stage_records_from_runner_results,
    stage_status_from_runner as _stage_status_from_runner,
    stages_for_live_certification,
    write_certification_json,
)

# Late import: fold module depends on types/helpers above; re-export keeps
# `from doc_engine.pipeline.compliance import build_certification_report` stable.
from doc_engine.pipeline.certification_fold import (  # noqa: E402, F401
    build_certification_report,
)

__all__ = [
    "CERTIFICATION_SCHEMA_VERSION",
    "CERTIFIED_GATE_IDS",
    "DETERMINISTIC_ONLY_GATE_ID",
    "GENERATIVE_EXTERNAL_STAGE",
    "SCAN_ONLY_GATE_ID",
    "CertificationReport",
    "ComplianceProfile",
    "GateRecord",
    "GenerativeExecutor",
    "RecordStatus",
    "StageExecutorKind",
    "StageRecord",
    "build_certification_report",
    "citations_are_strict",
    "deterministic_stage_names",
    "gates_required_for_profile",
    "generative_stage_names",
    "required_stage_names_for_profile",
    "resolve_compliance_profile",
    "stage_records_from_runner_results",
    "stages_for_live_certification",
    "stages_for_profile",
    "write_certification_json",
]
