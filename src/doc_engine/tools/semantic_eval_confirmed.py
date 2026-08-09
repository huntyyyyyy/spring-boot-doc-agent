"""Mechanical Confirmed-tag vs interview_answers overlap checks."""

from __future__ import annotations

import re

CONFIRMED_TAG_RE = re.compile(r"\[Confirmed — interview, ([^\]]+)\]")

STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "this", "that", "it",
    "its", "to", "of", "in", "on", "for", "and", "or", "not", "be", "by",
    "as", "with", "at", "if", "so", "than", "then", "will", "would",
})

DEFAULT_OVERLAP_THRESHOLD = 0.15


def tokenize(text):
    """Lowercased word-set tokenization, stopwords removed, for a cheap
    Jaccard-overlap comparison — not a semantic embedding, just enough to
    tell "clearly related" from "clearly unrelated" text."""
    return {w for w in re.findall(r"[a-z0-9]+", text.lower())
            if w not in STOPWORDS and len(w) > 1}


def claim_clause(text, tag_start):
    """The sentence (or sentence fragment) immediately preceding a tag —
    the thing the tag is actually claiming to confirm, not the whole
    surrounding paragraph."""
    prefix = text[:tag_start]
    pieces = re.split(r"(?<=[.!?])\s+", prefix)
    return pieces[-1] if pieces else prefix


def answered_entry_tokens(interview_answers):
    answered = [entry for entry in interview_answers if entry.get("status") == "answered"]
    return [
        (
            tokenize(
                " ".join(str(entry.get(key, "")) for key in ("topic", "question", "answer"))
            ),
            entry,
        )
        for entry in answered
    ]


def best_overlap(clause_tokens, entry_tokens):
    best_ratio, best_entry = 0.0, None
    for tokens, entry in entry_tokens:
        if not tokens:
            continue
        overlap = len(clause_tokens & tokens) / len(clause_tokens | tokens)
        if overlap > best_ratio:
            best_ratio, best_entry = overlap, entry
    return best_ratio, best_entry


def empty_clause_finding(tag: str, clause: str) -> dict:
    return {
        "tag": tag,
        "claim_clause": clause.strip(),
        "best_overlap": 0.0,
        "closest_entry_topic": None,
        "reason": "empty or unparseable claim clause preceding the tag",
    }


def low_overlap_finding(tag: str, clause: str, best_ratio: float, best_entry) -> dict:
    return {
        "tag": tag,
        "claim_clause": clause.strip(),
        "best_overlap": round(best_ratio, 3),
        "closest_entry_topic": best_entry.get("topic") if best_entry else None,
        "reason": (
            "no interview_answers.json entry closely matches this claim — "
            "candidate hallucinated Confirmed tag, needs semantic confirmation"
        ),
    }


def finding_for_confirmed_tag(match, text, entry_tokens, overlap_threshold):
    clause = claim_clause(text, match.start())
    clause_tokens = tokenize(clause)
    if not clause_tokens:
        return empty_clause_finding(match.group(0), clause)
    best_ratio, best_entry = best_overlap(clause_tokens, entry_tokens)
    if best_ratio < overlap_threshold:
        return low_overlap_finding(match.group(0), clause, best_ratio, best_entry)
    return None


def find_unmatched_confirmed_tags(text, interview_answers, overlap_threshold=DEFAULT_OVERLAP_THRESHOLD):
    """For every [Confirmed — interview, <date>] tag in text, check whether
    its preceding claim clause has meaningful word overlap with any
    "answered" entry in interview_answers.json. A tag with no reasonably
    close entry is a candidate hallucinated-Confirmed finding — flagged
    here for a human/LLM to look at (see semantic-pipeline-eval's Step 4),
    not asserted as a confirmed hallucination by this function alone: a
    genuine paraphrase can score a low overlap too, which is exactly why
    this is a worklist, not a verdict."""
    entry_tokens = answered_entry_tokens(interview_answers)
    findings = []
    for match in CONFIRMED_TAG_RE.finditer(text):
        finding = finding_for_confirmed_tag(
            match, text, entry_tokens, overlap_threshold
        )
        if finding is not None:
            findings.append(finding)
    return findings
