#!/usr/bin/env python3
"""Shim — Confirmed-tag helpers live in ``doc_engine.semantic_eval.confirmed``."""

from __future__ import annotations

from doc_engine.semantic_eval.confirmed import *  # noqa: F403
from doc_engine.semantic_eval.confirmed import (  # noqa: F401
    CONFIRMED_TAG_RE,
    DEFAULT_OVERLAP_THRESHOLD,
    STOPWORDS,
    answered_entry_tokens,
    best_overlap,
    claim_clause,
    empty_clause_finding,
    find_unmatched_confirmed_tags,
    finding_for_confirmed_tag,
    low_overlap_finding,
    tokenize,
)
