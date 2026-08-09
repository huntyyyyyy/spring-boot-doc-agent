"""Invoke / bisect / chunked ast-grep subprocess runs."""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

from doc_engine.scanning.astgrep.argv import (
    chunk_paths_for_argv,
    is_windows_cmdline_too_long,
)
from doc_engine.scanning.astgrep.errors import AstGrepError, AstGrepNotFoundError
from doc_engine.scanning.astgrep.ports import DEFAULT_RUNNER, AstGrepRunner


def parse_ast_grep_stdout(stdout: str) -> List[Dict[str, Any]]:
    """Parse compact JSON stdout from one ast-grep invocation."""
    try:
        return json.loads(stdout) if stdout.strip() else []
    except json.JSONDecodeError as exc:
        raise AstGrepError(f"ast-grep output is not valid JSON: {exc}") from exc


def scan_base_argv(ast_grep_path: str, rule_file: Any) -> List[str]:
    return [
        ast_grep_path, "scan",
        "--rule", str(rule_file),
        "--json=compact",
        "--no-ignore", "hidden",
        "--no-ignore", "dot",
        "--no-ignore", "vcs",
        "--no-ignore", "parent",
        "--no-ignore", "global",
        "--no-ignore", "exclude",
    ]


def require_ast_grep_ready(find_binary, rule_file: Any) -> str:
    """Return the ast-grep binary path or raise a NotFound error."""
    ast_grep_path = find_binary()
    if ast_grep_path is None:
        raise AstGrepNotFoundError(
            "ast-grep binary is not on PATH. "
            "Install ast-grep to enable this backend."
        )
    if not rule_file.is_file():
        raise AstGrepNotFoundError(f"ast-grep rule file not found: {rule_file}")
    return ast_grep_path


def invoke_ast_grep(
    cmd: List[str],
    *,
    runner: Optional[AstGrepRunner] = None,
) -> List[Dict[str, Any]]:
    """Run one ast-grep argv; raise on any process/JSON failure (fail-closed)."""
    active = runner if runner is not None else DEFAULT_RUNNER
    try:
        proc = active.run(cmd)
    except OSError as exc:
        if is_windows_cmdline_too_long(exc):
            raise
        raise AstGrepError(f"ast-grep failed to start: {exc}") from exc
    if proc.returncode != 0:
        raise AstGrepError(
            f"ast-grep exited with status {proc.returncode}: "
            f"{(proc.stderr or '').strip()}"
        )
    return parse_ast_grep_stdout(proc.stdout)


def bisect_oversized_chunk(
    backend: Any,
    base_argv: List[str],
    chunk: List[str],
    char_limit: int,
) -> tuple[List[Dict[str, Any]], int]:
    """Bisect a WinError-206 chunk; return (matches, additional_bisects)."""
    if len(chunk) == 1:
        raise AstGrepError(
            "single Java path exceeds CreateProcess argv limit; "
            f"incomplete inventory: {chunk[0]}"
        )
    mid = len(chunk) // 2
    print(
        "warning: CreateProcess WinError 206 on a path batch "
        f"({len(chunk)} files); bisecting and retrying",
        file=sys.stderr,
    )
    left, _left_batches, left_bisects = backend._invoke_ast_grep_chunked(
        base_argv, chunk[:mid], limit=char_limit,
    )
    right, _right_batches, right_bisects = backend._invoke_ast_grep_chunked(
        base_argv, chunk[mid:], limit=char_limit,
    )
    return left + right, 1 + left_bisects + right_bisects


def scan_one_chunk(
    backend: Any,
    base_argv: List[str],
    chunk: List[str],
    char_limit: int,
) -> tuple[List[Dict[str, Any]], int]:
    """Scan one argv chunk; bisect on WinError 206. Returns (matches, bisects)."""
    try:
        return backend._invoke_ast_grep(base_argv + chunk), 0
    except OSError as exc:
        if not is_windows_cmdline_too_long(exc):
            raise
        return bisect_oversized_chunk(backend, base_argv, chunk, char_limit)


def invoke_ast_grep_chunked(
    backend: Any,
    base_argv: List[str],
    paths: List[str],
    *,
    limit: Optional[int] = None,
) -> tuple[List[Dict[str, Any]], int, int]:
    """Scan paths in argv chunks. Returns (matches, batch_count, bisects)."""
    from doc_engine.scanning import _scanner_astgrep as facade

    char_limit = (
        facade._PATH_LIST_CHAR_LIMIT if limit is None else limit
    )
    chunks = chunk_paths_for_argv(base_argv, paths, char_limit)
    if len(chunks) > 1:
        print(
            "warning: Java path list exceeds this platform's command-line "
            f"budget ({len(paths)} files); scanning in {len(chunks)} "
            "ast-grep batches to preserve ScanContext inventory",
            file=sys.stderr,
        )
    matches: List[Dict[str, Any]] = []
    bisects = 0
    for chunk in chunks:
        chunk_matches, chunk_bisects = scan_one_chunk(
            backend, base_argv, chunk, char_limit
        )
        matches.extend(chunk_matches)
        bisects += chunk_bisects
    return matches, len(chunks), bisects
