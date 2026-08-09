"""G4: compile / syntax on watched Python trees."""

from __future__ import annotations

import py_compile
from pathlib import Path

from doc_engine.ci.stalker_sensors.finding_records import KIND_G4, StalkerFinding

_WATCH = ("src/doc_engine/ci", "scripts/ci", "tests/ci")
_SKIP_PARTS = frozenset({".venv", "venv", "__pycache__", ".git"})


def _compile_finding(root: Path, path: Path) -> StalkerFinding | None:
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as exc:
        return StalkerFinding(
            KIND_G4,
            f"syntax/compile fail {path.relative_to(root).as_posix()}",
            str(exc),
        )
    return None


def _scan_tree(root: Path, base: Path) -> list[StalkerFinding]:
    findings: list[StalkerFinding] = []
    for path in sorted(base.rglob("*.py")):
        if _SKIP_PARTS.intersection(path.parts):
            continue
        item = _compile_finding(root, path)
        if item is not None:
            findings.append(item)
    return findings


def scan_collect_syntax(root: Path) -> list[StalkerFinding]:
    findings: list[StalkerFinding] = []
    for rel in _WATCH:
        base = root / rel
        if base.is_dir():
            findings.extend(_scan_tree(root, base))
    return findings
