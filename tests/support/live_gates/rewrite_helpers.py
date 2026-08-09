"""Live-gates plant + stub helpers for certification rewrite tests."""

from __future__ import annotations

import json
from pathlib import Path

from doc_engine.pipeline.compliance import (
    ComplianceProfile,
    GateRecord,
    StageRecord,
    build_certification_report,
    write_certification_json,
)
from doc_engine.pipeline import live_gates
from doc_engine.tools.certification import verify_certification
from tests.doc_engine.cert_helpers import ok_det_stages_for
from tests.support.live_gates.fixtures import _live_ok_gates


def stub_live_gates_ok(monkeypatch) -> None:
    monkeypatch.setattr(live_gates.gates, "run_validate_all_artifacts", lambda _o: 0)
    monkeypatch.setattr(
        live_gates.gates, "run_pipeline_validators", lambda _o, _r: (0, "ok")
    )
    monkeypatch.setattr(
        live_gates.gates, "run_subprocess_gate", lambda _argv: (0, "ok")
    )


def plant_det_prior_and_summaries(out: Path) -> Path:
    docs = out / "docs"
    docs.mkdir()
    (out / "summaries.json").write_text("[]\n", encoding="utf-8")
    prior = build_certification_report(
        ComplianceProfile.DETERMINISTIC_ONLY,
        str(out / "repo"),
        str(out),
        stages=ok_det_stages_for(ComplianceProfile.CERTIFIED),
        gates=[GateRecord(id="validate_artifacts_all", label="all", status="ok")],
        generative_executor="none",
    )
    write_certification_json(out, prior)
    return docs


def plant_mock_generative_prior_and_summaries(out: Path) -> Path:
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
    write_certification_json(out, prior)
    return docs


def run_live_gates_no_write(out: Path, docs: Path) -> int:
    return live_gates.run_live_gates(
        out_dir=str(out),
        repo_path=str(out / "repo"),
        docs_dir=str(docs),
        no_write_check=True,
    )


def assert_live_certified_shape(out: Path) -> dict:
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
    return data


def assert_mock_poison_cleared(out: Path) -> dict:
    data = json.loads((out / "certification.json").read_text(encoding="utf-8"))
    assert data["certified"] is True
    assert data["generative_executor"] == "live"
    names = {s["name"] for s in data["stages"]}
    assert "signal_scan" in names
    assert "generative_external" in names
    assert "doc_writer" not in names
    assert "architect" not in names
    assert not any("mock_under_live" in f for f in data["failures"])
    return data
