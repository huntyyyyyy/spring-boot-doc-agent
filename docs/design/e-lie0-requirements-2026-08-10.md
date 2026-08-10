---
title: E-LIE0 Requirements — StRS · SRS (MoSCoW) · NFR · RTM
status: DRAFT — RE package (RE-1…3); Design Spec blocked until Approve + ADV-1…3
date: '2026-08-10'
epic: E-LIE0
category: design
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
spec_gate: docs/research/process/50-local-first-verified-architecture-agent-2026-08-10.md
related:
  - docs/research/process/50-local-first-verified-architecture-agent-2026-08-10.md
  - docs/research/process/51-e-lie0-adversarial-ddia-solid-polyglot-slate-2026-08-10.md
  - docs/design/ddia-north-star/domains/01-data-flow-and-truth/concepts/system-of-record-vs-derived.md
  - docs/research/quality-backlog.md
  - .cursor/rules/se-quality-constitution.mdc
do_not:
  - Treat architecture tours (ghost/LSP/Z3) as Must without MoSCoW re-prioritize
  - Bind REQ IDs to Rust/WASM/LanceDB — those are design choices
  - Dual-write coverage.xml or claims from a second kernel
  - Approve Design Spec without every Must REQ having an RTM Accept method
sources:
  web:
    - https://www.iso.org/standard/72089.html
  github:
    - https://github.com/sourcegraph/scip-java
    - https://github.com/Shopify/packwerk
  deepwiki_ask:
    - sourcegraph/scip-java · Spring DI / incomplete compile limits
  mcp: https://mcp.deepwiki.com/mcp
last_reviewed: '2026-08-10'
---

# E-LIE0 Requirements Engineering Package

**Purpose.** IEEE 29148-shaped **StRS + SRS + NFR + RTM** for the local-first
verified architecture agent epic. Architecture vision lives in
[`process/50`](../research/process/50-local-first-verified-architecture-agent-2026-08-10.md);
adversarial gaps in
[`process/51`](../research/process/51-e-lie0-adversarial-ddia-solid-polyglot-slate-2026-08-10.md).
This file is the **requirements SoR** for E-LIE0: Design cites `REQ-*` only;
no new capability without a REQ.

**Method.** Stakeholder need → capability (implementation-free) → MoSCoW →
Accept method. Tool names (Rust, WASM, SCIP, Z3) appear only under
*design notes* or *constraints*, never as the requirement text.

---

## 0. Bloom (Create = this package)

| Level | Evidence |
| --- | --- |
| **1** | ISO/IEC/IEEE 29148 shape; scip-java / Packwerk primary |
| **2** | Needs restated in Stage-0 / locks / coverage / Unknown types |
| **3** | Accept methods map to kitchen/OCS / `pre_pr` / claims witnesses |
| **4** | MoSCoW separates v1 graph+locks from ghost/LSP/SMT |
| **5** | Validation vs verification; false-green controls in RTM |
| **6** | `REQ-*` + RTM + change control — Design may proceed after ADV-1…3 |

---

## 1. StRS — Stakeholder requirements (RE-1)

### 1.1 Actors

| ID | Actor | Role |
| --- | --- | --- |
| **A-OP** | Agent operator | Runs doc-engine / IDE agent against a Spring repo |
| **A-ARCH** | Architect | Authors layer / package locks once for humans + AI |
| **A-DEV** | Developer (manual) | Edits Java without the agent; expects same policy |
| **A-CI** | CI / tip writer | Merge gates; single coverage + claims SoR |
| **A-OWN** | Target-repo owner | Pays index/build cost; prefers Unknown over wrong |

### 1.2 Mission need (problem statement)

Operators and architects need **answers about Spring wiring and architecture
policy** that are **traceable to index + locks**, not chat invention — without
replacing this repo’s merge floors (`coverage.xml`, claims) or inventing a
second truth writer.

**Measurable intent (v1):** when an injection or layer edge is queried or
checked, the system returns a **resolved edge or explicit Unknown**, with a
**proof-tour receipt** listing witness IDs; ambiguous DI never silently picks.

### 1.3 Goals / constraints / OpsCon

