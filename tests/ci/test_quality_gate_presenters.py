"""Tests for quality-gates presenters + Actions log groups (E-UX1)."""

from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

from doc_engine.ci import quality_gate_checks as checks
from doc_engine.ci.quality_gate_presenters import (
    begin_grouped_run,
    end_grouped_run,
    format_gates_markdown,
    format_gates_text,
    publish_gates_summary,
)

pytestmark = pytest.mark.domain_ci_meta


def test_format_gates_text_marks_fail_and_skip() -> None:
    planned = ["import-cycles", "size-ratchet", "duplication"]
    results = [("import-cycles", 0), ("size-ratchet", 1)]
    text = format_gates_text(planned, results)
    assert "- import-cycles: PASS" in text
    assert "- size-ratchet: FAIL (exit 1)" in text
    assert "- duplication: SKIPPED (fail-fast)" in text


def test_format_gates_markdown_includes_details_for_skipped() -> None:
    planned = ["a", "b"]
    results = [("a", 2)]
    md = format_gates_markdown(planned, results)
    assert "| `a` | FAIL (exit 2) |" in md
    assert "| `b` | SKIPPED (fail-fast) |" in md
    assert "<details>" in md
    assert "`b`" in md


def test_publish_gates_summary_appends_when_env_set(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    publish_gates_summary(["import-cycles"], [("import-cycles", 0)])
    out = capsys.readouterr().out
    assert "quality-gates summary" in out
    assert "PASS" in out
    body = summary.read_text(encoding="utf-8")
    assert "### Quality gates" in body
    assert "`import-cycles`" in body


def test_run_emits_actions_groups(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "true")

    def fake_subprocess_run(command, **_kwargs):
        return mock.Mock(returncode=0)

    monkeypatch.setattr(checks.subprocess, "run", fake_subprocess_run)
    assert checks._run(["true"], label="demo-gate") == 0
    out = capsys.readouterr().out
    assert "::group::demo-gate" in out
    assert "::endgroup::" in out


def test_begin_end_grouped_run_helpers(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert begin_grouped_run("local", ["echo"]) is False
    end_grouped_run(False)
    assert "::group::" not in capsys.readouterr().out
