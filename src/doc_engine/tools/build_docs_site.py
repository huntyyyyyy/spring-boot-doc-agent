#!/usr/bin/env python3
"""Thin tools shim — docs-site BC lives under ``doc_engine.docs_site``.

Keeps climb poke surface (``_copy_docs``, ``subprocess``, …) on this module.
Usage:
    python -m doc_engine.tools.build_docs_site --docs-dir <path> --out-dir <path>
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from doc_engine.docs_site.builder import (
    NAV_ORDER,
    _build_nav,
    _copy_docs,
    _run_mkdocs,
    _write_mkdocs_config,
    _yaml_nav,
)
from doc_engine.docs_site.builder import (
    main as _builder_main,
)


def _find_mkdocs_yml() -> Path:
    """Climb-compat stub — builder generates mkdocs.yml; name-only contract."""
    return Path("mkdocs.yml")


def main() -> int:
    """Delegate through façade attrs so monkeypatch.setattr(bds, …) still bites."""
    return _builder_main(facade=sys.modules[__name__])


__all__ = [
    "NAV_ORDER",
    "_build_nav",
    "_copy_docs",
    "_find_mkdocs_yml",
    "_run_mkdocs",
    "_write_mkdocs_config",
    "_yaml_nav",
    "main",
    "subprocess",
]

if __name__ == "__main__":
    sys.exit(main())
