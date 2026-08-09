"""Cohesive suite: capacity schema characterization cases."""

from __future__ import annotations

from typing import get_args

import pytest
from pydantic import ValidationError

from tests.support.capacity_preflight.characterization import (
    STAGE4_METRIC_KINDS,
    _LEGACY_SHARED_ROOT_KEYS,
    characterization_calibration_report,
    characterization_stage0_report,
)

pytestmark = pytest.mark.domain_schemas


def test_characterization_shared_keys_are_writer_intersection() -> None:
    stage0 = characterization_stage0_report(with_schema_version=False)
    calib = characterization_calibration_report(with_schema_version=False)
    assert set(stage0) & set(calib) == _LEGACY_SHARED_ROOT_KEYS


def test_stage4_metric_kind_literal_matches_writer_vocabulary() -> None:
    from doc_engine.pipeline.artifacts import Stage4MetricKind

    assert set(get_args(Stage4MetricKind)) == STAGE4_METRIC_KINDS


def test_schema_version_required() -> None:
    from doc_engine.pipeline.artifacts import CapacityPreflightReportArtifact

    with pytest.raises(ValidationError):
        CapacityPreflightReportArtifact.model_validate(
            characterization_stage0_report(with_schema_version=False)
        )

    CapacityPreflightReportArtifact.model_validate(
        characterization_stage0_report(with_schema_version=True)
    )


@pytest.mark.parametrize("kind", sorted(STAGE4_METRIC_KINDS))
def test_each_known_metric_kind_validates(kind: str) -> None:
    from doc_engine.pipeline.artifacts import CapacityPreflightReportArtifact

    report = characterization_stage0_report(with_schema_version=True)
    report["stage4_metric_kind"] = kind
    CapacityPreflightReportArtifact.model_validate(report)


def test_unknown_metric_kind_rejected() -> None:
    from doc_engine.pipeline.artifacts import CapacityPreflightReportArtifact

    report = characterization_stage0_report(with_schema_version=True)
    report["stage4_metric_kind"] = "upper_bound"
    with pytest.raises(ValidationError):
        CapacityPreflightReportArtifact.model_validate(report)


def test_calibration_mode_validates() -> None:
    from doc_engine.pipeline.artifacts import CapacityPreflightReportArtifact

    CapacityPreflightReportArtifact.model_validate(
        characterization_calibration_report(with_schema_version=True)
    )
