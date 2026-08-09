"""Stage-0 capacity preflight compute + threshold warnings."""

from __future__ import annotations

from doc_engine.tools.capacity_preflight_constants import (
    CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION,
    STAGE3_ARCH_TEST_REVIEW_FANOUT,
    STAGE3_FIXED_FANOUT,
    STAGE4_FIXED_FANOUT,
)
from doc_engine.tools.capacity_preflight_groups import estimate_stage1_slice_tokens
from doc_engine.tools.capacity_preflight_stage4 import estimate_stage4_shared_pool_tokens


def _stage4_pool_fields(stage4_pool):
    """Flatten a Stage-4 pool dict into report keys (proxy or measured)."""
    return {
        "stage4_metric_kind": stage4_pool["metric_kind"],
        "stage4_included_now": stage4_pool["included_now"],
        "stage4_omitted_not_estimated": stage4_pool["omitted_not_estimated"],
        "stage4_shared_pool_upper_bound_est_tokens": (
            stage4_pool["shared_pool_upper_bound_est_tokens"]
        ),
        "stage4_summaries_est_tokens": stage4_pool["summaries_est_tokens"],
        "stage4_interview_answers_est_tokens": stage4_pool.get(
            "interview_answers_est_tokens", 0
        ),
        "stage4_interview_answers_omitted": stage4_pool.get(
            "interview_answers_omitted", True
        ),
        "stage4_signals_est_tokens": stage4_pool["signals_est_tokens"],
        "stage4_signals_omitted": stage4_pool["signals_omitted"],
        "stage4_aggregate_input_upper_bound_est_tokens": (
            stage4_pool["aggregate_input_upper_bound_est_tokens"]
        ),
        "stage4_return_payloads_estimated": stage4_pool["return_payloads_estimated"],
    }


def _stage4_shared_pool_warning(stage4_pool, threshold):
    if stage4_pool["shared_pool_upper_bound_est_tokens"] <= threshold:
        return None
    kind = stage4_pool["metric_kind"]
    interview_note = ""
    if stage4_pool.get("interview_answers_omitted"):
        interview_note = ", interview_omitted"
    elif stage4_pool.get("interview_answers_est_tokens"):
        interview_note = (
            f", interview≈{stage4_pool['interview_answers_est_tokens']}"
        )
    return {
        "dimension": "stage4_shared_pool_upper_bound_est_tokens",
        "value": stage4_pool["shared_pool_upper_bound_est_tokens"],
        "threshold": threshold,
        "message": (
            f"Stage-4 shared-pool {kind} is "
            f"~{stage4_pool['shared_pool_upper_bound_est_tokens']} "
            f"est. tokens (summaries≈{stage4_pool['summaries_est_tokens']}"
            f"{interview_note}, "
            f"signals≈{stage4_pool['signals_est_tokens']}"
            f"{', signals_omitted' if stage4_pool['signals_omitted'] else ''}), "
            f"and each of {STAGE4_FIXED_FANOUT} doc-writers receives a pool "
            f"(aggregate≈"
            f"{stage4_pool['aggregate_input_upper_bound_est_tokens']}). "
            f"Omitted (not estimated): "
            f"{', '.join(stage4_pool['omitted_not_estimated'])}. "
            f"Do not treat a quiet Stage-1 slice — or this metric — as "
            f"closed Stage-4 capacity risk."
        ),
    }


