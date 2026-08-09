#!/usr/bin/env python3
"""Citation-coverage façade — untagged claims and weak Evidenced anchors.

Run with: python -m doc_engine.tools.citation_coverage <docs_dir> --target-repo <repo>

Concept modules: ``citation_coverage_constants``, ``_claims``, ``_anchors``,
``_report``, ``_cli``, ``_ports``. This façade keeps the stable ``-m`` entrypoint
used by live_gates and the ``cc.*`` import surface for unit tests.

Usage:
    python -m doc_engine.tools.citation_coverage <docs_dir> --target-repo <repo>
    python -m doc_engine.tools.citation_coverage <docs_dir> --json
    python -m doc_engine.tools.citation_coverage <docs_dir> --strict
"""

from __future__ import annotations

from doc_engine.tools.citation_coverage_anchors import (
    _classify_weak_anchor,
    _read_lines,
    _symbols_for_evidenced_match,
    _weak_anchor_finding,
    _weak_anchor_for_match,
    claim_symbols,
    find_weak_anchors,
)
from doc_engine.tools.citation_coverage_claims import (
    _advance_fence,
    _claim_clause,
    _claim_units_from_raw_line,
    _has_tag,
    _named_artifacts,
    _sentences_from_line,
    _skip_claim_line,
    _strip_inline_code,
    find_miscased_tags,
    find_untagged_claims,
    iter_claim_units,
)
from doc_engine.tools.citation_coverage_cli import main
from doc_engine.tools.citation_coverage_constants import (
    ANY_CASE_TAG_SPAN,
    ARTIFACT_PATTERNS,
    BULLET_PREFIX_RE,
    CLAIM_SYMBOL_PATTERNS,
    DEFAULT_ANCHOR_WINDOW,
    EXEMPT_LINE_RE,
    FENCE_RE,
    HEADING_RE,
    MD_LINK_RE,
    SENTENCE_SPLIT_RE,
    TABLE_RULE_RE,
    URL_RE,
)
from doc_engine.tools.citation_coverage_ports import CitationCoveragePort
from doc_engine.tools.citation_coverage_report import (
    _format_file_findings,
    _format_miscased_lines,
    _format_untagged_lines,
    _format_weak_anchor_lines,
    check_docs,
    format_report,
    total_findings,
)
from doc_engine.tools.doc_tag_utils import TAG_PATTERNS, TAG_WORD_SPAN

__all__ = [
    "ANY_CASE_TAG_SPAN",
    "ARTIFACT_PATTERNS",
    "BULLET_PREFIX_RE",
    "CLAIM_SYMBOL_PATTERNS",
    "CitationCoveragePort",
    "DEFAULT_ANCHOR_WINDOW",
    "EXEMPT_LINE_RE",
    "FENCE_RE",
    "HEADING_RE",
    "MD_LINK_RE",
    "SENTENCE_SPLIT_RE",
    "TABLE_RULE_RE",
    "TAG_PATTERNS",
    "TAG_WORD_SPAN",
    "URL_RE",
    "_advance_fence",
    "_claim_clause",
    "_claim_units_from_raw_line",
    "_classify_weak_anchor",
    "_format_file_findings",
    "_format_miscased_lines",
    "_format_untagged_lines",
    "_format_weak_anchor_lines",
    "_has_tag",
    "_named_artifacts",
    "_read_lines",
    "_sentences_from_line",
    "_skip_claim_line",
    "_strip_inline_code",
    "_symbols_for_evidenced_match",
    "_weak_anchor_finding",
    "_weak_anchor_for_match",
    "check_docs",
    "claim_symbols",
    "find_miscased_tags",
    "find_untagged_claims",
    "find_weak_anchors",
    "format_report",
    "iter_claim_units",
    "main",
    "total_findings",
]

if __name__ == "__main__":
    raise SystemExit(main())
