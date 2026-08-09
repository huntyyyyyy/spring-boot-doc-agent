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
from .registry_hooks_absence_recall import (
    extra_recall as _extra_recall,
    measured_recall_projection as _measured_recall_projection,
    omitted_recall_projection as _omitted_recall_projection,
    project_absence as _project_absence,
    project_recall as _project_recall,
    reopen_absence as _reopen_absence,
    reopen_recall as _reopen_recall,
    run_absence as _run_absence,
    run_recall as _run_recall,
    uncertainty_absence as _uncertainty_absence,
)
from .registry_hooks_basic import (
    harvest_lin as _harvest_lin,
    project_code_dep as _project_code_dep,
    project_lin as _project_lin,
    reopen_coll as _reopen_coll,
    reopen_join as _reopen_join,
    reopen_lin as _reopen_lin,
    run_code_dep as _run_code_dep,
    run_coll as _run_coll,
    run_join as _run_join,
    run_lin as _run_lin,
    run_sym as _run_sym,
    uncertainty_code_dep as _uncertainty_code_dep,
    uncertainty_coll as _uncertainty_coll,
    uncertainty_join as _uncertainty_join,
    uncertainty_lin as _uncertainty_lin,
)
from .registry_types import (
    UNCERTAINTY_DEFAULTS as _UNCERTAINTY_DEFAULTS,
    DesignReopenHook,
    FailureHook,
    GapViews,
    MeasureContext,
    MeasureRunner,
    MeasuredRates,
    RateProjector,
    RecallClaim,
    RegisteredMeasure,
    UncertaintyInputs,
    default_harvest as _default_harvest,
    project_rate_block as _project_rate_block,
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
