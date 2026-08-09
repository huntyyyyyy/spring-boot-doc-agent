"""Coverage climb B4: run_manifest finalize / format / CLI commands.

Q2 witness: mutmut_slice on doc_engine.tools.run_manifest (not Arm-1).
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.tools import run_manifest as rm

pytestmark = pytest.mark.domain_climb_sensor


def test_format_summary_and_finalize_roundtrip(tmp_path: Path) -> None:
    manifest = rm.build_init_manifest(str(tmp_path), now_ms=1_700_000_000_000)
    rm.start_stage(manifest, "signal_scan", fanout=1, now_ms=1_700_000_000_100)
    rm.end_stage(manifest, "signal_scan", "complete", now_ms=1_700_000_000_200)
    rm.start_stage(manifest, "doc_writer", now_ms=1_700_000_000_300)
    finalized, warnings = rm.finalize_manifest(
        manifest,
        file_signatures={"a.java": "x"},
        evidence_tag_counts={
            "readme.md": {
                "Evidenced": 2,
                "Confirmed": 1,
                "Unknown": 0,
                "PerExistingDocs": 0,
            }
        },
        interview={"asked": 1, "answered": 1, "skipped": 0, "questions": []},
        capacity_preflight={
            "unmapped_preflight_keys": ["x"],
            "predicted_fanout_by_manifest_stage": {"signal_scan": 1},
        },
        now_ms=1_700_000_000_400,
    )
    assert finalized["status"] == "partial"
    assert warnings and "doc_writer" in warnings[0]
    assert finalized["file_signatures"]["a.java"] == "x"
    text = rm.format_summary(finalized)
    assert "run_id=" in text
    assert "signal_scan" in text
    assert "evidence tags" in text
    assert "interview:" in text
    assert "unmapped" in text
    assert "fanout[signal_scan]" in text


def test_cmd_end_finalize_summary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    man_path = tmp_path / "run_manifest.json"
    manifest = {
        "run_id": "rid",
        "status": "running",
        "stages": [
            {
                "name": "scan",
                "status": "running",
                "start_time_ms": 1,
                "end_time_ms": None,
                "duration_ms": None,
                "error": None,
                "actual_fanout": None,
            }
        ],
        "target_repo": {"path": str(tmp_path)},
        "file_signatures": {},
        "evidence_tag_counts": {},
        "interview": None,
        "capacity_preflight": None,
        "timestamp_start": "2023-01-01T00:00:00Z",
        "timestamp_end": None,
    }
    man_path.write_text(json.dumps(manifest), encoding="utf-8")

    rm._cmd_end_stage(
        SimpleNamespace(
            manifest_path=str(man_path),
            stage_name="scan",
            status="complete",
            error=None,
            now_ms=10,
        )
    )
    assert "ended" in capsys.readouterr().out

    with pytest.raises(SystemExit):
        rm._cmd_end_stage(
            SimpleNamespace(
                manifest_path=str(man_path),
                stage_name="missing",
                status="complete",
                error=None,
                now_ms=20,
            )
        )

    sigs = tmp_path / "signals.json"
    sigs.write_text(json.dumps({"file_signatures": {"z.java": "1"}}), encoding="utf-8")
    args = SimpleNamespace(
        manifest_path=str(man_path),
        status=None,
        signals_file=str(sigs),
        docs_dir=None,
        interview_file=None,
        preflight_file=None,
        now_ms=30,
    )
    rm._cmd_finalize(args)
    assert "run_manifest:" in capsys.readouterr().out

    rm._cmd_summary(SimpleNamespace(manifest_path=str(man_path)))
    assert "run_id=" in capsys.readouterr().out

    with pytest.raises(SystemExit):
        rm._cmd_init(
            SimpleNamespace(
                repo_path=str(tmp_path / "nope"),
                out=str(tmp_path / "x.json"),
                now_ms=1,
            )
        )

    # Finalize without --signals-file walks target_repo; warning lines print.
    man2 = tmp_path / "m2.json"
    man2.write_text(
        json.dumps(
            {
                "run_id": "r2",
                "status": "running",
                "stages": [],
                "target_repo": {"path": str(tmp_path)},
                "file_signatures": {},
                "evidence_tag_counts": {},
                "interview": None,
                "capacity_preflight": None,
                "timestamp_start": "2023-01-01T00:00:00Z",
                "timestamp_end": None,
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(rm, "load_file_signatures", lambda **k: {"w.java": "1"})
    rm._cmd_finalize(
        SimpleNamespace(
            manifest_path=str(man2),
            status="complete",
            signals_file=None,
            docs_dir=None,
            interview_file=None,
            preflight_file=None,
            now_ms=40,
        )
    )
    assert "run_manifest:" in capsys.readouterr().out
    assert rm._summary_timestamp_line({"timestamp_start": None}) is None

    not_list = tmp_path / "not_list.json"
    not_list.write_text(json.dumps({"x": 1}), encoding="utf-8")
    assert rm.parse_interview_file(str(not_list))["asked"] == 0
