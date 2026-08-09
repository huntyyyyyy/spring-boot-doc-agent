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
    answered_entry_tokens as _answered_entry_tokens,
    best_overlap as _best_overlap,
    claim_clause as _claim_clause,
    empty_clause_finding as _empty_clause_finding,
    find_unmatched_confirmed_tags,
    finding_for_confirmed_tag as _finding_for_confirmed_tag,
    low_overlap_finding as _low_overlap_finding,
    tokenize as _tokenize,
)
from doc_engine.tools.semantic_eval_mermaid import (
    EDGE_RE,
    END_RE,
    NODE_DECL_RE,
    SUBGRAPH_RE,
    bracket_balance_findings as _bracket_balance_findings,
    check_mermaid_syntax,
    extract_mermaid_block as _extract_mermaid_block,
    find_undefined_node_refs,
    subgraph_quote_findings as _subgraph_quote_findings,
)
from doc_engine.tools.semantic_eval_scan import (
    confirmed_findings_for_doc as _confirmed_findings_for_doc,
    is_safe_markdown_basename as _is_safe_markdown_basename,
    load_interview_answers as _load_interview_answers,
    main,
    markdown_names as _markdown_names,
    resolve_architecture_path as _resolve_architecture_path,
    run,
    scan_confirmed_docs as _scan_confirmed_docs,
    scan_mermaid as _scan_mermaid,
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
