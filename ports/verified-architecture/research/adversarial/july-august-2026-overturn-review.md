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
the principal architecture brief (local command-line interface · graph+locks+receipts · SQLite
derived · Source Code Index Protocol consume · SMT/WebAssembly deferred · monorepo-after-Spec)?

**Method.** Pull arXiv with verified `published` timestamps; attack each brief
decision; verdict **HOLD / AMEND / OVERTURN**. LinkedIn/blog star claims without
API check = **Unknown**, not evidence.

---

## 0. One-page verdict

| Brief suggestion | July–Aug pressure | Verdict |
| --- | --- | --- |
| minimum viable product = graph + locks + receipts + Unknown | **EA-Graph** (Aug 4) *strengthens* artifact-anchored claims + unprovable | **AMEND** schema (freshness≠evidence; unprovable) — **not** overturn |
| Deterministic harness; large language model ≠ Source of Truth | **Aria** (Jul 7), **VeriSynth** (Jul 22) — large language model proposes, kernel/SMT decides | **HOLD** (reinforced) |
| Defer SMT/Iris from Java minimum viable product | Aria proves **Iris/Rust lemmas**, not Spring Dependency Injection; VeriSynth is zkEVM | **HOLD** deferral |
| SQLite derived registry | Codebase-Memory (earlier ’26) also SQLite+TS+Model Context Protocol; Neo4j wins *agent memory* | **AMEND** split verify-registry vs agent-memory |
| Refuse Kuzu org graph | Graphiti marks **Kuzu deprecated** (ecosystem) | **HOLD** refuse (stronger) |
| Source Code Index Protocol + structural L1 | AOCI (May) hybrid symbolic–semantic; RIG build graphs | **AMEND** L1 “blueprint” ambition — still refuse embeddings-as-System of Record |
| Packwerk pattern Adopt | Shopify retrospective + 2026 guides: CI-static, soft enforce, less central | **AMEND** — pattern only; don’t bet on Ruby Packwerk product |
| Spec before codegen; human Approve | TimeArch/MAAD: agents draft architecture; GenAI skips arch layer is the *problem* | **HOLD** Approve gate; **AMEND** allow agent *draft* under harness |
| Formal verify of agent+tools | **Stateful Tool-Enabled Agentic Deployment** (Aug 4): FO-CTL verify undecidable; needs equivariance wrapper | **AMEND** Model Context Protocol/tool design constraint — Phase-2 research |
| Refuse physical RC / Landauer CI | Aug PRC + Jul Landauer papers | **HOLD** locked transfers only |
| Local command-line interface tool / monorepo-after-Spec | No Jul–Aug paper shows SaaS org-graph Must for this problem | **HOLD** |

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
**Does not say:** replace LockCheck with large language model memory.  
**Does not say:** embeddings become System of Record.

