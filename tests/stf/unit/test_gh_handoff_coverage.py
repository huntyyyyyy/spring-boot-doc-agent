"""Coverage climb for ``stf.adapters.gh_handoff`` create/dry-run paths."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from stf.adapters import gh_handoff
from tests.stf.conftest import build_minimal_valid_tasks


def test_issues_from_tasks_skips_t0() -> None:
    tasks = build_minimal_valid_tasks(target="demo")
    issues = gh_handoff.issues_from_tasks(tasks)
    assert len(issues) == 1
    assert issues[0]["title"].startswith("[STF demo] T1")
    assert "stf" in issues[0]["labels"]


def test_gh_issue_cmd_with_and_without_repo() -> None:
    issue = {"title": "t", "body": "b", "labels": ["stf", "x"]}
    bare = gh_handoff._gh_issue_cmd(issue, None)
    assert bare[:3] == ["gh", "issue", "create"]
    assert "--repo" not in bare
    with_repo = gh_handoff._gh_issue_cmd(issue, "org/repo")
    assert with_repo[with_repo.index("--repo") + 1] == "org/repo"
    assert with_repo.count("--label") == 2


def test_create_gh_issue_captures_proc(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        gh_handoff.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=0, stdout=" https://x \n", stderr=""),
    )
    out = gh_handoff._create_gh_issue(
        {"title": "t", "body": "b", "labels": []},
        repo="org/r",
    )
    assert out["rc"] == 0
    assert out["stdout"] == "https://x"


def test_handoff_gh_dry_run_and_live(monkeypatch: pytest.MonkeyPatch) -> None:
    tasks = build_minimal_valid_tasks()
    dry = gh_handoff.handoff_gh(tasks, dry_run=True)
    assert dry[0]["dry_run"] is True
    monkeypatch.setattr(
        gh_handoff,
        "_create_gh_issue",
        lambda issue, repo: {"title": issue["title"], "rc": 0, "repo": repo},
    )
    live = gh_handoff.handoff_gh(tasks, dry_run=False, repo="org/r")
    assert live[0]["rc"] == 0
    assert live[0]["repo"] == "org/r"


def test_write_handoff_checklist(tmp_path: Path) -> None:
    path = tmp_path / "handoff.md"
    out = gh_handoff.write_handoff_checklist(path, build_minimal_valid_tasks())
    text = out.read_text(encoding="utf-8")
    assert "# STF handoff checklist" in text
    assert "T1" in text
