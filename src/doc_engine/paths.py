"""Portable path resolution for the doc-engine kernel.

Kernel code uses these helpers instead of CLAUDE_PLUGIN_ROOT. Adapters may
still use CLAUDE_PLUGIN_ROOT for agent prompt paths only.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from doc_engine.core.walk import is_path_inside_root


class PathValidationError(ValueError):
    """CLI/LLM-supplied path failed kind or containment checks."""


_KIND_PREDICATES: dict[str, tuple[Callable[[Path], bool], str]] = {
    "file": (Path.is_file, "not a file"),
    "dir": (Path.is_dir, "not a directory"),
}


def _reject_dotdot_segments(raw: Path, *, display: str | Path) -> None:
    if ".." in raw.parts:
        raise PathValidationError(f"path must not contain '..': {display}")


def _resolve_or_validation_error(raw: Path, *, display: str | Path) -> Path:
    try:
        return raw.resolve()
    except OSError as exc:
        raise PathValidationError(f"cannot resolve path: {display}") from exc


def _require_existing_kind(resolved: Path, want: str) -> None:
    entry = _KIND_PREDICATES.get(want)
    if entry is None:
        raise ValueError(f"unknown want={want!r}")
    predicate, message = entry
    if not predicate(resolved):
        raise PathValidationError(f"{message}: {resolved}")


def checked_path(path: str | Path, *, want: str) -> Path:
    """Validate a user-supplied path before any filesystem access.

    Rejects ``..`` segments, resolves symlinks, then requires the expected
    kind (``file`` or ``dir``). Matches the containment pattern Sonar S2083
    expects for CLI-tainted paths.
    """
    raw = Path(path)
    _reject_dotdot_segments(raw, display=path)
    resolved = _resolve_or_validation_error(raw, display=path)
    _require_existing_kind(resolved, want)
    return resolved


def _require_output_parent_and_file_slot(resolved: Path) -> None:
    parent = resolved.parent
    if not parent.is_dir():
        raise PathValidationError(f"output parent is not a directory: {parent}")
    if resolved.exists() and not resolved.is_file():
        raise PathValidationError(
            f"output path exists and is not a file: {resolved}"
        )


def checked_output_path(path: str | Path) -> Path:
    """Validate a user-supplied output path (file may not exist yet).

    Rejects ``..``, resolves, requires an existing parent directory, and
    refuses to overwrite a non-file at the destination.
    """
    raw = Path(path)
    _reject_dotdot_segments(raw, display=path)
    resolved = _resolve_or_validation_error(raw, display=path)
    _require_output_parent_and_file_slot(resolved)
    return resolved


def _reject_unsafe_join_component(part: str | Path) -> None:
    component = Path(part)
    if component.is_absolute() or ".." in component.parts:
        raise PathValidationError(f"refusing unsafe path component: {part!r}")


def _resolve_base_or_raise(base: str | Path) -> Path:
    try:
        return Path(base).resolve()
    except OSError as exc:
        raise PathValidationError(f"cannot resolve base path: {base}") from exc


def _require_inside_base(resolved: Path, base_resolved: Path) -> None:
    if not is_path_inside_root(str(resolved), str(base_resolved)):
        raise PathValidationError(
            f"path escapes base directory {base_resolved}: {resolved}"
        )


def join_under(base: str | Path, *parts: str | Path) -> Path:
    """Join *parts* under *base* and require the result stay inside *base*.

    Absolute components are rejected (``os.path.join`` would discard *base*).
    """
    base_resolved = _resolve_base_or_raise(base)
    for part in parts:
        _reject_unsafe_join_component(part)
    candidate = base_resolved.joinpath(*parts)
    resolved = _resolve_or_validation_error(candidate, display=candidate)
    _require_inside_base(resolved, base_resolved)
    return resolved


def repo_root() -> Path:
    """Repository root in editable installs (src/doc_engine/paths.py → parents[2])."""
    return Path(__file__).resolve().parents[2]


def scripts_dir() -> Path:
    return repo_root() / "scripts"


def scripts_meta_path_entries() -> list[str]:
    """``sys.path`` entries for bare imports of nested meta modules.

    Meta CLIs live under ``scripts/{ci,ratchets,coverage,fixtures}`` after the
    subdir layout. Tests and cross-bucket imports insert these leaves so
    ``import check_repo_claims`` / ``import mutate`` keep working without
    dual-home shims at ``scripts/*.py``.
    """
    root = scripts_dir()
    return [str(root / name) for name in ("ci", "ratchets", "coverage", "fixtures")]


def codeql_dir() -> Path:
    return repo_root() / "codeql"


def schemas_dir() -> Path:
    return scripts_dir() / "schemas"


def codeql_pack_dir() -> Path:
    return codeql_dir() / "spring-signals"


def ast_grep_rules_path() -> Path:
    packaged = (
        Path(__file__).resolve().parent
        / "scanning"
        / "resources"
        / "spring_ast_grep_rules.yml"
    )
    if packaged.is_file():
        return packaged
    return repo_root() / "scripts" / "spring_ast_grep_rules.yml"
