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


def test_oracle_cell_posture_flags_missing_policy(tmp_path: Path) -> None:
    hits = scan_oracle_cell_posture(tmp_path)
    assert hits and hits[0].kind == "oracle_cell_posture"
    assert "missing" in hits[0].summary


def test_oracle_cell_posture_flags_unwired_pre_pr(tmp_path: Path) -> None:
    policy = tmp_path / "src/doc_engine/ci/oracle_push_policy.py"
    policy.parent.mkdir(parents=True)
    policy.write_text("# present\n", encoding="utf-8")
    pre = tmp_path / "scripts/ci/pre_pr.py"
    pre.parent.mkdir(parents=True)
    pre.write_text("print('no oracle wire')\n", encoding="utf-8")
    qg = tmp_path / "scripts/ci/pre_pr_quality_gates_suite.py"
    qg.write_text("skip_coverage = True\n# never opens oracle xml\n", encoding="utf-8")
    kinds = {f.summary for f in scan_oracle_cell_posture(tmp_path)}
    assert any("oracle remesure" in s for s in kinds)
    assert any("never consults" in s for s in kinds)


def test_codeql_change_presence_flags_absent(tmp_path: Path) -> None:
    wf = tmp_path / ".github/workflows/codeql-signals.yml"
    wf.parent.mkdir(parents=True)
    wf.write_text("name: bare\n", encoding="utf-8")
    hits = scan_codeql_change_presence(tmp_path)
    assert len(hits) == 2
    assert all(h.kind == "codeql_change_presence" for h in hits)


def test_workflow_suite_map_flags_missing_hard_names(tmp_path: Path) -> None:
    pre = tmp_path / "scripts/ci/pre_pr.py"
    pre.parent.mkdir(parents=True)
    pre.write_text("SUITES = []\n", encoding="utf-8")
    hits = scan_workflow_suite_map(tmp_path)
    assert len(hits) == 3
    assert all(h.kind == "workflow_suite_map" for h in hits)


def test_public_surface_policy_residuals_and_private_all(tmp_path: Path) -> None:
    from doc_engine.ci import public_surface_policy as psp

    base = tmp_path / "src/doc_engine/pipeline/local_runner_phases"
    base.mkdir(parents=True)
    (base / "support.py").write_text("# residual\n", encoding="utf-8")
    assert any(p.endswith("support.py") for p in psp.forbidden_residual_paths(tmp_path))
    assert psp.forbidden_residual_paths(tmp_path / "nope") == []
    assert psp.module_private_all_exports("doc_engine.ci.oracle_push_policy") == []
