"""Cohesive suite from tests/doc_engine/test_real_fixture_adversarial.py: TestCoveringVerifiedLie, TestJoinIncompleteEmptyDenom, TestBaselineBandsNotVacuous, TestContestedRaisesColl, TestForgedCoveringProof."""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest import mock
import pytest
from doc_engine.paths import repo_root
from doc_engine.real_fixture import real_artifacts_dir, real_repo_path
from doc_engine.scanning.covering import (
    build_covering_proof,
    build_receipt,
    inventory_root,
    verify_covering_proof,
)
from doc_engine.scanning.gap_probe import (
    CoveringPreconditionError,
    build_gap_report,
    measure_r_coll,
)
from doc_engine.scanning.symbol import format_type
from doc_engine.tools import spring_drift_check

pytestmark = pytest.mark.domain_stage0

REPO_ROOT = repo_root()
BASELINE = REPO_ROOT / "scripts" / "coverage" / "real_repo_gap_baseline.json"
from tests.support.real_fixture.adversarial_factories import (
    _maps_to_fact,
    _minimal_signals,
)

class TestCoveringVerifiedLie:
    """Deviation: covering_ok=True with no proof still claimed s1.verified."""

    def test_covering_ok_without_proof_is_not_verified(self) -> None:
        report, _ = build_gap_report(
            _minimal_signals(),
            [_maps_to_fact("com.example", "Order", "orders")],
            covering_ok=True,
            covering_why="",
            covering_proof=None,
        )
        assert report["s1_covering"]["proof_present"] is False
        assert report["s1_covering"]["verified"] is False
        assert report["s1_covering"]["inventory_root"] is None

    def test_covering_ok_with_proof_is_verified(self) -> None:
        sigs = {"Order.java": "abc"}
        root = inventory_root(sigs)
        proof = build_covering_proof(
            file_signatures=sigs,
            scanner_version="adv",
            receipts=[
                build_receipt(
                    scanner="filesystem",
                    version_hash="v",
                    scope="all_signatures",
                    expected_subset_root=root,
                    acked_subset_root=root,
                    status="complete",
                )
            ],
        )
        report, _ = build_gap_report(
            _minimal_signals(file_signatures=sigs),
            [_maps_to_fact("com.example", "Order", "orders")],
            covering_ok=True,
            covering_proof=proof,
        )
        assert report["s1_covering"]["verified"] is True
        assert report["s1_covering"]["proof_present"] is True
        assert report["s1_covering"]["inventory_root"] == root

    def test_covering_ok_false_still_refuses(self) -> None:
        signals = _minimal_signals()
        with pytest.raises(CoveringPreconditionError):
            build_gap_report(
                signals,
                [],
                covering_ok=False,
                covering_why="adversarial",
            )

class TestJoinIncompleteEmptyDenom:
    """Deviation: wiping entity_table_map left join_incomplete=False (rate None)."""

    def test_empty_path_a_with_orphan_maps_to_reopens_join(self) -> None:
        signals = _minimal_signals(entity_table_map={})
        facts = [_maps_to_fact("com.example", "Order", "orders")]
        report, _ = build_gap_report(
            signals, facts, covering_ok=True, covering_why=""
        )
        assert report["rates"]["R_join"]["rate"] is None
        assert report["counts"]["maps_to"] == 1
        assert report["counts"]["entity_table_map"] == 0
        assert report["design_reopen"]["join_incomplete"] is True

    def test_path_a_with_zero_maps_to_reopens_join(self) -> None:
        report, _ = build_gap_report(
            _minimal_signals(), [], covering_ok=True, covering_why=""
        )
        assert report["counts"]["maps_to"] == 0
        assert report["counts"]["entity_table_map"] == 1
        assert report["design_reopen"]["join_incomplete"] is True

    def test_healthy_dual_emit_does_not_reopen_join(self) -> None:
        report, _ = build_gap_report(
            _minimal_signals(),
            [_maps_to_fact("com.example", "Order", "orders")],
            covering_ok=True,
            covering_why="",
        )
        assert report["rates"]["R_join"]["rate"] == 1.0
        assert report["design_reopen"]["join_incomplete"] is False

class TestBaselineBandsNotVacuous:
    """Deviation: R_lin∈[0,1] and U_max=1 accepted any measurement."""

    def test_lin_and_u_bands_are_strict(self) -> None:
        data = json.loads(BASELINE.read_text(encoding="utf-8"))
        bands = data["bands"]
        assert bands["R_lin_mean_min"] > 0.0
        assert bands["R_lin_mean_max"] < 1.0
        assert bands["U_max"] < 1.0
        # Measured external-dev-corpus point must sit inside the band.
        exp = data["expected"]
        assert bands["R_lin_mean_min"] <= exp["R_lin_mean"] <= bands["R_lin_mean_max"]
        assert exp["U"] <= bands["U_max"]

class TestContestedRaisesColl:
    """Deviation: identity_rates_healthy could ignore small R_coll if only >0 checks."""

    def test_single_contested_key_moves_r_coll_off_zero(self) -> None:
        signals = _minimal_signals(
            entity_table_map={
                "User": {
                    "file": "a/User.java",
                    "table": "a_user",
                    "status": "contested",
                    "fqcn": "com.example.a.User",
                    "package": "com.example.a",
                    "candidates": [
                        {
                            "file": "a/User.java",
                            "table": "a_user",
                            "package": "com.example.a",
                            "fqcn": "com.example.a.User",
                        },
                        {
                            "file": "b/User.java",
                            "table": "b_user",
                            "package": "com.example.b",
                            "fqcn": "com.example.b.User",
                        },
                    ],
                }
            }
        )
        block = measure_r_coll(signals)
        assert block["rate"] == 1.0
        report, _ = build_gap_report(signals, [], covering_ok=True, covering_why="")
        assert report["design_reopen"]["path_a_to_symbols"] is True

class TestForgedCoveringProof:
    """Deviation: mismatched acked_subset_root must not verify."""

    def test_forged_acked_root_fails_verify(self) -> None:
        sigs = {"a.java": "1", "b.java": "2"}
        root = inventory_root(sigs)
        proof = build_covering_proof(
            file_signatures=sigs,
            scanner_version="sv",
            receipts=[
                build_receipt(
                    scanner="filesystem",
                    version_hash="v",
                    scope="all_signatures",
                    expected_subset_root=root,
                    acked_subset_root="deadbeef",
                    status="complete",
                )
            ],
        )
        ok, why = verify_covering_proof(
            proof, file_signatures=sigs, scanner_version="sv"
        )
        assert ok is False
        assert "acked_subset_root" in why
