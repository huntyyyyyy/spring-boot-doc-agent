"""Stage4 partial-proxy suite."""

from __future__ import annotations

import os
import sys
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.tools import (
    build_cross_group_edges,
    capacity_preflight,
    partition_repo,
    spring_signal_scan,
)

import pytest

pytestmark = pytest.mark.domain_pipeline

SCRIPT_DIR = SCRIPTS_DIR
from tests.support.capacity_preflight.fixtures import (
    _edges_data,
    _groups_data,
    _imp,
    _pkg,
)

class Stage4PartialProxyTest(unittest.TestCase):
    """L2 honesty: Stage-0 proxy mirrors pipeline SoR, does not claim full bound."""

    def test_stage4_fanout_tracks_valid_doc_files(self):
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=_groups_data(2), edges=_edges_data(2),
        )
        self.assertEqual(
            report["stage_fanout"]["stage4_doc_writer"],
            len(capacity_preflight.VALID_DOC_FILES),
        )
        self.assertEqual(
            capacity_preflight.STAGE4_FIXED_FANOUT,
            len(capacity_preflight.VALID_DOC_FILES),
        )

    def test_stage0_invocation_mirror_omits_interview(self):
        """Mirror stages.py capacity_preflight argv: groups + signals, no interview."""
        groups = _groups_data(3)
        for g in groups["groups"]:
            g["est_tokens"] = 1_000
        report = capacity_preflight.compute_preflight(
            "/fake/repo",
            groups_data=groups,
            edges=_edges_data(3),
            signals_data={"evidence": {"references": []}},
            group_warn_threshold=1000,
            fanout_warn_threshold=1000,
            stage4_shared_tokens_warn_threshold=10_000_000,
        )
        self.assertEqual(report["stage4_metric_kind"], "partial_proxy_pre_stage4")
        self.assertIn("interview_answers", report["stage4_omitted_not_estimated"])
        self.assertIn(
            "architecture_merge_beyond_summary_proxy",
            report["stage4_omitted_not_estimated"],
        )
        self.assertIn("stage4_return_payloads", report["stage4_omitted_not_estimated"])
        self.assertFalse(report["stage4_return_payloads_estimated"])
        self.assertFalse(report["stage4_signals_omitted"])
        self.assertNotEqual(report["stage4_metric_kind"], "upper_bound")
        # Numeric fields may still say upper_bound in the name; kind must not.
        self.assertIn("partial_proxy", report["stage4_metric_kind"])

    def test_signals_omitted_flag_when_no_signals(self):
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=_groups_data(2), edges=_edges_data(2),
            signals_data=None,
            group_warn_threshold=1000, fanout_warn_threshold=1000,
            stage4_shared_tokens_warn_threshold=10_000_000,
        )
        self.assertTrue(report["stage4_signals_omitted"])
        self.assertEqual(report["stage4_signals_est_tokens"], 0)

    def test_signals_increase_stage4_proxy(self):
        groups = _groups_data(2)
        for g in groups["groups"]:
            g["est_tokens"] = 100
        bare = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=groups, edges=_edges_data(2),
            group_warn_threshold=1000, fanout_warn_threshold=1000,
            stage4_shared_tokens_warn_threshold=10_000_000,
        )
        with_signals = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=groups, edges=_edges_data(2),
            signals_data={"evidence": {"pad": "y" * 4000}},
            group_warn_threshold=1000, fanout_warn_threshold=1000,
            stage4_shared_tokens_warn_threshold=10_000_000,
        )
        self.assertGreater(
            with_signals["stage4_shared_pool_upper_bound_est_tokens"],
            bare["stage4_shared_pool_upper_bound_est_tokens"],
        )
        self.assertGreater(with_signals["stage4_signals_est_tokens"], 0)

    def test_stage4_warning_fires_when_slice_is_quiet(self):
        """Polarity: Stage-1 slice under threshold must not hide Stage-4 proxy."""
        groups = _groups_data(5)
        for g in groups["groups"]:
            g["est_tokens"] = 25_000  # shared proxy = 125_000 > 80_000
        report = capacity_preflight.compute_preflight(
            "/fake/repo",
            groups_data=groups,
            edges=_edges_data(5, arcs_per_group=0),
            group_warn_threshold=1000,
            fanout_warn_threshold=1000,
            slice_tokens_warn_threshold=30_000,
            stage4_shared_tokens_warn_threshold=80_000,
        )
        dims = {w["dimension"] for w in report["warnings"]}
        self.assertNotIn("stage1_slice_est_tokens_max", dims)
        self.assertIn("stage4_shared_pool_upper_bound_est_tokens", dims)
        stage4_warn = next(
            w for w in report["warnings"]
            if w["dimension"] == "stage4_shared_pool_upper_bound_est_tokens"
        )
        self.assertIn("partial_proxy_pre_stage4", stage4_warn["message"])

    def test_stage4_warning_absent_under_threshold(self):
        groups = _groups_data(2)
        for g in groups["groups"]:
            g["est_tokens"] = 100
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=groups, edges=_edges_data(2),
            group_warn_threshold=1000, fanout_warn_threshold=1000,
            stage4_shared_tokens_warn_threshold=80_000,
        )
        dims = {w["dimension"] for w in report["warnings"]}
        self.assertNotIn("stage4_shared_pool_upper_bound_est_tokens", dims)

    def test_omitted_list_matches_pipeline_doc_writer_gap(self):
        """Omitted set must include interview — a real doc_writer input_artifact."""
        from doc_engine.pipeline.stages import build_stage_specs, StageKind
        from doc_engine.pipeline.artifacts import ARTIFACT_FILENAMES

        doc_writer = next(
            s for s in build_stage_specs()
            if s.name == "doc_writer" and s.kind == StageKind.GENERATIVE
        )
        self.assertIn(ARTIFACT_FILENAMES["interview_answers"], doc_writer.input_artifacts)
        self.assertIn(
            "interview_answers",
            capacity_preflight.STAGE4_PROXY_OMITTED,
        )
