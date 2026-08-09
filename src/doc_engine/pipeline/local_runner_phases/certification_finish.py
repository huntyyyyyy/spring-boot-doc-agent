"""Certification write + finish helpers for local-runner phases."""

from __future__ import annotations

import os

from doc_engine.pipeline.compliance import (
    build_certification_report,
    stage_records_from_runner_results,
    write_certification_json,
)


def failed_required_gate_ids(runner) -> list[str]:
    return [
        gate.id
        for gate in runner.gate_records
        if gate.required and gate.status != "ok"
    ]


def failed_stage_names(report) -> list[str]:
    return [stage.name for stage in report.stages if stage.status != "ok"]


def certification_failure_summary(runner, report) -> str:
    parts = []
    failed_stages = failed_stage_names(report)
    failed_gates = failed_required_gate_ids(runner)
    if failed_stages:
        parts.append(f"stages: {', '.join(failed_stages)}")
    if failed_gates:
        parts.append(f"gates: {', '.join(failed_gates)}")
    return f"RESULT: certification failed — {'; '.join(parts)}"


def emit_log_lines(log, lines) -> None:
    if not lines:
        return
    for line in lines:
        log(line)


def emit_certification_outcome(log, runner, report, success_lines, notice_lines) -> None:
    emit_log_lines(log, notice_lines)
    if report.certified:
        emit_log_lines(log, success_lines)
        return
    if not notice_lines:
        log(certification_failure_summary(runner, report))


def build_and_write_certification(
    runner,
    profile,
    repo_path,
    out_dir,
    generative_executor,
    *,
    allow_mock=False,
):
    report = build_certification_report(
        profile,
        repo_path,
        out_dir,
        stage_records_from_runner_results(runner.results),
        runner.gate_records,
        generative_executor=generative_executor,
        allow_mock=allow_mock,
    )
    cert_path = write_certification_json(out_dir, report)
    return report, cert_path


def close_certification_log(log, report, cert_path, out_dir) -> None:
    log(f"  certification: {report.certified} -> {cert_path}")
    log(f"Full transcript: {os.path.join(out_dir, 'run.log')}")
    log.close()


def write_certification_and_finish(
    log,
    runner,
    profile,
    repo_path,
    out_dir,
    generative_executor,
    *,
    allow_mock=False,
    show_table=True,
    success_lines=None,
    notice_lines=None,
):
    if show_table:
        runner.table()

    report, cert_path = build_and_write_certification(
        runner,
        profile,
        repo_path,
        out_dir,
        generative_executor,
        allow_mock=allow_mock,
    )
    log("")
    emit_certification_outcome(log, runner, report, success_lines, notice_lines)
    close_certification_log(log, report, cert_path, out_dir)
    return 0 if report.certified else 1
