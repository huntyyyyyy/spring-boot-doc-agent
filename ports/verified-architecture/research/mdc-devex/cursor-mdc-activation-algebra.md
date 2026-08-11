---
title: Cursor MDC activation algebra (Retrieval-Augmented Generation + DevEx)
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
| Mass `.md` → `.mdc`? | **No** — category error. Research/human Source of Truth stays Markdown for Retrieval-Augmented Generation. |
| Always-on budget | **≤2** slim invariants |
| Path scope Source of Truth | **MDC `globs` only** — refuse nested `AGENTS.md` as a second path system |
| Depth procedures | **Skills** + **forced frontmatter walk** (`look_first` / `related`); rules mandate + `@` skill |
| Shared Spec Model Context Protocol SoT | Same frontmatter schema — not a second catalog |
| Hard deny | **Hooks** when needed — not prose “don’t” |

See also: `research/gaps/frontmatter-forced-traversal-mcp-2026-08-10.md`.

## Activation modes (Evidenced — Cursor rules docs)

| `alwaysApply` | `description` | `globs` | Behavior | Primary use case |
| --- | --- | --- | --- | --- |
| `true` | — | — | Always in context | Constitution / Retrieval-Augmented Generation progressive-disclosure invariant |
| `false` | — | provided | Auto-attach when matching files in context | Nest bounded context work; docs/standards edits |
| `false` | provided | omitted | Agent pulls when relevant | Topic cards (Architecture Tradeoff Analysis Method, polyglot, promote-claim) |
| `false` | omitted | omitted | Manual `@`-mention only | Rare deep playbooks (formal honesty) |

## Use cases mapped (agents ∪ developers)

| Use case | Actor | Mode | Why |
| --- | --- | --- | --- |
| Never weaken draft standards form | Both | always (thin) | False-green if missing |
| Edit one nest / bounded context | Agent | globs `nests/<bc>/**` | Path-scoped lens |
| Edit RE / Architecture Decision Record / C4 | Agent + human | globs `docs/**` | Standards attach with files |
| Retrieve long research | Agent + Retrieval-Augmented Generation | agent-requested + Skill | Don’t dump corpus always-on |
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

## Forced pointing (Adopt 2026-08-10)

Always-on rules **mandate** a frontmatter graph walk (`look_first` then
`related`). Schema:
`07-system-design/schemas/va-doc-frontmatter.schema.json`. Spec corpus Model
Context Protocol tools must filter on the same keys — not a second catalog.
Rationale: `research/gaps/frontmatter-forced-traversal-mcp-2026-08-10.md`.

## Port MDC projections (Adopt 2026-08-11)

**Port scope only.** Do not bulk-rename Markdown → `.mdc` under `research/`.
Cursor only loads `.mdc` from `.cursor/rules/`. Add thin **projections** that
carry `globs`/`description` and point at MD SoTs. Inventory:
`research/mdc-devex/mdc-projection-inventory-2026-08-11.md`. Rust/WASM stack:
`research/gaps/port-mdc-projection-rust-wasm-2026-08-11.md`.
