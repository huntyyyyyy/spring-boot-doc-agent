"""Token estimation and path helpers for partition_repo."""

from __future__ import annotations

import os

from doc_engine.tools.partition_repo_constants import (
    CHARS_PER_TOKEN_DEFAULT,
    CHARS_PER_TOKEN_DENSE,
    DENSE_EXTS,
)


def _decode_file_bytes(chunk: bytes):
    """Return (text, skip_reason). skip_reason is set when undecodable."""
    if b"\x00" in chunk[:8000]:
        return None, "binary"
    try:
        return chunk.decode("utf-8"), None
    except UnicodeDecodeError:
        try:
            return chunk.decode("latin-1"), None
        except Exception:
            return None, "undecodable"


def _read_file_bytes(path: str, size: int):
    try:
        with open(path, "rb") as handle:
            return handle.read(size), None
    except OSError:
        return None, "read-failed"


def estimate_tokens(path, max_file_bytes):
    """Cheap token estimate: chars / N, where N is CHARS_PER_TOKEN_DENSE for
    structured-data extensions (DENSE_EXTS) and CHARS_PER_TOKEN_DEFAULT
    otherwise. Skips files that look binary or are too large; returns
    (tokens, skipped_reason_or_None)."""
    try:
        size = os.path.getsize(path)
    except OSError:
        return 0, "stat-failed"
    if size > max_file_bytes:
        return 0, f"too-large ({size} bytes)"
    chunk, read_error = _read_file_bytes(path, size)
    if read_error:
        return 0, read_error
    text, decode_error = _decode_file_bytes(chunk)
    if decode_error:
        return 0, decode_error
    _, extension = os.path.splitext(path)
    divisor = (
        CHARS_PER_TOKEN_DENSE
        if extension.lower() in DENSE_EXTS
        else CHARS_PER_TOKEN_DEFAULT
    )
    return max(1, len(text) // divisor), None


def to_posix(path: str) -> str:
    """Backslashes to forward slashes. Trivial, and deliberately its own
    named function rather than an inline .replace() repeated at each site.

    Every artifact this pipeline writes keys on relative paths, and separate
    scripts' outputs are then joined by those paths -- groups.json against
    spring_signals.json, spring_signals.json against a doc's [Evidenced —
    path:line] citation. A backslash on one side of that join and a forward
    slash on the other matches nothing and raises no error; the consumer just
    receives an empty slice. That failure has now been found and fixed three
    separate times (spring_drift_check.py's tier1_scan(), partition_repo's own
    main(), and capacity_preflight.py's compute_preflight() on 2026-07-25),
    which is the signal that the fix belonged in one named place rather than
    in a comment telling the next author to remember."""
    return path.replace("\\", "/")


def relpath_posix(full: str, root: str) -> str:
    """os.path.relpath, normalized. The pairing above is the whole point:
    os.path.relpath is the thing that introduces the platform separator, so
    the normalization belongs immediately next to it."""
    return to_posix(os.path.relpath(full, root))

