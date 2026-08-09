"""E-STK1 stalker sensors — characterization for G1–G6 runners."""

from __future__ import annotations

import pytest

from doc_engine.ci.stalker_sensors.finding_records import ALL_KINDS
from doc_engine.ci.stalker_sensors.parallel_tip import scan_parallel_tip
from doc_engine.ci.stalker_sensors.policy_verify import scan_policy_verify
from doc_engine.ci.stalker_sensors.scan import run_all_sensors
from doc_engine.ci.stalker_sensors.schema_skew import scan_schema_skew
from doc_engine.paths import repo_root

pytestmark = pytest.mark.domain_ci_meta


def test_schema_skew_clean_on_tip() -> None:
    assert scan_schema_skew(repo_root()) == []


def test_policy_verify_pack_healthy() -> None:
    assert scan_policy_verify(repo_root()) == []


def test_single_active_tip_in_backlog() -> None:
    assert scan_parallel_tip(repo_root()) == []


def test_run_all_sensors_returns_list() -> None:
    findings = run_all_sensors(repo_root())
    assert isinstance(findings, list)
    for item in findings:
        assert item.kind in ALL_KINDS
