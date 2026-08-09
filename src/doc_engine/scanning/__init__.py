"""Stage 0 scanning package.

Heavy scanners and sqllineage stay behind lazy loaders so lightweight tool
CLIs (secrets heuristics, walk helpers) do not cold-start sqlfluff on every
``python -m`` invocation. Public names are listed in ``__all__`` and resolved
via ``__getattr__`` (PEP 562) — not by calling ``__getattr__`` from wrappers.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

__all__ = [
    "scan",
    "scan_repository",
    "run_scan",
    "get_scanner",
    "resolve_scanner_names",
    "SpringSignalMerger",
    "SpringLineageResolver",
]


def _load_scan() -> Any:
    from doc_engine.scanning.spring import scan

    return scan


def _load_scan_repository() -> Any:
    from doc_engine.scanning.repository_scan import scan_repository

    return scan_repository


def _load_run_scan() -> Any:
    from doc_engine.scanning._orchestrator import run_scan

    return run_scan


def _load_get_scanner() -> Any:
    from doc_engine.scanning._scanner_registry import get_scanner

    return get_scanner


def _load_resolve_scanner_names() -> Any:
    from doc_engine.scanning._scanner_registry import resolve_scanner_names

    return resolve_scanner_names


def _load_spring_signal_merger() -> Any:
    from doc_engine.scanning._merge_signals import SpringSignalMerger

    return SpringSignalMerger


def _load_spring_lineage_resolver() -> Any:
    from doc_engine.scanning._resolve_lineage import SpringLineageResolver

    return SpringLineageResolver


_LAZY_LOADERS: Dict[str, Callable[[], Any]] = {
    "scan": _load_scan,
    "scan_repository": _load_scan_repository,
    "run_scan": _load_run_scan,
    "get_scanner": _load_get_scanner,
    "resolve_scanner_names": _load_resolve_scanner_names,
    "SpringSignalMerger": _load_spring_signal_merger,
    "SpringLineageResolver": _load_spring_lineage_resolver,
}


def __getattr__(name: str) -> Any:
    loader = _LAZY_LOADERS.get(name)
    if loader is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return loader()
