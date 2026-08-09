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
from typing import Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]

# Stable public façades that characterization / kitchen / climb tests patch.
FACADES: Dict[str, str] = {
    "doc_engine.tools.run_manifest": "run_manifest",
    "doc_engine.tools.citation_coverage": "citation_coverage",
    "doc_engine.tools.capacity_preflight": "capacity_preflight",
    "doc_engine.tools.spring_drift_check": "spring_drift_check",
    "doc_engine.tools.partition_repo": "partition_repo",
    "doc_engine.pipeline.mock_stages": "mock_stages",
}

AttrNeed = Tuple[str, str, str]  # facade_mod, attr, test_path


def _iter_test_files() -> Iterable[Path]:
    tests = REPO_ROOT / "tests"
    yield from sorted(tests.rglob("test_*.py"))


def _alias_map(tree: ast.AST) -> Dict[str, str]:
    """Map local name → fully-qualified façade module."""
    aliases: Dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mod = alias.name
                if mod in FACADES:
                    aliases[alias.asname or alias.name.split(".")[-1]] = mod
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module in FACADES:
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    local = alias.asname or alias.name
                    # from doc_engine.tools import run_manifest as rm
                    if f"{node.module}" in FACADES or node.module.startswith(
                        "doc_engine.tools"
                    ):
                        # import submodule from package path
                        full = (
                            node.module
                            if alias.name == node.module.split(".")[-1]
                            else f"{node.module}.{alias.name}"
                            if node.module.count(".") >= 2
                            else f"doc_engine.tools.{alias.name}"
                        )
                        # Prefer exact façade keys
                        if full in FACADES:
                            aliases[local] = full
                        elif alias.name in {v for v in FACADES.values()}:
                            for k, v in FACADES.items():
                                if v == alias.name:
                                    aliases[local] = k
                                    break
            # from doc_engine.tools import run_manifest as rm
            if node.module in {"doc_engine.tools", "doc_engine.pipeline"}:
                for alias in node.names:
                    candidate = f"{node.module}.{alias.name}"
                    if candidate in FACADES:
                        aliases[alias.asname or alias.name] = candidate
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
        func = node.func
        # monkeypatch.setattr(target, name, ...) or setattr(mp, ...)
        name = None
        if isinstance(func, ast.Attribute) and func.attr == "setattr":
            name = "setattr"
        elif isinstance(func, ast.Attribute) and func.attr == "patch":
            # mock.patch("doc_engine.tools.run_manifest.json.dump") — string form
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(
                node.args[0].value, str
            ):
                target = node.args[0].value
                for fac in FACADES:
                    prefix = fac + "."
                    if target.startswith(prefix):
                        rest = target[len(prefix) :].split(".", 1)[0]
                        needs.append((fac, rest, rel))
            continue
        elif isinstance(func, ast.Attribute) and func.attr == "object":
            # mock.patch.object(run_manifest.json, "dump")
            name = "patch_object"
        else:
            continue

        if name == "setattr" and len(node.args) >= 2:
            target, attr_node = node.args[0], node.args[1]
            if not isinstance(attr_node, ast.Constant) or not isinstance(
                attr_node.value, str
            ):
                continue
            chain = _attr_chain(target)
            if not chain:
                continue
            root = chain[0]
            if root not in aliases:
                continue
            fac = aliases[root]
            # setattr(rm, "dfs_walk") → need dfs_walk; setattr(rm.os, "replace") → need os
            need_attr = chain[1] if len(chain) > 1 else attr_node.value
            needs.append((fac, need_attr, rel))
        elif name == "patch_object" and len(node.args) >= 1:
            target = node.args[0]
            chain = _attr_chain(target)
            if len(chain) < 2:
                continue
            root = chain[0]
            if root not in aliases:
                continue
            fac = aliases[root]
            needs.append((fac, chain[1], rel))
    return needs


def _module_has_attr(mod_name: str, attr: str) -> bool:
    mod = importlib.import_module(mod_name)
    return hasattr(mod, attr)


def main() -> int:
    needs: List[AttrNeed] = []
    for path in _iter_test_files():
        needs.extend(_collect_needs(path))

    # Deduplicate by facade+attr
    unique: Dict[Tuple[str, str], str] = {}
    for fac, attr, rel in needs:
        unique.setdefault((fac, attr), rel)

    missing: List[str] = []
    for (fac, attr), rel in sorted(unique.items()):
        if not _module_has_attr(fac, attr):
            missing.append(
                f"{fac!s} missing attribute {attr!r} "
                f"(poked from {rel})"
            )

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
