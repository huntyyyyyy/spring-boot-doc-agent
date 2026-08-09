"""Cohesive suite from tests/ratchets/test_mutate.py: ApplyMutationTest, SurvivorDetectionTest, ReportTest, BaselineTest, SandboxIsolationTest."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
import mutate
import mutator_registry
_KNOWN_GATE_MUTATOR_NAMES = frozenset({
    "secret-heuristic-stops-unquoting",
    "build-file-guard-loosened",
    "relation-permits-everything",
    "query-limit-ceiling-removed",
    "context-packet-budget-trim-disabled",
    "freshness-mismatch-always-fresh",
    "agent-regains-grep",
    "rule-loses-its-args-form",
    "derived-count-edited",
    "prompt-contract-drifts",
})

class ApplyMutationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _mutator(self, find="alpha", replace="beta", path="f.txt", lang=""):
        return mutate.Mutator("m", path, lang, find, replace,
                              "tests/ratchets/test_set_delta.py", "why " * 6)

    def test_a_structural_pattern_that_matches_nothing_is_an_error(self) -> None:
        """ast-grep exits 0 whether or not its pattern matched -- the silent
        zero this repo has been bitten by twice. The applier compares the file
        before and after rather than trusting the exit code."""
        (self.tmp / "m.py").write_text("x = 1\n", encoding="utf-8")
        error = mutate.apply_mutation(
            self.tmp, self._mutator(find="totally_absent($A)", replace="other($A)",
                                    path="m.py", lang="python"))
        self.assertIn("matched nothing", error or "")

    def test_a_structural_rewrite_survives_reindentation(self) -> None:
        """The reason for structural anchors at all: a literal one breaks
        when someone reformats the target."""
        (self.tmp / "m.py").write_text(
            "def f():\n        return lambda member, direction: False\n",
            encoding="utf-8")
        error = mutate.apply_mutation(
            self.tmp,
            self._mutator(find="return lambda member, direction: False",
                          replace="return lambda member, direction: True",
                          path="m.py", lang="python"))
        self.assertIsNone(error)
        self.assertIn("True", (self.tmp / "m.py").read_text(encoding="utf-8"))

    def test_applies_the_replacement(self) -> None:
        (self.tmp / "f.txt").write_text("alpha\n", encoding="utf-8")
        self.assertIsNone(mutate.apply_mutation(self.tmp, self._mutator()))
        self.assertEqual((self.tmp / "f.txt").read_text(encoding="utf-8"), "beta\n")

    def test_a_missing_anchor_is_an_error_not_a_silent_noop(self) -> None:
        """The failure this returns an error for: a mutator that quietly
        changes nothing would be scored as 'killed' or 'survived' on the
        strength of a file it never touched."""
        (self.tmp / "f.txt").write_text("nothing here\n", encoding="utf-8")
        self.assertIn("anchor not found", mutate.apply_mutation(self.tmp, self._mutator()))

    def test_a_missing_file_is_an_error(self) -> None:
        self.assertIn("not in the tracked tree",
                      mutate.apply_mutation(self.tmp, self._mutator()))

    def test_only_the_first_occurrence_is_replaced(self) -> None:
        (self.tmp / "f.txt").write_text("alpha alpha\n", encoding="utf-8")
        mutate.apply_mutation(self.tmp, self._mutator())
        self.assertEqual((self.tmp / "f.txt").read_text(encoding="utf-8"), "beta alpha\n")


class SurvivorDetectionTest(unittest.TestCase):
    """The load-bearing case. A harness that cannot report a survivor emits a
    reassuring score while checking nothing."""

    def test_a_mutation_no_suite_catches_is_reported_as_survived(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mutate_selftest_") as tmp:
            harmless = mutate.Mutator(
                "harmless-comment-edit", "scripts/ratchets/set_delta.py", "",
                "THE RESIDUE IS THE FINDING", "THE RESIDUE IS THE FINDING.",
                "tests/ratchets/test_set_delta.py",
                "editing a docstring changes no behaviour, so nothing should catch it")
            outcome = mutate.evaluate(harmless, Path(tmp))
        self.assertEqual(outcome.status, "survived", outcome.detail)

    def test_a_real_mutation_is_reported_as_killed(self) -> None:
        """The other direction, so 'survived' is not simply what this
        harness always says."""
        with tempfile.TemporaryDirectory(prefix="mutate_selftest_") as tmp:
            real = next(m for m in mutate.MUTATORS if m.name == "relation-permits-everything")
            outcome = mutate.evaluate(real, Path(tmp))
        self.assertEqual(outcome.status, "killed", outcome.detail)


class ReportTest(unittest.TestCase):
    def _outcomes(self, *pairs):
        return [mutate.Outcome(n, s, "detail") for n, s in pairs]

    def test_a_new_survivor_is_a_nonzero_result(self) -> None:
        self.assertEqual(mutate.report(self._outcomes(("a", "survived")), {}), 1)

    def test_a_baselined_survivor_is_accepted(self) -> None:
        self.assertEqual(mutate.report(self._outcomes(("a", "survived")), {"a": "known"}), 0)

    def test_all_killed_is_zero(self) -> None:
        self.assertEqual(mutate.report(self._outcomes(("a", "killed")), {}), 0)

    def test_an_unapplied_mutator_is_nonzero_even_if_baselined(self) -> None:
        """A drifted anchor is never acceptable: it means the mutator is
        inert, which the baseline must not be able to excuse."""
        self.assertEqual(mutate.report(self._outcomes(("a", "not-applied")), {"a": "known"}), 1)


class BaselineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self._real = mutate.BASELINE_FILE
        mutate.BASELINE_FILE = self.tmp / "baseline.json"

    def tearDown(self) -> None:
        mutate.BASELINE_FILE = self._real
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_round_trip(self) -> None:
        mutate.write_baseline([mutate.Outcome("a", "survived", "because"),
                               mutate.Outcome("b", "killed", "-")])
        loaded = mutate.load_baseline()
        self.assertEqual(loaded, {"a": "because"})

    def test_a_stale_schema_version_is_ignored_not_trusted(self) -> None:
        mutate.BASELINE_FILE.write_text(
            json.dumps({"schema_version": 999, "accepted_survivors": {"a": "x"}}),
            encoding="utf-8")
        self.assertEqual(mutate.load_baseline(), {})

    def test_a_missing_baseline_accepts_nothing(self) -> None:
        self.assertEqual(mutate.load_baseline(), {})


class SandboxIsolationTest(unittest.TestCase):
    """The property that makes this safe to run on every commit."""

    def _tracked_diff(self) -> str:
        return subprocess.run(["git", "-C", str(mutate.REPO_ROOT), "diff", "--stat"],
                              capture_output=True, text=True).stdout.strip()

    def test_a_run_leaves_the_tracked_tree_untouched(self) -> None:
        before = self._tracked_diff()
        with tempfile.TemporaryDirectory(prefix="mutate_iso_") as tmp:
            mutate.evaluate(mutate.MUTATORS[0], Path(tmp))
        self.assertEqual(self._tracked_diff(), before,
                         "a mutation escaped the sandbox into the working tree")

    def test_materialize_copies_only_tracked_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mutate_mat_") as tmp:
            dest = Path(tmp) / "copy"
            dest.mkdir()
            mutate.materialize(dest)
            self.assertTrue((dest / "scripts" / "ratchets" / "set_delta.py").is_file())
            # Working-tree target checkouts stay untracked; materialize must
            # not pull them in. Assert via denylist tokens without hardcoding
            # a client name in this suite.
            import check_no_client_identifiers as client_gate  # noqa: E402

            for token in client_gate.load_denylist(mutate.REPO_ROOT):
                self.assertFalse(
                    (dest / token).exists(),
                    f"materialize copied denylisted checkout dir {token!r}",
                )
            self.assertFalse((dest / "target-repo").exists())
            self.assertFalse((dest / ".git").exists())
