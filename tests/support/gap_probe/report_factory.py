"""Cohesive suite from tests/doc_engine/test_gap_probe.py: _report."""

from __future__ import annotations

from doc_engine.scanning.facts import facts_from_signals
from doc_engine.scanning.gap_probe import (
    GAP_PROBE_SCHEMA_VERSION,
    SCORING_ENV_CALLABLE,
    SCORING_ENV_POOLED,
    apply_failure_budget,
    build_gap_report,
    failure_locator,
    measure_r_coll,
    measure_r_lin,
    measure_r_sym,
    write_gap_report,
)
from doc_engine.scanning.symbol import format_type

def _report(signals, facts, **kwargs):
    return build_gap_report(signals, facts, covering_ok=True, covering_why="", **kwargs)
