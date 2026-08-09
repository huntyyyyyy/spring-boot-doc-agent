"""Gate tools path require/which helpers."""

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
from doc_engine.ci import quality_gate_checks as qgc
from doc_engine.ci import quality_gates as qg

pytestmark = pytest.mark.domain_ci_meta

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

def test_run_prints_and_returns(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setattr(
        qgc.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=7),
    )
    assert qgc._run(["echo", "hi"], label="demo") == 7
    assert "demo" in capsys.readouterr().out

def test_changed_python_filters(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(qgc, "REPO_ROOT", tmp_path)
    (tmp_path / "src" / "doc_engine").mkdir(parents=True)
    keep = tmp_path / "src" / "doc_engine" / "a.py"
    keep.write_text("x", encoding="utf-8")
    stdout = "src/doc_engine/a.py\nsrc/doc_engine/missing.py\nREADME.md\n"
    monkeypatch.setattr(
        qgc.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=0, stdout=stdout, stderr=""),
    )
    assert qgc.changed_python_under_packages("HEAD~1") == ["src/doc_engine/a.py"]

def test_gate_cognitive_complexity(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "doc_engine.ci.gate_tools.require_on_path",
        lambda _n: "/bin/complexipy",
    )
    monkeypatch.setattr(qgc, "_run", lambda cmd, label: 0)
    assert qgc.gate_cognitive_complexity() == 0

def test_baseline_offender_ceiling_bad_json(tmp_path: Path) -> None:
    path = tmp_path / "b.json"
    path.write_text("{", encoding="utf-8")
    assert qg.baseline_offender_ceiling(path) is None
    assert qg.baseline_offender_ceiling(tmp_path / "absent.json") is None

def test_main_with_coverage_and_exit_codes(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(qg, "REPO_ROOT", tmp_path)
    xml = tmp_path / "coverage.xml"
    xml.write_text("<coverage/>", encoding="utf-8")
    monkeypatch.setattr(qg, "gate_import_cycles", lambda: 0)
    monkeypatch.setattr(qg, "gate_size_ratchet", lambda: 0)
    monkeypatch.setattr(qg, "gate_duplication", lambda _r: 0)
    monkeypatch.setattr(qg, "gate_new_code_coverage", lambda _r, _x: 0)
    monkeypatch.setattr(qg, "gate_cognitive_complexity", lambda: 0)
    monkeypatch.setattr(qg, "gate_complexity_ratchet", lambda: 0)
    monkeypatch.setattr(qg, "report_gap_average", lambda _x: None)
    assert qg.main(["--compare-ref", "HEAD~1", "--coverage-xml", str(xml)]) == 0

    monkeypatch.setattr(qg, "gate_import_cycles", lambda: 2)
    assert qg.main(["--compare-ref", "HEAD~1", "--skip-coverage"]) == 2
