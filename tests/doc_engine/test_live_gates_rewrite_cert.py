"""Live-gates certification rewrite paths."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from doc_engine.pipeline import live_gates
from doc_engine.pipeline.compliance import (
    ComplianceProfile,
    build_certification_report,
    write_certification_json,
)
from doc_engine.tools.certification import verify_certification
from tests.doc_engine.cert_helpers import ok_stages_for
from tests.support.live_gates.fixtures import _live_ok_gates
from tests.support.live_gates.rewrite_helpers import (
    assert_live_certified_shape,
    assert_mock_poison_cleared,
    plant_det_prior_and_summaries,
    plant_mock_generative_prior_and_summaries,
    run_live_gates_no_write,
    stub_live_gates_ok,
)

pytestmark = pytest.mark.domain_compliance


def test_live_gates_rewrites_cert_with_executor_live():
    """Stale mock certified:true must not survive a failing live gates pass."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        docs = out / "docs"
        docs.mkdir()
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
        docs = plant_det_prior_and_summaries(out)
        stub_live_gates_ok(monkeypatch)
        assert run_live_gates_no_write(out, docs) == 0
        assert_live_certified_shape(out)


def test_live_gates_strips_mock_generative_and_survives_skipped_poison(monkeypatch):
    """Prior mock generative + skipped rows must not poison a live rewrite."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        docs = plant_mock_generative_prior_and_summaries(out)
        stub_live_gates_ok(monkeypatch)
        assert run_live_gates_no_write(out, docs) == 0
        assert_mock_poison_cleared(out)
