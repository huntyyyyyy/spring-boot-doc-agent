"""Registry hooks for R_sym / R_coll / R_join / R_lin / R_code_dep."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping

from .code_dep import measure_r_code_dep
from .common import ScoringEnv
from .join import measure_r_join
from .lineage import _dominant_failure_stratum, measure_r_lin
from .registry_types import MeasureContext, project_rate_block
from .symbol_collision import measure_r_coll, measure_r_sym


def run_sym(ctx: MeasureContext) -> Dict[str, Any]:
    return measure_r_sym(ctx.facts)


def run_coll(ctx: MeasureContext) -> Dict[str, Any]:
    return measure_r_coll(ctx.signals)


def uncertainty_coll(
    block: Mapping[str, Any], _ctx: MeasureContext
) -> Mapping[str, Any]:
    return {"r_coll": block["rate"]}


def reopen_coll(
    block: Mapping[str, Any], _ctx: MeasureContext
) -> Mapping[str, Any]:
    return {"path_a_to_symbols": (block["rate"] or 0) > 0}


def run_join(ctx: MeasureContext) -> Dict[str, Any]:
    return measure_r_join(ctx.signals, ctx.facts)


def uncertainty_join(
    block: Mapping[str, Any], _ctx: MeasureContext
) -> Mapping[str, Any]:
    return {"r_join": block["rate"]}


def reopen_join(
    block: Mapping[str, Any], _ctx: MeasureContext
) -> Mapping[str, Any]:
    return {"join_incomplete": block["rate"] is None or block["rate"] < 1.0}


def run_lin(ctx: MeasureContext) -> Dict[str, Any]:
    return {
        "callable": measure_r_lin(ctx.signals, scoring_env=ScoringEnv.CALLABLE),
        "pooled": measure_r_lin(ctx.signals, scoring_env=ScoringEnv.POOLED),
    }


def _lineage_core_fields(lineage_block: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "mean_rate": lineage_block["mean_rate"],
        "numerator": lineage_block["numerator"],
        "denominator": lineage_block["denominator"],
        "callable_denominator": lineage_block["callable_denominator"],
        "strata": lineage_block["strata"],
    }


def project_lin(
    bundle: Mapping[str, Any], _ctx: MeasureContext
) -> Dict[str, Any]:
    callable_lineage = bundle["callable"]
    pooled_lineage = bundle["pooled"]
    return {
        "scoring_env": ScoringEnv.CALLABLE,
        **_lineage_core_fields(callable_lineage),
        "failure_taxonomy": callable_lineage["failure_taxonomy"],
        "pooled_contrast": {
            "scoring_env": ScoringEnv.POOLED,
            **_lineage_core_fields(pooled_lineage),
        },
    }


def harvest_lin(
    bundle: Mapping[str, Any], _ctx: MeasureContext
) -> List[Dict[str, Any]]:
    # Failures live on the normative callable stratum only.
    return list((bundle.get("callable") or {}).get("failures") or [])


def uncertainty_lin(
    bundle: Mapping[str, Any], _ctx: MeasureContext
) -> Mapping[str, Any]:
    return {"r_lin_mean": bundle["callable"]["mean_rate"]}


def reopen_lin(
    bundle: Mapping[str, Any], _ctx: MeasureContext
) -> Mapping[str, Any]:
    return {
        "lineage_dominant_stratum": _dominant_failure_stratum(bundle["callable"]),
    }


def run_code_dep(ctx: MeasureContext) -> Dict[str, Any]:
    return measure_r_code_dep(ctx.signals)


def project_code_dep(
    block: Mapping[str, Any], ctx: MeasureContext
) -> Dict[str, Any]:
    projected = project_rate_block(block, ctx)
    projected["per_family"] = block["per_family"]
    return projected


def uncertainty_code_dep(
    block: Mapping[str, Any], _ctx: MeasureContext
) -> Mapping[str, Any]:
    return {"r_code_dep": block["rate"]}
