"""Standing fitness: control-plane tests must not be check-free.

Catches the open-loop pattern where a ``test_*`` exists (Cover% / discovery)
but performs no assert / pytest.raises / unittest assertion — so it cannot
fail closed. Scoped to ``tests/ci`` + ``tests/adapters`` (gate/hook surface).

Follows one level of same-module ``_test_*`` helpers (statement-split prelude/
core pattern) so split wrappers are not false positives.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.domain_ci_meta

REPO = Path(__file__).resolve().parents[2]
SCAN_ROOTS = (REPO / "tests" / "ci", REPO / "tests" / "adapters")

_UNITTEST = {
    "assertEqual",
    "assertTrue",
    "assertFalse",
    "assertIn",
    "assertNotIn",
    "assertRaises",
    "assertIs",
    "assertIsNone",
    "assertIsNotNone",
    "assertAlmostEqual",
    "assertGreater",
    "assertLess",
    "assertRegex",
    "assertCountEqual",
    "fail",
}
_PYTEST_CTX = {"raises", "warns", "deprecated_call"}


def _direct_check(node: ast.AST) -> bool:
    for child in ast.walk(node):
        if isinstance(child, ast.Assert):
            return True
        if isinstance(child, ast.With):
            for item in child.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr in _PYTEST_CTX:
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
            if child.func.attr in _UNITTEST or child.func.attr.startswith("assert"):
                return True
    return False


def _called_helper_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for child in ast.walk(node):
        if not isinstance(child, ast.Call) or not isinstance(child.func, ast.Name):
            continue
        if child.func.id.startswith("_test_"):
            names.add(child.func.id)
    return names


def _module_helpers(tree: ast.AST) -> dict[str, ast.AST]:
    out: dict[str, ast.AST] = {}
    for node in tree.body if isinstance(tree, ast.Module) else []:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_test_"):
                out[node.name] = node
    return out


def _has_check(node: ast.AST, helpers: dict[str, ast.AST]) -> bool:
    if _direct_check(node):
        return True
    for name in _called_helper_names(node):
        helper = helpers.get(name)
        if helper is not None and _direct_check(helper):
            return True
    return False


def _check_free_tests(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return [f"{path}: syntax error"]
    helpers = _module_helpers(tree)
    hits: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _has_check(node, helpers):
            rel = path.relative_to(REPO).as_posix()
            hits.append(f"{rel}:{node.lineno}:{node.name}")
    return hits


def test_ci_and_adapter_suites_are_not_check_free() -> None:
    """Fail closed: a discovered test with no check is Cover% theater."""
    problems: list[str] = []
    for root in SCAN_ROOTS:
        for path in sorted(root.rglob("test_*.py")):
            problems.extend(_check_free_tests(path))
    assert problems == [], (
        "check-free tests (no assert / raises / unittest assert*) — "
        "add a real fail-closed check or delete the test:\n  "
        + "\n  ".join(problems)
    )
