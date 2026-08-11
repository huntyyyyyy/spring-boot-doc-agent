---
title: Research corpus index
role: rag-ingest-map
audience: [developer, agent, rag]
doc_role: index
freeze_class: read_only
look_first:
  - STATUS.md
  - gaps/frontmatter-forced-traversal-mcp-2026-08-10.md
  - ../07-system-design/schemas/va-doc-frontmatter.schema.json
mcp_tools:
  - spec_lookup
  - spec_gap
accepted: false
corpus_version: '2026-08-10'
related:
  - gaps/frontmatter-forced-traversal-mcp-2026-08-10.md
  - gaps/spec-corpus-mcp-polyglot-2026-08-10.md
  - mdc-devex/cursor-mdc-activation-algebra.md
---

# Research corpus index

Use this file as the **Retrieval-Augmented Generation catalog**. Chunk by file; embed `title` + first H2
+ claim-tier tags from frontmatter when present.

## Topic packs

| Pack | Path | Use when |
| --- | --- | --- |
| **Architecture brief (principal)** | `07-system-design/ARCHITECTURE_BRIEF.md` | Shape, minimum viable product, math, leaders |
| **Paper digest framework** | `research/method/paper-digest-framework.md` | Type keys + sections + references walk (arXiv has categories, **not** paper-type fields) |
| **Paper digest template** | `research/method/PAPER_DIGEST_TEMPLATE.md` | Fill one file per arXiv id under `papers-2026-may-aug/digests/` |
| **Worked digest example** | `research/papers-2026-may-aug/digests/2608.04278-ea-graph.md` | Empirical + section map for Artifact-Anchored Verification Memory |
| **Shallow approvals deep-dive** | `research/gaps/shallow-approvals-deep-dive-2026-08-10.md` | Model Context Protocol `2026-07-28` stateless, receipts, claims, lock IR, freshness, harness, Quality Attribute Scenario, C4 + agent-codegen bites |
| **Shallow decisions honesty / FREEZE** | `research/gaps/shallow-decisions-honesty-2026-08-10.md` | Overclaim audit; deepen-max-3; demote Chosen→Working hypothesis |
| **Parallel predicate rewrite plan** | `research/gaps/parallel-predicate-rewrite-plan-2026-08-11.md` | Domain-isolated fan-out partitions A–F |
| **Anti-tautology / predicate prose** | `research/gaps/anti-tautology-predicate-prose-2026-08-11.md` | A→B tests; Skill `predicate-prose` |
| **Port MDC projections + Rust/WASM** | `research/gaps/port-mdc-projection-rust-wasm-2026-08-11.md` | Port-only: thin `.mdc` projections; Rust Spec host; WASM guest Could |
| **MDC projection inventory** | `research/mdc-devex/mdc-projection-inventory-2026-08-11.md` | Which port MD stay MD vs get Cursor projections |
| **Forced pointing + frontmatter / Spec Model Context Protocol** | `research/gaps/frontmatter-forced-traversal-mcp-2026-08-10.md` | MDC mandates graph walk; shared FM schema with Spec tools |
| **Spec corpus Model Context Protocol + polyglot** | `research/gaps/spec-corpus-mcp-polyglot-2026-08-10.md` | Read-only Spec Model Context Protocol vs product verify; Rust/WebAssembly/Go feature map |
| **Model Context Protocol open items (schemas / mint / fixtures)** | `research/gaps/mcp-open-items-research-2026-08-10.md` | Per-tool JSON Schema 2020-12, `snapshot_open`, DynamicMCPBench effect fixtures |
| **Spec / corpus Model Context Protocol polyglot** | `research/gaps/spec-corpus-mcp-polyglot-2026-08-10.md` | Read-only Spec Model Context Protocol (not product verify); software development kit tiers; Rust/WebAssembly/Go/TS/Python/Ruby/Clojure; Architectures A–D |
| **DynamicMCPBench digest** | `research/papers-2026-may-aug/digests/2607.20531-dynamicmcpbench.md` | Effect checkpoints, minefields, Tier-1; engine pending |
| **Decision Framework** | `docs/standards/decision-framework.md` | Six-vector Selection Taxonomy (Decision Matrix / Architecture Decision Record companion / Governance) |
| **Math / formal brainstorm** | `research/atam-formal/math-decision-methods-brainstorm-2026-08-10.md` | Temporal Logic of Actions / Alloy / theorem provers / Java Modelling Tools / Analytic Hierarchy Process / Monte Carlo — **ideas only, not Must** |
| **Cursor rules catalog** | `.cursor/rules/README.md` | Activation modes; FREEZE in constitution; dual globs for monorepo |
| **Architecture Tradeoff Analysis Method + formal boundaries** | `research/atam-formal/atam-qas-adr-formal-boundaries-2026-08-10.md` | Quality Attribute Scenarios before Design; TLA+/Verus honesty |
| **Model Context Protocol Decision Matrix** | `07-system-design/decisions/mcp-decision-matrix.md` | Usage cases UC-Model Context Protocol-01…08, planned code loci, scored alternatives |
| **Model Context Protocol open-items research** | `research/gaps/mcp-open-items-research-2026-08-10.md` | Per-tool schemas, snapshot_open, DynamicMCPBench plants |
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
| Architecture Tradeoff Analysis Method / formal | `research/atam-formal/` | Quality Attribute Scenario, tactics, Architecture Decision Record method, formal bounds |
| Polyglot portfolio | `research/polyglot/` | Language peers, WebAssembly, mental models |
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
