---
name: semantic-adversarial-review
description: >-
  Write adversarial / principal-SE reviews as if→then entailments, not
  Support/Refuse/Nuance scoreboard stamps — use when the user asks for an
  adversarial review, architecture review of a proposed package, or critique
  of Implement-Ready / FREEZE / ADR / DDL / ICD claims
---

# Skill: Semantic adversarial review

**Hook:** `.cursor/hooks/inject_semantic_review.py` (beforeSubmitPrompt) +
`audit_semantic_review_response.py` / `stop_semantic_review_rewrite.py`.  
**Adjacent Spec skill:** `ports/verified-architecture/.cursor/skills/predicate-prose/SKILL.md`.

## Fail-mode (banned shape)

“It is raining; it is wet.” — restating the claim as a verdict stamp.

Banned as the *spine* of a review:

- Tables whose load-bearing cell is only Support / Refuse / Nuance / Embody
- Paragraphs that open `**Refuse.**` / `**Support.**` and then paraphrase the
  same claim without a new predicate
- “Claim-by-claim” scoreboards that never say what follows if a premise holds

## Required shape

Lead with entailments:

`If <premise from disk or external SoT>, then <consequence the proposal did not already state>.`

Examples:

- If the registry is wipe/rebuild derived, then a `lock_registry` row cannot be
  the single-writer mechanism (rebuild erases the lock).
- If LockCheck means policy IR ↔ edges, then `validate_write` on SQL leases is a
  different predicate — renaming it LockCheck is not a resolution.
- If digests of Must-spine papers are absent, then a “140+ paper validation
  layer” cannot Adopt the DDL.

## Procedure

1. Collate ground-truth paths (read them); do not invent parallel SoT files.
2. For each load-bearing proposal sentence, write one if→then that would be
   false if the proposal were good — or true and blocking.
3. Use Embody / Adopt / Refuse only as a **disposition after** the entailment,
   never as the only content of a row.
4. Mark claim tiers on the *evidence*, not on the slogan.
5. Keep DoR / FREEZE honest: prose does not PASS rows.

## Exit

A cold reader can act differently after the review (reject a path, open a Spike,
deepen one vector). If they only learn “Refuse,” rewrite.
