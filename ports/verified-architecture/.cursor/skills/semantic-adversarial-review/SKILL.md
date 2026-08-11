---
name: semantic-adversarial-review
description: >-
  Write adversarial / principal-SE reviews as if→then entailments, not
  Support/Refuse/Nuance scoreboard stamps — use when reviewing Implement-Ready
  packages, ADR/DDL/ICD proposals, FREEZE claims, or slogan-heavy Spec text
  under ports/verified-architecture
---

# Skill: Semantic adversarial review (port)

**Monorepo tip hooks (SoT):** repo-root `.cursor/hooks/inject_semantic_review.py`
(+ audit + stop rewrite). Those run whenever the workspace root is this tip —
including edits under `ports/verified-architecture/`.

**If this folder is exported as its own GitHub root:** copy the tip hook scripts
+ `hooks.json` entries, or the inject will not fire. This Skill still applies
via Cursor Skills discovery under `.cursor/skills/`.

**Theory (Embody):** `research/gaps/anti-tautology-predicate-prose-2026-08-11.md`
— Logical A→B, Semantic predication, Epistemological information-gain (Nygard
consequences; progressive disclosure ≠ predication `[Evidenced — arXiv:2607.17598]`).

**Adjacent Spec skill:** `.cursor/skills/predicate-prose/SKILL.md`.

## Fail-mode

“It is raining; it is wet.” Verdict stamps / Support–Refuse tables that restate
the claim without a new predicate.

## Required shape

`If <premise from disk or external SoT>, then <consequence the proposal did not already state>.`

Disposition (Embody / Adopt / Refuse) only **after** the entailment.

## Exit

Cold reader’s next action set shrinks (reject a path, open a Spike, deepen one
vector). If they only learn “Refuse,” rewrite.
