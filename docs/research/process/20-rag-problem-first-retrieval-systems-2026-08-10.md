---
title: RAG & retrieval systems — problem-first inventory (SoT vs sensor vs adapter)
status: ACTIVE research packet — Spec seeds DRAFT; no Implement without Approve
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine (Stage-0 structure facts + query/MCP adapters)
related:
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
  - docs/research/archive/claude-lore/research/query-seam-audit-e4-2026-08-07.md
  - docs/research/archive/claude-lore/research/s-stf-e-mcp-isolation-adr-2026-08-08.md
  - docs/research/archive/claude-lore/research/e1-s2-token-proxy-adr-2026-08-08.md
  - src/doc_engine/query/
  - adapters/mcp/
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

**Question.** What human/system failure modes existed *before* each major
retrieval / RAG class — and which of those failures does doc-engine already
solve with **Stage-0 structure facts as citation SoT**, vs which remain open
as **sensors / adapters** only?

**Method.** Primary arXiv abstracts + GitHub README/API star counts + DeepWiki
cartography (Evaluate/Create only). Tiers: **`[Evidenced]`** fetched primary ·
**`[Confirmed]`** this repo · **`[Unknown]`** unverified / Explicit Defer.

**Product map (cold invariants — non-negotiable):**

| Layer | Role in doc-engine |
| --- | --- |
| Stage-0 structure facts (ast-grep / CodeQL / scanners) | **Citation SoT** |
| Embeddings / rank / recall@k / RAGAS-style scores | **Sensors only** |
| MCP / CLI / packet envelopes | **Adapters** |
| Human Approve / Spec / merge | **Merge SoT** |

---

## 0. One-page verdict

| Stance | Choice |
| --- | --- |
| **Embody** | Structure-first retrieval over bag-of-chunks; cite only what Stage-0 (or human-approved fact) supports; dual-sink receipts; human merge floor `[Confirmed]` |
| **Adopt** | Adaptive / on-demand retrieve *pattern* (Self-RAG / FLARE / Adaptive-RAG); hierarchical packet budgets (RAPTOR *idea*); agent tool-shaped query kinds (A-RAG); faithfulness *as sensor* (RAGAS Faithfulness class) |
| **Refuse** | Embedding similarity as citation SoT; chunk-neighbor as claim support; RAGAS/ARES as merge proof; LLM-extracted GraphRAG KG as Stage-0 replacement; unattended merge from “good answer” metrics |

---

## 1. Problem inventory (A–G)

| ID | Failure mode BEFORE the class | Restored job / invariant (claim) | Category errors (does NOT solve) | SoT / sensor / adapter |
| --- | --- | --- | --- | --- |
| **A** | Parametric memory: model lacks private / current docs; fine-tune is slow/opaque | Non-parametric memory updatable without retrain | Does not make retrieved text *true*; does not fix bad chunking | Index = **adapter** to corpus; corpus freshness = separate SoT |
| **B** | Hallucination / unsupported claims when answering from (or without) corpus | Ground generation in retrieved passages | Retrieval of *wrong* passages can *induce* hallucination; “has a citation” ≠ supported | Faithfulness metrics = **sensor**; claim↔span check = SoT-shaped only if structural |
| **C** | Stale index: answer looks fluent but corpus/index drifted | Freshness of non-parametric memory | Fresh wrong docs still wrong; re-index ≠ correctness | Index timestamp / content hash = **sensor**; truth of facts = Stage-0 / human SoT |
| **D** | Citation theater: chunk retrieved near topic but does not support claim | Evidence provenance / support | Dense recall ≠ entailment; line number in dump ≠ claim fingerprint | Stage-0 Finding fingerprints = **SoT**; embedding hit = **sensor** |
| **E** | Bag-of-chunks fails multi-hop / thematic / relational questions | Structured / hierarchical / graph retrieval | Graph edges from LLM extract can invent relations; hierarchy ≠ verification | AST/KG structure = **SoT** if deterministic; LLM graph = **sensor** |
| **F** | Classic RAG is single-shot; agents need iterative tool retrieval | Tool-use retrieval / hierarchical interfaces | Tool loops ≠ merge authority; more tools ≠ more truth | `dispatch_tool` / query kinds = **adapter**; policy/Approve = **SoT** |
| **G** | “Good retrieval” conflated with “good answer” | Separate IR metrics vs answer faithfulness / human grade | LLM-as-judge ≠ boolean merge gate | Recall@k / RAGAS = **sensor**; human Approve = **merge SoT** |

