"""Cohesive suite from tests/ci/test_repo_claims_baselines.py: TestBaseline, TestBacktest, TestUnchangedSince."""

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

class TestBaseline(TreeCase):
    def test_baseline_absorbs_an_existing_finding_but_not_a_new_one(self) -> None:
        self.write("README.md", "See `scripts/nope.py`.\n")
        baseline = self.dir / "baseline.json"
        crc.main(["--root", str(self.dir), "--baseline", str(baseline), "--update"])
        self.assertEqual(
            crc.main(["--root", str(self.dir), "--baseline", str(baseline)]), 0)

        self.write("README.md", "See `scripts/nope.py` and `scripts/also_nope.py`.\n")
        self.assertEqual(
            crc.main(["--root", str(self.dir), "--baseline", str(baseline)]), 1)

    def test_exact_checks_are_never_baselined(self) -> None:
        """A/D/E and a contradicted verify: predicate must stay fatal even
        immediately after --update, or the ratchet becomes an off switch.

        Uses Check A (stale derived). Check D now flags scripts/test_*.py
        revival rather than unwired scripts/ suites."""
        self.write(
            "README.md",
            "There are <!-- derived: test_suite_count -->9<!-- /derived --> "
            "suites.\n",
        )
        baseline = self.dir / "baseline.json"
        code = crc.main(["--root", str(self.dir), "--baseline", str(baseline),
                         "--update"])
        self.assertEqual(code, 1)
        self.assertEqual(
            crc.main(["--root", str(self.dir), "--baseline", str(baseline)]), 1)

    def test_schema_version_mismatch_is_rejected(self) -> None:
        baseline = self.dir / "baseline.json"
        baseline.write_text(json.dumps({"schema_version": 99, "accepted": []}),
                            encoding="utf-8")
        self.assertEqual(
            crc.main(["--root", str(self.dir), "--baseline", str(baseline)]), 2)

    def test_fingerprint_survives_the_claim_moving_line(self) -> None:
        self.write("README.md", "See `scripts/nope.py`.\n")
        before = crc.check_references(self.dir, ["README.md"])[0].fingerprint
        self.write("README.md", "\n\n\n\nSee `scripts/nope.py`.\n")
        after = crc.check_references(self.dir, ["README.md"])[0].fingerprint
        self.assertEqual(before, after)

class TestBacktest(unittest.TestCase):
    """Against the real tree, reconstructing defects this repo actually had.

    A checker that passes its own unit tests but would have missed every
    historical instance is mis-aimed, and that is not visible from synthetic
    fixtures. Backtesting caught exactly that: check B originally exempted
    fenced blocks, which made the launcher incident below invisible.
    """

    def _flag_count(self, rel: str, mutate) -> int:
        path = REPO_ROOT / rel
        original = path.read_text(encoding="utf-8")
        try:
            path.write_text(mutate(original), encoding="utf-8")
            _, soft = crc.collect_all(REPO_ROOT)
            return len([f for f in soft if f.path == rel])
        finally:
            path.write_text(original, encoding="utf-8")

    def test_launcher_pointing_at_missing_prompts_is_caught(self) -> None:
        """The renumbering incident: 12-review-session-launcher.md told fresh
        sessions to read two prompt files where "neither exists". Its payload
        is one fenced block of bare, un-backticked paths -- both properties
        that an earlier draft of this checker skipped."""
        rel = "claude/steering-prompts/12-review-session-launcher.md"
        found = self._flag_count(rel, lambda t: t
                                 .replace("10-review-persona-and-standards.md",
                                          "08-review-persona-and-standards.md")
                                 .replace("11-context-traversal-protocol.md",
                                          "09-context-traversal-protocol.md"))
        self.assertGreaterEqual(found, 2, "the launcher incident is not caught")

    def test_current_launcher_is_clean(self) -> None:
        rel = "claude/steering-prompts/12-review-session-launcher.md"
        self.assertEqual(self._flag_count(rel, lambda t: t), 0)

    def test_current_state_doc_citing_a_deleted_script_is_caught(self) -> None:
        """CONSTRAINTS.md cited verify_llms_docs.py after 2f82971 deleted it.
        The real commit added the tombstone in the same change, so the stale
        state was never committed -- this reconstructs it without one."""
        found = self._flag_count(
            "CONSTRAINTS.md",
            lambda t: t + "\n\nThe checker `scripts/verify_llms_docs.py` runs in CI.\n")
        self.assertGreaterEqual(found, 1)

