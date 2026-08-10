"""Append stalker findings under docs/research/findings/ (STK2)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from doc_engine.ci.stalker_sensors.finding_records import StalkerFinding


def write_findings_ledger(
    root: Path,
    findings: list[StalkerFinding],
    *,
    day: date | None = None,
) -> Path:
    stamp = (day or date.today()).isoformat()
    out_dir = root / "docs" / "research" / "findings"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{stamp}-stalker-scan.md"
    lines = [
        f"# Stalker scan — {stamp}",
        "",
        "Structured findings (E-STK1 / STK2). Advisory only — does not rewrite SoT.",
        "",
        f"Backlog: P15.1 · count={len(findings)}",
        "",
    ]
    if not findings:
        lines.append("No G1–G6 findings.")
    else:
        lines.extend(["| Kind | Summary | Evidence |", "| --- | --- | --- |"])
        for item in findings:
            lines.append(
                f"| `{item.kind}` | {item.summary} | {item.evidence} |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
