"""Phase 7: full gates + post-run checks + finalize + drift + certification."""

from __future__ import annotations

from doc_engine.paths import repo_root
from doc_engine.pipeline import gates
from doc_engine.pipeline.local_runner_phases.artifact_inventory import (
    artifact_inventory,
)
from doc_engine.pipeline.local_runner_phases.certification_finish import (
    write_certification_and_finish,
)
from doc_engine.pipeline.local_runner_phases.drift_check_phase import run_drift_check
from doc_engine.pipeline.local_runner_phases.full_finish_gates import (
    run_check_pipeline_output_gate,
    run_citation_and_secrets_gates,
    run_finalize_manifest,
    run_pipeline_stages_real_suite,
    run_validate_artifact_gates,
)
from doc_engine.pipeline.local_runner_phases.state import LocalRunState

# Climb tests monkeypatch these on the façade module.
REPO_ROOT = str(repo_root())

__all__ = [
    "REPO_ROOT",
    "artifact_inventory",
    "gates",
    "phase_full_finish",
    "run_drift_check",
    "write_certification_and_finish",
]


def phase_full_finish(state: LocalRunState) -> int:
    """Run certified-profile gates, finalize, drift, and write certification."""
    log, runner, args = state.log, state.runner, state.args
    repo_path, out_dir, docs_dir, py = (
        state.repo_path,
        state.out_dir,
        state.docs_dir,
        state.py,
    )

    log.rule("GATES AND POST-RUN CHECKS (real)")
    run_validate_artifact_gates(runner, out_dir, repo_path)
    run_check_pipeline_output_gate(log, runner, args, docs_dir, repo_path)
    run_citation_and_secrets_gates(
        runner,
        docs_dir,
        repo_path,
        out_dir,
        strict=state.strict_citations_effective,
    )
    run_pipeline_stages_real_suite(log, runner, py, out_dir, repo_path, docs_dir)

    log.rule("FINALIZE (real)")
    run_finalize_manifest(runner, state, docs_dir, out_dir)
    run_drift_check(
        log, runner, repo_path, state.manifest, out_dir, args, state.signals_path
    )
    artifact_inventory(log, out_dir)
    if args.docs_in_target_repo:
        log("")
        log(f"  plus the fourteen docs written into {docs_dir}")

    return write_certification_and_finish(
        log,
        runner,
        state.profile,
        repo_path,
        out_dir,
        "mock",
        allow_mock=state.allow_mock,
        success_lines=[
            "RESULT: every gate passed. Remember Stages 1-4 were mocked: this says the "
            "wiring and the checks work, not that any document is correct.",
        ],
    )
