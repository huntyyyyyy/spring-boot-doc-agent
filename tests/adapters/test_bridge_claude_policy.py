#!/usr/bin/env python3
"""Contract for .cursor/hooks/bridge_claude_policy.py (Cursor↔Claude I/O)."""
from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

import pytest

pytestmark = pytest.mark.domain_adapters

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOKS_DIR = REPO_ROOT / ".cursor" / "hooks"
sys.path.insert(0, str(HOOKS_DIR))

import bridge_claude_policy as bridge  # noqa: E402


class NormalizePayloadTest(unittest.TestCase):
    def test_before_shell_becomes_bash(self) -> None:
        out = bridge.normalize_to_claude({"command": "rg foo", "cwd": "/x"})
        self.assertEqual(out["tool_name"], "Bash")
        self.assertEqual(out["tool_input"]["command"], "rg foo")

    def test_shell_tool_aliases_to_bash(self) -> None:
        out = bridge.normalize_to_claude(
            {"tool_name": "Shell", "tool_input": {"command": "curl x"}}
        )
        self.assertEqual(out["tool_name"], "Bash")
        self.assertEqual(out["tool_input"]["command"], "curl x")

    def test_grep_tool_preserved(self) -> None:
        out = bridge.normalize_to_claude({"tool_name": "Grep", "tool_input": {}})
        self.assertEqual(out["tool_name"], "Grep")


class ExtractDenyReasonTest(unittest.TestCase):
    def test_claude_nested_deny(self) -> None:
        raw = json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "no peep",
                }
            }
        )
        self.assertEqual(bridge.extract_deny_reason(raw), "no peep")

    def test_design_research_block(self) -> None:
        raw = json.dumps({"decision": "block", "reason": "need memo"})
        self.assertEqual(bridge.extract_deny_reason(raw), "need memo")

    def test_empty_is_allow(self) -> None:
        self.assertIsNone(bridge.extract_deny_reason(""))


class BridgeMainIntegrationTest(unittest.TestCase):
    def _run(self, stdin_obj: dict, script: str) -> dict:
        buf = io.StringIO()
        payload = json.dumps(stdin_obj)
        with mock.patch.object(bridge.sys, "stdin", io.StringIO(payload)):
            with mock.patch("builtins.print", side_effect=lambda *a, **k: buf.write(a[0])):
                code = bridge.main(["bridge", script])
        self.assertEqual(code, 0)
        return json.loads(buf.getvalue())

    def test_cursor_shell_rg_denied(self) -> None:
        data = self._run(
            {"command": "rg foo src"},
            "adapters/claude/hooks/deny_text_search.py",
        )
        self.assertEqual(data["permission"], "deny")
        self.assertIn("ast-grep", data["agent_message"])

    def test_cursor_shell_ast_grep_allowed(self) -> None:
        data = self._run(
            {"command": "ast-grep run -l python -p 'x' ."},
            "adapters/claude/hooks/deny_text_search.py",
        )
        self.assertEqual(data["permission"], "allow")

    def test_cursor_shell_curl_denied(self) -> None:
        data = self._run(
            {"command": "curl https://example.com"},
            "adapters/claude/hooks/deny_raw_network.py",
        )
        self.assertEqual(data["permission"], "deny")
        self.assertIn("WebFetch", data["agent_message"])
