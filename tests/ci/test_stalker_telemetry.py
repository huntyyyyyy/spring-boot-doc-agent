"""Tests for stalker telemetry ETL + G7 masked advisory (E-TEL1)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from doc_engine.ci.stalker_sensors.masked_advisory import scan_masked_advisory
from doc_engine.ci.stalker_telemetry.run_store import (
    TelemetryRun,
    latest_index,
    telemetry_root,
)

pytestmark = pytest.mark.domain_ci_meta


def test_telemetry_records_error_excerpt_for_nonzero(tmp_path: Path) -> None:
    run = TelemetryRun(tmp_path, "deadbeef", "fast")
    body = (
        "Traceback (most recent call last):\n"
        "  File \"x.py\", line 1\n"
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
