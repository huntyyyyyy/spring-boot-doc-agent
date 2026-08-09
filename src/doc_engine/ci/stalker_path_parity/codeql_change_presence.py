"""G9: CodeQL fingerprint gate presence (E-TEL2 / E-CQL1)."""

from __future__ import annotations

from pathlib import Path

from doc_engine.ci.stalker_sensors.finding_records import KIND_G9, StalkerFinding


def scan_codeql_change_presence(root: Path) -> list[StalkerFinding]:
    """Fail closed when the E-CQL1 skip seam is absent (always-on waste)."""
    findings: list[StalkerFinding] = []
    gate = root / "scripts/ci/codeql_signals_change_gate.py"
    workflow = root / ".github/workflows/codeql-signals.yml"
    if not gate.is_file():
        findings.append(
            StalkerFinding(
                KIND_G9,
                "codeql_signals_change_gate.py missing",
                str(gate),
                backlog_pointer="E-CQL1",
            )
        )
    text = workflow.read_text(encoding="utf-8") if workflow.is_file() else ""
    if "run_expensive" not in text or "codeql_signals_change_gate" not in text:
        findings.append(
            StalkerFinding(
                KIND_G9,
                "codeql-signals.yml lacks fingerprint gate / if: seam",
                str(workflow),
                backlog_pointer="E-CQL1",
            )
        )
    return findings
