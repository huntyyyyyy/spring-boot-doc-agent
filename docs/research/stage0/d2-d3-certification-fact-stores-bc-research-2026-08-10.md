---
title: D2 Certification & attestation + D3 Fact stores & code KGs (cold BC research)
status: ACTIVE research packet — Spec seeds DRAFT; no Implement without Approve
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine
related:
  - docs/design/ddia-north-star/deviations/dev-certification-derived-view.md
  - docs/research/stage0/claim-symbol-entity-identity-adr-2026-07-30.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
do_not:
  - hand-edit or LWW-merge certification.json
  - treat embeddings as citation SoT
  - Implement FACT1/CERT1 before Spec Approve
  - adopt full SLSA product signing as merge gate without human floor
human_review_floor: true
epics: E-CERT0, E-FACT0
---

# D2 + D3 cold BC research packet (2026-08-10)

**Question.** For doc-engine cold BCs **D2 Certification & attestation** and
**D3 Fact stores & code knowledge graphs**, which external patterns (arXiv /
GitHub) should Embody / Adopt / Refuse — given invariants: `certification.json`
is **derived never LWW**; Stage-0 facts are SoR; **refuse embedding citation
SoT**; **human review floor**.

**Method.** WebSearch + WebFetch of primary abstracts/repos (2026-08-10).
Star counts via GitHub API unless noted. Tiers: **Evidenced** (fetched primary),
**Confirmed** (this repo), **Unknown** (unverified).

---

## Cross-cutting Bloom for doc-engine

| Stance | Choice |
| --- | --- |
| **Embody** | Recompute `certification.json` from stage/gate SoR `[Confirmed]` B2.5; deterministic Stage-0 fact extraction as citation-capable SoR; structure-first typed edges for query/packet |
| **Adopt** | SLSA-/in-toto-**shaped** honesty fields (builder/executor, subjects, parameters) as schema — not full SLSA product; hash-triggered incremental re-index patterns; hybrid retrieval only as **sensor** for operators |
| **Refuse** | Dual-writer / LWW certification; vacuous `certified: true`; embedding similarity as citation SoT; LLM-extracted KG replacing ast-grep/CodeQL plant; unattended AI merge; full Sigstore/SLSA signing as mandatory merge gate without human floor |

---

# D2 — Certification & attestation

**Maps to:** E-CERT0 (`pipeline/certification_fold.py`, `compliance*`,
`tools/certification.py`, `local_runner_phases/certification_finish.py`).

### Domain-level sources (≥3 arXiv + ≥2 GitHub)

#### arXiv

