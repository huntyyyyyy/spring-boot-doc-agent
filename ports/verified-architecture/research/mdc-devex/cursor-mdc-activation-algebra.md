---
title: Cursor MDC activation algebra (RAG + DevEx)
status: RESEARCH COMPLETE
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
audience: [developer, agent, rag]
sources:
  primary_docs:
    - https://cursor.com/docs/context/rules
    - https://cursor.com/docs/skills.md
    - https://cursor.com/llms.txt
---

# MDC activation algebra — agents and developers

**Question.** How do we use Cursor Project Rules so coding agents stay correct
and token-efficient, while developers still get progressive disclosure from
the same corpus?

## Verdict

| Question | Answer |
| --- | --- |
| Mass `.md` → `.mdc`? | **No** — category error. Research/human SoT stays Markdown for RAG. |
| Always-on budget | **≤2** slim invariants |
| Path scope SoT | **MDC `globs` only** — refuse nested `AGENTS.md` as a second path system |
| Depth procedures | **Skills** (progressive disclosure); rules mandate + `@` skill |
| Hard deny | **Hooks** when needed — not prose “don’t” |

## Activation modes (Evidenced — Cursor rules docs)

| `alwaysApply` | `description` | `globs` | Behavior | Primary use case |
| --- | --- | --- | --- | --- |
| `true` | — | — | Always in context | Constitution / RAG progressive-disclosure invariant |
| `false` | — | provided | Auto-attach when matching files in context | Nest BC work; docs/standards edits |
| `false` | provided | omitted | Agent pulls when relevant | Topic cards (ATAM, polyglot, promote-claim) |
| `false` | omitted | omitted | Manual `@`-mention only | Rare deep playbooks (formal honesty) |

## Use cases mapped (agents ∪ developers)

| Use case | Actor | Mode | Why |
| --- | --- | --- | --- |
| Never weaken draft standards form | Both | always (thin) | False-green if missing |
| Edit one nest / BC | Agent | globs `nests/<bc>/**` | Path-scoped lens |
| Edit RE / ADR / C4 | Agent + human | globs `docs/**` | Standards attach with files |
| Retrieve long research | Agent + RAG | agent-requested + Skill | Don’t dump corpus always-on |
| Promote research → `docs/` | Human/agent | agent-requested Skill | Explicit promotion gate |
| Formal “proved” claims | Agent | manual `@` | Rare; high damage if wrong |
| Developer reading path | Human | Markdown nests + INDEX | Same taxonomy, no alwaysApply |

## Explicit refuse

- Converting the research tree into always-on `.mdc`
- Growing `alwaysApply` “to be safe”
- Nested `AGENTS.md` path-scoping **beside** MDC globs
- Pasting full Skills into rules

## Implementation in this repo

See `.cursor/rules/` and `.cursor/skills/`. Catalog: `research/INDEX.md`.
