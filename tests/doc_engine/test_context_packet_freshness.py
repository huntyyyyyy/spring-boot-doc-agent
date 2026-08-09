"""Cohesive suite from tests/doc_engine/test_context_packet.py: test_signature_freshness_stale_on_mismatch, test_assume_indexed_when_no_repo, test_missing_signatures_unknown, test_packet_with_repo_marks_stale, test_mcp_path_escape_refused, test_mcp_help_lists_tools, test_fake_provider_strategy, test_mcp_stdio_initialize_roundtrip."""

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

def test_signature_freshness_stale_on_mismatch(tmp_path: Path) -> None:
    """Deviation: signature mismatch labeled fresh_indexed."""
    repo = tmp_path / "repo"
    repo.mkdir()
    f = repo / "src"
    f.mkdir()
    target = f / "Sec.java"
    target.write_text("class Sec {}", encoding="utf-8")
    from doc_engine.core.walk import compute_file_signature

    good = compute_file_signature(str(target))
    policy = SignatureFreshness(
        repo_root=repo,
        signatures={"src/Sec.java": "deadbeef"},
    )
    assert label_item_path(policy, "src/Sec.java") == "stale"
    policy_ok = SignatureFreshness(repo_root=repo, signatures={"src/Sec.java": good})
    assert label_item_path(policy_ok, "src/Sec.java") == "fresh_indexed"


def test_assume_indexed_when_no_repo() -> None:
    assert label_item_path(AssumeIndexed(), "src/X.java") == "unknown"


def test_missing_signatures_unknown(tmp_path: Path) -> None:
    """Deviation: missing file_signatures crashes instead of unknown."""
    run = _write_run_dir(tmp_path, signatures=None)
    # empty dict → unknown for paths not live-hashed
    pkt = run_context_packet(
        "security",
        run_dir=run,
        budget_tokens=4000,
        repo_path=None,
    )
    # without repo_path, freshness defaults to unknown via AssumeIndexed
    assert pkt["primaryContext"]
    for item in pkt["primaryContext"]:
        assert item.get("freshness") == "unknown"


def test_packet_with_repo_marks_stale(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "Sec.java").write_text("class Sec {}", encoding="utf-8")
    (repo / "src" / "Api.java").write_text("class Api {}", encoding="utf-8")
    (repo / "src" / "User.java").write_text("class User {}", encoding="utf-8")
    run = _write_run_dir(tmp_path, signatures={"src/Sec.java": "deadbeef", "src/Api.java": "deadbeef"})
    pkt = run_context_packet(
        "security PreAuthorize",
        run_dir=run,
        budget_tokens=4000,
        repo_path=repo,
    )
    freshes = {i.get("path"): i.get("freshness") for i in pkt["primaryContext"] + pkt["relatedContext"]}
    if "src/Sec.java" in freshes:
        assert freshes["src/Sec.java"] == "stale"


def test_mcp_path_escape_refused(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from doc_engine.query.mcp_tools import dispatch_tool

    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside.json"
    outside.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("DOC_ENGINE_ROOT", str(root))
    with pytest.raises((QueryPathError, QueryMissingError, QueryError)):
        dispatch_tool(
            "query_evidence",
            {"signals": str(outside), "bucket": "security"},
        )


def test_mcp_help_lists_tools() -> None:
    from doc_engine.query.mcp_tools import dispatch_tool

    out = dispatch_tool("doc_engine_help", {})
    assert "context_packet" in out["tools"]


def test_fake_provider_strategy(tmp_path: Path) -> None:
    """Deviation: composer ignores PacketProvider strategies (E4-T2)."""

    class FakeProvider:
        name = "fake"

        def provide(self, request, *, signals, facts_rows, run_dir, limit):
            return [
                {
                    "provider": "fake",
                    "path": "src/Fake.java",
                    "line": 1,
                    "match": request,
                    "bucket": "security",
                    "reason": "fake",
                    "payload": {},
                    "contested": False,
                }
            ]

    run = _write_run_dir(tmp_path)
    pkt = run_context_packet(
        "whatever",
        run_dir=run,
        budget_tokens=4000,
        providers=[FakeProvider()],
    )
    assert pkt["providersUsed"] == ["fake"]
    assert any(i.get("path") == "src/Fake.java" for i in pkt["primaryContext"])


def test_mcp_stdio_initialize_roundtrip() -> None:
    from adapters.mcp.server import handle_message

    resp = handle_message({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    assert resp is not None
    assert resp["result"]["serverInfo"]["name"] == "doc-engine-query"
