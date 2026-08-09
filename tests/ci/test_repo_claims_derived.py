"""Cohesive suite from tests/ci/test_repo_claims_derived_refs.py: TestCleanTree, TestDerivedBlocks."""

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

class TestCleanTree(TreeCase):
    def test_clean_tree_passes(self) -> None:
        self.assertEqual(self.run_check(), 0)


class TestDerivedBlocks(TreeCase):
    """Check A."""

    def test_correct_derived_value_passes(self) -> None:
        self.write("README.md", "There are <!-- derived: test_suite_count -->1<!-- /derived --> suites.\n")
        self.assertEqual(self.run_check(), 0)

    def test_stale_derived_value_fails(self) -> None:
        self.write("README.md", "There are <!-- derived: test_suite_count -->9<!-- /derived --> suites.\n")
        self.assertEqual(self.run_check(), 1)

    def test_fix_rewrites_the_stale_value(self) -> None:
        self.write("README.md", "There are <!-- derived: test_suite_count -->9<!-- /derived --> suites.\n")
        crc.main(["--root", str(self.dir), "--fix"])
        self.assertIn("-->1<!-- /derived -->",
                      (self.dir / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(self.run_check(), 0)

    def test_method_count_counts_test_functions(self) -> None:
        self.assertEqual(crc.derive_test_method_count(self.dir), "2")

    def test_fenced_example_is_not_a_claim(self) -> None:
        """CLAUDE.md documents this syntax by showing it. On the first run
        the checker read its own documentation as a false claim and failed
        the build -- found by the gate firing on its own author, the same way
        check_code_quality.py's statement-count metric was."""
        self.write("README.md",
                   "Wrap it like this:\n\n```\n"
                   "runs <!-- derived: test_suite_count -->N<!-- /derived --> suites\n"
                   "```\n")
        self.assertEqual(self.run_check(), 0)

    def test_fix_does_not_rewrite_a_fenced_example(self) -> None:
        original = ("```\n<!-- derived: test_suite_count -->N<!-- /derived -->\n```\n")
        self.write("README.md", original)
        crc.main(["--root", str(self.dir), "--fix"])
        self.assertEqual((self.dir / "README.md").read_text(encoding="utf-8"), original)

    def test_a_real_block_outside_a_fence_still_fails(self) -> None:
        """The fence exemption must not leak past the closing marker."""
        self.write("README.md",
                   "```\nexample\n```\n\n"
                   "runs <!-- derived: test_suite_count -->99<!-- /derived --> suites\n")
        self.assertEqual(self.run_check(), 1)

    def test_fenced_path_reference_IS_still_resolved(self) -> None:
        """The fence exemption covers values, not paths. Fences here hold
        commands to run and files to read; exempting them hid the launcher
        incident entirely (see TestBacktest)."""
        self.write("README.md", "```\nsee scripts/hypothetical.py\n```\n")
        self.assertEqual(self.run_check(), 1)

    def test_derived_block_is_checked_in_historical_files_too(self) -> None:
        """Check B is scoped to current-state docs; check A is not. A number
        is a claim about now no matter which file it sits in."""
        self.write("claude/session-log.md",
                   "Ran <!-- derived: test_suite_count -->77<!-- /derived --> suites.\n")
        self.assertEqual(self.run_check(), 1)
