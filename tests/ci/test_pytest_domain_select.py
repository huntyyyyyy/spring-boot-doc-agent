"""E-SEL1: fine ABI paths + path→domain pytest selection (must bite)."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci.pytest_domain_select import (
    build_select_plan,
    markers_for_paths,
)
from doc_engine.ci.test_path_shards import domain_path_matrix, paths_for_marker
from doc_engine.paths import repo_root

pytestmark = pytest.mark.domain_ci_meta


def test_mixed_doc_engine_emits_file_paths_not_sole_dir() -> None:
    """Climb must not collect all of tests/doc_engine via a bare dir path."""
    root = repo_root()
    climb_paths = paths_for_marker(root, "domain_climb_sensor")
    assert climb_paths, "climb shard must be non-empty"
    assert "tests/doc_engine" not in climb_paths
    assert any(path.endswith(".py") for path in climb_paths)


def test_pure_adapters_dir_still_dir_path() -> None:
    root = repo_root()
    paths = paths_for_marker(root, "domain_adapters")
    assert paths == ("tests/adapters",)


def test_ci_only_change_selects_ci_meta_not_full() -> None:
    root = repo_root()
    plan = build_select_plan(
        root,
        ["src/doc_engine/ci/quality_gate_checks.py", "tests/ci/test_pre_pr_classify_bypass.py"],
        force_full=False,
    )
    assert plan.mode == "domains"
    assert plan.markers == ("domain_ci_meta",)
    assert "tests/" not in plan.paths or plan.paths != ("tests/",)
    argv = plan.argv()
    assert "-m" in argv
    assert "domain_ci_meta" in argv[argv.index("-m") + 1]


def test_unknown_src_path_fail_closed_full() -> None:
    plan = build_select_plan(
        repo_root(),
        ["src/doc_engine/brand_new_widget/foo.py"],
        force_full=False,
    )
    assert plan.mode == "full"
    assert plan.argv()[-1] == "tests/"


def test_force_full_ignores_narrow_paths() -> None:
    plan = build_select_plan(
        repo_root(),
        ["tests/ci/test_foo.py"],
        force_full=True,
    )
    assert plan.mode == "full"


def test_markers_for_paths_docs_ignored() -> None:
    assert markers_for_paths(["README.md", "docs/research/foo.md"]) is None


def test_abi_matrix_climb_paths_are_files() -> None:
    groups = {g.marker: g for g in domain_path_matrix(repo_root())}
    climb = groups["domain_climb_sensor"]
    assert all(p.endswith(".py") for p in climb.paths)
    assert any(p.startswith("tests/doc_engine/") for p in climb.paths)
