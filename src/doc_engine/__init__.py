"""doc_engine — language-agnostic documentation generation SDK.

Public names resolve via PEP 562 ``__getattr__`` so ``python -m doc_engine.tools.*``
does not pay for Engine → scanning → sqllineage/sqlfluff on every short CLI.
"""

from __future__ import annotations

from typing import Any

__all__ = ["Config", "Settings", "Engine", "ScanContext"]


def __getattr__(name: str) -> Any:
    if name == "Config":
        from doc_engine.config import Config

        return Config
    if name == "Settings":
        from doc_engine.config import Settings

        return Settings
    if name == "ScanContext":
        from doc_engine.core import ScanContext

        return ScanContext
    if name == "Engine":
        from doc_engine.engine import Engine

        return Engine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
