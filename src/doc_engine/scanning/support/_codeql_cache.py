"""CodeQL results/DB cache I/O: directory hygiene, metadata, results JSON.

Cache *keys* (invalidation hashing) live in `_codeql_cache_keys`."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from doc_engine.paths import PathValidationError, join_under
from doc_engine.scanning.support._codeql_cache_keys import _cache_key
from doc_engine.scanning.support._codeql_cli import CodeQLError


def _cache_base_dir() -> Path:
    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg and str(xdg).strip():
        return Path(xdg)
    if sys.platform == "win32":
        local = os.environ.get("LOCALAPPDATA")
        return Path(local) if local else Path.home() / "AppData" / "Local"
    return Path.home() / ".cache"

def _refuse_symlink_cache_path(path: Path) -> None:
    if path.exists() and path.is_symlink():
        raise CodeQLError(f"refusing CodeQL cache path that is a symlink: {path}")
    if path.is_symlink():
        raise CodeQLError(f"refusing CodeQL cache path that is a symlink: {path}")

def _cache_dir() -> Path:
    """User-owned CodeQL cache root (mode 0700); never world-writable /tmp.

    Shared-host /tmp with exist_ok mkdir is a forgery vector for results JSON
    (CWE-377). Prefer XDG_CACHE_HOME / LOCALAPPDATA / ~/.cache under doc-engine.
    """
    path = _cache_base_dir() / "doc-engine" / "codeql-cache"
    _refuse_symlink_cache_path(path)
    path.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path, 0o700)
    except OSError:
        pass
    _refuse_symlink_cache_path(path)
    return path

def _ensure_regular_file(path: Path) -> None:
    if path.exists() and (path.is_symlink() or not path.is_file()):
        raise CodeQLError(f"refusing non-regular cache file: {path}")

def _cache_meta_path(db_path: Path) -> Path:
    """Resolve cache metadata under *db_path*; refuse path escape."""
    try:
        return join_under(db_path, "spring_signal_scan_cache.json")
    except PathValidationError as exc:
        raise CodeQLError(str(exc)) from exc

def _validate_one_cached_row(i: int, row: Any) -> Dict[str, Any]:
    if not isinstance(row, dict):
        raise CodeQLError(f"cached CodeQL row {i} is not an object")
    if not isinstance(row.get("file"), str) or not row["file"]:
        raise CodeQLError(f"cached CodeQL row {i} missing file")
    return row

def _validate_cached_evidence_rows(rows: Any) -> List[Dict[str, Any]]:
    """Treat cache JSON as untrusted input — shape-gate before returning as evidence."""
    if not isinstance(rows, list):
        raise CodeQLError("cached CodeQL results are not a list")
    return [_validate_one_cached_row(i, row) for i, row in enumerate(rows)]

def _cache_db_path(
    repo_path: Path,
    pack_dir: Path,
    build_command: str,
    scan_context: Any = None,
    codeql_cli_version: str = "",
) -> Path:
    cache_dir = _cache_dir()
    return cache_dir / _cache_key(
        repo_path, pack_dir, build_command, scan_context=scan_context,
        codeql_cli_version=codeql_cli_version,
    )

def _cache_metadata(db_path: Path) -> Optional[Dict[str, str]]:
    try:
        meta = _cache_meta_path(db_path)
    except CodeQLError:
        return None
    if not meta.is_file():
        return None
    try:
        _ensure_regular_file(meta)
        return json.loads(meta.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, CodeQLError):
        return None

def _write_cache_metadata(
    db_path: Path,
    repo_path: Path,
    pack_dir: Path,
    build_command: str,
    scan_context: Any = None,
    codeql_cli_version: str = "",
) -> None:
    meta = _cache_meta_path(db_path)
    meta.write_text(json.dumps({
        "cache_key": _cache_key(
            repo_path, pack_dir, build_command, scan_context=scan_context,
            codeql_cli_version=codeql_cli_version,
        ),
        "codeql_cli_version": codeql_cli_version,
    }), encoding="utf-8")

def _cache_is_valid(
    db_path: Path,
    repo_path: Path,
    pack_dir: Path,
    build_command: str,
    scan_context: Any = None,
    codeql_cli_version: str = "",
) -> bool:
    meta = _cache_metadata(db_path)
    if meta is None:
        return False
    return meta.get("cache_key") == _cache_key(
        repo_path, pack_dir, build_command, scan_context=scan_context,
        codeql_cli_version=codeql_cli_version,
    )

def _results_cache_path(
    repo_path: Path,
    pack_dir: Path,
    build_command: str,
    scanner_version: str,
    scan_context: Any = None,
    codeql_cli_version: str = "",
) -> Path:
    """Path to the cached query results for a fully determined scan."""
    h = hashlib.sha256()
    h.update(scanner_version.encode("utf-8"))
    h.update(b"\0")
    h.update(codeql_cli_version.encode("utf-8"))
    h.update(b"\0")
    h.update(_cache_key(
        repo_path, pack_dir, build_command, scan_context=scan_context,
        codeql_cli_version=codeql_cli_version,
    ).encode("utf-8"))
    return _cache_dir() / (h.hexdigest()[:32] + "_results.json")

def _load_results_cache(
    repo_path: Path,
    pack_dir: Path,
    build_command: str,
    scanner_version: str,
    scan_context: Any = None,
    codeql_cli_version: str = "",
) -> Optional[List[Dict[str, Any]]]:
    path = _results_cache_path(
        repo_path, pack_dir, build_command, scanner_version, scan_context=scan_context,
        codeql_cli_version=codeql_cli_version,
    )
    if not path.is_file():
        return None
    try:
        _ensure_regular_file(path)
        raw = json.loads(path.read_text(encoding="utf-8"))
        return _validate_cached_evidence_rows(raw)
    except (OSError, json.JSONDecodeError, CodeQLError):
        return None

def _save_results_cache(
    repo_path: Path,
    pack_dir: Path,
    build_command: str,
    scanner_version: str,
    rows: List[Dict[str, Any]],
    scan_context: Any = None,
    codeql_cli_version: str = "",
) -> None:
    path = _results_cache_path(
        repo_path, pack_dir, build_command, scanner_version, scan_context=scan_context,
        codeql_cli_version=codeql_cli_version,
    )
    if path.exists():
        _ensure_regular_file(path)
    path.write_text(json.dumps(rows), encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass

