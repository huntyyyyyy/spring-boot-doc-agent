"""Coverage climb: covering proof receipt/verify/write edges."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from doc_engine import cli
from doc_engine.query.load import QueryError
from doc_engine.scanning import covering as cov
from doc_engine.tools import check_no_secrets_leaked as secrets
from doc_engine.tools import check_pipeline_output as cpo
from doc_engine.tools import pipeline_validators as pv
from doc_engine.tools import query_artifacts as qa
from doc_engine.tools import validate_artifacts as va

def test_covering_build_receipt_extra_and_verify_edges() -> None:
    sigs = {"a.java": "aa", "b.java": "bb"}
    root = cov.inventory_root(sigs)
    receipt = cov.build_receipt(
        scanner="filesystem",
        version_hash="v1",
        scope="all_signatures",
        expected_subset_root=root,
        acked_subset_root=root,
        status="complete",
        batches=2,
        extra={"note": "x"},
    )
    assert receipt["batches"] == 2 and receipt["note"] == "x"
    ok, why = cov.verify_covering_proof(
        cov.build_covering_proof(
            file_signatures=sigs, scanner_version="sv", receipts=[receipt]
        ),
        file_signatures=sigs,
        scanner_version="sv",
    )
    assert ok and why == ""
    assert "unsupported covering_proof schema_version" in (
        cov._schema_version_error({"schema_version": 99}) or ""
    )
    assert cov._root_and_version_error(
        {"inventory_root": "nope", "scanner_version": "sv", "barrier": {}},
        expected_root=root,
        scanner_version="sv",
    )
    assert cov._root_and_version_error(
        {
            "inventory_root": root,
            "scanner_version": "other",
            "barrier": {"inventory_root": root},
        },
        expected_root=root,
        scanner_version="sv",
    )
    assert cov._root_and_version_error(
        {
            "inventory_root": root,
            "scanner_version": "sv",
            "barrier": {"inventory_root": "x"},
        },
        expected_root=root,
        scanner_version="sv",
    )
    assert "receipt failed" in (
        cov._receipt_status_error({"status": "failed", "scanner": "s", "error": "e"}) or ""
    )
    assert "not complete" in (
        cov._receipt_status_error({"status": "partial", "scanner": "s"}) or ""
    )
    assert cov._receipt_scope_root({"scope": ""}, sigs)[1]
    assert "unknown covering receipt scope" in (
        cov._receipt_scope_root({"scope": "weird"}, sigs)[1] or ""
    )
    bad = dict(receipt)
    bad["expected_subset_root"] = "wrong"
    assert cov._receipt_root_mismatch(bad, recomputed=root)
    bad2 = dict(receipt)
    bad2["acked_subset_root"] = "wrong"
    assert cov._receipt_root_mismatch(bad2, recomputed=root)
    assert "no receipts" in (cov._verify_receipts([], sigs) or "")
    assert cov.java_scope_paths(sigs) == ["a.java", "b.java"]
    assert cov.subset_root(sigs, ["missing.java", "a.java"]) != root


def test_covering_write_and_pop(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "covering_proof.json"
    cov.write_covering_proof(path, {"schema_version": 1})
    assert json.loads(path.read_text(encoding="utf-8"))["schema_version"] == 1
    partial = {"covering_receipt": {"scanner": "x"}, "keep": 1}
    assert cov.pop_receipt(partial) == {"scanner": "x"}
    assert "covering_receipt" not in partial
    assert (
        cov.covering_proof_path_for_signals_out(
            tmp_path / "out" / "spring_signals.json"
        ).name
        == "covering_proof.json"
    )
