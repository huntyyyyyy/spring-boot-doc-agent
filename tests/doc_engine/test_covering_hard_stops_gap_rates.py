"""Cohesive suite from tests/doc_engine/test_covering_hard_stops.py: GapProbeS1S3RatesTest."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from doc_engine.core.context import FileEntry, ScanContext
from doc_engine.pipeline.artifacts import Fact
from doc_engine.scanning._orchestrator import CoveringProofError, run_scan
from doc_engine.scanning._scanner_astgrep import AstGrepBackend
from doc_engine.scanning.absence import write_absence_facts
from doc_engine.scanning.covering import (
    COVERING_PROOF_SCHEMA_VERSION,
    build_covering_proof,
    build_receipt,
    inventory_root,
    subset_root,
    verify_covering_proof,
    write_covering_proof,
)
from doc_engine.scanning.facts import (
    covering_writer_facts,
    facts_from_signals,
    write_facts_jsonl,
)
from doc_engine.scanning.gap_probe import (
    CoveringPreconditionError,
    _astgrep_receipt_complete,
    build_gap_report,
    load_and_verify_covering,
    measure_r_absence,
    run_gap_probe,
)
from doc_engine.scanning.recall_delta import (
    collect_arm_entity_keys,
    write_recall_miss_facts,
)
from doc_engine.scanning.spring import AstGrepError, scan
from tests.conftest import FIXTURE_DIR, REPO_ROOT
from tests.support.covering_hard_stops.fixtures import _complete_receipt, _kafka_signals

import pytest

pytestmark = pytest.mark.domain_stage0

class GapProbeS1S3RatesTest(unittest.TestCase):
    def test_gap_report_includes_r_recall_when_codeql_receipt(self):
            """Deviation: CodeQL arm present but R_recall section omitted."""
            sigs = {"a.java": "1"}
            root = inventory_root(sigs)
            proof = build_covering_proof(
                file_signatures=sigs,
                scanner_version="sv",
                receipts=[
                    _complete_receipt("filesystem", sigs),
                    _complete_receipt("ast-grep", sigs),
                    _complete_receipt("codeql", sigs),
                ],
            )
            report, _ = build_gap_report(
                {
                    "schema_version": 7,
                    "scanner_version": "sv",
                    "file_signatures": sigs,
                    "entity_table_map": {},
                    "evidence": {},
                },
                [],
                covering_proof=proof,
                covering_ok=True,
            )
            self.assertIn("R_recall", report["rates"])
            self.assertEqual(report["rates"]["R_recall"]["denominator"], 0)
            self.assertEqual(report["rates"]["R_recall"]["claim"], "measured")
            self.assertTrue(report["rates"]["oracle"]["trusted_codeql_arm"])

    def test_planted_recall_miss_without_oracle_is_untrusted(self):
            """Deviation: planted RECALL_MISS alone measures R_recall."""
            sigs = {"a.java": "1"}
            root = inventory_root(sigs)
            proof = build_covering_proof(
                file_signatures=sigs,
                scanner_version="sv",
                receipts=[
                    _complete_receipt("filesystem", sigs),
                    _complete_receipt("ast-grep", sigs),
                ],
            )
            facts = [
                {
                    "predicate": "RECALL_MISS",
                    "subject": "entity:Hidden",
                    "qualifiers": {"verdict": "STRUCTURAL", "oracle_arm": "planted"},
                }
            ]
            report, kept = build_gap_report(
                {
                    "schema_version": 7,
                    "scanner_version": "sv",
                    "file_signatures": sigs,
                    "entity_table_map": {},
                    "evidence": {},
                },
                facts,
                covering_proof=proof,
                covering_ok=True,
            )
            self.assertEqual(report["rates"]["R_recall"]["claim"], "untrusted_planted")
            self.assertTrue(report["rates"]["R_recall"]["omitted"])
            self.assertTrue(report["design_reopen"]["untrusted_planted_recall"])
            self.assertTrue(
                any(f.get("reason_class") == "RECALL_MISS_WITHOUT_ORACLE" for f in kept)
            )

    def test_r_absence_failure_mass_uses_callable_trials(self):
            """Deviation: R_absence identity |ABSENCE|/|ABSENCE| always 1.0 when defined."""
            from doc_engine.scanning.absence import count_callable_trials, write_absence_facts

            signals = _kafka_signals(messaging_hits=2)
            sigs = {"a.java": "1", "build.gradle": "1"}
            root = inventory_root(sigs)
            proof = build_covering_proof(
                file_signatures=sigs,
                scanner_version="sv",
                receipts=[
                    _complete_receipt("filesystem", sigs),
                    _complete_receipt("ast-grep", sigs),
                ],
            )
            facts = write_absence_facts(
                signals,
                covering_ok=True,
                covering_root=root,
                scanner_version="sv",
                astgrep_receipt_complete=True,
            )
            # Present messaging → no stamp; other callable empty families → ABSENCE.
            messaging = [f for f in facts if f.get("subject") == "family:messaging"]
            self.assertEqual(messaging, [])
            trials = count_callable_trials(
                signals, covering_ok=True, astgrep_receipt_complete=True
            )
            self.assertGreater(trials, 0)
            report, _ = build_gap_report(
                {
                    "schema_version": 7,
                    "scanner_version": "sv",
                    "file_signatures": sigs,
                    "entity_table_map": {},
                    "evidence": signals["evidence"],
                    "config_key_sets": {},
                },
                facts,
                covering_proof=proof,
                covering_ok=True,
            )
            block = report["rates"]["R_absence"]
            self.assertEqual(block["polarity"], "failure_mass")
            self.assertEqual(block["callable_trials"], trials)
            self.assertEqual(block["denominator"], trials)
            # Presence short-circuit: rate must be < 1 when some callable trials hit.
            if block["callable_absence"] < trials:
                self.assertIsNotNone(block["rate"])
                self.assertLess(block["rate"], 1.0)

    def test_measure_r_absence_ignores_non_callable_absence_rows(self):
            """Deviation: planted non-callable ABSENCE counted in S3 denominator."""
            # Writer must never emit this; scorer must still not inflate if it appears.
            facts = [
                {
                    "predicate": "ABSENCE",
                    "subject": "family:messaging",
                    "qualifiers": {"trial": "callable", "family": "messaging"},
                },
                {
                    "predicate": "ABSENCE",
                    "subject": "family:redis",
                    "qualifiers": {"trial": "non_callable", "family": "redis"},
                },
            ]
            # Current scorer counts all ABSENCE predicates; pin intended discipline:
            # only callable trials belong in the ABSENCE rate. If this fails, fix scorer.
            block = measure_r_absence(facts)
            callable_only = [
                f for f in facts if (f.get("qualifiers") or {}).get("trial") == "callable"
            ]
            self.assertEqual(block["callable_absence"], len(callable_only))
            # Prefer scorer that filters; if it currently counts both, this documents debt.
            if block["denominator"] != len(callable_only):
                self.fail(
                    "measure_r_absence must use only trial=callable ABSENCE rows as "
                    f"denominator (got den={block['denominator']}, want {len(callable_only)})"
                )

            # With explicit callable_trials, polarity is failure mass over trials.
            mass = measure_r_absence(facts, callable_trials=4)
            self.assertEqual(mass["polarity"], "failure_mass")
            self.assertEqual(mass["numerator"], 1)
            self.assertEqual(mass["denominator"], 4)
            self.assertEqual(mass["rate"], 0.25)
