"""Cohesive suite from tests/doc_engine/test_covering_hard_stops.py: RecallVerdictFalsifiersTest."""

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

class RecallVerdictFalsifiersTest(unittest.TestCase):
    def test_recall_codeql_impl_is_evidentiary(self):
        """Deviation: *Impl CodeQL-only miss labelled STRUCTURAL."""
        facts = write_recall_miss_facts(
            {"entity_table_map": {}},
            native_entity_keys=set(),
            oracle_entity_keys={"FooImpl"},
            oracle_arm="codeql",
        )
        self.assertEqual(facts[0]["qualifiers"]["verdict"], "EVIDENTIARY")

    def test_recall_codeql_non_impl_is_structural(self):
        """Deviation: source-reachable miss labelled EVIDENTIARY."""
        facts = write_recall_miss_facts(
            {"entity_table_map": {}},
            native_entity_keys={"Seen"},
            oracle_entity_keys={"Seen", "HiddenEntity"},
            oracle_arm="codeql",
        )
        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0]["qualifiers"]["verdict"], "STRUCTURAL")
        self.assertEqual(facts[0]["qualifiers"]["display_name"], "HiddenEntity")

    def test_collect_arm_entity_keys_separates_native_and_oracle(self):
        """Deviation: CodeQL keys folded into native ast-grep bag."""
        native, oracle, arm = collect_arm_entity_keys(
            [
                {"entity_table_map_candidates": {"A": [{}]}},
                {"entity_table_map_candidates": {"B": [{}], "C": [{}]}},
                {"entity_table_map": {}},
            ],
            scanner_names=["ast-grep", "codeql", "filesystem"],
        )
        self.assertEqual(native, {"A"})
        self.assertEqual(oracle, {"B", "C"})
        self.assertEqual(arm, "codeql")
