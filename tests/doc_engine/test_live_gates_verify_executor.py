"""Live-gates verify/allow_mock executor paths."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest import mock
from doc_engine.pipeline.compliance import (
    CERTIFIED_GATE_IDS,
    ComplianceProfile,
    GateRecord,
    StageRecord,
    build_certification_report,
    write_certification_json,
)
from doc_engine.pipeline import live_gates
from doc_engine.tools.certification import main as cert_main
from doc_engine.tools.certification import verify_certification
from tests.doc_engine.cert_helpers import ok_det_stages_for, ok_stages_for
from tests.support.live_gates.fixtures import _live_ok_gates, _plant_weak_docs, _mock_non_citation_gates

import pytest

pytestmark = pytest.mark.domain_pipeline

def test_verify_rejects_mock_without_allow_mock():
    with tempfile.TemporaryDirectory() as tmp:
        # Builder itself refuses CERTIFIED+mock without allow_mock.
        denied = build_certification_report(
            ComplianceProfile.CERTIFIED,
            "/repo",
            tmp,
            stages=ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="mock"),
            gates=_live_ok_gates(),
            generative_executor="mock",
        )
        assert denied.certified is False
        assert "generative_executor:mock:allow_mock_required" in denied.failures

        # Issued under allow_mock — verify still requires the flag (refold + gate).
        report = build_certification_report(
            ComplianceProfile.CERTIFIED,
            "/repo",
            tmp,
            stages=ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="mock"),
            gates=_live_ok_gates(),
            generative_executor="mock",
            allow_mock=True,
        )
        assert report.certified is True
        path = write_certification_json(tmp, report)
        ok, msg = verify_certification(path)
        assert not ok
        assert "generative_executor" in msg
        assert "mock" in msg

        ok2, _ = verify_certification(path, allow_mock=True)
        assert ok2
        assert cert_main([str(path)]) == 1
        assert cert_main([str(path), "--allow-mock"]) == 0

def test_verify_rejects_none_without_allow_mock():
    with tempfile.TemporaryDirectory() as tmp:
        report = build_certification_report(
            ComplianceProfile.SCAN_ONLY,
            "/repo",
            tmp,
            stages=ok_stages_for(ComplianceProfile.SCAN_ONLY),
            gates=[
                GateRecord(
                    id="validate_artifacts_spring_signals",
                    label="signals",
                    status="ok",
                )
            ],
            generative_executor="none",
        )
        path = write_certification_json(tmp, report)
        ok, msg = verify_certification(path)
        assert not ok
        assert "none" in msg

def test_verify_accepts_live_certified():
    with tempfile.TemporaryDirectory() as tmp:
        report = build_certification_report(
            ComplianceProfile.CERTIFIED,
            "/repo",
            tmp,
            stages=ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="live"),
            gates=_live_ok_gates(),
            generative_executor="live",
        )
        path = write_certification_json(tmp, report)
        ok, msg = verify_certification(path)
        assert ok
        assert "OK" in msg
        assert cert_main([str(path)]) == 0
