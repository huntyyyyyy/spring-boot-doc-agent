#!/usr/bin/env python3
"""Shim — Mermaid helpers live in ``doc_engine.semantic_eval.mermaid``."""

from __future__ import annotations

from doc_engine.semantic_eval.mermaid import *  # noqa: F403
from doc_engine.semantic_eval.mermaid import (  # noqa: F401
    EDGE_RE,
    END_RE,
    NODE_DECL_RE,
    SUBGRAPH_RE,
    bracket_balance_findings,
    check_mermaid_syntax,
    extract_mermaid_block,
    find_undefined_node_refs,
    subgraph_quote_findings,
)
