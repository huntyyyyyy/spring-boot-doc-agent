"""Public-surface policy — fitness setpoints for curated façades (E-COH1).

Embody tach/Nx/Packwerk *public interface* patterns as an in-repo ratchet until
E-TACH0 Approves ``[[interfaces]]``. Do not expand tach.toml here.
"""

from __future__ import annotations

from pathlib import Path

from doc_engine.ci.gate_tools import REPO_ROOT

# Façades that must not list leading-underscore names in ``__all__``.
PUBLIC_ONLY_MODULES: tuple[str, ...] = (
    "doc_engine.tools.semantic_eval",
    "doc_engine.tools.semantic_eval_helpers",
    "doc_engine.pipeline.local_runner_phases",
)

# Residual-bin basenames refused under these package roots (COH3).
FORBIDDEN_BASENAMES: frozenset[str] = frozenset(
    {
        "support.py",
        "inventory_drift.py",
    }
)

FORBIDDEN_PACKAGE_ROOTS: tuple[str, ...] = (
    "src/doc_engine/pipeline/local_runner_phases",
)


def module_private_all_exports(module_name: str) -> list[str]:
    """Return ``__all__`` names that start with ``_`` (empty if no ``__all__``)."""
    import importlib

    mod = importlib.import_module(module_name)
    exported = getattr(mod, "__all__", None)
    if exported is None:
        return []
    return [name for name in exported if name.startswith("_")]


def _residual_hits_under(base: Path, repo_root: Path) -> list[str]:
    return [
        path.relative_to(repo_root).as_posix()
        for path in sorted(base.glob("*.py"))
        if path.name in FORBIDDEN_BASENAMES
    ]


def forbidden_residual_paths(repo_root: Path = REPO_ROOT) -> list[str]:
    """List residual-bin paths that still exist under curated package roots."""
    hits: list[str] = []
    for root in FORBIDDEN_PACKAGE_ROOTS:
        base = repo_root / root
        if base.is_dir():
            hits.extend(_residual_hits_under(base, repo_root))
    return hits
