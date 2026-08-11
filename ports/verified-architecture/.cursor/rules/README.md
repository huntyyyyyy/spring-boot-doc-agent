---
title: Cursor rules catalog — activation modes
status: ACTIVE
date: '2026-08-10'
---

# `.cursor/rules` catalog

Activation algebra: `research/mdc-devex/cursor-mdc-activation-algebra.md`.
Budget: **≤2** `alwaysApply: true`. Depth → Skills. Path → `globs` (port-root
*and* `ports/verified-architecture/…` for monorepo tips).

| File | Mode | Role |
| --- | --- | --- |
| `00-constitution.mdc` | always | FREEZE, dual surfaces, Must spine, circular-Why refuse |
| `01-rag-progressive-disclosure.mdc` | always | Forced pointing: frontmatter `look_first`/`related` + Spec tools |
| `02-working-draft-standards.mdc` | globs requirements/constraints | Standards form |
| `03-architecture-docs.mdc` | globs `07-system-design` + adr/c4 | Decisions / Interface Control Documents / C4 |
| `04-research-corpus.mdc` | globs `research/**` | Claim tiers + honesty |
| `05-look-first.mdc` | agent-requested | Domain map |
| `06-atam-qas-topic.mdc` | agent-requested | Quality Attribute Scenarios |
| `07-polyglot-topic.mdc` | agent-requested | Language lanes |
| `08-formal-honesty-manual.mdc` | manual `@` | Proof claims |
| `09-cold-start.mdc` | agent-requested | Lost session |
| `10-verification-stack.mdc` | globs `08-verification/**` | Locks/claims/receipts |
| `11-mcp-surfaces.mdc` | agent-requested | Spec vs verify Model Context Protocol |
| `projections/*.mdc` | globs / agent-requested | Thin pointers at MD SoTs (Wave-0) — see inventory |

Nests: `nests/*/.cursor/rules/nest.mdc` — thin, dual globs, one nest at a time.

**Port-only policy:** do not rename `research/**` or ADR/QAS bodies to `.mdc`.
Cursor only activates `.mdc` under `.cursor/rules/`. Inventory:
`research/mdc-devex/mdc-projection-inventory-2026-08-11.md`. Research:
`research/gaps/port-mdc-projection-rust-wasm-2026-08-11.md`.

Parent monorepo also has `.cursor/rules/verified-architecture-port.mdc` (globs
`ports/verified-architecture/**`).
