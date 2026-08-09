"""Covering callable-absence core falsifiers."""

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
from tests.support.covering_hard_stops.fixtures import _absence_stamp_pairs, _assert_absence_stamps_match_writer, _complete_receipt, _kafka_signals

import pytest

pytestmark = pytest.mark.domain_stage0

class CallableAbsenceFalsifiersTest(unittest.TestCase):
    def test_astgrep_receipt_incomplete_forces_unproven(self):
            """Deviation: ABSENCE emitted when rule-pack receipt is incomplete."""
            facts = write_absence_facts(
                _kafka_signals(),
                covering_ok=True,
                covering_root="root",
                scanner_version="sv",
                astgrep_receipt_complete=False,
            )
            messaging = [f for f in facts if f["subject"] == "family:messaging"]
            self.assertEqual(messaging[0]["predicate"], "UNPROVEN")

    def test_present_family_emits_no_absence_row(self):
            """Deviation: callable present family still stamped ABSENCE/UNPROVEN."""
            facts = write_absence_facts(
                _kafka_signals(messaging_hits=2),
                covering_ok=True,
                covering_root="root",
                scanner_version="sv",
                astgrep_receipt_complete=True,
            )
            messaging = [f for f in facts if f["subject"] == "family:messaging"]
            self.assertEqual(messaging, [])
