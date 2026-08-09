#!/usr/bin/env python3
"""Record a research-map Read receipt for look-first gating.

postToolUse matcher Read. Spec DOC7 — receipt tied to Read of
``docs/research/README.md``, not agent-authored markdown.

Usage::

    python3 .cursor/hooks/record_research_map_read.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from research_map_common import (
    MAP_REL,
    RECEIPT_DIR,
    is_research_map,
    paths_from_payload,
    receipt_path,
)


def _payload() -> dict:
    try:
        raw = json.loads(sys.stdin.read() or "{}")
    except (ValueError, TypeError):
        return {}
    return raw if isinstance(raw, dict) else {}


def main() -> int:
    raw = _payload()
    if any(is_research_map(path) for path in paths_from_payload(raw)):
        RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        receipt_path().write_text(MAP_REL + "\n", encoding="utf-8")
    print(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
