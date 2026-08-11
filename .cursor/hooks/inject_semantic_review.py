#!/usr/bin/env python3
"""beforeSubmitPrompt: inject semantic-review mandate on adversarial asks.

When the user prompt looks like an architecture / adversarial review, inject
if→then discipline and arm the afterAgentResponse/stop rewrite loop.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from semantic_review_common import (  # noqa: E402
    INJECT_CONTEXT,
    mark_review_active,
    prompt_is_review,
)


def main() -> int:
    try:
        raw = json.loads(sys.stdin.read() or "{}")
    except (ValueError, TypeError):
        print(json.dumps({"continue": True}))
        return 0
    if not isinstance(raw, dict):
        print(json.dumps({"continue": True}))
        return 0
    prompt = raw.get("prompt") if isinstance(raw.get("prompt"), str) else ""
    if prompt_is_review(prompt):
        mark_review_active(prompt)
        print(
            json.dumps(
                {
                    "continue": True,
                    "additional_context": INJECT_CONTEXT,
                }
            )
        )
        return 0
    print(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
