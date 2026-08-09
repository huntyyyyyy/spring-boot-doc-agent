"""Synthetic capacity-preflight report shapes for schema characterization."""

from __future__ import annotations

from doc_engine.tools import capacity_preflight

STAGE4_METRIC_KINDS = frozenset({
    "partial_proxy_pre_stage4",
    "measured_stage4_inputs",
})

_LEGACY_SHARED_ROOT_KEYS = frozenset({
    "repo_path",
    "stage4_metric_kind",
    "stage4_included_now",
    "stage4_omitted_not_estimated",
    "stage4_shared_pool_upper_bound_est_tokens",
    "stage4_summaries_est_tokens",
    "stage4_interview_answers_est_tokens",
    "stage4_interview_answers_omitted",
    "stage4_signals_est_tokens",
    "stage4_signals_omitted",
    "stage4_aggregate_input_upper_bound_est_tokens",
    "stage4_return_payloads_estimated",
    "warnings",
})


def characterization_stage0_report(*, with_schema_version: bool = False) -> dict:
    """Minimal synthetic Stage-0 report matching today's compute_preflight shape."""
    report = {
        "repo_path": "/tmp/example-repo",
        "num_groups": 2,
        "max_tokens_per_group": 120000,
        "stage_fanout": {
            "stage1_file_summarizer": 2,
            "stage2_architect_segment": 2,
            "stage2_architect_merge": 1,
            "stage3_gap_analyzer": 1,
            "stage3_software_architect_and_testing": 1,
            "stage4_doc_writer": 14,
        },
        "total_fanout": 21,
        "stage1_slice_est_tokens_max": 10,
        "stage1_slice_est_tokens_mean": 5,
        "stage1_slice_est_tokens_total": 10,
        "stage1_slice_est_tokens_per_group": {"0": 5, "1": 5},
        "stage4_metric_kind": "partial_proxy_pre_stage4",
        "stage4_included_now": [
            "group_est_tokens_proxy_for_summaries",
            "spring_signals_optional",
        ],
        "stage4_omitted_not_estimated": [
            "interview_answers",
            "architecture_merge_beyond_summary_proxy",
            "stage4_return_payloads",
        ],
        "stage4_shared_pool_upper_bound_est_tokens": 200,
        "stage4_summaries_est_tokens": 200,
        "stage4_interview_answers_est_tokens": 0,
        "stage4_interview_answers_omitted": True,
        "stage4_signals_est_tokens": 0,
        "stage4_signals_omitted": True,
        "stage4_aggregate_input_upper_bound_est_tokens": 2800,
        "stage4_return_payloads_estimated": False,
        "edge_join_stats": {},
        "warnings": [],
    }
    if with_schema_version:
        report["schema_version"] = (
            capacity_preflight.CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION
        )
    return report


def characterization_calibration_report(*, with_schema_version: bool = False) -> dict:
    """Minimal synthetic L2b calibration report matching compute_stage4_calibration."""
    report = {
        "repo_path": "/tmp/example-repo",
        "mode": "stage4_calibration",
        "stage4_metric_kind": "measured_stage4_inputs",
        "stage4_included_now": ["summaries"],
        "stage4_omitted_not_estimated": [
            "interview_answers",
            "spring_signals",
            "stage4_return_payloads",
        ],
        "stage4_shared_pool_upper_bound_est_tokens": 50,
        "stage4_summaries_est_tokens": 50,
        "stage4_interview_answers_est_tokens": 0,
        "stage4_interview_answers_omitted": True,
        "stage4_signals_est_tokens": 0,
        "stage4_signals_omitted": True,
        "stage4_aggregate_input_upper_bound_est_tokens": 700,
        "stage4_return_payloads_estimated": False,
        "stage4_proxy_comparison": None,
        "warnings": [],
    }
    if with_schema_version:
        report["schema_version"] = (
            capacity_preflight.CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION
        )
    return report
