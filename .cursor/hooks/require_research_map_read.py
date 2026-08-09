#!/usr/bin/env python3
"""Deny design-shaped writes until docs/research/README.md was Read.

preToolUse matcher Write|StrReplace|EditNotebook. Fail closed on design paths
when receipt missing (DOC7–DOC8). Allow research-map / archive typo fixes.

Usage::

    python3 .cursor/hooks/require_research_map_read.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from research_map_common import paths_from_payload, receipt_path, repo_relative

DESIGN_RE = re.compile(
    r"("
    r"^docs/design/"
    r"|^docs/research/(?!README\.md$|archive/)"
    r"|^src/doc_engine/"
    r"|^scripts/ci/"
    r"|^adapters/claude/hooks/"
    r"|^\.cursor/hooks"
    r")"
)

ALLOW_RE = re.compile(
    r"("
    r"^docs/research/README\.md$"
    r"|^docs/research/archive/"
    r"|^docs/research/quality-backlog\.md$"
    r")"
)


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "permission": "deny",
                "continue": True,
                "agent_message": reason,
                "user_message": reason,
            }
        )
    )


def allow() -> None:
    print(json.dumps({"permission": "allow", "continue": True}))


def _gated_rels(raw: dict) -> list[str]:
    rels = [repo_relative(path) for path in paths_from_payload(raw)]
    return [r for r in rels if DESIGN_RE.search(r) and not ALLOW_RE.search(r)]


def main() -> int:
    try:
        raw = json.loads(sys.stdin.read() or "{}")
    except (ValueError, TypeError):
        allow()
        return 0
    if not isinstance(raw, dict):
        allow()
        return 0
    gated = _gated_rels(raw)
    if not gated:
        allow()
        return 0
    if receipt_path().is_file():
        allow()
        return 0
    deny(
        "Look-first: read docs/research/README.md (domain map) before "
        f"design-shaped writes ({', '.join(gated[:3])}). "
        "Spec: docs/research/process/18-docs-research-taxonomy-claude-consolidation-2026.md"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
