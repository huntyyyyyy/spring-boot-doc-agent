"""Subprocess spawn helpers for the local Runner."""

from __future__ import annotations

import subprocess
import time

from doc_engine.core.timeouts import tool_timeout_seconds


def record_spawn_error(
    runner,
    label: str,
    elapsed: float,
    detail: str,
    *,
    gate: bool,
    gate_id: str | None,
    critical: bool,
) -> None:
    runner.record(label, "ERROR", elapsed, detail)
    if gate:
        runner._maybe_record_gate(gate_id, label, "ERROR", detail)
    runner._abort_on_critical_spawn_failure(critical=critical)


def handle_spawn_exception(
    runner,
    label: str,
    started: float,
    timeout: float,
    exc: BaseException,
    *,
    gate: bool,
    gate_id: str | None,
    critical: bool,
) -> None:
    elapsed = time.time() - started
    if isinstance(exc, subprocess.TimeoutExpired):
        detail = f"timed out after {timeout}s"
        runner.log(f"  !! {detail}: {exc}")
    else:
        detail = str(exc)
        runner.log(f"  !! could not execute: {exc}")
    record_spawn_error(
        runner, label, elapsed, detail, gate=gate, gate_id=gate_id, critical=critical
    )


def spawn_step_process(
    runner,
    label: str,
    argv: list[str],
    *,
    cwd,
    env,
    started: float,
    gate: bool,
    gate_id: str | None,
    critical: bool,
):
    timeout = tool_timeout_seconds()
    try:
        return subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        handle_spawn_exception(
            runner,
            label,
            started,
            timeout,
            exc,
            gate=gate,
            gate_id=gate_id,
            critical=critical,
        )
        return None


def echo_process_output(runner, proc) -> None:
    body = (proc.stdout or "") + (proc.stderr or "")
    for line in body.rstrip("\n").splitlines():
        runner.log(f"  | {line}")


def record_step_outcome(
    runner,
    label: str,
    status: str,
    elapsed: float,
    returncode: int,
    *,
    gate: bool,
    gate_id: str | None,
) -> None:
    detail = f"exit {returncode}"
    runner.log(f"  -> exit {returncode} in {elapsed:.2f}s")
    runner.record(label, status, elapsed, detail)
    if gate:
        runner._maybe_record_gate(gate_id, label, status, detail)
