---
title: Cold product BC research map — beyond E-OAS0 (2026-08-10)
status: ACTIVE portfolio — Spec seeds DRAFT; no Implement without per-epic Approve
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine + Stage-0 + thin MCP + certification
related:
  - docs/research/quality-backlog.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
  - docs/research/process/15-legacy-remediation-spec-gate-2026.md
do_not:
  - implement from this map without a named Spec Approve
  - add more process/ Specs for product BCs (process/ already overcrowded)
  - unattended AI merge / embedding citation SoT / rich CI SoT
  - invent universal OS/terminal emulator as merge SoT
human_review_floor: true
---

# Cold product BC research map (portfolio)

**Question.** Tip energy has concentrated on local CI / stalker / vacuity / OCS
plant / E-OAS0. Which **product bounded contexts** are cold (little post-import
churn), under-Spec’d, and need principal research for better logic/frameworks —
**with human review as floor**, not full AI adoption?

**Method.** Backlog DRAFT/Deferred inventory + post-import git churn
(`[Confirmed]` history root `e5bc0175`) + archive memos as historical pointers +
external SoR (arXiv / SLSA / code-KG MCP patterns) with tiers.

---

## 0. One-page verdict

| Stance | Choice |
| --- | --- |
| **Embody** | Stage-0 signals + typed `query`/`context_packet` as agent retrieval SoR; `certification.json` as **derived** view (never LWW); human Spec/operator review floor |
| **Adopt** | Finite campaign OS×shell matrix (E-OAS16); SLSA-*shaped honesty for cert predicates (pattern, not full SLSA product); structure-first KG/index patterns for **facts next phase** Spec |
| **Refuse** | Embedding as citation SoT; Spec Kit WorkflowEngine runtime; OTel tip SoT; rich CI SoT; unattended AI merge; phone/device-farm as CLI SoT; boiling all cold BCs in one tip |

**Ordered research thrusts (Spec-before-code):**

1. **E-QUERY0** — query/packet BC + MCP isolation contracts  
2. **E-CERT0** — certification fold honesty under phase runner  
3. **E-FACT0** — fact-store next phase (promote archive → `stage0/` Spec)  
4. **E-CQLJ0** — CodeQL backend + OpenAPI/facts join (fixture↔OCS)  
5. **E-TOOL4 slice** — drift + capacity plant-honesty Spec (before more façades)

E-OAS0 remains parallel Spec (operator surface); do **not** Implement OAS/QUERY/CERT
in parallel tip thrash — one active Implement stream after Approves.

---

## 1. Why “cold” matters here

| Hot (post-import) `[Confirmed]` | Cold (≈0 product touches) `[Confirmed]` |
| --- | --- |
| `scripts/ci`, `doc_engine/ci` stalker/vacuity/adequacy | `src/doc_engine/query/`, `adapters/mcp/` |
| OCS plant / grading / OAS docs | `scanning/facts*`, `_scanner_codeql*`, `support/_codeql_*` |
| COH1 façade pokes | `pipeline/certification_fold.py`, `compliance*`, `tools/certification.py` |
| | `tools/spring_drift_*`, `tools/capacity_preflight*` |
| | `src/stf/` (P12 last), most of `local_runner_phases/` |

`docs/research/process/` is **crowded** (~21 memos). New Spec seeds for product
BCs go under **`stage0/`** or **`modularity/`**, not another process ordinal.

---

## 2. Backlog open set (compressed)

Standing DRAFTs already Spec-shaped but parked: E-TACH0, E-SOL0, E-GND0 (demoted),
E-RT0, E-RUST0, E-CPL0, E-AST0, **E-OAS0**.  

P12.2 still orders Implement: **E-TOOL4 → E-PIPE1 → E-QUERY1 → E-STF1** — this
map supplies the **missing Spec precursors** (QUERY0, CERT0/PIPE0, FACT0, CQLJ0).

---

## 3. Thrust deep-dives

