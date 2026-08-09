"""StageRecord conversion and live-gates certification stage rewrite."""

from __future__ import annotations

import json
from pathlib import Path

from doc_engine.pipeline.compliance_models import (
    GENERATIVE_EXTERNAL_STAGE,
    CertificationReport,
    RecordStatus,
    StageExecutorKind,
    StageRecord,
)
from doc_engine.pipeline.compliance_profile import (
    deterministic_stage_names,
    generative_stage_names,
)


def stage_status_from_runner(status: str) -> RecordStatus:
    if status in ("OK", "MOCK"):
        return RecordStatus.OK
    if status == "SKIPPED":
        return RecordStatus.SKIPPED
    return RecordStatus.FAIL


def skipped_stage_executor(stage_name: str) -> StageExecutorKind:
    """Executor stamp for a SKIPPED runner stage row."""
    if stage_name in generative_stage_names():
        return StageExecutorKind.NONE
    return StageExecutorKind.DETERMINISTIC


def generative_stage_executor(status: str) -> StageExecutorKind:
    """Executor stamp for a non-skipped generative stage."""
    # OK without MOCK ⇒ non-mock generative adapter (live-in-runner).
    # Fail/error must not be labelled live.
    if status == "OK":
        return StageExecutorKind.LIVE
    return StageExecutorKind.NONE


def stage_executor_from_runner(
    status: str,
    stage_name: str,
) -> StageExecutorKind:
    """Preserve mock-ness; classify OK stages by graph kind."""
    if status == "MOCK":
        return StageExecutorKind.MOCK
    if status == "SKIPPED":
        return skipped_stage_executor(stage_name)
    if stage_name not in generative_stage_names():
        return StageExecutorKind.DETERMINISTIC
    return generative_stage_executor(status)


def write_certification_json(out_dir: str | Path, report: CertificationReport) -> Path:
    """Write certification.json into the run artifact directory."""
    path = Path(out_dir) / "certification.json"
    path.write_text(
        json.dumps(report.model_dump(), indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def should_drop_prior_stage(
    stage: StageRecord,
    deterministic_names: frozenset[str],
    generative_names: frozenset[str],
) -> bool:
    """True when a prior stage row must not survive a live gates rewrite."""
    if stage.name in generative_names or stage.name == GENERATIVE_EXTERNAL_STAGE:
        return True
    if stage.executor in (StageExecutorKind.MOCK, StageExecutorKind.LIVE):
        return True
    if (
        stage.name not in deterministic_names
        and stage.executor != StageExecutorKind.DETERMINISTIC
    ):
        return True
    return False


def normalize_kept_prior_stage(
    stage: StageRecord,
    deterministic_names: frozenset[str],
) -> StageRecord | None:
    """Return a kept prior row (deterministic-labelled), or None to drop."""
    if stage.name in deterministic_names:
        if stage.executor != StageExecutorKind.DETERMINISTIC:
            return stage.model_copy(
                update={"executor": StageExecutorKind.DETERMINISTIC}
            )
        return stage
    if stage.executor == StageExecutorKind.DETERMINISTIC:
        # Non-graph deterministic-labelled row (unusual); keep as-is.
        return stage
    return None


def stages_for_live_certification(prior: list[StageRecord]) -> list[StageRecord]:
    """Derive stage facts for a live gates rewrite (not a LWW merge).

    Keep deterministic prior rows; drop generative history (including legacy v1
    rows that default ``executor=deterministic``); append ``generative_external``.
    """
    deterministic_names = deterministic_stage_names()
    generative_names = generative_stage_names()
    kept: list[StageRecord] = []
    for stage in prior:
        if should_drop_prior_stage(stage, deterministic_names, generative_names):
            continue
        normalized = normalize_kept_prior_stage(stage, deterministic_names)
        if normalized is not None:
            kept.append(normalized)
    kept.append(
        StageRecord(
            name=GENERATIVE_EXTERNAL_STAGE,
            status=RecordStatus.OK,
            executor=StageExecutorKind.LIVE,
            detail="docs produced outside PipelineRunner; proven by live gates",
        )
    )
    return kept


def stage_records_from_runner_results(
    results: list[tuple[str, str, float, str]],
    prefix: str = "pipeline:",
) -> list[StageRecord]:
    """Convert Runner.results entries for pipeline stages into StageRecords."""
    records: list[StageRecord] = []
    for label, status, _seconds, detail in results:
        if not label.startswith(prefix):
            continue
        name = label[len(prefix):]
        records.append(
            StageRecord(
                name=name,
                status=stage_status_from_runner(status),
                detail=detail,
                executor=stage_executor_from_runner(status, name),
            )
        )
    return records
