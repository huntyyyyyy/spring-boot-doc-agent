"""Unit coverage for ``doc_engine.ci.vacuity.ripgrep_triage``."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.ci.vacuity import ripgrep_triage as triage

pytestmark = pytest.mark.domain_ci_meta


def test_missing_rg_returns_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(triage.shutil, "which", lambda _name: None)
    assert triage.run_rg_triage(tmp_path, ("tests/ci",)) == []


def test_non_directory_roots_skipped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(triage.shutil, "which", lambda _name: "/usr/bin/rg")
    assert triage.run_rg_triage(tmp_path, ("missing",)) == []


def test_rg_nonzero_exit_yields_no_hits_for_pattern(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "tests" / "ci"
    target.mkdir(parents=True)
    monkeypatch.setattr(triage.shutil, "which", lambda _name: "/usr/bin/rg")

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(returncode=2, stdout="x", stderr="err")

    monkeypatch.setattr(triage.subprocess, "run", fake_run)
    assert triage.run_rg_triage(tmp_path, ("tests/ci",)) == []


def test_triage_hits_parse_and_skip_bad_lines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "tests" / "ci"
    target.mkdir(parents=True)
    monkeypatch.setattr(triage.shutil, "which", lambda _name: "/usr/bin/rg")
    call_count = {"n": 0}

    def fake_run(*_args, **_kwargs):
        call_count["n"] += 1
        # First pattern returns mixed good/bad lines; later patterns empty.
        if call_count["n"] == 1:
            stdout = "\n".join(
                [
                    "bad-line",
                    "path.py:notint:text",
                    "path.py:12:  assert True",
                ]
            )
            return SimpleNamespace(returncode=0, stdout=stdout, stderr="")
        return SimpleNamespace(returncode=1, stdout="", stderr="")

    monkeypatch.setattr(triage.subprocess, "run", fake_run)
    hits = triage.run_rg_triage(tmp_path, ("tests/ci",))
    assert len(hits) == 1
    assert hits[0].kind == "rg_triage__assert_true"
    assert hits[0].path == "path.py"
    assert hits[0].line == 12
    assert hits[0].text == "assert True"


def test_parse_rg_line_helpers() -> None:
    assert triage._parse_rg_line("only-two:parts", "k") is None
    assert triage._parse_rg_line("a:x:body", "k") is None
    hit = triage._parse_rg_line("a.py:3:  pass", "rg_triage__pass_only_line")
    assert hit is not None
    assert hit.line == 3
    assert hit.text == "pass"
