#!/usr/bin/env python3
"""stop: one rewrite follow-up when semantic-review audit found tautology.

loop_limit in hooks.json caps auto-follow-ups. Clears session state when the
review passes or the loop is exhausted.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from semantic_review_common import (  # noqa: E402
    FOLLOWUP,
    clear_state,
    load_state,
)


def main() -> int:
    try:
        raw = json.loads(sys.stdin.read() or "{}")
    except (ValueError, TypeError):
        print(json.dumps({}))
        return 0
    if not isinstance(raw, dict):
        print(json.dumps({}))
        return 0
    if raw.get("status") != "completed":
        print(json.dumps({}))
        return 0
    state = load_state()
    if not state.get("active"):
        print(json.dumps({}))
        return 0
    finding = state.get("finding")
    loop_count = raw.get("loop_count")
    loops = int(loop_count) if isinstance(loop_count, int) else 0
    if finding and loops < 2:
        # Keep active so the rewrite can be re-audited.
        print(json.dumps({"followup_message": FOLLOWUP}))
        return 0
    clear_state()
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
