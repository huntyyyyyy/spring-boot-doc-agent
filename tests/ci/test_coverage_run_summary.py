"""Coverage for scripts/ci/coverage_run_summary.py."""

from __future__ import annotations

from pathlib import Path

import coverage_run_summary as summary
import pytest

pytestmark = pytest.mark.domain_ci_meta


def _minimal_coverage_xml(path: Path, line_rate: str = "0.987") -> None:
    path.write_text(
        f'<coverage line-rate="{line_rate}" branch-rate="0.9" '
        f'version="7" timestamp="1"></coverage>\n',
        encoding="utf-8",
    )


def test_print_line_rate_ok(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    xml_path = tmp_path / "coverage.xml"
    _minimal_coverage_xml(xml_path)
    assert summary.print_line_rate(xml_path) == 0
    assert "98.70%" in capsys.readouterr().out


def test_print_line_rate_missing(tmp_path: Path) -> None:
    assert summary.print_line_rate(tmp_path / "missing.xml") == 1


def test_github_summary_writes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    xml_path = tmp_path / "coverage.xml"
    _minimal_coverage_xml(xml_path)
    out = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(out))
    monkeypatch.setenv("PYTHON_VERSION", "3.11")
    monkeypatch.setenv("COV_FAIL_UNDER", "98.7")
    assert summary.main(["--coverage-xml", str(xml_path), "--github-summary"]) == 0
    assert "98.70%" in out.read_text(encoding="utf-8")


def test_github_summary_missing_xml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(out))
    rc = summary.main(
        ["--coverage-xml", str(tmp_path / "nope.xml"), "--github-summary"]
    )
    assert rc == 0
    assert "missing" in out.read_text(encoding="utf-8")