| Kind | Statement |
| --- | --- |
| **G1** | Virtual Spring/dep graph + lock checks usable on kitchen/OCS-scale trees |
| **G2** | Same lock policy for agent and human paths (eventual LSP = same checks) |
| **G3** | Explainable verify: every “allowed/denied” cites lock + graph witnesses |
| **C1** | Python tip remains sole `coverage.xml` / claims writer until cutover Approve |
| **C2** | Static model ≠ full JVM; conditional/AOP/SpEL → Unknown or out-of-scope |
| **C3** | Index blobs are local-derived; git SoR for locks only |
| **Ops** | Index rebuild is a local/CI job; stale index fails strict verify |

### 1.4 Out of scope (StRS Won’t for this epic wave)

- Replacing Stage-0 ast-grep as the tip firehose without separate Approve  
- Full JVM fidelity (runtime `@Conditional`, AOP proxies, SpEL) as “proved”  
- Chat/RAG embeddings as authority for wiring facts  
- Mesh / Backstage / remote multi-tenant index SaaS  
- In-tree Rust tip kernel cutover without profiled hotspot + Approve  

---

## 2. SRS — Functional requirements (RE-2)

Quality bar: singular, verifiable, **implementation-free**. MoSCoW applies to
**v1 product wave** (graph + locks + receipts).

### 2.1 Must (v1)

| ID | Requirement | Actor |
| --- | --- | --- |
| **REQ-F-01** | The system shall expose a query: given an injection site (or type request), return the bound implementation symbol **or** `Unknown` with a reason code. | A-OP |
| **REQ-F-02** | When more than one candidate satisfies stereotypes/qualifiers under the static model, the system shall **not** select a winner; it shall return `Unknown`. | A-OP, A-OWN |
| **REQ-F-03** | The system shall build a virtual dependency graph from resolved injection edges (and declared package/layer edges from locks). | A-OP, A-ARCH |
| **REQ-F-04** | The system shall detect cycles in the virtual dependency graph and report offending edge sets. | A-ARCH, A-CI |
| **REQ-F-05** | The system shall evaluate architecture locks (allowed caller→callee packages/layers) and report violations with lock IDs. | A-ARCH, A-DEV, A-CI |
| **REQ-F-06** | Every verify/deny result shall emit a proof-tour receipt listing ordered witness IDs (lock, edge, and/or symbol locations). Missing required IDs ⇒ fail. | A-OP, A-CI |
| **REQ-F-07** | Ambiguous or incomplete index/state shall be classified in a closed failure taxonomy: at least `unknown`, `ambiguous`, `stale`, `conflict`. | A-OWN, A-CI |
| **REQ-F-08** | Locks shall be versioned text under git; changing locks shall not require distributing index blobs. | A-ARCH |
| **REQ-F-09** | Merge SoR for this monorepo (`coverage.xml`, claims predicates) shall remain a single writer path; LIE verify shall not dual-write those artifacts. | A-CI |

### 2.2 Should (near-term after Must green)

| ID | Requirement | Actor |
| --- | --- | --- |
| **REQ-F-10** | The system should refuse verify when index content digest does not match the declared source revision (stale-index gate). | A-CI |
| **REQ-F-11** | Lock packages should support Packwerk-like dependency direction and public API folders as executable checks (not prose-only MDC). | A-ARCH |
| **REQ-F-12** | Human editors should receive the same lock violations as the agent path (red-squiggle / diagnostics). | A-DEV |
| **REQ-F-13** | Proof-tour receipts should be renderable as clickable steps (path + symbol + lock). | A-OP |

### 2.3 Could (later waves)

| ID | Requirement | Actor |
| --- | --- | --- |
| **REQ-F-14** | The system could prefetch symbol/lock facts for predicted edit regions (ghost) without treating embeddings as SoR. | A-OP |
| **REQ-F-15** | The system could answer cross-language “what breaks?” via a declared bridge SoR (e.g. OpenAPI) or dual indexes. | A-OP |
| **REQ-F-16** | The system could sandbox untrusted lock-check plugins under a capability-limited guest. | A-CI |

### 2.4 Won’t (this epic unless MoSCoW reopened)

| ID | Requirement (explicit non-goal) |
| --- | --- |
| **REQ-F-17** | Shall **not** claim mathematical proof of Spring bean wiring via SMT in v1. |
| **REQ-F-18** | Shall **not** treat vector/RAG recall as proof of a bean binding. |
| **REQ-F-19** | Shall **not** require a second language runtime as tip merge SoT. |

---

## 3. NFR (RE-2 continued)