class TestUnchangedSince(unittest.TestCase):
    """The stability predicate. It does not assert a claim is true -- nothing
    here can judge that -- it asserts nobody has re-read the claim since the
    thing it describes moved."""

    SUBJECT = 'def f(x):\n    """Docs."""\n    return x + 1\n'

    def _repo(self, tmp):
        root = Path(tmp)
        (root / "scripts").mkdir()
        (root / "scripts" / "sub.py").write_text(self.SUBJECT, encoding="utf-8")
        return root

    def _pred(self, root, level="t2", digest=None):
        if digest is None:
            digest = crc._ast_signature.signature(root / "scripts/sub.py", level).split(":")[1]
        return f"unchanged_since:scripts/sub.py:{level}:{digest}"

    def test_a_matching_signature_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            self.assertTrue(crc.evaluate_predicate(root, self._pred(root))[0])

    def test_never_affirmed_is_reported_differently_from_changed(self):
        """These are different problems with different fixes -- one needs a
        stamp, the other needs a human to re-read a claim. Collapsing them
        into one message would train people to run --affirm reflexively,
        which defeats the predicate."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            _, unaffirmed = crc.evaluate_predicate(root, self._pred(root, digest=""))
            _, changed = crc.evaluate_predicate(root, self._pred(root, digest="0" * 64))
            self.assertIn("never been affirmed", unaffirmed)
            self.assertIn("changed since", changed)
            self.assertNotEqual(unaffirmed, changed)

    def test_an_unknown_level_fails_rather_than_falling_back(self):
        """Falling back to a different relation would compare two
        incomparable digests and report the answer confidently."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            passed, why = crc.evaluate_predicate(root, self._pred(root, level="t9",
                                                                 digest="0" * 64))
            self.assertFalse(passed)
            self.assertIn("unknown signature level", why)

    def test_a_missing_subject_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            passed, why = crc.evaluate_predicate(
                root, "unchanged_since:scripts/gone.py:t2:" + "0" * 64)
            self.assertFalse(passed)
            self.assertIn("does not exist", why)

    def test_a_malformed_predicate_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            self.assertFalse(crc.evaluate_predicate(
                root, "unchanged_since:scripts/sub.py")[0])

    def test_reformatting_the_subject_does_not_trip_t2(self):
        """The end-to-end form of the property that decides adoption. If this
        fails, `ruff format` breaks every claim in the repo at once."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            predicate = self._pred(root)
            (root / "scripts" / "sub.py").write_text(
                'def f(x):\n    """Docs."""\n    return x+1\n', encoding="utf-8")
            self.assertTrue(crc.evaluate_predicate(root, predicate)[0])

    def test_a_docstring_edit_does_not_trip_t2_but_does_trip_t1(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            t2_pred = self._pred(root, "t2")
            t1_pred = self._pred(root, "t1")
            (root / "scripts" / "sub.py").write_text(
                'def f(x):\n    """Different prose."""\n    return x + 1\n', encoding="utf-8")
            self.assertTrue(crc.evaluate_predicate(root, t2_pred)[0])
            self.assertFalse(crc.evaluate_predicate(root, t1_pred)[0])

    def test_a_behaviour_change_trips_t2(self):
        """Non-vacuity: a predicate that never fails detects nothing, and
        every other test in this class would still pass."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            predicate = self._pred(root)
            (root / "scripts" / "sub.py").write_text(
                'def f(x):\n    """Docs."""\n    return x + 2\n', encoding="utf-8")
            self.assertFalse(crc.evaluate_predicate(root, predicate)[0])
