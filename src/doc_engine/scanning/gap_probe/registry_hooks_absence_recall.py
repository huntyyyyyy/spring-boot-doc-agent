"""Registry hooks for R_absence and R_recall."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Sequence

from .absence_recall import (
    _planted_recall_failures,
    measure_r_absence,
    measure_r_recall,
)
from .registry_types import MeasureContext, RecallClaim


def run_absence(ctx: MeasureContext) -> Dict[str, Any]:
    return measure_r_absence(ctx.facts, callable_trials=ctx.callable_trials)


def project_absence(
    block: Mapping[str, Any], ctx: MeasureContext
) -> Dict[str, Any]:
    return {
        "numerator": block["numerator"],
        "denominator": block["denominator"],
        "callable_denominator": block["callable_denominator"],
        "rate": block["rate"],
        "callable_absence": block["callable_absence"],
        "callable_trials": ctx.callable_trials,
        "unproven": block["unproven"],
        "polarity": "failure_mass",
        "omitted": block["rate"] is None,
        "note": block["note"],
    }


def uncertainty_absence(
    block: Mapping[str, Any], _ctx: MeasureContext
) -> Mapping[str, Any]:
    return {
        "callable_absence": int(block["callable_absence"]),
        "unproven": int(block["unproven"]),
    }


def reopen_absence(
    block: Mapping[str, Any], _ctx: MeasureContext
) -> Mapping[str, Any]:
    return {
        "unproven_present": bool(block["unproven"]),
        "absence_present": bool(block["callable_absence"]),
        "r_absence_failure_mass": block.get("rate"),
    }


def run_recall(ctx: MeasureContext) -> Optional[Dict[str, Any]]:
    return measure_r_recall(ctx.facts, oracle_arm_present=ctx.oracle_arm)


def measured_recall_projection(block: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "numerator": block["numerator"],
        "denominator": block["denominator"],
        "callable_denominator": block["callable_denominator"],
        "rate": block["rate"],
        "structural": block["structural"],
        "evidentiary": block["evidentiary"],
        "omitted": False,
        "claim": RecallClaim.MEASURED,
    }


def omitted_recall_projection(*, claim: RecallClaim, note: str) -> Dict[str, Any]:
    return {
        "numerator": 0,
        "denominator": 0,
        "callable_denominator": 0,
        "rate": None,
        "omitted": True,
        "claim": claim,
        "note": note,
    }


def project_recall(
    block: Optional[Mapping[str, Any]], ctx: MeasureContext
) -> Dict[str, Any]:
    if block is not None:
        return measured_recall_projection(block)
    if ctx.planted_misses > 0:
        return omitted_recall_projection(
            claim=RecallClaim.UNTRUSTED_PLANTED,
            note=(
                "Planted RECALL_MISS stamps are not an oracle. "
                "R_recall stays omitted until a trusted CodeQL receipt is present."
            ),
        )
    return omitted_recall_projection(
        claim=RecallClaim.OMITTED_WITHOUT_ORACLE,
        note="R_recall requires a trusted CodeQL covering receipt",
    )


def reopen_recall(
    block: Optional[Mapping[str, Any]], ctx: MeasureContext
) -> Mapping[str, Any]:
    return {
        "structural_recall_misses": bool(block and block.get("structural")),
        "untrusted_planted_recall": bool(ctx.planted_misses and not ctx.oracle_arm),
    }


def extra_recall(
    block: Optional[Mapping[str, Any]], ctx: MeasureContext
) -> Sequence[Mapping[str, Any]]:
    if block is None and ctx.planted_misses > 0:
        return _planted_recall_failures(ctx.facts)
    return []