| ID | MoSCoW | Requirement |
| --- | --- | --- |
| **REQ-N-01** | Must | Resolve or Unknown for a single injection site on kitchen fixtures completes within a documented budget (default target ≤2s local warm cache; spike measures Confirmed). |
| **REQ-N-02** | Must | Lock check of one changed file’s outbound edges completes within a documented budget (default target ≤500ms warm). |
| **REQ-N-03** | Must | Unknown rate and reason codes are observable (metric or receipt field) for CI dashboards. |
| **REQ-N-04** | Should | Index rebuild cost for OCS-scale trees is bounded and documented; owners can opt strict vs advisory stale. |
| **REQ-N-05** | Must | Privacy: ghost/prefetch caches do not exfiltrate source; local-first default. |
| **REQ-N-06** | Must | Determinism: same inputs (sources digest + locks version) ⇒ same resolve/lock outcomes. |
| **REQ-N-07** | Should | LSP diagnostic latency feels interactive (budget TBD after REQ-F-12 Spike). |

---

## 4. Validation vs verification

| Activity | Question | Owner method |
| --- | --- | --- |
| **Validation** | Are we locking the *right* architecture intents? | Architect review of lock IR + OpsCon; kitchen demos of intended deny/allow |
| **Verification** | Does this change violate declared locks / graph rules? | Automated LockCheck + cycle gate + receipt schema tests |

“Proof tour” is a **verification witness UX**, not validation that locks match
business intent. RE-4 change control covers lock intent drift.

---

## 5. RTM — Need → REQ → design port → Accept (RE-3)

| Need / goal | REQ | Design port (ADV/LIE0) | Accept method |
| --- | --- | --- | --- |
| No hallucinated beans | F-01, F-02, F-07 | `WiringResolver` + Unknown taxonomy (ADV-3) | Fixture: multi-impl → Unknown; single → impl id |
| Graph for cycles/layers | F-03, F-04 | Registry + graph builder (LIE0-3/4) | Kitchen cycle fixture fails gate |
| Shared policy AI+human | F-05, F-08, F-12 | `LockCheck` + lock IR (ADV-4); LSP Spike | Same violation ID from CLI and editor Spike |
| Explainable deny | F-06, F-13 | Receipt schema (ADV-6 / LIE0-5) | Schema reject if step IDs missing |
| Stale / conflict honesty | F-07, F-10 | Index freshness (ADV-1 SoR matrix) | Mismatch digest → stale fail under strict |
| No dual Cover% | F-09, F-19 | Constitution; ACI boundary | Claims/oracle path unchanged in Pilot |
| Package locks | F-11 | Packwerk-inspired IR (ADV-4) | controller→repo demo red |
| Latency budgets | N-01, N-02, N-07 | Chain budget (ADV-5) | Spike numbers recorded Confirmed |
| Privacy / local | N-05 | Prefetch design (later) | No network in default Pilot path |
| Sandbox Could | F-16 | WASM LockCheck (LIE0-6) | Parity suite native vs guest |
| SMT Won’t v1 | F-17 | Defer L3 | Spec text + MoSCoW Won’t |
| RAG not SoR | F-18 | Ghost labeled derived | Adversarial test: embedding ≠ witness |

Every **Must** row has an Accept method. Design Spec shall not invent Must
capabilities outside this table without amending this file (RE-4).

---

## 6. Change control (RE-4)

| Event | Action |
| --- | --- |
| New capability desired | Add/amend `REQ-*` here; bump `last_reviewed`; update RTM |
| Lock schema change | Bump lock `schema_version`; invalidate proof tours older than version; migration note in Design |
| MoSCoW re-prioritize | Explicit row edit (Should→Must only with Accept method ready) |
| Design-only choice (Rust vs Py) | **No** new REQ; record under Design `approved_decisions` |
| Conflict with constitution | Constitution wins; REQ amended or epic Refuse |

---

## 7. Status / gate

| Ticket | State |
| --- | --- |
| **RE-1** StRS | **Drafted** in this file §1 |
| **RE-2** SRS + NFR | **Drafted** §2–3 |
| **RE-3** RTM | **Drafted** §5 |
| **RE-4** change control | **Drafted** §6 |
| Human **Approve** RE package | **Open** |
| ADV-1…3 (SoR / ports / DI envelope) | Still required before Design Spec Approve |
| Implement (Cargo / tip kernel) | **Blocked** |

---

## 8. Design notes (non-requirements)

Optional Pilot tech (not REQ text): scip-java index, tree-sitter summaries,
Python ACI today, Rust resolve later, wasmtime sandbox, Babashka graph REPL,
Cobra watch daemon. See process/50–51.
