---
title: D1 Query & agent retrieval (cold BC research)
status: ACTIVE research packet — Spec seeds DRAFT; no Implement without Approve
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine
related:
- docs/research/stage0/query-packet-bc-research-2026-08-10.md
- docs/research/cold-product-bc-research-map-2026-08-10.md
- docs/research/cold-bc-domain-subdomain-taxonomy-2026-08-10.md
- docs/research/process/25-tip-grounding-mcp-2026.md
- docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
- docs/research/archive/claude-lore/research/s-stf-e-mcp-isolation-adr-2026-08-08.md
- docs/research/archive/claude-lore/research/e1-s2-token-proxy-adr-2026-08-08.md
- docs/research/archive/claude-lore/research/query-seam-audit-e4-2026-08-07.md
- docs/research/se-quality-synthesis-2026-08-08.md
- src/doc_engine/query/
- adapters/mcp/
do_not:
- treat embeddings as citation SoT
- add MCP write / codegen / apply_patch tools
- accept caller-supplied root (confused deputy)
- treat packet completeness / Cover% as merge SoR
- unattended AI merge
- Implement E-QUERY1 size chops or new MCP tools before E-QUERY0 Approve
human_review_floor: true
epics: E-QUERY0
stars_as_of: 2026-08-10 (GitHub API)
last_reviewed: '2026-08-10'
---

# D1 — Query & agent retrieval (cold BC research packet, 2026-08-10)

**Question.** For doc-engine cold BC **D1 Query & agent retrieval** (typed
`query` / `context_packet` + thin MCP), which external patterns (arXiv /
GitHub / DeepWiki) should **Embody / Adopt / Refuse** — given invariants:
**human review floor**; **refuse embedding as citation SoT**; **refuse MCP
write/codegen**; **refuse unattended AI merge**; Embody tip stance
(`dispatch_tool` library SoR; server-derived root; envelope caps; stderr-only
stdio diagnostics; structure-first over dumps).

**Method.** WebSearch + WebFetch of primary abstracts/repos + DeepWiki
cartography (2026-08-10). Star counts via GitHub API. Tiers:
**Evidenced** (fetched primary), **Confirmed** (this repo), **Unknown**
(unverified / Explicit Defer).

**Maps to:** E-QUERY0 (`src/doc_engine/query/*`, `adapters/mcp/server.py`);
unblocks E-QUERY1 size work only after Q0-1–Q0-10 Approve
(`[Confirmed]` `docs/research/stage0/query-packet-bc-research-2026-08-10.md`).

---

## Cross-cutting Bloom for doc-engine (D1)

| Stance | Choice |
| --- | --- |
| **Embody** | `dispatch_tool` as library SoR; server-derived FS root; envelope + nested caps + honest `truncated`; freshness labels; stderr for diagnostics on stdio MCP; structure-first typed kinds over corpus dumps `[Confirmed]` |
| **Adopt** | Hierarchical / logical retrieval *interfaces*; RepoMap / code-KG *patterns*; fail-closed pre-action authorization *shape*; official MCP SDK only after Spike (GND9) |
| **Refuse** | Embedding similarity as citation SoT; MCP write/codegen; caller `root`; packet as Cover%/merge proof; capability-list-as-authorization theater; unattended AI merge |

---

# D1 — Domain-level sources

### Domain arXiv (≥3; agentic RAG for code + compaction + tool isolation)

