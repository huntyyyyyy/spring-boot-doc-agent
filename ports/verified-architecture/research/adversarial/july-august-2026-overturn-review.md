---
title: Adversarial review — do July–Aug 2026 papers overturn the architecture brief?
status: RESEARCH COMPLETE
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
window: 2026-07-01 .. 2026-08-10
adversarial: true
related:
  - 07-system-design/ARCHITECTURE_BRIEF.md
  - research/papers-2026-may-aug/README.md
---

# Adversarial review — July/August 2026 vs our suggestions

**Question.** Did research published **July–August 2026** falsify or force rewrite of
the principal architecture brief (local CLI · graph+locks+receipts · SQLite
derived · SCIP consume · SMT/WASM deferred · monorepo-after-Spec)?

**Method.** Pull arXiv with verified `published` timestamps; attack each brief
decision; verdict **HOLD / AMEND / OVERTURN**. LinkedIn/blog star claims without
API check = **Unknown**, not evidence.

---

## 0. One-page verdict

| Brief suggestion | July–Aug pressure | Verdict |
| --- | --- | --- |
| MVP = graph + locks + receipts + Unknown | **EA-Graph** (Aug 4) *strengthens* artifact-anchored claims + unprovable | **AMEND** schema (freshness≠evidence; unprovable) — **not** overturn |
| Deterministic harness; LLM ≠ SoT | **Aria** (Jul 7), **VeriSynth** (Jul 22) — LLM proposes, kernel/SMT decides | **HOLD** (reinforced) |
| Defer SMT/Iris from Java MVP | Aria proves **Iris/Rust lemmas**, not Spring DI; VeriSynth is zkEVM | **HOLD** deferral |
| SQLite derived registry | Codebase-Memory (earlier ’26) also SQLite+TS+MCP; Neo4j wins *agent memory* | **AMEND** split verify-registry vs agent-memory |
| Refuse Kuzu org graph | Graphiti marks **Kuzu deprecated** (ecosystem) | **HOLD** refuse (stronger) |
| SCIP + structural L1 | AOCI (May) hybrid symbolic–semantic; RIG build graphs | **AMEND** L1 “blueprint” ambition — still refuse embeddings-as-SoR |
| Packwerk pattern Adopt | Shopify retrospective + 2026 guides: CI-static, soft enforce, less central | **AMEND** — pattern only; don’t bet on Ruby Packwerk product |
| Spec before codegen; human Approve | TimeArch/MAAD: agents draft architecture; GenAI skips arch layer is the *problem* | **HOLD** Approve gate; **AMEND** allow agent *draft* under harness |
| Formal verify of agent+tools | **STEAD** (Aug 4): FO-CTL verify undecidable; needs equivariance wrapper | **AMEND** MCP/tool design constraint — Phase-2 research |
| Refuse physical RC / Landauer CI | Aug PRC + Jul Landauer papers | **HOLD** locked transfers only |
| Local CLI tool / monorepo-after-Spec | No Jul–Aug paper shows SaaS org-graph Must for this problem | **HOLD** |

**Nothing in the Jul–Aug window OVERTURNS the Must spine.** Several papers
**force schema and phase amendments** we should write down now.

---

## 1. Papers that actually bite (Jul–Aug 2026)

