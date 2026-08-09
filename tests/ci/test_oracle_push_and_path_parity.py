"""E-HOOK2 / E-CQL1 / E-TEL2 regression tests that bite."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

import pre_pr
from doc_engine.ci.oracle_push_policy import (
    path_triggers_oracle,
    should_remesure_oracle,
)
from doc_engine.ci.stalker_path_parity import (
    scan_codeql_change_presence,
    scan_oracle_cell_posture,
    scan_workflow_suite_map,
)
from doc_engine.ci.stalker_sensors.finding_records import ALL_KINDS
from doc_engine.ci.stalker_sensors.scan import run_all_sensors

REPO = Path(__file__).resolve().parents[2]

pytestmark = pytest.mark.domain_ci_meta


def test_oracle_policy_triggers_on_package_and_tests() -> None:
    assert path_triggers_oracle("src/doc_engine/ci/x.py")
    assert path_triggers_oracle("tests/ci/test_x.py")
    assert not path_triggers_oracle("README.md")


def test_should_remesure_oracle_modes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PRE_PR_SKIP_ORACLE", raising=False)
    monkeypatch.delenv("PRE_PR_FORCE_ORACLE", raising=False)
    assert should_remesure_oracle("full", []) is True
    assert should_remesure_oracle("fast", ["src/doc_engine/a.py"]) is False
    assert should_remesure_oracle("standard", ["README.md"]) is False
    assert should_remesure_oracle("standard", ["src/doc_engine/a.py"]) is True
    monkeypatch.setenv("PRE_PR_SKIP_ORACLE", "1")
    assert should_remesure_oracle("full", ["src/doc_engine/a.py"]) is False


def test_pre_pr_standard_includes_oracle_or_pytest_name() -> None:
    os.environ["PRE_PR_FORCE_ORACLE"] = "1"
    try:
        names = [n for n, _, _ in pre_pr.build_suites("standard")]
        assert "oracle_coverage" in names
        assert "pytest" not in names
    finally:
        os.environ.pop("PRE_PR_FORCE_ORACLE", None)
    os.environ["PRE_PR_SKIP_ORACLE"] = "1"
    try:
        names = [n for n, _, _ in pre_pr.build_suites("standard")]
        assert "pytest" in names
        assert "oracle_coverage" not in names
    finally:
        os.environ.pop("PRE_PR_SKIP_ORACLE", None)


def test_codeql_gate_script_runs() -> None:
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts/ci/codeql_signals_change_gate.py")],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "run_expensive=" in proc.stdout


def test_path_parity_sensors_clean_on_tip() -> None:
    assert scan_oracle_cell_posture(REPO) == []
    assert scan_codeql_change_presence(REPO) == []
    assert scan_workflow_suite_map(REPO) == []
    run_all_sensors(REPO)
    assert "oracle_cell_posture" in ALL_KINDS
    assert "codeql_change_presence" in ALL_KINDS
    assert "workflow_suite_map" in ALL_KINDS
