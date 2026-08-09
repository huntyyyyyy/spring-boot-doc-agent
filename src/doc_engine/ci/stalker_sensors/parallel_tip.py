"""G5: more than one Active tip stream in quality-backlog."""

from __future__ import annotations

from pathlib import Path

from doc_engine.ci.stalker_sensors.finding_records import KIND_G5, StalkerFinding


def _active_tip_lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if line.startswith("**Active:**") and "Spec draft" not in line
    ]


def scan_parallel_tip(root: Path) -> list[StalkerFinding]:
    backlog = root / "docs" / "research" / "quality-backlog.md"
    if not backlog.is_file():
        return [StalkerFinding(KIND_G5, "quality-backlog.md missing", str(backlog))]
    actives = _active_tip_lines(backlog.read_text(encoding="utf-8"))
    if len(actives) == 1:
        return []
    if not actives:
        return [
            StalkerFinding(
                KIND_G5,
                "no **Active:** tip line in backlog posture",
                "set one Active Implement stream",
            )
        ]
    return [
        StalkerFinding(
            KIND_G5,
            f"{len(actives)} Active tip lines (want 1)",
            " | ".join(actives),
        )
    ]
