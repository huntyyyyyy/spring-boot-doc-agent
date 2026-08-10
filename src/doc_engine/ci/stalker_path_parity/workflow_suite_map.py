"""G10: remote-hard suite missing or advisory-only in local pre_pr (E-TEL2)."""

from __future__ import annotations

from pathlib import Path

from doc_engine.ci.stalker_sensors.finding_records import KIND_G10, StalkerFinding

# Suites that remote CI treats as hard evaluation — local must not soft-mask them.
REQUIRED_LOCAL_HARD: tuple[str, ...] = (
    "oracle_coverage",
    "public_surface",
    "facade_poke_surface",
)


def scan_workflow_suite_map(root: Path) -> list[StalkerFinding]:
    """Flag missing local hard wiring for known remote-critical suite names."""
    pre_pr = root / "scripts/ci/pre_pr.py"
    text = pre_pr.read_text(encoding="utf-8") if pre_pr.is_file() else ""
    findings: list[StalkerFinding] = []
    for name in REQUIRED_LOCAL_HARD:
        if f'"{name}"' not in text and f"'{name}'" not in text:
            findings.append(
                StalkerFinding(
                    KIND_G10,
                    f"pre_pr missing hard suite {name!r}",
                    str(pre_pr),
                    backlog_pointer="E-TEL2",
                )
            )
    return findings
