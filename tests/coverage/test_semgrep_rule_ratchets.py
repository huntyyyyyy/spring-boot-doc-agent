"""Cohesive suite from tests/coverage/test_semgrep_rule_coverage.py: TestRatchet, TestFpRatchet, TestExitCodes."""

from __future__ import annotations

import collections
import json
import sys
import tempfile
import unittest
from pathlib import Path
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
import semgrep_rule_coverage as sc

class TestRatchet(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.real_baseline = sc.BASELINE_FILE
        sc.BASELINE_FILE = Path(self.tmp.name) / "baseline.json"

    def tearDown(self) -> None:
        sc.BASELINE_FILE = self.real_baseline
        self.tmp.cleanup()

    def baseline(self, counts: dict) -> None:
        sc.BASELINE_FILE.write_text(json.dumps({
            "schema_version": sc.SCHEMA_VERSION,
            "corpus": "fake",
            "counts": counts,
        }), encoding="utf-8")

    def test_a_rule_dropping_to_zero_is_a_regression(self) -> None:
        self.baseline({"a__b": 5})
        self.assertTrue(sc.check_ratchet(collections.Counter()))

    def test_rising_counts_pass(self) -> None:
        self.baseline({"a__b": 5})
        self.assertEqual(sc.check_ratchet(collections.Counter({"a__b": 9})), [])

    def test_a_rule_that_was_already_zero_is_not_a_regression(self) -> None:
        self.baseline({"a__b": 0})
        self.assertEqual(sc.check_ratchet(collections.Counter()), [])

    def test_a_missing_baseline_is_a_failure(self) -> None:
        """Recall SoR absent ≠ OK (fail-closed; do not invent a baseline)."""
        self.assertFalse(sc.BASELINE_FILE.is_file())
        problems = sc.check_ratchet(collections.Counter())
        self.assertTrue(problems)
        self.assertTrue(any("missing" in p.lower() for p in problems), problems)

    def test_a_stale_schema_version_is_rejected(self) -> None:
        sc.BASELINE_FILE.write_text(
            json.dumps({"schema_version": 999, "counts": {}}), encoding="utf-8")
        self.assertTrue(sc.check_ratchet(collections.Counter()))

    def test_missing_counts_key_is_rejected(self) -> None:
        sc.BASELINE_FILE.write_text(json.dumps({
            "schema_version": sc.SCHEMA_VERSION,
            "corpus": "fake",
        }), encoding="utf-8")
        problems = sc.check_ratchet(collections.Counter())
        self.assertTrue(any("counts" in p for p in problems), problems)


class TestFpRatchet(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.real_fp = sc.FP_BASELINE_FILE
        self.real_neg = sc.NEGATIVE_FIXTURE_DIR
        sc.FP_BASELINE_FILE = Path(self.tmp.name) / "fp_baseline.json"

    def tearDown(self) -> None:
        sc.FP_BASELINE_FILE = self.real_fp
        sc.NEGATIVE_FIXTURE_DIR = self.real_neg
        self.tmp.cleanup()

    def fp_baseline(self, counts: dict) -> None:
        sc.FP_BASELINE_FILE.write_text(json.dumps({
            "schema_version": sc.SCHEMA_VERSION,
            "corpus": "fake",
            "counts": counts,
        }), encoding="utf-8")

    def test_a_rising_fp_count_is_a_regression(self) -> None:
        self.fp_baseline({"a__b": 0})
        self.assertTrue(sc.check_fp_ratchet(collections.Counter({"a__b": 2})))

    def test_falling_fp_counts_pass(self) -> None:
        self.fp_baseline({"a__b": 3})
        self.assertEqual(sc.check_fp_ratchet(collections.Counter({"a__b": 1})), [])

    def test_missing_fp_baseline_fails_closed(self) -> None:
        # file absent
        problems = sc.check_fp_ratchet(collections.Counter())
        self.assertTrue(any("missing" in p for p in problems), problems)

    def test_missing_negative_dir_fails(self) -> None:
        sc.NEGATIVE_FIXTURE_DIR = Path(self.tmp.name) / "no-negatives"
        self.assertTrue(any("missing" in p for p in sc.check_fp_ratchet()))

    def test_committed_negatives_pass_fp_ratchet(self) -> None:
        try:
            sc.find_semgrep()
        except sc.SemgrepNotFoundError:
            self.skipTest("semgrep not on PATH")
        sc.FP_BASELINE_FILE = self.real_fp
        sc.NEGATIVE_FIXTURE_DIR = self.real_neg
        self.assertEqual(sc.check_fp_ratchet(), [])


class TestExitCodes(unittest.TestCase):
    """Assert the exit code, not an internal list -- the exit code is what CI
    actually reads."""

    def test_fixture_mode_exits_zero_or_two_without_semgrep(self) -> None:
        code = sc.main([])
        try:
            sc.find_semgrep()
            self.assertEqual(code, 0)
        except sc.SemgrepNotFoundError:
            self.assertEqual(code, 2)

    def test_a_missing_target_directory_exits_two(self) -> None:
        self.assertEqual(sc.main(["no-such-directory-here"]), 2)

    def test_fp_ratchet_failure_exits_one(self) -> None:
        try:
            sc.find_semgrep()
        except sc.SemgrepNotFoundError:
            self.skipTest("semgrep not on PATH")
        with tempfile.TemporaryDirectory() as tmp:
            real_fp = sc.FP_BASELINE_FILE
            real_neg = sc.NEGATIVE_FIXTURE_DIR
            neg = Path(tmp) / "neg"
            neg.mkdir()
            # empty negatives → all zeros; baseline with zeros for known rules
            # then inject a rise via stubbed hit_counts
            fp = Path(tmp) / "fp.json"
            fp.write_text(json.dumps({
                "schema_version": sc.SCHEMA_VERSION,
                "counts": {rid: 0 for rid in sc.rule_ids()},
            }), encoding="utf-8")
            original_hits = sc.hit_counts
            try:
                sc.FP_BASELINE_FILE = fp
                sc.NEGATIVE_FIXTURE_DIR = neg
                sc.hit_counts = lambda *a, **k: collections.Counter(  # type: ignore[assignment]
                    {sc.rule_ids()[0]: 3}
                )
                self.assertEqual(sc.main([]), 1)
            finally:
                sc.FP_BASELINE_FILE = real_fp
                sc.NEGATIVE_FIXTURE_DIR = real_neg
                sc.hit_counts = original_hits  # type: ignore[assignment]

    def test_update_fp_baseline_writes_file(self) -> None:
        try:
            sc.find_semgrep()
        except sc.SemgrepNotFoundError:
            self.skipTest("semgrep not on PATH")
        with tempfile.TemporaryDirectory() as tmp:
            real = sc.FP_BASELINE_FILE
            try:
                sc.FP_BASELINE_FILE = Path(tmp) / "fp.json"
                self.assertEqual(sc.main(["--update-fp-baseline"]), 0)
                self.assertTrue(sc.FP_BASELINE_FILE.is_file())
                payload = json.loads(sc.FP_BASELINE_FILE.read_text(encoding="utf-8"))
                self.assertEqual(payload["corpus"], "semgrep_rule_fixtures_negative")
                self.assertEqual(payload["schema_version"], sc.SCHEMA_VERSION)
            finally:
                sc.FP_BASELINE_FILE = real
