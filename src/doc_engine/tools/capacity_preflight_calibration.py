"""L2b Stage-4 calibration against on-disk Stage-4 inputs."""

from __future__ import annotations

from doc_engine.tools.capacity_preflight_compute import (
    _stage4_pool_fields,
    _stage4_shared_pool_warning,
)
from doc_engine.tools.capacity_preflight_constants import (
    CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION,
)
from doc_engine.tools.capacity_preflight_stage4 import (
    compare_stage4_proxy_to_measured,
    estimate_stage4_shared_pool_tokens,
    measure_stage4_shared_pool_tokens,
)


def _proxy_pool_from_stage0_report(stage0_preflight_report):
    """Rebuild a pool-shaped dict from a prior Stage-0 report's flat fields."""
    return {
        "metric_kind": stage0_preflight_report.get(
            "stage4_metric_kind", "partial_proxy_pre_stage4"
        ),
        "summaries_est_tokens": stage0_preflight_report.get(
            "stage4_summaries_est_tokens", 0
        ),
        "interview_answers_est_tokens": stage0_preflight_report.get(
            "stage4_interview_answers_est_tokens", 0
        ),
        "signals_est_tokens": stage0_preflight_report.get(
            "stage4_signals_est_tokens", 0
        ),
        "shared_pool_upper_bound_est_tokens": stage0_preflight_report.get(
            "stage4_shared_pool_upper_bound_est_tokens", 0
        ),
    }


def _resolve_stage4_proxy(stage0_preflight_report, groups_data, warnings):
    """Pick proxy pool + source for measured/proxy comparison; may warn."""
    both_proxy_sources = (
        stage0_preflight_report is not None and groups_data is not None
    )
    if stage0_preflight_report is not None:
        if both_proxy_sources:
            warnings.append({
                "dimension": "stage4_proxy_comparison_source",
                "value": "stage0_preflight_report",
                "threshold": "groups_file_ignored",
                "message": (
                    "Both a Stage-0 preflight report and groups_data were supplied "
                    "for proxy comparison; using stage0_preflight_report "
                    "(groups ignored for the measured/proxy ratio)."
                ),
            })
        return _proxy_pool_from_stage0_report(stage0_preflight_report), "stage0_preflight_report"
    if groups_data is not None:
        # Compare against Stage-0 proxy recomputed from groups only (no signals)
        # so the ratio highlights summary compression vs est_tokens, not a
        # shared signals term on both sides.
        return estimate_stage4_shared_pool_tokens(groups_data, None), "groups_est_tokens_proxy"
    return None, None


def compute_stage4_calibration(
    repo_path,
    summaries_data,
    interview_answers=None,
    signals_data=None,
    groups_data=None,
    stage0_preflight_report=None,
    stage4_shared_tokens_warn_threshold=80_000,
):
    """L2b post-artifact calibration — measured Stage-4 inputs vs optional proxy.

    Requires on-disk summaries. Interview/signals optional (listed omitted if
    absent). When ``groups_data`` or a Stage-0 preflight report is supplied,
    attach a derived proxy comparison. If **both** are supplied, the Stage-0
    report wins and a warning is emitted (groups are ignored for the ratio).
    Does not change Stage-0 defaults. Not invoked by the Stage 0 pipeline step.
    """
    measured = measure_stage4_shared_pool_tokens(
        summaries_data,
        interview_answers=interview_answers,
        signals_data=signals_data,
    )
    warnings = []
    stage4_warn = _stage4_shared_pool_warning(
        measured, stage4_shared_tokens_warn_threshold,
    )
    if stage4_warn:
        warnings.append(stage4_warn)

    proxy_pool, proxy_source = _resolve_stage4_proxy(
        stage0_preflight_report, groups_data, warnings,
    )
    proxy_comparison = None
    if proxy_pool is not None:
        proxy_comparison = compare_stage4_proxy_to_measured(proxy_pool, measured)
        proxy_comparison["proxy_source"] = proxy_source

    return {
        "schema_version": CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION,
        "repo_path": (
            (groups_data or {}).get("repo_path")
            or (stage0_preflight_report or {}).get("repo_path")
            or repo_path
        ),
        "mode": "stage4_calibration",
        **_stage4_pool_fields(measured),
        "stage4_proxy_comparison": proxy_comparison,
        "warnings": warnings,
    }

