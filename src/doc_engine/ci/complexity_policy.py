"""Complexity policy setpoints — single owner for complexipy ceilings.

Consumers import ``COMPLEXITY_MAX`` / ``DEFAULT_BASELINE``; do not re-literal
``5`` in gate strategies or ratchets.
"""

from __future__ import annotations

import json
from pathlib import Path

from doc_engine.ci.gate_tools import REPO_ROOT

COMPLEXITY_MAX = 5
DEFAULT_BASELINE = REPO_ROOT / "scripts" / "ratchets" / "complexipy_baseline.json"
SCHEMA_VERSION = 1


def baseline_offender_ceiling(path: Path = DEFAULT_BASELINE) -> int | None:
    """Return committed ratchet ceiling, or None if missing/unreadable."""
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return int(data["offender_count"])
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None
