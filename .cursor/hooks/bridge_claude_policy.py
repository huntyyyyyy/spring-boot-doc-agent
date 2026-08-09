#!/usr/bin/env python3
"""Bridge Cursor hook I/O to Claude PreToolUse policy scripts.

Policy SoT stays in ``adapters/claude/hooks/`` and ``.claude/hooks/``.
Cursor Cloud loads **project** ``.cursor/hooks.json`` only (not
``~/.cursor/hooks.json``). This adapter normalizes stdin and maps deny
reasons so the same policy scripts work in Cursor Desktop/Cloud without
relying on Claude third-party hook import.

Usage (from ``.cursor/hooks.json``, cwd = repo root)::

    python3 .cursor/hooks/bridge_claude_policy.py \\
        adapters/claude/hooks/deny_text_search.py

Evidence: https://cursor.com/docs/hooks (Cloud project hooks; Shell vs
Claude Bash; ``beforeShellExecution`` / ``preToolUse`` schemas).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]

# Cursor Shell tool == Claude Bash; Grep keeps the same name.
TOOL_ALIASES = {"Shell": "Bash", "shell": "Bash"}


def _as_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
        except (ValueError, TypeError):
            return {"command": value}
        return parsed if isinstance(parsed, dict) else {"command": value}
    return {}


def normalize_to_claude(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Map Cursor ``beforeShellExecution`` / ``preToolUse`` JSON to Claude shape."""
    tool_input = _as_dict(raw.get("tool_input"))
    if "command" in raw and "command" not in tool_input:
        tool_input = {**tool_input, "command": str(raw.get("command") or "")}
    if "tool_name" in raw or "tool_input" in raw:
        tool = str(raw.get("tool_name") or "Bash")
        tool = TOOL_ALIASES.get(tool, tool)
        return {"tool_name": tool, "tool_input": tool_input}
    if "command" in raw:
        return {
            "tool_name": "Bash",
            "tool_input": {"command": str(raw.get("command") or "")},
        }
    return {"tool_name": "Bash", "tool_input": tool_input}


def extract_deny_reason(stdout: str) -> Optional[str]:
    """Accept Claude nested deny, design-research block, or Cursor-native deny."""
    text = (stdout or "").strip()
    if not text:
        return None
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return None
    if not isinstance(data, dict):
        return None
    nested = data.get("hookSpecificOutput") or {}
    if isinstance(nested, dict) and nested.get("permissionDecision") == "deny":
        return str(
            nested.get("permissionDecisionReason") or "denied by project policy"
        )
    if data.get("decision") == "block":
        return str(data.get("reason") or "blocked by project policy")
    if data.get("permission") == "deny":
        return str(
            data.get("agent_message")
            or data.get("user_message")
            or data.get("reason")
            or "denied by project policy"
        )
    return None


def emit_cursor(permission: str, reason: str = "") -> None:
    payload: Dict[str, Any] = {"permission": permission, "continue": True}
    if permission == "deny" and reason:
        payload["agent_message"] = reason
        payload["user_message"] = reason
    print(json.dumps(payload))


def run_policy(script: Path, claude_payload: Dict[str, Any]) -> Optional[str]:
    """Run one Claude policy script; return deny reason or None (allow / fail-open)."""
    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            input=json.dumps(claude_payload),
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            check=False,
        )
    except OSError:
        return None
    return extract_deny_reason(proc.stdout)


def resolve_script(arg: str) -> Path:
    path = Path(arg)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def main(argv: List[str]) -> int:
    # Fail open: never wedge the agent on hook infrastructure errors.
    try:
        if len(argv) < 2:
            emit_cursor("allow")
            return 0
        script = resolve_script(argv[1])
        if not script.is_file():
            emit_cursor("allow")
            return 0
        raw = json.load(sys.stdin)
        if not isinstance(raw, dict):
            emit_cursor("allow")
            return 0
        claude = normalize_to_claude(raw)
        reason = run_policy(script, claude)
        if reason:
            emit_cursor("deny", reason)
        else:
            emit_cursor("allow")
        return 0
    except Exception:  # noqa: BLE001 — fail open
        emit_cursor("allow")
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
