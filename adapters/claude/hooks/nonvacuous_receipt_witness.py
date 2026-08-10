"""Non-vacuous receipt witness for control-plane / telemetry changes.

A gate that stores exit codes but empty suite logs is not observation.
When control-plane modules are staged, require the standing pytest witness
that a green run still produces a non-empty body/excerpt (E-TEL / E-CPL0).
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Set

# Paths whose staged edits demand the non-vacuous receipt witness suite.
CONTROL_PLANE_FRAGMENTS = (
    "stalker_telemetry",
    "stalker_sensors",
    "stalker_path_parity",
    "scripts/ci/pre_pr.py",
    "oracle_push_policy",
    "mutation_driver",
    "codeql_signals_change_gate",
)

WITNESS_REL = "tests/ci/test_stalker_telemetry.py"

# Markers that must all appear in the witness suite (fail-closed if missing).
REQUIRED_MARKERS = (
    "test_success_run_keeps_warning_excerpt",
    "getvalue()",
    "WARNING",
    "empty_telemetry",
)


def is_control_plane_path(rel: str) -> bool:
    norm = rel.replace("\\", "/")
    return any(fragment in norm for fragment in CONTROL_PLANE_FRAGMENTS)


def missing_nonvacuous_witness(
    repo: Path,
    staged: List[str],
    deletions: Optional[Set[str]] = None,
) -> List[str]:
    """Return problems when staged control-plane edits lack the witness suite."""
    deleted = deletions if deletions is not None else set()
    relevant = [
        rel
        for rel in staged
        if rel not in deleted and is_control_plane_path(rel)
    ]
    if not relevant:
        return []
    witness = repo / WITNESS_REL
    if not witness.is_file():
        return [
            f"control-plane edit ({relevant[0]}) requires {WITNESS_REL} "
            f"with a non-vacuous receipt witness (green run → non-empty "
            f"log/excerpt; empty receipt must fail). See E-CPL0 CPL2/CPL3."
        ]
    text = witness.read_text(encoding="utf-8")
    missing = [marker for marker in REQUIRED_MARKERS if marker not in text]
    if not missing:
        return []
    return [
        f"{WITNESS_REL} is missing non-vacuous receipt markers {missing!r} "
        f"while staging {relevant[0]}. Green telemetry must assert non-empty "
        f"body/excerpt (exit-only is not observation)."
    ]