### P-A · EA-Graph — artifact-anchored verification memory  
[arXiv:2608.04278](https://arxiv.org/abs/2608.04278) · published **2026-08-04**

| Claim | Evidence |
| --- | --- |
| Verification claims must anchor to artifact digests | Paper model: ANCH + (evidence, freshness) separated |
| On drift: unaffected \| affected \| **unprovable** — not guess | Explicit; no session fabricated withheld content in study |
| Bounded empirical win for smaller models | Haiku Wilcoxon p=0.0156; Sonnet ceilinged |

**Attack on us:** Our receipt draft lacks freshness vs evidence and “unprovable.”  
**Response:** **AMEND** `receipt-schema-draft` + Unknown taxonomy — add
`unprovable` and independent freshness.  
**Does not say:** replace LockCheck with LLM memory.  
**Does not say:** embeddings become SoR.

### P-B · STEAD — formal verification of agentic systems over operational data  
[arXiv:2608.03609](https://arxiv.org/abs/2608.03609) · published **2026-08-04**

| Claim | Evidence |
| --- | --- |
| Verifying LLM+tools over relational data vs FO-CTL is **undecidable** in general | Theorem in paper |
| Finite-domain + **equivariance** → PSPACE-complete | Sufficient conditions |
| LLM agents can violate equivariance; need canonical deployment wrapper | Construction; GI-hard canonical forms |

**Attack on us:** “Ship MCP tools over SQLite registry and you’re done” is naive once
agents mutate/query operational state under business FO-CTL specs.  
**Response:** **AMEND** Phase-2 constraint: tool interfaces must be designed for
identifier equivariance / canonicalization if we ever claim formal agent
properties. MVP structural LockCheck still valid (different predicate class).  
**Does not overturn:** local graph+lock MVP without FO-CTL claims.

### P-C · Aria — code agents + verification harness  
[arXiv:2607.06341](https://arxiv.org/abs/2607.06341) · published **2026-07-07**

| Claim | Evidence |
| --- | --- |
| Agent + harness; **kernel** is trust anchor | Iris 4257 lemmas; Rust stdlib 217; reglang 318 |
| Fixed human proof strategies underperform free agent+harness | Comparison narrative |

**Attack on us:** “Defer all formal / agent proof” looks timid.  
**Response:** **HOLD** MVP scope — Aria’s oracle is **Coq/Iris**, not Spring DI.
**AMEND** product loop language: *agent proposes edits; LockCheck+receipt harness
accepts* (same shape as Aria’s layers). Pull harness earlier in ACI design docs.

### P-D · VeriSynth — LLM frontend, Z3 arbiter (zkEVM)  
[arXiv:2607.19795](https://arxiv.org/abs/2607.19795) · published **2026-07-22**

LLM synthesizes constraints; SMT decides; >90% bug detection on their bench.  
**Attack:** SMT should be MVP.  
**Response:** **HOLD** deferral — domain is zkEVM opcodes, not bean graphs.
**AMEND** Phase-2 playbook: “LLM proposes lock formulas / Z3 decides” is the
right *pattern* when locks become FOL.

### P-E · Multi-agent RTL repair with Yosys/SBY/Z3  
[arXiv:2607.28877](https://arxiv.org/abs/2607.28877) · published **2026-07-30**

Same propose/decide split; wrong substrate (RTL). **HOLD** MVP; pattern Adopt.

### P-F · Digital→physical RC dynamics matching  
[arXiv:2608.00484](https://arxiv.org/abs/2608.00484) · published **2026-08-01**

Improves soft-robot PRC via dynamics matching.  
**Attack:** physical RC now “co-optimizable” → tip?  
**Response:** **HOLD** refuse hardware. Still strengthens **climb→oracle ≈
reservoir→readout** metaphor only.

### P-G · Quantum vs classical erasure (Landauer)  
[arXiv:2607.27341](https://arxiv.org/abs/2607.27341) · published **2026-07-29**

Finite-resource erasure costs; classical advantages.  
**HOLD** refuse \(kT\ln 2\) as CI floor; remasure-cost language OK.

---

## 2. Near-window / ecosystem attacks (not all Jul–Aug, but used adversarially)

| Source | Attack | Verdict |
| --- | --- | --- |
| **AOCI** [2605.02421] (May) | SCIP-alone under-sells symbolic–semantic blueprints | **AMEND** L1: plan for blueprint entries (symbol+semantics); still not embedding-SoR |
| **Codebase-Memory** [2603.27277] | Tree-sitter → **SQLite** → MCP single binary | **Supports** our local SQLite+MCP shape |
| **RIG** [2601.10112] | Deterministic build/test graph helps agents a lot | **AMEND** optional build-graph port (not MVP Must) |
| **Packwerk 2026 commentary + Shopify retrospective** | Soft CI enforcement; Shopify less central; privacy feature risk | **AMEND** lock IR owned by us; Ruby Packwerk = inspiration |
| **Graphiti / Kuzu deprecation** | Kuzu unmaintained | **HOLD** refuse RE-MASTER Kuzu |
| **Neo4j agent-memory** | Graph memory is productizing hard | **AMEND** split: verify registry ≠ agent conversational memory |
| LinkedIn “Graphify 75k stars” etc. | Unverified marketing | **Unknown** — ignore for SoT |

---

## 3. Decision-by-decision adjudication

### 3.1 Local CLI tool (not org SaaS MVP) — **HOLD**
No Jul–Aug paper shows org-wide social KG as necessary for architectural lock
verify. Neo4j memory papers are about *agent memory*, not merge locks.

### 3.2 Graph + locks + receipts MVP — **HOLD + AMEND**
EA-Graph is the strongest Jul–Aug paper for us: it *needs* artifact identity,
digests, and refuses guessing — isomorphic to Unknown/unprovable. Amend receipt.

### 3.3 SQLite as derived registry — **HOLD + AMEND boundary**
Still right for hermetic verify facts (Codebase-Memory converges). Do **not**
also force agent episodic memory into the same SQLite if Neo4j-class memory is
chosen later — separate ports.

### 3.4 SCIP consume — **HOLD + AMEND ambition**
Still best JVM symbol pipeline with adoption. AOCI argues for richer
symbolic–semantic entries — treat as L1 Should after MVP ingest works.

### 3.5 Defer Z3/Kani/Iris from wave-1 — **HOLD**
Jul papers make agent+formal *exciting* and *pattern-valid*, but oracles are
Coq/SMT on encodings — not DI graphs. Bringing Z3 into MVP without lock FOL
is cosplay.

### 3.6 WASM ≠ proof — **HOLD**
Unchallenged by Jul–Aug formal papers (they use Coq/Z3/Yosys, not “WASM proves”).

### 3.7 Monorepo after Spec — **HOLD**
TimeArch (ECSA 2026 industrial): GenAI skipping architecture is the failure mode.
Supports Spec layer; does not demand microservices.

### 3.8 Human Approve before Implement — **HOLD + AMEND**
MAAD/TimeArch: agents can **draft** RE/architecture; Evaluator/ATAM reports help.
They do **not** replace stakeholder Approve or deterministic DoR. Amend process:
agent-draft allowed; promote-claim + signoff still required.

### 3.9 Science transfers — **HOLD**
Aug PRC / Jul Landauer do not unlock hardware tip SoT.

---

## 4. Required amendments (write into Spec now)

| ID | Change | Target file |
| --- | --- | --- |
| **A1** | Receipt: separate `evidence` vs `freshness`; add `unprovable` disposition | `08-verification/receipts/` |
| **A2** | Unknown taxonomy += UNPROVABLE / STALE_ANCHOR | `06-domain/ubiquitous-language/` + OQ-03 |
| **A3** | ACI loop: explicit “propose → LockCheck harness → receipt” (Aria-shaped) | `07-system-design/ARCHITECTURE_BRIEF.md` patch |
| **A4** | Ports: `VerifyRegistry` ≠ `AgentMemory` (optional Neo4j-class later) | `PORTS.md` |
| **A5** | Phase-2 research spike: STEAD equivariance for MCP tools | `12-delivery/spike-charters/` |
| **A6** | Lock IR owned in-repo; Packwerk = pattern citation only | constraints / ADR-0003 note |
| **A7** | L1 Should: symbolic–semantic blueprint (AOCI-informed) after SCIP MVP | waves README |

---

## 5. What would have OVERTURNED us (counterfactuals)

We would overturn MVP if Jul–Aug showed **with plants**:

1. Embedding-only or LLM-judge matching structural graph+locks on Spring DI
   violation detection with calibrated FP/FN — **not published**.
2. WASM capability config implying Iris/Watt theorems for arbitrary guests —
   **not published**.
3. Org Neo4j/Kuzu as necessary for local lock sync — **contradicted** (git locks;
   Kuzu deprecated).
4. Agent-generated architecture safe to Implement without harness/Approve —
   **TimeArch argues the opposite problem**.

---

## 6. Bloom / claim hygiene

- **Evidenced:** arXiv IDs + `published` timestamps via export API (2026-08-10).
- **Confirmed:** aligns with prior locked transfers + RAG≠verify constitution.
- **Unknown:** whether EA-Graph’s synthetic worlds transfer to Spring plants;
  whether STEAD wrappers are practical for our MCP surface — needs Spike.

**Implement still Refuse** until DoR; this memo only amends Spec.
