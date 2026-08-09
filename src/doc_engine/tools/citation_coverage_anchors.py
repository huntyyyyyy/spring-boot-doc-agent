"""Weak-anchor checks: claim symbols near Evidenced path:line citations."""

from __future__ import annotations

import os

from doc_engine.tools.citation_coverage_claims import _claim_clause, _strip_inline_code
from doc_engine.tools.citation_coverage_constants import (
    CLAIM_SYMBOL_PATTERNS,
    DEFAULT_ANCHOR_WINDOW,
)
from doc_engine.tools.doc_tag_utils import TAG_PATTERNS


def claim_symbols(clause):
    """Identifiers from a claim that would plausibly appear verbatim in source."""
    stripped = _strip_inline_code(clause)
    return {
        (m.group(1) if m.re.groups else m.group(0))
        for pattern in CLAIM_SYMBOL_PATTERNS
        for m in pattern.finditer(stripped)
    }


def _read_lines(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read().splitlines()


def _weak_anchor_finding(kind, match, clause, symbols, in_file, reason):
    return {
        "kind": kind,
        "citation": match.group(0),
        "claim": clause.strip(),
        "symbols": sorted(symbols),
        "found_elsewhere_in_file": sorted(in_file),
        "reason": reason,
    }


def _symbols_for_evidenced_match(text, match, relpath):
    """Claim symbols for one Evidenced tag, minus the cited file's own stem."""
    clause = _claim_clause(text, match.start())
    symbols = claim_symbols(clause)
    stem = os.path.splitext(os.path.basename(relpath))[0]
    symbols.discard(stem)
    return clause, symbols


def _classify_weak_anchor(match, clause, symbols, lines, target, relpath, window):
    """Return one weak-anchor finding dict, or None when the window is fine."""
    lo = max(0, target - 1 - window)
    hi = min(len(lines), target + window)
    window_text = "\n".join(lines[lo:hi])
    if any(symbol in window_text for symbol in symbols):
        return None

    file_text = "\n".join(lines)
    in_file = {s for s in symbols if s in file_text}
    if in_file:
        return _weak_anchor_finding(
            "symbol_outside_window",
            match,
            clause,
            symbols,
            in_file,
            (
                f"none of the claim's symbols appear within +/-{window} "
                f"lines of {relpath}:{target}, though they exist elsewhere "
                f"in the file — the line anchor looks imprecise"
            ),
        )
    return _weak_anchor_finding(
        "symbol_absent_from_file",
        match,
        clause,
        symbols,
        (),
        (
            f"none of the claim's symbols appear anywhere in "
            f"{relpath} — candidate fabricated citation"
        ),
    )


def _weak_anchor_for_match(text, match, repo_root, window):
    """Evaluate one Evidenced match; return a finding or None."""
    relpath, line = match.group(1), match.group(2)
    if line is None:
        return None
    abspath = os.path.join(repo_root, relpath)
    if not os.path.isfile(abspath):
        return None

    clause, symbols = _symbols_for_evidenced_match(text, match, relpath)
    if not symbols:
        return None

    lines = _read_lines(abspath)
    target = int(line)
    if target > len(lines):
        return None
    return _classify_weak_anchor(
        match, clause, symbols, lines, target, relpath, window
    )


def find_weak_anchors(text, repo_root, window=DEFAULT_ANCHOR_WINDOW):
    """Check Evidenced path:line tags for symbols near the cited line."""
    findings = []
    for match in TAG_PATTERNS["evidenced"].finditer(text):
        finding = _weak_anchor_for_match(text, match, repo_root, window)
        if finding:
            findings.append(finding)
    return findings
