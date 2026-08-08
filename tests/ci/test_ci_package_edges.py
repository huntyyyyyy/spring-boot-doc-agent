"""Edge coverage for ``doc_engine.ci`` helpers still below the floor."""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from doc_engine.ci import coverage_gap_average as cga
from doc_engine.ci import gate_tools
from doc_engine.ci import quality_gates as qg


def test_parse_condition_coverage_edges() -> None:
    assert cga._parse_condition_coverage(None) == (0, 0)
    assert cga._parse_condition_coverage("no-paren") == (0, 0)
    assert cga._parse_condition_coverage("50% (1/2)") == (1, 2)
    assert cga._parse_condition_coverage("bad (x/y)") == (0, 0)


def test_file_coverage_empty_measurable() -> None:
    row = cga.FileCoverage("x.py", 0, 0, 0, 0)
    assert row.measurable == 0
    assert row.cover_pct == 100.0


def test_format_text_and_markdown_when_all_green() -> None:
    rows = [
        cga.FileCoverage("src/a.py", 10, 0, 2, 0),
    ]
    report = cga.build_report(rows, floor=50.0)
    text = cga.format_text(report, worst=5)
    assert "none — every measured file meets the floor" in text
    md = cga.format_markdown(report, worst=5)
    assert "Every measured file meets the floor" in md


def test_main_missing_and_bad_xml(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert cga.main(["--coverage-xml", str(tmp_path / "missing.xml")]) == 2
    assert "missing coverage report" in capsys.readouterr().err
    bad = tmp_path / "bad.xml"
    bad.write_text("<not-coverage>", encoding="utf-8")
    # empty classes → parse succeeds with zero files OR parse error
    # force ParseError:
    bad.write_text("<<<", encoding="utf-8")
    assert cga.main(["--coverage-xml", str(bad)]) == 2


def test_append_github_summary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    cga._append_github_summary("hello")
    assert "hello" in summary.read_text(encoding="utf-8")


def test_validate_git_rev_rejects_unsafe() -> None:
    with pytest.raises(SystemExit):
        gate_tools.validate_git_rev("-evil")
    with pytest.raises(SystemExit):
        gate_tools.validate_git_rev("foo;rm")
    assert gate_tools.validate_git_rev("origin/main") == "origin/main"


def test_checked_path_rejects_dotdot(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(gate_tools, "REPO_ROOT", tmp_path)
    with pytest.raises(SystemExit):
        gate_tools.checked_path_under_repo(Path("../outside"))


def test_require_on_path_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(gate_tools.shutil, "which", lambda _n: None)
    monkeypatch.setattr(gate_tools.Path, "is_file", lambda self: False)
    with pytest.raises(SystemExit):
        gate_tools.require_on_path("definitely-missing-tool-xyz")


def test_jscpd_command_prefers_wrapper(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(gate_tools, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(gate_tools, "_jscpd_native_candidates", lambda: [])
    wrapper = tmp_path / "node_modules" / "jscpd" / "run-jscpd.js"
    wrapper.parent.mkdir(parents=True)
    wrapper.write_text("//", encoding="utf-8")
    monkeypatch.setattr(gate_tools, "require_on_path", lambda name: f"/bin/{name}")
    cmd = gate_tools.jscpd_command("--threshold=3")
    assert cmd[0] == "/bin/node"
    assert str(wrapper) in cmd[1]


def test_resolve_compare_ref_requires_explicit() -> None:
    with pytest.raises(SystemExit):
        qg.resolve_compare_ref(None)
    assert qg.resolve_compare_ref("HEAD~1") == "HEAD~1"


def test_gate_new_code_coverage_missing_xml(tmp_path: Path) -> None:
    assert qg.gate_new_code_coverage("origin/main", tmp_path / "no.xml") == 2


def test_gate_duplication_skip_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(qg, "changed_python_under_packages", lambda _ref: [])
    assert qg.gate_duplication("origin/main") == 0
    monkeypatch.setattr(
        qg, "changed_python_under_packages", lambda _ref: ["src/doc_engine/a.py"]
    )
    assert qg.gate_duplication("origin/main") == 0


def test_changed_python_git_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        qg.subprocess,
        "run",
        lambda *a, **k: MagicMock(returncode=1, stdout="", stderr="boom"),
    )
    with pytest.raises(SystemExit):
        qg.changed_python_under_packages("origin/main")
