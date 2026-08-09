"""Cohesive suite from tests/ci/test_check_no_client_identifiers.py: MinimalValidAggregateTest, UnknownKeyTest, GeneratedKeyPatternTest, StringValueVocabularyTest, ProseFieldTest, PatternedStringValueTest."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import List
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
import check_no_client_identifiers as gate
from tests.support.client_identifiers.harness import findings, run_main

class MinimalValidAggregateTest(unittest.TestCase):
    def test_a_minimal_valid_aggregate_has_no_findings(self) -> None:
        payload = {
            "schema_version": 1,
            "_producer": "stage0-oracle-compare",
            "evidence_tier": "source-text",
            "shared_input_digest": "0" * 64,
            "java_files_scanned": 10,
            "interfaces_with_extends": 5,
            "summaries": [],
            "misses": [],
            "unclassified_total": 0,
            "thresholds": {
                "min_recall": None,
                "max_unclassified": None,
                "note": "null until derived"
            }
        }
        self.assertEqual(findings(payload), [])


class UnknownKeyTest(unittest.TestCase):
    def test_an_unknown_top_level_key_is_a_finding(self) -> None:
        result = findings({"totally_new_field": 1})
        self.assertEqual(len(result), 1)
        self.assertIn("totally_new_field", result[0])
        self.assertIn("not in the allowlist", result[0])

    def test_an_unknown_nested_key_is_a_finding(self) -> None:
        result = findings({"summaries": [{"bogus_field": 1}]})
        self.assertEqual(len(result), 1)
        self.assertIn("bogus_field", result[0])


class GeneratedKeyPatternTest(unittest.TestCase):
    def test_a_valid_delta_by_cause_key_has_no_finding(self) -> None:
        self.assertEqual(
            findings({"delta_by_cause": {"INTERMEDIATE_BASE_INHERITANCE": 3}}), [])
        self.assertEqual(
            findings({"delta_by_cause": {"UNCLASSIFIED": 1}}), [])

    def test_an_invalid_delta_by_cause_key_is_a_finding(self) -> None:
        result = findings({"delta_by_cause": {"UNKNOWN_CAUSE": 1}})
        self.assertEqual(len(result), 1)
        self.assertIn("UNKNOWN_CAUSE", result[0])

    def test_a_valid_verdict_by_cause_key_has_no_finding(self) -> None:
        self.assertEqual(
            findings({"verdict_by_cause": {"META_OR_INHERITED_ANNOTATION": "INVESTIGATE"}}), [])

    def test_an_invalid_verdict_by_cause_key_is_a_finding(self) -> None:
        result = findings({"verdict_by_cause": {"SPURIOUS_CAUSE": "EVIDENTIARY"}})
        self.assertEqual(len(result), 1)


class StringValueVocabularyTest(unittest.TestCase):
    def test_allowed_producer_values_have_no_finding(self) -> None:
        self.assertEqual(findings({"_producer": "stage0-oracle-compare"}), [])

    def test_allowed_evidence_tier_values_have_no_finding(self) -> None:
        self.assertEqual(findings({"evidence_tier": "source-text"}), [])

    def test_allowed_arm_values_have_no_finding(self) -> None:
        self.assertEqual(findings({"arm": "native"}), [])
        self.assertEqual(findings({"arm": "multipass"}), [])

    def test_allowed_engine_values_have_no_finding(self) -> None:
        for engine in ["astgrep", "semgrep"]:
            self.assertEqual(findings({"variant": engine}), [])

    def test_a_string_value_outside_the_vocabulary_is_a_finding(self) -> None:
        result = findings({"_producer": "com.acme.client.OracleRunner"})
        self.assertEqual(len(result), 1)
        self.assertIn("not in the permitted vocabulary", result[0])


class ProseFieldTest(unittest.TestCase):
    def test_prose_with_no_package_shaped_token_has_no_finding(self) -> None:
        self.assertEqual(findings({"note": "measured over three runs"}), [])

    def test_prose_containing_a_package_shaped_token_is_a_finding(self) -> None:
        result = findings({"note": "seen in com.acme.client.service.FooBar"})
        self.assertEqual(len(result), 1)
        self.assertIn("com.acme.client.service", result[0])


class PatternedStringValueTest(unittest.TestCase):
    """shared_input_digest and entity_pseudonym are documented as
    generated-but-shape-constrained. A legitimate value matching the
    pattern has no finding; a package-name-shaped fake must be caught."""

    def test_a_valid_shared_input_digest_has_no_finding(self) -> None:
        valid_digest = "a" * 64
        self.assertEqual(findings({"shared_input_digest": valid_digest}), [])

    def test_an_invalid_shared_input_digest_is_a_finding(self) -> None:
        result = findings({"shared_input_digest": "not-hex"})
        self.assertEqual(len(result), 1)

    def test_a_valid_entity_pseudonym_has_no_finding(self) -> None:
        valid_pseudonym = "iface_" + "a" * 12
        self.assertEqual(findings({"entity_pseudonym": valid_pseudonym}), [])

    def test_an_invalid_entity_pseudonym_is_a_finding(self) -> None:
        result = findings({"entity_pseudonym": "com.acme.MyInterface"})
        self.assertEqual(len(result), 1)

    def test_a_package_shaped_fake_digest_is_still_a_finding(self) -> None:
        """The fix must enforce the pattern, not just allow-list the field --
        this is the non-vacuity proof for the fix itself."""
        result = findings({"shared_input_digest": "com.acme.client.service"})
        self.assertEqual(len(result), 1)
