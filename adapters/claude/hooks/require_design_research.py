#!/usr/bin/env python3
"""PreToolUse hook: refuse design-shaped commits without research Spec evidence.

Mirrors ``require_hardened_tests`` doctrine: memory failed (E-MOD3), so enforce
at ``git commit``. Spec: docs/research/14-facade-poke-research-hooks-2026.md
(RES1–RES3).

Fail open on internal errors; fail closed on a real finding.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[3]

COMMIT_RE = re.compile(r"(^|[;&|]\s*)git\s+(-C\s+\S+\s+)?commit\b")

DESIGN_PATH_RE = re.compile(
    r"("
    r"src/doc_engine/.+_ports\.py$"
    r"|src/doc_engine/.+_strategy\.py$"
    r"|docs/design/"
    r"|docs/research/"
    r"|scripts/ci/check_facade_poke_surface\.py$"
    r"|adapters/claude/hooks/require_design_research\.py$"
    r")"
)

SKILL = "principal-se-research-epic"


def is_commit(command: str) -> bool:
    return bool(COMMIT_RE.search(command))


def staged_files() -> List[str]:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def design_shaped(staged: List[str]) -> List[str]:
    return [p for p in staged if DESIGN_PATH_RE.search(p.replace("\\", "/"))]


def research_memo_ok(staged: List[str]) -> bool:
    """True when a staged research memo carries Spec + tiered external evidence."""
    memos = [
        p
        for p in staged
        if p.replace("\\", "/").startswith("docs/research/") and p.endswith(".md")
    ]
    if not memos:
        return False
    for rel in memos:
        text = (REPO_ROOT / rel).read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        if "spec_gate:" not in lower and "spec_gate :" not in lower:
            continue
        has_tier = "[evidenced]" in lower or "claim tiers" in lower
        has_arxiv = "arxiv.org/" in lower or "arxiv:" in lower
        has_gh = "github.com/" in lower
        # DeepWiki allowed as orientation; must not be the only external cite.
        if has_tier and has_arxiv and has_gh:
            return True
    return False


def deny(message: str) -> None:
    payload = {
        "decision": "block",
        "reason": (
            f"{message}\n"
            f"Load skill `{SKILL}` and file docs/research/* with spec_gate + "
            f"[Evidenced] arXiv abs URL + GitHub (stars/recency) before commit. "
            f"DeepWiki is Tier C orientation only (steering 00/10)."
        ),
    }
    print(json.dumps(payload))
    sys.exit(0)


def allow() -> None:
    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        tool_input = data.get("tool_input") or {}
        command = tool_input.get("command") or ""
        if not is_commit(command):
            allow()
        staged = staged_files()
        shaped = design_shaped(staged)
        if not shaped:
            allow()
        if research_memo_ok(staged):
            allow()
        deny(
            "Design-shaped paths staged without a research Spec memo in this commit:\n  - "
            + "\n  - ".join(shaped[:12])
        )
    except Exception as exc:  # noqa: BLE001 — fail open
        print(json.dumps({"decision": "approve", "reason": f"hook error fail-open: {exc}"}))
        sys.exit(0)


if __name__ == "__main__":
    main()
