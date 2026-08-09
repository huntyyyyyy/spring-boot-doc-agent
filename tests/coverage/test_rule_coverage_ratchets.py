"""Cohesive suite from tests/coverage/test_rule_coverage.py: TestRatchet, TestExitCodes."""

from __future__ import annotations

import collections
import json
import sys
import tempfile
import unittest
from pathlib import Path
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
import rule_coverage as rc

import pytest

pytestmark = pytest.mark.domain_ci_meta

class TestRatchet(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.real_baseline = rc.BASELINE_FILE
        rc.BASELINE_FILE = Path(self.tmp.name) / "baseline.json"

    def tearDown(self) -> None:
        rc.BASELINE_FILE = self.real_baseline
        self.tmp.cleanup()

    def baseline(self, counts: dict, *, schema_version: int | None = None) -> None:
        rc.BASELINE_FILE.write_text(json.dumps({
            "schema_version": rc.SCHEMA_VERSION if schema_version is None else schema_version,
            "corpus": "fake",
            "counts": counts,
        }), encoding="utf-8")

    def test_a_rule_dropping_to_zero_is_a_regression(self) -> None:
        self.baseline({"a__b": 5})
        self.assertTrue(rc.check_ratchet(collections.Counter()))

    def test_rising_counts_pass(self) -> None:
        self.baseline({"a__b": 5})
        self.assertEqual(rc.check_ratchet(collections.Counter({"a__b": 9})), [])

    def test_a_rule_that_was_already_zero_is_not_a_regression(self) -> None:
        """Zero-to-zero is the ordinary case for a framework this corpus does
        not use, and flagging it would make the gate cry wolf permanently."""
        self.baseline({"a__b": 0})
        self.assertEqual(rc.check_ratchet(collections.Counter()), [])

    def test_partial_count_drop_is_not_a_regression(self) -> None:
        """Polarity pin: drop-to-zero only; 5→3 stays green (coverage-gates)."""
        self.baseline({"a__b": 5})
        self.assertEqual(rc.check_ratchet(collections.Counter({"a__b": 3})), [])

    def test_a_missing_baseline_is_a_failure(self) -> None:
        """SoR absent ≠ OK (L6 fail-closed)."""
        self.assertFalse(rc.BASELINE_FILE.is_file())
        problems = rc.check_ratchet(collections.Counter())
        self.assertTrue(problems)
        self.assertTrue(any("missing" in p.lower() or "absent" in p.lower()
                            for p in problems), problems)

    def test_a_stale_schema_version_is_rejected(self) -> None:
        rc.BASELINE_FILE.write_text(
            json.dumps({"schema_version": 999, "counts": {}}), encoding="utf-8")
        self.assertTrue(rc.check_ratchet(collections.Counter()))

    def test_counts_not_an_object_is_rejected(self) -> None:
        rc.BASELINE_FILE.write_text(json.dumps({
            "schema_version": rc.SCHEMA_VERSION,
            "counts": ["not", "an", "object"],
        }), encoding="utf-8")
        problems = rc.check_ratchet(collections.Counter())
        self.assertTrue(any("counts" in p for p in problems), problems)

    def test_missing_counts_key_is_rejected(self) -> None:
        rc.BASELINE_FILE.write_text(json.dumps({
            "schema_version": rc.SCHEMA_VERSION,
            "corpus": "fake",
        }), encoding="utf-8")
        problems = rc.check_ratchet(collections.Counter())
        self.assertTrue(any("counts" in p for p in problems), problems)

    def test_corrupt_json_baseline_is_rejected(self) -> None:
        rc.BASELINE_FILE.write_text("{not-json", encoding="utf-8")
        problems = rc.check_ratchet(collections.Counter())
        self.assertTrue(problems)
        self.assertTrue(any("json" in p.lower() or "parse" in p.lower()
                            for p in problems), problems)

class TestExitCodes(unittest.TestCase):
    """Assert the exit code, not an internal list -- the exit code is what CI
    actually reads."""

    def test_fixture_mode_exits_zero(self) -> None:
        self.assertEqual(rc.main([]), 0)

    def test_a_missing_target_directory_exits_two(self) -> None:
        self.assertEqual(rc.main(["no-such-directory-here"]), 2)

    def test_non_vacuity_failure_exits_one(self) -> None:
        original = rc.rule_ids
        try:
            rc.rule_ids = lambda *a, **k: original() + ["invented__exit1"]  # type: ignore[assignment]
            self.assertEqual(rc.main([]), 1)
        finally:
            rc.rule_ids = original  # type: ignore[assignment]

    def test_ratchet_failure_exits_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "corpus"
            repo.mkdir()
            (repo / "Empty.java").write_text("// empty\n", encoding="utf-8")
            real_baseline = rc.BASELINE_FILE
            baseline = Path(tmp) / "baseline.json"
            baseline.write_text(json.dumps({
                "schema_version": rc.SCHEMA_VERSION,
                "corpus": "fake",
                "counts": {"persistence__entity": 5},
            }), encoding="utf-8")
            try:
                rc.BASELINE_FILE = baseline
                self.assertEqual(rc.main([str(repo)]), 1)
            finally:
                rc.BASELINE_FILE = real_baseline