---

## 2. Tool / paper responses by problem class

Stars are GitHub API **2026-08-10** unless noted `[Unknown]`.

### A — Context window / parametric memory failure

**Before.** Facts live only in weights; private Spring repos and yesterday’s commits are invisible; long context still fails when evidence is mid-window (`Lost in the Middle`).

| Artifact | Role | Fit |
| --- | --- | --- |
| [2005.11401](https://arxiv.org/abs/2005.11401) Lewis et al. — **RAG** | Parametric seq2seq + dense Wikipedia index (DPR) as non-parametric memory `[Evidenced]` | **Adopt pattern** (external memory); **Refuse** as citation SoT |
| [2208.03299](https://arxiv.org/abs/2208.03299) **Atlas** | Few-shot RAG LM; retrieval + FiD-style fusion beats sheer params `[Evidenced]` | **Adopt** “retrieval ≫ params for KI tasks”; **Refuse** Atlas stack as product dep |
| [2301.12652](https://arxiv.org/abs/2301.12652) **REPLUG** | Black-box LM + tuneable retriever; no LM cross-attn surgery `[Evidenced]` | **Adopt** black-box + external rank for agent hosts; adapter-shaped |
| [2307.03172](https://arxiv.org/abs/2307.03172) **Lost in the Middle** | Position bias: mid-context underused `[Evidenced]` | **Embody** budgeted packets + structure-first over dumping whole trees |
| GitHub: [facebookresearch/faiss](https://github.com/facebookresearch/faiss) **~40699★** | ANN index for dense vectors | **Adapter** only — similarity ≠ support |
| GitHub: [facebookresearch/DPR](https://github.com/facebookresearch/DPR) **~1869★** | Bi-encoder passage retrieval | **Sensor** / research reference |

**Does not solve.** Private-corpus *correctness*; citation fingerprinting; merge authority.

**DeepWiki — faiss `[Evidenced]` Evaluate/Create:** Evaluate = Index is ANN over dense floats (L2/IP), not a fact ledger. Create = treat Faiss (or any vector store) as a **pluggable sensor backend** behind a port — never as Stage-0 SoR.

---

### B — Hallucination / unsupported claims

**Before.** Model invents fluent answers; naive RAG prepends passages but does not *check* consistency; bad retrieval can *worsen* hallucination (CRAG framing).

| Artifact | Role | Fit |
| --- | --- | --- |
| [2310.11511](https://arxiv.org/abs/2310.11511) **Self-RAG** | On-demand retrieve + reflection/critique tokens; relevance & support critique `[Evidenced]` | **Adopt** on-demand + critique *pattern*; **Refuse** reflection tokens as merge SoT |
| [2401.15884](https://arxiv.org/abs/2401.15884) **CRAG** | Retrieval evaluator → Correct / Incorrect / Ambiguous; web fallback; decompose-recompose `[Evidenced]` | **Adopt** “evaluate retrieval quality before trust”; **Refuse** web scrape as Stage-0 fact |
| [2305.06983](https://arxiv.org/abs/2305.06983) **FLARE** (Active RAG) | Retrieve when next-token confidence drops `[Evidenced]` | **Adopt** confidence-triggered fetch for generative stages; not for Stage-0 |
| GitHub: [AkariAsai/self-rag](https://github.com/AkariAsai/self-rag) **~2415★** | Self-RAG reference impl | Pattern library |
| GitHub: [HuskyInSalt/CRAG](https://github.com/HuskyInSalt/CRAG) **~468★** | Official CRAG code pointer from paper | Pattern library (below 10k★ bar for Embody-dep) |

**Does not solve.** Structural claim↔symbol identity; `[Evidenced — path:line]` citation correctness (this repo’s ast-grep mandate).

**doc-engine map `[Confirmed]`.** Hallucination control for *docs* is Stage-0 findings + claim grammar + human review — not denser RAG.

---

### C — Stale index / freshness vs correctness

**Before.** Non-parametric memory drifts; operators confuse “indexed recently” with “still true.”

| Artifact | Role | Fit |
| --- | --- | --- |
| [2005.11401](https://arxiv.org/abs/2005.11401) RAG + [2208.03299](https://arxiv.org/abs/2208.03299) Atlas | Explicit separation of parametric vs updatable index `[Evidenced]` | Embody *separation*; index rebuild is ops, not truth |
| [2401.15884](https://arxiv.org/abs/2401.15884) CRAG | Static corpus insufficiency → web extension `[Evidenced]` | Shows freshness *pressure*; web ≠ verified Spring fact |
| [2312.10997](https://arxiv.org/abs/2312.10997) RAG survey | Catalogues index freshness as open challenge `[Evidenced]` | Sensor taxonomy |

**Does not solve.** Semantic correctness of a fresh wrong API; content-hash freshness is necessary but not sufficient.

**doc-engine map `[Confirmed]`.** Stage-0 rescan + certification / drift checks are the freshness *and* correctness path for structure facts; vector re-embed is optional sensor refresh only.

---

### D — Citation grounding / evidence provenance (chunk ≠ claim support)

**Before.** Systems show a retrieved chunk as “source” even when the claim is unsupported (or supported elsewhere). Text-search citations land on comments/strings (this repo’s Grep ban exists for that reason).

| Artifact | Role | Fit |
| --- | --- | --- |
| [2310.11511](https://arxiv.org/abs/2310.11511) Self-RAG | Critique tokens for relevance / support `[Evidenced]` | **Sensor** toward support; still LM-judged |
| [2309.15217](https://arxiv.org/abs/2309.15217) **RAGAS** | Faithfulness, context precision/recall, answer relevancy `[Evidenced]` | **Sensor only** — LLM metrics ≠ boolean SoT |
| [2311.09476](https://arxiv.org/abs/2311.09476) **ARES** | Automated RAG eval + PPI; reduces human labels `[Evidenced]` | **Sensor** / experiment harness |
| [2004.12832](https://arxiv.org/abs/2004.12832) **ColBERT** | Late interaction MaxSim — better *rank*, not entailment `[Evidenced]` | Rank **sensor** |
| GitHub: [vibrantlabsai/ragas](https://github.com/vibrantlabsai/ragas) (explodinggradients/ragas) **~15238★** | Eval library | Adopt as *optional* eval harness after Spec; Refuse as CI merge gate |

**Does not solve.** `Finding.fingerprint` / claim-symbol identity; structural ast-grep hits.

**DeepWiki — ragas `[Evidenced]` Evaluate/Create:** Evaluate = closes “vibe check” gap with repeatable LLM metrics (`Faithfulness`, `ContextPrecision`, …). Create = if used, wire as **labeled climb-like sensor** (distinct artifact path, never `coverage.xml` / certification SoR analogy).

**doc-engine map `[Confirmed]`.** Citation SoT = Stage-0 structure facts + claim grammar. Embedding hit near a symbol is **not** claim support.

---

### E — Multi-hop / structured retrieval vs bag-of-chunks

**Before.** Top-k short chunks cannot answer thematic / multi-hop / relational questions (RAPTOR Cinderella example; GraphRAG “connecting the dots”).

| Artifact | Role | Fit |
| --- | --- | --- |
| [2401.18059](https://arxiv.org/abs/2401.18059) **RAPTOR** | Recursive embed → cluster → summarize tree; retrieve at multiple abstractions `[Evidenced]` | **Adopt** hierarchical packet *idea*; **Refuse** LLM summaries as Stage-0 facts |
| [2404.16130](https://arxiv.org/abs/2404.16130) Microsoft **GraphRAG** (local→global) | Entity/relation graph + community summaries; global/local search `[Evidenced]` | **Adopt** global vs local query *strategies*; **Refuse** LLM-extracted edges as SoT |
| [2501.00309](https://arxiv.org/abs/2501.00309) GraphRAG survey | Formalises graph-augmented RAG design space `[Evidenced]` | Cartography |
| [2601.08773](https://arxiv.org/abs/2601.08773) AST-derived vs LLM KG for code | Deterministic AST graphs beat LLM KGs for codebase RAG `[Evidenced]` | **Embody** for this product |
| GitHub: [microsoft/graphrag](https://github.com/microsoft/graphrag) **~35363★** | Production GraphRAG suite | Pattern / Explicit Defer product dep |
| GitHub: [parthsarthi03/raptor](https://github.com/parthsarthi03/raptor) **~1740★** | RAPTOR reference | Pattern library |

**DeepWiki — microsoft/graphrag `[Evidenced]` Evaluate/Create:** Evaluate = baseline vector RAG fails on “connecting the dots” and corpus-holistic questions; GraphRAG answers with Leiden communities + Global/Local/DRIFT search. Create = map Global/Local to **typed query kinds** over Stage-0 facts — do **not** import LLM entity extraction as fact writer.

**Does not solve.** Invented edges; summary drift; using community summary as a citeable “fact.”

---

### F — Agent tool-use retrieval vs classic RAG

**Before.** Single-shot retrieve-then-generate cannot plan multi-step evidence gathering; agents need retrieval as **tools** with budgets and authorization.

| Artifact | Role | Fit |
| --- | --- | --- |
| [2403.14403](https://arxiv.org/abs/2403.14403) **Adaptive-RAG** | Route by question complexity: no retrieve / single / multi-hop `[Evidenced]` | **Adopt** complexity routing for query kinds |
| [2602.03442](https://arxiv.org/abs/2602.03442) **A-RAG** | Hierarchical retrieval interfaces for agentic RAG `[Evidenced]` | **Adopt** granular tools ≫ dump |
| [2605.27123](https://arxiv.org/abs/2605.27123) Logical retrieval beyond embeddings | LLM-driven logical/lexical retrieval ≫ embedding-first `[Evidenced]` | **Embody** structure/logic first for code docs |
| GitHub: [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) **~39333★** | Durable agent graphs + HITL | **Adopt** HITL interrupt *pattern*; **Refuse** as merge SoT |
| GitHub: [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp) **~27142★** | MCP server ergonomics (stderr discipline) | **Adopt** stdio logging discipline |
| GitHub: [openai/openai-agents-python](https://github.com/openai/openai-agents-python) **~28515★** | Tool loop + guardrails | **Adopt** guardrails-outside-model; **Refuse** write tools |

**Does not solve.** Confused-deputy roots; unattended merge; capability-list-as-authorization theater.

**doc-engine map `[Confirmed]`.** Already partial-RAG: typed `query` / `context_packet` + thin MCP `dispatch_tool` library SoR — agent retrieval without vector citation SoT.

---

### G — Evaluation: “good retrieval” vs “good answer”

**Before.** Teams optimize Recall@k or “looks grounded” and ship wrong merge decisions; or use LLM-judge as if it were `fail_under`.

| Artifact | Role | Fit |
| --- | --- | --- |
| [2004.04906](https://arxiv.org/abs/2004.04906) **DPR** | Dense bi-encoder; IR metric culture (top-k) `[Evidenced]` | Retrieval **sensor** metrics |
| [2212.10496](https://arxiv.org/abs/2212.10496) **HyDE** | Hypothetical doc embedding for zero-shot dense retrieval `[Evidenced]` | Query rewrite **sensor**; GitHub [texttron/hyde](https://github.com/texttron/hyde) **~583★** |
| [2004.12832](https://arxiv.org/abs/2004.12832) ColBERT + [stanford-futuredata/ColBERT](https://github.com/stanford-futuredata/ColBERT) **~3910★** | Better ranking sensor | Not answer truth |
| [2309.15217](https://arxiv.org/abs/2309.15217) RAGAS + [2311.09476](https://arxiv.org/abs/2311.09476) ARES | Separate context quality vs faithfulness vs answer relevancy `[Evidenced]` | **Adopt separation**; **Refuse** as merge/cert SoT |
| [2407.01219](https://arxiv.org/abs/2407.01219) Best practices RAG | Practice catalogue `[Evidenced]` | Sensors / engineering checklist |

**Does not solve.** Boolean certification; whole-repo coverage floor analogy — same trap as climb Cover% as 98.7 proof (`[Confirmed]` se-quality synthesis).

**Analogy to embody `[Confirmed]`:**

```text
RETRIEVAL SENSORS                         ANSWER / MERGE SoT
─────────────────                         ──────────────────
Recall@k / nDCG / ColBERT score           Stage-0 claim support
RAGAS Faithfulness / ContextPrecision     Human Approve / Spec
HyDE / Adaptive router confidence         certification verify (boolean)
embedding rank                            Finding.fingerprint
```

---

## 3. Cross-class paper / repo matrix (minimum bar)

| Problem | ≥2 arXiv | ≥1 GitHub (stars 2026-08-10) |
| --- | --- | --- |
| A | 2005.11401, 2208.03299, 2307.03172 | faiss ~40699★ |
| B | 2310.11511, 2401.15884, 2305.06983 | AkariAsai/self-rag ~2415★ |
| C | 2005.11401, 2401.15884, 2312.10997 | (ops on same indexes; faiss as adapter) |
| D | 2310.11511, 2309.15217, 2311.09476 | vibrantlabsai/ragas ~15238★ |
| E | 2401.18059, 2404.16130, 2601.08773 | microsoft/graphrag ~35363★ |
| F | 2403.14403, 2602.03442, 2605.27123 | langgraph ~39333★ / fastmcp ~27142★ |
| G | 2004.04906, 2212.10496, 2309.15217 | ColBERT ~3910★ / ragas ~15238★ |

---

## 4. Embody / Adopt / Refuse for doc-engine

### Embody (already true or must stay true)

1. **Stage-0 structure facts = citation SoT** — not embeddings. `[Confirmed]` + `[Evidenced]` 2601.08773 AST-KG.
2. **Human Approve = merge SoT** — agents/RAG assist only. `[Confirmed]`
3. **Structure-first packets over corpus dumps** — Lost-in-the-Middle + A-RAG interfaces. `[Evidenced]` + `[Confirmed]` query envelopes.
4. **Refuse embedding / chunk neighbor as claim support** — same family as Grep citation ban. `[Confirmed]`
5. **Separate IR sensors from answer/merge predicates** — oracle-vs-climb isomorphism. `[Confirmed]`

### Adopt (patterns only; Spec before tip deps)

| Pattern | Source | Notes |
| --- | --- | --- |
| On-demand / adaptive retrieve | Self-RAG, FLARE, Adaptive-RAG | For generative stages 1–4 — not Stage-0 |
| Hierarchical context budgets | RAPTOR idea | Packet levels ≠ summarized “facts” |
| Global vs local query strategies | GraphRAG search modes | Typed `QueryKind` strategies (OCP) |
| Retrieval quality gate before trust | CRAG evaluator *shape* | Emit sensor labels; fail-closed on Ambiguous for cite paths |
| Faithfulness as labeled sensor | RAGAS | Distinct artifact; never certification SoR |
| HITL interrupt | LangGraph pattern | Operator Path B |
| Logical/lexical before dense | 2605.27123 | Matches ast-grep / symbol query |

### Refuse

| Item | Why |
| --- | --- |
| Vector similarity as citation SoT | Chunk ≠ support; category error |
| LLM-extracted GraphRAG KG as Stage-0 writer | Invented edges; non-deterministic SoT |
| RAGAS / ARES / LLM-judge as merge or `fail_under` analogue | Sensor ≠ boolean SoT |
| Classic bag-of-chunks RAG replacing Stage-0 | Wrong problem class for Spring structure docs |
| Unattended “good answer” auto-merge | Human review floor |
| Pinning LangChain/LlamaIndex/GraphRAG as mandatory runtime | Adapter optional after Spike; ≥10k★ still not citation SoT |

---

## 5. Spec seeds (E-RAG0 — DRAFT, pending Approve)

| ID | Title | Acceptance (decidable) |
| --- | --- | --- |
| RAG0-1 | Lock SoT stack | Written: Stage-0 cite SoT; embed/rank sensor; MCP adapter; human merge SoT |
| RAG0-2 | Sensor artifact path | Any RAGAS/faithfulness/recall run writes a **distinct** path (policy 16-A analogue); never overwrites certification / coverage oracle |
| RAG0-3 | QueryKind OCP | Adaptive/global/local/structure kinds are strategies — no if/elif god |
| RAG0-4 | No vector cite | Claims checker or test: citation paths cannot be satisfied by embedding-only evidence |
| RAG0-5 | HITL floor | MCP surface remains read-only; no write/codegen tools |
| RAG0-6 | Eval separation | Docs state IR metrics ≠ answer grade ≠ merge |

**Exit.** E-RAG0 Approve recorded → optional E-RAG1 (sensor harness / Adaptive routing) one-stream Implement.

**Invariants.** fail_under 98.7; complexipy ≤5; LOC ≤225; no `utils/`; no embedding citation SoT.

---

## 6. Unknowns

| Item | Status |
| --- | --- |
| Whether tip should ever ship an optional dense index behind a port | **Unknown** — Explicit Defer until E-RAG0 + product need |
| Best faithfulness metric that is *not* LLM-judge for structure claims | **Unknown** — prefer structural entailment / claim-symbol join |
| GraphRAG Fast (NLP extract) vs refuse-all LLM graph for Spring | **Unknown** — spike only; AST path preferred |
| DeepWiki pages for Self-RAG / RAPTOR / DPR (not fetched this pass) | **Unknown** — cartography incomplete; GraphRAG / ragas / faiss fetched |
| Interaction with parallel streams E-OAS0 / E-QUERY0 (if present on other tips) | **Unknown** on this base tip — reconcile at merge; do not dual-write Spec |
| REPLUG/Atlas training cost vs black-box host agents we actually run | **Unknown** product measurement |

---

## 7. Adversarial checklist (review packet)

- [ ] Does any sentence treat Recall@k or RAGAS Faithfulness as merge proof?
- [ ] Does any design use embedding hit as `[Evidenced — path:line]` substitute?
- [ ] Is GraphRAG community summary ever citeable as Stage-0 fact?
- [ ] Is “fresh index” confused with “correct fact”?
- [ ] Are agent tool loops granted write/merge authority?
- [ ] Is climb/oracle lesson applied (distinct sensor artifact path)?

If any box fails → **Refuse** the design until fixed.

---
## 8. Sources (primary)

**arXiv (fetched 2026-08-10):** 2005.11401, 2004.04906, 2004.12832, 2208.03299, 2212.10496, 2301.12652, 2305.06983, 2307.03172, 2309.15217, 2310.11511, 2311.09476, 2312.10997, 2401.15884, 2401.18059, 2403.14403, 2404.16130, 2407.01219, 2501.00309, 2601.08773, 2602.03442, 2605.27123.

**GitHub API stars (2026-08-10):** faiss 40699; microsoft/graphrag 35363; vibrantlabsai/ragas 15238; langgraph 39333; fastmcp 27142; openai-agents-python 28515; FlagEmbedding 12034; ColBERT 3910; self-rag 2415; DPR 1869; raptor 1740; texttron/hyde 583; HuskyInSalt/CRAG 468.

**DeepWiki (cartography only):** microsoft/graphrag, explodinggradients/ragas, facebookresearch/faiss — Evaluate/Create notes above. Not Spec SoT.
