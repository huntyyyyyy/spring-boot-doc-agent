"""G2 split_scope_break witness: prelude/core pairs must not leak Locals.

E-HOT1-A / finding G2 — structural Accept for statement-chop handoffs.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from doc_engine.paths import repo_root

pytestmark = pytest.mark.domain_ci_meta

_SKIP_PARTS = frozenset({".venv", "venv", "__pycache__", ".git"})

def _assigned_names(prelude: ast.AST) -> set[str]:
    assigned: set[str] = set()
    for node in ast.walk(prelude):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assigned.add(node.target.id)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                assigned.add(alias.asname or alias.name)
    return assigned

def _core_load_names(core: ast.AST) -> set[str]:
    return {
        node.id
        for node in ast.walk(core)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }

def _leaks_for_pair(prelude: ast.AST, core: ast.AST) -> list[str]:
    params = {arg.arg for arg in core.args.args + core.args.kwonlyargs}
    leaked = (_assigned_names(prelude) & _core_load_names(core)) - params - {"self", "cls"}
    return sorted(leaked)

def _prelude_core_leaks(tree: ast.AST) -> list[tuple[str, list[str]]]:
    by_name = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    leaks: list[tuple[str, list[str]]] = []
    for name, prelude in by_name.items():
        if not name.endswith("_prelude"):
            continue
        core = by_name.get(name[: -len("_prelude")] + "_core")
        if core is None:
            continue
        leaked = _leaks_for_pair(prelude, core)
        if leaked:
            leaks.append((name, leaked))
    return leaks

def test_no_prelude_core_local_leaks_in_repo() -> None:
    """Fail while any *_prelude assigns names *_core Loads without params."""
    root = repo_root()
    offenders: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if _SKIP_PARTS.intersection(path.parts):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        for prelude_name, leaked in _prelude_core_leaks(tree):
            rel = path.relative_to(root).as_posix()
            offenders.append(f"{rel}::{prelude_name} leaks {leaked}")
    assert offenders == [], "G2 split_scope_break:\n" + "\n".join(offenders)
