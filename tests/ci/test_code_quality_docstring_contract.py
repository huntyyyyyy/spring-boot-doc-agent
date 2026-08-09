"""Cohesive suite from tests/ci/test_code_quality_docs_baseline.py: DocstringContractTest."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH

import pytest

pytestmark = pytest.mark.domain_ci_meta

SCRIPT_DIR = SCRIPTS_DIR
import check_code_quality as checker
from tests.support.code_quality.measure import measure_one

class DocstringContractTest(unittest.TestCase):
    """The orientation contract from CONTRIBUTING.md: a runnable module says
    how to run it near the top.

    The exemption test matters more than the violation tests. A check that
    demanded a Usage block from an imported-only module would be pointed at
    the wrong thing, and would push four library modules to invent a command
    they do not have -- this repo's own "a validator that validates fixtures"
    anti-pattern, one step removed."""

    MAIN = '\n\nif __name__ == "__main__":\n    pass\n'

    def test_usage_near_the_top_passes(self):
        source = '"""One line.\n\nUsage:\n    python3 mod.py\n"""' + self.MAIN
        self.assertIsNone(checker.docstring_violation(source, "mod.py"))

    def test_run_with_is_accepted_too(self):
        """The repo already uses both spellings; the contract is about the
        reader finding it, not about one exact word."""
        source = '"""One line.\n\nRun with:\n    python3 mod.py\n"""' + self.MAIN
        self.assertIsNone(checker.docstring_violation(source, "mod.py"))

    def test_usage_buried_below_the_threshold_is_flagged(self):
        filler = "\n".join(f"line {i}" for i in range(30))
        source = f'"""One line.\n\n{filler}\n\nUsage:\n    python3 mod.py\n"""' + self.MAIN
        violation = checker.docstring_violation(source, "mod.py")
        self.assertIsNotNone(violation)
        self.assertIn("docstring line", violation)

    def test_runnable_module_with_no_usage_at_all_is_flagged(self):
        source = '"""One line.\n\nSome rationale, but no command anywhere.\n"""' + self.MAIN
        violation = checker.docstring_violation(source, "mod.py")
        self.assertIsNotNone(violation)
        self.assertIn("never says how to run it", violation)

    def test_runnable_module_with_no_docstring_is_flagged(self):
        violation = checker.docstring_violation("x = 1" + self.MAIN, "mod.py")
        self.assertIsNotNone(violation)
        self.assertIn("no module docstring", violation)

    def test_library_module_without_a_cli_is_exempt(self):
        """doc_tag_utils.py and the three underscore helpers are imported and
        never run. They must not be asked for a command."""
        source = '"""A shared constant table.\n\nLong rationale, no command, correctly.\n"""\nX = 1\n'
        self.assertIsNone(checker.docstring_violation(source, "lib.py"))

    def test_a_main_string_that_is_not_the_guard_does_not_count(self):
        """`"__main__"` inside a docstring or an error message must not make a
        library module look runnable."""
        source = '"""Mentions __main__ in prose only."""\nMSG = "see __main__"\n'
        self.assertIsNone(checker.docstring_violation(source, "lib.py"))

    def test_syntax_error_defers_rather_than_double_reporting(self):
        """measure_tree already reports unparseable files; this check stays
        quiet so one broken file does not produce two findings."""
        self.assertIsNone(checker.docstring_violation("def f(:\n", "broken.py"))

    def test_a_new_violation_fails_the_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "scripts"
            scripts.mkdir()
            good = '"""One line.\n\nUsage:\n    python3 mod.py\n"""' + self.MAIN
            (scripts / "mod.py").write_text(good, encoding="utf-8")
            baseline = checker.measure_tree(scripts)
            self.assertEqual(baseline["docstring_violations"], {})

            filler = "\n".join(f"line {i}" for i in range(30))
            (scripts / "mod.py").write_text(
                f'"""One line.\n\n{filler}\n\nUsage:\n    python3 mod.py\n"""' + self.MAIN,
                encoding="utf-8")
            issues = checker.compare(baseline, checker.measure_tree(scripts))
            self.assertTrue(any("docstring contract" in i for i in issues), issues)
            self.assertEqual(checker.exit_code(issues), 1)

    def test_a_baselined_violation_does_not_fail_the_gate(self):
        """The ratchet's whole point: modules predating the rule are recorded,
        not blocking."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "scripts"
            scripts.mkdir()
            bad = '"""One line.\n\nNo command here.\n"""' + self.MAIN
            (scripts / "mod.py").write_text(bad, encoding="utf-8")
            baseline = checker.measure_tree(scripts)
            self.assertIn("mod.py", baseline["docstring_violations"])
            self.assertEqual(checker.compare(baseline, checker.measure_tree(scripts)), [])

    def test_violations_are_compared_by_module_not_by_message(self):
        """The messages carry line numbers. If comparison used them, shifting
        an unrelated line in an already-violating module would report a new
        violation."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "scripts"
            scripts.mkdir()
            filler = "\n".join(f"line {i}" for i in range(30))
            (scripts / "mod.py").write_text(
                f'"""One line.\n\n{filler}\n\nUsage:\n    python3 mod.py\n"""' + self.MAIN,
                encoding="utf-8")
            baseline = checker.measure_tree(scripts)

            longer = "\n".join(f"line {i}" for i in range(40))
            (scripts / "mod.py").write_text(
                f'"""One line.\n\n{longer}\n\nUsage:\n    python3 mod.py\n"""' + self.MAIN,
                encoding="utf-8")
            current = checker.measure_tree(scripts)
            self.assertNotEqual(baseline["docstring_violations"]["mod.py"],
                                current["docstring_violations"]["mod.py"])
            self.assertEqual(checker.compare(baseline, current), [])