| ID | Title | Relevance (1 line) |
| --- | --- | --- |
| [2602.03442](https://arxiv.org/abs/2602.03442) | A-RAG: Scaling Agentic Retrieval-Augmented Generation via Hierarchical Retrieval Interfaces | Exposes granular retrieval tools — maps to typed `query_*` + `context_packet` over dumps `[Evidenced]` |
| [2605.27123](https://arxiv.org/abs/2605.27123) | Rethinking Agentic RAG: Toward LLM-Driven Logical Retrieval Beyond Embeddings | Logical/lexical interface ≫ embedding-first — refuse embedding citation SoT `[Evidenced]` |
| [2601.08773](https://arxiv.org/abs/2601.08773) | Reliable Graph-RAG for Codebases: AST-Derived Graphs vs LLM-Extracted Knowledge Graphs | Deterministic AST KG ≫ LLM KG — Embody Stage-0 facts as retrieval SoR `[Evidenced]` |
| [2603.27277](https://arxiv.org/abs/2603.27277) | Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP | Structure-first MCP tools + hash re-index — closest external shape to query MCP `[Evidenced]` |
| [2310.05736](https://arxiv.org/abs/2310.05736) | LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models | Budget-controlled compaction — Adopt *budget honesty*, Refuse silent lossy compress as citation SoT `[Evidenced]` |
| [2601.17549](https://arxiv.org/abs/2601.17549) | Breaking the Protocol: Security Analysis of the Model Context Protocol Specification… | Protocol-level MCP threats — grounds isolation ADR S-STF-E `[Evidenced]` |

### Domain GitHub (≥2; prefer ≥10k★, recent pushes)

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | **89383★**; pushed 2026-08-10; releases 2026.7.x | Reference MCP server surface; Adopt *read patterns*, Refuse shipping write tools `[Evidenced]` API |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | **23954★**; pushed 2026-08-07; v2.0.0 (2026-07-28) | Official Python SDK — Explicit Defer pin until Spike `[Evidenced]` API |
| [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp) | **27142★**; pushed 2026-08-10; active | Stderr/logging discipline for stdio — Adopt patterns `[Evidenced]` API |
| [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) | **65600★**; pushed 2026-08-08; v1.5.0 | Structure-first agent KG — Adopt *tool kinds*, Refuse product dep `[Evidenced]` API |
| [Aider-AI/aider](https://github.com/Aider-AI/aider) | **48087★**; pushed 2026-05-22; v0.86.0 | RepoMap structural context — Adopt map *idea*; slower push cadence noted `[Evidenced]` API |

**Elegant &lt;10k:** [scip-code/scip](https://github.com/scip-code/scip) — precise symbol index protocol.

### Domain Bloom

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Packet vs full-signal kinds; tool ⊆ library surface; budget honesty | Spec Q0-1–Q0-10 locked in design memo | `dispatch_tool` SoR; server root; structure-first `[Confirmed]` | Hierarchical retrieval interfaces; RepoMap/KG patterns | Embedding citation SoT; write MCP; unattended merge |

---

## DeepWiki architecture cartography (≥4 repos)

*Evaluate/Create-level insights only; DeepWiki is cartography, not Spec SoT.*

### 1. modelcontextprotocol/python-sdk `[Evidenced]` DeepWiki

| Level | Insight for doc-engine |
| --- | --- |
| **Evaluate** | Dual API: high-level FastMCP vs low-level Server with explicit tool handlers — tip already chose thin stdio + library dispatch `[Confirmed]` |
| **Create** | Transport-agnostic core; protocol types via Pydantic — upgrade path = swap shell, keep SoR |
| **Embody** | Tools/resources/prompts as distinct primitives — maps to `QueryKindSpec` registry OCP |
| **Adopt** | Inspector/`mcp dev` for contract testing — Spike candidate, not merge gate |
| **Refuse** | Pinning SDK as mandatory runtime before Spike |

### 2. Aider-AI/aider `[Evidenced]` DeepWiki

| Level | Insight |
| --- | --- |
| **Evaluate** | `RepoMap` (tree-sitter) supplies ranked tags under context limits — same problem as `context_packet` budgets |
| **Create** | Separate edit strategies from repo understanding — OCP split mirrors query handlers vs rank/packet |
| **Embody** | Structural repo map over raw dumps for agent context |
| **Adopt** | Ranked-tag selection under token budget |
| **Refuse** | Aider as citation SoT; auto-commit codegen via MCP |

### 3. langchain-ai/langgraph `[Evidenced]` DeepWiki

| Level | Insight |
| --- | --- |
| **Evaluate** | Durable agent state ≠ Stage-0 fact SoR |
| **Create** | Human-in-the-loop interrupt — aligns with human review floor |
| **Embody** | Explicit channels/reducers over implicit shared mutable context |
| **Adopt** | HITL pause/resume *pattern* for operator Path B |
| **Refuse** | LangGraph as merge authority / certification SoT |

### 4. continuedev/continue `[Evidenced]` DeepWiki

| Level | Insight |
| --- | --- |
| **Evaluate** | Core ↔ IDE adapters via typed protocols; CodebaseIndexer uses embeddings |
| **Create** | Strict protocol boundaries — model for CLI↔MCP↔query seams |
| **Embody** | Shared core + thin adapters (matches `dispatch_tool` + stdio shell) |
| **Adopt** | Dual config surfaces; typed IPC |
| **Refuse** | Vector indexer as Stage-0 citation SoT |

### 5. openai/openai-agents-python `[Evidenced]` DeepWiki

| Level | Insight |
| --- | --- |
| **Evaluate** | Guardrails around tool loop; MCP tool category |
| **Create** | Turn loop with session history tiers |
| **Embody** | Guardrails *outside* the model for fail-closed policy |
| **Adopt** | Read-only MCP tool category + tracing as *sensor* |
| **Refuse** | Hosted write/shell tools as doc-engine MCP surface |

### 6. PrefectHQ/fastmcp (DeepWiki may index `jlowin/fastmcp`) `[Evidenced]`

| Level | Insight |
| --- | --- |
| **Evaluate** | **stdio must not mix logs into protocol stream** |
| **Create** | Provider/transform architecture — OCP for tool registration |
| **Embody** | Decorator registration; stdio for local hosts |
| **Adopt** | Explicit transport choice; inspector/dev UX |
| **Refuse** | Background-task write side-effects on query server |

### 7. tree-sitter/tree-sitter `[Evidenced]` DeepWiki

| Level | Insight |
| --- | --- |
| **Evaluate** | Incremental CST + query language — foundation for structure-first retrieval |
| **Embody** | Deterministic structure over NL chunking for code citations |
| **Adopt** | Incremental update API for fact/index freshness |
| **Refuse** | Treating parse trees as optional when claiming `[Evidenced]` path:line |

---

# D1.1 — Context packets / compaction / token budgets

**Tip Embody (Confirmed):** `context_packet` emits ranked **pointers** (`row_ref`), not payload dumps; token proxy Option A = `len(json.dumps(emission)) // 4` with no silent field exclusion; nested lists capped; honesty labels on truncate.

### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2310.05736](https://arxiv.org/abs/2310.05736) | LLMLingua… | Explicit compression **budget controller** — Adopt budget as first-class; Refuse opaque drop `[Evidenced]` |
| [2310.06839](https://arxiv.org/abs/2310.06839) | LongLLMLingua… | Question-aware compression + reorder against lost-in-the-middle `[Evidenced]` |
| [2403.12968](https://arxiv.org/abs/2403.12968) | LLMLingua-2… | Faithful task-agnostic compression — caution: faithfulness ≠ citation integrity `[Evidenced]` |
| [2501.16214](https://arxiv.org/abs/2501.16214) | Provence: efficient and robust context pruning for RAG | Prune + rerank with honesty about retained context `[Evidenced]` |
| [2510.05381](https://arxiv.org/abs/2510.05381) | Context Length Alone Hurts LLM Performance Despite Perfect Retrieval | Embody fail-closed budgets / prefer short packets `[Evidenced]` |
| [2606.26105](https://arxiv.org/abs/2606.26105) | Context Recycling for Long-Horizon LLM Inference | Fixed-budget workspace + compaction — Adopt recycle *doctrine* `[Evidenced]` |
| [2307.03172](https://arxiv.org/abs/2307.03172) | Lost in the Middle: How Language Models Use Long Contexts | Foundational position-bias motivating ranked short packets `[Evidenced]` |

### GitHub (≥2)

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [Aider-AI/aider](https://github.com/Aider-AI/aider) | **48087★**; RepoMap under token limits | Structural compaction pattern `[Evidenced]` |
| [letta-ai/letta](https://github.com/letta-ai/letta) | **~24k★**; MemGPT lineage | Adopt *workspace recycle* idea, Refuse as citation SoT |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | **39331★**; pushed 2026-08-09 | Checkpointed short-term channels vs unbounded chat dump `[Evidenced]` |

### Bloom (D1.1)

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Whether tokensUsed matches serialized emission (Option A) | Explicit packet vs full-signal kinds in Spec (Q0-1/Q0-2) | Pointer packets; fail-closed truncate + `truncated` `[Confirmed]` | Question-aware rank; hierarchical load | Silent payload exclusion from budget; dump-full-corpus; LLMLingua as citation SoT |

---

# D1.2 — MCP isolation / tool surface contracts

**Tip Embody (Confirmed):** ADR S-STF-E — server-derived root only; `dispatch_tool` pops caller `root`; path pin under root; tools read-only; thin stdio adapter; startup errors on **stderr**; JSON-RPC on stdout.

### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2601.17549](https://arxiv.org/abs/2601.17549) | Breaking the Protocol… MCP security analysis | Capability attestation absence + multi-server trust — grounds minimal tool surface `[Evidenced]` |
| [2604.05969](https://arxiv.org/abs/2604.05969) | A Formal Security Framework for MCP-Based AI Agents… | Threat taxonomy + trust-boundary — Adopt isolation properties `[Evidenced]` |
| [2604.07551](https://arxiv.org/abs/2604.07551) | MCP-DPT: A Defense-Placement Taxonomy… | Places defenses at Host/Client/Server layers `[Evidenced]` |
| [2603.20953](https://arxiv.org/abs/2603.20953) | Before the Tool Call: Deterministic Pre-Action Authorization… | Fail-closed PDP/PEP *before* side effects `[Evidenced]` |
| [2606.28679](https://arxiv.org/abs/2606.28679) | Capability Gates Are Not Authorization… | Exposing tools ≠ authorizing calls — matches “no caller root” `[Evidenced]` |

### GitHub (≥2)

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | **23954★**; v2 releases | Protocol SoR candidate after Spike `[Evidenced]` |
| [modelcontextprotocol/inspector](https://github.com/modelcontextprotocol/inspector) | **~10.6k★**; pushed 2026-08-09 | Contract testing UI — Adopt for MCP surface audits |
| [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp) | **27142★** | Stdio/HTTP transport discipline `[Evidenced]` |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | **~28.5k★** | Guardrails + MCP tool category — pattern only |

### Bloom (D1.2)

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Tool names ⊆ library registry; path escape tests | Isolation contract in Spec (Q0-4/Q0-5); SDK Spike exit criteria | Server root; pop `root`; read-only tools; thin adapter `[Confirmed]` | Pre-action auth *shape*; Inspector audits | Write/codegen MCP; caller root; capability-list-as-auth; SDK pin without Spike |

---

# D1.3 — Rank / freshness / envelope honesty

**Tip Embody (Confirmed):** Freshness labels ∈ {`live`, `fresh_indexed`, `stale`, `unknown`} — never invent freshness; envelope carries `truncated` / `count` / `schema_version`; deterministic bucket priorities in `rank.py`.

### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2604.14227](https://arxiv.org/abs/2604.14227) | FRESCO: Benchmarking and Optimizing Re-rankers for Evolving Semantic Conflict in RAG | Re-rankers bias to rich-but-obsolete docs — Embody explicit freshness labels `[Evidenced]` |
| [2607.04281](https://arxiv.org/abs/2607.04281) | Risk-Constrained Freshness-Aware Semantic Caching… | Cache reuse as risk-constrained temporal inference `[Evidenced]` |
| [2601.17824](https://arxiv.org/abs/2601.17824) | OwlerLite: Scope- and Freshness-Aware Web Retrieval for LLM Assistants | Scope + freshness as first-class retrieval dimensions `[Evidenced]` |
| [2509.17486](https://arxiv.org/abs/2509.17486) | AttnComp: Attention-Guided Adaptive Context Compression for RAG | Adaptive retain-until-budget — related to honest trim `[Evidenced]` |
| [2406.04744](https://arxiv.org/abs/2406.04744) | CRAG — Comprehensive RAG Benchmark | Eval for retrieval honesty / rejection — sensor for operator harnesses `[Evidenced]` |

### GitHub (≥2)

| Repo | Stars / recency / health | Note |
| --- | --- | --- |
| [getzep/graphiti](https://github.com/getzep/graphiti) | **29718★**; pushed 2026-08-07 | Real-time temporal KG — Adopt *freshness-aware edges* pattern `[Evidenced]` |
| [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) | **65600★**; auto-sync on change | Structure + change sync — pattern for stale vs live `[Evidenced]` |
| [continuedev/continue](https://github.com/continuedev/continue) | **35414★**; pushed 2026-08-09 | Indexer + chat — embeddings as *sensor* only for us `[Evidenced]` |

### Bloom (D1.3)

| Evaluate | Create | Embody | Adopt | Refuse |
| --- | --- | --- | --- | --- |
| Whether every envelope can lie about freshness/truncation | Spec Q0-2/Q0-3: budgets fail-closed; freshness labels mandatory | `truncated` + freshness enums; unknown &gt; fake-fresh `[Confirmed]` | FRESCO-style recency conflict tests; temporal risk gates | Silent stale hits; embedding rank as citation truth; soft-green on unknown freshness |

---

## Product decisions locked by this packet (→ E-QUERY0)

| ID | Decision | Tier |
| --- | --- | --- |
| **Q0-1** | Packet vs full-signal kinds stay explicit; no silent full-corpus dumps | Embody + `[Confirmed]` tip |
| **Q0-2** | Token/rank budgets fail-closed; truncate with honesty labels | Embody E1-S2 `[Confirmed]` |
| **Q0-3** | Freshness labels on envelopes | Embody `[Confirmed]` |
| **Q0-4** | MCP tools ⊆ library `dispatch_tool` surface; adapter stays thin stdio | Embody E3-S1 `[Confirmed]` |
| **Q0-5** | Isolation ADR S-STF-E binding (server root; no caller `root`) | Embody `[Confirmed]` |
| **Q0-6** | E-QUERY1 size splits follow ports/strategies — no utils bag | Constitution `[Confirmed]` |
| **Q0-7** | Tip-grounding tools stay on E-GND0 (not this epic) | Portfolio map `[Confirmed]` |
| **Q0-8** | Human review of agent citations remains floor | human_review_floor |
| **Q0-9** | Official MCP SDK Explicit Defer until Spike | `[Unknown]` product choice |
| **Q0-10** | ≥10k★ bar for any new query runtime SoR | gh_sor_bar doctrine |

**Refuse (non-negotiable):** embedding citation SoT; MCP write/codegen; unattended AI merge; packet completeness as Cover%/merge proof.

---

## Adversarial review checklist

| # | Attack / failure mode | Expected defense |
| --- | --- | --- |
| 1 | Confused deputy via `root` / path escape | `args.pop("root")` + path-inside-root `[Confirmed]` |
| 2 | Stdio protocol corruption by logs | Diagnostics → stderr; JSON-RPC → stdout `[Confirmed]` |
| 3 | Budget lie (exclude payload from proxy) | Option A ADR; count full emission JSON `[Confirmed]` |
| 4 | Stale index presented as live | Freshness labels; unknown default `[Confirmed]` |
| 5 | Embedding chunk cited as Stage-0 evidence | Refuse; structure-first facts + path:line `[Confirmed]` |
| 6 | Write/codegen tool “just for convenience” | Refuse; readOnlyHint; S-STF-E `[Confirmed]` |
| 7 | Capability list treated as authorization | 2606.28679 — gates ≠ auth `[Evidenced]` |
| 8 | Agent merges without human Spec/operator review | human_review_floor |
| 9 | SDK pin without Spike | Q0-9 Explicit Defer |
| 10 | Packet used as quality/Cover% floor | Refuse; sensors ≠ SoT |

---

## Unknown / open

| Item | Tier |
| --- | --- |
| Whether/when to pin `modelcontextprotocol/python-sdk` vs keep thin stdio | Unknown — Spike (Q0-9) |
| Token proxy chars//4 vs tokenizer-accurate for operator dashboards | Unknown — sensor only; Option A remains Spec SoR |
| Tip-grounding tools schedule vs E-QUERY0 | Unknown — E-GND0 |
| Live star counts after 2026-08-10 | Unknown (API snapshot) |

---

## Exit (research)

Feeds **E-QUERY0** Approve of Q0-1–Q0-10. **No Implement** from this packet alone. Human review remains the merge floor.
