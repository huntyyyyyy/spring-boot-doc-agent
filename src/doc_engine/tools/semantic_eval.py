#!/usr/bin/env python3
"""Thin public façade — BC home is ``doc_engine.semantic_eval`` (E-REPO1-A / E-COH1).

Re-exports the stable CLI/API from the nest package. Concept modules stay under
``doc_engine.semantic_eval`` (``confirmed``, ``mermaid``, ``scan``); tools shims
(``semantic_eval_helpers`` / ``*_confirmed`` / ``*_mermaid`` / ``*_scan``) keep
legacy ``-m`` and climb monkeypatch surfaces.

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
