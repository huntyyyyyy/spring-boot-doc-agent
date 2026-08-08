"""Drive ``doc_engine.ci`` modules to ≥98.7% Cover% (leave the gap list)."""

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


# --- coverage_gap_average ---------------------------------------------------


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


# --- gate_tools -------------------------------------------------------------


def test_checkout_root_fallback_pyproject(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        gate_tools.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=1, stdout="", stderr=""),
    )
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    (tmp_path / "src" / "doc_engine").mkdir(parents=True)
    assert gate_tools.checkout_root(tmp_path) == tmp_path.resolve()


def test_checkout_root_git_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        gate_tools.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=0, stdout=str(tmp_path) + "\n", stderr=""),
    )
    assert gate_tools.checkout_root(tmp_path) == Path(tmp_path)


def test_checkout_root_cwd_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        gate_tools.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=1, stdout="", stderr=""),
    )
    monkeypatch.chdir(tmp_path)
    assert gate_tools.checkout_root(tmp_path) == tmp_path.resolve()


def test_checked_path_under_repo_ok_and_escape(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(gate_tools, "REPO_ROOT", tmp_path)
    inside = tmp_path / "a.txt"
    inside.write_text("x", encoding="utf-8")
    assert gate_tools.checked_path_under_repo(inside) == inside.resolve()
    outside = tmp_path.parent / "escape.txt"
    outside.write_text("y", encoding="utf-8")
    with pytest.raises(SystemExit):
        gate_tools.checked_path_under_repo(outside)


def test_checked_path_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(gate_tools, "REPO_ROOT", tmp_path)
    real_resolve = Path.resolve

    def _boom(self, *args, **kwargs):
        if "bad-path" in str(self):
            raise OSError("boom")
        return real_resolve(self, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", _boom)
    with pytest.raises(SystemExit):
        gate_tools.checked_path_under_repo(tmp_path / "bad-path")


def test_require_on_path_which_hit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(gate_tools.shutil, "which", lambda n: f"/usr/bin/{n}")
    assert gate_tools.require_on_path("node") == "/usr/bin/node"


def test_checkout_root_empty_git_stdout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        gate_tools.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=0, stdout="\n", stderr=""),
    )
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    (tmp_path / "src" / "doc_engine").mkdir(parents=True)
    assert gate_tools.checkout_root(tmp_path) == tmp_path.resolve()


