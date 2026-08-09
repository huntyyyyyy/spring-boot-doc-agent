"""Argv chunking for ast-grep path lists (WinError 206 CreateProcess budget)."""

from __future__ import annotations

import sys
from typing import List

# Windows CreateProcess fails with WinError 206 when hundreds of absolute paths
# are passed as separate argv entries. Chunking preserves ScanContext inventory.
_PATH_LIST_CHAR_LIMIT = 7000 if sys.platform == "win32" else 2 ** 31


def _argv_char_len(parts: List[str]) -> int:
    return sum(len(part) + 1 for part in parts)


def _flush_path_chunk(
    chunks: List[List[str]],
    current: List[str],
) -> List[str]:
    """Append *current* to *chunks* and return a fresh empty chunk list."""
    chunks.append(current)
    return []


def _append_path_within_budget(
    path: str,
    budget: int,
    chunks: List[List[str]],
    current: List[str],
    current_len: int,
) -> tuple[List[str], int]:
    """Add one path to the active chunk, flushing when the budget would break."""
    cost = len(path) + 1
    if current and current_len + cost > budget:
        current = _flush_path_chunk(chunks, current)
        current_len = 0
    current.append(path)
    current_len += cost
    if current_len > budget and len(current) == 1:
        current = _flush_path_chunk(chunks, current)
        current_len = 0
    return current, current_len


def chunk_paths_for_argv(
    base_argv: List[str],
    paths: List[str],
    limit: int,
) -> List[List[str]]:
    """Partition ``paths`` so each ``base_argv + chunk`` stays within ``limit`` chars."""
    if not paths:
        return []
    budget = max(limit - _argv_char_len(base_argv), 1)
    chunks: List[List[str]] = []
    current: List[str] = []
    current_len = 0
    for path in paths:
        current, current_len = _append_path_within_budget(
            path, budget, chunks, current, current_len
        )
    if current:
        chunks.append(current)
    return chunks


def is_windows_cmdline_too_long(exc: OSError) -> bool:
    return getattr(exc, "winerror", None) == 206
