---
title: Problem-first landscape — RAG, data science/MLOps, CLI
status: RESEARCH — problem → tool (not tool → hype)
date: '2026-08-10'
epic_seed: E-PROB0
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/research/se-quality-synthesis-2026-08-08.md
- docs/research/quality-backlog.md
- docs/research/process/20-rag-problem-first-retrieval-systems-2026-08-10.md
- docs/research/coverage-quality/42-ds-mlops-problem-first-tooling-2026-08-10.md
- docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
- docs/research/process/38-cli-dx-a11y-dual-sinks-2026-08-10.md
- docs/research/process/39-cli-operator-problem-classes-2026-08-10.md
- docs/design/operator-agent-surface-design-2026-08-10.md
do_not:
- treat embeddings / RAGAS / LLM-judge as citation or merge SoT
- treat climb Cover% / drift dashboards as fail_under 98.7
- treat rich TUI as CI machine SoT
- schedule LangChain/LlamaIndex/GraphRAG as tip runtime without Spec
spec_gate: DRAFT — research only; no Implement from this memo alone
last_reviewed: '2026-08-10'
---

# Problem-first: what RAG, data science, and CLI tools actually solve

**Question.** Catalogs list *tools*. This memo asks: **what failure existed
before the tool class**, what **job** it restores, and what it **does not**
solve. Then map each class to **SoT / sensor / adapter** for `doc-engine`.

**Lattice.** Identity · Honesty labels · Budget/caps · Isolation · Dual sink ·
Human review floor · Fixture ≠ campaign · Derived ≠ LWW · Sensor ≠ SoT.

```text
FAILURE MODE ──► TOOL CLASS CLAIMS TO RESTORE ──► ACTUAL PREDICATE
                      ├─ SoT     (boolean merge / citation / oracle)
                      ├─ Sensor  (advisory rank, drift, climb, judge)
                      └─ Adapter (CLI/MCP/shell boundary)
```

---

## 0. One-page verdict

| Domain | Core problem | Excellent response class | For doc-engine |
| --- | --- | --- | --- |
| **RAG** | Parametric LMs cannot revise private knowledge, lack provenance, invent unsupported claims | Non-parametric memory + retrieve-then-generate; later corrective/reflective/structured indices | **Refuse** embed/rank as citation SoT. **Adopt** typed packets + structure facts. Rank/RAGAS = sensors. Human Approve = merge SoT |
| **DS / MLOps** | Silent bad data, irreproducible runs, leakage theater, dashboard green ≠ decision quality | Contracts (GE/Pandera), lineage (DVC), experiment identity (MLflow), drift (Evidently) | **Embody** contract/oracle pattern. **Adopt** schema-as-code for fixtures. **Refuse** dashboard/judge as 98.7 |
| **CLI** | Opaque exits, matrix hell, help≠behavior, human vs agent consumers collide | Dual-sink CLIs, actionable diagnostics, subcommand frameworks, optional TUI | **Embody** dual sink + actionable stderr. **Adopt** clig.dev / Typer. **Refuse** rich as CI SoT |

**Sibling depth packets:**

| Depth | Path | Epic |
| --- | --- | --- |
| RAG A–G | [`20-rag-…`](20-rag-problem-first-retrieval-systems-2026-08-10.md) | E-RAG0 |
| DS/MLOps | [`coverage-quality/42-ds-mlops-…`](../coverage-quality/42-ds-mlops-problem-first-tooling-2026-08-10.md) | E-DS0 |
| Operator Spec | [`37-OAS…`](37-operator-agent-surface-cli-mcp-rag-2026.md) | E-OAS0 |
| CLI DX / a11y | [`38-…`](38-cli-dx-a11y-dual-sinks-2026-08-10.md) | feeds E-OAS0 |
| CLI problems A–J | [`39-…`](39-cli-operator-problem-classes-2026-08-10.md) | feeds E-OAS0 |
| Design stub | [`docs/design/operator-agent-surface-…`](../../design/operator-agent-surface-design-2026-08-10.md) | E-OAS0 Approve |

---

## 1. RAG — compressed problem → tool map

Lewis et al. `[Evidenced — 2005.11401]`: parametric LMs cannot easily revise
memory, lack insight into predictions, may hallucinate.

| ID | Failure | Response class | Layer |
| --- | --- | --- | --- |
| R1 Parametric memory | Private/current knowledge invisible | RAG hybrid memory | Adapter + sensor |
| R2 Lexical miss | BM25 misses paraphrases | DPR dense dual-encoder `[2004.04906]` | Sensor |
| R3 Query–doc asymmetry | Short query ≠ doc language | HyDE `[2212.10496]` | Sensor |
| R4 Chunk myopia | Flat chunks lose theme / multi-hop | RAPTOR `[2401.18059]`; GraphRAG `[2404.16130]` (~35k★) | Sensor / derived index |
| R5 Bad retrieval poison | Irrelevant context misleads | CRAG `[2401.15884]` | Sensor + control |
| R6 Blind retrieve-always | Noise + budget waste | Self-RAG `[2310.11511]` | Sensor / policy |
| R7 Lost-in-middle | In-window ≠ used | Attention-aware packing `[2307.03172]` | Sensor constraint |
| R8 Eval vacuum | No refs → cannot tell if RAG works | RAGAS `[2309.15217]` | Sensor **only** |

**Refuse:** embedding as citation SoT; RAGAS as merge gate; GraphRAG tip runtime
without Spec; LangChain/LlamaIndex as architecture SoT.

---

## 2. Data science — compressed map

Leakage crisis across fields `[Evidenced — 2207.07048]`.

