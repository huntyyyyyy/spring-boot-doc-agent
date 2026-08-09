#!/usr/bin/env python3
"""Contract for hooks/deny_text_search.py after the ripgrep allow lift.

Text search (Grep tool / ``rg`` / ``grep``) is allowed. This suite proves the
allow, keeps the ast-grep substring self-defeat guard, and keeps heredoc
tokenization helpers honest for ``deny_raw_network`` imports.

Run with: pytest tests/adapters/test_deny_text_search.py -v
"""
from __future__ import annotations

import sys
import unittest

import pytest

from tests.conftest import REPO_ROOT

pytestmark = pytest.mark.domain_adapters

sys.path.insert(0, str(REPO_ROOT / "adapters" / "claude" / "hooks"))

import deny_text_search as dts  # noqa: E402


def denies(tool: str, command: str = "") -> bool:
    return dts.decide({"tool_name": tool, "tool_input": {"command": command}})["deny"]


class TestGrepToolAllowed(unittest.TestCase):
    def test_grep_tool_is_allowed(self) -> None:
        self.assertFalse(denies("Grep"))

    def test_unrelated_tools_pass(self) -> None:
        for tool in ("Read", "Glob", "Write", "Edit"):
            self.assertFalse(denies(tool), tool)


class TestAstGrepIsNeverBlocked(unittest.TestCase):
    """Self-defeat guard: ``ast-grep`` contains the substring ``grep``."""

    SANCTIONED = (
        "ast-grep run -l java -p '@Entity' src",
        "ast-grep scan --rule src/doc_engine/scanning/resources/spring_ast_grep_rules.yml .",
        "ast-grep test",
        "ast-grep --version",
        "cat f.java | ast-grep run --stdin -l java -p '@X'",
        "python -m doc_engine.tools.spring_signal_scan .",
    )

    def test_ast_grep_is_never_blocked(self) -> None:
        for command in self.SANCTIONED:
            self.assertFalse(denies("Bash", command), command)


class TestTextSearchIsAllowed(unittest.TestCase):
    ALLOWED = (
        "grep -rn foo .",
        "egrep foo f",
        "fgrep foo f",
        "rg foo",
        "cat f | grep foo",
        "ls && grep foo f",
        "/usr/bin/grep foo f",
        "FOO=1 grep foo f",
        "sudo grep foo f",
        "python x.py; grep foo f",
        "ripgrep -n pattern src",
    )

    def test_each_form_is_allowed(self) -> None:
        for command in self.ALLOWED:
            self.assertFalse(denies("Bash", command), command)

    def test_unrelated_bash_passes(self) -> None:
        for command in ("python -m unittest", "git status", "ls -la"):
            self.assertFalse(denies("Bash", command), command)


class TestDetectionHelpersStillRecognizeSearchers(unittest.TestCase):
    """Tokenizer helpers remain accurate for sibling hooks / diagnostics."""

    def test_uses_text_search_detects_rg_and_grep(self) -> None:
        self.assertTrue(dts.uses_text_search("rg foo src"))
        self.assertTrue(dts.uses_text_search("grep -n x f"))
        self.assertFalse(dts.uses_text_search("ast-grep run -l py -p x ."))


class TestHeredocBodiesAreData(unittest.TestCase):
    def test_prose_beginning_with_grep_inside_a_heredoc_is_not_a_command(self) -> None:
        command = (
            "python - <<'PY'\n"
            "entry = '''\n"
            "grep against a consistent per-entry Tags: line, versus an index\n"
            "'''\n"
            "PY"
        )
        self.assertFalse(dts.uses_text_search(command))
        self.assertFalse(denies("Bash", command))

    def test_a_real_grep_after_a_heredoc_is_detected_but_allowed(self) -> None:
        command = (
            "python - <<'PY'\n"
            "print(1)\n"
            "PY\n"
            "grep -rn foo ."
        )
        self.assertTrue(dts.uses_text_search(command))
        self.assertFalse(denies("Bash", command))

    def test_an_unquoted_heredoc_tag_is_handled(self) -> None:
        self.assertFalse(denies("Bash", "cat <<EOF\ngrep is a word here\nEOF"))


class TestFailOpen(unittest.TestCase):
    def test_unparseable_payload_does_not_block(self) -> None:
        self.assertFalse(dts.decide({})["deny"])

    def test_missing_command_key_does_not_block(self) -> None:
        self.assertFalse(dts.decide({"tool_name": "Bash"})["deny"])


class TestPreferNoteDocumentsAstGrep(unittest.TestCase):
    def test_prefer_note_names_ast_grep_traps(self) -> None:
        self.assertIn("ast-grep", dts.ASTGREP_PREFER_NOTE)
        self.assertIn("$$$", dts.ASTGREP_PREFER_NOTE)
        self.assertIn("unproven", dts.ASTGREP_PREFER_NOTE.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
