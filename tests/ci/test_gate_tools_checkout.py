"""Gate tools checkout/root helpers."""

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
    """Find tool next to sys.executable when which() misses.

    Does not monkeypatch ``os.name`` or ``pathlib.Path``: on modern Python,
    ``Path.__new__`` consults ``os.name``, so forcing ``posix`` on Windows
    (or ``WindowsPath`` on Linux) raises UnsupportedOperation / NotImplementedError.
    The bare-name candidate is always tried first, so this hits the sibling-dir
    lookup on both POSIX CI and Windows.
    """
    monkeypatch.setattr(gate_tools.shutil, "which", lambda _n: None)
    tool = tmp_path / "mytool"
    tool.write_text("", encoding="utf-8")
    monkeypatch.setattr(sys, "executable", str(tmp_path / "python"))
    assert "mytool" in gate_tools.require_on_path("mytool")
