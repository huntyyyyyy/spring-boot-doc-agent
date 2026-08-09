"""Stage-4 shared-pool estimate, measure, and proxy-vs-measured compare."""

from __future__ import annotations

import json

from doc_engine.tools import partition_repo
from doc_engine.tools.capacity_preflight_constants import (
    STAGE4_FIXED_FANOUT,
    STAGE4_MEASURED_ALWAYS_OMITTED,
    STAGE4_PROXY_INCLUDED,
    STAGE4_PROXY_OMITTED,
)


def _json_est_tokens(obj):
    """Same chars/N heuristic as Stage-1 slices / Stage-0 signals."""
    if obj is None:
        return 0
    return max(1, len(json.dumps(obj)) // partition_repo.CHARS_PER_TOKEN_DEFAULT)


def estimate_stage4_shared_pool_tokens(groups_data, signals_data=None):
    """Partial Stage-0 *proxy* for Stage-4 shared-pool input — not a full bound.

    SoR for dispatch count is ``VALID_DOC_FILES``. Stage-4's real inputs are
    summaries + interview_answers + spring_signals (pipeline stages.py). At
    Stage 0 those summaries/interview do not exist yet, so we proxy merged
    summary size as the sum of per-group ``est_tokens`` (overlap can inflate)
    and optionally add signals chars/N.

    ``metric_kind`` is ``partial_proxy_pre_stage4``. Numeric fields keep the
    ``*_upper_bound_*`` names for the warn threshold only — they are **not**
    an upper bound on full Stage-4 input while omissions are non-empty.
    """
    groups = groups_data.get("groups") or []
    summaries_est = sum(int(g.get("est_tokens") or 0) for g in groups)
    signals_omitted = signals_data is None
    signals_est = _json_est_tokens(signals_data) if signals_data is not None else 0
    shared = summaries_est + signals_est
    return {
        "metric_kind": "partial_proxy_pre_stage4",
        "included_now": list(STAGE4_PROXY_INCLUDED),
        "omitted_not_estimated": list(STAGE4_PROXY_OMITTED),
        "summaries_est_tokens": summaries_est,
        "interview_answers_est_tokens": 0,
        "interview_answers_omitted": True,
        "signals_est_tokens": signals_est,
        "signals_omitted": signals_omitted,
        "shared_pool_upper_bound_est_tokens": shared,
        "aggregate_input_upper_bound_est_tokens": shared * STAGE4_FIXED_FANOUT,
        "return_payloads_estimated": False,
        "note": (
            "partial_proxy_pre_stage4: group est_tokens proxy for future "
            "summaries (overlap can inflate) + optional signals; omitted "
            "interview_answers / architecture_merge_beyond_summary_proxy / "
            "stage4_return_payloads; not a full Stage-4 upper_bound"
        ),
    }


def _optional_json_est(obj):
    """Return ``(est_tokens, omitted)`` for an optional on-disk JSON blob."""
    if obj is None:
        return 0, True
    return _json_est_tokens(obj), False


def _measured_included_omitted(interview_omitted, signals_omitted):
    """Build included/omitted lists for measured Stage-4 pool accounting."""
    included = ["summaries"]
    omitted = []
    if interview_omitted:
        omitted.append("interview_answers")
    else:
        included.append("interview_answers")
    if signals_omitted:
        omitted.append("spring_signals")
    else:
        included.append("spring_signals")
    omitted.extend(STAGE4_MEASURED_ALWAYS_OMITTED)
    return included, omitted


def _measured_stage4_note(interview_omitted, signals_omitted):
    """Honesty note for measured_stage4_inputs metric_kind."""
    return (
        "measured_stage4_inputs: chars/N of on-disk summaries"
        f"{'' if interview_omitted else ' + interview_answers'}"
        f"{'' if signals_omitted else ' + spring_signals'}; "
        "omitted stage4_return_payloads"
        f"{' / interview_answers' if interview_omitted else ''}"
        f"{' / spring_signals' if signals_omitted else ''}; "
        "not a claim that Stage-4 capacity risk is closed"
    )


def measure_stage4_shared_pool_tokens(
    summaries_data, interview_answers=None, signals_data=None,
):
    """L2b: measure Stage-4 shared-pool input from on-disk artifacts.

    SoR = summaries.json (+ optional interview_answers.json / spring_signals.json).
    ``metric_kind`` is ``measured_stage4_inputs``. Return payloads are never
    estimated. Missing interview/signals are listed in omissions — do not invent
    sizes. Numeric ``*_upper_bound_*`` names remain warn-threshold fields only.
    """
    if summaries_data is None:
        raise ValueError("summaries_data is required for measured_stage4_inputs")
    summaries_est = _json_est_tokens(summaries_data)
    interview_est, interview_omitted = _optional_json_est(interview_answers)
    signals_est, signals_omitted = _optional_json_est(signals_data)
    shared = summaries_est + interview_est + signals_est
    included, omitted = _measured_included_omitted(interview_omitted, signals_omitted)

    return {
        "metric_kind": "measured_stage4_inputs",
        "included_now": included,
        "omitted_not_estimated": omitted,
        "summaries_est_tokens": summaries_est,
        "interview_answers_est_tokens": interview_est,
        "interview_answers_omitted": interview_omitted,
        "signals_est_tokens": signals_est,
        "signals_omitted": signals_omitted,
        "shared_pool_upper_bound_est_tokens": shared,
        "aggregate_input_upper_bound_est_tokens": shared * STAGE4_FIXED_FANOUT,
        "return_payloads_estimated": False,
        "note": _measured_stage4_note(interview_omitted, signals_omitted),
    }


def compare_stage4_proxy_to_measured(proxy_pool, measured_pool):
    """Derived view: Stage-0 proxy vs measured on-disk inputs (not a second SoR)."""
    proxy_shared = int(proxy_pool.get("shared_pool_upper_bound_est_tokens") or 0)
    measured_shared = int(measured_pool.get("shared_pool_upper_bound_est_tokens") or 0)
    ratio = (
        (measured_shared / proxy_shared) if proxy_shared > 0 else None
    )
    return {
        "proxy_metric_kind": proxy_pool.get("metric_kind"),
        "measured_metric_kind": measured_pool.get("metric_kind"),
        "stage0_proxy_shared_est_tokens": proxy_shared,
        "measured_shared_est_tokens": measured_shared,
        "measured_over_proxy_ratio": ratio,
        "proxy_summaries_est_tokens": proxy_pool.get("summaries_est_tokens"),
        "measured_summaries_est_tokens": measured_pool.get("summaries_est_tokens"),
        "measured_interview_answers_est_tokens": measured_pool.get(
            "interview_answers_est_tokens"
        ),
        "note": (
            "derived comparison only; measured SoR is on-disk Stage-4 inputs; "
            "proxy SoR is group est_tokens + optional signals at Stage 0"
        ),
    }

