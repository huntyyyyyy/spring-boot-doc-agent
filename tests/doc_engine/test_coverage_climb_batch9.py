"""Coverage climb batch9: build_docs_site CLI + live_gates helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from doc_engine.pipeline import live_gates as lg
from doc_engine.pipeline.compliance import GateRecord
from doc_engine.tools import build_docs_site as bds


def test_build_docs_site_main_missing_and_ok(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "build_docs_site",
            "--docs-dir",
            str(tmp_path / "nope"),
            "--out-dir",
            str(tmp_path / "site"),
        ],
    )
    assert bds.main() == 1
    assert "not found" in capsys.readouterr().err

    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "readme.md").write_text("# hi", encoding="utf-8")
    out = tmp_path / "site"
    monkeypatch.setattr(
        "sys.argv",
        [
            "build_docs_site",
            "--docs-dir",
            str(docs),
            "--out-dir",
            str(out),
            "--site-name",
            "T",
        ],
    )
    monkeypatch.setattr(bds, "_copy_docs", lambda *a, **k: None)
    monkeypatch.setattr(bds, "_write_mkdocs_config", lambda *a, **k: None)
    monkeypatch.setattr(bds, "_run_mkdocs", lambda *a, **k: None)
    assert bds.main() == 0
    assert "site built" in capsys.readouterr().out


def test_live_gates_prior_stages_and_write(tmp_path: Path) -> None:
    assert lg._load_prior_stages(str(tmp_path)) == []
    cert = tmp_path / "certification.json"
    cert.write_text("{not-json", encoding="utf-8")
    assert lg._load_prior_stages(str(tmp_path)) == []
    cert.write_text(
        json.dumps(
            {
                "stages": [
                    {
                        "name": "stage0",
                        "status": "ok",
                        "executor": "deterministic",
                    },
                    {"name": "broken"},
                ]
            }
        ),
        encoding="utf-8",
    )
    rows = lg._load_prior_stages(str(tmp_path))
    assert len(rows) == 1
    assert rows[0].name == "stage0"

    path = lg._write_live_certification(
        out_dir=str(tmp_path),
        repo_path=str(tmp_path),
        gate_records=[
            GateRecord(id="validate_artifacts_all", label="v", status="ok"),
        ],
    )
    assert path.is_file()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data.get("generative_executor") == "live"


def test_record_gate_result_ok_and_fail(
    capsys: pytest.CaptureFixture[str],
) -> None:
    records: list = []
    failures: list[str] = []
    lg._record_gate_result(records, failures, "g1", "Gate One", 0)
    lg._record_gate_result(records, failures, "g2", "Gate Two", 1, "boom\nline2")
    assert records[0].status == "ok"
    assert records[1].status == "fail"
    assert failures == ["Gate Two"]
    assert "FAIL" in capsys.readouterr().err
