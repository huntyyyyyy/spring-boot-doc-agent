"""Resolve OCS checkout paths for spring-signals plant preflight."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

OCS_REPO_ENV = "SPRING_SIGNALS_OCS_REPO"
# Same pointer as Stage-0 real-repo lane (never commit the path).
REAL_REPO_ENV = "DOC_ENGINE_REAL_REPO"
REAL_REPO_PATH_FILE = Path("local-runs") / "real-repo.path"


def env_checkout_paths() -> list[Path]:
    out: list[Path] = []
    for key in (OCS_REPO_ENV, REAL_REPO_ENV):
        raw = os.environ.get(key, "").strip()
        if raw:
            out.append(Path(raw))
    return out


def pointer_checkout_path(repo_root: Path) -> Optional[Path]:
    pointer = repo_root / REAL_REPO_PATH_FILE
    if not pointer.is_file():
        return None
    for line in pointer.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return Path(stripped)
    return None


def candidate_paths(repo_root: Path) -> list[Path]:
    """Configured OCS checkout paths (env first, then gitignored pointer)."""
    out = env_checkout_paths()
    pointed = pointer_checkout_path(repo_root)
    if pointed is not None:
        out.append(pointed)
    return out


def first_existing(candidates: list[Optional[Path]]) -> Optional[Path]:
    for path in candidates:
        if path is None:
            continue
        resolved = path.expanduser()
        if resolved.is_dir():
            return resolved.resolve()
    return None


def resolve_ocs_checkout(repo_root: Path) -> Optional[Path]:
    """Env wins, then gitignored pointer file (same doctrine as real_fixture)."""
    return first_existing(list(candidate_paths(repo_root)))


def missing_checkout_reason(repo_root: Path) -> str:
    configured = candidate_paths(repo_root)
    if not configured:
        return (
            "ocs plant needs a checkout: set DOC_ENGINE_REAL_REPO or "
            "SPRING_SIGNALS_OCS_REPO, or local-runs/real-repo.path"
        )
    shown = ", ".join(repr(str(path)) for path in configured)
    return (
        "ocs plant checkout configured but not a directory on this machine: "
        f"{shown} — fix the path, or sync the tree onto this host"
    )