| ID | Title | Relevance (1 line) |
| --- | --- | --- |
| [2310.06300](https://arxiv.org/abs/2310.06300) | An Empirically Grounded Reference Architecture for Software Supply Chain Metadata Management | Frames SBOM / provenance / attestation as authenticated metadata with clear subject–predicate roles — maps to cert as derived attestation over gate facts `[Evidenced]` |
| [2409.05014](https://arxiv.org/abs/2409.05014) | Analyzing Challenges in Deployment of the SLSA Framework for Software Supply Chain Security | Documents SLSA build-track honesty (builder id, signed provenance, verifier expectations) and adoption friction — Adopt **pattern**, Refuse full product dep `[Evidenced]` |
| [2602.23193](https://arxiv.org/abs/2602.23193) | ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering | Event log as SoR + deterministic projection + projection hash — direct analogy for cert as replayable derived view `[Evidenced]` |

#### GitHub

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [sigstore/cosign](https://github.com/sigstore/cosign) | **~6.2k★**; pushed 2026-08; active releases (v3.x) | Industry attestation signing; elegant &lt;10k — Adopt honesty *shape*, Explicit Defer mandatory Cosign in CLI merge path `[Evidenced]` API |
| [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | **~12.1k★**; pushed 2026-08; CNCF graduated | Policy-as-code gates over structured evidence — pattern for compliance fold inputs, not a second SoT `[Evidenced]` API |

### Domain Bloom

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Fold inputs table vs phase runner; mock/`generative_executor` honesty | Schema fields for builder/executor/subjects (SLSA-shaped) | Derived recompute; never LWW `[Confirmed]` | Predicate honesty labels; OPA-like gate predicates as *data* | Hand-edit demos; dual-writer; LLM-judge as cert; silent mock-as-live |

---

## D2.1 — Derived views / SoR vs projection

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2602.23193](https://arxiv.org/abs/2602.23193) | ESAA: Event Sourcing for Autonomous Agents… | Immutable intention/effect log → pure projection + `projection_hash_sha256` — template for cert rebuild honesty `[Evidenced]` |
| [2203.16684](https://arxiv.org/abs/2203.16684) | DBSP: Automatic Incremental View Maintenance for Rich Query Languages | Formal IVM: views are derived; updates must preserve equivalence to full recompute `[Evidenced]` (2022; still SoT theory) |
| [2404.16486](https://arxiv.org/abs/2404.16486) | OpenIVM: a SQL-to-SQL Compiler for Incremental Computations | Compiles view maintenance to SQL deltas — Adopt *recompute-or-delta with equivalence*, Refuse treating delta store as SoR `[Evidenced]` |
| [2603.27775](https://arxiv.org/abs/2603.27775) | Enzyme: Incremental View Maintenance for Data Engineering | Cost-based choose incremental vs full refresh — Adopt full-refresh as always-correct cert fold default `[Evidenced]` |

#### GitHub (≥2)

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [kurrent-io/KurrentDB](https://github.com/kurrent-io/KurrentDB) (ex EventStore) | **~5.8k★**; pushed 2026-08; active | Event-log SoR + projections — elegant &lt;10k; pattern only, not a dep `[Evidenced]` API |
| [feldera/feldera](https://github.com/feldera/feldera) | **~2.0k★**; pushed 2026-08; active DBSP impl | Incremental view engine — elegant &lt;10k; Embody *derived* doctrine, Refuse embedding Feldera in doc-engine `[Evidenced]` API |

#### Bloom (D2.1)

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Whether fold should always full-recompute (yes default) | Explicit SoR→projection inventory in Spec | Stage/gate facts = SoR; cert = disposable projection `[Confirmed]` | IVM equivalence tests; projection hashes as sensors | Promoting certification.json to LWW SoR; eventual-consistency “good enough” for `certified` |

---

## D2.2 — Software provenance / SLSA-like honesty

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2409.05014](https://arxiv.org/abs/2409.05014) | Analyzing Challenges in Deployment of the SLSA Framework… | Builder identity, non-falsifiable provenance, verifier matching — honesty fields for `generative_executor` `[Evidenced]` |
| [2310.06300](https://arxiv.org/abs/2310.06300) | Empirically Grounded Reference Architecture for SSC Metadata | Distinguishes SBOM vs provenance vs signed attestation — keep cert predicates typed `[Evidenced]` |
| [2605.08363](https://arxiv.org/abs/2605.08363) | Kettle: Attested builds for verifiable software provenance | in-toto Statement + SLSA Provenance v1.2 predicate binding — schema reference for subjects/digests `[Evidenced]` |
| [2603.02512](https://arxiv.org/abs/2603.02512) | Human-Certified Module Repositories for the AI Age | Human certification floor + SLSA-shaped provenance for modules — aligns with human review floor `[Evidenced]` |

#### GitHub (≥2)

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [sigstore/cosign](https://github.com/sigstore/cosign) | **~6.2k★**; frequent releases | Signing/attestation tooling; Defer mandatory signing `[Evidenced]` |
| [slsa-framework/slsa-github-generator](https://github.com/slsa-framework/slsa-github-generator) | **~0.6k★**; last release ~2025-02; many open issues | Reference for provenance *shape*; elegant &lt;10k with **changelog health caution** `[Evidenced]` WebFetch |
| [in-toto/attestation](https://github.com/in-toto/attestation) | **~0.3k★**; release v1.2.0 (2026-03) | Spec SoR for statement/predicate; elegant &lt;10k `[Evidenced]` |

#### Bloom (D2.2)

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Which honesty fields land in cert schema (C0-6) | Optional predicate: builder id, params, subjects digests | Fail-closed mock/live labeling `[Confirmed]` AGENTS.md | SLSA-shaped fields; in-toto vocabulary | Full SLSA L3 hermetic builds as product SoT; Cosign as merge authority |

---

## D2.3 — Pipeline gate folding / compliance artifacts

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2511.20313](https://arxiv.org/abs/2511.20313) | A Reality Check on SBOM-based Vulnerability Management… | Compliance artifacts as noisy sensors; reachability needed — do not treat SBOM alone as certified truth `[Evidenced]` |
| [2507.10584](https://arxiv.org/abs/2507.10584) | ARPaCCino: An Agentic-RAG for Policy as Code Compliance | PaC/OPA in pipelines — Adopt machine-checkable gate predicates; Refuse agentic RAG as compliance SoT `[Evidenced]` |
| [2310.06300](https://arxiv.org/abs/2310.06300) | SSC Metadata Management reference architecture | Fold heterogeneous evidence (SBOM, provenance, attestation) under one subject — gate folding pattern `[Evidenced]` |

**Non-arXiv (marked):** MDPI *Software* 2026 Continuous Compliance Framework (CCF) — compliance lakehouse + signed attestations as **queryable derived products** `[Evidenced]` DOI 10.3390/software5010006 — use as cartography, not Spec SoT.

#### GitHub (≥2)

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | **~12.1k★**; healthy | Gate evaluation pattern over JSON facts `[Evidenced]` |
| [anchore/syft](https://github.com/anchore/syft) | **~9.4k★**; pushed 2026-08; active | SBOM generators as **compliance sensors** (near 10k bar); not cert SoR `[Evidenced]` API |

#### Bloom (D2.3)

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Enumerate phase artifacts that feed fold (C0-3) | Compliance artifact inventory + honesty labels (sensor vs SoT) | Fold is pure function of gate facts; vacuous cert is defect `[Confirmed]` E-CERT0 | OPA-like predicates; SBOM/attestation as optional evidence rows | Compliance lakehouse as tip SoT; soft-green on missing gates; LLM PaC as certified |

---

# D3 — Fact stores & code knowledge graphs

**Maps to:** E-FACT0 (`scanning/facts*`, query consumers); archive fact-store memos → promote Spec under `stage0/`.

### Domain-level sources (≥3 arXiv + ≥2 GitHub)

#### arXiv

| ID | Title | Relevance |
| --- | --- | --- |
| [2601.08773](https://arxiv.org/abs/2601.08773) | Reliable Graph-RAG for Codebases: AST-Derived Graphs vs LLM-Extracted Knowledge Graphs | Deterministic AST KG ≫ LLM KG on coverage/latency — Embody Stage-0 extraction `[Evidenced]` |
| [2603.27277](https://arxiv.org/abs/2603.27277) | Codebase-Memory: Tree-Sitter-Based Knowledge Graphs… via MCP | Structure-first MCP tools + hash incremental re-index — Adopt patterns for query/packet `[Evidenced]` |
| [2604.26523](https://arxiv.org/abs/2604.26523) | RepoDoc: A Knowledge Graph-Based Framework to Automatic Documentation Generation and Incremental Updates | RepoKG for doc generation + impact propagation — closest product analog; Adopt graph SoR for facts, refuse LLM as fact extractor `[Evidenced]` |

#### GitHub

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [tree-sitter/tree-sitter](https://github.com/tree-sitter/tree-sitter) | **~26.6k★**; pushed 2026-08; healthy | Incremental parser foundation for deterministic facts `[Evidenced]` API |
| [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) | **~65.6k★**; pushed 2026-08; very active | Structure-first local KG for agents — Adopt *patterns* (edges, blast radius), Refuse product dep / embedding SoT `[Evidenced]` API |
| [github/codeql](https://github.com/github/codeql) | **~9.9k★**; pushed 2026-08; healthy | Declarative fact DB for security queries — already in Stage-0 plant; near 10k `[Evidenced]` API |

### Domain Bloom

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Forever-sidecar vs typed edges / MAPS_TO consumers | Fact identity + edge schema Spec (FACT0) | Deterministic Stage-0 facts as citation SoR `[Confirmed]` | Incremental re-index; structure-first MCP lookups | Embedding citation SoT; LLM KG replace ast-grep/CodeQL |

---

## D3.1 — Deterministic fact extraction from code

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2601.08773](https://arxiv.org/abs/2601.08773) | Reliable Graph-RAG… AST-Derived vs LLM-Extracted | Quantifies LLM skip/miss rates vs Tree-sitter DKB — refuse LLM extraction as SoR `[Evidenced]` |
| [2603.27277](https://arxiv.org/abs/2603.27277) | Codebase-Memory… | Tree-sitter → SQLite graph → structural tools — extraction recipe `[Evidenced]` |
| [2604.26523](https://arxiv.org/abs/2604.26523) | RepoDoc… | RepoKG entity/relationship extraction as doc backbone — dual-emit without silent drop `[Evidenced]` |

#### GitHub (≥2)

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [tree-sitter/tree-sitter](https://github.com/tree-sitter/tree-sitter) | **~26.6k★** | Parser SoR for structure `[Evidenced]` |
| [joernio/joern](https://github.com/joernio/joern) | **~3.4k★**; pushed 2026-08 | Code property graphs; elegant &lt;10k — CPG ideas, not a dep `[Evidenced]` API |
| [github/codeql](https://github.com/github/codeql) | **~9.9k★** | Relational code facts for Spring signals plant `[Confirmed]` + `[Evidenced]` |

#### Bloom (D3.1)

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| ast-grep vs Tree-sitter vs CodeQL fact coverage gaps | Dual-emit contracts; fingerprint-stable fact IDs | Deterministic scanners as fact SoR `[Confirmed]` | CPG / Tree-sitter patterns; fixture↔OCS same assertion engine | LLM entity extraction as Stage-0 replacement |

---

## D3.2 — Incremental re-indexing

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2308.09660](https://arxiv.org/abs/2308.09660) | Incrementalizing Production CodeQL Analyses | Hybrid incremental Datalog; update ∝ commit size — Spike for CodeQL cache honesty `[Evidenced]` |
| [2603.27277](https://arxiv.org/abs/2603.27277) | Codebase-Memory… | XXH3 content-hash file re-index (~4× vs full) — Adopt for facts sidecar `[Evidenced]` |
| [2604.26523](https://arxiv.org/abs/2604.26523) | RepoDoc… | Semantic impact propagation for selective regen — Adopt for query packet invalidation `[Evidenced]` |

**Non-arXiv (marked):** Zhao et al., ICSE-SEIP 2023 *Incremental Call Graph Construction in Industrial Practice* (DOI 10.1109/ICSE-SEIP58684.2023.00048) — reset-recompute prune+patch, ~20× speedup; **no arXiv id found** `[Unknown]` arXiv mirror / `[Evidenced]` IEEE PDF abstract.

#### GitHub (≥2)

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [tree-sitter/tree-sitter](https://github.com/tree-sitter/tree-sitter) | **~26.6k★** | Native incremental parse API `[Evidenced]` |
| [Aider-AI/aider](https://github.com/Aider-AI/aider) | **~48.1k★**; last push 2026-05 (slower than peers) | Repo map / tree-sitter usage; Adopt map *idea*, Refuse as citation SoT `[Evidenced]` API |
| [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) | **~65.6k★** | Auto-sync on change — pattern for watch+hash `[Evidenced]` |

#### Bloom (D3.2)

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Full rebuild vs hash-scoped reindex for Stage-0 facts | Invalidation keys (path digest, plant fingerprint) | Correctness &gt; speed; full rebuild always valid SoR refresh | Content-hash reindex; CodeQL cache invalidation honesty `[Confirmed]` plant | Stale index as silent SoR; soft-reuse across plant fingerprint change |

---

## D3.3 — Structure-first retrieval vs embedding citation SoT

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2601.08773](https://arxiv.org/abs/2601.08773) | Reliable Graph-RAG… | Vector-only fails multi-hop architecture; AST graph wins — refuse embedding SoT `[Evidenced]` |
| [2509.16112](https://arxiv.org/abs/2509.16112) | CodeRAG: Finding Relevant and Necessary Knowledge… | Multi-path (sparse+dense+dataflow) — Adopt hybrid as **sensor**, structure as SoT `[Evidenced]` |
| [2602.11671](https://arxiv.org/abs/2602.11671) | Do Not Treat Code as Natural Language… (Hydra) | Chunking/similarity miss true dependencies; structure-aware indexing — Embody structure-first `[Evidenced]` |

#### GitHub (≥2)

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) | **~65.6k★** | Callers/callees/blast-radius tools — matches query packet doctrine `[Evidenced]` |
| [Aider-AI/aider](https://github.com/Aider-AI/aider) | **~48.1k★** | Repo-map structural context for agents `[Evidenced]` |
| [scip-code/scip](https://github.com/scip-code/scip) (was sourcegraph/scip) | **~0.7k★**; pushed 2026-08 | Precise symbol index protocol; elegant &lt;10k — Adopt SCIP-like identity if needed `[Evidenced]` API |

#### Bloom (D3.3)

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Packet vs full-signal reads; citation anchors = path:line from facts | Typed retrieval ports (callers/dependents/packet) | Structure-first facts as citation SoT `[Confirmed]` CLAUDE.md | Embeddings only as optional operator sensor / ranking | Embedding similarity as citation SoT; RAG chunks as claim evidence |

---

## Product decisions locked by this packet

1. **`certification.json`**: derived projection; recompute on disagreement; never LWW `[Confirmed]` + Embody D2.1.
2. **Stage-0 facts**: deterministic extraction SoR for citations `[Confirmed]` + Embody D3.1.
3. **Embeddings**: sensor only; **Refuse** as citation SoT (D3.3).
4. **Human review floor**: Spec Approve + operator Path B; no unattended cert/merge (D2.2 / 2603.02512).
5. **SLSA**: Adopt honesty *fields*; Explicit Defer product signing (C0-6).

## Unknown / open

| Item | Tier |
| --- | --- |
| Whether FACT0 store is forever-sidecar JSON vs SQLite edges | Unknown — Spike before Implement |
| Cosign/Sigstore as optional export path for cert | Unknown — Explicit Defer |
| ICSE-SEIP 2023 call-graph paper arXiv id | Unknown (IEEE only) |
| Live star counts drift after 2026-08-10 | Unknown (snapshot) |

## Exit (research)

Feeds **E-CERT0** Approve (C0-1–C0-8) and **E-FACT0** Spec promotion from archive → `stage0/`. No Implement from this packet alone.
