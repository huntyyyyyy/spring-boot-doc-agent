"""CodeQL Stage-0 scan facade.

Application orchestration: discover CLI → cache short-circuit → ensure DB →
run queries. Ports/adapters live in sibling modules:

- ``_codeql_cli`` — allowlisted CodeQL binary invoke
- ``_codeql_cache_keys`` — invalidation hashing
- ``_codeql_cache`` — cache directory / metadata / results JSON
- ``_codeql_database`` — database create + pack install + reuse
- ``_codeql_queries`` — query run + BQRS decode
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import doc_engine.scanning.support._codeql_cache as cache
import doc_engine.scanning.support._codeql_cache_keys as cache_keys
import doc_engine.scanning.support._codeql_cli as cli
import doc_engine.scanning.support._codeql_database as database
import doc_engine.scanning.support._codeql_queries as queries
from doc_engine.scanning.build_command import BuildCommandError, validate_build_command

# Stable facade surface (tests and scanners import from this module).
CodeQLError = cli.CodeQLError
CodeQLNotFoundError = cli.CodeQLNotFoundError
find_codeql = cli.find_codeql
codeql_version = cli.codeql_version
_invoke_codeql = cli._invoke_codeql
_CODEQL_SUBCOMMANDS = cli._CODEQL_SUBCOMMANDS
_parse_codeql_version_stdout = cli._parse_codeql_version_stdout
_version_token_from_line = cli._version_token_from_line
_reject_unsafe_option = cli._reject_unsafe_option
_resolve_codeql_exe = cli._resolve_codeql_exe

_cache_dir = cache._cache_dir
_cache_base_dir = cache._cache_base_dir
_cache_is_valid = cache._cache_is_valid
_cache_meta_path = cache._cache_meta_path
_cache_metadata = cache._cache_metadata
_ensure_regular_file = cache._ensure_regular_file
_load_results_cache = cache._load_results_cache
_refuse_symlink_cache_path = cache._refuse_symlink_cache_path
_results_cache_path = cache._results_cache_path
_save_results_cache = cache._save_results_cache
_validate_cached_evidence_rows = cache._validate_cached_evidence_rows
_validate_one_cached_row = cache._validate_one_cached_row
_write_cache_metadata = cache._write_cache_metadata

_cache_key = cache_keys._cache_key
_hash_from_repo_walk = cache_keys._hash_from_repo_walk
_hash_from_scan_context = cache_keys._hash_from_scan_context
_hash_one_walk_file = cache_keys._hash_one_walk_file
_is_codeql_hash_file = cache_keys._is_codeql_hash_file
_is_codeql_walk_filename = cache_keys._is_codeql_walk_filename
_prune_hash_walk_dirs = cache_keys._prune_hash_walk_dirs
_query_pack_hash = cache_keys._query_pack_hash
_repo_content_hash = cache_keys._repo_content_hash

DEFAULT_PACK_DIR = database.DEFAULT_PACK_DIR
create_database = database.create_database
install_pack = database.install_pack
_ensure_codeql_database = database._ensure_codeql_database
_prepare_scan_targets = database._prepare_scan_targets
_reuse_or_rebuild_cached_db = database._reuse_or_rebuild_cached_db

decode_bqrs = queries.decode_bqrs
discover_queries = queries.discover_queries
run_all_queries = queries.run_all_queries
run_query = queries.run_query
_rows_from_bqrs_json = queries._rows_from_bqrs_json


def _validated_build_command(build_command: str) -> str:
    try:
        return validate_build_command(build_command)
    except BuildCommandError as exc:
        raise CodeQLError(str(exc)) from exc


def _load_cached_scan_rows(
    *,
    using_cache: bool,
    scanner_version: Optional[str],
    repo_path: Path,
    pack_dir: Path,
    build_command: str,
    scan_context: Any,
    cli_version: str,
) -> Optional[List[Dict[str, Any]]]:
    """Return results-cache rows when cache+version allow a full skip."""
    if not (using_cache and scanner_version):
        return None
    return cache._load_results_cache(
        repo_path,
        pack_dir,
        build_command,
        scanner_version,
        scan_context=scan_context,
        codeql_cli_version=cli_version,
    )


def _run_queries_and_maybe_cache(
    *,
    codeql_path: Path,
    repo_path: Path,
    db_path: Path,
    pack_dir: Path,
    build_command: str,
    using_cache: bool,
    scanner_version: Optional[str],
    scan_context: Any,
    cli_version: str,
    tmp: Path,
) -> List[Dict[str, Any]]:
    rows = run_all_queries(codeql_path, db_path, pack_dir, tmp)
    if using_cache and scanner_version:
        _save_results_cache(
            repo_path,
            pack_dir,
            build_command,
            scanner_version,
            rows,
            scan_context=scan_context,
            codeql_cli_version=cli_version,
        )
    return rows


def _cleanup_scan_temps(db_path: Path, tmp: str, keep_database: bool) -> None:
    if not keep_database:
        shutil.rmtree(db_path, ignore_errors=True)
    shutil.rmtree(tmp, ignore_errors=True)


def scan_with_codeql(
    repo_path: Path,
    build_command: str,
    pack_dir: Optional[Path] = None,
    db_path: Optional[Path] = None,
    keep_database: bool = False,
    scanner_version: Optional[str] = None,
    scan_context: Any = None,
) -> List[Dict[str, Any]]:
    """End-to-end: create database, run queries, return evidence rows."""
    build_command = _validated_build_command(build_command)
    # Facade-local lookups so monkeypatch.setattr(runner, ...) keeps working.
    codeql_path = find_codeql()
    cli_version = codeql_version(codeql_path)
    pack_dir, db_path, using_cache, keep_database = _prepare_scan_targets(
        repo_path,
        build_command,
        pack_dir,
        db_path,
        keep_database,
        scan_context,
        cli_version,
    )

    cached_rows = _load_cached_scan_rows(
        using_cache=using_cache,
        scanner_version=scanner_version,
        repo_path=repo_path,
        pack_dir=pack_dir,
        build_command=build_command,
        scan_context=scan_context,
        cli_version=cli_version,
    )
    if cached_rows is not None:
        return cached_rows

    install_pack(codeql_path, pack_dir)

    tmp = tempfile.mkdtemp(prefix="codeql_stage0_")
    try:
        _ensure_codeql_database(
            codeql_path=codeql_path,
            repo_path=repo_path,
            db_path=db_path,
            pack_dir=pack_dir,
            build_command=build_command,
            using_cache=using_cache,
            keep_database=keep_database,
            scan_context=scan_context,
            cli_version=cli_version,
        )
        return _run_queries_and_maybe_cache(
            codeql_path=codeql_path,
            repo_path=repo_path,
            db_path=db_path,
            pack_dir=pack_dir,
            build_command=build_command,
            using_cache=using_cache,
            scanner_version=scanner_version,
            scan_context=scan_context,
            cli_version=cli_version,
            tmp=Path(tmp),
        )
    finally:
        _cleanup_scan_temps(db_path, tmp, keep_database)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "usage: python -m doc_engine.scanning.support._codeql_runner "
            "<repo_path> <build_command> [db_path]"
        )
        sys.exit(1)
    repo = Path(sys.argv[1])
    build = sys.argv[2]
    db = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    rows = scan_with_codeql(repo, build, db_path=db, keep_database=True)
    print(json.dumps({"row_count": len(rows), "sample": rows[:5]}, indent=2))
