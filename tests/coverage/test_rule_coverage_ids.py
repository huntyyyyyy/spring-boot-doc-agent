"""Cohesive suite from tests/coverage/test_rule_coverage.py: TestRuleIdParsing, TestNonVacuity, TestCommittedBaselineSoR."""

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

class TestRuleIdParsing(unittest.TestCase):
    def test_the_real_rule_file_yields_rules(self) -> None:
        """If this ever returns [], every other check here passes vacuously."""
        ids = rc.rule_ids()
        self.assertGreaterEqual(len(ids), 20)
        self.assertIn("persistence__entity", ids)

    def test_duplicate_rule_ids_are_deduplicated(self) -> None:
        """A query may repeat the same rule_id in multiple branches; the
        denominator must count each logical rule only once."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Dummy.ql"
            path.write_text(
                'rule_id = "bucket__real"\n'
                'rule_id = "bucket__real"\n'
                'rule_id = "bucket__other"\n',
                encoding="utf-8")
            self.assertEqual(rc.rule_ids(path), ["bucket__real", "bucket__other"])

    def test_as_rule_id_spelling_is_enumerated(self) -> None:
        """RawQueries.ql uses `"…" as rule_id`; missing it under-counts the pack."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Raw.ql"
            path.write_text('"bucket__as_form" as rule_id,\n', encoding="utf-8")
            self.assertEqual(rc.rule_ids(path), ["bucket__as_form"])
        self.assertIn("raw_queries__query", rc.rule_ids())
        self.assertGreaterEqual(len(rc.rule_ids()), 29)

class TestNonVacuity(unittest.TestCase):
    def test_every_real_rule_fires_on_the_fixture_corpus(self) -> None:
        """The invariant itself, against the committed fixtures."""
        self.assertEqual(rc.check_non_vacuity(), [])

    def test_a_rule_with_no_fixture_is_caught(self) -> None:
        """Proves the gate is not passing because it looked at nothing: a
        rule that exists but nothing triggers must be reported."""
        original = rc.rule_ids
        try:
            rc.rule_ids = lambda *a, **k: original() + ["invented__rule"]  # type: ignore[assignment]
            problems = rc.check_non_vacuity()
            self.assertTrue(any("invented__rule" in p for p in problems), problems)
        finally:
            rc.rule_ids = original  # type: ignore[assignment]

    def test_a_missing_fixture_corpus_fails_rather_than_passing(self) -> None:
        real_dir = rc.FIXTURE_DIR
        try:
            rc.FIXTURE_DIR = Path(tempfile.gettempdir()) / "definitely-not-here"
            self.assertTrue(rc.check_non_vacuity())
        finally:
            rc.FIXTURE_DIR = real_dir

    def test_an_empty_fixture_directory_fails(self) -> None:
        """Present-but-empty corpus is not a vacuous pass."""
        real_dir = rc.FIXTURE_DIR
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "spring_signals"
            empty.mkdir()
            try:
                rc.FIXTURE_DIR = empty
                problems = rc.check_non_vacuity()
                self.assertTrue(problems, "empty fixture dir must fail non-vacuity")
            finally:
                rc.FIXTURE_DIR = real_dir

    def test_an_empty_pack_fails_rather_than_passing_vacuously(self) -> None:
        original = rc.rule_ids
        try:
            rc.rule_ids = lambda *a, **k: []  # type: ignore[assignment]
            problems = rc.check_non_vacuity()
            self.assertTrue(any("empty" in p.lower() or "no rule" in p.lower()
                                for p in problems), problems)
        finally:
            rc.rule_ids = original  # type: ignore[assignment]

    def test_an_exemption_must_state_a_reason(self) -> None:
        real = dict(rc.FIXTURE_EXEMPT)
        try:
            rc.FIXTURE_EXEMPT["some__rule"] = "   "
            self.assertTrue(any("no stated reason" in p
                                for p in rc.check_non_vacuity()))
        finally:
            rc.FIXTURE_EXEMPT.clear()
            rc.FIXTURE_EXEMPT.update(real)

    def test_fixture_dir_is_spring_signals_not_metamorphic_rule_fixtures(self) -> None:
        """Corpus ownership: coverage SoR ≠ metamorphic rule_fixtures/."""
        resolved = rc.FIXTURE_DIR.resolve()
        self.assertEqual(resolved.name, "spring_signals")
        self.assertEqual(
            resolved,
            (SCRIPTS_DIR / "fixtures" / "spring_signals").resolve(),
        )
        metamorphic = (SCRIPTS_DIR / "coverage" / "rule_fixtures").resolve()
        self.assertNotEqual(resolved, metamorphic)

class TestCommittedBaselineSoR(unittest.TestCase):
    """Hermetic CI witness: committed baseline stamp matches SCHEMA_VERSION
    and count keys are pack-owned. Does not require an external corpus."""

    def test_write_baseline_keeps_only_pack_owned_keys(self) -> None:
        """--update must not reintroduce scanner-only / non-pack tags."""
        with tempfile.TemporaryDirectory() as tmp:
            real = rc.BASELINE_FILE
            try:
                rc.BASELINE_FILE = Path(tmp) / "baseline.json"
                counts = collections.Counter({
                    "persistence__entity": 3,
                    "deployment__build_gradle": 99,  # filesystem tag, not pack
                    "raw_queries__query": 7,
                })
                rc.write_baseline(Path(tmp) / "corpus", counts)
                data = json.loads(rc.BASELINE_FILE.read_text(encoding="utf-8"))
                self.assertEqual(data["schema_version"], rc.SCHEMA_VERSION)
                self.assertIn("persistence__entity", data["counts"])
                self.assertIn("raw_queries__query", data["counts"])
                self.assertNotIn("deployment__build_gradle", data["counts"])
            finally:
                rc.BASELINE_FILE = real
