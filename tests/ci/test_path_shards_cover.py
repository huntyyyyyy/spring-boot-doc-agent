"""Hermetic coverage: discovered domain path matrix covers parallel modules."""

from __future__ import annotations

import pytest

from doc_engine.ci.test_domain_catalog import parallel_shard_markers
from doc_engine.ci.test_path_shards import (
    DISCOVERY_ROOTS,
    domain_path_matrix,
    github_matrix_include,
    orphan_parallel_modules,
)
from doc_engine.paths import repo_root

pytestmark = pytest.mark.domain_ci_meta


def test_domain_path_matrix_groups_by_parallel_marker() -> None:
    """Matrix rows are the short parallel catalog, paths discovered from dirs."""
    root = repo_root()
    groups = domain_path_matrix(root)
    assert groups
    parallel = set(parallel_shard_markers())
    seen_markers = {group.marker for group in groups}
    assert seen_markers <= parallel
    for group in groups:
        assert group.paths
        assert group.shard_id == group.marker.removeprefix("domain_")
        for path in group.paths:
            assert not path.startswith("tests/support")
            assert (root / path).is_dir()


def test_discovery_roots_exclude_support() -> None:
    assert "tests/support" not in DISCOVERY_ROOTS


def test_no_orphan_parallel_modules() -> None:
    assert orphan_parallel_modules(repo_root()) == []


def test_github_matrix_include_paths_are_space_joined() -> None:
    rows = github_matrix_include(repo_root())
    assert rows
    for row in rows:
        assert " " not in row["marker"]
        assert row["paths"]
        for path in row["paths"].split():
            assert path.startswith("tests/")
