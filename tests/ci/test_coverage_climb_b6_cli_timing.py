"""Coverage climb B6: cli_scan_config + suite_timing leftover edges.

Q2 adequacy witness: mutmut_slice on doc_engine.cli_scan_config and
doc_engine.ci.suite_timing.* — asserts bite optional flag True branches,
classname::name junit ids, junit-present render path, and OTHER plateau.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest

from doc_engine import cli_scan_config as csc
from doc_engine.ci.suite_timing.duration_records import SuiteTimingReport
from doc_engine.ci.suite_timing.github_timing_summary import (
    format_timing_markdown,
    render_from_junit,
)
from doc_engine.ci.suite_timing.junit_duration_parse import (
    _testcase_node_id,
    parse_junit_durations,
)
from doc_engine.ci.suite_timing.plateau_buckets import (
    OTHER_BUCKET,
    plateau_label_for,
    plateau_totals_seconds,
)
from doc_engine.config import Config

pytestmark = pytest.mark.domain_climb_sensor


def test_split_and_optional_scan_flags() -> None:
    assert csc.split_scanner_names(" a, ,b ,c ") == ["a", "b", "c"]
    assert csc.split_scanner_names("") == []

    overrides: dict = {}
    csc.apply_optional_scan_flags(
        SimpleNamespace(respect_gitignore=False, build_command=None, db_path=None),
        overrides,
    )
    assert overrides == {}

    csc.apply_optional_scan_flags(
        SimpleNamespace(
            respect_gitignore=True,
            build_command="mvn -q",
            db_path="/tmp/db",
        ),
        overrides,
    )
    assert overrides["respect_gitignore"] is True
    assert overrides["build_command"] == "mvn -q"
    assert overrides["db_path"] == "/tmp/db"


def test_scan_cli_overrides_and_scan_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    empty = csc.scan_cli_overrides(
        SimpleNamespace(
            scanners=None,
            sql_dialect="ansi",
            respect_gitignore=False,
            build_command=None,
            db_path=None,
        )
    )
    assert empty == {}

    full = csc.scan_cli_overrides(
        SimpleNamespace(
            scanners="filesystem,codeql",
            sql_dialect="postgres",
            respect_gitignore=True,
            build_command="gradle",
            db_path="db",
        )
    )
    assert full["scanners"] == ["filesystem", "codeql"]
    assert full["sql_dialect"] == "postgres"
    assert full["respect_gitignore"] is True

    monkeypatch.setattr(csc, "load_repo_config", lambda _repo: None)
    monkeypatch.setattr(csc, "sanitize_repo_settings", lambda cfg, _trust: cfg)
    monkeypatch.setattr(
        csc, "merge_config", lambda base, overrides: SimpleNamespace(base=base, **overrides)
    )
    args = argparse.Namespace(
        scanners="filesystem",
        sql_dialect="ansi",
        respect_gitignore=False,
        build_command=None,
        db_path=None,
        trust_repo_config=False,
    )
    cfg = csc.scan_config(str(tmp_path), args)
    assert isinstance(cfg.base, Config)
    assert cfg.scanners == ["filesystem"]


def test_junit_both_names_and_render_present(tmp_path: Path) -> None:
    element = mock.Mock()
    element.attrib = {"classname": "tests.ci.test_x", "name": "test_y", "time": "0.5"}
    assert _testcase_node_id(element) == "tests.ci.test_x::test_y"

    junit = tmp_path / "junit.xml"
    junit.write_text(
        '<?xml version="1.0"?><testsuite>'
        '<testcase classname="tests.ci.test_gate_tools" name="test_a" time="1.25"/>'
        '<testcase classname="tests.other.test_z" name="test_b" time="0.5"/>'
        "</testsuite>\n",
        encoding="utf-8",
    )
    report = parse_junit_durations(junit)
    assert any("::" in row.node_id for row in report.records)

    cov = tmp_path / "coverage.xml"
    cov.write_text('<coverage line-rate="1"/>', encoding="utf-8")
    # Happy path: junit present → format_timing_markdown (lines 70-71).
    text = render_from_junit(junit, coverage_xml=cov, top_n=2)
    assert "Total recorded test time" in text
    assert "1.250s" in text
    assert "gate_tools" in text or "other" in text.lower() or "Plateau" in text

    totals = plateau_totals_seconds(report.records)
    assert totals[OTHER_BUCKET] >= 0.0
    assert plateau_label_for("tests/ci/test_unrelated.py::test_x") == OTHER_BUCKET
    assert plateau_label_for("tests.ci.test_gate_tools.Test::t") == "gate_tools"

    empty_md = format_timing_markdown(
        SuiteTimingReport.from_records([]), top_n=1, coverage_xml=cov
    )
    assert "No junit testcase durations found" in empty_md
