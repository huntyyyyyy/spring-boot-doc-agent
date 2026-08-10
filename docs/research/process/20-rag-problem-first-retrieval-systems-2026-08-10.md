---
title: RAG & retrieval systems — problem-first inventory (SoT vs sensor vs adapter)
status: ACTIVE research packet — Spec seeds DRAFT; no Implement without Approve
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine (Stage-0 structure facts + query/MCP adapters)
related:
  - docs/research/process/42-problem-first-rag-ds-cli-2026-08-10.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
do_not:
  - treat embeddings / vector rank as citation SoT
  - treat RAGAS/ARES/LLM-judge as merge or certification SoT
  - treat GraphRAG LLM-extracted KG as Stage-0 fact replacement
  - unattended AI merge
  - Implement vector index / CRAG / RAPTOR as tip SoT before Spec Approve
human_review_floor: true
epics: E-RAG0 (proposed Spec gate)
stars_as_of: 2026-08-10 (GitHub API)
---

# Problem-first RAG inventory → doc-engine Embody / Adopt / Refuse

**Question.** What failure modes existed *before* each retrieval/RAG class — and
which does doc-engine already solve with **Stage-0 structure facts as citation
SoT**, vs which remain **sensors / adapters** only?

**Product map (non-negotiable):**

| Layer | Role |
| --- | --- |
| Stage-0 structure facts (ast-grep / CodeQL / scanners) | **Citation SoT** |
| Embeddings / rank / recall@k / RAGAS-style scores | **Sensors only** |
| MCP / CLI / packet envelopes | **Adapters** |
| Human Approve / Spec / merge | **Merge SoT** |

---

## 0. Verdict

| Stance | Choice |
| --- | --- |
| **Embody** | Structure-first retrieval; cite only Stage-0 (or human-approved) support; dual-sink receipts; human merge floor |
| **Adopt** | On-demand retrieve *pattern* (Self-RAG/Adaptive); hierarchical packet budgets (RAPTOR *idea*); faithfulness **as sensor** |
| **Refuse** | Embedding similarity as citation SoT; chunk-neighbor as claim support; RAGAS as merge proof; LLM GraphRAG KG as Stage-0 replacement; unattended merge |

---

## 1. Problem inventory (A–G)

| ID | Failure BEFORE the class | Job restored (claim) | Does NOT solve | Layer |
| --- | --- | --- | --- | --- |
| **A** | Parametric memory: private/current docs invisible; fine-tune slow/opaque | Non-parametric memory without retrain | Corpus truth; merge authority | Index = adapter; corpus freshness separate |
| **B** | Hallucination / unsupported claims | Ground generation in passages | Wrong passages *induce* hallucination; citation ≠ support | Faithfulness = sensor |
| **C** | Stale index; fluent but drifted | Freshness of non-parametric memory | Fresh wrong docs still wrong | Timestamp/hash = sensor |
| **D** | Citation theater: near-topic chunk ≠ claim support | Evidence provenance | Dense recall ≠ entailment | Stage-0 fingerprints = SoT; embed hit = sensor |
| **E** | Bag-of-chunks fails multi-hop / thematic Q | Structured / hierarchical / graph retrieval | LLM-extracted edges can invent relations | Deterministic AST/KG = SoT; LLM graph = sensor |
| **F** | Single-shot RAG vs agent tool loops | Tool-use / iterative retrieval | Tool loops ≠ merge authority | Query kinds = adapter; Approve = SoT |
| **G** | “Good retrieval” conflated with “good answer” | Separate IR vs faithfulness vs human grade | LLM-judge ≠ boolean merge | Recall@k / RAGAS = sensor |

---

## 2. Primaries by class

### A — Parametric memory failure

Lewis et al.: LMs cannot easily expand/revise memory, lack provenance, may hallucinate; hybrid parametric + non-parametric memory addresses revise/inspect `[Evidenced — arXiv:2005.11401]`. Lost-in-the-middle: gold in window ≠ used `[Evidenced — 2307.03172]`.

| Artifact | Fit |
| --- | --- |
| RAG (Lewis) | Founding hybrid memory recipe |
| LlamaIndex ~51k★ / LangChain ~144k★ | Orchestration **adapters** — not citation SoT |
| Chroma ~29k★ | Vector store adapter |

### B / D — Hallucination & citation support

Self-RAG reflection tokens (retrieve on demand + isSup) `[Evidenced — 2310.11511]`. CRAG: low-quality retrieval poisons generation `[Evidenced — 2401.15884]`.

**doc-engine:** claim↔span only via Stage-0 / approved facts — never via cosine.

### C — Freshness

Index hot-swap without retrain is a RAG selling point `[Evidenced — 2005.11401]`; content-hash / plant digests are the local analogue `[Confirmed]`.

### E — Multi-hop / global

| Artifact | Problem it answers |
| --- | --- |
| DPR `[2004.04906]` | Sparse lexical miss → dense dual-encoder |
| HyDE `[2212.10496]` | Query–doc asymmetry / zero-shot dense without labels |
| RAPTOR `[2401.18059]` | Flat chunks lose abstraction levels |
| GraphRAG `[2404.16130]` / `microsoft/graphrag` ~35k★ | Global QFS + “connect the dots” — DeepWiki: baseline vector RAG fails holistic corpus questions |

**Create for us:** typed query packet BC that can attach graph/rank **sensors** later — not GraphRAG tip runtime.

### F — Agent tool retrieval

Haystack ~26k★; ColBERT late interaction ~3.9k★ — ranking sensors / pipelines. MCP `dispatch_tool` is the local adapter shape `[Confirmed]`.

### G — Evaluation

RAGAS faithfulness / answer relevance / context relevance without references `[Evidenced — 2309.15217]`. **Sensor only** — same refuse class as LLM-judge ≠ fail_under.

---

## 3. DeepWiki Evaluate / Create (GraphRAG)

- **Evaluate:** Correctly names global-sensemaking and multi-hop linking failures.
- **Create:** Do **not** create GraphRAG tip SoT. Create honesty-labeled rank/community **sensors** behind packets after Spec.

---

## 4. Embody / Adopt / Refuse

| Stance | Action |
| --- | --- |
| Embody | Stage-0 facts; typed packets; cert derived≠LWW; human Approve |
| Adopt | Adaptive retrieve pattern; RAPTOR-like budgets; RAGAS-class sensors; MCP isolation |
| Refuse | Embed citation SoT; RAGAS merge gate; GraphRAG KG as Stage-0; unattended AI merge |

**Unknowns.** Exact E-QUERY packet schema; whether any rank sensor ships before E-RAG0 Approve.

**Epic:** `E-RAG0` Spec gate only — see umbrella [`42-…`](42-problem-first-rag-ds-cli-2026-08-10.md).
