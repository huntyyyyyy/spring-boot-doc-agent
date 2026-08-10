"""Scan/report/CLI coverage for ``doc_engine.ci.vacuity``."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.ci.vacuity import __main__ as vacuity_main
from doc_engine.ci.vacuity.astgrep_engine import VacuityHit
from doc_engine.ci.vacuity.ripgrep_triage import RgTriageHit
from doc_engine.ci.vacuity.scan import VacuityReport, format_report, scan_vacuity
from doc_engine.ci.vacuity import scan as scan_mod
from doc_engine.ci.vacuity.telemetry_ledger import TelemetryVacuity

pytestmark = pytest.mark.domain_ci_meta


def test_format_report_ok_and_fail() -> None:
    ok = VacuityReport(structural=(), telemetry=(), triage=(), ledger=None)
    assert format_report(ok) == "vacuity gate: OK"

    fail = VacuityReport(
        structural=(VacuityHit("vacuous__assert_true", "a.py", 1, "assert True"),),
        telemetry=(TelemetryVacuity("suite", "s.log", 0),),
        triage=(RgTriageHit("rg_triage__pass_only_line", "b.py", 2, "pass"),),
        ledger=Path("/tmp/ledger.jsonl"),
    )
    text = format_report(fail)
    assert text.startswith("vacuity gate: FAIL")
    assert "[vacuous__assert_true]" in text
    assert "[telemetry__empty_hard_log]" in text
    assert "rg triage candidates (learning only): 1" in text
    assert "ledger:" in text


def test_git_sha_success_and_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def ok_run(*_args, **_kwargs):
        return SimpleNamespace(returncode=0, stdout="abc123\n", stderr="")

    monkeypatch.setattr(scan_mod.subprocess, "run", ok_run)
    assert scan_mod._git_sha(tmp_path) == "abc123"

    def fail_run(*_args, **_kwargs):
        return SimpleNamespace(returncode=1, stdout="", stderr="err")

    monkeypatch.setattr(scan_mod.subprocess, "run", fail_run)
    assert scan_mod._git_sha(tmp_path) == "unknown"

    def blank_run(*_args, **_kwargs):
        return SimpleNamespace(returncode=0, stdout="   ", stderr="")

    monkeypatch.setattr(scan_mod.subprocess, "run", blank_run)
    assert scan_mod._git_sha(tmp_path) == "unknown"


def test_dedupe_structural_hits() -> None:
    hit_a = VacuityHit("r", "a.py", 1, "x")
    hit_b = VacuityHit("r", "a.py", 1, "y")
    hit_c = VacuityHit("r", "b.py", 1, "z")
    assert scan_mod._dedupe([hit_a, hit_b, hit_c]) == (hit_a, hit_c)


def test_scan_writes_ledger_when_findings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "tests" / "ci").mkdir(parents=True)
    monkeypatch.setattr(
        scan_mod,
        "run_astgrep_vacuity",
        lambda *_a, **_k: [VacuityHit("vacuous__x", "a.py", 1, "x")],
    )
    monkeypatch.setattr(scan_mod, "run_vacuous_engine", lambda *_a, **_k: [])
    monkeypatch.setattr(scan_mod, "run_rg_triage", lambda *_a, **_k: [])
    monkeypatch.setattr(scan_mod, "scan_latest_telemetry_empties", lambda *_a: [])
    monkeypatch.setattr(scan_mod, "_git_sha", lambda _repo: "sha")
    report = scan_vacuity(tmp_path, ("tests/ci",), write_ledger=True)
    assert not report.ok
    assert report.ledger is not None
    assert report.ledger.is_file()


def test_main_cli_no_ledger(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    (tmp_path / "tests" / "ci").mkdir(parents=True)
    (tmp_path / "tests" / "ci" / "test_ok.py").write_text(
        "def test_real():\n    assert 1 + 1 == 2\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(scan_mod, "run_vacuous_engine", lambda *_a, **_k: [])
    monkeypatch.setattr(scan_mod, "run_rg_triage", lambda *_a, **_k: [])
    monkeypatch.setattr(scan_mod, "scan_latest_telemetry_empties", lambda *_a: [])
    monkeypatch.setattr(
        scan_mod,
        "run_astgrep_vacuity",
        lambda *_a, **_k: [],
    )
    code = vacuity_main.main(
        ["--root", str(tmp_path), "--roots", "tests/ci", "--no-ledger"]
    )
    assert code == 0
    assert "vacuity gate: OK" in capsys.readouterr().out


def test_main_cli_fail_exit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        vacuity_main,
        "scan_vacuity",
        lambda *_a, **_k: VacuityReport(
            structural=(VacuityHit("vacuous__x", "a.py", 1, "x"),),
            telemetry=(),
            triage=(),
            ledger=None,
        ),
    )
    code = vacuity_main.main(["--root", str(tmp_path), "--no-ledger"])
    assert code == 1
    assert "FAIL" in capsys.readouterr().out


def test_main_defaults_repo_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(vacuity_main, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(
        vacuity_main,
        "scan_vacuity",
        lambda root, roots, write_ledger: VacuityReport(
            structural=(), telemetry=(), triage=(), ledger=None
        ),
    )
    assert vacuity_main.main(["--no-ledger"]) == 0


def test_module_entrypoint_system_exit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["doc_engine.ci.vacuity", "--root", str(tmp_path), "--no-ledger"],
    )
    monkeypatch.setattr(
        "doc_engine.ci.vacuity.scan.scan_vacuity",
        lambda *_a, **_k: VacuityReport(
            structural=(), telemetry=(), triage=(), ledger=None
        ),
    )
    sys.modules.pop("doc_engine.ci.vacuity.__main__", None)
    with pytest.raises(SystemExit) as raised:
        runpy.run_module("doc_engine.ci.vacuity", run_name="__main__")
    assert raised.value.code == 0
