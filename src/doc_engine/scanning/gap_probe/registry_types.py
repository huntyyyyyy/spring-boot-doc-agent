"""Gap-probe registry types and shared projection helpers (ports surface)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence

from doc_engine._compat import StrEnum

from .common import RateKey


class RecallClaim(StrEnum):
    """Closed claim stamps for the R_recall projection."""

    MEASURED = "measured"
    UNTRUSTED_PLANTED = "untrusted_planted"
    OMITTED_WITHOUT_ORACLE = "omitted_without_oracle"


@dataclass
class MeasureContext:
    """Shared inputs for registered rate callables."""

    signals: Mapping[str, Any]
    facts: Sequence[Mapping[str, Any]]
    covering_proof: Optional[Mapping[str, Any]] = None
    covering_ok: bool = False
    astgrep_ok: bool = False
    callable_trials: Optional[int] = None
    oracle_arm: bool = False
    planted_misses: int = 0


MeasureRunner = Callable[[MeasureContext], Any]
RateProjector = Callable[[Any, MeasureContext], Dict[str, Any]]
# Fragments merge into compute_uncertainty kwargs (Path A dens + S3 stamps).
UncertaintyInputs = Callable[[Any, MeasureContext], Mapping[str, Any]]
DesignReopenHook = Callable[[Any, MeasureContext], Mapping[str, Any]]
FailureHook = Callable[[Any, MeasureContext], Sequence[Mapping[str, Any]]]


@dataclass(frozen=True)
class RegisteredMeasure:
    """One gap-probe rate: run → project + optional assembly hooks."""

    key: RateKey
    run: MeasureRunner
    project: RateProjector
    collect_failures: bool = True
    harvest_failures: Optional[FailureHook] = None
    uncertainty_inputs: Optional[UncertaintyInputs] = None
    design_reopen: Optional[DesignReopenHook] = None
    extra_failures: Optional[FailureHook] = None


@dataclass
class MeasuredRates:
    """Result of running ``RATE_REGISTRY`` once over a context."""

    blocks: Dict[str, Any] = field(default_factory=dict)
    rates: Dict[str, Any] = field(default_factory=dict)
    failures: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class GapViews:
    """Rates plus folded uncertainty / design_reopen from registry hooks.

    ``design_reopen`` holds measure-contributed flags and ``vacuous_uncertainty``.
    Report assembly still adds ``truncation_alarm`` after the failure budget.
    """

    measured: MeasuredRates
    uncertainty: Dict[str, Any]
    design_reopen: Dict[str, Any]


def project_rate_block(
    block: Mapping[str, Any], _ctx: MeasureContext
) -> Dict[str, Any]:
    return {
        "numerator": block["numerator"],
        "denominator": block["denominator"],
        "callable_denominator": block["callable_denominator"],
        "rate": block["rate"],
    }


def default_harvest(block: Any, _ctx: MeasureContext) -> List[Dict[str, Any]]:
    if isinstance(block, Mapping):
        return list(block.get("failures") or [])
    return []


UNCERTAINTY_DEFAULTS: Dict[str, Any] = {
    "r_coll": None,
    "r_join": None,
    "r_lin_mean": None,
    "r_code_dep": None,
    "callable_absence": 0,
    "unproven": 0,
}
