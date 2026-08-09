#!/usr/bin/env python3
"""Cursor beforeSubmitPrompt: inject research domain map into agent context.

Spec: docs/research/process/18-docs-research-taxonomy-claude-consolidation-2026.md
(DOC7 / DOC9). Cloud-safe (does not use sessionStart).

Usage::

    python3 .cursor/hooks/inject_research_map.py
"""

from __future__ import annotations

import json
import sys

MAP = "docs/research/README.md"
BACKLOG = "docs/research/quality-backlog.md"
SKILL = ".cursor/skills/principal-se-research-epic/SKILL.md"

CONTEXT = (
    f"Research SoR entry door: read `{MAP}` and pick a domain before weighing "
    f"frameworks or writing Spec/Implement. Active stream: `{BACKLOG}`. "
    f"Skill: `{SKILL}`. Look-first hooks deny design-shaped writes until the "
    f"map has been Read this session."
)


def main() -> int:
    try:
        raw = sys.stdin.read()
        if raw.strip():
            json.loads(raw)
    except (ValueError, TypeError):
        pass
    print(
        json.dumps(
            {
                "continue": True,
                "additional_context": CONTEXT,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