### 3.1 E-QUERY0 — Query / packet / MCP BC

**Paths:** `src/doc_engine/query/` (`packet.py`, `providers.py`, `rank.py`,
handlers), `adapters/mcp/server.py`, `query/mcp_tools.py`.  

**Archive:** `docs/research/archive/claude-lore/research/query-seam-audit-e4-2026-08-07.md`,
S-STF-E MCP isolation ADR.

**Question.** What is the fail-closed contract for packet vs full-signal reads,
token budgets, and MCP tool surface **before** OAS/GND Implement?

| Stance | Detail |
| --- | --- |
| Embody | Library `dispatch_tool` SoR; server-derived root; stderr-only on stdio MCP `[Evidenced]` FastMCP doctrine |
| Adopt | Structure-first retrieval (callers/dependents/packet) like code-index / sciogen **patterns** — not their DBs as deps `[Evidenced]` |
| Refuse | MCP write/codegen; caller-supplied root; treating packet as Cover% proof |

**External:** RepoDoc / code-KG MCP tools show agents prefer typed graph lookups
over raw dumps `[Evidenced]` arXiv 2604.26523 + GH patterns — aligns with Embody
partial RAG already in synthesis.

**Spec seed:** `docs/research/stage0/query-packet-bc-research-2026-08-10.md`  
**Human floor:** tool results are evidence for human/agent review — not merge authority.

---

### 3.2 E-CERT0 — Certification fold under phase runner

**Paths:** `pipeline/certification_fold.py`, `compliance*`, `tools/certification.py`,
`local_runner_phases/certification_finish.py`.  

**SoT:** `docs/design/ddia-north-star/deviations/dev-certification-derived-view.md`
(B2.5 — derived, never LWW).

**Question.** After local_runner phase splits, is fold still a pure derived view
with honest `generative_executor` / mock labeling?

| Stance | Detail |
| --- | --- |
| Embody | Recompute-from-SoR; refuse hand-edit certification `[Confirmed]` deviation |
| Adopt | Attestation **honesty patterns** from SLSA provenance (builder id, parameters, subjects) as **predicate fields** — not full SLSA product dep `[Evidenced]` slsa.dev |
| Refuse | Dual-writer / LWW merge; vacuous `certified: true` without gate facts; LLM-judge as cert |

**Spec seed:** `docs/research/modularity/certification-fold-phase-runner-2026-08-10.md`  
**External packet (D2):** `docs/research/stage0/d2-d3-certification-fact-stores-bc-research-2026-08-10.md`  
**Unblocks:** E-PIPE1 size cuts without breaking trust.

---

### 3.3 E-FACT0 — Fact-store next phase

**Paths:** `scanning/facts*.py` (+ consumers in query).  

**Archive:** `fact-store-phase1-decision-memo`, `fact-store-approaches-collation`,
`fact-store-prior-art-corpus` (2026-07-30); claim-symbol identity ADR.

**Question.** Forever-sidecar vs next identity / MAPS_TO / query consumers —
Explicit Embody/Adopt/Refuse for phase 2.

| Stance | Detail |
| --- | --- |
| Embody | Deterministic Stage-0 extraction as fact SoR; dual-emit without silent drop |
| Adopt | Incremental re-index / typed edges patterns from structure-first KGs `[Evidenced]` — **Spike** before picking store |
| Refuse | Vector embeddings as citation SoT; replacing ast-grep/CodeQL plant with LLM KG |

**Promote** archive → active `stage0/` Spec before any FACT1 Implement.  
**External packet (D3):** `docs/research/stage0/d2-d3-certification-fact-stores-bc-research-2026-08-10.md`

---

### 3.4 E-CQLJ0 — CodeQL backend + OpenAPI/facts join

**Paths:** `_scanner_codeql.py`, `support/_codeql_*`, `spring-signals/.../OpenApiSurface.ql`,
operator P33.5 join_openapi evidence.

