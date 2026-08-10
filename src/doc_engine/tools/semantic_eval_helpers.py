#!/usr/bin/env python3
"""Thin tools shim — semantic_eval BC lives under ``doc_engine.semantic_eval``.

Concept modules: ``confirmed``, ``mermaid``, ``scan``. This façade keeps the
stable ``-m`` entrypoint and climb/monkeypatch import surface.

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
from doc_engine.semantic_eval.confirmed import (
    CONFIRMED_TAG_RE,
    DEFAULT_OVERLAP_THRESHOLD,
    STOPWORDS,
    find_unmatched_confirmed_tags,
)
from doc_engine.semantic_eval.confirmed import (
    answered_entry_tokens as _answered_entry_tokens,
)
from doc_engine.semantic_eval.confirmed import (
    best_overlap as _best_overlap,
)
from doc_engine.semantic_eval.confirmed import (
    claim_clause as _claim_clause,
)
from doc_engine.semantic_eval.confirmed import (
    empty_clause_finding as _empty_clause_finding,
)
from doc_engine.semantic_eval.confirmed import (
    finding_for_confirmed_tag as _finding_for_confirmed_tag,
)
from doc_engine.semantic_eval.confirmed import (
    low_overlap_finding as _low_overlap_finding,
)
from doc_engine.semantic_eval.confirmed import (
    tokenize as _tokenize,
)
from doc_engine.semantic_eval.mermaid import (
    EDGE_RE,
    END_RE,
    NODE_DECL_RE,
    SUBGRAPH_RE,
    check_mermaid_syntax,
    find_undefined_node_refs,
)
from doc_engine.semantic_eval.mermaid import (
    bracket_balance_findings as _bracket_balance_findings,
)
from doc_engine.semantic_eval.mermaid import (
    extract_mermaid_block as _extract_mermaid_block,
)
from doc_engine.semantic_eval.mermaid import (
    subgraph_quote_findings as _subgraph_quote_findings,
)
from doc_engine.semantic_eval.scan import (
    confirmed_findings_for_doc as _confirmed_findings_for_doc,
)
from doc_engine.semantic_eval.scan import (
    is_safe_markdown_basename as _is_safe_markdown_basename,
)
from doc_engine.semantic_eval.scan import (
    load_interview_answers as _load_interview_answers,
)
from doc_engine.semantic_eval.scan import (
    main,
    run,
)
from doc_engine.semantic_eval.scan import (
    markdown_names as _markdown_names,
)
from doc_engine.semantic_eval.scan import (
    resolve_architecture_path as _resolve_architecture_path,
)
from doc_engine.semantic_eval.scan import (
    scan_confirmed_docs as _scan_confirmed_docs,
)
from doc_engine.semantic_eval.scan import (
    scan_mermaid as _scan_mermaid,
)

# Public entry + climb-stable constants only. Underscore aliases stay importable
# for monkeypatch but must not appear in __all__ (check_public_surface).
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
    "PathValidationError",
    "checked_output_path",
    "checked_path",
    "join_under",
]

if __name__ == "__main__":
    main()
