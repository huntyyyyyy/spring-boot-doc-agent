"""Cohesive suite from tests/ratchets/test_drift_normalization.py: Test03SemanticChangesMustBeCaught, Test04NormalizerCandidates, Test05NormalizerProperties."""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest
from typing import Callable, Dict, List, NamedTuple, Optional
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.scanning import java_extract
from doc_engine.scanning import _scanner_astgrep as astgrep_backend
from doc_engine.tools import spring_drift_check, spring_signal_scan
import drift_match_normalizers as norms
import java_perturbations as perturb

import pytest

pytestmark = pytest.mark.domain_ci_meta

SCRIPT_DIR = SCRIPTS_DIR
FIXTURES = os.path.join(SCRIPT_DIR, "fixtures", "spring_signals")
_BILLING = os.path.join("src", "main", "java", "com", "example", "billing")
CONTROLLER_REL = os.path.join(_BILLING, "InvoiceController.java")
LEDGER_REL = os.path.join(_BILLING, "PaymentLedger.java")
CONFIRMING = ("confirmed_still_present", "unchanged")
CONTROLLER_BASENAME = "InvoiceController.java"
LEDGER_BASENAME = "PaymentLedger.java"
SEMANTIC_TOUCHED = frozenset({CONTROLLER_BASENAME, LEDGER_BASENAME})
from tests.support.drift_normalization import harness as dn
from tests.support.drift_normalization.harness import (
    Outcome,
    _apply_to_java,
    _citation_count,
    _fixtures_usable,
    _locate_getmapping_line,
    _report_basename,
    _run_scenario,
    _semantic_edits,
)
from tests.ratchets.test_drift_normalization_harness_gate import Test02TheKnownGap


def setUpModule() -> None:
    dn.setUpModule()


def tearDownModule() -> None:
    dn.tearDownModule()

class Test03SemanticChangesMustBeCaught(unittest.TestCase):
    """Arm 2. Without this class, every assertion above could be satisfied by a
    checker that confirms everything."""

    def _graded(self, cand: str) -> List[dict]:
        outcome = dn.OUTCOMES[f"{cand}/semantic"]
        self.assertTrue(outcome.valid,
                        "the semantic edits changed the citation count, so they "
                        "are not comparable to the formatting arm")
        return [
            r for r in outcome.report["results"]
            if _report_basename(r["file"]) in SEMANTIC_TOUCHED
        ]

    def _is_expected_to_drift(self, r: dict) -> bool:
        """Hand-labelled. Deriving the expected set from a fresh scan would
        grade the checker against a restatement of its own comparison."""
        return (
            (_report_basename(r["file"]) == CONTROLLER_BASENAME
             and r["line"] == dn.GETMAPPING_LINE)
            or r["source"] == "entity_table_map.PaymentLedger"
        )

    def test_a_changed_mapping_and_a_renamed_table_are_both_reported(self):
        graded = self._graded(norms.STATUS_QUO)
        expected = [r for r in graded if self._is_expected_to_drift(r)]
        self.assertEqual(2, len(expected),
                         "the two labelled citations are no longer present in the "
                         "report at all -- the labels have gone stale")
        for r in expected:
            with self.subTest(source=r["source"], line=r["line"]):
                self.assertEqual("drifted", r["status"])

    def test_untouched_citations_in_the_same_files_are_not_reported(self):
        """Over-reporting inside a genuinely-changed file is the failure mode
        the whole two-tier design exists to avoid -- see spring_drift_check's
        "WHY TWO TIERS" docstring."""
        for r in self._graded(norms.STATUS_QUO):
            if self._is_expected_to_drift(r):
                continue
            with self.subTest(source=r["source"], line=r["line"]):
                self.assertIn(r["status"], CONFIRMING,
                              f"{r['match']!r} did not change but was reported "
                              f"{r['status']}")

