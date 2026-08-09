"""Untagged-claim and miscased-tag detection for citation coverage."""

from __future__ import annotations

from doc_engine.tools.citation_coverage_constants import (
    ANY_CASE_TAG_SPAN,
    ARTIFACT_PATTERNS,
    BULLET_PREFIX_RE,
    EXEMPT_LINE_RE,
    FENCE_RE,
    HEADING_RE,
    MD_LINK_RE,
    SENTENCE_SPLIT_RE,
    TABLE_RULE_RE,
    URL_RE,
)
from doc_engine.tools.doc_tag_utils import TAG_WORD_SPAN


def _strip_inline_code(text):
    """Drop backticks/URLs for artifact detection; keep identifier content."""
    text = MD_LINK_RE.sub(r"\1", text)
    text = URL_RE.sub(" ", text)
    return text.replace("`", "")


def _skip_claim_line(line):
    """True when a stripped markdown line cannot carry a claim unit."""
    if not line or HEADING_RE.match(line) or TABLE_RULE_RE.match(line):
        return True
    if line.startswith("<!--") or line.startswith(">"):
        return True
    return bool(EXEMPT_LINE_RE.match(BULLET_PREFIX_RE.sub("", line)))


def _sentences_from_line(line):
    body = BULLET_PREFIX_RE.sub("", line)
    for sentence in SENTENCE_SPLIT_RE.split(body):
        sentence = sentence.strip()
        if sentence:
            yield sentence


def _advance_fence(raw, in_fence):
    """Toggle fence state when ``raw`` is a fence marker; else unchanged."""
    if FENCE_RE.match(raw):
        return (not in_fence), True
    return in_fence, False


def _claim_units_from_raw_line(lineno, raw, in_fence):
    """Yield claim units from one raw line; return updated fence state."""
    in_fence, is_fence = _advance_fence(raw, in_fence)
    if is_fence or in_fence or _skip_claim_line(raw.strip()):
        return in_fence, ()
    return in_fence, tuple(
        (lineno, sentence) for sentence in _sentences_from_line(raw.strip())
    )


def iter_claim_units(text):
    """Yield (line_number, sentence) for every sentence that could carry a claim."""
    in_fence = False
    for lineno, raw in enumerate(text.splitlines(), start=1):
        in_fence, units = _claim_units_from_raw_line(lineno, raw, in_fence)
        yield from units


def _has_tag(sentence):
    """True if the sentence carries any recognized tag-word span (any casing)."""
    return bool(ANY_CASE_TAG_SPAN.search(sentence))


def _claim_clause(text, tag_start):
    """The sentence immediately preceding a tag."""
    prefix = text[:tag_start]
    pieces = SENTENCE_SPLIT_RE.split(prefix)
    return pieces[-1] if pieces else prefix


def find_miscased_tags(text):
    """Bracketed spans that read as a tag in non-required casing."""
    findings = []
    for m in ANY_CASE_TAG_SPAN.finditer(text):
        if TAG_WORD_SPAN.match(m.group(0)):
            continue
        findings.append(
            {
                "kind": "miscased_tag",
                "tag": m.group(0),
                "claim": _claim_clause(text, m.start()).strip(),
                "reason": (
                    "tag word is not in its required casing — invisible to "
                    "both find_malformed_tags() and the tag counters, so "
                    "this citation is scored as absent everywhere"
                ),
            }
        )
    return findings


def _named_artifacts(sentence):
    found = []
    stripped = _strip_inline_code(sentence)
    for pattern in ARTIFACT_PATTERNS:
        for m in pattern.finditer(stripped):
            found.append(m.group(0))
    return found


def find_untagged_claims(text):
    """Sentences that name a concrete repo artifact but carry no tag."""
    findings = []
    for lineno, sentence in iter_claim_units(text):
        if _has_tag(sentence):
            continue
        artifacts = _named_artifacts(sentence)
        if not artifacts:
            continue
        findings.append(
            {
                "kind": "untagged_claim",
                "line": lineno,
                "claim": sentence,
                "named_artifacts": sorted(set(artifacts)),
                "reason": (
                    "names a code artifact but carries no evidence tag — "
                    "every substantive claim must end in one of the five "
                    "forms in doc-taxonomy.md"
                ),
            }
        )
    return findings
