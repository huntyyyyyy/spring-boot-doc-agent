"""E-HOOK1: install_git_hooks + quality-gates suite helper."""

from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

import install_git_hooks
import pre_pr
import pre_pr_quality_gates_suite as qg_suite

pytestmark = pytest.mark.domain_ci_meta


def test_quality_gates_argv_skips_coverage_by_default(tmp_path: Path) -> None:
    with mock.patch.dict("os.environ", {}, clear=True):
        with mock.patch.object(
            qg_suite.subprocess,
            "run",
            return_value=mock.Mock(returncode=1, stdout="", stderr=""),
        ):
            argv = qg_suite.quality_gates_argv(tmp_path, skip_coverage=True)
    assert argv[:2] == ["quality-gates", "--compare-ref"]
    assert "--skip-coverage" in argv


def test_resolve_compare_ref_prefers_env(tmp_path: Path) -> None:
    with mock.patch.dict("os.environ", {"PRE_PR_COMPARE_REF": "origin/feature"}):
        assert qg_suite.resolve_compare_ref(tmp_path) == "origin/feature"


def test_standard_suites_include_in_repo_quality_gates() -> None:
    names = [name for name, _, _ in pre_pr.build_suites("standard")]
    assert "in_repo_quality_gates" in names
    assert "sonar_local_advisory" not in names


def test_full_suites_include_sonar_advisory() -> None:
    names = [name for name, _, _ in pre_pr.build_suites("full")]
    assert "in_repo_quality_gates" in names
    assert "sonar_local_advisory" in names


def test_hooks_healthy_false_when_unset(tmp_path: Path) -> None:
    (tmp_path / ".githooks").mkdir()
    (tmp_path / ".githooks" / "pre-push").write_text("#!/bin/sh\n", encoding="utf-8")
    with mock.patch.object(install_git_hooks, "repo_root", return_value=tmp_path):
        with mock.patch.object(install_git_hooks, "current_hooks_path", return_value=""):
            ok, detail = install_git_hooks.hooks_healthy(tmp_path)
    assert ok is False
    assert "unset" in detail


def test_install_chain_writes_marker(tmp_path: Path) -> None:
    hooks = tmp_path / "external-hooks"
    target = install_git_hooks.install_chain(hooks)
    text = target.read_text(encoding="utf-8")
    assert install_git_hooks.CHAIN_MARKER in text
    assert target.stat().st_mode & 0o111
