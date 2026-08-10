"""RATE_REGISTRY table plus prepare / run / assemble gap views."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

from .absence_recall import (
    _astgrep_receipt_complete,
    _trusted_codeql_oracle_arm,
)
from .common import RateKey
from .registry_hooks_absence_recall import (
    extra_recall,
    project_absence,
    project_recall,
    reopen_absence,
    reopen_recall,
    run_absence,
    run_recall,
    uncertainty_absence,
)
from .registry_hooks_rate_measures import (
    harvest_lin,
    project_code_dep,
    project_lin,
    reopen_coll,
    reopen_join,
    reopen_lin,
    run_code_dep,
    run_coll,
    run_join,
    run_lin,
    run_sym,
    uncertainty_code_dep,
    uncertainty_coll,
    uncertainty_join,
    uncertainty_lin,
)
from .registry_types import (
    UNCERTAINTY_DEFAULTS,
    GapViews,
    MeasureContext,
    MeasuredRates,
    RegisteredMeasure,
    default_harvest,
    project_rate_block,
)
from .uncertainty import UncertaintyClaim, compute_uncertainty

# Extension point: append a RegisteredMeasure for a new R_* family.
RATE_REGISTRY: tuple[RegisteredMeasure, ...] = (
    RegisteredMeasure(RateKey.SYM, run_sym, project_rate_block),
    RegisteredMeasure(
        RateKey.COLL,
        run_coll,
        project_rate_block,
        uncertainty_inputs=uncertainty_coll,
        design_reopen=reopen_coll,
    ),
    RegisteredMeasure(
        RateKey.JOIN,
        run_join,
        project_rate_block,
        uncertainty_inputs=uncertainty_join,
        design_reopen=reopen_join,
    ),
    RegisteredMeasure(
        RateKey.LIN,
        run_lin,
        project_lin,
        harvest_failures=harvest_lin,
        uncertainty_inputs=uncertainty_lin,
        design_reopen=reopen_lin,
    ),
    RegisteredMeasure(
        RateKey.CODE_DEP,
        run_code_dep,
        project_code_dep,
        uncertainty_inputs=uncertainty_code_dep,
    ),
    RegisteredMeasure(
        RateKey.ABSENCE,
        run_absence,
        project_absence,
        uncertainty_inputs=uncertainty_absence,
        design_reopen=reopen_absence,
    ),
    RegisteredMeasure(
        RateKey.RECALL,
        run_recall,
        project_recall,
        design_reopen=reopen_recall,
        extra_failures=extra_recall,
    ),
)


def prepare_measure_context(
    signals: Mapping[str, Any],
    facts: Sequence[Mapping[str, Any]],
    *,
    covering_proof: Optional[Mapping[str, Any]],
    covering_ok: bool,
    callable_trials: int,
) -> MeasureContext:
    """Fill covering/oracle fields shared by registered measures."""
    planted_misses = sum(
        1 for fact in facts if fact.get("predicate") == "RECALL_MISS"
    )
    return MeasureContext(
        signals=signals,
        facts=facts,
        covering_proof=covering_proof,
        covering_ok=covering_ok,
        astgrep_ok=_astgrep_receipt_complete(covering_proof),
        callable_trials=callable_trials,
        oracle_arm=_trusted_codeql_oracle_arm(covering_proof),
        planted_misses=planted_misses,
    )


def _harvest_measure_failures(
    measure: RegisteredMeasure,
    block: Any,
    ctx: MeasureContext,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if measure.collect_failures and block is not None:
        harvest = measure.harvest_failures or default_harvest
        rows.extend(harvest(block, ctx))
    if measure.extra_failures is not None:
        rows.extend(measure.extra_failures(block, ctx))
    return rows


def _run_one_measure(
    measure: RegisteredMeasure,
    ctx: MeasureContext,
    measured: MeasuredRates,
) -> None:
    block = measure.run(ctx)
    measured.blocks[measure.key] = block
    measured.rates[measure.key] = measure.project(block, ctx)
    measured.failures.extend(_harvest_measure_failures(measure, block, ctx))


def run_rate_registry(ctx: MeasureContext) -> MeasuredRates:
    """Execute every registered measure; harvest primary + extra failures."""
    measured = MeasuredRates()
    for measure in RATE_REGISTRY:
        _run_one_measure(measure, ctx, measured)
    return measured


def _fold_uncertainty(fragments: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """Merge measure fragments into the closed U_w kwarg surface (formula SoR)."""
    merged = dict(UNCERTAINTY_DEFAULTS)
    for fragment in fragments:
        merged.update(fragment)
    return compute_uncertainty(
        merged["r_coll"],
        merged["r_join"],
        merged["r_lin_mean"],
        merged["r_code_dep"],
        callable_absence=int(merged["callable_absence"]),
        unproven=int(merged["unproven"]),
    )


def assemble_gap_views(ctx: MeasureContext) -> GapViews:
    """Run registry then fold uncertainty / design_reopen via measure hooks."""
    measured = run_rate_registry(ctx)
    uncertainty_fragments: List[Mapping[str, Any]] = []
    design_reopen: Dict[str, Any] = {}
    for measure in RATE_REGISTRY:
        block = measured.blocks[measure.key]
        if measure.uncertainty_inputs is not None:
            uncertainty_fragments.append(measure.uncertainty_inputs(block, ctx))
        if measure.design_reopen is not None:
            design_reopen.update(measure.design_reopen(block, ctx))
    uncertainty = _fold_uncertainty(uncertainty_fragments)
    design_reopen["vacuous_uncertainty"] = (
        uncertainty.get("claim") == UncertaintyClaim.VACUOUS_NO_SUPPORT
    )
    return GapViews(
        measured=measured,
        uncertainty=uncertainty,
        design_reopen=design_reopen,
    )
