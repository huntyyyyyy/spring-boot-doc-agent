"""Semantic-eval mechanical pre-pass (sensor BC).

Stage-adjacent sensor: Confirmed-tag overlap + Mermaid structure checks for the
``semantic-pipeline-eval`` skill. Product invoke stays
``python -m doc_engine.tools.semantic_eval_helpers``.
"""

from __future__ import annotations

from doc_engine.semantic_eval.confirmed import (
    CONFIRMED_TAG_RE,
    DEFAULT_OVERLAP_THRESHOLD,
    STOPWORDS,
    find_unmatched_confirmed_tags,
)
from doc_engine.semantic_eval.mermaid import (
    EDGE_RE,
    END_RE,
    NODE_DECL_RE,
    SUBGRAPH_RE,
    check_mermaid_syntax,
    find_undefined_node_refs,
)
from doc_engine.semantic_eval.scan import main, run

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
