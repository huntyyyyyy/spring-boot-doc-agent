"""Cohesive suite from tests/doc_engine/test_verify_certification.py: test_pre_schema_incomplete_dicts_fail_schema_gate, test_incomplete_cert_fails_schema_gate, test_main_rejects_incomplete_certified_true_dict, test_verify_rejects_forged_certified_bit, test_verify_rejects_certified_with_nonempty_failures."""

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

pytestmark = pytest.mark.domain_compliance

def test_pre_schema_incomplete_dicts_fail_schema_gate(payload: dict):
    """Exact HEAD fixture shapes that broke CI after CertificationReport gating."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "certification.json"
        _write_incomplete(path, payload)
        with pytest.raises(ValueError, match="certification schema"):
            load_certification(path)
        ok, msg = verify_certification(path)
        assert not ok
        assert "certification schema" in msg
        # Schema path — must not look like a well-formed "not certified" report.
        assert "not certified" not in msg

def test_incomplete_cert_fails_schema_gate():
    """Alias kept for discoverability — certified:true alone is not enough."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "certification.json"
        _write_incomplete(path, {"certified": True})
        with pytest.raises(ValueError, match="certification schema"):
            load_certification(path)
        ok, msg = verify_certification(path)
        assert not ok
        assert "certification schema" in msg

def test_main_rejects_incomplete_certified_true_dict():
    """Regression: main([path]) used to return 0 on {\"certified\": True} alone."""
    from doc_engine.tools.certification import main

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "certification.json"
        _write_incomplete(path, {"certified": True})
        assert main([str(path)]) == 1

def test_verify_rejects_forged_certified_bit():
    """Deviation: stamped certified=true survives when refold fails."""
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
        data = json.loads(path.read_text(encoding="utf-8"))
        # Drop a required stage row but keep certified=true / empty failures.
        data["stages"] = [s for s in data["stages"] if s["name"] != "signal_scan"]
        data["certified"] = True
        data["failures"] = []
        path.write_text(json.dumps(data), encoding="utf-8")
        ok, msg = verify_certification(path)
        assert not ok
        assert "refold" in msg.lower() or "≠" in msg

def test_verify_rejects_certified_with_nonempty_failures():
    """Deviation: certified∧failures≠∅ accepted as coherent."""
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
        data = json.loads(path.read_text(encoding="utf-8"))
        data["certified"] = True
        data["failures"] = ["stage:forged:fail"]
        path.write_text(json.dumps(data), encoding="utf-8")
        ok, msg = verify_certification(path)
        assert not ok
        assert "non-empty failures" in msg
