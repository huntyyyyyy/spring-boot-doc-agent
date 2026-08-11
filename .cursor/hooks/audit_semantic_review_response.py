#!/usr/bin/env python3
"""afterAgentResponse: flag tautological adversarial reviews.

If a review turn was armed by inject_semantic_review, scan the assistant text
for Support/Refuse scoreboards without if→then density. Record a finding for
the stop hook; never block the response channel.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from semantic_review_common import (  # noqa: E402
    clear_finding,
    load_state,
    record_finding,
    scan_review_text,
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
    state = load_state()
    if not state.get("active"):
        print(json.dumps({}))
        return 0
    text = raw.get("text") if isinstance(raw.get("text"), str) else ""
    bad, reasons = scan_review_text(text)
    if bad:
        record_finding(reasons)
    else:
        clear_finding()
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
