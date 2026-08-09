"""Shared runtime helpers for the local pipeline runner (Log, Runner, finish).

Concept modules: ``runner_log``, ``runner``, ``runner_spawn``, ``stage_recording``,
``certification_finish``, ``inventory_drift``. This façade keeps the stable
``local_runner_phases.support`` import path used by phase modules and tests.
"""

from __future__ import annotations

from doc_engine.pipeline.local_runner_phases.certification_finish import (
    build_and_write_certification as _build_and_write_certification,
    certification_failure_summary as _certification_failure_summary,
    close_certification_log as _close_certification_log,
    emit_certification_outcome as _emit_certification_outcome,
    emit_log_lines as _emit_log_lines,
    failed_required_gate_ids as _failed_required_gate_ids,
    failed_stage_names as _failed_stage_names,
    write_certification_and_finish as _write_certification_and_finish,
)
from doc_engine.pipeline.local_runner_phases.inventory_drift import (
    artifact_inventory as _artifact_inventory,
    py_mod as _py_mod,
    run_drift_check as _run_drift_check,
)
from doc_engine.pipeline.local_runner_phases.runner import Runner
from doc_engine.pipeline.local_runner_phases.runner_log import (
    Log,
    reconfigure_stdio_utf8 as _reconfigure_stdio_utf8,
)
from doc_engine.pipeline.local_runner_phases.stage_recording import (
    _RUNNER_FAIL_STATUSES,
    classify_subprocess_status as _classify_subprocess_status,
    gate_status_from_runner_status as _gate_status_from_runner_status,
    quote as _quote,
    record_one_pipeline_stage as _record_one_pipeline_stage,
    record_pipeline_stage_results as _record_pipeline_stage_results,
    stage_result_detail as _stage_result_detail,
)

__all__ = [
    "Log",
    "Runner",
    "_RUNNER_FAIL_STATUSES",
    "_artifact_inventory",
    "_build_and_write_certification",
    "_certification_failure_summary",
    "_classify_subprocess_status",
    "_close_certification_log",
    "_emit_certification_outcome",
    "_emit_log_lines",
    "_failed_required_gate_ids",
    "_failed_stage_names",
    "_gate_status_from_runner_status",
    "_py_mod",
    "_quote",
    "_reconfigure_stdio_utf8",
    "_record_one_pipeline_stage",
    "_record_pipeline_stage_results",
    "_run_drift_check",
    "_stage_result_detail",
    "_write_certification_and_finish",
]
