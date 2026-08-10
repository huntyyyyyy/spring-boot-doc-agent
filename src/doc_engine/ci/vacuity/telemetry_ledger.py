"""Telemetry + ledger for vacuous observation learning (hybrid gate)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

from doc_engine.ci.vacuity.astgrep_engine import VacuityHit
from doc_engine.ci.vacuity.ripgrep_triage import RgTriageHit


@dataclass(frozen=True)
class TelemetryVacuity:
    """Empty hard-suite receipt from a prior pre_pr run."""

    suite: str
    log_relpath: str
    bytes: int


def ledger_path(repo: Path) -> Path:
    return repo / ".git" / "pre-pr-telemetry" / "vacuity-ledger.jsonl"


def scan_latest_telemetry_empties(repo: Path) -> list[TelemetryVacuity]:
    """Fail-closed evidence: hard suite logs with zero bytes are vacuous."""
    run_dir = _resolve_latest_run(repo / ".git" / "pre-pr-telemetry")
    if run_dir is None or not (run_dir / "index.json").is_file():
        return []
    data = json.loads((run_dir / "index.json").read_text(encoding="utf-8"))
    return _empty_hard_suites(run_dir, data.get("suites") or [])


def _resolve_latest_run(root: Path) -> Path | None:
    latest = root / "latest"
    if latest.is_symlink():
        return (root / latest.readlink()).resolve()
    if latest.is_file():
        name = latest.read_text(encoding="utf-8").strip()
        return root / name
    return None


def _empty_hard_suites(run_dir: Path, suites: object) -> list[TelemetryVacuity]:
    if not isinstance(suites, list):
        return []
    hits: list[TelemetryVacuity] = []
    for suite in suites:
        hit = _empty_hard_suite(run_dir, suite)
        if hit is not None:
            hits.append(hit)
    return hits


def _empty_hard_suite(run_dir: Path, suite: object) -> TelemetryVacuity | None:
    if not isinstance(suite, dict) or suite.get("kind") != "hard":
        return None
    rel = str(suite.get("log_relpath") or "")
    log = run_dir / rel
    size = log.stat().st_size if log.is_file() else 0
    if size != 0:
        return None
    return TelemetryVacuity(
        suite=str(suite.get("name") or rel),
        log_relpath=rel,
        bytes=size,
    )


def append_ledger(
    repo: Path,
    *,
    git_sha: str,
    structural: Sequence[VacuityHit],
    telemetry: Sequence[TelemetryVacuity],
    triage: Sequence[RgTriageHit] = (),
) -> Path:
    """Append one learning record (kinds + counts) for later diagnosis."""
    path = ledger_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "git_sha": git_sha,
        "kinds": _kind_counts(structural, telemetry, triage),
        "structural": [asdict(hit) for hit in structural],
        "telemetry": [asdict(row) for row in telemetry],
        "triage": [asdict(row) for row in triage],
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return path


def _kind_counts(
    structural: Sequence[VacuityHit],
    telemetry: Sequence[TelemetryVacuity],
    triage: Sequence[RgTriageHit],
) -> dict[str, int]:
    kinds: dict[str, int] = {}
    for hit in structural:
        kinds[hit.rule_id] = kinds.get(hit.rule_id, 0) + 1
    for hit in triage:
        kinds[hit.kind] = kinds.get(hit.kind, 0) + 1
    if telemetry:
        kinds["telemetry__empty_hard_log"] = len(telemetry)
    return kinds


def summarize_kinds(records: Iterable[dict]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for record in records:
        for kind, count in (record.get("kinds") or {}).items():
            totals[str(kind)] = totals.get(str(kind), 0) + int(count)
    return totals
