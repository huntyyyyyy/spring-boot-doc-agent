"""G7: advisory (or last-run) suites that exited non-zero — masked local green."""

from __future__ import annotations

import json
from pathlib import Path

from doc_engine.ci.stalker_sensors.finding_records import KIND_G7, StalkerFinding
from doc_engine.ci.stalker_telemetry.run_store import latest_index


def scan_masked_advisory(root: Path) -> list[StalkerFinding]:
    """Flag last telemetry index rows with kind=advisory and exit_code != 0."""
    idx_path = latest_index(root)
    if idx_path is None:
        return []
    try:
        data = json.loads(idx_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [
            StalkerFinding(
                KIND_G7,
                "telemetry index unreadable",
                str(idx_path),
                backlog_pointer="P25.1",
            )
        ]
    findings: list[StalkerFinding] = []
    for suite in data.get("suites") or []:
        if suite.get("kind") != "advisory":
            continue
        if int(suite.get("exit_code") or 0) == 0:
            continue
        excerpt = (suite.get("error_excerpt") or "")[:400]
        findings.append(
            StalkerFinding(
                KIND_G7,
                f"advisory suite {suite.get('name')!r} exit={suite.get('exit_code')}",
                excerpt or suite.get("log_relpath", ""),
                backlog_pointer="P25.1",
            )
        )
    return findings
