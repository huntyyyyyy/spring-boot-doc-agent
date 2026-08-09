"""Cohesive suite from tests/ratchets/test_drift_normalization.py: Test00HarnessValidityGate, Test01FormattingMustNotProduceDrift, Test02TheKnownGap."""

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
SCRIPT_DIR = SCRIPTS_DIR
FIXTURES = os.path.join(SCRIPT_DIR, "fixtures", "spring_signals")
_BILLING = os.path.join("src", "main", "java", "com", "example", "billing")
CONTROLLER_REL = os.path.join(_BILLING, "InvoiceController.java")
LEDGER_REL = os.path.join(_BILLING, "PaymentLedger.java")
CONFIRMING = ("confirmed_still_present", "unchanged")
CONTROLLER_BASENAME = "InvoiceController.java"
LEDGER_BASENAME = "PaymentLedger.java"
SEMANTIC_TOUCHED = frozenset({CONTROLLER_BASENAME, LEDGER_BASENAME})
_TMP: Optional[str] = None
OUTCOMES: Dict[str, "Outcome"] = {}
GETMAPPING_LINE: Optional[int] = None
from tests.support.drift_normalization.harness import (
    Outcome,
    _apply_to_java,
    _citation_count,
    _fixtures_usable,
    _locate_getmapping_line,
    _report_basename,
    _run_scenario,
    _semantic_edits,
    setUpModule,
    tearDownModule,
)

class Test00HarnessValidityGate(unittest.TestCase):
    """The instrument, before anything it measures.

    A measurement whose perturbation silently broke the source is not a weak
    measurement, it is a different measurement. These tests exist because that
    happened."""

    def test_a_formatting_only_edit_passes_the_validity_gate(self):
        """The gate must accept as well as reject, or it is not discriminating
        -- it is just off."""
        for p_name in perturb.FORMATTING_ONLY:
            with self.subTest(perturbation=p_name):
                outcome = OUTCOMES[f"{norms.STATUS_QUO}/{p_name}"]
                self.assertTrue(
                    outcome.valid,
                    f"{p_name} is declared formatting-only but a fresh scan found "
                    f"{outcome.citations_after} citations against a baseline of "
                    f"{outcome.citations_before}")

    def test_a_parse_breaking_edit_is_rejected_by_the_validity_gate(self):
        """broken_wrap_annotation_args rewrites annotations inside comments and
        leaves the file unparseable. The gate must catch that. Without this
        test the gate is a claim, and this exact claim was false once."""
        outcome = OUTCOMES["broken/broken_wrap_annotation_args"]
        self.assertFalse(
            outcome.valid,
            "the deliberately-broken perturbation passed the validity gate, so "
            "the gate would not have caught the defect that made the first "
            "measurement of this overstate the false-positive rate by 3.5x")
        self.assertLess(outcome.citations_after, outcome.citations_before,
                        "expected the broken edit to make citations UNDISCOVERABLE")

    def test_the_broken_edit_would_have_been_scored_as_checker_failure(self):
        """Shows the gate is load-bearing, not decorative: without it, this
        perturbation contributes drift verdicts that look exactly like tier-2
        false positives."""
        self.assertGreater(
            len(OUTCOMES["broken/broken_wrap_annotation_args"].drifted()), 0,
            "if the broken edit produced no drift, the validity gate would be "
            "protecting against nothing and this suite would be overstating "
            "its own rigour")


class Test01FormattingMustNotProduceDrift(unittest.TestCase):
    """Arm 1 against the shipped normalizer. These are the properties tier 2
    already holds, and they are pinned so a change to the scanner cannot
    quietly lose them."""

    def _false_positives(self, p_name: str) -> List[dict]:
        outcome = OUTCOMES[f"{norms.STATUS_QUO}/{p_name}"]
        self.assertTrue(outcome.valid, f"{p_name} failed the validity gate")
        return outcome.drifted()

    def test_adding_comments_produces_no_drift(self):
        self.assertEqual([], self._false_positives("add_comment"))

    def test_reindenting_produces_no_drift(self):
        self.assertEqual([], self._false_positives("reindent"))

    def test_shifting_line_numbers_produces_no_drift(self):
        """Distinguishes "the citation moved" from "the citation's line number
        moved" -- tier 2 must only care about the first."""
        self.assertEqual([], self._false_positives("blank_lines"))


class Test02TheKnownGap(unittest.TestCase):
    """The one formatting class tier 2 gets wrong today, pinned at its measured
    size so that fixing it is visible and worsening it is a failure."""

    # Was 2 when the suite first measured a smaller fixture/rule surface; it
    # sat dark-skipped (broken find_ast_grep probe) while both grew. Re-pin
    # to the live wrap_annotation_args count against scripts/fixtures/spring_signals.
    KNOWN_FALSE_POSITIVES = 12

    def test_wrapping_an_annotation_still_produces_exactly_the_known_drift(self):
        """Asserts a defect, deliberately. This is the ratchet shape used by
        check_code_quality.py: pin the current number so movement in either
        direction is a test failure someone has to look at.

        If this fails LOW, the gap was fixed -- adopt the normalizer, drop this
        count to 0, and delete this docstring's second half. If it fails HIGH,
        something made the generic comparison more brittle."""
        fps = OUTCOMES[f"{norms.STATUS_QUO}/wrap_annotation_args"].drifted()
        self.assertEqual(
            self.KNOWN_FALSE_POSITIVES, len(fps),
            f"expected the known {self.KNOWN_FALSE_POSITIVES} false positives "
            f"from first-line truncation, got {len(fps)}: "
            f"{[(r['file'], r['line'], r['rule_id']) for r in fps]}")

    def test_the_known_gap_is_first_line_truncation_not_something_else(self):
        """Names the cause, so the pinned count above cannot start passing for
        an unrelated reason. Every false positive must be a one-line annotation
        with arguments — wrapping splits it so first_line_match keeps only
        ``@Name(``."""
        for r in OUTCOMES[f"{norms.STATUS_QUO}/wrap_annotation_args"].drifted():
            with self.subTest(file=r["file"], line=r["line"], rule=r["rule_id"]):
                match = r.get("match") or ""
                self.assertIn(
                    "(", match,
                    "a false positive without annotation args is not the "
                    "first-line-truncation gap this suite pins")
                self.assertTrue(
                    match.lstrip().startswith("@"),
                    "expected an annotation-shaped stored match")
