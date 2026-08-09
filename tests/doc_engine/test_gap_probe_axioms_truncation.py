"""Gap-probe truncation/vacuous axioms."""

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
from tests.support.gap_probe.report_factory import _report

import pytest

pytestmark = pytest.mark.domain_stage0

def test_a2_scoring_env_preserves_identity_rates() -> None:
    """A2: scoring-env does not invent identity failure."""
    signals = {
        "schema_version": 7,
        "scanner_version": "test",
        "entity_table_map": {
            "Order": {
                "file": "Order.java",
                "table": "orders",
                "package": "com.acme",
                "fqcn": "com.acme.Order",
            }
        },
        "evidence": {
            "raw_queries": [
                {
                    "file": "A.java",
                    "line": 1,
                    "query_kind": "native",
                    "query": None,
                    "lineage": {"available": False},
                },
                {
                    "file": "B.java",
                    "line": 2,
                    "query_kind": "native",
                    "query": "SELECT 1",
                    "lineage": {"available": True},
                },
            ],
            "deployment": [],
        },
    }
    facts = facts_from_signals(signals)
    report, _ = _report(signals, facts)
    assert report["rates"]["R_sym"]["rate"] == 1.0
    assert report["rates"]["R_coll"]["rate"] == 0.0
    assert report["rates"]["R_join"]["rate"] == 1.0
    delta = report["measurement"]["delta_r_scoring_env"]
    assert delta["R_sym"] == 0.0
    assert delta["R_coll"] == 0.0
    assert delta["R_join"] == 0.0
    assert delta["R_lin_mean"] == 0.5

def test_a3_collision_only_does_not_force_dialect_lineage_reopen() -> None:
    """A3: collision-only fixture must not set lineage dominant to dialect_or_syntax."""
    signals = {
        "entity_table_map": {
            "User": {
                "file": "a/User.java",
                "table": "a_user",
                "status": "contested",
                "fqcn": "com.example.a.User",
                "package": "com.example.a",
                "candidates": [
                    {
                        "file": "a/User.java",
                        "table": "a_user",
                        "package": "com.example.a",
                        "fqcn": "com.example.a.User",
                    },
                    {
                        "file": "b/User.java",
                        "table": "b_user",
                        "package": "com.example.b",
                        "fqcn": "com.example.b.User",
                    },
                ],
            }
        },
        "evidence": {"raw_queries": [], "deployment": []},
    }
    facts = [
        {
            "predicate": "MAPS_TO",
            "subject": format_type("com.example.a", "User"),
            "object": "a_user",
            "qualifiers": {
                "display_name": "User",
                "fqcn": "com.example.a.User",
                "symbol_kind": "type",
            },
            "file": "a/User.java",
            "line": None,
            "rule_id": None,
            "scanner": None,
        }
    ]
    report, _ = _report(signals, facts)
    assert report["design_reopen"]["path_a_to_symbols"] is True
    dominant = report["design_reopen"]["lineage_dominant_stratum"]
    assert dominant is None or dominant.get("reason_class") != "dialect_or_syntax"

def test_a4_truncation_loss_monotone_in_b() -> None:
    """A4: B' < B => L(B') >= L(B) on planted must-keep set."""
    failures = [
        {
            "layer": "lineage",
            "stratum": "native",
            "reason_class": "dialect_or_syntax",
            "file": f"F{i}.java",
            "line": i,
        }
        for i in range(5)
    ]
    locs = [failure_locator(f) for f in failures]
    must_keep = [locs[0], locs[4]]  # first and last in sort order
    _, t_full = apply_failure_budget(failures, budget=5, must_keep=must_keep)
    _, t_mid = apply_failure_budget(failures, budget=2, must_keep=must_keep)
    _, t_zero = apply_failure_budget(failures, budget=0, must_keep=must_keep)
    assert t_full["L"] <= t_mid["L"] <= t_zero["L"]
    assert t_full["L"] == 0.0
    assert t_zero["L"] == 1.0

def test_a5_truncation_slot_typed() -> None:
    """A5: truncation loss lives under measurement.truncation only."""
    signals = {
        "entity_table_map": {},
        "evidence": {
            "raw_queries": [
                {
                    "file": "A.java",
                    "line": 1,
                    "query_kind": "native",
                    "query": "SELECT 1",
                    "lineage": {"available": False, "reason": "InvalidSyntaxException"},
                }
            ],
            "deployment": [],
        },
    }
    report, _ = _report(signals, facts=[], failure_budget=0, must_keep=["x"])
    trunc = report["measurement"]["truncation"]
    assert trunc["slot"] == "truncation_loss"
    assert "L" in trunc
    assert "truncation" not in report["uncertainty"]
    assert report["uncertainty"]["slot"] == "comparison_index"
    assert GAP_PROBE_SCHEMA_VERSION == 3
    assert report["schema_version"] == 3
