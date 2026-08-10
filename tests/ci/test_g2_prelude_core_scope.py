"""G2 split_scope_break witness: prelude/core pairs must not leak Locals.

E-HOT1-A / finding G2 — structural Accept for statement-chop handoffs.
Logic SoR: ``doc_engine.ci.stalker_sensors.split_scope``.
"""
from __future__ import annotations

import ast

import pytest

from doc_engine.ci.stalker_sensors.split_scope import prelude_core_leaks
from doc_engine.paths import repo_root

pytestmark = pytest.mark.domain_ci_meta

_SKIP_PARTS = frozenset({".venv", "venv", "__pycache__", ".git"})


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
        for prelude_name, leaked in prelude_core_leaks(tree):
            rel = path.relative_to(root).as_posix()
            offenders.append(f"{rel}::{prelude_name} leaks {leaked}")
    assert offenders == [], "G2 split_scope_break:\n" + "\n".join(offenders)
