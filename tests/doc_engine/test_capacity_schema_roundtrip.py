"""Cohesive suite from tests/doc_engine/test_capacity_preflight_schema.py: test_round_trip_preserves_required_identity, test_compute_preflight_emits_schema_version, test_compute_stage4_calibration_emits_schema_version, test_capacity_preflight_report_registered, test_validate_artifact_file_accepts_fixture, test_validate_artifact_file_rejects_bad_metric_kind, test_exported_schema_file_committed."""

from __future__ import annotations

import json
from pathlib import Path
from typing import get_args
import pytest
from pydantic import ValidationError
from doc_engine.pipeline.artifacts import ARTIFACT_FILENAMES, ARTIFACT_MODELS
from doc_engine.pipeline.validation import ArtifactValidationError, validate_artifact_file
from doc_engine.tools import capacity_preflight
from tests.support.capacity_preflight.characterization import (
    characterization_stage0_report,
)

pytestmark = pytest.mark.domain_schemas

STAGE4_METRIC_KINDS = frozenset({
    "partial_proxy_pre_stage4",
    "measured_stage4_inputs",
})
_LEGACY_SHARED_ROOT_KEYS = frozenset({
    "repo_path",
    "stage4_metric_kind",
    "stage4_included_now",
    "stage4_omitted_not_estimated",
    "stage4_shared_pool_upper_bound_est_tokens",
    "stage4_summaries_est_tokens",
    "stage4_interview_answers_est_tokens",
    "stage4_interview_answers_omitted",
    "stage4_signals_est_tokens",
    "stage4_signals_omitted",
    "stage4_aggregate_input_upper_bound_est_tokens",
    "stage4_return_payloads_estimated",
    "warnings",
})

def test_round_trip_preserves_required_identity() -> None:
    from doc_engine.pipeline.artifacts import CapacityPreflightReportArtifact

    report = characterization_stage0_report(with_schema_version=True)
    dumped = CapacityPreflightReportArtifact.model_validate(report).model_dump()
    assert dumped["schema_version"] == (
        capacity_preflight.CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION
    )
    assert dumped["repo_path"] == report["repo_path"]
    assert dumped["stage4_metric_kind"] == "partial_proxy_pre_stage4"
    assert dumped["stage4_return_payloads_estimated"] is False

def test_compute_preflight_emits_schema_version() -> None:
    groups = {
        "repo_path": "/fake/repo",
        "max_tokens_per_group": 120000,
        "num_groups": 1,
        "groups": [{"id": 0, "files": ["a.java"], "est_tokens": 10}],
    }
    edges = {
        "num_groups": 1,
        "groups": {"0": {"outbound": [], "inbound": [], "same_package_outside": []}},
        "stats": {},
    }
    report = capacity_preflight.compute_preflight(
        "/fake/repo", groups_data=groups, edges=edges,
        group_warn_threshold=1000, fanout_warn_threshold=1000,
        stage4_shared_tokens_warn_threshold=10_000_000,
    )
    assert report["schema_version"] == (
        capacity_preflight.CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION
    )
    assert set(report) >= _LEGACY_SHARED_ROOT_KEYS | {
        "schema_version", "num_groups", "stage_fanout", "edge_join_stats",
    }

def test_compute_stage4_calibration_emits_schema_version() -> None:
    report = capacity_preflight.compute_stage4_calibration(
        "/fake/repo",
        summaries_data=[{"file": "a.java", "summary": "s"}],
        stage4_shared_tokens_warn_threshold=10_000_000,
    )
    assert report["schema_version"] == (
        capacity_preflight.CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION
    )
    assert report["mode"] == "stage4_calibration"
    assert report["stage4_metric_kind"] == "measured_stage4_inputs"

def test_capacity_preflight_report_registered() -> None:
    assert "capacity_preflight_report" in ARTIFACT_MODELS
    assert (
        ARTIFACT_FILENAMES["capacity_preflight_report"]
        == "capacity_preflight_report.json"
    )

def test_validate_artifact_file_accepts_fixture(tmp_path: Path) -> None:
    path = tmp_path / "capacity_preflight_report.json"
    path.write_text(
        json.dumps(characterization_stage0_report(with_schema_version=True)),
        encoding="utf-8",
    )
    model = validate_artifact_file("capacity_preflight_report", path)
    assert model.schema_version == (
        capacity_preflight.CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION
    )

def test_validate_artifact_file_rejects_bad_metric_kind(tmp_path: Path) -> None:
    report = characterization_stage0_report(with_schema_version=True)
    report["stage4_metric_kind"] = "bogus"
    path = tmp_path / "capacity_preflight_report.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    with pytest.raises(ArtifactValidationError):
        validate_artifact_file("capacity_preflight_report", path)

def test_exported_schema_file_committed() -> None:
    from tests.conftest import REPO_ROOT

    schema_path = (
        REPO_ROOT / "scripts" / "schemas" / "capacity_preflight_report.schema.json"
    )
    assert schema_path.is_file()
    from doc_engine.pipeline.artifacts import export_json_schemas

    assert "capacity_preflight_report" in export_json_schemas()
