"""doc_engine — language-agnostic documentation generation SDK.

Public names are resolved lazily so ``python -m doc_engine.tools.*`` does not
pay for Engine → scanning → sqllineage/sqlfluff on every short CLI process.
"""

from typing import Any

__all__ = ["Config", "Settings", "Engine", "ScanContext"]


def __getattr__(name: str) -> Any:
    if name in ("Config", "Settings"):
        from doc_engine.config import Config, Settings

        return Config if name == "Config" else Settings
    if name == "ScanContext":
        from doc_engine.core import ScanContext

        return ScanContext
    if name == "Engine":
        from doc_engine.engine import Engine

        return Engine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
