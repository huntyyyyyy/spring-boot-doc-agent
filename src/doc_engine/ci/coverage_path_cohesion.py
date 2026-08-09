"""Guard: coverage report source paths must stay inside one checkout.

Rejects Cobertura ``filename`` values that escape the active git worktree
(absolute paths into a sibling ``wt-*`` tree, ``..`` climbs, or foreign
worktree directory segments). Callers such as gap-average depend on this
check — never on ``cwd`` accidentally holding another tree's XML.

Usage:
    from doc_engine.ci.coverage_path_cohesion import assert_paths_cohesive
    assert_paths_cohesive(paths, repo_root)
"""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath, PureWindowsPath

# Sibling climb/measure worktrees and the recurring defect prefix.
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
    if not match:
        return None
    return match.group(2)


def _resolve_under_root(raw: str, root: Path) -> Path | None:
    """Return resolved path if it stays under *root*, else ``None``."""
    root_res = root.resolve()
    candidate = Path(raw)
    if not _looks_absolute(raw):
        candidate = root_res / raw
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root_res)
        return resolved
    except (OSError, ValueError):
        return None


def cohesion_violations(paths: list[str], repo_root: Path) -> list[str]:
    """Return human-readable violations for *paths* vs *repo_root*."""
    root = repo_root.resolve()
    root_name = root.name
    violations: list[str] = []
    for raw in paths:
        if not raw or not str(raw).strip():
            continue
        norm = normalize_source_path(raw)
        # Paths that resolve inside this checkout are cohesive even when the
        # worktree directory itself is named wt-cov-* (measure trees).
        if _resolve_under_root(raw, root) is not None:
            continue
        foreign = _foreign_segment(norm)
        if foreign and foreign != root_name:
            violations.append(f"foreign worktree segment {foreign!r}: {norm}")
            continue
        violations.append(f"path escapes repo root {root}: {norm}")
    return violations


def assert_paths_cohesive(paths: list[str], repo_root: Path) -> None:
    """Raise :class:`PathCohesionError` when any source path is foreign."""
    bad = cohesion_violations(paths, repo_root)
    if not bad:
        return
    detail = "; ".join(bad[:8])
    extra = f" (+{len(bad) - 8} more)" if len(bad) > 8 else ""
    raise PathCohesionError(
        "coverage report path cohesion failed — refuse gap-average / measure "
        f"on a cross-worktree or escaped report ({len(bad)} path(s)): "
        f"{detail}{extra}"
    )
