"""Stage 0 scanning package.

Heavy scanners and sqllineage stay behind ``__getattr__`` so lightweight tool
CLIs do not cold-start sqlfluff. ``scan_repository`` lives in
``repository_scan`` — this module only dispatches, it does not call
``__getattr__`` from a wrapper body.
"""

from __future__ import annotations

import importlib
from typing import Any

__all__ = [
    "scan",
    "scan_repository",
    "run_scan",
    "get_scanner",
    "resolve_scanner_names",
    "SpringSignalMerger",
    "SpringLineageResolver",
]

# Pair of class exports — one branch keeps __getattr__ at complexipy ≤5.
_CLASS_EXPORTS = {
    "SpringSignalMerger": "doc_engine.scanning._merge_signals",
    "SpringLineageResolver": "doc_engine.scanning._resolve_lineage",
}


def __getattr__(name: str) -> Any:
    if name == "scan":
        from doc_engine.scanning.spring import scan

        return scan
    if name == "scan_repository":
        from doc_engine.scanning.repository_scan import scan_repository

        return scan_repository
    if name == "run_scan":
        from doc_engine.scanning._orchestrator import run_scan

        return run_scan
    if name in ("get_scanner", "resolve_scanner_names"):
        from doc_engine.scanning import _scanner_registry as registry

        return getattr(registry, name)
    if name in _CLASS_EXPORTS:
        return getattr(importlib.import_module(_CLASS_EXPORTS[name]), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
