"""coverage_gap_average CLI / markdown / summary suites."""

from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from doc_engine.ci import complexipy_ratchet as ratchet
from doc_engine.ci import coverage_gap_average as cga
from doc_engine.ci import gate_tools
from doc_engine.ci import quality_gates as qg
SAMPLE_WITH_EDGES = """\
<?xml version="1.0" ?>
<coverage line-rate="0.5" branch-rate="0.5" version="7.0" timestamp="1">
  <packages>
    <package name="demo" line-rate="0.5" branch-rate="0.5" complexity="0">
      <classes>
        <class name="skip.py" filename="" line-rate="0" branch-rate="0" complexity="0">
          <lines><line number="1" hits="0"/></lines>
        </class>
        <class name="empty.py" filename="src/empty.py" line-rate="0" branch-rate="0" complexity="0">
          <lines></lines>
        </class>
        <class name="fallback_name.py" line-rate="1" branch-rate="1" complexity="0">
          <lines>
            <line number="1" hits="1"/>
            <line number="2" hits="0" branch="true" condition-coverage="0% (0/2)" missing-branches="1,2"/>
          </lines>
        </class>
        <class name="low.py" filename="src\\\\low.py" line-rate="0" branch-rate="0" complexity="0">
          <lines>
            <line number="1" hits="0"/>
            <line number="2" hits="0"/>
          </lines>
        </class>
      </classes>
    </package>
  </packages>
</coverage>
"""

def test_parse_skips_blank_filename_and_empty_lines(tmp_path: Path) -> None:
    xml = tmp_path / "c.xml"
    # Class with neither filename nor name → skipped (line 95).
    xml.write_text(
        SAMPLE_WITH_EDGES.replace(
            '<class name="skip.py" filename=""',
            '<class filename=""',
        ).replace('src\\\\low.py', 'src/low.py'),
        encoding="utf-8",
    )
    # Append a truly nameless class via ElementTree-built sibling is overkill;
    # empty filename="" still falls through to name= — use raw fragment:
    raw = xml.read_text(encoding="utf-8").replace(
        '<class filename="" line-rate="0" branch-rate="0" complexity="0">',
        '<class line-rate="0" branch-rate="0" complexity="0">',
    )
    xml.write_text(raw, encoding="utf-8")
    rows = cga.parse_file_coverages(xml)
    paths = {r.path for r in rows}
    assert "src/empty.py" not in paths
    assert "" not in paths
    assert "src/low.py" in paths
    assert any(r.branches >= 2 for r in rows)


def test_empty_report_whole_repo_100() -> None:
    report = cga.build_report([], floor=98.7)
    assert report.whole_repo_cover_pct == 100.0
    assert report.below_floor_cover_pct == 100.0


def test_main_success_markdown_and_summary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    xml = tmp_path / "coverage.xml"
    xml.write_text(SAMPLE_WITH_EDGES, encoding="utf-8")
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    # relative path resolution via REPO_ROOT
    monkeypatch.setattr(cga, "REPO_ROOT", tmp_path)
    rc = cga.main(
        [
            "--coverage-xml",
            "coverage.xml",
            "--floor",
            "98.7",
            "--worst",
            "5",
            "--markdown",
            "--append-github-summary",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "Cover%" in out or "gap-average" in out.lower() or "|" in out
    assert summary.is_file()
    assert "below-floor" in summary.read_text(encoding="utf-8").lower() or "Floor" in summary.read_text(encoding="utf-8")


def test_format_markdown_with_below_floor_rows() -> None:
    report = cga.build_report(
        [
            cga.FileCoverage("low.py", 10, 8, 2, 2),
            cga.FileCoverage("mid.py", 10, 3, 0, 0),
        ],
        floor=98.7,
    )
    md = cga.format_markdown(report, worst=2)
    assert "| Cover%" in md
    assert "low.py" in md


def test_coverage_gap_main_module(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    xml = tmp_path / "coverage.xml"
    xml.write_text(SAMPLE_WITH_EDGES.replace("src\\\\low.py", "src/low.py"), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["coverage_gap_average", "--coverage-xml", str(xml)])
    with pytest.raises(SystemExit) as exc:
        runpy.run_module(
            "doc_engine.ci.coverage_gap_average",
            run_name="__main__",
            alter_sys=True,
        )
    assert exc.value.code == 0


def test_append_summary_noop_without_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    cga._append_github_summary("ignored")


def test_report_gap_average_missing_and_present(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(qg, "REPO_ROOT", tmp_path)
    qg._report_gap_average(tmp_path / "missing.xml")  # no-op
    xml = tmp_path / "coverage.xml"
    xml.write_text("<coverage/>", encoding="utf-8")
    called = []
    monkeypatch.setattr(qg, "_run", lambda cmd, label: called.append(cmd) or 0)
    qg._report_gap_average(Path("coverage.xml"))
    assert called and "doc_engine.ci.coverage_gap_average" in called[0]
