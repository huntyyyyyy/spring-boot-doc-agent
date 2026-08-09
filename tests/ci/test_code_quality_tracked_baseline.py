"""Cohesive suite from tests/ci/test_code_quality_docs_baseline.py: TrackedFilesOnlyTest, BaselineRoundTripTest, CommittedBaselineTest."""

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

class TrackedFilesOnlyTest(unittest.TestCase):
    """The baseline is a committed artifact, so it must describe the committed
    tree -- not whatever happens to be sitting in the working directory.

    This is a regression test for a real incident: regenerating the baseline
    while a concurrent session's untracked files were present absorbed 93 of
    their functions and raised the annotation floor above what the committed
    tree could meet, which would have failed CI on its first run while blaming
    files that were never committed."""

    def _git(self, cwd, *args):
        subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)

    def test_untracked_file_is_not_measured(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._git(repo, "init", "-q")
            scripts = repo / "scripts"
            scripts.mkdir()
            (scripts / "tracked.py").write_text("def a():\n    return 1\n", encoding="utf-8")
            self._git(repo, "add", "scripts/tracked.py")
            self._git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")

            (scripts / "untracked.py").write_text("def b():\n    return 2\n", encoding="utf-8")

            measured = checker.measure_tree(scripts)
            keys = list(measured["functions"])
            self.assertIn("tracked.py::a", keys)
            self.assertNotIn("untracked.py::b", keys,
                             "an untracked file leaked into a committed artifact")

    def test_falls_back_to_glob_outside_a_git_checkout(self):
        """An exported tarball has no .git; the script must still work rather
        than silently measuring nothing."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "scripts"
            scripts.mkdir()
            (scripts / "mod.py").write_text("def a():\n    return 1\n", encoding="utf-8")
            self.assertIn("mod.py::a", checker.measure_tree(scripts)["functions"])

    def test_nested_fixture_python_files_are_not_measured(self):
        """scripts/fixtures/ holds fixture sources, not modules of this
        tool; measuring them would ratchet somebody else's sample code."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "scripts"
            (scripts / "test_fixtures").mkdir(parents=True)
            (scripts / "mod.py").write_text("def a():\n    return 1\n", encoding="utf-8")
            (scripts / "test_fixtures" / "sample.py").write_text(
                "def fixture():\n    return 1\n", encoding="utf-8")
            keys = list(checker.measure_tree(scripts)["functions"])
            self.assertIn("mod.py::a", keys)
            self.assertNotIn("sample.py::fixture", keys)


class BaselineRoundTripTest(unittest.TestCase):
    def test_baseline_survives_a_json_round_trip(self):
        """compare() runs against JSON-loaded data in production, where dict
        key order and int/str typing can differ from the in-memory object."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "scripts"
            scripts.mkdir()
            (scripts / "mod.py").write_text("def f(a):\n    return a\n", encoding="utf-8")
            path = Path(tmp) / "baseline.json"
            checker.write_baseline(path, checker.measure_tree(scripts))
            reloaded = checker.load_baseline(path)
            self.assertIsNotNone(reloaded)
            self.assertEqual(checker.compare(reloaded, checker.measure_tree(scripts)), [])

    def test_measurement_is_byte_stable_across_runs(self):
        """The baseline is committed and diffed; an unstable serialization
        would make every regeneration look like a change."""
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "scripts"
            scripts.mkdir()
            (scripts / "b.py").write_text("def b():\n    return 1\n", encoding="utf-8")
            (scripts / "a.py").write_text("def a():\n    return 1\n", encoding="utf-8")
            first = Path(tmp) / "one.json"
            second = Path(tmp) / "two.json"
            checker.write_baseline(first, checker.measure_tree(scripts))
            checker.write_baseline(second, checker.measure_tree(scripts))
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_function_keys_are_sorted(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "scripts"
            scripts.mkdir()
            (scripts / "mod.py").write_text(
                "def z():\n    return 1\ndef a():\n    return 1\n", encoding="utf-8")
            keys = list(checker.measure_tree(scripts)["functions"])
            self.assertEqual(keys, sorted(keys))

    def test_a_missing_baseline_is_a_usage_error_not_a_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(checker.load_baseline(Path(tmp) / "absent.json"))


class CommittedBaselineTest(unittest.TestCase):
    def test_the_committed_baseline_matches_the_current_tree(self):
        """The real gate, run against this repo. If this fails, either
        annotation/docstring coverage regressed or the baseline needs
        --update -- the message says which."""
        baseline = checker.load_baseline(checker.DEFAULT_BASELINE)
        self.assertIsNotNone(baseline, "no committed baseline; run with --update")
        self.assertEqual(baseline.get("schema_version"), checker.SCHEMA_VERSION)
        current = checker.measure_tree(
            SCRIPT_DIR,
            extra_roots=[SCRIPT_DIR, SCRIPT_DIR.parent / "src" / "doc_engine"],
            repo_root=SCRIPT_DIR.parent,
        )
        issues = checker.compare(baseline, current)
        self.assertEqual(issues, [], "\n".join(issues))
