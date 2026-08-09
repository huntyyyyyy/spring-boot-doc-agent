"""Pipeline stage recording helpers shared by local-runner phases."""

from __future__ import annotations

_RUNNER_FAIL_STATUSES = frozenset({"FAIL", "ERROR"})


def stage_result_detail(stage_result) -> str:
    return stage_result.detail or stage_result.error or ""


def record_one_pipeline_stage(runner, stage_name, stage_result, *, ok_status: str) -> None:
    status = ok_status if stage_result.success else "FAIL"
    runner.record(
        f"pipeline:{stage_name}",
        status,
        0.0,
        stage_result_detail(stage_result),
    )
    if not stage_result.success:
        runner.aborted = True


def record_pipeline_stage_results(runner, results, *, ok_status: str) -> None:
    """Fold PipelineRunner results into the local Runner table + abort flag."""
    for stage_name, stage_result in results:
        record_one_pipeline_stage(
            runner, stage_name, stage_result, ok_status=ok_status
        )


def gate_status_from_runner_status(status: str) -> str:
    """Map Runner table status to certification gate status vocabulary."""
    if status == "OK":
        return "ok"
    if status == "SKIPPED":
        return "skipped"
    return "fail"


def classify_subprocess_status(returncode: int, *, gate: bool) -> str:
    """Map a subprocess exit code to the Runner table status vocabulary."""
    if returncode == 0:
        return "OK"
    if gate:
        return "FAIL"
    return "NONZERO"


def quote(arg):
    return f'"{arg}"' if " " in arg else arg
