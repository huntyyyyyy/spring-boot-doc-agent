"""Sizing inventory: file LOC and per-function statement counts.

Walks ``SIZE_ROOTS`` (production packages + ``tests/``). AST/filesystem
enumeration only — ceilings and baseline persistence stay in ``size_ratchet``.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from doc_engine.ci.gate_tools import REPO_ROOT

# Production packages plus tests — same 225 LOC cohesion bar on both.
SIZE_ROOTS = ("src/doc_engine", "src/stf", "tests")
# Backward-compatible alias (baseline payload historically used this key).
PACKAGE_ROOTS = SIZE_ROOTS


def line_count(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def _strip_leading_docstring(body: list) -> list:
    if not body:
        return body
    first = body[0]
    if not isinstance(first, ast.Expr):
        return body
    value = getattr(first, "value", None)
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return body[1:]
    return body


def _is_definition(stmt: ast.AST) -> bool:
    return isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))


def statement_count(node: ast.AST) -> int:
    """Count statements in *node*, excluding docstring and nested defs."""
    total = 0
    stack = list(_strip_leading_docstring(list(getattr(node, "body", []))))
    while stack:
        stmt = stack.pop()
        if _is_definition(stmt):
            continue
        total += 1
        stack.extend(_nested_blocks(stmt))
    return total


def _nested_blocks(stmt: ast.AST) -> list:
    nested: list = []
    for field in ("body", "orelse", "finalbody", "handlers"):
        nested.extend(getattr(stmt, field, []) or [])
    return nested


def _record_function(
    child: ast.AST, prefix: str, relpath: str, out: Dict[str, int]
) -> str:
    qual = f"{prefix}{child.name}"
    key = f"{relpath}::{qual}"
    stmts = statement_count(child)
    prior = out.get(key)
    out[key] = stmts if prior is None else max(prior, stmts)
    return qual


def _visit_child(
    child: ast.AST, prefix: str, relpath: str, out: Dict[str, int]
) -> None:
    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
        qual = _record_function(child, prefix, relpath, out)
        _visit_functions(child, f"{qual}.", relpath, out)
        return
    if isinstance(child, ast.ClassDef):
        _visit_functions(child, f"{prefix}{child.name}.", relpath, out)
        return
    _visit_functions(child, prefix, relpath, out)


def _visit_functions(
    node: ast.AST, prefix: str, relpath: str, out: Dict[str, int]
) -> None:
    for child in ast.iter_child_nodes(node):
        _visit_child(child, prefix, relpath, out)


def _py_files_under(root: Path) -> List[Path]:
    return [
        path
        for path in sorted(root.rglob("*.py"))
        if "__pycache__" not in path.parts
    ]


def iter_package_py_files(roots: Iterable[str] = SIZE_ROOTS) -> List[Path]:
    """Return sorted ``.py`` paths under size roots (skip ``__pycache__``)."""
    files: List[Path] = []
    for root_name in roots:
        root = REPO_ROOT / root_name
        if root.is_dir():
            files.extend(_py_files_under(root))
    return files


def measure_tree(
    roots: Iterable[str] = SIZE_ROOTS,
) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Return (file_loc, function_statements) keyed by repo-relative paths."""
    file_loc: Dict[str, int] = {}
    functions: Dict[str, int] = {}
    for path in iter_package_py_files(roots):
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        file_loc[rel] = line_count(text)
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        _visit_functions(tree, "", rel, functions)
    return file_loc, functions
