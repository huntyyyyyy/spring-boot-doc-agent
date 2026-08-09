"""Tests for GitHub step-summary append (path validation + append semantics)."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci.github_step_summary import append_markdown
from doc_engine.paths import PathValidationError

pytestmark = pytest.mark.domain_ci_meta


def test_append_markdown_creates_file(tmp_path: Path) -> None:
    target = tmp_path / "summary.md"
    append_markdown("### first\n", target)
    assert target.read_text(encoding="utf-8") == "### first\n"


def test_append_markdown_adds_newline_when_missing(tmp_path: Path) -> None:
    target = tmp_path / "summary.md"
    target.write_text("prior", encoding="utf-8")
    append_markdown("### next\n", target)
    assert target.read_text(encoding="utf-8") == "prior\n### next\n"


def test_append_markdown_rejects_dotdot(tmp_path: Path) -> None:
    bad = tmp_path / ".." / "escape.md"
    with pytest.raises(PathValidationError, match=r"\.\."):
        append_markdown("x", bad)


def test_append_markdown_cli_rejects_dotdot(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from doc_engine.ci.github_step_summary import append_markdown_cli

    bad = tmp_path / ".." / "escape.md"
    assert append_markdown_cli("x", bad, ok_message="ok") == 1
    assert "error:" in capsys.readouterr().err
