"""Cohesive suite from tests/doc_engine/test_covering_hard_stops.py: CoveringPropertyTest, CoveringContractTest, CoveringWriterFactsIntegrationTest."""

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

class CoveringPropertyTest(unittest.TestCase):
    def test_inventory_root_permutation_invariant(self):
        """Deviation: inventory_root depends on dict iteration order."""
        items = [(f"f{i}.java", f"sig{i}") for i in range(20)]
        a = inventory_root(dict(items))
        b = inventory_root(dict(reversed(items)))
        c = inventory_root({k: v for k, v in sorted(items, key=lambda kv: kv[0][::-1])})
        self.assertEqual(a, b)
        self.assertEqual(a, c)

    def test_subset_root_monotonic_on_path_add(self):
        """Deviation: adding a path leaves subset_root unchanged."""
        sigs = {"a.java": "1", "b.java": "2"}
        r1 = subset_root(sigs, ["a.java"])
        r2 = subset_root(sigs, ["a.java", "b.java"])
        self.assertNotEqual(r1, r2)

    def test_matching_garbage_subset_roots_are_rejected(self):
        """Deviation: expected==acked garbage still verifies if inventory is honest."""
        sigs = {"a.java": "1", "b.kt": "2"}
        proof = build_covering_proof(
            file_signatures=sigs,
            scanner_version="sv",
            receipts=[
                build_receipt(
                    scanner="ast-grep",
                    version_hash="v",
                    scope="java",
                    expected_subset_root="deadbeef",
                    acked_subset_root="deadbeef",
                    status="complete",
                )
            ],
        )
        ok, why = verify_covering_proof(
            proof, file_signatures=sigs, scanner_version="sv",
        )
        self.assertFalse(ok, why)
        self.assertIn("recomputed", why)

    def test_honest_java_scope_receipt_verifies(self):
        sigs = {"a.java": "1", "b.kt": "2"}
        proof = build_covering_proof(
            file_signatures=sigs,
            scanner_version="sv",
            receipts=[_complete_receipt("ast-grep", sigs)],
        )
        ok, why = verify_covering_proof(
            proof, file_signatures=sigs, scanner_version="sv",
        )
        self.assertTrue(ok, why)


class CoveringContractTest(unittest.TestCase):
    def test_covering_proof_schema_accepts_emitted_proof(self):
        """Deviation: emitted covering_proof fails its own schema contract."""
        schema = json.loads(
            (REPO_ROOT / "scripts" / "schemas" / "covering_proof.schema.json").read_text(
                encoding="utf-8"
            )
        )
        sigs = {"a.java": "x"}
        root = inventory_root(sigs)
        proof = build_covering_proof(
            file_signatures=sigs,
            scanner_version="sv",
            receipts=[_complete_receipt("filesystem", sigs), _complete_receipt("ast-grep", sigs)],
        )
        for key in schema["required"]:
            self.assertIn(key, proof)
        self.assertEqual(proof["schema_version"], schema["properties"]["schema_version"]["const"])
        self.assertEqual(proof["schema_version"], COVERING_PROOF_SCHEMA_VERSION)
        self.assertGreaterEqual(len(proof["receipts"]), 1)
        for receipt in proof["receipts"]:
            for key in schema["properties"]["receipts"]["items"]["required"]:
                self.assertIn(key, receipt)
            self.assertIn(receipt["status"], {"complete", "failed"})

    def test_facts_jsonl_absence_unproven_recall_roundtrip(self):
        """Deviation: ABSENCE/UNPROVEN/RECALL_MISS rejected by Fact or lose fields on disk."""
        facts = write_absence_facts(
            _kafka_signals(),
            covering_ok=True,
            covering_root="root",
            scanner_version="sv",
            astgrep_receipt_complete=True,
        )
        facts.extend(
            write_recall_miss_facts(
                {"entity_table_map": {}},
                native_entity_keys=set(),
                oracle_entity_keys={"Hidden"},
                oracle_arm="codeql",
            )
        )
        for f in facts:
            Fact.model_validate(f)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "facts.jsonl"
            write_facts_jsonl(path, facts)
            loaded = [
                json.loads(line)
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        self.assertEqual(len(loaded), len(facts))
        predicates = {f["predicate"] for f in loaded}
        self.assertIn("ABSENCE", predicates)
        self.assertIn("RECALL_MISS", predicates)
        for row in loaded:
            Fact.model_validate(row)


class CoveringWriterFactsIntegrationTest(unittest.TestCase):
    def test_covering_writer_facts_emits_recall_from_partials_meta(self):
        """Deviation: RECALL_MISS not emitted from _scan_partials_meta keys."""
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
        signals = {
            "file_signatures": sigs,
            "scanner_version": "sv",
            "evidence": {"deployment": [], "messaging": []},
            "config_key_sets": {},
            "entity_table_map": {},
            "_covering_proof": proof,
            "_scan_partials_meta": {
                "scanner_names": ["filesystem", "ast-grep", "codeql"],
                "entity_keys_by_scanner": {
                    "ast-grep": ["Seen"],
                    "codeql": ["Seen", "Missed"],
                    "filesystem": [],
                },
            },
        }
        facts = covering_writer_facts(signals)
        misses = [f for f in facts if f["predicate"] == "RECALL_MISS"]
        self.assertEqual([m["qualifiers"]["display_name"] for m in misses], ["Missed"])
