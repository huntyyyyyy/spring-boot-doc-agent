"""Coverage climb B4: run_manifest helpers (git/stage/interview/preflight).

Q2 witness: mutmut_slice on doc_engine.tools.run_manifest (not Arm-1).
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from doc_engine.tools import run_manifest as rm

pytestmark = pytest.mark.domain_climb_sensor


def test_write_json_cleanup_and_git_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "m.json"
    monkeypatch.setattr(rm.os, "replace", MagicMock(side_effect=OSError("boom")))
    with pytest.raises(OSError):
        rm._write_json_atomic(str(path), {"a": 1})
    assert list(tmp_path.iterdir()) == []

    monkeypatch.setattr(rm.os, "replace", MagicMock(side_effect=OSError("boom2")))
    monkeypatch.setattr(rm.os, "remove", MagicMock(side_effect=OSError("gone")))
    with pytest.raises(OSError):
        rm._write_json_atomic(str(path), {"b": 2})

    monkeypatch.setattr(
        rm.subprocess,
        "run",
        MagicMock(side_effect=rm.subprocess.TimeoutExpired(cmd="git", timeout=1)),
    )
    assert rm._run_git(str(tmp_path), ["rev-parse", "HEAD"], "rev-parse HEAD") is None
    assert "could not run" in capsys.readouterr().err

    monkeypatch.setattr(
        rm.subprocess,
        "run",
        MagicMock(return_value=SimpleNamespace(returncode=1, stdout="", stderr="nope")),
    )
    assert rm._run_git(str(tmp_path), ["status"], "status") is None
    assert "failed" in capsys.readouterr().err


def test_stage_end_finalize_infer_and_cancel() -> None:
    m = {"stages": []}
    rm.start_stage(m, "scan", fanout=2, now_ms=1000)
    rm.end_stage(m, "scan", "complete", now_ms=1500)
    assert m["stages"][0]["duration_ms"] == 500
    assert m["stages"][0]["actual_fanout"] == 2

    with pytest.raises(ValueError, match="unknown end-stage"):
        rm.end_stage(m, "scan", "bogus", now_ms=1600)
    with pytest.raises(ValueError, match="no running stage"):
        rm.end_stage(m, "scan", "complete", now_ms=1600)

    m2 = {"stages": []}
    rm.start_stage(m2, "docs", now_ms=10)
    warnings = rm._cancel_running_stages(m2, now_ms=20)
    assert m2["stages"][0]["status"] == "canceled"
    assert "docs" in warnings[0]
    assert rm._infer_finalize_status(m2) == "partial"

    m3 = {
        "stages": [
            {"name": "a", "status": "failed"},
            {"name": "b", "status": "complete"},
        ]
    }
    assert rm._infer_finalize_status(m3) == "failed"
    m4 = {"stages": [{"name": "a", "status": "complete"}]}
    assert rm._infer_finalize_status(m4) == "complete"


def test_load_file_signatures_sources(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    assert rm.load_file_signatures() == {}
    sig_path = tmp_path / "signals.json"
    sig_path.write_text(
        json.dumps({"file_signatures": {"a.java": "sha"}}), encoding="utf-8"
    )
    assert rm.load_file_signatures(signals_file=str(sig_path)) == {"a.java": "sha"}

    java = tmp_path / "b.java"
    java.write_text("class B {}", encoding="utf-8")

    def fake_walk(_repo: str):
        yield str(java)
        yield str(tmp_path / "missing.java")

    monkeypatch.setattr(rm, "dfs_walk", fake_walk)

    def fake_sig(path: str) -> str:
        if path.endswith("missing.java"):
            raise OSError("gone")
        return "sig"

    monkeypatch.setattr(rm, "compute_file_signature", fake_sig)
    assert rm.load_file_signatures(repo_path=str(tmp_path))["b.java"] == "sig"
    assert "could not read" in capsys.readouterr().err


def test_compute_evidence_tag_counts(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "readme.md").write_text(
        "X [Evidenced — a.java:1]. Y [Confirmed — interview, 2026-07-23].",
        encoding="utf-8",
    )
    tags = rm.compute_evidence_tag_counts(str(docs))
    assert tags["readme.md"]["Evidenced"] == 1
    assert tags["readme.md"]["Confirmed"] == 1


def test_parse_interview_file_statuses(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    interview = tmp_path / "interview.json"
    interview.write_text(
        json.dumps(
            [
                {"id": "q1", "status": "answered"},
                {"id": "q2", "status": "skipped"},
                {"id": "q3", "status": "weird"},
                {"no": "keys"},
            ]
        ),
        encoding="utf-8",
    )
    parsed = rm.parse_interview_file(str(interview))
    assert parsed["asked"] == 3
    assert parsed["answered"] == 1
    assert parsed["skipped"] == 1
    err = capsys.readouterr().err
    assert "unrecognized status" in err
    assert "missing required" in err
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    assert rm.parse_interview_file(str(bad))["asked"] == 0


def test_capacity_preflight_tie_in(tmp_path: Path) -> None:
    preflight = tmp_path / "preflight.json"
    preflight.write_text(
        json.dumps(
            {
                "total_fanout": 5,
                "stage_fanout": {
                    "stage1_file_summarizer": 3,
                    "unknown_stage_key": 2,
                },
            }
        ),
        encoding="utf-8",
    )
    tie = rm.compute_capacity_preflight_tie_in(str(preflight))
    assert tie is not None
    assert tie["total_predicted_fanout"] == 5
    assert "unknown_stage_key" in tie["unmapped_preflight_keys"]
    assert rm.compute_capacity_preflight_tie_in(str(tmp_path / "gone.json")) is None
