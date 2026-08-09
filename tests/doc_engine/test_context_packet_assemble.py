"""Cohesive suite from tests/doc_engine/test_context_packet.py: test_tokenize_splits_on_non_alnum, test_bucket_priority_security_beats_references, test_score_item_boosts_request_overlap, test_trim_to_budget_respects_token_proxy, test_context_packet_budget_trims_primary, test_context_packet_hints_always_present, test_context_packet_corrupt_signals_fail_closed, test_cli_context_packet."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from doc_engine.query.freshness import (
    AssumeIndexed,
    SignatureFreshness,
    label_item_path,
)
from doc_engine.query.load import QueryError, QueryMissingError, QueryPathError
from doc_engine.query.packet import CONTEXT_PACKET_SCHEMA_VERSION, run_context_packet
from doc_engine.query.rank import (
    bucket_priority,
    estimate_tokens,
    score_item,
    tokenize,
    trim_to_budget,
)
from tests.support.context_packet.factories import _write_run_dir

def test_tokenize_splits_on_non_alnum() -> None:
    assert "onboarding" in tokenize("fix /api/onboarding role")


def test_bucket_priority_security_beats_references() -> None:
    assert bucket_priority("security") > bucket_priority("references")


def test_score_item_boosts_request_overlap() -> None:
    """Deviation: ranking ignores request tokens (Mako packet useless)."""
    high = score_item(
        request="onboarding role check",
        path="src/Api.java",
        text='@GetMapping("/api/onboarding")',
        bucket="api_surface",
        contested=False,
    )
    low = score_item(
        request="onboarding role check",
        path="src/Other.java",
        text="unrelated",
        bucket="references",
        contested=False,
    )
    assert high > low


def test_trim_to_budget_respects_token_proxy() -> None:
    """Deviation: budgetTokens ignored — unbounded primaryContext."""
    items = [
        {
            "path": f"f{i}.java",
            "match": f"hit-{i}",
            "score": 1.0 - i * 0.01,
            "provider": "evidence",
            "reason": "stage-0",
            "bucket": "security",
            "payload": {"blob": "y" * 5000},
        }
        for i in range(20)
    ]
    kept, truncated, used = trim_to_budget(items, budget_tokens=50)
    assert truncated is True
    assert len(kept) < 20
    assert used <= 50 or (len(kept) == 1 and truncated)
    # Emission must be row_ref-shaped (Option A), not fat payload.
    assert all("row_ref" in k and "payload" not in k for k in kept)
    assert used == sum(estimate_tokens(k) for k in kept)


def test_context_packet_budget_trims_primary(tmp_path: Path) -> None:
    run = _write_run_dir(tmp_path)
    pkt = run_context_packet("onboarding", run_dir=run, budget_tokens=80)
    assert pkt["truncated"] is True or pkt["tokensUsed"] <= 80
    assert len(pkt["primaryContext"]) + len(pkt["relatedContext"]) <= 15


def test_context_packet_hints_always_present(tmp_path: Path) -> None:
    run = _write_run_dir(tmp_path)
    pkt = run_context_packet("zzz-no-match-xyz", run_dir=run, budget_tokens=4000)
    assert isinstance(pkt["_hints"], list)
    assert len(pkt["_hints"]) >= 1


def test_context_packet_corrupt_signals_fail_closed(tmp_path: Path) -> None:
    run = tmp_path / "run"
    run.mkdir()
    (run / "spring_signals.json").write_text("{bad", encoding="utf-8")
    with pytest.raises(QueryError):
        run_context_packet("x", run_dir=run)


def test_cli_context_packet(tmp_path: Path) -> None:
    run = _write_run_dir(tmp_path)
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "doc_engine.tools.query_artifacts",
            "context-packet",
            "--run-dir",
            str(run),
            "--request",
            "onboarding",
            "--budget-tokens",
            "2000",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["kind"] == "context-packet"


def test_mcp_dispatch_context_packet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from doc_engine.query.mcp_tools import dispatch_tool

    run = _write_run_dir(tmp_path)
    monkeypatch.setenv("DOC_ENGINE_ROOT", str(tmp_path))
    out = dispatch_tool(
        "context_packet",
        {"request": "onboarding", "run_dir": str(run), "budget_tokens": 2000},
    )
    assert out["kind"] == "context-packet"


def test_envelope_schema_check_context_packet(tmp_path: Path) -> None:
    from doc_engine.query.schema_check import validate_envelope

    run = _write_run_dir(tmp_path)
    pkt = run_context_packet("onboarding", run_dir=run, budget_tokens=2000)
    validate_envelope("context_packet", pkt)
