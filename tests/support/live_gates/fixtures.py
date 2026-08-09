"""Cohesive suite from tests/doc_engine/test_live_gates.py: _live_ok_gates, _plant_weak_docs, _mock_non_citation_gates."""

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

def _live_ok_gates() -> list[GateRecord]:
    return [
        GateRecord(id=gid, label=gid, status="ok")
        for gid in sorted(CERTIFIED_GATE_IDS)
    ]


def _plant_weak_docs(docs: Path) -> None:
    """Untagged class claim — citation_coverage finding under --strict."""
    (docs / "readme.md").write_text(
        "The InvoiceController handles invoice lookups on every request.\n",
        encoding="utf-8",
    )


def _mock_non_citation_gates(monkeypatch):
    """Stub validate/validators/secrets/pipeline-output; run real citation_coverage."""
    import subprocess as sp

    monkeypatch.setattr(
        live_gates.gates, "run_validate_all_artifacts", lambda _o: 0
    )
    monkeypatch.setattr(
        live_gates.gates,
        "run_pipeline_validators",
        lambda _o, _r: (0, "ok"),
    )

    def _subprocess_real_cc(argv: list[str]) -> tuple[int, str]:
        joined = " ".join(argv)
        if "doc_engine.tools.citation_coverage" in joined:
            proc = sp.run(
                argv,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            body = (proc.stdout or "") + (proc.stderr or "")
            return proc.returncode, body
        return 0, "ok"

    monkeypatch.setattr(live_gates.gates, "run_subprocess_gate", _subprocess_real_cc)
