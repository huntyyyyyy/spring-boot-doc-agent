"""Discover ABI path groups from test subdomain folders (E-TEST3 / Spec T19).

Collection dirs are parents of ``test_*.py`` under known roots (not
``tests/support``). Paths are grouped by parallel parent ``domain_*`` marker
so the CI matrix stays short (~one row per domain).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from doc_engine.ci.test_domain_catalog import parallel_shard_markers, require_domain
from doc_engine.ci.test_domain_classify import classify_test_path

# Roots scanned for collection dirs. ``tests/support`` is intentionally absent.
DISCOVERY_ROOTS: tuple[str, ...] = (
    "tests/doc_engine",
    "tests/ci",
    "tests/ratchets",
    "tests/adapters",
    "tests/stf",
    "tests/coverage",
    "tests/research",
    "tests/spring_signals",
)


@dataclass(frozen=True)
class DomainPathGroup:
    """One ABI matrix row: parallel marker + discovered collection paths."""

    shard_id: str
    marker: str
    paths: tuple[str, ...]


def discover_collection_dirs(repo: Path) -> list[Path]:
    """Directories under discovery roots that directly contain ``test_*.py``."""
    found: set[Path] = set()
    for rel_root in DISCOVERY_ROOTS:
        found.update(_collection_dirs_under(repo / rel_root))
    return sorted(found)


def _collection_dirs_under(root: Path) -> set[Path]:
    if not root.is_dir():
        return set()
    found: set[Path] = set()
    for module in root.rglob("test_*.py"):
        if _is_discoverable_test_module(module):
            found.add(module.parent.resolve())
    return found


def _is_discoverable_test_module(module: Path) -> bool:
    if "__pycache__" in module.parts:
        return False
    if "support" in module.parts:
        return False
    return True


def domain_path_matrix(repo: Path) -> tuple[DomainPathGroup, ...]:
    """Group collection paths by parallel parent marker (file-classified)."""
    by_marker = _paths_by_parallel_marker(repo)
    return tuple(_groups_from_marker_paths(by_marker))


def _paths_by_parallel_marker(repo: Path) -> dict[str, set[str]]:
    parallel = set(parallel_shard_markers())
    by_marker: dict[str, set[str]] = {marker: set() for marker in parallel}
    for collection_dir in discover_collection_dirs(repo):
        _add_collection_to_marker_map(repo, collection_dir, parallel, by_marker)
    return by_marker


def _add_collection_to_marker_map(
    repo: Path,
    collection_dir: Path,
    parallel: set[str],
    by_marker: dict[str, set[str]],
) -> None:
    """Add dir path when pure; else per-file paths (mixed-marker dirs — SEL1)."""
    modules_by_marker = _parallel_modules_by_marker(repo, collection_dir, parallel)
    if not modules_by_marker:
        return
    rel_dir = collection_dir.relative_to(repo.resolve()).as_posix()
    if len(modules_by_marker) == 1:
        marker = next(iter(modules_by_marker))
        by_marker[marker].add(rel_dir)
        return
    for marker, modules in modules_by_marker.items():
        for module in modules:
            by_marker[marker].add(module.relative_to(repo.resolve()).as_posix())


def _parallel_modules_by_marker(
    repo: Path,
    collection_dir: Path,
    parallel: set[str],
) -> dict[str, list[Path]]:
    grouped: dict[str, list[Path]] = {}
    for module in sorted(collection_dir.glob("test_*.py")):
        marker = classify_test_path(repo, module)
        if marker not in parallel:
            continue
        grouped.setdefault(marker, []).append(module)
    return grouped


def _groups_from_marker_paths(
    by_marker: dict[str, set[str]],
) -> list[DomainPathGroup]:
    groups: list[DomainPathGroup] = []
    for marker in parallel_shard_markers():
        group = _group_for_marker(marker, by_marker)
        if group is not None:
            groups.append(group)
    return groups


def _group_for_marker(
    marker: str, by_marker: dict[str, set[str]]
) -> DomainPathGroup | None:
    require_domain(marker)
    paths = tuple(sorted(by_marker[marker]))
    if not paths:
        return None
    return DomainPathGroup(
        shard_id=marker.removeprefix("domain_"),
        marker=marker,
        paths=paths,
    )


def paths_for_marker(repo: Path, marker: str) -> tuple[str, ...]:
    """Collection paths for one parallel marker (empty if unknown/serial)."""
    require_domain(marker)
    for group in domain_path_matrix(repo):
        if group.marker == marker:
            return group.paths
    return ()


def parallel_path_shards(repo: Path) -> tuple[DomainPathGroup, ...]:
    """Alias for ABI consumers — discovered domain path groups."""
    return domain_path_matrix(repo)


def github_matrix_include(repo: Path) -> list[dict[str, str]]:
    """Rows for a generated GitHub matrix (id / marker / paths)."""
    return [
        {
            "id": group.shard_id,
            "marker": group.marker,
            "paths": " ".join(group.paths),
        }
        for group in domain_path_matrix(repo)
    ]


def orphan_parallel_modules(repo: Path) -> list[str]:
    """Parallel-marked modules whose parent is outside discovered paths."""
    covered = _covered_collection_paths(repo)
    parallel = set(parallel_shard_markers())
    tests_root = repo / "tests"
    if not tests_root.is_dir():
        return []
    return _orphan_rels(repo, tests_root, parallel, covered)


def _covered_collection_paths(repo: Path) -> set[str]:
    covered: set[str] = set()
    for group in domain_path_matrix(repo):
        covered.update(group.paths)
    return covered


def _orphan_rels(
    repo: Path,
    tests_root: Path,
    parallel: set[str],
    covered: set[str],
) -> list[str]:
    orphans: list[str] = []
    for module in tests_root.rglob("test_*.py"):
        if _is_orphan_parallel(repo, module, parallel, covered):
            orphans.append(module.relative_to(repo).as_posix())
    return orphans


def _is_orphan_parallel(
    repo: Path,
    module: Path,
    parallel: set[str],
    covered: set[str],
) -> bool:
    if not _is_discoverable_test_module(module):
        return False
    marker = classify_test_path(repo, module)
    if marker not in parallel:
        return False
    rel = module.relative_to(repo.resolve()).as_posix()
    if rel in covered:
        return False
    parent = module.parent.resolve().relative_to(repo.resolve()).as_posix()
    return parent not in covered
