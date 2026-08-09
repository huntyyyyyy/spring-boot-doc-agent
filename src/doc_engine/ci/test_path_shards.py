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
        root = repo / rel_root
        if not root.is_dir():
            continue
        for module in root.rglob("test_*.py"):
            if "__pycache__" in module.parts:
                continue
            if "support" in module.parts:
                continue
            found.add(module.parent.resolve())
    return sorted(found)


def domain_path_matrix(repo: Path) -> tuple[DomainPathGroup, ...]:
    """Group collection paths by parallel parent marker (file-classified)."""
    parallel = set(parallel_shard_markers())
    by_marker: dict[str, set[str]] = {marker: set() for marker in parallel}
    for collection_dir in discover_collection_dirs(repo):
        for module in sorted(collection_dir.glob("test_*.py")):
            marker = classify_test_path(repo, module)
            if marker not in parallel:
                continue
            rel = collection_dir.relative_to(repo.resolve()).as_posix()
            by_marker[marker].add(rel)

    groups: list[DomainPathGroup] = []
    for marker in parallel_shard_markers():
        require_domain(marker)
        paths = tuple(sorted(by_marker[marker]))
        if not paths:
            continue
        shard_id = marker.removeprefix("domain_")
        groups.append(DomainPathGroup(shard_id=shard_id, marker=marker, paths=paths))
    return tuple(groups)


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
    covered: set[str] = set()
    for group in domain_path_matrix(repo):
        covered.update(group.paths)
    parallel = set(parallel_shard_markers())
    orphans: list[str] = []
    tests_root = repo / "tests"
    if not tests_root.is_dir():
        return orphans
    for module in tests_root.rglob("test_*.py"):
        if "__pycache__" in module.parts or "support" in module.parts:
            continue
        marker = classify_test_path(repo, module)
        if marker not in parallel:
            continue
        parent = module.parent.resolve().relative_to(repo.resolve()).as_posix()
        if parent not in covered:
            orphans.append(module.relative_to(repo).as_posix())
    return orphans
