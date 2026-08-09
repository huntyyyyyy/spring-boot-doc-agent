#!/usr/bin/env python3
"""Public façade for semantic-pipeline-eval mechanical pre-pass (E-COH1).

Concept modules: ``semantic_eval_confirmed``, ``semantic_eval_mermaid``,
``semantic_eval_scan``. This module exports the stable public CLI/API only —
no private ``_`` re-exports (COH4).

Run with:
    python -m doc_engine.tools.semantic_eval <artifacts_dir> [--target-repo <path>]
                                      [--out mechanical_findings.json]
"""

from __future__ import annotations

from doc_engine.paths import (
    PathValidationError,
    checked_output_path,
    checked_path,
    join_under,
)
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
