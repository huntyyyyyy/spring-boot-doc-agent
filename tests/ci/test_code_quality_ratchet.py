"""Cohesive suite from tests/ci/test_check_code_quality.py: RatchetTest."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
SCRIPT_DIR = SCRIPTS_DIR
import check_code_quality as checker
from tests.support.code_quality.measure import measure_one

class RatchetTest(unittest.TestCase):
    """The failure modes, each asserted to reach a non-zero exit code."""

    def _tree(self, tmp: str, source: str) -> Path:
        scripts = Path(tmp) / "scripts"
        scripts.mkdir(exist_ok=True)
        (scripts / "mod.py").write_text(source, encoding="utf-8")
        return scripts

    SIMPLE = "def f(a):\n    if a:\n        return 1\n    return 2\n"

    def test_unchanged_tree_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, self.SIMPLE)
            baseline = checker.measure_tree(scripts)
            self.assertEqual(checker.compare(baseline, checker.measure_tree(scripts)), [])
            self.assertEqual(checker.exit_code([]), 0)

    def test_a_function_growing_more_complex_is_advisory_not_hard(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, "def f(a):\n    return a\n")
            baseline = checker.measure_tree(scripts)
            # BoolOp raises complexity without adding statements.
            (scripts / "mod.py").write_text(
                "def f(a):\n    return a and a and a and a\n",
                encoding="utf-8")
            current = checker.measure_tree(scripts)
            self.assertEqual(checker.compare(baseline, current), [])
            advisories = checker.size_advisories(baseline, current)
            self.assertTrue(any("complexity" in i for i in advisories), advisories)
            self.assertEqual(checker.exit_code(checker.compare(baseline, current)), 0)

    def test_a_function_doing_more_fails_on_statement_growth(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, self.SIMPLE)
            baseline = checker.measure_tree(scripts)
            body = "\n".join(f"    x{i} = {i}" for i in range(20))
            (scripts / "mod.py").write_text(
                f"def f(a):\n{body}\n    if a:\n        return 1\n    return 2\n", encoding="utf-8")
            current = checker.measure_tree(scripts)
            issues = checker.compare(baseline, current)
            self.assertTrue(any("statements" in i for i in issues), issues)
            self.assertEqual(checker.exit_code(issues), 1)

    def test_adding_comments_is_not_a_regression(self):
        """The metric is statements, not line span, precisely so that
        documenting a subtle piece of code does not read as making it worse.
        This repo is 38-54% prose in its larger modules; a gate that fires on
        a new comment block is a gate that gets deleted."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, self.SIMPLE)
            baseline = checker.measure_tree(scripts)
            commentary = "\n".join(f"    # explanatory line {i}" for i in range(30))
            (scripts / "mod.py").write_text(
                f"def f(a):\n{commentary}\n    if a:\n        return 1\n    return 2\n",
                encoding="utf-8")
            self.assertEqual(checker.compare(baseline, checker.measure_tree(scripts)), [])

    def test_a_docstring_does_not_count_as_a_statement(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, "def f(a):\n    return a\n")
            bare = checker.measure_tree(scripts)["functions"]["mod.py::f"]["statements"]
            (scripts / "mod.py").write_text(
                'def f(a):\n    """Now documented."""\n    return a\n', encoding="utf-8")
            documented = checker.measure_tree(scripts)["functions"]["mod.py::f"]["statements"]
            self.assertEqual(bare, documented)

    def test_a_nested_functions_body_is_not_counted_in_its_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, "def outer():\n    def inner():\n        return 1\n    return inner\n")
            functions = checker.measure_tree(scripts)["functions"]
            # outer counts one statement: the `return`. The nested `def` is
            # skipped rather than counted, because inner has its own entry
            # below -- otherwise growing inner would regress outer too.
            self.assertEqual(functions["mod.py::outer"]["statements"], 1)
            self.assertEqual(functions["mod.py::outer.inner"]["statements"], 1)

    def test_a_function_getting_simpler_passes_and_does_not_auto_tighten(self):
        """Improvement is allowed without --update, but it does not silently
        become the new floor -- otherwise a refactor followed by a revert
        would fail for no reason the author could see."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, self.SIMPLE)
            baseline = checker.measure_tree(scripts)
            (scripts / "mod.py").write_text("def f(a):\n    return 2\n", encoding="utf-8")
            self.assertEqual(checker.compare(baseline, checker.measure_tree(scripts)), [])

    def test_a_new_function_worse_than_hard_ceiling_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, self.SIMPLE)
            baseline = checker.measure_tree(scripts)
            body = "\n".join(f"    x{i} = {i}" for i in range(55))
            (scripts / "mod.py").write_text(
                self.SIMPLE + f"def g():\n{body}\n    return 0\n",
                encoding="utf-8")
            current = checker.measure_tree(scripts)
            issues = checker.compare(baseline, current)
            self.assertTrue(any("new function" in i and "statements" in i for i in issues), issues)
            self.assertEqual(checker.exit_code(issues), 1)

    def test_a_new_function_above_prior_complexity_is_advisory(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, self.SIMPLE)
            baseline = checker.measure_tree(scripts)
            (scripts / "mod.py").write_text(
                self.SIMPLE
                + "def g(a, b, c, d):\n"
                + "    if a:\n        if b:\n            if c:\n                if d:\n                    return 1\n"
                + "    return 0\n",
                encoding="utf-8")
            current = checker.measure_tree(scripts)
            self.assertEqual(checker.compare(baseline, current), [])
            advisories = checker.size_advisories(baseline, current)
            self.assertTrue(any("new function" in i for i in advisories), advisories)

    def test_a_new_function_within_existing_limits_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, self.SIMPLE)
            baseline = checker.measure_tree(scripts)
            (scripts / "mod.py").write_text(self.SIMPLE + "def g(a):\n    return a\n",
                                            encoding="utf-8")
            self.assertEqual(checker.compare(baseline, checker.measure_tree(scripts)), [])

    def test_dropping_type_annotations_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, "def f(a: int) -> int:\n    return a\n")
            baseline = checker.measure_tree(scripts)
            (scripts / "mod.py").write_text("def f(a):\n    return a\n", encoding="utf-8")
            issues = checker.compare(baseline, checker.measure_tree(scripts))
            self.assertTrue(any("annotation coverage fell" in i for i in issues), issues)
            self.assertEqual(checker.exit_code(issues), 1)

    def test_deleting_a_function_is_not_a_regression(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, self.SIMPLE + "def g(a):\n    return a\n")
            baseline = checker.measure_tree(scripts)
            (scripts / "mod.py").write_text(self.SIMPLE, encoding="utf-8")
            self.assertEqual(checker.compare(baseline, checker.measure_tree(scripts)), [])

    def test_an_unparseable_file_is_reported_rather_than_skipped_silently(self):
        """A syntax error must not read as "nothing to measure here." Silent
        truncation reading as completeness is on this repo's own
        anti-pattern list."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = self._tree(tmp, self.SIMPLE)
            baseline = checker.measure_tree(scripts)
            (scripts / "broken.py").write_text("def f(:\n", encoding="utf-8")
            issues = checker.compare(baseline, checker.measure_tree(scripts))
            self.assertTrue(any("could not parse" in i for i in issues), issues)
            self.assertEqual(checker.exit_code(issues), 1)
