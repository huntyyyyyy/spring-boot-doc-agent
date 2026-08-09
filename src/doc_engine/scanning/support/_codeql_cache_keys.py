"""CodeQL cache invalidation keys (content / pack / CLI version hashing).

Domain of "what invalidates a CodeQL DB/results entry" — repo walk / scan
context signatures / query-pack bytes — separate from cache file I/O.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

_HASH_EXCLUDED_DIRS = {
    ".git", ".gradle", "build", "target", "out", "node_modules", ".idea", ".vscode",
    "__pycache__", ".pytest_cache", ".mypy_cache",
}

def _update_hash_pair(h: Any, key: str, value: bytes | str) -> None:
    h.update(key.encode("utf-8"))
    h.update(b"\0")
    h.update(value if isinstance(value, bytes) else value.encode("utf-8"))
    h.update(b"\0")

def _is_codeql_hash_file(rel: str) -> bool:
    name = Path(rel).name
    return (
        name.endswith(".gradle")
        or name.endswith(".gradle.kts")
        or name in {"pom.xml", "build.xml", "settings.gradle", "settings.gradle.kts"}
        or name.endswith(".properties")
        or name.endswith(".yml")
        or name.endswith(".yaml")
    )

def _hash_from_scan_context(scan_context: Any) -> str:
    h = hashlib.sha256()
    java_rels = {entry.rel_path for entry in scan_context.java_files}
    for rel in sorted(scan_context.file_signatures):
        if rel in java_rels or _is_codeql_hash_file(rel):
            _update_hash_pair(h, rel, scan_context.file_signatures[rel])
    return h.hexdigest()[:32]

def _is_codeql_walk_filename(name: str) -> bool:
    return name.endswith(".java") or _is_codeql_hash_file(name)

def _prune_hash_walk_dirs(dirs: list[str]) -> None:
    dirs[:] = [d for d in dirs if d not in _HASH_EXCLUDED_DIRS]

def _matching_walk_paths(walk_root: str, files: list[str]):
    for name in sorted(files):
        if _is_codeql_walk_filename(name):
            yield Path(walk_root) / name

def _iter_codeql_hash_paths(repo_path: Path):
    for walk_root, dirs, files in os.walk(repo_path):
        _prune_hash_walk_dirs(dirs)
        yield from _matching_walk_paths(walk_root, files)

def _hash_one_walk_file(
    h: Any,
    repo_path: Path,
    root: str,
    path: Path,
    is_path_inside_root: Any,
) -> None:
    if not is_path_inside_root(str(path), root):
        return
    try:
        data = path.read_bytes()
    except OSError:
        return
    _update_hash_pair(h, str(path.relative_to(repo_path)), data)

def _hash_from_repo_walk(repo_path: Path) -> str:
    from doc_engine.core.walk import is_path_inside_root

    h = hashlib.sha256()
    root = str(repo_path.resolve())
    for path in _iter_codeql_hash_paths(repo_path):
        _hash_one_walk_file(h, repo_path, root, path, is_path_inside_root)
    return h.hexdigest()[:32]

def _repo_content_hash(repo_path: Path, scan_context: Any = None) -> str:
    """Return a deterministic hash of the source files that affect CodeQL extraction."""
    if scan_context is not None:
        return _hash_from_scan_context(scan_context)
    return _hash_from_repo_walk(repo_path)

def _query_pack_hash(pack_dir: Path) -> str:
    """Hash every .ql file in the pack so query changes invalidate the cache."""
    h = hashlib.sha256()
    for ql in sorted(pack_dir.glob("*.ql")):
        h.update(ql.name.encode("utf-8"))
        h.update(b"\0")
        h.update(ql.read_bytes())
        h.update(b"\0")
    return h.hexdigest()[:32]

def _cache_key(
    repo_path: Path,
    pack_dir: Path,
    build_command: str,
    scan_context: Any = None,
    codeql_cli_version: str = "",
) -> str:
    """Combined cache key: repo + build command + pack + CodeQL CLI version."""
    h = hashlib.sha256()
    h.update(_repo_content_hash(repo_path, scan_context=scan_context).encode("utf-8"))
    h.update(b"\0")
    h.update(build_command.encode("utf-8"))
    h.update(b"\0")
    h.update(_query_pack_hash(pack_dir).encode("utf-8"))
    h.update(b"\0")
    h.update(codeql_cli_version.encode("utf-8"))
    return h.hexdigest()[:32]

