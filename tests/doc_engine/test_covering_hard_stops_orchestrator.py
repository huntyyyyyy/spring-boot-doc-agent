"""Cohesive suite from tests/doc_engine/test_covering_hard_stops.py: OrchestratorBarrierTest."""

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

class OrchestratorBarrierTest(unittest.TestCase):
    def test_run_scan_missing_receipt_refuses(self):
        """Deviation: scanner without covering_receipt still greens Path A."""

        class NoReceipt:
            name = "bogus"

            def version_hash(self) -> str:
                return "x"

            def scan(self, repo_path: str, **kwargs):
                return {"evidence": {}, "entity_table_map": {}}

        class DummyMerger:
            def merge(self, partials, repo_path, scanner_version, scanner_names=None):
                return {
                    "evidence": {},
                    "entity_table_map": {},
                    "file_signatures": {},
                    "scanner_version": scanner_version,
                    "scanners": scanner_names or [],
                }

        class DummyLineage:
            def resolve(self, merged, **kwargs):
                return merged

        with self.assertRaises(CoveringProofError) as ctx:
            run_scan(
                str(FIXTURE_DIR),
                [NoReceipt()],
                DummyMerger(),
                DummyLineage(),
            )
        self.assertIn("covering_receipt", str(ctx.exception))

    def test_run_scan_acked_mismatch_refuses(self):
        """Deviation: acked≠expected receipt still passes barrier."""

        class BadAck:
            name = "bad"

            def version_hash(self) -> str:
                return "x"

            def scan(self, repo_path: str, **kwargs):
                from doc_engine.scanning.covering import COVERING_RECEIPT_KEY

                return {
                    "evidence": {},
                    COVERING_RECEIPT_KEY: build_receipt(
                        scanner="bad",
                        version_hash="x",
                        scope="all",
                        expected_subset_root="aaa",
                        acked_subset_root="bbb",
                        status="complete",
                    ),
                }

        class DummyMerger:
            def merge(self, partials, repo_path, scanner_version, scanner_names=None):
                return {
                    "evidence": {},
                    "entity_table_map": {},
                    "file_signatures": {},
                    "scanner_version": scanner_version,
                    "scanners": scanner_names or [],
                }

        class DummyLineage:
            def resolve(self, merged, **kwargs):
                return merged

        with self.assertRaises(CoveringProofError):
            run_scan(
                str(FIXTURE_DIR),
                [BadAck()],
                DummyMerger(),
                DummyLineage(),
            )
