#!/usr/bin/env python3
"""PreToolUse hook: text search is allowed; keep tokenizer helpers for siblings.

Historically this hook denied ``Grep`` / ``rg`` / ``grep`` so agents would use
ast-grep for code citations. That hard deny is lifted (2026-08-09): inventory
and prose search via ripgrep is permitted. Citation correctness still prefers
ast-grep for structural code claims — soft guidance in CLAUDE.md / SEARCH.md,
not a runtime deny.

This module remains the shared tokenizer home for ``deny_raw_network`` (ENV /
segment / heredoc helpers). ``decide`` always allows so wired hooks stay
harmless no-ops while network egress deny stays independent.

Usage: wired from hooks/hooks.json; not run by hand.
       echo '{"tool_name":"Grep"}' | python3 hooks/deny_text_search.py
"""
from __future__ import annotations

import json
import re
import sys

# Recognized text-search command words (detection helpers / tests only).
# ``ast-grep`` / ``sg`` stay absent so substring traps are still covered.
TEXT_SEARCHERS = frozenset({"grep", "egrep", "fgrep", "rg", "ripgrep", "ack", "ag"})

SEGMENT_SPLIT_RE = re.compile(r"(?:\|\||&&|[;|&\n()])")

HEREDOC_RE = re.compile(
    r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1.*?^\s*\2\s*$",
    re.DOTALL | re.MULTILINE,
)


def strip_heredocs(command: str) -> str:
    return HEREDOC_RE.sub("<<HEREDOC", command)


ENV_ASSIGN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=\S*$")
WRAPPERS = frozenset({"sudo", "command", "time", "nice", "env", "xargs", "then", "do", "!"})

# Soft guidance only — never returned as a deny reason after the allow lift.
ASTGREP_PREFER_NOTE = (
    "Prefer ast-grep for structural code citations "
    "(try both @Name and @Name($$$). Zero matches = unproven, not absent)."
)


def command_words(command: str) -> list:
    """First real word of each shell segment, skipping env assignments/wrappers."""
    words = []
    for segment in SEGMENT_SPLIT_RE.split(strip_heredocs(command)):
        for token in segment.strip().split():
            bare = token.strip("\"'`")
            if ENV_ASSIGN_RE.match(bare) or bare in WRAPPERS:
                continue
            words.append(bare.replace("\\", "/").rsplit("/", 1)[-1])
            break
    return words


def uses_text_search(command: str) -> bool:
    return any(word in TEXT_SEARCHERS for word in command_words(command))


def decide(payload: dict) -> dict:
    """Always allow. Text search is permitted; network deny lives elsewhere."""
    del payload  # payload retained for hook API symmetry / future advisories
    return {"deny": False, "reason": ""}


def main(argv: list) -> int:
    del argv
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    verdict = decide(payload if isinstance(payload, dict) else {})
    if not verdict["deny"]:
        return 0
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": verdict["reason"],
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
