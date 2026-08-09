"""Tests for stalker telemetry ETL + G7 masked advisory (E-TEL1)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from doc_engine.ci.stalker_sensors.masked_advisory import scan_masked_advisory
from doc_engine.ci.stalker_telemetry.run_store import (
    TelemetryRun,
    latest_index,
    tee_stdio,
    telemetry_root,
)

pytestmark = pytest.mark.domain_ci_meta


def test_telemetry_records_error_excerpt_for_nonzero(tmp_path: Path) -> None:
    run = TelemetryRun(tmp_path, "deadbeef", "fast")
    body = (
        "Traceback (most recent call last):\n"
        '  File "x.py", line 1\n'
        "ModuleNotFoundError: No module named 'tests'\n"
    )
    run.record(
        name="mutation_driver_advisory",
        kind="advisory",
        status="advisory",
        exit_code=1,
        duration_ms=12,
        body=body,
    )
    idx = run.flush()
    data = json.loads(idx.read_text(encoding="utf-8"))
    assert data["suites"][0]["exit_code"] == 1
    assert "ModuleNotFoundError" in data["suites"][0]["error_excerpt"]
    assert (run.dir / "suites" / "mutation_driver_advisory.log").is_file()


def test_g7_flags_masked_advisory_nonzero(tmp_path: Path) -> None:
    run = TelemetryRun(tmp_path, "abc123", "full")
    run.record(
        name="mutation_driver_advisory",
        kind="advisory",
        status="advisory",
        exit_code=1,
        duration_ms=5,
        body="ModuleNotFoundError: No module named 'tests'\n",
    )
    run.record(
        name="ok_advisory",
        kind="advisory",
        status="advisory",
        exit_code=0,
        duration_ms=1,
        body="ok\n",
    )
    run.flush()
    findings = scan_masked_advisory(tmp_path)
    assert len(findings) == 1
    assert findings[0].kind == "masked_advisory_nonzero"
    assert "mutation_driver_advisory" in findings[0].summary


def test_g7_quiet_when_no_telemetry(tmp_path: Path) -> None:
    assert scan_masked_advisory(tmp_path) == []
    assert latest_index(tmp_path) is None
    assert telemetry_root(tmp_path).name == "pre-pr-telemetry"


def test_error_excerpt_falls_back_to_tail(tmp_path: Path) -> None:
    run = TelemetryRun(tmp_path, "cafe", "standard")
    run.record(
        name="plain_fail",
        kind="hard",
        status="fail",
        exit_code=2,
        duration_ms=3,
        body="line-a\nline-b\nline-c\n",
    )
    run.flush()
    data = json.loads((run.dir / "index.json").read_text(encoding="utf-8"))
    assert "line-c" in data["suites"][0]["error_excerpt"]


def test_flush_pointer_file_when_symlink_blocked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run = TelemetryRun(tmp_path, "pointer", "fast")
    run.record(
        name="ok",
        kind="hard",
        status="ok",
        exit_code=0,
        duration_ms=1,
        body="",
    )

    def _boom(*_a: object, **_k: object) -> None:
        raise OSError("no symlink")

    monkeypatch.setattr(Path, "symlink_to", _boom)
    run.flush()
    latest = telemetry_root(tmp_path) / "latest"
    assert latest.is_file()
    assert latest_index(tmp_path) == run.dir / "index.json"


def test_tee_stdio_captures_stdout_and_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    with tee_stdio() as buf:
        print("hello-out")
        print("hello-err", file=sys.stderr)
        # Live sink: getvalue must work *inside* the with (pre_pr historic bug).
        assert "hello-out" in buf.getvalue()
    text = buf.getvalue()
    assert "hello-out" in text
    assert "hello-err" in text
    captured = capsys.readouterr()
    assert "hello-out" in captured.out
    assert "hello-err" in captured.err


def test_success_run_keeps_warning_excerpt(tmp_path: Path) -> None:
    """Green suites must still surface WARNING/advisory lines in the excerpt."""
    run = TelemetryRun(tmp_path, "warnok", "standard")
    run.record(
        name="ruff",
        kind="hard",
        status="pass",
        exit_code=0,
        duration_ms=4,
        body="ok line\nWARNING deprecated rule X\nstill green\n",
    )
    run.flush()
    data = json.loads((run.dir / "index.json").read_text(encoding="utf-8"))
    excerpt = data["suites"][0]["error_excerpt"]
    assert "WARNING deprecated rule X" in excerpt
    log = (run.dir / "suites" / "ruff.log").read_text(encoding="utf-8")
    assert "WARNING deprecated rule X" in log


def test_g7_unreadable_index(tmp_path: Path) -> None:
    root = telemetry_root(tmp_path)
    run_dir = root / "x-fast-1"
    run_dir.mkdir(parents=True)
    (run_dir / "index.json").write_text("{bad", encoding="utf-8")
    (root / "latest").write_text(run_dir.name + "\n", encoding="utf-8")
    findings = scan_masked_advisory(tmp_path)
    assert findings and "unreadable" in findings[0].summary


def test_g7_skips_non_advisory_nonzero(tmp_path: Path) -> None:
    run = TelemetryRun(tmp_path, "hardfail", "full")
    run.record(
        name="pytest",
        kind="hard",
        status="fail",
        exit_code=1,
        body="ERROR boom\n",
        duration_ms=1,
    )
    run.flush()
    assert scan_masked_advisory(tmp_path) == []