### P-B · Stateful Tool-Enabled Agentic Deployment — formal verification of agentic systems over operational data  
[arXiv:2608.03609](https://arxiv.org/abs/2608.03609) · published **2026-08-04**

| Claim | Evidence |
| --- | --- |
| Verifying large language model+tools over relational data vs FO-CTL is **undecidable** in general | Theorem in paper |
| Finite-domain + **equivariance** → PSPACE-complete | Sufficient conditions |
| large language model agents can violate equivariance; need canonical deployment wrapper | Construction; GI-hard canonical forms |

**Attack on us:** “Ship Model Context Protocol tools over SQLite registry and you’re done” is naive once
agents mutate/query operational state under business FO-CTL specs.  
**Response:** **AMEND** Phase-2 constraint: tool interfaces must be designed for
identifier equivariance / canonicalization if we ever claim formal agent
properties. minimum viable product structural LockCheck still valid (different predicate class).  
**Does not overturn:** local graph+lock minimum viable product without FO-CTL claims.

### P-C · Aria — code agents + verification harness  
[arXiv:2607.06341](https://arxiv.org/abs/2607.06341) · published **2026-07-07**

| Claim | Evidence |
| --- | --- |
| Agent + harness; **kernel** is trust anchor | Iris 4257 lemmas; Rust stdlib 217; reglang 318 |
| Fixed human proof strategies underperform free agent+harness | Comparison narrative |

**Attack on us:** “Defer all formal / agent proof” looks timid.  
**Response:** **HOLD** minimum viable product scope — Aria’s oracle is **Coq/Iris**, not Spring Dependency Injection.
**AMEND** product loop language: *agent proposes edits; LockCheck+receipt harness
accepts* (same shape as Aria’s layers). Pull harness earlier in ACI design docs.

### P-D · VeriSynth — large language model frontend, Z3 arbiter (zkEVM)  
[arXiv:2607.19795](https://arxiv.org/abs/2607.19795) · published **2026-07-22**

large language model synthesizes constraints; SMT decides; >90% bug detection on their bench.  
**Attack:** SMT should be minimum viable product.  
**Response:** **HOLD** deferral — domain is zkEVM opcodes, not bean graphs.
**AMEND** Phase-2 playbook: “large language model proposes lock formulas / Z3 decides” is the
right *pattern* when locks become FOL.

### P-E · Multi-agent RTL repair with Yosys/SBY/Z3  
[arXiv:2607.28877](https://arxiv.org/abs/2607.28877) · published **2026-07-30**

Same propose/decide split; wrong substrate (RTL). **HOLD** minimum viable product; pattern Adopt.

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
| **AOCI** [2605.02421] (May) | Source Code Index Protocol-alone under-sells symbolic–semantic blueprints | **AMEND** L1: plan for blueprint entries (symbol+semantics); still not embedding-System of Record |
| **Codebase-Memory** [2603.27277] | Tree-sitter → **SQLite** → Model Context Protocol single binary | **Supports** our local SQLite+Model Context Protocol shape |
| **RIG** [2601.10112] | Deterministic build/test graph helps agents a lot | **AMEND** optional build-graph port (not minimum viable product Must) |
| **Packwerk 2026 commentary + Shopify retrospective** | Soft CI enforcement; Shopify less central; privacy feature risk | **AMEND** lock IR owned by us; Ruby Packwerk = inspiration |
| **Graphiti / Kuzu deprecation** | Kuzu unmaintained | **HOLD** refuse RE-MASTER Kuzu |
| **Neo4j agent-memory** | Graph memory is productizing hard | **AMEND** split: verify registry ≠ agent conversational memory |
| LinkedIn “Graphify 75k stars” etc. | Unverified marketing | **Unknown** — ignore for Source of Truth |

---

## 3. Decision-by-decision adjudication

### 3.1 Local command-line interface tool (not org SaaS minimum viable product) — **HOLD**
No Jul–Aug paper shows org-wide social KG as necessary for architectural lock
verify. Neo4j memory papers are about *agent memory*, not merge locks.

### 3.2 Graph + locks + receipts minimum viable product — **HOLD + AMEND**
EA-Graph is the strongest Jul–Aug paper for us: it *needs* artifact identity,
digests, and refuses guessing — isomorphic to Unknown/unprovable. Amend receipt.

### 3.3 SQLite as derived registry — **HOLD + AMEND boundary**
Still right for hermetic verify facts (Codebase-Memory converges). Do **not**
also force agent episodic memory into the same SQLite if Neo4j-class memory is
chosen later — separate ports.

### 3.4 Source Code Index Protocol consume — **HOLD + AMEND ambition**
Still best JVM symbol pipeline with adoption. AOCI argues for richer
symbolic–semantic entries — treat as L1 Should after minimum viable product ingest works.

### 3.5 Defer Z3/Kani/Iris from wave-1 — **HOLD**
Jul papers make agent+formal *exciting* and *pattern-valid*, but oracles are
Coq/SMT on encodings — not Dependency Injection graphs. Bringing Z3 into minimum viable product without lock FOL
is cosplay.

### 3.6 WebAssembly ≠ proof — **HOLD**
Unchallenged by Jul–Aug formal papers (they use Coq/Z3/Yosys, not “WebAssembly proves”).

### 3.7 Monorepo after Spec — **HOLD**
TimeArch (ECSA 2026 industrial): GenAI skipping architecture is the failure mode.
Supports Spec layer; does not demand microservices.

### 3.8 Human Approve before Implement — **HOLD + AMEND**
MAAD/TimeArch: agents can **draft** RE/architecture; Evaluator/Architecture Tradeoff Analysis Method reports help.
They do **not** replace stakeholder Approve or deterministic Definition of Ready. Amend process:
agent-draft allowed; promote-claim + signoff still required.

### 3.9 Science transfers — **HOLD**
Aug PRC / Jul Landauer do not unlock hardware tip Source of Truth.

---

## 4. Required amendments (write into Spec now)

| ID | Change | Target file |
| --- | --- | --- |
| **A1** | Receipt: separate `evidence` vs `freshness`; add `unprovable` disposition | `08-verification/receipts/` |
| **A2** | Unknown taxonomy += UNPROVABLE / STALE_ANCHOR | `06-domain/ubiquitous-language/` + open question OQ-03 |
| **A3** | ACI loop: explicit “propose → LockCheck harness → receipt” (Aria-shaped) | `07-system-design/ARCHITECTURE_BRIEF.md` patch |
| **A4** | Ports: `VerifyRegistry` ≠ `AgentMemory` (optional Neo4j-class later) | `PORTS.md` |
| **A5** | Phase-2 research spike: Stateful Tool-Enabled Agentic Deployment equivariance for Model Context Protocol tools | `12-delivery/spike-charters/` |
| **A6** | Lock IR owned in-repo; Packwerk = pattern citation only | constraints / Architecture Decision Record ADR-0003 note |
| **A7** | L1 Should: symbolic–semantic blueprint (AOCI-informed) after Source Code Index Protocol minimum viable product | waves README |

---

## 5. What would have OVERTURNED us (counterfactuals)

We would overturn minimum viable product if Jul–Aug showed **with plants**:

1. Embedding-only or large language model-judge matching structural graph+locks on Spring Dependency Injection
   violation detection with calibrated FP/FN — **not published**.
2. WebAssembly capability config implying Iris/Watt theorems for arbitrary guests —
   **not published**.
3. Org Neo4j/Kuzu as necessary for local lock sync — **contradicted** (git locks;
   Kuzu deprecated).
4. Agent-generated architecture safe to Implement without harness/Approve —
   **TimeArch argues the opposite problem**.

---

## 6. Bloom / claim hygiene

- **Evidenced:** arXiv IDs + `published` timestamps via export API (2026-08-10).
- **Confirmed:** aligns with prior locked transfers + Retrieval-Augmented Generation≠verify constitution.
- **Unknown:** whether EA-Graph’s synthetic worlds transfer to Spring plants;
  whether Stateful Tool-Enabled Agentic Deployment wrappers are practical for our Model Context Protocol surface — needs Spike.

**Implement still Refuse** until Definition of Ready; this memo only amends Spec.
