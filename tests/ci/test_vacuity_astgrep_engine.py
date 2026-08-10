"""Unit coverage for ``doc_engine.ci.vacuity.astgrep_engine`` parse/error paths."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.ci.vacuity import astgrep_engine as engine

pytestmark = pytest.mark.domain_ci_meta


def test_missing_rules_file_is_hard_finding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    missing = tmp_path / "absent_rules.yml"
    monkeypatch.setattr(engine, "rules_path", lambda _repo=None: missing)
    hits = engine.run_astgrep_vacuity(tmp_path, ("tests/ci",))
    assert hits == [
        engine.VacuityHit(
            "vacuous__missing_rules",
            str(missing),
            0,
            "astgrep_rules.yml missing",
        )
    ]


def test_no_existing_root_dirs_returns_empty(tmp_path: Path) -> None:
    assert engine.run_astgrep_vacuity(tmp_path, ("missing/root",)) == []


def test_astgrep_nonzero_exit_is_hard_finding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "tests" / "ci"
    target.mkdir(parents=True)

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(returncode=2, stdout="", stderr="boom")

    monkeypatch.setattr(engine.subprocess, "run", fake_run)
    hits = engine.run_astgrep_vacuity(tmp_path, ("tests/ci",))
    assert hits[0].rule_id == "vacuous__astgrep_error"
    assert "boom" in hits[0].text


def test_empty_stdout_yields_no_hits(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "tests" / "ci").mkdir(parents=True)

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(returncode=0, stdout="  \n", stderr="")

    monkeypatch.setattr(engine.subprocess, "run", fake_run)
    assert engine.run_astgrep_vacuity(tmp_path, ("tests/ci",)) == []


def test_compact_json_list_and_dict_payloads(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "tests" / "ci").mkdir(parents=True)
    list_payload = [
        {
            "ruleId": "vacuous__assert_true",
            "file": "a.py",
            "range": {"start": {"line": 3}},
            "text": "assert True",
        },
        "skip-me",
    ]
    dict_payload = {
        "id": "from-id",
        "path": "b.py",
        "line": 9,
        "lines": "pass",
    }

    def fake_run(*_args, **_kwargs):
        stdout = getattr(fake_run, "stdout")
        return SimpleNamespace(returncode=0, stdout=stdout, stderr="")

    fake_run.stdout = json.dumps(list_payload)
    monkeypatch.setattr(engine.subprocess, "run", fake_run)
    list_hits = engine.run_astgrep_vacuity(tmp_path, ("tests/ci",))
    assert list_hits[0].line == 4
    assert list_hits[0].rule_id == "vacuous__assert_true"

    fake_run.stdout = json.dumps(dict_payload)
    dict_hits = engine.run_astgrep_vacuity(tmp_path, ("tests/ci",))
    assert dict_hits[0].rule_id == "from-id"
    assert dict_hits[0].path == "b.py"
    assert dict_hits[0].line == 9


def test_non_object_json_payload_and_ndjson_and_bad_lines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "tests" / "ci").mkdir(parents=True)

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(
            returncode=0, stdout=getattr(fake_run, "stdout"), stderr=""
        )

    monkeypatch.setattr(engine.subprocess, "run", fake_run)

    fake_run.stdout = "42"
    assert engine.run_astgrep_vacuity(tmp_path, ("tests/ci",)) == []

    ndjson = "\n".join(
        [
            "not-json",
            "",  # middle blank → _load_json_object empty-line branch
            json.dumps([1, 2]),
            json.dumps(
                {
                    "ruleId": "vacuous__ndjson",
                    "file": "c.py",
                    "range": "bad",
                    "text": "x",
                }
            ),
            json.dumps(
                {
                    "ruleId": "vacuous__ndjson2",
                    "file": "d.py",
                    "range": {"start": "bad"},
                    "text": "y",
                }
            ),
        ]
    )
    fake_run.stdout = ndjson
    hits = engine.run_astgrep_vacuity(tmp_path, ("tests/ci",))
    assert {hit.rule_id for hit in hits} == {
        "vacuous__ndjson",
        "vacuous__ndjson2",
    }
    assert all(hit.line == 0 for hit in hits)


def test_rules_path_defaults_to_package_yaml() -> None:
    path = engine.rules_path()
    assert path.name == "astgrep_rules.yml"
    assert path.is_file()


def test_load_json_object_empty_and_non_dict() -> None:
    assert engine._load_json_object("") is None
    assert engine._load_json_object("[]") is None
    assert engine._load_json_object("{") is None
    row = engine._load_json_object('{"ruleId": "r"}')
    assert row == {"ruleId": "r"}


def test_astgrep_error_uses_stdout_when_stderr_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "tests" / "ci").mkdir(parents=True)

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(returncode=99, stdout="from-stdout", stderr="")

    monkeypatch.setattr(engine.subprocess, "run", fake_run)
    hits = engine.run_astgrep_vacuity(tmp_path, ("tests/ci",))
    assert hits[0].text == "from-stdout"
