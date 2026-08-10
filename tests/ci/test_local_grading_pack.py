"""Hermetic tests for local grading pack launchers (Windows/IntelliJ hygiene)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.domain_ci_meta

REPO = Path(__file__).resolve().parents[2]
CI = REPO / "scripts" / "ci"
CMD = CI / "run_local_grading_pack.cmd"
SH = CI / "run_local_grading_pack.sh"
STEPS = CI / "grading_pack_steps.sh"
DOC = REPO / "docs" / "process" / "local-grading-pack.md"


def _bash() -> str:
    return os.environ.get("GIT_BASH") or "bash"


def _run_sh(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [_bash(), str(SH), *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def _assert_ascii(path: Path) -> None:
    raw = path.read_bytes()
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{path.name} must be ASCII-only (cmd/Git Bash): {exc}")
    assert "\ufeff" not in text
    # Em-dash / en-dash often sneak into REM comments and break cmd.exe.
    for bad in ("\u2014", "\u2013", "\u2018", "\u2019", "\u201c", "\u201d"):
        assert bad not in text, f"{path.name} contains Unicode {bad!r}"


def test_launcher_files_exist() -> None:
    assert CMD.is_file()
    assert SH.is_file()
    assert STEPS.is_file()
    assert DOC.is_file()


def test_cmd_and_shell_are_ascii_only() -> None:
    _assert_ascii(CMD)
    _assert_ascii(SH)
    _assert_ascii(STEPS)


def test_cmd_is_batch_not_python() -> None:
    text = CMD.read_text(encoding="ascii")
    assert text.lstrip().lower().startswith("@echo off")
    assert "run_local_grading_pack.sh" in text
    assert "%BASH%" in text or "bash.exe" in text.lower()
    # Guard the failure mode operators hit: python ...run_local_grading_pack.cmd
    py = subprocess.run(
        [sys.executable, str(CMD)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert py.returncode != 0
    blob = (py.stderr or "") + (py.stdout or "")
    assert "SyntaxError" in blob


def test_shell_has_shebang_and_sources_steps() -> None:
    text = SH.read_text(encoding="ascii")
    assert text.startswith("#!/usr/bin/env bash")
    assert "grading_pack_steps.sh" in text
    assert "source" in text


def test_list_exits_zero_and_names_ids() -> None:
    completed = _run_sh("list")
    assert completed.returncode == 0, completed.stderr
    out = completed.stdout
    for token in ("doctor", "p1", "p2", "p3", "priority1", "self-test"):
        assert token in out, token


def test_unknown_id_exits_nonzero() -> None:
    completed = _run_sh("not-a-real-grading-id")
    assert completed.returncode != 0


def test_doctor_smoke() -> None:
    completed = _run_sh("doctor")
    assert completed.returncode == 0, completed.stderr + completed.stdout
    assert "ROOT=" in completed.stdout
    assert "ast-grep=" in completed.stdout or "ast-grep" in completed.stdout


def test_self_test_passes_in_repo() -> None:
    completed = _run_sh("self-test")
    assert completed.returncode == 0, completed.stderr + completed.stdout
    assert "self-test ok" in completed.stdout.lower()


def test_markdown_avoids_bash_fences_and_documents_git_bash() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "```bash" not in text
    assert "```text" in text
    assert "run_local_grading_pack.sh" in text
    assert "python" in text.lower() and ".cmd" in text
    assert "Markdown play" in text or "markdown play" in text.lower()
