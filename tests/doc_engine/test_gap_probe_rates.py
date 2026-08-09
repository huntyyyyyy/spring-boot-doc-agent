"""Cohesive suite from tests/doc_engine/test_gap_probe.py: test_healthy_dual_emit_join_and_sym, test_vacuous_uncertainty_is_null_not_zero, test_vacuous_without_s3_stamps, test_uncertainty_propagates_absence_unproven_counts, test_partial_support_claim, test_unscored_s3_outranks_partial_support, test_write_gap_report_roundtrip, test_rate_registry_keys_match_schema_rates."""

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

def test_healthy_dual_emit_join_and_sym() -> None:
    """Deviation: healthy Path A + facts emit reports R_join/R_sym < 1."""
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
        "evidence": {"raw_queries": [], "deployment": []},
    }
    facts = facts_from_signals(signals)
    report, failures = _report(signals, facts)
    assert report["rates"]["R_sym"]["rate"] == 1.0
    assert report["rates"]["R_coll"]["rate"] == 0.0
    assert report["rates"]["R_join"]["rate"] == 1.0
    assert report["uncertainty"]["U"] == 0.0
    # Dual-emit may stamp UNPROVEN for non-callable families — claim must not
    # look like full_support when S3 stamps exist.
    if report["uncertainty"]["unproven"] or report["uncertainty"]["callable_absence"]:
        assert report["uncertainty"]["claim"] == "comparison_index_with_unscored_s3"
    else:
        assert report["uncertainty"]["claim"] == "comparison_index_full_support"
    assert "callable_absence" in report["uncertainty"]
    assert "unproven" in report["uncertainty"]
    assert failures == []
    assert report["rates"]["R_sym"]["callable_denominator"] == 1


def test_vacuous_uncertainty_is_null_not_zero() -> None:
    """Deviation: empty dens published U=0.0 as if healthy Stage-0."""
    from doc_engine.scanning.gap_probe import compute_uncertainty

    block = compute_uncertainty(None, None, None, None, callable_absence=0, unproven=3)
    assert block["U"] is None
    assert block["claim"] == "vacuous_no_support_with_s3_stamps"
    assert block["unproven"] == 3
    assert block["support"] == []


def test_vacuous_without_s3_stamps() -> None:
    from doc_engine.scanning.gap_probe import compute_uncertainty

    block = compute_uncertainty(None, None, None, None)
    assert block["U"] is None
    assert block["claim"] == "vacuous_no_support"


def test_uncertainty_propagates_absence_unproven_counts() -> None:
    from doc_engine.scanning.gap_probe import compute_uncertainty

    block = compute_uncertainty(
        0.0, 1.0, 1.0, 1.0, callable_absence=2, unproven=5
    )
    assert block["U"] == 0.0
    assert block["callable_absence"] == 2
    assert block["unproven"] == 5
    assert block["claim"] == "comparison_index_with_unscored_s3"


def test_partial_support_claim() -> None:
    """Deviation: one measured dens + imputed rest still looked like full U."""
    from doc_engine.scanning.gap_probe import compute_uncertainty

    block = compute_uncertainty(0.0, None, None, None)
    assert block["U"] == 0.0
    assert block["claim"] == "comparison_index_partial_support"
    assert block["support"] == ["coll"]
    assert set(block["imputed_axes"]) == {"join", "lin", "code"}


def test_unscored_s3_outranks_partial_support() -> None:
    from doc_engine.scanning.gap_probe import compute_uncertainty

    block = compute_uncertainty(0.0, None, None, None, unproven=1)
    assert block["claim"] == "comparison_index_with_unscored_s3"


def test_write_gap_report_roundtrip(tmp_path) -> None:
    """Deviation: gap_report artifacts not written deterministically."""
    report = {"schema_version": GAP_PROBE_SCHEMA_VERSION, "rates": {"R_sym": {"rate": 1.0}}}
    failures = [
        {
            "layer": "facts",
            "stratum": "maps_to_symbol",
            "reason_class": "unparseable_or_non_type",
            "subject": "User",
        }
    ]
    write_gap_report(tmp_path, report, failures)
    assert (tmp_path / "gap_report.json").is_file()
    assert (tmp_path / "gap_failures.jsonl").is_file()
    lines = (tmp_path / "gap_failures.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert '"subject": "User"' in lines[0]


def test_rate_registry_keys_match_schema_rates() -> None:
    """OCP registry must expose exactly the closed R_* schema keys."""
    from doc_engine.scanning.gap_probe import RATE_REGISTRY

    assert tuple(spec.key for spec in RATE_REGISTRY) == (
        "R_sym",
        "R_coll",
        "R_join",
        "R_lin",
        "R_code_dep",
        "R_absence",
        "R_recall",
    )


def test_registry_hooks_drive_uncertainty_and_design_reopen() -> None:
    """Assembly hooks are registry-owned; report only adds truncation_alarm."""
    from doc_engine.scanning.gap_probe import RATE_REGISTRY

    u_keys = tuple(s.key for s in RATE_REGISTRY if s.uncertainty_inputs is not None)
    reopen_keys = tuple(s.key for s in RATE_REGISTRY if s.design_reopen is not None)
    extra_keys = tuple(s.key for s in RATE_REGISTRY if s.extra_failures is not None)
    assert u_keys == ("R_coll", "R_join", "R_lin", "R_code_dep", "R_absence")
    assert reopen_keys == ("R_coll", "R_join", "R_lin", "R_absence", "R_recall")
    assert extra_keys == ("R_recall",)

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
        "evidence": {"raw_queries": [], "deployment": []},
    }
    facts = facts_from_signals(signals)
    report, _ = _report(signals, facts)
    assert set(report["design_reopen"]) == {
        "path_a_to_symbols",
        "join_incomplete",
        "lineage_dominant_stratum",
        "truncation_alarm",
        "structural_recall_misses",
        "unproven_present",
        "absence_present",
        "vacuous_uncertainty",
        "untrusted_planted_recall",
        "r_absence_failure_mass",
    }
    assert set(report["uncertainty"]["residuals"]) == {
        "R_coll",
        "join_gap",
        "lineage_gap",
        "code_dep_gap",
    }
    assert report["uncertainty"]["slot"] == "comparison_index"
    assert "U" in report["uncertainty"]
