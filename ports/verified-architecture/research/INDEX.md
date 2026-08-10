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
