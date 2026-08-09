"""Constants and structural regexes for citation coverage checks."""

from __future__ import annotations

import re

# A window of +/- this many lines around a cited line counts as "near" the
# citation for the weak-anchor check.
DEFAULT_ANCHOR_WINDOW = 8

# Concrete repo artifacts. A sentence naming any of these is making a claim
# about the code and therefore needs a citation.
ARTIFACT_PATTERNS = (
    re.compile(r"\b[\w./-]+\.(?:java|kt|xml|ya?ml|properties|gradle|sql|json|tf|sh)\b"),
    re.compile(r"\bDockerfile\b"),
    re.compile(r"@[A-Z]\w+"),
    re.compile(r"\b[a-z]\w*\(\)"),
    re.compile(r"\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+\b"),
    re.compile(r"\b[a-z][a-z0-9_-]*(?:\.[a-z0-9_-]+){2,}\b"),
    re.compile(r"\b[A-Z][A-Z0-9]{2,}(?:_[A-Z0-9]+)+\b"),
)

# Identifier-ish tokens pulled out of a claim to look for near its citation.
CLAIM_SYMBOL_PATTERNS = (
    re.compile(r"@[A-Z]\w+"),
    re.compile(r"\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+\b"),
    re.compile(r"\b([a-z]\w*)\(\)"),
    re.compile(r"\b[A-Z][A-Z0-9]{2,}(?:_[A-Z0-9]+)+\b"),
    re.compile(r"\b[a-z][a-z0-9_-]*(?:\.[a-z0-9_-]+){2,}\b"),
)

EXEMPT_LINE_RE = re.compile(
    r"^\s*(?:none found|not applicable|n/?a|asked,\s*not answered|tbd)\s*\.?\s*$",
    re.IGNORECASE,
)

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)")
HEADING_RE = re.compile(r"^\s*#")
TABLE_RULE_RE = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*$")
BULLET_PREFIX_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")

URL_RE = re.compile(r"<?https?://[^\s>)\]]+>?")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\((?:[^)]*)\)")

# Case-insensitive tag span — catches miscased tags invisible to TAG_WORD_SPAN.
ANY_CASE_TAG_SPAN = re.compile(
    r"\[(?:evidenced|confirmed|unknown|per existing docs)\b[^\]]*\]",
    re.IGNORECASE,
)
