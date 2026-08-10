"""Docs-site builder BC — static MkDocs site from the fourteen-view taxonomy.

Stable invoke: ``python -m doc_engine.tools.build_docs_site``.
"""

from __future__ import annotations

from doc_engine.docs_site.builder import NAV_ORDER, main

__all__ = ["NAV_ORDER", "main"]