class Test04NormalizerCandidates(unittest.TestCase):
    """The comparison table from drift_match_normalizers.py's docstring,
    re-derived rather than quoted -- a table in a comment goes stale silently,
    and this repo has been bitten by exactly that."""

    ZERO_FALSE_POSITIVE = ("strip_ws_outside_strings", "tokens")

    def _false_positives(self, cand: str) -> int:
        total = 0
        for p_name in perturb.FORMATTING_ONLY:
            outcome = dn.OUTCOMES[f"{cand}/{p_name}"]
            self.assertTrue(outcome.valid, f"{cand}/{p_name} failed the validity gate")
            total += len(outcome.drifted())
        return total

    def test_the_status_quo_is_the_row_with_false_positives(self):
        self.assertEqual(Test02TheKnownGap.KNOWN_FALSE_POSITIVES,
                         self._false_positives(norms.STATUS_QUO))

    def test_collapsing_whitespace_alone_does_not_help(self):
        """Recorded because it is the obvious first fix and it does not work:
        '@Get( "/x" )' still differs from '@Get("/x")'. Pinning the negative
        result stops it being re-proposed."""
        self.assertEqual(Test02TheKnownGap.KNOWN_FALSE_POSITIVES,
                         self._false_positives("collapse_ws"))

    def test_the_stronger_candidates_reach_zero_false_positives(self):
        for cand in self.ZERO_FALSE_POSITIVE:
            with self.subTest(normalizer=cand):
                self.assertEqual(0, self._false_positives(cand))

    def test_no_candidate_buys_that_by_missing_a_real_change(self):
        """The non-vacuity check on the table itself. A candidate reaching zero
        false positives while confirming a renamed table has not improved
        anything -- it has stopped working."""
        for cand in norms.CANDIDATES:
            with self.subTest(normalizer=cand):
                outcome = dn.OUTCOMES[f"{cand}/semantic"]
                graded = [
                    r for r in outcome.report["results"]
                    if _report_basename(r["file"]) in SEMANTIC_TOUCHED
                ]
                missed = [r for r in graded
                          if Test03SemanticChangesMustBeCaught._is_expected_to_drift(self, r)
                          and r["status"] in CONFIRMING]
                self.assertEqual([], missed,
                                 f"{cand} confirmed a citation that really changed")

class Test05NormalizerProperties(unittest.TestCase):
    """Properties of the candidate relations themselves, independent of the
    corpus -- these would still hold if the fixtures were deleted."""

    def test_every_candidate_is_stable_under_whitespace(self):
        wrapped = '@RequestMapping(\n        "/api/invoices"\n)'
        flat = '@RequestMapping("/api/invoices")'
        for name in Test04NormalizerCandidates.ZERO_FALSE_POSITIVE:
            with self.subTest(normalizer=name):
                fn = norms.CANDIDATES[name]
                self.assertEqual(fn(wrapped), fn(flat))

    def test_every_candidate_still_separates_a_changed_literal(self):
        """The direction that matters: stability must not become blindness."""
        a = '@GetMapping("/{id}")'
        b = '@GetMapping("/{invoiceId}")'
        for name, fn in norms.CANDIDATES.items():
            with self.subTest(normalizer=name):
                self.assertNotEqual(fn(a), fn(b))

    def test_the_token_separator_cannot_occur_in_java_source(self):
        """What makes `tokens` injective where strip_ws_outside_strings is not.
        If this ever stops holding, two distinct token sequences could join to
        the same string and the relation silently loses its guarantee."""
        self.assertEqual(1, len(norms.TOKEN_SEP))
        self.assertFalse(norms.TOKEN_SEP.isprintable())
        seen_java = False
        for dirpath, _dirs, files in os.walk(FIXTURES):
            for fname in sorted(files):
                if not fname.endswith(".java"):
                    continue
                seen_java = True
                with open(os.path.join(dirpath, fname), encoding="utf-8") as f:
                    self.assertNotIn(norms.TOKEN_SEP, f.read())
        self.assertTrue(seen_java, f"no .java under nested fixtures at {FIXTURES}")

    def test_stripping_whitespace_outside_strings_is_not_injective(self):
        """Asserts the known weakness of the runner-up, so the choice of
        `tokens` rests on a demonstrated collision rather than on taste."""
        fn = norms.CANDIDATES["strip_ws_outside_strings"]
        self.assertEqual(fn("int a"), fn("inta"))
        self.assertNotEqual(norms.tokens("int a"), norms.tokens("inta"))

    def test_whitespace_inside_a_string_literal_is_preserved(self):
        """A query or path with meaningful internal spacing must not be
        normalized into equality with a different one."""
        for name in Test04NormalizerCandidates.ZERO_FALSE_POSITIVE:
            with self.subTest(normalizer=name):
                fn = norms.CANDIDATES[name]
                self.assertNotEqual(fn('@Q("select a")'), fn('@Q("selecta")'))
