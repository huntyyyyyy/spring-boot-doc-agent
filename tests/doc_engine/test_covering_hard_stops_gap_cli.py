"""Cohesive suite from tests/doc_engine/test_covering_hard_stops.py: GapProbeS1S3CliTest."""

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

class GapProbeS1S3CliTest(unittest.TestCase):
    def test_run_gap_probe_missing_covering_raises(self):
            """Deviation: gap_probe scores S2 without covering_proof sibling."""
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                signals_path = root / "spring_signals.json"
                facts_path = root / "facts.jsonl"
                signals_path.write_text(
                    json.dumps(
                        {
                            "schema_version": 7,
                            "scanner_version": "sv",
                            "file_signatures": {"a.java": "1"},
                            "entity_table_map": {},
                            "evidence": {},
                        }
                    ),
                    encoding="utf-8",
                )
                facts_path.write_text("", encoding="utf-8")
                with self.assertRaises(CoveringPreconditionError):
                    run_gap_probe(signals_path, facts_path, root / "out")

    def test_gap_probe_cli_exit_3_on_missing_covering(self):
            """Deviation: gap_probe CLI exit 0 when covering missing."""
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                signals_path = root / "spring_signals.json"
                facts_path = root / "facts.jsonl"
                out = root / "gap"
                signals_path.write_text(
                    json.dumps(
                        {
                            "schema_version": 7,
                            "scanner_version": "sv",
                            "file_signatures": {"a.java": "1"},
                            "entity_table_map": {},
                            "evidence": {},
                        }
                    ),
                    encoding="utf-8",
                )
                facts_path.write_text("", encoding="utf-8")
                proc = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "doc_engine.tools.gap_probe",
                        "--signals",
                        str(signals_path),
                        "--facts",
                        str(facts_path),
                        "--out",
                        str(out),
                    ],
                    cwd=str(REPO_ROOT),
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
            self.assertEqual(proc.returncode, 3)
            self.assertFalse((out / "gap_report.json").is_file())

    def test_gap_report_omits_r_recall_without_oracle_arm(self):
            """Deviation: R_recall measured without trusted CodeQL receipt."""
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
            self.assertTrue(report["rates"]["R_recall"]["omitted"])
            self.assertEqual(report["rates"]["R_recall"]["claim"], "omitted_without_oracle")
            self.assertFalse(report["rates"]["oracle"]["trusted_codeql_arm"])
