"""Invoke the Rust ``vacuous`` crate (pinned wheel) for certain findings."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Sequence

from doc_engine.ci.vacuity.astgrep_engine import VacuityHit


def run_vacuous_engine(
    repo: Path,
    roots: Sequence[str],
    *,
    vacuous_bin: str = "vacuous",
    min_confidence: str = "certain",
) -> list[VacuityHit]:
    """Run ``vacuous check`` per root; missing binary is a hard finding."""
    if shutil.which(vacuous_bin) is None:
        return [
            VacuityHit(
                "vacuous__tool_missing",
                vacuous_bin,
                0,
                "vacuous binary not on PATH — pin vacuous in requirements.txt",
            )
        ]
    hits: list[VacuityHit] = []
    for root in roots:
        hits.extend(
            _check_root(
                repo,
                root,
                vacuous_bin=vacuous_bin,
                min_confidence=min_confidence,
            )
        )
    return hits


def _check_root(
    repo: Path,
    root: str,
    *,
    vacuous_bin: str,
    min_confidence: str,
) -> list[VacuityHit]:
    target = repo / root
    if not target.is_dir():
        return []
    completed = subprocess.run(
        [
            vacuous_bin,
            "check",
            str(target),
            "--format",
            "json",
            "--min-confidence",
            min_confidence,
            "--no-baseline",
        ],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1):
        return [
            VacuityHit(
                "vacuous__engine_error",
                str(target),
                0,
                (completed.stderr or completed.stdout or "vacuous failed")[:500],
            )
        ]
    return _parse_vacuous_json(completed.stdout, root)


def _parse_vacuous_json(stdout: str, root_label: str) -> list[VacuityHit]:
    text = (stdout or "").strip()
    if not text:
        return []
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return [
            VacuityHit(
                "vacuous__engine_error",
                root_label,
                0,
                "vacuous JSON parse failed",
            )
        ]
    return _findings_to_hits(payload)


def _findings_to_hits(payload: object) -> list[VacuityHit]:
    findings = payload.get("findings") if isinstance(payload, dict) else None
    if not isinstance(findings, list):
        return []
    out: list[VacuityHit] = []
    for row in findings:
        hit = _finding_row(row)
        if hit is not None:
            out.append(hit)
    return out


def _finding_row(row: object) -> VacuityHit | None:
    if not isinstance(row, dict):
        return None
    rule = str(row.get("rule") or "unknown")
    return VacuityHit(
        rule_id=f"vacuous_crate__{rule}",
        path=str(row.get("file") or ""),
        line=int(row.get("line") or 0),
        text=str(row.get("message") or row.get("test") or "")[:240],
    )