def _preflight_threshold_warnings(
    num_groups,
    total_fanout,
    slice_tokens,
    groups_data,
    max_tokens,
    group_warn_threshold,
    fanout_warn_threshold,
    slice_tokens_warn_threshold,
):
    """Build Stage-0 warning entries for group/fanout/slice thresholds."""
    warnings = []
    if num_groups > group_warn_threshold:
        warnings.append({
            "dimension": "num_groups",
            "value": num_groups,
            "threshold": group_warn_threshold,
            "message": (
                f"{num_groups} groups exceeds the group-count warning threshold "
                f"({group_warn_threshold}). Practical Task-tool concurrency and "
                f"per-turn dispatch limits are untested at this scale — consider "
                f"raising --max-tokens or reviewing before a full run."
            ),
        })
    if total_fanout > fanout_warn_threshold:
        warnings.append({
            "dimension": "total_fanout",
            "value": total_fanout,
            "threshold": fanout_warn_threshold,
            "message": (
                f"{total_fanout} total subagent dispatches across all five stages "
                f"exceeds the fan-out warning threshold ({fanout_warn_threshold}). "
                f"This pipeline has no built-in cap on fan-out today — this is a "
                f"stated, tunable guess about practical concurrency limits, not a "
                f"validated ceiling."
            ),
        })
    if slice_tokens["max"] > slice_tokens_warn_threshold:
        warnings.append({
            "dimension": "stage1_slice_est_tokens_max",
            "value": slice_tokens["max"],
            "threshold": slice_tokens_warn_threshold,
            "message": (
                f"The largest single Stage-1 edge slice is ~{slice_tokens['max']} est. "
                f"tokens, on top of that group's own files (budgeted at "
                f"{groups_data.get('max_tokens_per_group', max_tokens)}). Across all "
                f"{num_groups} groups the slices total ~{slice_tokens['total']}. A "
                f"context limit is breached by one dispatch, not by the sum, so the "
                f"max is the number that matters — consider lowering --max-tokens to "
                f"cut smaller groups, which shrinks each slice."
            ),
        })
    return warnings


def _stage_fanout_for_groups(num_groups):
    """Per-stage subagent fan-out dict for a given group count."""
    return {
        "stage1_file_summarizer": num_groups,
        "stage2_architect_segment": num_groups,
        "stage2_architect_merge": 1,
        "stage3_gap_analyzer": STAGE3_FIXED_FANOUT,
        "stage3_software_architect_and_testing": STAGE3_ARCH_TEST_REVIEW_FANOUT,
        "stage4_doc_writer": STAGE4_FIXED_FANOUT,
    }


def compute_preflight(repo_path, max_tokens=120000, overlap=0.10,
                       groups_data=None, edges=None, signals_data=None,
                       group_warn_threshold=15, fanout_warn_threshold=40,
                       slice_tokens_warn_threshold=30_000,
                       stage4_shared_tokens_warn_threshold=80_000):
    """Pure function over already-loaded groups_data/edges (or repo_path to
    derive them) — kept separate from CLI/file-IO so it's directly unit
    testable against synthetic data without touching disk.

    The two derivation branches below are order-dependent, unlike the pair
    this replaced: the edge join consumes the partition.

    Derivation helpers are resolved via the ``capacity_preflight`` façade so
    characterization tests can monkeypatch the public module surface.
    """
    from doc_engine.tools import capacity_preflight as cap

    if groups_data is None:
        groups_data = cap._load_or_build_groups(
            repo_path, max_tokens, overlap, None
        )
    if edges is None:
        edges = cap._load_or_build_edges(repo_path, None, groups_data, None)

    num_groups = groups_data["num_groups"]
    stage_fanout = _stage_fanout_for_groups(num_groups)
    total_fanout = sum(stage_fanout.values())

    slice_tokens = estimate_stage1_slice_tokens(edges)
    stage4_pool = estimate_stage4_shared_pool_tokens(groups_data, signals_data)
    warnings = _preflight_threshold_warnings(
        num_groups,
        total_fanout,
        slice_tokens,
        groups_data,
        max_tokens,
        group_warn_threshold,
        fanout_warn_threshold,
        slice_tokens_warn_threshold,
    )
    stage4_warn = _stage4_shared_pool_warning(
        stage4_pool, stage4_shared_tokens_warn_threshold,
    )
    if stage4_warn:
        warnings.append(stage4_warn)

    return {
        "schema_version": CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION,
        "repo_path": groups_data.get("repo_path", repo_path),
        "num_groups": num_groups,
        "max_tokens_per_group": groups_data.get("max_tokens_per_group", max_tokens),
        "stage_fanout": stage_fanout,
        "total_fanout": total_fanout,
        "stage1_slice_est_tokens_max": slice_tokens["max"],
        "stage1_slice_est_tokens_mean": slice_tokens["mean"],
        "stage1_slice_est_tokens_total": slice_tokens["total"],
        "stage1_slice_est_tokens_per_group": slice_tokens["per_group"],
        **_stage4_pool_fields(stage4_pool),
        # Reported straight from the join rather than re-derived here, so the
        # broadcast-vs-shipped comparison has exactly one implementation.
        "edge_join_stats": edges.get("stats", {}),
        "warnings": warnings,
    }

