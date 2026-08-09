"""CodeQL database lifecycle: create, pack install, cache reuse/rebuild."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Optional

from doc_engine.core.timeouts import codeql_database_timeout_seconds, tool_timeout_seconds
from doc_engine.paths import codeql_pack_dir
from doc_engine.scanning.build_command import validate_build_command
from doc_engine.scanning.support import _codeql_cache as cache
from doc_engine.scanning.support import _codeql_cli as cli
from doc_engine.scanning.support._codeql_cli import CodeQLError

DEFAULT_PACK_DIR = codeql_pack_dir()

def create_database(
    codeql_path: Path,
    repo_path: Path,
    db_path: Path,
    build_command: str,
    overwrite: bool = True,
) -> None:
    """Create a CodeQL Java database for the repo using the supplied build.

    ``build_command`` is re-validated here before being passed as a single
    ``--command=`` argv element (no shell). CodeQL still executes that build
    inside ``--source-root`` — callers must also pass ``--allow-codeql-build``
    for untrusted trees; this layer only removes free-form OS argv and
    foot-gun build strings.
    """
    safe_build = validate_build_command(build_command)
    options = [
        str(db_path),
        "--language=java",
        f"--command={safe_build}",
        f"--source-root={repo_path}",
    ]
    if overwrite:
        options.append("--overwrite")
    proc = cli._invoke_codeql(
        codeql_path,
        ("database", "create"),
        *options,
        timeout=codeql_database_timeout_seconds(),
    )
    if proc.returncode != 0:
        raise CodeQLError(
            f"codeql database create failed (exit {proc.returncode}):\n"
            f"{proc.stderr}\n{proc.stdout}"
        )

def install_pack(codeql_path: Path, pack_dir: Path) -> None:
    """Install the QL pack dependencies (codeql/java-all, etc.)."""
    proc = cli._invoke_codeql(
        codeql_path,
        ("pack", "install"),
        str(pack_dir),
        timeout=tool_timeout_seconds(),
    )
    if proc.returncode != 0:
        raise CodeQLError(
            f"codeql pack install failed (exit {proc.returncode}):\n"
            f"{proc.stderr}\n{proc.stdout}"
        )

def _prepare_scan_targets(
    repo_path: Path,
    build_command: str,
    pack_dir: Optional[Path],
    db_path: Optional[Path],
    keep_database: bool,
    scan_context: Any,
    cli_version: str,
) -> tuple[Path, Path, bool, bool]:
    """Return ``(pack_dir, db_path, using_cache, keep_database)``."""
    resolved_pack = pack_dir or DEFAULT_PACK_DIR
    if not resolved_pack.is_dir():
        raise CodeQLError(f"query pack not found: {resolved_pack}")
    using_cache = db_path is None
    if using_cache:
        db_path = cache._cache_db_path(
            repo_path, resolved_pack, build_command, scan_context=scan_context,
            codeql_cli_version=cli_version,
        )
        keep_database = True
    assert db_path is not None
    return resolved_pack, db_path, using_cache, keep_database

def _ensure_codeql_database(
    *,
    codeql_path: Path,
    repo_path: Path,
    db_path: Path,
    pack_dir: Path,
    build_command: str,
    using_cache: bool,
    keep_database: bool,
    scan_context: Any,
    cli_version: str,
) -> None:
    if db_path.exists() and keep_database:
        _reuse_or_rebuild_cached_db(
            codeql_path=codeql_path,
            repo_path=repo_path,
            db_path=db_path,
            pack_dir=pack_dir,
            build_command=build_command,
            using_cache=using_cache,
            scan_context=scan_context,
            cli_version=cli_version,
        )
        return
    create_database(codeql_path, repo_path, db_path, build_command, overwrite=True)
    if using_cache:
        cache._write_cache_metadata(
            db_path, repo_path, pack_dir, build_command, scan_context=scan_context,
            codeql_cli_version=cli_version,
        )

def _reuse_or_rebuild_cached_db(
    *,
    codeql_path: Path,
    repo_path: Path,
    db_path: Path,
    pack_dir: Path,
    build_command: str,
    using_cache: bool,
    scan_context: Any,
    cli_version: str,
) -> None:
    if not using_cache:
        # Caller-provided db_path with keep_database: trust it.
        return
    if cache._cache_is_valid(
        db_path, repo_path, pack_dir, build_command, scan_context=scan_context,
        codeql_cli_version=cli_version,
    ):
        return
    # Cache is stale (source, build command, or queries changed): rebuild.
    shutil.rmtree(db_path, ignore_errors=True)
    create_database(codeql_path, repo_path, db_path, build_command, overwrite=True)
    cache._write_cache_metadata(
        db_path, repo_path, pack_dir, build_command, scan_context=scan_context,
        codeql_cli_version=cli_version,
    )

