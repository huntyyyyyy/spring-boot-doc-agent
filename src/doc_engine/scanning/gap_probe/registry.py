"""Closed registry of Stage-0 gap rate measures (OCP extension point).

Add a new rate by appending a ``RegisteredMeasure`` in ``registry_assembly``
and implementing the callable in its domain module — ``report.build_gap_report``
stays closed to unrelated churn. Schema keys (``R_sym``, …) remain the encoding
SoR via ``RateKey``.

Concept modules: ``registry_types``, ``registry_hooks_basic``,
``registry_hooks_absence_recall``, ``registry_assembly``. This façade keeps the
stable ``gap_probe.registry`` import path.
"""

from __future__ import annotations

from .registry_assembly import (
    RATE_REGISTRY,
    assemble_gap_views,
    prepare_measure_context,
    run_rate_registry,
)
from .registry_types import (
    DesignReopenHook,
    FailureHook,
    GapViews,
    MeasureContext,
    MeasuredRates,
    MeasureRunner,
    RateProjector,
    RecallClaim,
    RegisteredMeasure,
    UncertaintyInputs,
)

__all__ = [
    "RATE_REGISTRY",
    "DesignReopenHook",
    "FailureHook",
    "GapViews",
    "MeasureContext",
    "MeasureRunner",
    "MeasuredRates",
    "RateProjector",
    "RecallClaim",
    "RegisteredMeasure",
    "UncertaintyInputs",
    "assemble_gap_views",
    "prepare_measure_context",
    "run_rate_registry",
]
