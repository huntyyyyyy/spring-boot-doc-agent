"""PathCohesionGuard — coverage report paths must stay in one checkout.

Rejects Cobertura filenames that escape the active git worktree (absolute
paths into a sibling ``wt-*`` tree, ``..`` climbs, foreign worktree segments).

Usage:
    from doc_engine.ci.coverage_path_cohesion import PathCohesionGuard
    PathCohesionGuard(repo_root).assert_cohesive(paths)
"""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath, PureWindowsPath

_FOREIGN_SEGMENT_RE = re.compile(
    r"(?i)(^|[/\\])(wt-cov-[^/\\]*|wt-complexity-[^/\\]*|wt-pr\d+|wt-size-[^/\\]*|"
    r"wt-mutation-[^/\\]*)([/\\]|$)"
)


class PathCohesionError(ValueError):
    """Coverage report paths are not cohesive with the active repo root."""


def normalize_source_path(raw: str) -> str:
    """Normalize separators to POSIX for stable comparison / display."""
    return raw.replace("\\", "/").strip()


def _looks_absolute(raw: str) -> bool:
    text = raw.strip()
    if not text:
        return False
    if PureWindowsPath(text).is_absolute() or PurePosixPath(text).is_absolute():
        return True
    return bool(re.match(r"^[A-Za-z]:[/\\]", text))


def _foreign_segment(raw: str) -> str | None:
    match = _FOREIGN_SEGMENT_RE.search(normalize_source_path(raw))
    return match.group(2) if match else None


def _candidate_under_root(raw: str, root: Path) -> Path:
    """Build a path to resolve under *root*.

    Windows drive paths look absolute to :func:`_looks_absolute` but are
    relative ``pathlib.Path`` objects on POSIX; resolving them would join the
    checkout (``/repo/C:/Users/...``) and falsely pass cohesion.
    """
    if not _looks_absolute(raw):
        return root / raw
    candidate = Path(raw)
    if not candidate.is_absolute():
        raise ValueError("foreign-os absolute path")
    return candidate


def _resolve_under_root(raw: str, root: Path) -> Path | None:
    """Return resolved path when *raw* is inside *root*; else None."""
    root_res = root.resolve()
    try:
        resolved = _candidate_under_root(raw, root_res).resolve()
        resolved.relative_to(root_res)
        return resolved
    except (OSError, ValueError):
        return None


def _blank_source_path(raw: str) -> bool:
    return not raw or not str(raw).strip()


def _escape_violation_message(raw: str, repo_root: Path, root_name: str) -> str:
    """Describe why *raw* is not cohesive with *repo_root* (already escaped)."""
    norm = normalize_source_path(raw)
    foreign = _foreign_segment(norm)
    if foreign and foreign != root_name:
        return f"foreign worktree segment {foreign!r}: {norm}"
    return f"path escapes repo root {repo_root}: {norm}"


def _violation_for_path(raw: str, repo_root: Path, root_name: str) -> str | None:
    """Return a violation message for *raw*, or None when cohesive / blank."""
    if _blank_source_path(raw):
        return None
    if _resolve_under_root(raw, repo_root) is not None:
        return None
    return _escape_violation_message(raw, repo_root, root_name)


class PathCohesionGuard:
    """Behavioral check: every report source path belongs to *repo_root*."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root.resolve()

    def violations(self, paths: list[str]) -> list[str]:
        """Return human-readable violations (empty means cohesive)."""
        root_name = self.repo_root.name
        out: list[str] = []
        for raw in paths:
            message = _violation_for_path(raw, self.repo_root, root_name)
            if message is not None:
                out.append(message)
        return out

    def assert_cohesive(self, paths: list[str]) -> None:
        """Raise :class:`PathCohesionError` when any source path is foreign."""
        bad = self.violations(paths)
        if not bad:
            return
        detail = "; ".join(bad[:8])
        extra = f" (+{len(bad) - 8} more)" if len(bad) > 8 else ""
        raise PathCohesionError(
            "coverage report path cohesion failed — refuse gap-average / measure "
            f"on a cross-worktree or escaped report ({len(bad)} path(s)): "
            f"{detail}{extra}"
        )


def cohesion_violations(paths: list[str], repo_root: Path) -> list[str]:
    """Compat: list violations for *paths* vs *repo_root*."""
    return PathCohesionGuard(repo_root).violations(paths)


def assert_paths_cohesive(paths: list[str], repo_root: Path) -> None:
    """Compat: raise when any path escapes *repo_root*."""
    PathCohesionGuard(repo_root).assert_cohesive(paths)
