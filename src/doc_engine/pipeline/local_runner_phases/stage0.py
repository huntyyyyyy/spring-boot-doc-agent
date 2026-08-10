"""Phase 3: Stage 0 deterministic PipelineRunner + early abort certification."""

from __future__ import annotations

from typing import Optional

from doc_engine.pipeline.executor import MockStageExecutor
from doc_engine.pipeline.local_runner_phases.certification_finish import (
    write_certification_and_finish,
)
from doc_engine.pipeline.local_runner_phases.stage_recording import (
    record_pipeline_stage_results,
)
from doc_engine.pipeline.local_runner_phases.state import LocalRunState
from doc_engine.pipeline.runner import PipelineRunner


def phase_stage0(state: LocalRunState) -> Optional[int]:
    """Run deterministic Stage 0. Returns an exit code when the run aborts."""
    log = state.log
    runner = state.runner
    assert state.pipeline_ctx is not None

    log.rule("STAGE 0 — deterministic (PipelineRunner, real scripts)")
    det_runner = PipelineRunner(
        generative_executor=MockStageExecutor({}),
        stages=state.deterministic_specs,
    )
    record_pipeline_stage_results(
        runner, det_runner.run(state.pipeline_ctx), ok_status="OK"
    )

    if runner.aborted:
        return write_certification_and_finish(
            log,
            runner,
            state.profile,
            state.repo_path,
            state.out_dir,
            "none",
            allow_mock=state.allow_mock,
            notice_lines=["Run aborted before later stages — see above."],
        )
    return None
