"""Stage4 measured-calibration suite."""

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

class Stage4MeasuredCalibrationTest(unittest.TestCase):
    """L2b: on-disk Stage-4 inputs; returns still unestimated; default 80k unchanged."""

    def test_measured_includes_interview_and_flags_returns(self):
        summaries = [{"file": "a.java", "summary": "x" * 400}]
        interview = {"q1": "answer " * 50}
        signals = {"evidence": {"references": [{"pad": "z" * 200}]}}
        measured = capacity_preflight.measure_stage4_shared_pool_tokens(
            summaries, interview_answers=interview, signals_data=signals,
        )
        self.assertEqual(measured["metric_kind"], "measured_stage4_inputs")
        self.assertIn("summaries", measured["included_now"])
        self.assertIn("interview_answers", measured["included_now"])
        self.assertIn("spring_signals", measured["included_now"])
        self.assertFalse(measured["interview_answers_omitted"])
        self.assertFalse(measured["signals_omitted"])
        self.assertIn("stage4_return_payloads", measured["omitted_not_estimated"])
        self.assertNotIn("interview_answers", measured["omitted_not_estimated"])
        self.assertFalse(measured["return_payloads_estimated"])
        self.assertGreater(measured["interview_answers_est_tokens"], 0)
        self.assertGreater(measured["shared_pool_upper_bound_est_tokens"],
                           measured["summaries_est_tokens"])

    def test_measured_omits_interview_when_absent(self):
        measured = capacity_preflight.measure_stage4_shared_pool_tokens(
            [{"file": "a.java", "summary": "short"}],
        )
        self.assertTrue(measured["interview_answers_omitted"])
        self.assertEqual(measured["interview_answers_est_tokens"], 0)
        self.assertIn("interview_answers", measured["omitted_not_estimated"])
        self.assertIn("stage4_return_payloads", measured["omitted_not_estimated"])
        self.assertTrue(measured["signals_omitted"])

    def test_calibration_warns_on_measured_pool(self):
        # Pad enough that chars/N exceeds a low threshold.
        summaries = [{"pad": "y" * 20_000}]
        report = capacity_preflight.compute_stage4_calibration(
            "/fake/repo",
            summaries_data=summaries,
            interview_answers={"a": "b" * 1000},
            signals_data={"evidence": {}},
            stage4_shared_tokens_warn_threshold=100,
        )
        self.assertEqual(report["mode"], "stage4_calibration")
        self.assertEqual(report["stage4_metric_kind"], "measured_stage4_inputs")
        dims = {w["dimension"] for w in report["warnings"]}
        self.assertIn("stage4_shared_pool_upper_bound_est_tokens", dims)
        self.assertIn("measured_stage4_inputs", report["warnings"][0]["message"])
        self.assertFalse(report["stage4_return_payloads_estimated"])

    def test_proxy_comparison_from_groups(self):
        groups = _groups_data(2)
        for g in groups["groups"]:
            g["est_tokens"] = 5_000
        summaries = [{"pad": "s" * 400}]
        report = capacity_preflight.compute_stage4_calibration(
            "/fake/repo",
            summaries_data=summaries,
            interview_answers={"pad": "i" * 400},
            signals_data={"evidence": {"pad": "z" * 2000}},
            groups_data=groups,
            stage4_shared_tokens_warn_threshold=10_000_000,
        )
        cmp_ = report["stage4_proxy_comparison"]
        self.assertIsNotNone(cmp_)
        self.assertEqual(cmp_["proxy_metric_kind"], "partial_proxy_pre_stage4")
        self.assertEqual(cmp_["measured_metric_kind"], "measured_stage4_inputs")
        self.assertEqual(cmp_["proxy_source"], "groups_est_tokens_proxy")
        # Groups-path proxy excludes signals so the ratio is about summaries.
        self.assertEqual(cmp_["stage0_proxy_shared_est_tokens"], 10_000)
        self.assertGreater(cmp_["measured_shared_est_tokens"], 0)
        self.assertIsNotNone(cmp_["measured_over_proxy_ratio"])
        self.assertNotIn(
            "stage4_proxy_comparison_source",
            {w["dimension"] for w in report["warnings"]},
        )

    def test_proxy_comparison_from_stage0_report(self):
        stage0 = {
            "stage4_metric_kind": "partial_proxy_pre_stage4",
            "stage4_summaries_est_tokens": 1000,
            "stage4_signals_est_tokens": 100,
            "stage4_shared_pool_upper_bound_est_tokens": 1100,
        }
        report = capacity_preflight.compute_stage4_calibration(
            "/fake/repo",
            summaries_data=[{"x": "y" * 800}],
            stage0_preflight_report=stage0,
            stage4_shared_tokens_warn_threshold=10_000_000,
        )
        cmp_ = report["stage4_proxy_comparison"]
        self.assertEqual(cmp_["stage0_proxy_shared_est_tokens"], 1100)
        self.assertEqual(cmp_["measured_metric_kind"], "measured_stage4_inputs")
        self.assertEqual(cmp_["proxy_source"], "stage0_preflight_report")

    def test_both_proxy_sources_prefers_stage0_report_and_warns(self):
        groups = _groups_data(2)
        for g in groups["groups"]:
            g["est_tokens"] = 50_000  # would dominate if wrongly chosen
        stage0 = {
            "stage4_metric_kind": "partial_proxy_pre_stage4",
            "stage4_summaries_est_tokens": 1000,
            "stage4_signals_est_tokens": 0,
            "stage4_shared_pool_upper_bound_est_tokens": 1000,
        }
        report = capacity_preflight.compute_stage4_calibration(
            "/fake/repo",
            summaries_data=[{"x": "y" * 100}],
            groups_data=groups,
            stage0_preflight_report=stage0,
            stage4_shared_tokens_warn_threshold=10_000_000,
        )
        cmp_ = report["stage4_proxy_comparison"]
        self.assertEqual(cmp_["proxy_source"], "stage0_preflight_report")
        self.assertEqual(cmp_["stage0_proxy_shared_est_tokens"], 1000)
        dims = {w["dimension"] for w in report["warnings"]}
        self.assertIn("stage4_proxy_comparison_source", dims)

    def test_default_stage4_threshold_unchanged(self):
        """L2b must not silently recalibrate the Stage-0 / L2b default (80k)."""
        import inspect

        for fn in (
            capacity_preflight.compute_preflight,
            capacity_preflight.compute_stage4_calibration,
        ):
            default = inspect.signature(fn).parameters[
                "stage4_shared_tokens_warn_threshold"
            ].default
            self.assertEqual(default, 80_000, msg=fn.__name__)

        groups = _groups_data(2)
        for g in groups["groups"]:
            g["est_tokens"] = 100
        report = capacity_preflight.compute_preflight(
            "/fake/repo", groups_data=groups, edges=_edges_data(2),
            group_warn_threshold=1000, fanout_warn_threshold=1000,
        )
        self.assertEqual(report["stage4_metric_kind"], "partial_proxy_pre_stage4")
        self.assertNotIn(
            "stage4_shared_pool_upper_bound_est_tokens",
            {w["dimension"] for w in report["warnings"]},
        )
