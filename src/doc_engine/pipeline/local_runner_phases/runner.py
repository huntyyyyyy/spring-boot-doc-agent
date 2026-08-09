"""Subprocess step Runner for the local pipeline (record table + abort)."""

from __future__ import annotations

import time

from doc_engine.pipeline.local_runner_phases.runner_spawn import (
    echo_process_output,
    record_step_outcome,
    spawn_step_process,
)
from doc_engine.pipeline.local_runner_phases.stage_recording import (
    _RUNNER_FAIL_STATUSES,
    classify_subprocess_status,
    gate_status_from_runner_status,
    quote,
)


class Runner:
    """Runs the pipeline's steps, records each one's outcome, prints a table."""

    def __init__(self, log, keep_going):
        self.log = log
        self.keep_going = keep_going
        self.results = []  # (label, status, seconds, detail)
        self.gate_records = []
        self.aborted = False

    def record(self, label, status, seconds, detail=""):
        self.results.append((label, status, seconds, detail))

    def _record_gate(self, gate_id, label, status, detail="", required=True):
        from doc_engine.pipeline.compliance import GateRecord

        self.gate_records.append(
            GateRecord(
                id=gate_id,
                label=label,
                status=gate_status_from_runner_status(status),
                required=required,
                detail=detail,
            )
        )

    def _maybe_record_gate(self, gate_id, label, status, detail=""):
        if gate_id:
            self._record_gate(gate_id, label, status, detail)

    def _mark_critical_abort(self, label: str) -> None:
        if self.keep_going:
            return
        self.log("")
        self.log(
            f"  !! {label} is a prerequisite for every later stage "
            f"— stopping. Re-run with --keep-going to push past it."
        )
        self.aborted = True

    def _abort_on_critical_spawn_failure(self, *, critical: bool) -> None:
        """Abort silently on spawn failure (no prerequisite banner)."""
        if critical and not self.keep_going:
            self.aborted = True

    def _log_step_header(self, label: str, argv: list[str], *, quiet: bool) -> None:
        printable = " ".join(quote(arg) for arg in argv)
        if quiet:
            self.log(f"  $ {printable}")
            return
        self.log("")
        self.log(f"--- {label}")
        self.log(f"  $ {printable}")

    def run(
        self,
        label,
        argv,
        gate=False,
        gate_id=None,
        critical=False,
        cwd=None,
        env=None,
        quiet=False,
    ):
        """Run one subprocess, echoing its exact command line and full output.

        gate=True     a non-zero exit is a real failure of the run, not just
                      information — it lands in the table as FAIL and makes
                      this script's own exit code non-zero.
        critical=True a non-zero exit means nothing downstream can be
                      meaningful, so stop (unless --keep-going).
        quiet=True    for the manifest bookkeeping calls, whose one-line
                      output would otherwise drown the stages themselves.
        """
        if self.aborted:
            self.record(label, "SKIPPED", 0.0, "aborted earlier")
            return None

        self._log_step_header(label, argv, quiet=quiet)
        started = time.time()
        proc = spawn_step_process(
            self,
            label,
            argv,
            cwd=cwd,
            env=env,
            started=started,
            gate=gate,
            gate_id=gate_id,
            critical=critical,
        )
        if proc is None:
            return None

        elapsed = time.time() - started
        echo_process_output(self, proc)
        status = classify_subprocess_status(proc.returncode, gate=gate)
        record_step_outcome(
            self, label, status, elapsed, proc.returncode, gate=gate, gate_id=gate_id
        )
        if proc.returncode != 0 and critical:
            self._mark_critical_abort(label)
        return proc

    def mock(self, label, fn):
        """Run one of the four mocked LLM stages."""
        if self.aborted:
            self.record(label, "SKIPPED", 0.0, "aborted earlier")
            return None
        self.log("")
        self.log(f"--- {label}")
        started = time.time()
        try:
            detail = fn()
        except Exception as exc:  # a broken mock shouldn't look like a gate failure
            elapsed = time.time() - started
            self.log(f"  !! mock stage raised: {exc!r}")
            self.record(label, "ERROR", elapsed, repr(exc))
            if not self.keep_going:
                self.aborted = True
            return None
        elapsed = time.time() - started
        self.record(label, "MOCK", elapsed, detail or "")
        self.log(f"  -> {detail}")
        self.log(f"  -> {elapsed:.2f}s")
        return detail

    def gates_failed(self):
        return [
            result for result in self.results if result[1] in _RUNNER_FAIL_STATUSES
        ]

    def table(self):
        self.log.rule("STEP RESULTS")
        width = max(len(result[0]) for result in self.results)
        for label, status, seconds, detail in self.results:
            self.log(f"  {status:<8} {label:<{width}}  {seconds:6.2f}s  {detail}")
