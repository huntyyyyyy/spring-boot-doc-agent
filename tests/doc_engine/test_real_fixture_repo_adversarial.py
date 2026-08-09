"""Cohesive suite from tests/doc_engine/test_real_fixture_adversarial.py: TestRealRepoAdversarial, TestRealWorldFixtureMustRequireCovering."""

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
    _minimal_signals,
    _real_artifacts_available,
    real_artifacts_bundle,
)

class TestRealRepoAdversarial:
    """Opt-in attacks against a local mid-size Spring dump + checkout."""

    def test_artifact_lane_without_covering_must_not_claim_verified(
        self, real_artifacts_bundle: tuple[dict, list, Path]
    ) -> None:
        signals, facts, root = real_artifacts_bundle
        if (root / "covering_proof.json").is_file():
            pytest.skip("covering present — vacuous-verified attack N/A")
        report, _ = build_gap_report(
            signals, facts, covering_ok=True, covering_why=""
        )
        # Product honesty: even if a caller forces covering_ok, no proof ⇒ not verified.
        assert report["s1_covering"]["verified"] is False

    def test_empty_entity_map_reopens_on_real_facts(
        self, real_artifacts_bundle: tuple[dict, list, Path]
    ) -> None:
        signals, facts, _root = real_artifacts_bundle
        broken = dict(signals)
        broken["entity_table_map"] = {}
        report, _ = build_gap_report(
            broken, facts, covering_ok=True, covering_why=""
        )
        assert report["counts"]["maps_to"] > 0
        assert report["design_reopen"]["join_incomplete"] is True

    def test_mutated_signature_marks_file_changed(
        self, real_artifacts_bundle: tuple[dict, list, Path]
    ) -> None:
        signals, _facts, _root = real_artifacts_bundle
        repo = real_repo_path()
        if repo is None or not repo.is_dir():
            pytest.skip("DOC_ENGINE_REAL_REPO unset")
        mutated = json.loads(json.dumps(signals))
        sigs = dict(mutated.get("file_signatures") or {})
        java = [k for k in sigs if k.endswith(".java")]
        if not java:
            pytest.skip("no java signatures")
        target = java[0]
        sigs[target] = "adversarial-deadbeef"
        mutated["file_signatures"] = sigs
        report = spring_drift_check.check_drift(str(repo), mutated)
        assert target in report["file_summary"]["changed"]

    def test_wrong_repo_tree_is_not_identity_drift(
        self, real_artifacts_bundle: tuple[dict, list, Path]
    ) -> None:
        signals, _facts, _root = real_artifacts_bundle
        # Point drift at *this* plugin repo — almost every cited path should vanish.
        wrong = REPO_ROOT
        report = spring_drift_check.check_drift(str(wrong), signals)
        deleted = report["file_summary"]["deleted"]
        assert len(deleted) > 100, (
            f"wrong-tree attack expected mass deletions, got {len(deleted)}"
        )
        # Must not look like a healthy identity drift (status_counts ⊆ {unchanged}).
        assert set(report["status_counts"]) - {"unchanged"}

class TestRealWorldFixtureMustRequireCovering:
    """Deviation: real-world AET fixture forced covering_ok=True with no proof."""

    def test_ocs_report_fixture_refuses_missing_covering(self, tmp_path: Path) -> None:
        """Simulate artifact dir without covering — fixture helper must skip/fail closed."""
        from tests.doc_engine import test_gap_probe_ocs_real_world as mod

        art = tmp_path / "arts"
        art.mkdir()
        (art / "spring_signals.json").write_text(
            json.dumps(_minimal_signals()), encoding="utf-8"
        )
        (art / "facts.jsonl").write_text("{}\n", encoding="utf-8")
        with mock.patch.dict(
            os.environ,
            {"DOC_ENGINE_REAL_ARTIFACTS_DIR": str(art)},
            clear=False,
        ):
            # Re-import resolution path: call the fixture logic indirectly.
            root = mod._resolve_artifacts_dir()
            assert root == art
            covering = art / "covering_proof.json"
            assert not covering.is_file()
            # The module's ocs_report path must not silently covering_ok=True forever:
            # after the fix, callers should use run_gap_probe / require covering.
            # Enforce the contract the real-world module documents.
            assert hasattr(mod, "REQUIRE_COVERING_PROOF")
            assert mod.REQUIRE_COVERING_PROOF is True
