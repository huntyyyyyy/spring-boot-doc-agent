"""Coverage climb B7: compliance profile / stage executor / prior-drop.

Q2 adequacy witness: mutmut_slice on doc_engine.pipeline.compliance — asserts
bite string profile coerce, SKIPPED/LIVE executor stamps, and prior-stage drop
/ normalize branches (not padding).
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from doc_engine.pipeline import compliance as comp

pytestmark = pytest.mark.domain_climb_sensor


def test_resolve_compliance_profile_from_string_config() -> None:
    cfg = SimpleNamespace(compliance_profile="scan_only")
    args = SimpleNamespace(compliance_profile=None, deterministic_only=False)
    assert (
        comp.resolve_compliance_profile(cfg, args) == comp.ComplianceProfile.SCAN_ONLY
    )


def test_stage_status_and_executor_branches() -> None:
    assert comp._stage_status_from_runner("SKIPPED") == comp.RecordStatus.SKIPPED
    assert (
        comp._skipped_stage_executor("interview") == comp.StageExecutorKind.NONE
        or comp._skipped_stage_executor("signal_scan")
        == comp.StageExecutorKind.DETERMINISTIC
    )
    # Generative skip → NONE; deterministic skip → DETERMINISTIC
    gen_names = comp.generative_stage_names()
    gen = next(iter(gen_names))
    assert comp._skipped_stage_executor(gen) == comp.StageExecutorKind.NONE
    assert (
        comp._skipped_stage_executor("signal_scan")
        == comp.StageExecutorKind.DETERMINISTIC
    )
    assert comp._generative_stage_executor("OK") == comp.StageExecutorKind.LIVE
    assert (
        comp._stage_executor_from_runner("SKIPPED", "signal_scan")
        == comp.StageExecutorKind.DETERMINISTIC
    )
    assert (
        comp._stage_executor_from_runner("SKIPPED", gen) == comp.StageExecutorKind.NONE
    )
    assert (
        comp._stage_executor_from_runner("OK", gen) == comp.StageExecutorKind.LIVE
    )


def test_should_drop_and_normalize_prior_stages() -> None:
    det = comp.deterministic_stage_names()
    gen = comp.generative_stage_names()
    det_name = next(iter(det))
    gen_name = next(iter(gen))

    mock_row = comp.StageRecord(
        name=det_name,
        status=comp.RecordStatus.OK,
        executor=comp.StageExecutorKind.MOCK,
    )
    assert comp._should_drop_prior_stage(mock_row, det, gen) is True

    weird = comp.StageRecord(
        name="not_in_graph",
        status=comp.RecordStatus.OK,
        executor=comp.StageExecutorKind.NONE,
    )
    assert comp._should_drop_prior_stage(weird, det, gen) is True

    mismatched = comp.StageRecord(
        name=det_name,
        status=comp.RecordStatus.OK,
        executor=comp.StageExecutorKind.NONE,
    )
    fixed = comp._normalize_kept_prior_stage(mismatched, det)
    assert fixed is not None
    assert fixed.executor == comp.StageExecutorKind.DETERMINISTIC

    drop = comp.StageRecord(
        name="ghost",
        status=comp.RecordStatus.OK,
        executor=comp.StageExecutorKind.NONE,
    )
    assert comp._normalize_kept_prior_stage(drop, det) is None
