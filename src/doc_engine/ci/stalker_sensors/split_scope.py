"""G2: prelude/core pairs must not leak Locals (split_scope_break)."""

from __future__ import annotations

import ast
from pathlib import Path

from doc_engine.ci.stalker_sensors.finding_records import KIND_G2, StalkerFinding

_SKIP_PARTS = frozenset({".venv", "venv", "__pycache__", ".git"})


def _add_name_target(assigned: set[str], target: ast.AST) -> None:
    if isinstance(target, ast.Name):
        assigned.add(target.id)


def _add_assign_targets(assigned: set[str], node: ast.AST) -> None:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            _add_name_target(assigned, target)
        return
    if isinstance(node, ast.AnnAssign):
        _add_name_target(assigned, node.target)


def _add_import_aliases(assigned: set[str], node: ast.AST) -> None:
    if not isinstance(node, ast.ImportFrom):
        return
    for alias in node.names:
        assigned.add(alias.asname or alias.name)


def assigned_names(prelude: ast.AST) -> set[str]:
    assigned: set[str] = set()
    for node in ast.walk(prelude):
        _add_assign_targets(assigned, node)
        _add_import_aliases(assigned, node)
    return assigned


def core_load_names(core: ast.AST) -> set[str]:
    return {
        node.id
        for node in ast.walk(core)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }


def leaks_for_pair(prelude: ast.AST, core: ast.AST) -> list[str]:
    params = {arg.arg for arg in core.args.args + core.args.kwonlyargs}
    leaked = (assigned_names(prelude) & core_load_names(core)) - params - {"self", "cls"}
    return sorted(leaked)


def _fn_map(tree: ast.AST) -> dict[str, ast.AST]:
    return {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _leak_entry(
    by_name: dict[str, ast.AST], name: str, prelude: ast.AST
) -> tuple[str, list[str]] | None:
    if not name.endswith("_prelude"):
        return None
    core = by_name.get(name[: -len("_prelude")] + "_core")
    if core is None:
        return None
    leaked = leaks_for_pair(prelude, core)
    if not leaked:
        return None
    return (name, leaked)


def prelude_core_leaks(tree: ast.AST) -> list[tuple[str, list[str]]]:
    by_name = _fn_map(tree)
    leaks: list[tuple[str, list[str]]] = []
    for name, prelude in by_name.items():
        entry = _leak_entry(by_name, name, prelude)
        if entry is not None:
            leaks.append(entry)
    return leaks


def _findings_for_path(root: Path, path: Path) -> list[StalkerFinding]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return []
    rel = path.relative_to(root).as_posix()
    return [
        StalkerFinding(
            KIND_G2,
            f"{rel}::{prelude_name} leaks {leaked}",
            "pass prelude locals into _core params",
        )
        for prelude_name, leaked in prelude_core_leaks(tree)
    ]


def scan_split_scope(root: Path) -> list[StalkerFinding]:
    findings: list[StalkerFinding] = []
    for path in sorted(root.rglob("*.py")):
        if _SKIP_PARTS.intersection(path.parts):
            continue
        findings.extend(_findings_for_path(root, path))
    return findings
