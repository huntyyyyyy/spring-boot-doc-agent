# Verified Architecture — planning + Retrieval-Augmented Generation corpus

Greenfield **product planning** repository for a verified polyglot system,
plus a research corpus shaped for both developers and coding agents.

**Language:** use **whole words** in prose — see [`GLOSSARY.md`](GLOSSARY.md).

## What this is

| Layer | Role |
| --- | --- |
| `00/`–`12/` | Authoritative specification tree (preferred) |
| `docs/` | Legacy product artifacts (demoted; promote into `00/`–`12/`) |
| `research/` | Evidence corpus (claim-tiered) — retrieve, do not always-load |
| `nests/` | Legacy bounded-context folders (demoted) |
| `.cursor/rules/` | Repo-wide Cursor rule activation algebra |
| `.cursor/skills/` | Deep playbooks agents pull on demand |
| `AGENTS.md` | Thin ingest pointer (not a second rule system) |

## Product intent (short)

Ship a **polyglot verified architecture** platform: languages are first-class
peers; verification Musts are graph + locks + artifact-anchored claim memory +
Stateful Tool-Enabled Agentic Deployment tool constraints + receipts; formal
methods only where earned. This tree is also a **Retrieval-Augmented Generation
tool surface**: the same Markdown corpus is retrieved for agents and developers
via Cursor rule modes + Skills + indexes.

## How context is loaded

| Mode | When | Use here |
| --- | --- | --- |
| `alwaysApply: true` | Rare — constitution + retrieval budget | Exactly 2 under `.cursor/rules/` |
| `globs:` | Path-scoped work | Nest rules + `docs/**` / `research/**` |
| Agent-requested | Agent pulls by description | Look-first, Architecture Tradeoff Analysis Method, polyglot topics |
| Manual `@rule` | Human attaches | Formal honesty |
| Skills | On-demand depth | `rag-retrieve`, `promote-claim` |

**Do not** convert the whole research tree into always-on Cursor rules. Theory:
`research/mdc-devex/`.

## Start here

**Agents (new repository / no chat):**  
[AGENT_BOOTSTRAP.md](AGENT_BOOTSTRAP.md) → [STATUS.md](STATUS.md) →
[AGENT_WALKTHROUGH.md](AGENT_WALKTHROUGH.md) → [STRUCTURE.md](STRUCTURE.md) →
[GLOSSARY.md](GLOSSARY.md) →
[08-verification/VERIFY_STACK.md](08-verification/VERIFY_STACK.md)

Paste prompt: [HOW_TO_PRIME_AGENTS.md](HOW_TO_PRIME_AGENTS.md).

## Status

**Port ready:** YES — [`PORT_READY.md`](PORT_READY.md) (export specification corpus via [`EXPORT.md`](EXPORT.md)).  
**Implement ready:** NO — see [`STATUS.md`](STATUS.md).  
Research that closed specification gaps: [`june-august-2026-port-readiness.md`](research/papers-2026-may-aug/june-august-2026-port-readiness.md).
