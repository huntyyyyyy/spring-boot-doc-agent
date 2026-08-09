"""Gap-probe identity/collision axioms."""

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

def test_contested_map_raises_r_coll() -> None:
    """Deviation: contested collision not reflected in R_coll."""
    clean = {
        "entity_table_map": {
            "Order": {
                "file": "Order.java",
                "table": "orders",
                "fqcn": "com.acme.Order",
                "package": "com.acme",
            }
        },
        "evidence": {},
    }
    contested = {
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
        "evidence": {},
    }
    r_clean = measure_r_coll(clean)["rate"]
    r_bad = measure_r_coll(contested)["rate"]
    assert r_clean == 0.0
    assert r_bad == 1.0
    assert r_bad > r_clean


def test_bare_maps_to_subject_lowers_r_sym() -> None:
    """Deviation: illegal MAPS_TO subjects still scored as perfect R_sym."""
    good_facts = [
        {
            "predicate": "MAPS_TO",
            "subject": format_type("com.acme", "Order"),
            "object": "orders",
            "qualifiers": {
                "display_name": "Order",
                "fqcn": "com.acme.Order",
                "symbol_kind": "type",
            },
            "file": "Order.java",
            "line": None,
            "rule_id": None,
            "scanner": None,
        }
    ]
    bad_facts = [
        {
            "predicate": "MAPS_TO",
            "subject": "User",
            "object": "users",
            "qualifiers": {"display_name": "User", "fqcn": "User", "symbol_kind": "type"},
            "file": "User.java",
            "line": None,
            "rule_id": None,
            "scanner": None,
        }
    ]
    assert measure_r_sym(good_facts)["rate"] == 1.0
    assert measure_r_sym(bad_facts)["rate"] == 0.0


def test_null_query_stratum_isolated() -> None:
    """Deviation: null-query rows mixed into native available rate (callable env)."""
    signals = {
        "entity_table_map": {},
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
            ]
        },
    }
    lin = measure_r_lin(signals, scoring_env=SCORING_ENV_CALLABLE)
    assert lin["strata"]["null_query"]["denominator"] == 1
    assert lin["strata"]["null_query"]["numerator"] == 0
    assert lin["strata"]["native"]["denominator"] == 1
    assert lin["strata"]["native"]["rate"] == 1.0
    assert lin["mean_rate"] == 1.0  # null_query excluded from callable mean
    assert lin["failure_taxonomy"].get("null_query") == 1


def test_a1_callable_vs_pooled_moves_r_lin() -> None:
    """A1: scoring-env changes R_lin mean when null_query rows exist."""
    signals = {
        "entity_table_map": {},
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
            ]
        },
    }
    call = measure_r_lin(signals, scoring_env=SCORING_ENV_CALLABLE)
    pooled = measure_r_lin(signals, scoring_env=SCORING_ENV_POOLED)
    assert call["mean_rate"] == 1.0
    assert call["denominator"] == 1
    assert pooled["mean_rate"] == 0.5
    assert pooled["denominator"] == 2
    assert call["mean_rate"] != pooled["mean_rate"]
