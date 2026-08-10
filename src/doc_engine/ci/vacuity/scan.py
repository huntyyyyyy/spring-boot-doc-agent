"""Compose ast-grep + vacuous(crate) + rg triage + telemetry into one verdict.

Hard fail: structural hits (ast-grep or vacuous) or empty hard-suite telemetry.
rg triage is ledger-only learning (text search is not citation/SoT alone).
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from doc_engine.ci.vacuity.astgrep_engine import (
    DEFAULT_ROOTS,
    VacuityHit,
    run_astgrep_vacuity,
)
from doc_engine.ci.vacuity.ripgrep_triage import RgTriageHit, run_rg_triage
from doc_engine.ci.vacuity.telemetry_ledger import (
    TelemetryVacuity,
    append_ledger,
    scan_latest_telemetry_empties,
)
from doc_engine.ci.vacuity.vacuous_engine import run_vacuous_engine


@dataclass(frozen=True)
class VacuityReport:
    """Hard-gate report: structural or empty telemetry ⇒ fail closed."""

    structural: tuple[VacuityHit, ...]
    telemetry: tuple[TelemetryVacuity, ...]
    triage: tuple[RgTriageHit, ...]
    ledger: Path | None

    @property
    def ok(self) -> bool:
        return not self.structural and not self.telemetry


def _git_sha(repo: Path) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return "unknown"
    return (completed.stdout or "").strip() or "unknown"


def _dedupe(hits: Sequence[VacuityHit]) -> tuple[VacuityHit, ...]:
    seen: set[tuple[str, str, int]] = set()
    out: list[VacuityHit] = []
    for hit in hits:
        key = (hit.rule_id, hit.path, hit.line)
        if key in seen:
            continue
        seen.add(key)
        out.append(hit)
    return tuple(out)


def scan_vacuity(
    repo: Path,
    roots: Sequence[str] = DEFAULT_ROOTS,
    *,
    write_ledger: bool = True,
) -> VacuityReport:
    """Scan test trees + latest telemetry; always ledger triage for learning."""
    structural = _dedupe(
        (
            *run_astgrep_vacuity(repo, roots),
            *run_vacuous_engine(repo, roots),
        )
    )
    triage = tuple(run_rg_triage(repo, roots))
    telemetry = tuple(scan_latest_telemetry_empties(repo))
    ledger: Path | None = None
    if write_ledger and (structural or telemetry or triage):
        ledger = append_ledger(
            repo,
            git_sha=_git_sha(repo),
            structural=structural,
            telemetry=telemetry,
            triage=triage,
        )
    return VacuityReport(
        structural=structural,
        telemetry=telemetry,
        triage=triage,
        ledger=ledger,
    )


def format_report(report: VacuityReport) -> str:
    lines = ["vacuity gate: FAIL" if not report.ok else "vacuity gate: OK"]
    for hit in report.structural:
        lines.append(f"  [{hit.rule_id}] {hit.path}:{hit.line}: {hit.text!r}")
    for row in report.telemetry:
        lines.append(
            f"  [telemetry__empty_hard_log] {row.suite} "
            f"log={row.log_relpath} bytes={row.bytes}"
        )
    if report.triage:
        lines.append(f"  rg triage candidates (learning only): {len(report.triage)}")
    if report.ledger is not None:
        lines.append(f"  ledger: {report.ledger}")
    return "\n".join(lines)
