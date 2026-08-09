"""Cohesive suite from tests/doc_engine/test_covering_absence_recall.py: CoveringProofTest, CoveringWriteRoundTripTest."""

from __future__ import annotations

import unittest
from pathlib import Path
from doc_engine.scanning.absence import write_absence_facts
from doc_engine.scanning.covering import (
    build_covering_proof,
    build_receipt,
    inventory_root,
    subset_root,
    verify_covering_proof,
    write_covering_proof,
)
from doc_engine.scanning.gap_probe import (
    CoveringPreconditionError,
    build_gap_report,
    measure_r_absence,
    measure_r_recall,
)
from doc_engine.scanning.recall_delta import write_recall_miss_facts

class CoveringProofTest(unittest.TestCase):
    def test_inventory_root_stable(self):
        sigs = {"a.java": "aaa", "b.yml": "bbb"}
        self.assertEqual(inventory_root(sigs), inventory_root(dict(reversed(list(sigs.items())))))

    def test_subset_root_diverges_on_missing_path(self):
        sigs = {"a.java": "aaa"}
        self.assertNotEqual(
            subset_root(sigs, ["a.java"]),
            subset_root(sigs, ["a.java", "missing.java"]),
        )

    def test_verify_requires_acked_eq_expected(self):
        sigs = {"x.java": "1"}
        root = inventory_root(sigs)
        good = build_receipt(
            scanner="filesystem",
            version_hash="v",
            scope="all_signatures",
            expected_subset_root=root,
            acked_subset_root=root,
            status="complete",
        )
        proof = build_covering_proof(
            file_signatures=sigs,
            scanner_version="sv",
            receipts=[good],
        )
        ok, why = verify_covering_proof(proof, file_signatures=sigs, scanner_version="sv")
        self.assertTrue(ok, why)

        bad = dict(good)
        bad["acked_subset_root"] = "nope"
        proof_bad = build_covering_proof(
            file_signatures=sigs,
            scanner_version="sv",
            receipts=[bad],
        )
        ok2, why2 = verify_covering_proof(
            proof_bad, file_signatures=sigs, scanner_version="sv",
        )
        self.assertFalse(ok2)
        self.assertIn("acked_subset_root", why2)


class CoveringWriteRoundTripTest(unittest.TestCase):
    def test_write_covering_proof(self):
        import tempfile

        sigs = {"z.java": "zz"}
        root = inventory_root(sigs)
        proof = build_covering_proof(
            file_signatures=sigs,
            scanner_version="sv",
            receipts=[
                build_receipt(
                    scanner="ast-grep",
                    version_hash="v",
                    scope="java",
                    expected_subset_root=subset_root(sigs, ["z.java"]),
                    acked_subset_root=subset_root(sigs, ["z.java"]),
                    status="complete",
                )
            ],
        )
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "covering_proof.json"
            write_covering_proof(path, proof)
            self.assertTrue(path.is_file())
            ok, why = verify_covering_proof(
                proof, file_signatures=sigs, scanner_version="sv",
            )
            self.assertTrue(ok, why)
            self.assertEqual(proof["inventory_root"], root)