**Related hot:** CI CodeQL fingerprint skip (`ci/17`) — **semantics cold**.

**Question.** One projection model fixture↔OCS; how OpenAPI rows join facts/query
without a second assertion engine (OCS2).

| Stance | Detail |
| --- | --- |
| Embody | Same assertion engine; fixture = merge SoR; OCS = campaign `[Confirmed]` E-OCS0 |
| Adopt | Explicit join contracts (CSV↔YAML↔facts) with human-reviewed floors |
| Refuse | Artifactory DB as CI SoT; soft-green Messaging/OpenAPI |

**External packet (D4):** `docs/research/stage0/d4-d5-d6-static-join-drift-cli-2026-08-10.md`

---

### 3.5 E-TOOL4 slice — Drift + capacity honesty

**Paths:** `tools/spring_drift_*`, `tools/capacity_preflight*`.  

**Question.** Tier oracles and Stage-4 proxies still honest under dual plant?

| Stance | Detail |
| --- | --- |
| Embody | Characterization plants before threshold rewrite |
| Adopt | Documented proxy honesty labels (sensor vs SoT) |
| Refuse | Capacity numbers as Cover% proof |

**External packet (D5 + brief D6):** same
`docs/research/stage0/d4-d5-d6-static-join-drift-cli-2026-08-10.md`
(operator CLI deep Spec remains E-OAS0 / `process/37`).

---

### 3.6 Deferred cold (after 1–5)

| Area | Note |
| --- | --- |
| `src/stf/` | E-STF1 last in P12; Spec after QUERY/PIPE/CERT |
| `semantic_eval*` | Sensor only — never generative quality SoT |
| `adapters/github`, `adapters/cursor` | Thin ingest; low leverage vs Stage-0 |
| Kitchen P9.2 | Optional spike only |

---

## 4. Cross-cutting invariants (all thrusts)

1. **Human review floor** — Spec Approve + operator review; MCP assists `[Confirmed]` OAS15  
2. fail_under 98.7 · complexipy ≤5 · LOC ≤225 · no utils  
3. One tip Implement stream  
4. No embedding citation SoT · no OTel tip SoT · no rich CI SoT  
5. Campaign shell matrix ≠ Cover% SoR (OAS16)

---

## 5. Suggested Spec order (fresh-chat)

```text
Approve E-OAS0 (operator surface)     — optional parallel docs-only
Approve E-QUERY0                      — unlocks QUERY1 + safe MCP growth
Approve E-CERT0                       — unlocks PIPE1 without trust rot
Approve E-FACT0                       — unlocks query consumers
Approve E-CQLJ0                       — unlocks OCS join honesty
Then TOOL4 / PIPE1 / QUERY1 per P12.2
```

**Do not** schedule E-RUST0 / enterprise RAG / Spec Kit runtime / Harn as product.

---

## 6. Adversarial checklist

- [ ] Is this map an excuse to skip E-OAS0 human-review floor? → No; OAS15 stands.  
- [ ] Does “code KG” smuggle vector citation? → FACT0/QUERY0 Refuse.  
- [ ] Does SLSA Adopt become mandatory signing product? → Pattern-only unless new Spec.  
- [ ] Does cold-map create parallel tip thrash? → One Implement after Approves.  
- [ ] process/ sprawl? → Seeds live in stage0/modularity.

---

## 7. Exit

This portfolio is **research SoR for prioritization**. Each thrust needs its own
design Spec Approve before code. Linked seeds:

- [`stage0/query-packet-bc-research-2026-08-10.md`](stage0/query-packet-bc-research-2026-08-10.md)
- [`modularity/certification-fold-phase-runner-2026-08-10.md`](modularity/certification-fold-phase-runner-2026-08-10.md)
- [`stage0/d4-d5-d6-static-join-drift-cli-2026-08-10.md`](stage0/d4-d5-d6-static-join-drift-cli-2026-08-10.md) (E-CQLJ0 / E-TOOL4 / OAS16)
