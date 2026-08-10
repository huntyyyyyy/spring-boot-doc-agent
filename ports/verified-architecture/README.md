# Verified Architecture — planning + RAG corpus

Greenfield **product planning** repository for a verified polyglot system,
plus a **RAG-oriented research corpus** shaped for both developers and coding
agents.

## What this is

| Layer | Role |
| --- | --- |
| `docs/` | Authoritative product artifacts (requirements, constraints, C4, ADRs) |
| `research/` | Evidence corpus (claim-tiered) — retrieve, don't always-load |
| `nests/` | Bounded-context folders with scoped `.mdc` rules |
| `.cursor/rules/` | Repo-wide MDC activation algebra |
| `.cursor/skills/` | Deep playbooks agents pull on demand |
| `AGENTS.md` | Thin ingest pointer (not a second rule system) |

## Product intent (short)

Ship a **polyglot verified architecture** platform: languages are first-class
peers; verification Musts are graph + locks + receipts; formal methods only
where earned. This tree is also a **RAG tool surface**: the same Markdown
corpus is retrieved for agents and developers via MDC modes + Skills + INDEX.

## RAG + MDC — how context is loaded

| Mode | When | Use here |
| --- | --- | --- |
| `alwaysApply: true` | Rare — constitution + RAG budget | Exactly 2 under `.cursor/rules/` |
| `globs:` | Path-scoped work | Nest MDCs + `docs/**` / `research/**` |
| Agent-requested | Agent pulls by description | Look-first, ATAM, polyglot topics |
| Manual `@rule` | Human attaches | Formal honesty |
| Skills | On-demand depth | `rag-retrieve`, `promote-claim` |

**Do not** convert the whole research tree into always-on `.mdc`. Theory:
`research/mdc-devex/`.

## Start here

**Agents (new repo / no chat):**  
[AGENT_BOOTSTRAP.md](AGENT_BOOTSTRAP.md) → [STATUS.md](STATUS.md) →
[AGENT_WALKTHROUGH.md](AGENT_WALKTHROUGH.md) → [STRUCTURE.md](STRUCTURE.md) →
[08-verification/VERIFY_STACK.md](08-verification/VERIFY_STACK.md)

Paste prompt: [HOW_TO_PRIME_AGENTS.md](HOW_TO_PRIME_AGENTS.md).

## Status

**No product implementation yet.** Spec / gap-fill only — see `STATUS.md`.
