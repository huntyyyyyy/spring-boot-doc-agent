"""Cohesive suite from tests/doc_engine/test_verify_certification.py: _ok_gates_for, _write_incomplete."""

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

def _ok_gates_for(profile: ComplianceProfile) -> list[GateRecord]:
    from doc_engine.pipeline.compliance import gates_required_for_profile

    return [
        GateRecord(id=gid, label=gid, status="ok")
        for gid in sorted(gates_required_for_profile(profile))
    ]


def _write_incomplete(path: Path, data: dict) -> None:
    """Deliberately bypass the builder — only for schema-rejection cases."""
    path.write_text(json.dumps(data), encoding="utf-8")
