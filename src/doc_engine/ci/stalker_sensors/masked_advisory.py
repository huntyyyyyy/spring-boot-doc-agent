"""G7: advisory suites that exited non-zero — masked local green."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from doc_engine.ci.stalker_sensors.finding_records import KIND_G7, StalkerFinding
from doc_engine.ci.stalker_telemetry.run_store import latest_index


def _load_suites(idx_path: Path) -> list[dict[str, Any]] | StalkerFinding:
    try:
        data = json.loads(idx_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return StalkerFinding(
            KIND_G7,
            "telemetry index unreadable",
            str(idx_path),
            backlog_pointer="P25.1",
        )
    return list(data.get("suites") or [])


def _advisory_nonzero(suite: dict[str, Any]) -> StalkerFinding | None:
    if suite.get("kind") != "advisory":
        return None
    if int(suite.get("exit_code") or 0) == 0:
        return None
    excerpt = (suite.get("error_excerpt") or "")[:400]
    return StalkerFinding(
        KIND_G7,
        f"advisory suite {suite.get('name')!r} exit={suite.get('exit_code')}",
        excerpt or suite.get("log_relpath", ""),
        backlog_pointer="P25.1",
    )


def scan_masked_advisory(root: Path) -> list[StalkerFinding]:
    """Flag last telemetry index rows with kind=advisory and exit_code != 0."""
    idx_path = latest_index(root)
    if idx_path is None:
        return []
    loaded = _load_suites(idx_path)
    if isinstance(loaded, StalkerFinding):
        return [loaded]
    findings: list[StalkerFinding] = []
    for suite in loaded:
        item = _advisory_nonzero(suite)
        if item is not None:
            findings.append(item)
    return findings
