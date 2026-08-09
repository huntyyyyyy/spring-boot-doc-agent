#!/usr/bin/env python3
"""Inventory characterization poke surfaces and assert façades expose them.

Scans tests for ``monkeypatch.setattr(facade, …)`` / ``patch.object(facade, …)``
against known thin façades. Catches E-MOD-style DIP misses (e.g. kitchen
patching ``run_manifest.json`` after a vertical split).

Run: ``python3 scripts/ci/check_facade_poke_surface.py``
"""

from __future__ import annotations

import ast
import importlib
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]

FACADES: Dict[str, str] = {
    "doc_engine.tools.run_manifest": "run_manifest",
    "doc_engine.tools.citation_coverage": "citation_coverage",
    "doc_engine.tools.capacity_preflight": "capacity_preflight",
    "doc_engine.tools.spring_drift_check": "spring_drift_check",
    "doc_engine.tools.partition_repo": "partition_repo",
    "doc_engine.pipeline.mock_stages": "mock_stages",
}

PACKAGE_ROOTS = ("doc_engine.tools", "doc_engine.pipeline")
AttrNeed = Tuple[str, str, str]


def _iter_test_files() -> Iterable[Path]:
    yield from sorted((REPO_ROOT / "tests").rglob("test_*.py"))


def _facade_for_short_name(short: str) -> Optional[str]:
    for full, name in FACADES.items():
        if name == short:
            return full
    return None


def _record_import(aliases: Dict[str, str], local: str, mod: str) -> None:
    if mod in FACADES:
        aliases[local] = mod


def _handle_import(aliases: Dict[str, str], node: ast.Import) -> None:
    for alias in node.names:
        _record_import(aliases, alias.asname or alias.name.split(".")[-1], alias.name)


def _handle_import_from(aliases: Dict[str, str], node: ast.ImportFrom) -> None:
    if not node.module:
        return
    if node.module in PACKAGE_ROOTS:
        for alias in node.names:
            candidate = f"{node.module}.{alias.name}"
            _record_import(aliases, alias.asname or alias.name, candidate)
        return
    if node.module not in FACADES:
        return
    for alias in node.names:
        if alias.name == "*":
            continue
        local = alias.asname or alias.name
        short = _facade_for_short_name(alias.name)
        if short:
            aliases[local] = short
        else:
            _record_import(aliases, local, node.module)


def _alias_map(tree: ast.AST) -> Dict[str, str]:
    """Map local name → fully-qualified façade module."""
    aliases: Dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _handle_import(aliases, node)
        elif isinstance(node, ast.ImportFrom):
            _handle_import_from(aliases, node)
    return aliases


def _attr_chain(node: ast.AST) -> List[str]:
    parts: List[str] = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
        parts.reverse()
        return parts
    return []


def _call_kind(func: ast.AST) -> Optional[str]:
    if not isinstance(func, ast.Attribute):
        return None
    if func.attr == "setattr":
        return "setattr"
    if func.attr == "patch":
        return "patch"
    if func.attr == "object":
        return "patch_object"
    return None


def _needs_from_patch_string(target: str, rel: str) -> List[AttrNeed]:
    needs: List[AttrNeed] = []
    for fac in FACADES:
        prefix = fac + "."
        if target.startswith(prefix):
            needs.append((fac, target[len(prefix) :].split(".", 1)[0], rel))
    return needs


def _needs_from_setattr(
    aliases: Dict[str, str], node: ast.Call, rel: str
) -> List[AttrNeed]:
    if len(node.args) < 2:
        return []
    target, attr_node = node.args[0], node.args[1]
    if not isinstance(attr_node, ast.Constant) or not isinstance(attr_node.value, str):
        return []
    chain = _attr_chain(target)
    if not chain or chain[0] not in aliases:
        return []
    need_attr = chain[1] if len(chain) > 1 else attr_node.value
    return [(aliases[chain[0]], need_attr, rel)]


def _needs_from_patch_object(
    aliases: Dict[str, str], node: ast.Call, rel: str
) -> List[AttrNeed]:
    if not node.args:
        return []
    chain = _attr_chain(node.args[0])
    if len(chain) < 2 or chain[0] not in aliases:
        return []
    return [(aliases[chain[0]], chain[1], rel)]


def _collect_needs(path: Path) -> List[AttrNeed]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return []
    aliases = _alias_map(tree)
    needs: List[AttrNeed] = []
    rel = str(path.relative_to(REPO_ROOT))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        kind = _call_kind(node.func)
        if kind == "patch":
            arg0 = node.args[0] if node.args else None
            if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                needs.extend(_needs_from_patch_string(arg0.value, rel))
        elif kind == "setattr":
            needs.extend(_needs_from_setattr(aliases, node, rel))
        elif kind == "patch_object":
            needs.extend(_needs_from_patch_object(aliases, node, rel))
    return needs


def _module_has_attr(mod_name: str, attr: str) -> bool:
    return hasattr(importlib.import_module(mod_name), attr)


def main() -> int:
    unique: Dict[Tuple[str, str], str] = {}
    for path in _iter_test_files():
        for fac, attr, rel in _collect_needs(path):
            unique.setdefault((fac, attr), rel)

    missing = [
        f"{fac} missing attribute {attr!r} (poked from {rel})"
        for (fac, attr), rel in sorted(unique.items())
        if not _module_has_attr(fac, attr)
    ]
    if missing:
        print("facade poke-surface check failed:", file=sys.stderr)
        for line in missing:
            print(f"  - {line}", file=sys.stderr)
        print(
            "Re-export the attribute on the thin façade (DIP / characterization seam).",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK: {len(unique)} façade poke attribute(s) present across "
        f"{len(FACADES)} façade(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
