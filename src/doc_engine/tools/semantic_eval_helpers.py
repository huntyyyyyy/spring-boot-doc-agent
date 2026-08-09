#!/usr/bin/env python3
"""
semantic_eval_helpers.py — the mechanical pre-pass for the
semantic-pipeline-eval skill.

Concept modules: ``semantic_eval_confirmed``, ``semantic_eval_mermaid``,
``semantic_eval_scan``. This façade keeps the stable ``-m`` entrypoint and
``find_unmatched_confirmed_tags`` / ``check_mermaid_syntax`` import surface.

Run with:
    python -m doc_engine.tools.semantic_eval_helpers <artifacts_dir> [--target-repo <path>]
                                      [--out mechanical_findings.json]
"""

from __future__ import annotations

from doc_engine.tools.semantic_eval_confirmed import (
    CONFIRMED_TAG_RE,
    DEFAULT_OVERLAP_THRESHOLD,
    STOPWORDS,
    find_unmatched_confirmed_tags,
)
from doc_engine.tools.semantic_eval_mermaid import (
    EDGE_RE,
    END_RE,
    NODE_DECL_RE,
    SUBGRAPH_RE,
    check_mermaid_syntax,
    find_undefined_node_refs,
)
from doc_engine.tools.semantic_eval_scan import (
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
    "check_mermaid_syntax",
    "find_undefined_node_refs",
    "find_unmatched_confirmed_tags",
    "main",
    "run",
]

if __name__ == "__main__":
    main()
