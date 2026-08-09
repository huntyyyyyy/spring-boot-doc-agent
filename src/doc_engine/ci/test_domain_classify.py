"""Classify test modules and read/write declared ``domain_*`` markers."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from doc_engine.ci.test_domain_catalog import known_markers
from doc_engine.ci.test_domain_rules import CLASSIFICATION_RULES

_DOMAIN_ATTR = re.compile(r"^domain_[a-z0-9_]+$")
_PYTESTMARK_ASSIGN = re.compile(
    r"^pytestmark\s*=\s*pytest\.mark\.(domain_[a-z0-9_]+)\s*$",
    re.MULTILINE,
)


def iter_test_modules(repo_root: Path) -> list[Path]:
    """All ``test_*.py`` under ``tests/`` (skip caches)."""
    tests_root = repo_root / "tests"
    if not tests_root.is_dir():
        return []
    return sorted(
        path
        for path in tests_root.rglob("test_*.py")
        if "__pycache__" not in path.parts
    )


def classify_test_path(repo_root: Path, test_file: Path) -> str:
    """Return catalog marker for *test_file* via ordered rules."""
    rel = test_file.resolve().relative_to(repo_root.resolve()).as_posix()
    filename = test_file.name
    for rule in CLASSIFICATION_RULES:
        marker = rule.match(rel, filename)
        if marker is not None:
            return marker
    raise RuntimeError(f"no classification rule matched {rel}")


def declared_domain_markers(source: str) -> list[str]:
    """Domain markers declared via module ``pytestmark`` (AST + line form)."""
    found = _line_form_markers(source)
    found.extend(_ast_pytestmark_markers(source))
    return _dedupe_known_markers(found)


def _line_form_markers(source: str) -> list[str]:
    return [match.group(1) for match in _PYTESTMARK_ASSIGN.finditer(source)]


def _ast_pytestmark_markers(source: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    found: list[str] = []
    for node in tree.body:
        found.extend(_markers_from_assign(node))
    return found


def _markers_from_assign(node: ast.AST) -> list[str]:
    if not isinstance(node, ast.Assign):
        return []
    if not _assigns_pytestmark(node):
        return []
    return _markers_from_pytestmark_value(node.value)


def _assigns_pytestmark(node: ast.Assign) -> bool:
    return any(
        isinstance(target, ast.Name) and target.id == "pytestmark"
        for target in node.targets
    )


def _dedupe_known_markers(found: list[str]) -> list[str]:
    known = known_markers()
    seen: set[str] = set()
    ordered: list[str] = []
    for marker in found:
        if marker in seen or marker not in known:
            continue
        seen.add(marker)
        ordered.append(marker)
    return ordered


def _markers_from_pytestmark_value(value: ast.AST) -> list[str]:
    if isinstance(value, ast.Attribute):
        return _domain_attr_markers(value)
    if isinstance(value, (ast.List, ast.Tuple)):
        return _markers_from_sequence(value)
    if isinstance(value, ast.Call):
        return _markers_from_mark_call(value)
    return []


def _domain_attr_markers(value: ast.Attribute) -> list[str]:
    if _DOMAIN_ATTR.match(value.attr):
        return [value.attr]
    return []


def _markers_from_sequence(value: ast.List | ast.Tuple) -> list[str]:
    markers: list[str] = []
    for elt in value.elts:
        markers.extend(_markers_from_pytestmark_value(elt))
    return markers


def _markers_from_mark_call(value: ast.Call) -> list[str]:
    func = value.func
    if isinstance(func, ast.Attribute) and _DOMAIN_ATTR.match(func.attr):
        return [func.attr]
    return []


def ensure_pytestmark(source: str, marker: str) -> str:
    """Place ``pytestmark`` after the top import block (AST line numbers)."""
    if marker not in known_markers():
        raise KeyError(marker)
    # Two-pass normalize so apply is idempotent (stable blank lines).
    once = _inject_after_imports(_strip_domain_pytestmark_lines(source), marker)
    return _inject_after_imports(_strip_domain_pytestmark_lines(once), marker)


def _strip_domain_pytestmark_lines(source: str) -> str:
    """Drop domain ``pytestmark`` assigns; keep other code intact."""
    text = _PYTESTMARK_ASSIGN.sub("", source)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _inject_after_imports(source: str, marker: str) -> str:
    lines = source.splitlines(keepends=True)
    if not lines:
        return f"import pytest\n\npytestmark = pytest.mark.{marker}\n"
    insert_at = _ast_insert_index(source, lines)
    block = _pytestmark_insert_block(lines, insert_at, marker)
    return "".join(lines[:insert_at] + block + lines[insert_at:])


def _pytestmark_insert_block(
    lines: list[str], insert_at: int, marker: str
) -> list[str]:
    block: list[str] = []
    if _needs_blank_before_insert(lines, insert_at):
        block.append("\n")
    if not _lines_import_pytest(lines):
        block.append("import pytest\n")
    block.append(f"pytestmark = pytest.mark.{marker}\n")
    if _needs_blank_after_insert(lines, insert_at):
        block.append("\n")
    return block


def _needs_blank_before_insert(lines: list[str], insert_at: int) -> bool:
    return insert_at > 0 and bool(lines[insert_at - 1].strip())


def _needs_blank_after_insert(lines: list[str], insert_at: int) -> bool:
    return insert_at < len(lines) and bool(lines[insert_at].strip())


def _lines_import_pytest(lines: list[str]) -> bool:
    return any(
        re.match(r"^import pytest\b", line) or re.match(r"^from pytest\b", line)
        for line in lines
    )


def _ast_insert_index(source: str, lines: list[str]) -> int:
    """0-based line index after module docstring + contiguous import nodes."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return _fallback_insert_index(lines)
    return _end_lineno_after_imports(tree.body)


def _end_lineno_after_imports(body: list[ast.stmt]) -> int:
    index, last_end = _skip_module_docstring(body)
    while index < len(body) and isinstance(body[index], (ast.Import, ast.ImportFrom)):
        last_end = body[index].end_lineno or last_end
        index += 1
    return last_end


def _skip_module_docstring(body: list[ast.stmt]) -> tuple[int, int]:
    if body and _is_docstring(body[0]):
        return 1, body[0].end_lineno or 0
    return 0, 0


def _is_docstring(node: ast.AST) -> bool:
    if not isinstance(node, ast.Expr):
        return False
    value = node.value
    return isinstance(value, ast.Constant) and isinstance(value.value, str)


def _fallback_insert_index(lines: list[str]) -> int:
    """Shebang/docstring-only fallback when AST parse fails."""
    index = 0
    if index < len(lines) and lines[index].startswith("#!"):
        index += 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    return index
