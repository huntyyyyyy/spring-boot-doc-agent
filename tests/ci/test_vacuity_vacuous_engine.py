"""Unit coverage for ``doc_engine.ci.vacuity.vacuous_engine``."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.ci.vacuity import vacuous_engine as ve
from doc_engine.ci.vacuity.astgrep_engine import VacuityHit

pytestmark = pytest.mark.domain_ci_meta


def test_missing_vacuous_binary_is_hard_finding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(ve.shutil, "which", lambda _name: None)
    hits = ve.run_vacuous_engine(tmp_path, ("tests/ci",))
    assert hits == [
        VacuityHit(
            "vacuous__tool_missing",
            "vacuous",
            0,
            "vacuous binary not on PATH — pin vacuous in requirements.txt",
        )
    ]


def test_missing_root_directory_skipped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(ve.shutil, "which", lambda _name: "/bin/vacuous")
    assert ve.run_vacuous_engine(tmp_path, ("no/such",)) == []


def test_engine_nonzero_exit_is_hard_finding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "tests" / "ci"
    target.mkdir(parents=True)
    monkeypatch.setattr(ve.shutil, "which", lambda _name: "/bin/vacuous")

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(returncode=3, stdout="", stderr="engine boom")

    monkeypatch.setattr(ve.subprocess, "run", fake_run)
    hits = ve.run_vacuous_engine(tmp_path, ("tests/ci",))
    assert hits[0].rule_id == "vacuous__engine_error"
    assert "engine boom" in hits[0].text


def test_empty_stdout_and_bad_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "tests" / "ci").mkdir(parents=True)
    monkeypatch.setattr(ve.shutil, "which", lambda _name: "/bin/vacuous")

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(
            returncode=0, stdout=getattr(fake_run, "stdout"), stderr=""
        )

    monkeypatch.setattr(ve.subprocess, "run", fake_run)

    fake_run.stdout = "   "
    assert ve.run_vacuous_engine(tmp_path, ("tests/ci",)) == []

    fake_run.stdout = "{not-json"
    bad = ve.run_vacuous_engine(tmp_path, ("tests/ci",))
    assert bad[0].rule_id == "vacuous__engine_error"
    assert "JSON parse failed" in bad[0].text


def test_findings_parse_edges(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "tests" / "ci").mkdir(parents=True)
    monkeypatch.setattr(ve.shutil, "which", lambda _name: "/bin/vacuous")

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(
            returncode=1, stdout=getattr(fake_run, "stdout"), stderr=""
        )

    monkeypatch.setattr(ve.subprocess, "run", fake_run)

    fake_run.stdout = json.dumps({"findings": "nope"})
    assert ve.run_vacuous_engine(tmp_path, ("tests/ci",)) == []

    fake_run.stdout = json.dumps([1, 2, 3])
    assert ve.run_vacuous_engine(tmp_path, ("tests/ci",)) == []

    fake_run.stdout = json.dumps(
        {
            "findings": [
                "skip",
                {
                    "rule": "pass_only",
                    "file": "t.py",
                    "line": 2,
                    "message": "empty body",
                },
                {"file": "u.py", "test": "fallback"},
            ]
        }
    )
    hits = ve.run_vacuous_engine(tmp_path, ("tests/ci",))
    assert hits[0].rule_id == "vacuous_crate__pass_only"
    assert hits[0].text == "empty body"
    assert hits[1].rule_id == "vacuous_crate__unknown"
    assert hits[1].text == "fallback"
