"""TDD coverage for ``doc_engine.ci.suite_timing`` (E-RUN1 sensors)."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci.suite_timing.duration_records import (
    CaseDuration,
    SuiteTimingReport,
)
from doc_engine.ci.suite_timing.github_timing_summary import (
    append_github_summary,
    format_timing_markdown,
    render_from_junit,
)
from doc_engine.ci.suite_timing.junit_duration_parse import parse_junit_durations
from doc_engine.ci.suite_timing.plateau_buckets import (
    plateau_label_for,
    plateau_totals_seconds,
)
from doc_engine.ci.suite_timing.pre_pytest_cascade import cascade_markdown

pytestmark = pytest.mark.domain_ci_meta


def _write_junit(path: Path, cases: list[tuple[str, str, str]]) -> None:
    rows = "\n".join(
        f'<testcase classname="{classname}" name="{name}" time="{time}"/>'
        for classname, name, time in cases
    )
    path.write_text(
        f'<?xml version="1.0"?><testsuite name="pytest">{rows}</testsuite>\n',
        encoding="utf-8",
    )


def test_parse_junit_sorted_by_duration_descending(tmp_path: Path) -> None:
    junit = tmp_path / "pytest-oracle.junit.xml"
    _write_junit(
        junit,
        [
            ("tests.ci.test_a", "test_fast", "0.10"),
            ("tests.ci.test_b", "test_slow", "2.50"),
            ("tests.ci.test_c", "test_mid", "1.00"),
        ],
    )
    report = parse_junit_durations(junit)
    assert [row.node_id for row in report.records] == [
        "tests.ci.test_b::test_slow",
        "tests.ci.test_c::test_mid",
        "tests.ci.test_a::test_fast",
    ]
    assert report.records[0].duration_seconds == pytest.approx(2.5)
    assert report.total_seconds == pytest.approx(3.6)


def test_plateau_buckets_on_research_path_prefixes() -> None:
    assert (
        plateau_label_for("tests.ci.test_gate_tools.test_foo::test_bar")
        == "gate_tools"
    )
    assert (
        plateau_label_for("tests.ci.test_repo_claims_real_core::test_x")
        == "repo_claims_real"
    )
    assert (
        plateau_label_for("tests/ci/test_run_manifest.py::test_scan")
        == "run_manifest"
    )
    assert plateau_label_for("tests.ci.test_coverage_run_summary::test_y") == "other"


def test_plateau_totals_seconds_aggregate() -> None:
    records = (
        CaseDuration("tests.ci.test_gate_tools.X::a", 1.0),
        CaseDuration("tests.ci.test_gate_tools.X::b", 0.5),
        CaseDuration("tests.ci.test_other::c", 2.0),
    )
    totals = plateau_totals_seconds(records)
    assert totals["gate_tools"] == pytest.approx(1.5)
    assert totals["other"] == pytest.approx(2.0)
    assert totals["repo_claims_real"] == pytest.approx(0.0)
    assert totals["run_manifest"] == pytest.approx(0.0)


def test_cascade_markdown_when_coverage_xml_absent(tmp_path: Path) -> None:
    text = cascade_markdown(coverage_xml=tmp_path / "coverage.xml")
    assert "coverage.xml missing" in text
    assert "ruff" in text
    assert "check_code_quality" in text
    assert "fail_under" in text


def test_cascade_empty_when_coverage_xml_present(tmp_path: Path) -> None:
    coverage = tmp_path / "coverage.xml"
    coverage.write_text('<coverage line-rate="0.99"/>', encoding="utf-8")
    assert cascade_markdown(coverage_xml=coverage) == ""


def test_render_from_junit_missing_and_cascade(tmp_path: Path) -> None:
    missing_junit = tmp_path / "absent.junit.xml"
    missing_cov = tmp_path / "coverage.xml"
    text = render_from_junit(missing_junit, coverage_xml=missing_cov, top_n=3)
    assert "junit xml missing" in text
    assert "Pre-pytest cascade" in text
    assert "ruff" in text


def test_format_timing_empty_report(tmp_path: Path) -> None:
    coverage = tmp_path / "coverage.xml"
    coverage.write_text('<coverage line-rate="0.99"/>', encoding="utf-8")
    markdown = format_timing_markdown(
        SuiteTimingReport.from_records([]), top_n=5, coverage_xml=coverage
    )
    assert "No junit testcase durations found" in markdown


def test_presenter_smoke_no_network(tmp_path: Path) -> None:
    junit = tmp_path / "j.xml"
    _write_junit(
        junit,
        [("tests.ci.test_gate_tools.T", "test_slow", "3.0")],
    )
    coverage = tmp_path / "coverage.xml"
    coverage.write_text('<coverage line-rate="0.99"/>', encoding="utf-8")
    report = SuiteTimingReport.from_records(
        [CaseDuration("tests.ci.test_gate_tools.T::test_slow", 3.0)]
    )
    markdown = format_timing_markdown(
        report, top_n=5, coverage_xml=coverage
    )
    assert "Suite timing" in markdown
    assert "gate_tools" in markdown
    assert "3.000s" in markdown
    rendered = render_from_junit(junit, coverage_xml=coverage, top_n=1)
    assert "test_slow" in rendered
    summary = tmp_path / "summary.md"
    summary.write_text("### prior\n", encoding="utf-8")
    append_github_summary(rendered, summary)
    assert "### prior" in summary.read_text(encoding="utf-8")
    assert "Suite timing" in summary.read_text(encoding="utf-8")
