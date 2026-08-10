#!/usr/bin/env python3
"""Thin tools shim — semantic_eval BC lives under ``doc_engine.semantic_eval``.

Stable ``-m`` entrypoint for legacy callers. Public API matches
``doc_engine.tools.semantic_eval`` (no private ``_`` names in ``__all__``).

Run with:
    python -m doc_engine.tools.semantic_eval_helpers <artifacts_dir> [--target-repo <path>]
                                      [--out mechanical_findings.json]
"""

from __future__ import annotations

from doc_engine.paths import (
    PathValidationError,
    checked_output_path,
    checked_path,
    join_under,
)
from doc_engine.semantic_eval import (
    CONFIRMED_TAG_RE,
    DEFAULT_OVERLAP_THRESHOLD,
    EDGE_RE,
    END_RE,
    NODE_DECL_RE,
    STOPWORDS,
    SUBGRAPH_RE,
    check_mermaid_syntax,
    find_undefined_node_refs,
    find_unmatched_confirmed_tags,
    main,
    run,
)

__all__ = [
    "CONFIRMED_TAG_RE",
    "DEFAULT_OVERLAP_THRESHOLD",
    "EDGE_RE",
    "END_RE",
    "NODE_DECL_RE",
    "STOPWORDS",
    "SUBGRAPH_RE",
    "PathValidationError",
    "check_mermaid_syntax",
    "checked_output_path",
    "checked_path",
    "find_undefined_node_refs",
    "find_unmatched_confirmed_tags",
    "join_under",
    "main",
    "run",
]

if __name__ == "__main__":
    main()