def test_jscpd_native_candidates_other_platforms(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(gate_tools, "REPO_ROOT", tmp_path)
    for system, machine, needle in (
        ("Darwin", "arm64", "darwin-arm64"),
        ("Darwin", "x86_64", "darwin-x64"),
        ("Linux", "x86_64", "linux-x64"),
        ("Linux", "arm64", "linux-arm64"),
    ):
        monkeypatch.setattr(gate_tools.platform, "system", lambda s=system: s)
        monkeypatch.setattr(gate_tools.platform, "machine", lambda m=machine: m)
        joined = " ".join(str(c) for c in gate_tools._jscpd_native_candidates())
        assert needle in joined
    # Unmatched platform: fall through elif chain to empty list (143->145).
    monkeypatch.setattr(gate_tools.platform, "system", lambda: "FreeBSD")
    monkeypatch.setattr(gate_tools.platform, "machine", lambda: "x86_64")
    assert gate_tools._jscpd_native_candidates() == []


def test_require_on_path_sibling_scripts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(gate_tools.shutil, "which", lambda _n: None)
    scripts = tmp_path / "Scripts"
    scripts.mkdir()
    tool = scripts / ("fake-tool.exe" if sys.platform == "win32" else "fake-tool")
    tool.write_text("", encoding="utf-8")
    monkeypatch.setattr(sys, "executable", str(tmp_path / "python.exe"))
    found = gate_tools.require_on_path("fake-tool")
    assert Path(found).name.startswith("fake-tool")


def test_require_on_path_non_nt_name_list(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Hit the non-Windows name list branch without switching pathlib OS."""
    from pathlib import WindowsPath

    monkeypatch.setattr(gate_tools.shutil, "which", lambda _n: None)
    monkeypatch.setattr(gate_tools, "Path", WindowsPath)
    monkeypatch.setattr(gate_tools.os, "name", "posix")
    tool = tmp_path / "mytool"
    tool.write_text("", encoding="utf-8")
    monkeypatch.setattr(sys, "executable", str(tmp_path / "python"))
    assert "mytool" in gate_tools.require_on_path("mytool")


def test_jscpd_skips_nonfile_native_then_wrapper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(gate_tools, "REPO_ROOT", tmp_path)
    missing = tmp_path / "missing-native"
    monkeypatch.setattr(gate_tools, "_jscpd_native_candidates", lambda: [missing])
    wrapper = tmp_path / "node_modules" / "jscpd" / "run-jscpd.js"
    wrapper.parent.mkdir(parents=True)
    wrapper.write_text("//", encoding="utf-8")
    monkeypatch.setattr(gate_tools, "require_on_path", lambda n: f"/bin/{n}")
    cmd = gate_tools.jscpd_command("--x")
    assert cmd[0] == "/bin/node"


def test_require_venv_script_delegates(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(gate_tools, "require_on_path", lambda n: f"/bin/{n}")
    assert gate_tools.require_venv_script("complexipy") == "/bin/complexipy"


def test_arch_token_variants(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(gate_tools.platform, "machine", lambda: "AMD64")
    assert gate_tools._arch_token() == "x64"
    monkeypatch.setattr(gate_tools.platform, "machine", lambda: "arm64")
    assert gate_tools._arch_token() == "arm64"
    monkeypatch.setattr(gate_tools.platform, "machine", lambda: "riscv64")
    assert gate_tools._arch_token() == "riscv64"


def test_jscpd_native_candidates_windows_x64(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(gate_tools, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(gate_tools.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(gate_tools.platform, "system", lambda: "Windows")
    cands = gate_tools._jscpd_native_candidates()
    assert any("windows-x64" in str(c) for c in cands)


def test_jscpd_command_native_and_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(gate_tools, "REPO_ROOT", tmp_path)
    native = tmp_path / "node_modules" / "jscpd-windows-x64-msvc" / "bin" / "jscpd.exe"
    native.parent.mkdir(parents=True)
    native.write_text("", encoding="utf-8")
    monkeypatch.setattr(gate_tools, "_jscpd_native_candidates", lambda: [native])
    assert gate_tools.jscpd_command("--help")[0] == str(native)

    monkeypatch.setattr(gate_tools, "_jscpd_native_candidates", lambda: [])
    with pytest.raises(SystemExit):
        gate_tools.jscpd_command("--help")


def test_python_module_command() -> None:
    cmd = gate_tools.python_module_command("pkg.mod", "--flag")
    assert cmd[:3] == [sys.executable, "-m", "pkg.mod"]
    assert cmd[-1] == "--flag"


# --- quality_gates ----------------------------------------------------------


def test_run_prints_and_returns(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setattr(
        qg.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=7),
    )
    assert qg._run(["echo", "hi"], label="demo") == 7
    assert "demo" in capsys.readouterr().out


def test_changed_python_filters(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(qg, "REPO_ROOT", tmp_path)
    (tmp_path / "src" / "doc_engine").mkdir(parents=True)
    keep = tmp_path / "src" / "doc_engine" / "a.py"
    keep.write_text("x", encoding="utf-8")
    stdout = "src/doc_engine/a.py\nsrc/doc_engine/missing.py\nREADME.md\n"
    monkeypatch.setattr(
        qg.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=0, stdout=stdout, stderr=""),
    )
    assert qg.changed_python_under_packages("HEAD~1") == ["src/doc_engine/a.py"]


def test_gate_cognitive_complexity(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "doc_engine.ci.gate_tools.require_on_path",
        lambda _n: "/bin/complexipy",
    )
    monkeypatch.setattr(qg, "_run", lambda cmd, label: 0)
    assert qg.gate_cognitive_complexity() == 0


def test_baseline_offender_ceiling_bad_json(tmp_path: Path) -> None:
    path = tmp_path / "b.json"
    path.write_text("{", encoding="utf-8")
    assert qg.baseline_offender_ceiling(path) is None
    assert qg.baseline_offender_ceiling(tmp_path / "absent.json") is None


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


def test_main_with_coverage_and_exit_codes(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(qg, "REPO_ROOT", tmp_path)
    xml = tmp_path / "coverage.xml"
    xml.write_text("<coverage/>", encoding="utf-8")
    monkeypatch.setattr(qg, "gate_import_cycles", lambda: 0)
    monkeypatch.setattr(qg, "gate_duplication", lambda _r: 0)
    monkeypatch.setattr(qg, "gate_new_code_coverage", lambda _r, _x: 0)
    monkeypatch.setattr(qg, "gate_cognitive_complexity", lambda: 0)
    monkeypatch.setattr(qg, "gate_complexity_ratchet", lambda: 0)
    monkeypatch.setattr(qg, "_report_gap_average", lambda _x: None)
    assert qg.main(["--compare-ref", "HEAD~1", "--coverage-xml", str(xml)]) == 0

    monkeypatch.setattr(qg, "gate_import_cycles", lambda: 2)
    assert qg.main(["--compare-ref", "HEAD~1", "--skip-coverage"]) == 2