| ID | Failure | Response class | Layer |
| --- | --- | --- | --- |
| D1 Schema/null drift | Silent pipeline “success” | GX / Pandera contracts | SoT-shaped when boolean |
| D2 Irreproducible data | Same notebook, different answers | DVC lineage | Input identity SoT |
| D3 Experiment chaos | Which run produced the claim? | MLflow tracking | Run identity adapter |
| D4 Drift | Prod silently degrades | Evidently / adv. validation | Sensor |
| D5 Train/serve skew | Feature mismatch | Feast | Defer tip |
| D6 Leakage | Metric theater | Info sheets + isolation | Process SoT |
| D7 Invisible quality | Stakeholders blind | Data Docs dual sink | Dual sink |

**Local Embody:** coverage.xml oracle, claims checker, fixture plants.
**Local sensors:** climb Cover%, gap-average — never floor.

---

## 3. CLI — compressed map

clig.dev: modern CLI is **human-first** yet must stay **automatable**
`[Evidenced]`. Dual-consumer errors (human + agent) are now first-class.

| ID | Failure | Response class | Layer |
| --- | --- | --- | --- |
| C1 Opaque failure | Exit 1, no next step | Actionable diagnostics (Nielsen H9) | Adapter UX |
| C2 Human↔machine collision | Pretty tables break pipes | Dual sink (tty / `--json`) | Adapter |
| C3 Discovery sprawl | Flags undocumented | Cobra/Click/Typer/Clap | Adapter framework |
| C4 Interactive chaos | Ad-hoc curses | Bubble Tea MVU (~44k★) | Optional TUI |
| C5 Matrix hell | OS×shell×PATH | Campaign matrix (not merge SoR) | Process sensor |
| C6 Progress lies | Spinner hides hang | Heartbeats / cancel / honest status | Adapter honesty |
| C7 Config fog | Which flag wins? | Dump-effective-config | Adapter |
| C8 Footguns | Unsafe defaults | Safe defaults / dry-run | Policy |
| C9 Plugin trust | Host-authority extensions | MCP / capability isolation | Isolation |
| C10 Doc drift | help ≠ README ≠ flags | Generated help + claim verify | Claims spirit |

**Why frameworks exist:** they answer C3 (and partly C1/C2) — they are not the
research question. See [`39-…`](39-cli-operator-problem-classes-2026-08-10.md).

---

## 4. Unified problem → predicate map

| Problem class | Boolean SoT | Allowed sensor | Adapter |
| --- | --- | --- | --- |
| Unsupported doc claim | Structure fact + path:line / packet | Embed rank, Self-RAG critique | MCP retrieve |
| Coverage floor | Whole-repo oracle XML fail_under | Climb scoped Cover%, gap | CLI measure modes |
| Data/fixture integrity | Fixture plant + schema/digest | Drift reports | Pipeline hooks |
| Operator failure | Nonzero exit + structured error | Spinners, TUI chrome | doc-engine CLI / CI |
| Certification | Derived view from gates — never LWW | LLM narrative of cert | certification verify |

---

## 5. Adversarial packet

| # | Attack | Response |
| --- | --- | --- |
| A1 | Ship GraphRAG — Microsoft paper | Solves R4 *sensor*; not citation SoT; index cost = budget |
| A2 | RAGAS in CI like coverage | Faithfulness judge ≠ boolean floor |
| A3 | Add MLflow so quality is tracked | Tracking ≠ correct predicate |
| A4 | Bubble Tea for all gates | Solves C4 for humans; breaks C2 for agents/CI |
| A5 | Pandera everywhere | Good for fixtures; ≠ ast-grep citation |
| A6 | Stars prove SoT | Stars = adoption; predicate = constitution |

---

## 6. Epic seed — E-PROB0

| Field | Content |
| --- | --- |
| Goal | Lock problem→SoT/sensor/adapter map before tip Implement |
| PROB0-1 | Spec: publish §4; human Approve | Acceptance: `spec_gate: APPROVED E-PROB0` |
| PROB0-2 | Spike: dual-sink error on one CLI command | JSON + human stderr parity; no rich-as-SoT |
| PROB0-3 | Spike: optional rank sensor behind honesty label | Sensor cannot satisfy citation verify alone |
| Exit | Approve recorded; backlog P18 ordered; no LangChain/GraphRAG tip runtime |
| Invariants | fail_under 98.7; complexipy ≤5; LOC ≤225; no utils/; 16-A; human review floor |

Child Specs: **E-RAG0** · **E-DS0** · **E-OAS0** (see siblings). One tip stream —
do not thrash vs Active E-COH1 without handoff.

---

## 7. Source index (selected)

**RAG.** 2005.11401 · 2004.04906 · 2212.10496 · 2401.18059 · 2404.16130 ·
2401.15884 · 2310.11511 · 2307.03172 · 2309.15217 · graphrag ~35k★ · haystack
~26k★ · chroma ~29k★ · ColBERT ~3.9k★.

**DS.** 2207.07048 · 2311.04179 · 2004.03045 · 2506.16051 · 2404.18673 ·
GX ~12k★ · pandera ~4.3k★ · evidently ~7.8k★ · dvc ~16k★ · mlflow ~27k★ ·
feast ~7.2k★.

**CLI.** clig.dev · dual-consumer errors (2026) · Nielsen H9 · bubbletea ~44k★ ·
cobra ~44k★ · click ~18k★ · typer ~20k★ · clap ~17k★ · gh dual-sink pattern.

**DeepWiki (cartography).** microsoft/graphrag · great_expectations · mlflow ·
bubbletea.

Stars via GitHub API **2026-08-10** (approximate). Research only — Spec →
Implement → Verify → Archive after Approve.
