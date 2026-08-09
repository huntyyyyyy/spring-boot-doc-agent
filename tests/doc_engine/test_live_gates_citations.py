"""Cohesive suite from tests/doc_engine/test_live_gates.py: test_certified_profile_fails_live_gates_on_weak_citations, test_non_certified_profile_allows_weak_citations_as_worklist, test_force_strict_citations_overrides_non_certified_profile."""

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

def test_certified_profile_fails_live_gates_on_weak_citations(monkeypatch):
    """B3: certified ⇒ strict citations; planted untagged claim fails the gate."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        docs = out / "docs"
        docs.mkdir()
        repo = out / "repo"
        repo.mkdir()
        (out / "summaries.json").write_text("[]\n", encoding="utf-8")
        _plant_weak_docs(docs)
        _mock_non_citation_gates(monkeypatch)

        code = live_gates.run_live_gates(
            out_dir=str(out),
            repo_path=str(repo),
            docs_dir=str(docs),
            compliance_profile="certified",
            no_write_check=True,
        )
        assert code == 1
        data = json.loads((out / "certification.json").read_text(encoding="utf-8"))
        assert data["certified"] is False
        assert any("citation_coverage" in f for f in data["failures"])


def test_non_certified_profile_allows_weak_citations_as_worklist(monkeypatch):
    """B3: deterministic_only keeps citation_coverage as a worklist (exit 0)."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        docs = out / "docs"
        docs.mkdir()
        repo = out / "repo"
        repo.mkdir()
        (out / "summaries.json").write_text("[]\n", encoding="utf-8")
        _plant_weak_docs(docs)
        _mock_non_citation_gates(monkeypatch)
        prior = build_certification_report(
            ComplianceProfile.DETERMINISTIC_ONLY,
            str(repo),
            str(out),
            stages=ok_det_stages_for(ComplianceProfile.CERTIFIED),
            gates=[GateRecord(id="validate_artifacts_all", label="all", status="ok")],
            generative_executor="none",
        )
        write_certification_json(out, prior)

        code = live_gates.run_live_gates(
            out_dir=str(out),
            repo_path=str(repo),
            docs_dir=str(docs),
            compliance_profile="deterministic_only",
            no_write_check=True,
        )
        assert code == 0
        data = json.loads((out / "certification.json").read_text(encoding="utf-8"))
        assert data["certified"] is True


def test_force_strict_citations_overrides_non_certified_profile(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        docs = out / "docs"
        docs.mkdir()
        repo = out / "repo"
        repo.mkdir()
        (out / "summaries.json").write_text("[]\n", encoding="utf-8")
        _plant_weak_docs(docs)
        _mock_non_citation_gates(monkeypatch)

        code = live_gates.run_live_gates(
            out_dir=str(out),
            repo_path=str(repo),
            docs_dir=str(docs),
            compliance_profile="scan_only",
            strict_citations=True,
            no_write_check=True,
        )
        assert code == 1
