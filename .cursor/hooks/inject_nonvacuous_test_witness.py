#!/usr/bin/env python3
"""Cursor postToolUse: when tests are written, inject non-vacuous receipt rule.

After Write|StrReplace|EditNotebook on ``tests/**``, remind the agent that
logging/telemetry/sensor/gate tests must fail closed on empty receipts
(green run → non-empty body bound to HEAD). Exit-only is not observation.

Spec: docs/research/process/35-control-plane-closed-loop-2026.md (CPL2/CPL3/CPL5)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from research_map_common import paths_from_payload, repo_relative

CONTEXT = (
    "Non-vacuous receipt rule (when writing/editing tests for logging, "
    "telemetry, sensors, pre_pr, or gates): include a fail-closed witness that "
    "a green run produces a non-empty receipt/log body (bound to this worktree "
    "HEAD where applicable); empty receipt must fail the suite or overall. "
    "Exit-only is not observation. Standing suite: "
    "tests/ci/test_stalker_telemetry.py "
    "(test_success_run_keeps_warning_excerpt + live tee getvalue). "
    "Spec: docs/research/process/35-control-plane-closed-loop-2026.md "
    "CPL2/CPL3/CPL5; habit from E-TEL vacuous-log RCA."
)


def _is_test_rel(rel: str) -> bool:
    return rel.startswith("tests/") and (
        rel.endswith(".py") or rel.endswith(".ipynb")
    )


def main() -> int:
    try:
        raw = json.loads(sys.stdin.read() or "{}")
    except (ValueError, TypeError):
        return 0
    if not isinstance(raw, dict):
        return 0
    rels = [repo_relative(path) for path in paths_from_payload(raw)]
    if not any(_is_test_rel(rel) for rel in rels):
        return 0
    print(json.dumps({"additional_context": CONTEXT}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
