"""CLI façade coverage for ``scripts/ci/suite_timing_summary.py``."""

from __future__ import annotations

from pathlib import Path

import pytest
import suite_timing_summary as cli

pytestmark = pytest.mark.domain_ci_meta


def test_suite_timing_summary_appends(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    junit = tmp_path / "j.xml"
    junit.write_text(
        '<?xml version="1.0"?><testsuite>'
        '<testcase classname="tests.ci.test_a" name="test_one" time="0.2"/>'
        "</testsuite>\n",
        encoding="utf-8",
    )
    coverage = tmp_path / "coverage.xml"
    coverage.write_text('<coverage line-rate="0.99"/>', encoding="utf-8")
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    assert (
        cli.main(
            [
                "--junit-xml",
                str(junit),
                "--coverage-xml",
                str(coverage),
                "--top-n",
                "5",
                "--github-summary",
            ]
        )
        == 0
    )
    text = summary.read_text(encoding="utf-8")
    assert "Suite timing" in text
    assert "test_one" in text


def test_suite_timing_summary_requires_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    assert cli.main(["--github-summary"]) == 2
