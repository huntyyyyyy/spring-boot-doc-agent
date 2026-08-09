"""Cohesive suite from tests/doc_engine/test_verify_certification.py: test_verify_certified_true, test_verify_not_certified, test_verify_missing_file, test_load_certification_invalid_json, test_builder_round_trip_load_accepts_full_report, test_verify_certification_script_main, test_verify_refold_matches_honest_report."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
import pytest
from doc_engine.pipeline.compliance import (
    SCAN_ONLY_GATE_ID,
    ComplianceProfile,
    GateRecord,
    StageRecord,
    build_certification_report,
    write_certification_json,
)
from doc_engine.tools.certification import load_certification, verify_certification
from tests.doc_engine.cert_helpers import ok_stages_for
from tests.support.certification.verify_fixtures import _ok_gates_for, _write_incomplete

def test_verify_certified_true():
    with tempfile.TemporaryDirectory() as tmp:
        report = build_certification_report(
            ComplianceProfile.CERTIFIED,
            "/repo",
            tmp,
            stages=ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="live"),
            gates=_ok_gates_for(ComplianceProfile.CERTIFIED),
            generative_executor="live",
        )
        assert report.certified is True
        path = write_certification_json(tmp, report)
        ok, msg = verify_certification(path)
        assert ok
        assert "OK" in msg


def test_verify_not_certified():
    with tempfile.TemporaryDirectory() as tmp:
        report = build_certification_report(
            ComplianceProfile.CERTIFIED,
            "/repo",
            tmp,
            stages=[StageRecord(name="signal_scan", status="ok")],
            gates=[
                GateRecord(
                    id="validate_artifacts_all",
                    label="artifacts",
                    status="fail",
                    detail="contract broken",
                )
            ],
            generative_executor="live",
        )
        assert report.certified is False
        assert any("validate_artifacts_all" in f for f in report.failures)
        path = write_certification_json(tmp, report)
        ok, msg = verify_certification(path)
        assert not ok
        assert "not certified" in msg
        assert "certification schema" not in msg


def test_verify_missing_file():
    ok, msg = verify_certification(Path("/nonexistent/certification.json"))
    assert not ok
    assert "not found" in msg


def test_load_certification_invalid_json():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "certification.json"
        path.write_text("{not json", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            load_certification(path)


def test_builder_round_trip_load_accepts_full_report():
    with tempfile.TemporaryDirectory() as tmp:
        report = build_certification_report(
            ComplianceProfile.SCAN_ONLY,
            "/repo",
            tmp,
            stages=ok_stages_for(ComplianceProfile.SCAN_ONLY),
            gates=[
                GateRecord(id=SCAN_ONLY_GATE_ID, label="signals", status="ok"),
            ],
        )
        path = write_certification_json(tmp, report)
        data = load_certification(path)
        assert data["certified"] is True
        assert data["repo_path"] == "/repo"
        assert data["compliance_profile"] == "scan_only"
        assert SCAN_ONLY_GATE_ID in data["profile_gate_ids"]


def test_verify_certification_script_main():
    from doc_engine.tools.certification import main

    with tempfile.TemporaryDirectory() as tmp:
        ok_report = build_certification_report(
            ComplianceProfile.CERTIFIED,
            "/repo",
            tmp,
            stages=ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="live"),
            gates=_ok_gates_for(ComplianceProfile.CERTIFIED),
            generative_executor="live",
        )
        path = write_certification_json(tmp, ok_report)
        assert main([str(path)]) == 0

        stages = [
            StageRecord(name=s.name, status="fail", detail="exit 1", executor=s.executor)
            if s.name == "signal_scan"
            else s
            for s in ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="live")
        ]
        bad_report = build_certification_report(
            ComplianceProfile.CERTIFIED,
            "/repo",
            tmp,
            stages=stages,
            gates=_ok_gates_for(ComplianceProfile.CERTIFIED),
            generative_executor="live",
        )
        write_certification_json(tmp, bad_report)
        assert main([str(path)]) == 1


def test_verify_refold_matches_honest_report():
    with tempfile.TemporaryDirectory() as tmp:
        report = build_certification_report(
            ComplianceProfile.CERTIFIED,
            "/repo",
            tmp,
            stages=ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="live"),
            gates=_ok_gates_for(ComplianceProfile.CERTIFIED),
            generative_executor="live",
        )
        path = write_certification_json(tmp, report)
        ok, msg = verify_certification(path)
        assert ok
        assert "OK" in msg
