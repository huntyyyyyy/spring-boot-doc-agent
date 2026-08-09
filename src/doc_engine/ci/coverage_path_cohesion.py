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


def _resolve_under_root(raw: str, root: Path) -> Path | None:
    root_res = root.resolve()
    candidate = Path(raw) if _looks_absolute(raw) else root_res / raw
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root_res)
        return resolved
    except (OSError, ValueError):
        return None


class PathCohesionGuard:
    """Behavioral check: every report source path belongs to *repo_root*."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root.resolve()

    def violations(self, paths: list[str]) -> list[str]:
        """Return human-readable violations (empty means cohesive)."""
        root_name = self.repo_root.name
        out: list[str] = []
        for raw in paths:
            if not raw or not str(raw).strip():
                continue
            norm = normalize_source_path(raw)
            if _resolve_under_root(raw, self.repo_root) is not None:
                continue
            foreign = _foreign_segment(norm)
            if foreign and foreign != root_name:
                out.append(f"foreign worktree segment {foreign!r}: {norm}")
            else:
                out.append(f"path escapes repo root {self.repo_root}: {norm}")
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
