"""Unit coverage for ``doc_engine.ci.vacuity.telemetry_ledger``."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from doc_engine.ci.vacuity.astgrep_engine import VacuityHit
from doc_engine.ci.vacuity.ripgrep_triage import RgTriageHit
from doc_engine.ci.vacuity import telemetry_ledger as ledger

pytestmark = pytest.mark.domain_ci_meta


def _write_index(run_dir: Path, suites: list[dict]) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "index.json").write_text(
        json.dumps({"suites": suites}),
        encoding="utf-8",
    )


def test_latest_as_symlink_and_empty_hard_logs(tmp_path: Path) -> None:
    telem = tmp_path / ".git" / "pre-pr-telemetry"
    run_dir = telem / "run-abc"
    empty_log = run_dir / "suite.log"
    nonempty = run_dir / "ok.log"
    _write_index(
        run_dir,
        [
            {"kind": "soft", "name": "softy", "log_relpath": "suite.log"},
            {"kind": "hard", "name": "empty", "log_relpath": "suite.log"},
            {"kind": "hard", "name": "ok", "log_relpath": "ok.log"},
            {"kind": "hard", "log_relpath": "missing.log"},
            "skip-row",
        ],
    )
    empty_log.write_text("", encoding="utf-8")
    nonempty.write_text("passed\n", encoding="utf-8")
    (telem / "latest").symlink_to("run-abc")

    hits = ledger.scan_latest_telemetry_empties(tmp_path)
    names = {hit.suite for hit in hits}
    assert names == {"empty", "missing.log"}
    assert all(hit.bytes == 0 for hit in hits)


def test_latest_as_file_pointer(tmp_path: Path) -> None:
    telem = tmp_path / ".git" / "pre-pr-telemetry"
    run_dir = telem / "run-file"
    _write_index(
        run_dir,
        [{"kind": "hard", "name": "ghost", "log_relpath": "gone.log"}],
    )
    (telem / "latest").write_text("run-file\n", encoding="utf-8")
    hits = ledger.scan_latest_telemetry_empties(tmp_path)
    assert len(hits) == 1
    assert hits[0].suite == "ghost"


def test_no_latest_or_bad_suites_shape(tmp_path: Path) -> None:
    telem = tmp_path / ".git" / "pre-pr-telemetry"
    telem.mkdir(parents=True)
    assert ledger.scan_latest_telemetry_empties(tmp_path) == []

    run_dir = telem / "run-bad"
    run_dir.mkdir(parents=True)
    (run_dir / "index.json").write_text(
        json.dumps({"suites": {"not": "list"}}),
        encoding="utf-8",
    )
    (telem / "latest").write_text("run-bad", encoding="utf-8")
    assert ledger.scan_latest_telemetry_empties(tmp_path) == []


def test_append_ledger_and_summarize_kinds(tmp_path: Path) -> None:
    structural = [
        VacuityHit("vacuous__assert_true", "a.py", 1, "assert True"),
        VacuityHit("vacuous__assert_true", "b.py", 2, "assert True"),
    ]
    telemetry = [
        ledger.TelemetryVacuity("s1", "s1.log", 0),
    ]
    triage = [
        RgTriageHit("rg_triage__pass_only_line", "c.py", 3, "pass"),
    ]
    path = ledger.append_ledger(
        tmp_path,
        git_sha="deadbeef",
        structural=structural,
        telemetry=telemetry,
        triage=triage,
    )
    assert path == ledger.ledger_path(tmp_path)
    record = json.loads(path.read_text(encoding="utf-8").strip())
    assert record["git_sha"] == "deadbeef"
    assert record["kinds"]["vacuous__assert_true"] == 2
    assert record["kinds"]["rg_triage__pass_only_line"] == 1
    assert record["kinds"]["telemetry__empty_hard_log"] == 1

    totals = ledger.summarize_kinds([record, {"kinds": {"vacuous__assert_true": 1}}])
    assert totals["vacuous__assert_true"] == 3
    assert ledger.summarize_kinds([{}]) == {}
