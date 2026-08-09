"""doc_engine — language-agnostic documentation generation SDK.

Public names resolve via PEP 562 ``__getattr__`` so ``python -m doc_engine.tools.*``
does not pay for Engine → scanning → sqllineage/sqlfluff on every short CLI.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

__all__ = ["Config", "Settings", "Engine", "ScanContext"]


def _load_config() -> Any:
    from doc_engine.config import Config

    return Config


def _load_settings() -> Any:
    from doc_engine.config import Settings

    return Settings


def _load_scan_context() -> Any:
    from doc_engine.core import ScanContext

    return ScanContext


def _load_engine() -> Any:
    from doc_engine.engine import Engine

    return Engine


_LAZY_LOADERS: Dict[str, Callable[[], Any]] = {
    "Config": _load_config,
    "Settings": _load_settings,
    "ScanContext": _load_scan_context,
    "Engine": _load_engine,
}


def __getattr__(name: str) -> Any:
    loader = _LAZY_LOADERS.get(name)
    if loader is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return loader()
