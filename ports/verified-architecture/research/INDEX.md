---
title: Research corpus index
role: rag-ingest-map
audience: [developer, agent, rag]
---

# Research corpus index

Use this file as the **RAG catalog**. Chunk by file; embed `title` + first H2
+ claim-tier tags from frontmatter when present.

## Topic packs

| Pack | Path | Use when |
| --- | --- | --- |
| **Architecture brief (principal)** | `07-system-design/ARCHITECTURE_BRIEF.md` | Shape, MVP, math, leaders |
| **Paper digest framework** | `research/method/paper-digest-framework.md` | Type keys + sections + references walk (arXiv has categories, **not** paper-type fields) |
| **Paper digest template** | `research/method/PAPER_DIGEST_TEMPLATE.md` | Fill one file per arXiv id under `papers-2026-may-aug/digests/` |
| **Worked digest example** | `research/papers-2026-may-aug/digests/2608.04278-ea-graph.md` | Empirical + section map for Artifact-Anchored Verification Memory |
| **Shallow approvals deep-dive** | `research/gaps/shallow-approvals-deep-dive-2026-08-10.md` | MCP `2026-07-28` stateless, receipts, claims, lock IR, freshness, harness, QAS, C4 + agent-codegen bites |
| **Shallow decisions honesty / FREEZE** | `research/gaps/shallow-decisions-honesty-2026-08-10.md` | Overclaim audit; deepen-max-3; demote Chosen→Working hypothesis |
| **Spec corpus MCP + polyglot** | `research/gaps/spec-corpus-mcp-polyglot-2026-08-10.md` | Read-only Spec MCP vs product verify; Rust/WASM/Go feature map |
| **MCP open items (schemas / mint / fixtures)** | `research/gaps/mcp-open-items-research-2026-08-10.md` | Per-tool JSON Schema 2020-12, `snapshot_open`, DynamicMCPBench effect fixtures |
| **Spec / corpus MCP polyglot** | `research/gaps/spec-corpus-mcp-polyglot-2026-08-10.md` | Read-only Spec MCP (not product verify); SDK tiers; Rust/WASM/Go/TS/Python/Ruby/Clojure; Architectures A–D |
| **DynamicMCPBench digest** | `research/papers-2026-may-aug/digests/2607.20531-dynamicmcpbench.md` | Effect checkpoints, minefields, Tier-1; engine pending |
| **Decision Framework** | `docs/standards/decision-framework.md` | Six-vector Selection Taxonomy (Decision Matrix / ADR companion / Governance) |
| **Math / formal brainstorm** | `research/atam-formal/math-decision-methods-brainstorm-2026-08-10.md` | TLA+ / Alloy / theorem provers / JMT / AHP / Monte Carlo — **ideas only, not Must** |
| **ATAM + formal boundaries** | `research/atam-formal/atam-qas-adr-formal-boundaries-2026-08-10.md` | Quality Attribute Scenarios before Design; TLA+/Verus honesty |
| **MCP Decision Matrix** | `07-system-design/decisions/mcp-decision-matrix.md` | Usage cases UC-MCP-01…08, planned code loci, scored alternatives |
| **MCP open-items research** | `research/gaps/mcp-open-items-research-2026-08-10.md` | Per-tool schemas, snapshot_open, DynamicMCPBench plants |
| **Lock / receipt Decision Matrices** | `07-system-design/decisions/lock-ir-decision-matrix.md`, `receipt-decision-matrix.md` | Six-vector selection for G-L1 / G-R1 |
| **C4 + confidence** | `07-system-design/c4/C4-BRIEF-CONFIDENCE.md` | Context/Container sketch with per-entity scores |
| **Port readiness audit (honesty)** | `research/gaps/entity-adoption-audit-2026-08-10.md` | Papers understood vs ≥5 genuine GitHub algorithm adopters — **D0 FAIL** |
| **Port readiness (June–August 2026)** | `research/papers-2026-may-aug/june-august-2026-port-readiness.md` | Earlier memo — **superseded on depth** by the adoption audit |
| **Whole-words glossary** | `GLOSSARY.md` (repo root) | Prefer full phrases over bare short labels |
| **Jul–Aug adversarial** | `research/adversarial/july-august-2026-overturn-review.md` | Did new papers overturn us? |
| **Leaders / GitHub adoption** | `research/leaders-adoption/` | Who leads vs who ships |
| **Pre-code BFS taxonomy** | `research/pre-code-bfs/` | Classify domains before AI codegen |
| **Papers May–Aug 2026** | `research/papers-2026-may-aug/` | Cross-domain science + RE evidence |
| Layers of Truth / vision | `research/layers-of-truth/` | Product intent, local-first verification story |
| Adversarial + RE critique | `research/adversarial/` | Threaten Draft REQs; MoSCoW honesty |
| ATAM / formal | `research/atam-formal/` | QAS, tactics, ADR method, formal bounds |
| Polyglot portfolio | `research/polyglot/` | Language peers, WASM, mental models |
| MDC / DevEx / context | `research/mdc-devex/` | Activation algebra; agents + developers |
| Provenance | `research/PROVENANCE.md` | What this corpus is (no prior-repo identity) |
| Nested domain tree | `PRECODE_MAP.md` + `00-`…`12-` | Industry-shaped pre-code folders |

## Claim tiers

- **Evidenced** — citation supports the claim
- **Confirmed** — widely accepted or replicated
- **Unknown** — must not be silently upgraded

## Ingest rules

1. Prefer retrieving from `research/` over dumping into always-on agent context
2. Promote into `00/`–`12/` only via Skill `promote-claim` (legacy `docs/` demoted)
3. Nest MDCs point at *which* pack to retrieve — they do not inline the pack
4. Never mass-rename corpus Markdown into always-on `.mdc`
