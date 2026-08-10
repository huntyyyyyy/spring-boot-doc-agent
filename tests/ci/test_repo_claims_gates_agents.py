"""Cohesive suite from tests/ci/test_check_repo_claims.py: TestCiSuiteCoverage, TestGateHonesty, TestAgentSearchTooling, TestNotContainsPredicate, TestUtf8Encoding."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import check_repo_claims as crc
from tests.conftest import REPO_ROOT
from tests.support.repo_claims.tree import TreeCase, build_tree

import pytest

pytestmark = pytest.mark.domain_ci_meta

class TestCiSuiteCoverage(TreeCase):
    """Check D — refuse scripts/test_*.py revival; discovery covers tests/."""

    def test_wired_suite_passes(self) -> None:
        self.assertEqual(self.run_check(), 0)

    def test_scripts_test_wrapper_revival_is_flagged(self) -> None:
        (self.dir / "scripts" / "test_orphan.py").write_text(
            "def test_x():\n    pass\n", encoding="utf-8")
        self.assertEqual(self.run_check(), 1)

    def test_pytest_discovery_does_not_require_per_suite_ci_steps(self) -> None:
        (self.dir / "tests" / "test_orphan.py").write_text(
            "def test_x():\n    pass\n", encoding="utf-8")
        self.assertEqual(self.run_check(), 0)

    def test_ci_exempt_suites_registry_removed(self) -> None:
        """Dead CI_EXEMPT_SUITES must not return — opt-in uses skipUnless."""
        self.assertFalse(hasattr(crc, "CI_EXEMPT_SUITES"))

class TestGateHonesty(TreeCase):
    """Check E."""

    def _add_non_enforcing_script(self, step_name: str) -> None:
        (self.dir / "scripts" / "reporter.py").write_text(
            "ENFORCE = False\n", encoding="utf-8")
        (self.dir / ".github" / "workflows" / "ci.yml").write_text(
            "jobs:\n  test:\n    steps:\n"
            "      - name: pytest\n        run: pytest\n"
            f"      - name: {step_name}\n        run: python3 scripts/reporter.py\n",
            encoding="utf-8")

    def test_gate_named_as_a_gate_that_cannot_fail_is_flagged(self) -> None:
        self._add_non_enforcing_script("reporter.py (fails on missing docs)")
        self.assertEqual(self.run_check(), 1)

    def test_honest_non_blocking_name_passes(self) -> None:
        self._add_non_enforcing_script("reporter.py (reports missing docs; non-blocking)")
        self.assertEqual(self.run_check(), 0)

    def test_suite_step_for_the_same_script_is_not_flagged(self) -> None:
        """`test_reporter.py` contains `reporter.py`. A unit-test step makes
        no enforcement claim, and flagging it was a real bug in this check."""
        (self.dir / "scripts" / "reporter.py").write_text("ENFORCE = False\n",
                                                          encoding="utf-8")
        (self.dir / "tests" / "test_reporter.py").write_text(
            "def test_x():\n    pass\n", encoding="utf-8")
        (self.dir / ".github" / "workflows" / "ci.yml").write_text(
            "jobs:\n  test:\n    steps:\n"
            "      - name: pytest\n        run: pytest\n"
            "      - name: test_reporter.py\n        run: pytest tests/test_reporter.py\n"
            "      - name: reporter.py (non-blocking)\n        run: python3 scripts/reporter.py\n",
            encoding="utf-8")
        self.assertEqual(self.run_check(), 0)

class TestAgentSearchTooling(TreeCase):
    """Check F. Bash stays scoped; network denies required; text search OK."""

    SCOPED = ["Bash(ast-grep run:*)"]
    NETWORK = ["Bash(curl:*)", "Bash(wget:*)", "Bash(git clone:*)"]

    def agent(self, name: str, tools: str) -> None:
        folder = self.dir / "agents"
        folder.mkdir(exist_ok=True)
        (folder / name).write_text(
            f"---\nname: {name[:-3]}\ndescription: d\ntools: {tools}\n---\n\nBody.\n",
            encoding="utf-8")

    def settings(self, allow: list, deny: list) -> None:
        folder = self.dir / ".claude"
        folder.mkdir(exist_ok=True)
        (folder / "settings.json").write_text(
            json.dumps({"permissions": {"allow": allow, "deny": deny}}),
            encoding="utf-8")

    def test_structural_only_agent_passes(self) -> None:
        self.agent("writer.md", "Read, Glob, Write")
        self.assertEqual(self.run_check(), 0)

    def test_an_agent_declaring_grep_passes(self) -> None:
        """Grep tool is allowed after the 2026-08-09 ripgrep allow lift."""
        self.agent("writer.md", "Read, Grep, Glob, Write")
        self.assertEqual(self.run_check(), 0)

    def test_scoped_bash_grant_passes(self) -> None:
        self.agent("writer.md", "Read, Glob, Write, Bash")
        self.settings(self.SCOPED, self.NETWORK)
        self.assertEqual(self.run_check(), 0)

    def test_bash_without_a_scoped_allowlist_entry_fails(self) -> None:
        """A subagent's tools: field cannot scope Bash, so settings.json is
        the only thing standing between `Bash` and a general shell."""
        self.agent("writer.md", "Read, Glob, Write, Bash")
        self.settings(["Bash(git status:*)"], self.NETWORK)
        self.assertEqual(self.run_check(), 1)

    def test_bash_without_text_search_denies_still_passes(self) -> None:
        """TEXT_SEARCH_DENIES is empty — missing grep/rg denies is not a fail."""
        self.agent("writer.md", "Read, Glob, Write, Bash")
        self.settings(self.SCOPED, self.NETWORK)
        self.assertEqual(self.run_check(), 0)
        self.assertEqual(crc.TEXT_SEARCH_DENIES, ())

    def test_bash_without_network_denies_fails(self) -> None:
        """Network egress denies remain mandatory when Bash is granted."""
        self.agent("writer.md", "Read, Glob, Write, Bash")
        self.settings(self.SCOPED, [])  # network absent
        self.assertEqual(self.run_check(), 1)

    def test_scoped_bash_grant_with_network_denies_passes(self) -> None:
        self.agent("writer.md", "Read, Glob, Write, Bash")
        self.settings(self.SCOPED, self.NETWORK)
        self.assertEqual(self.run_check(), 0)

    def test_a_dot_claude_agent_with_grep_passes(self) -> None:
        folder = self.dir / ".claude" / "agents"
        folder.mkdir(parents=True)
        (folder / "local.md").write_text(
            "---\nname: local\ndescription: d\ntools: Read, Grep\n---\n\nBody.\n",
            encoding="utf-8")
        self.assertEqual(self.run_check(), 0)

    def test_grep_in_prose_is_not_a_violation(self) -> None:
        self.agent("writer.md", "Read, Glob, Write")
        (self.dir / "agents" / "writer.md").write_text(
            "---\nname: writer\ndescription: d\ntools: Read, Glob, Write\n---\n\n"
            "You are given the TODO/FIXME grep hits from Stage 0.\n",
            encoding="utf-8")
        self.assertEqual(self.run_check(), 0)

class TestNotContainsPredicate(TreeCase):
    def test_not_contains_both_directions(self) -> None:
        self.write("docs/process/steering-prompts/02-y-research-prompt.md",
                   "---\nstatus: resolved\n"
                   "verify:\n  - not_contains:scripts/widget.py:Grep\n---\n\nBody.\n")
        self.assertEqual(self.run_check(), 0)
        (self.dir / "scripts" / "widget.py").write_text(
            "def do_a_thing():\n    return Grep\n", encoding="utf-8")
        self.assertEqual(self.run_check(), 1)

    def test_not_contains_on_a_missing_file_fails(self) -> None:
        """Vacuous truth would turn a rename into a silent pass -- the exact
        direction prompt 06's status went wrong in."""
        self.write("docs/process/steering-prompts/02-y-research-prompt.md",
                   "---\nstatus: resolved\n"
                   "verify:\n  - not_contains:scripts/gone.py:Grep\n---\n\nBody.\n")
        self.assertEqual(self.run_check(), 1)

class TestUtf8Encoding(TreeCase):
    """Check G — non-UTF-8 markdown must be a Finding, never a traceback."""

    def test_non_utf8_markdown_reports_finding_without_raising(self) -> None:
        # cp1252 × (0xd7) — the byte that crashed CI on session-log.md
        path = self.dir / "README.md"
        path.write_bytes(b"bad byte: \xd7\n")
        findings = crc.check_utf8_markdown(self.dir, ["README.md"])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].check, "G")
        self.assertIn("byte offset", findings[0].message)
        self.assertIn("UTF-8", findings[0].message)
        # Full checker path: Finding, not UnicodeDecodeError
        self.assertEqual(self.run_check(), 1)

    def test_utf8_markdown_passes_encoding_check(self) -> None:
        self.write("README.md", "See `scripts/widget.py` — em dash ok.\n")
        self.assertEqual(crc.check_utf8_markdown(self.dir, ["README.md"]), [])
        self.assertEqual(self.run_check(), 0)
