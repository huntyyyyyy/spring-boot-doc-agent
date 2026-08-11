---
name: predicate-prose
description: >-
  Rewrite or review ports/verified-architecture Markdown so sentences predicate
  attributes (information gain) instead of tautologies/synonym circles — use when
  editing STATUS, ADRs, nest READMEs, Spikes, rules, or any Spec prose that only
  restates titles
---

# Skill: Predicate prose (anti-tautology)

**Scope:** `ports/verified-architecture/` only.  
**Theory:** `research/gaps/anti-tautology-predicate-prose-2026-08-11.md`.

**Adjacent:** root Skill `semantic-adversarial-review` (chat reviews / hooks) —
same three tests; that skill bans Support/Refuse scoreboards without if→then.

## Three tests (every sentence / bullet)

1. **Logical (A→B):** Delete the subject’s name from the predicate. If nothing
   informative remains, it is A→A — rewrite.  
2. **Semantic (predication):** The predicate must add an attribute, bound,
   owner, or fail-mode **not** already in the subject’s name/title.  
3. **Epistemological (information gain):** After reading, a cold agent’s set of
   *allowed next actions* must shrink. If uncertainty is unchanged, cut or replace.

## Detection checklist (fail if true)

- Body first sentence ≈ title / `H1`
- README body = folder name + “see PRECODE_MAP” only (unless file explicitly
  states **empty / zero artifacts** — that *is* information)
- Synonym pairs: complex/complicated, polyglot/multi-language, corpus/docs collection,
  Proposed/not yet decided without Accept criterion
- Policy repeated (`Refuse Python`, `FREEZE`) without a path that changes when violated
- “May or may not” / excluded-middle filler

## Forced rewrite shape

Prefer one line:

`Subject — attribute — bound (path/number/owner) — fail-mode`

| Bad (NOP) | Good (state change) |
| --- | --- |
| Rust owns the engine | Rust alone may write oracle artifacts and Spec corpus indexes; TypeScript may only present |
| Nest is a planning nest | Nest has README + optional `nest.mdc` only; no crates until Definition of Ready PASS |
| FREEZE is in effect | Editing may deepen only receipt β/ρ, claim withdrawal, or handle lifecycle — new matrices = reject |

## Architecture Decision Record rule

- **Context** = forces that exist without the decision  
- **Decision** = the choice (do not restate Context)  
- **Consequences** = at least one **negative** trade-off (Nygard)  

If Consequences only praise the Decision, it fails test 3.

## Procedure when editing

1. Run the three tests on every paragraph you touch.  
2. Prefer deleting a synonym sentence over polishing it.  
3. If a stub folder is empty, say **what is missing** (one concrete artifact name),
   not “this folder is for X.”  
4. Do not expand FREEZE scope; deepening ≠ adding tautological banners.  
5. Whole words — `GLOSSARY.md`.

## Exit

Cite which test caught each cut. Leave the file with fewer tokens and more
predicates, or leave it unchanged and say why it already passed.
