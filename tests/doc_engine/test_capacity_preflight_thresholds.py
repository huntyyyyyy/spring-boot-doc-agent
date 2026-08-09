"""Fanout arithmetic and threshold warning suites."""

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

class FanoutArithmeticTest(unittest.TestCase):
    def test_total_fanout_formula(self):
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=_groups_data(3), edges=_edges_data(3),
        )
        self.assertEqual(report["stage_fanout"]["stage1_file_summarizer"], 3)
        self.assertEqual(report["stage_fanout"]["stage2_architect_segment"], 3)
        self.assertEqual(report["stage_fanout"]["stage2_architect_merge"], 1)
        self.assertEqual(report["stage_fanout"]["stage3_gap_analyzer"], 1)
        self.assertEqual(report["stage_fanout"]["stage3_software_architect_and_testing"], 1)
        self.assertEqual(report["stage_fanout"]["stage4_doc_writer"], 14)
        # 2*num_groups + 1 (merge) + 1 (gap-analyzer) + 1 (software-architect-
        # and-testing) + 14 (doc-writer) = 2*3+17 = 23
        self.assertEqual(report["total_fanout"], 23)

    def test_single_group_minimum_fanout(self):
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=_groups_data(1), edges=_edges_data(1),
        )
        self.assertEqual(report["total_fanout"], 19)

class ThresholdWarningTest(unittest.TestCase):
    def test_no_warnings_under_all_thresholds(self):
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=_groups_data(2), edges=_edges_data(2),
            group_warn_threshold=15, fanout_warn_threshold=40,
            slice_tokens_warn_threshold=30_000,
        )
        self.assertEqual(report["warnings"], [])

    def test_group_count_warning_fires(self):
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=_groups_data(20), edges=_edges_data(20),
            group_warn_threshold=15,
        )
        dims = {w["dimension"] for w in report["warnings"]}
        self.assertIn("num_groups", dims)

    def test_fanout_warning_fires(self):
        # 20 groups -> total_fanout = 56, comfortably over a 40 threshold.
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=_groups_data(20), edges=_edges_data(20),
            group_warn_threshold=1000,  # suppress the group-count warning so only fanout is under test
            fanout_warn_threshold=40,
        )
        dims = {w["dimension"] for w in report["warnings"]}
        self.assertIn("total_fanout", dims)
        self.assertNotIn("num_groups", dims)

    def test_stage1_slice_warning_fires(self):
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=_groups_data(50),
            edges=_edges_data(50, arcs_per_group=10, arc_width=1000),
            group_warn_threshold=1000, fanout_warn_threshold=1000,
            slice_tokens_warn_threshold=1000,
        )
        dims = {w["dimension"] for w in report["warnings"]}
        self.assertIn("stage1_slice_est_tokens_max", dims)

    def test_warning_keys_on_the_max_not_the_sum(self):
        # The threshold deliberately guards the largest single dispatch, not
        # the whole-run total: a context window is breached by one dispatch.
        # Many small slices whose sum is large must NOT warn.
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=_groups_data(50),
            edges=_edges_data(50, arcs_per_group=1, arc_width=100),
            group_warn_threshold=1000, fanout_warn_threshold=1000,
            slice_tokens_warn_threshold=1000,
        )
        self.assertGreater(report["stage1_slice_est_tokens_total"], 1000)
        self.assertLess(report["stage1_slice_est_tokens_max"], 1000)
        self.assertEqual(report["warnings"], [])

    def test_splitting_the_same_repo_into_more_groups_does_not_multiply_cost(self):
        """The inverse of what this file used to assert.

        The deleted `test_references_bucket_tokens_scale_with_group_count`
        pinned the broadcast model as an invariant: per-dispatch payload
        constant, total strictly rising with group count — i.e. cost = |R| x g.
        Commit abd3ade replaced the broadcast with a partitioned join, so that
        relationship no longer holds, and the test kept passing anyway because
        it exercised capacity_preflight's own arithmetic rather than the
        pipeline's behavior. It was defending code that had already been
        removed.

        What actually holds now: shipped volume is bounded by the *cut*, not
        by the reference count times the group count. Same files, same
        imports, more groups -> more arcs cut, but each group ships only its
        own boundary, and the total stays far under the broadcast equivalent.
        """
        refs = [_pkg(f"p{i}/C{i}.java", f"p{i}") for i in range(8)]
        refs += [_imp(f"p{i}/C{i}.java", f"p{i + 1}.C{i + 1}") for i in range(7)]
        files = [f"p{i}/C{i}.java" for i in range(8)]

        def report_for(group_sizes):
            groups = []
            start = 0
            for n in group_sizes:
                groups.append({"id": len(groups), "files": files[start:start + n], "est_tokens": 100})
                start += n
            groups_data = {"repo_path": "/fake/repo", "max_tokens_per_group": 120000,
                           "num_groups": len(groups), "groups": groups}
            edges = build_cross_group_edges.build_report(
                groups_data, {"evidence": {"references": refs}})
            return capacity_preflight.compute_preflight(
                "/fake/repo", groups_data=groups_data, edges=edges,
                group_warn_threshold=1000, fanout_warn_threshold=1000)

        two = report_for([4, 4])
        eight = report_for([1] * 8)

        # More groups cuts more arcs, so total shipped does rise ...
        self.assertGreaterEqual(eight["stage1_slice_est_tokens_total"],
                                two["stage1_slice_est_tokens_total"])
        # ... but the per-dispatch payload does NOT stay constant the way a
        # broadcast's would, which is the actual behavioral difference.
        self.assertLess(eight["stage1_slice_est_tokens_max"],
                        eight["stage1_slice_est_tokens_total"])
        # And the join's own accounting must agree it beat broadcasting.
        stats = eight["edge_join_stats"]
        self.assertLess(stats["rows_shipped"], stats["broadcast_rows_avoided"])
