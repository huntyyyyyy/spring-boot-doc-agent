"""Live-gates certification rewrite paths."""

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

def test_live_gates_rewrites_cert_with_executor_live():
    """Stale mock certified:true must not survive a failing live gates pass."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        docs = out / "docs"
        docs.mkdir()
        # Prior mock certificate claims certified — live gates must overwrite it.
        prior = build_certification_report(
            ComplianceProfile.CERTIFIED,
            str(out / "repo"),
            str(out),
            stages=ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="mock"),
            gates=_live_ok_gates(),
            generative_executor="mock",
            allow_mock=True,
        )
        write_certification_json(out, prior)
        assert prior.certified is True

        def _fail_validate(_out_dir: str) -> int:
            return 1

        def _ok_validators(_out: str, _repo: str) -> tuple[int, str]:
            return 0, "ok"

        def _fail_subprocess(_argv: list[str]) -> tuple[int, str]:
            return 1, "planted failure"

        with mock.patch.object(
            live_gates.gates, "run_validate_all_artifacts", _fail_validate
        ), mock.patch.object(
            live_gates.gates, "run_pipeline_validators", _ok_validators
        ), mock.patch.object(
            live_gates.gates, "run_subprocess_gate", _fail_subprocess
        ):
            code = live_gates.run_live_gates(
                out_dir=str(out),
                repo_path=str(out / "repo"),
                docs_dir=str(docs),
                no_write_check=True,
            )
        assert code == 1
        data = json.loads((out / "certification.json").read_text(encoding="utf-8"))
        assert data["generative_executor"] == "live"
        assert data["certified"] is False
        assert any("validate_artifacts_all" in f for f in data["failures"])

        ok, msg = verify_certification(out / "certification.json")
        assert not ok
        assert "not certified" in msg


def test_live_gates_passing_writes_live_certified(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        docs = out / "docs"
        docs.mkdir()
        (out / "summaries.json").write_text("[]\n", encoding="utf-8")
        # Live rewrite keeps det priors; plant a complete det prior so omission
        # cannot vacuous-certify from generative_external alone.
        prior = build_certification_report(
            ComplianceProfile.DETERMINISTIC_ONLY,
            str(out / "repo"),
            str(out),
            stages=ok_det_stages_for(ComplianceProfile.CERTIFIED),
            gates=[GateRecord(id="validate_artifacts_all", label="all", status="ok")],
            generative_executor="none",
        )
        write_certification_json(out, prior)

        monkeypatch.setattr(
            live_gates.gates, "run_validate_all_artifacts", lambda _o: 0
        )
        monkeypatch.setattr(
            live_gates.gates,
            "run_pipeline_validators",
            lambda _o, _r: (0, "ok"),
        )
        monkeypatch.setattr(
            live_gates.gates,
            "run_subprocess_gate",
            lambda _argv: (0, "ok"),
        )

        code = live_gates.run_live_gates(
            out_dir=str(out),
            repo_path=str(out / "repo"),
            docs_dir=str(docs),
            no_write_check=True,
        )
        assert code == 0
        data = json.loads((out / "certification.json").read_text(encoding="utf-8"))
        assert data["generative_executor"] == "live"
        assert data["certified"] is True
        assert data["schema_version"] == 1
        stage_names = [s["name"] for s in data["stages"]]
        assert "generative_external" in stage_names
        assert "doc_writer" not in stage_names
        assert all("executor" in s for s in data["stages"])
        ok, _ = verify_certification(out / "certification.json")
        assert ok


def test_live_gates_strips_mock_generative_and_survives_skipped_poison(monkeypatch):
    """Prior mock generative + skipped rows must not poison a live rewrite."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        docs = out / "docs"
        docs.mkdir()
        (out / "summaries.json").write_text("[]\n", encoding="utf-8")
        prior = build_certification_report(
            ComplianceProfile.CERTIFIED,
            str(out / "repo"),
            str(out),
            stages=[
                *ok_det_stages_for(ComplianceProfile.CERTIFIED),
                StageRecord(name="doc_writer", status="ok", executor="mock"),
                StageRecord(name="architect", status="skipped", executor="none"),
            ],
            gates=_live_ok_gates(),
            generative_executor="mock",
        )
        # Prior may be uncertified due to skipped required stage; live rewrite must
        # still be able to certify from derived stages + passing gates.
        write_certification_json(out, prior)

        monkeypatch.setattr(
            live_gates.gates, "run_validate_all_artifacts", lambda _o: 0
        )
        monkeypatch.setattr(
            live_gates.gates,
            "run_pipeline_validators",
            lambda _o, _r: (0, "ok"),
        )
        monkeypatch.setattr(
            live_gates.gates,
            "run_subprocess_gate",
            lambda _argv: (0, "ok"),
        )

        code = live_gates.run_live_gates(
            out_dir=str(out),
            repo_path=str(out / "repo"),
            docs_dir=str(docs),
            no_write_check=True,
        )
        assert code == 0
        data = json.loads((out / "certification.json").read_text(encoding="utf-8"))
        assert data["certified"] is True
        assert data["generative_executor"] == "live"
        names = {s["name"] for s in data["stages"]}
        assert "signal_scan" in names
        assert "generative_external" in names
        assert "doc_writer" not in names
        assert "architect" not in names
        assert not any("mock_under_live" in f for f in data["failures"])
