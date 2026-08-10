---
title: Mathematical & formal methods for architecture choices — BRAINSTORM catalog
status: BRAINSTORM — ideas only; NOT Definition of Ready Must; NOT Implement Ready
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
audience: [architect, product, engineer, agent]
related:
  - research/atam-formal/atam-qas-adr-formal-boundaries-2026-08-10.md
  - docs/standards/decision-framework.md
  - 07-system-design/decisions/
github_snapshot: '2026-08-10'
---

# Mathematical decision methods — brainstorming catalog

> **Banner.** This is a **brainstorming / selection taxonomy** of mathematical and
> deterministic approaches that *could* harden architectural choices later.
> Nothing here is a Wave-1 Must, nothing unlocks Implement, and nothing replaces
> plants, human Accept, or the coverage oracle. Treat rows as **ideas to score**,
> not commitments.

Parent method memo (Architecture Tradeoff Analysis Method, Quality Attribute
Scenarios, TLA+ Pilot hint, Verus boundaries):
`atam-qas-adr-formal-boundaries-2026-08-10.md`.

Analytical six-vector Decision Framework (already in use for Model Context
Protocol / locks / receipts): `docs/standards/decision-framework.md`.

---

## Why this catalog exists

“Best practices” are heuristics. When we want less bias in **what / when / how /
who / where / why**, we can reach for:

| Goal | Math class | Example tools |
| --- | --- | --- |
| Logic & concurrency | Formal specification / model checking | TLA+, Alloy |
| Absolute correctness | Interactive theorem proving | Coq (Rocq), Isabelle, Lean, Verus |
| Throughput & latency prediction | Queueing networks / stochastic models | Java Modelling Tools, Monte Carlo |
| Comparative trade-offs | Multi-Criteria Decision Analysis / Analytic Hierarchy Process | AHPy, pyAHP, Expert Choice |
| Risk under uncertainty | Stochastic simulation | NumPy/SciPy Monte Carlo |

These **complement** (do not replace) Decision Matrices, Architecture Decision
Records, and six-part Quality Attribute Scenarios.

---

## Cross-cutting verdict (brainstorm tiers)

| Approach | Product tier (idea) | Exact public tools ≥5? | Fit to local verify CLI |
| --- | --- | --- | --- |
| **Analytic Hierarchy Process / Multi-Criteria Decision Analysis** | **Could → Pilot** on Decision Matrix weights | Libraries exist (AHPy, pyAHP, …); commercial Expert Choice | Best near-term *math* upgrade to our six-vector scores |
| **TLA+ / TLC** | **Pilot** (tiny protocols only) | Yes (`tlaplus/tlaplus` ★~3k, Examples ★~1.5k, Apalache ★~0.6k) `[Evidenced — GitHub 2026-08-10]` | Watch→reindex→verify freshness; MCP handle lifecycle |
| **Alloy** | **Could** | Yes (`AlloyTools/org.alloytools.alloy` ★~0.9k) | Lock Intermediate Representation / claim–anchor relational contradictions |
| **Verus / Lean (code-adjacent)** | **Could / later Pilot** | Yes (Verus ★~2.8k, Lean4 ★~8.7k) | Tiny pure LockCheck / digest core — not whole product |
| **Coq / Isabelle** | **Refuse tip**; **Embody** literature trust only | Yes (Coq/Rocq ★~5.5k) | Already: RustBelt/WasmCert as *language* trust — not our crates proved |
| **Java Modelling Tools (queueing)** | **Could Spike** for latency Quality Attribute Scenarios | Official site live; GitHub mirrors weak/sparse | Predict bottlenecks before Spike plants fill **T** |
| **MATLAB / Simulink** | **Refuse** product path | Commercial | Wrong domain (signal/hardware dynamics) |
| **Monte Carlo (NumPy/SciPy)** | **Could** | Yes (NumPy/SciPy) | Risk ranges on index rebuild time / Spike latency — sensor only |

---

## 1. Formal verification (proving design logic)

### 1.1 Temporal Logic of Actions (TLA+)

| Slot | Content |
| --- | --- |
| **(a) Math** | Temporal logic over actions; exhaustive (bounded) state exploration via TLC / symbolic via Apalache |
| **(b) Our fit** | Protocol properties: “no verify Accept on stale `material_digest`”; snapshot handle expiry; propose/decide never inverted |
| **(c) Adopters** | `tlaplus/tlaplus`, `tlaplus/Examples`, `informalsystems/apalache` (+ industry use Amazon/Microsoft lore — treat as Confirmed practice, not our proof) |
| **(d) Agent bite** | Agents paste huge PlusCal for Spring Dependency Injection → state explosion; claim “proved architecture” for UI code |
| **(e) Tier** | **Pilot** Spike: ≤1 tiny model for freshness/handle protocol; **Refuse** “TLA+ for whole engine” |

### 1.2 Alloy

| Slot | Content |
| --- | --- |
| **(a) Math** | Relational first-order logic + SAT; structural instances / counterexamples |
| **(b) Our fit** | Lock Intermediate Representation: package deps acyclic; claim anchors leaf-complete; todo fingerprint uniqueness |
| **(c) Adopters** | `AlloyTools/org.alloytools.alloy` (+ teaching corpora) |
| **(d) Agent bite** | Model file-level anchors only → misses EA-Graph leaf span; declare “schema proved” without plants |
| **(e) Tier** | **Could** Spike after `lock-ir.schema.json` Accept |

### 1.3 Coq / Isabelle / Lean / Verus

| Slot | Content |
| --- | --- |
| **(a) Math** | Machine-checked proofs (type theory / HOL / SMT-assisted) |
| **(b) Our fit** | Literature trust for Rust/WASM boundaries already recorded in ATAM formal memo; optional Verus on pure digest/ρ(E) helpers |
| **(c) Adopters** | `coq/coq`, Lean4, `verus-lang/verus`, WasmCert family |
| **(d) Agent bite** | Label WASM box “proved” because Wasmtime exists (explicitly forbidden in ATAM memo) |
| **(e) Tier** | **Embody** language results; **Refuse** tip “whole product in Coq”; **Could** Verus on fingernail-sized pure functions |

---

## 2. Performance & queueing (predicting scale)

### 2.1 Java Modelling Tools (queueing networks)

| Slot | Content |
| --- | --- |
| **(a) Math** | Queueing network theory → predicted residence time / utilization |
| **(b) Our fit** | Latency Quality Attribute Scenarios N-01/N-02: separate index-rebuild vs warm-resolve queues before inventing **T** |
| **(c) Adopters** | Primary: [jmt.sourceforge.net](https://jmt.sourceforge.net/) `[Evidenced — HTTP 200]`; GitHub ports sparse (anti-bogus: do not pretend ★ mirrors = engine) |
| **(d) Agent bite** | Treat model output as measured Accept; skip plant p95 |
| **(e) Tier** | **Could** Spike (sensor for Design talk only); plants remain SoR for thresholds |

### 2.2 MATLAB / Simulink

| Slot | Content |
| --- | --- |
| **(e) Tier** | **Refuse** for this product (hardware/signal dynamics ≠ local verify CLI) |

### 2.3 Monte Carlo (NumPy/SciPy)

| Slot | Content |
| --- | --- |
| **(a) Math** | Sample uncertain inputs → distribution of outcomes |
| **(b) Our fit** | Risk on index rebuild wall-clock, dirty-tree probability, Spike latency ranges |
| **(c) Adopters** | NumPy/SciPy (exact libs); Crystal Ball = commercial adjacent |
| **(d) Agent bite** | Fake tight distributions; replace Tier-1 effect plants with “p(success)=0.99” |
| **(e) Tier** | **Could** as Decision Matrix / Spike appendix — never merge SoR |

---

## 3. Decision analysis (comparing options)

### 3.1 Analytic Hierarchy Process / Multi-Criteria Decision Analysis

| Slot | Content |
| --- | --- |
| **(a) Math** | Pairwise comparisons → eigenvector weights; consistency ratio |
| **(b) Our fit** | **Natural upgrade** to six-vector Decision Matrices: turn 0–2 scores into weighted MCDA without inventing a second schema |
| **(c) Adopters** | `PhilipGriffith/AHPy` ★~153, `pyAHP/pyAHP` ★~168 (maintenance uneven — Pilot lib choice carefully); Expert Choice commercial |
| **(d) Agent bite** | Rig pairwise matrices to pre-chosen option; skip Rejected alternatives column |
| **(e) Tier** | **Could → Pilot** Spike: optional AHP worksheet beside MCP/lock/receipt matrices |

### 3.2 How this sits with Decision Framework + Architecture Tradeoff Analysis Method

```text
Quality Attribute Scenario (stimulus → measure)
        │
        ▼
Decision Matrix six vectors (Why…Where) + usage cases + loci
        │  optional math layer (brainstorm)
        ├─ AHP weights on vectors          ← comparative trade-offs
        ├─ TLA+/Alloy on chosen protocol   ← logic & structure
        ├─ JMT / Monte Carlo on latency    ← prediction sensors
        ▼
Architecture Decision Record (engineering record)
        │
        ▼
Plants / Tier-1 effects / human Accept     ← still boolean SoR
```

AHP does **not** replace Why/What/Who/How/When/Where — it only **quantifies
preference weights** among vectors or alternatives already listed.

---

## Problem → method → tool → Spike trigger

| If we want to test… | Mathematical approach | Candidate tool | Open a Spike when… |
| --- | --- | --- | --- |
| Logic & concurrency of freshness / handles | Formal specification | TLA+ / TLC (Apalache Could) | MCP `snapshot_open` + receipt β/ρ Accepted as Draft |
| Schema / relationship contradictions | Structural modeling | Alloy | Lock Intermediate Representation human-Accepted |
| Absolute correctness of a tiny pure function | Theorem proving / SMT | Verus (not whole Coq tip) | After engine Pilot exists; LOC-bounded target named |
| Throughput & latency prediction | Queueing theory | Java Modelling Tools | Before locking latency **T** into Design; always dual-run plants |
| Comparative trade-offs | Multi-Criteria Decision Analysis / Analytic Hierarchy Process | AHPy or spreadsheet | Third Decision Matrix onwards (reduce scoring bias) |
| Risk & uncertainty | Stochastic modeling | NumPy Monte Carlo | Cost/time ranges for index rebuild Spike |
| Hardware/signal dynamics | Differential equations | MATLAB/Simulink | **Never** (Refuse) |

---

## Agent-codegen / rubber-stamp bites (global)

1. Declaring Architecture Decision Records “mathematically proved” without machine-checked artifacts in-tree.  
2. Using AHP weights to soft-pass Definition of Ready.  
3. Replacing Quality Attribute Scenario plants with JMT charts.  
4. Expanding TLA+ models until TLC cannot finish, then claiming “no bugs found.”  
5. Treating Expert Choice / MATLAB licenses as required contributor toolchain.

---

## Explicit Refuse (even as brainstorm ends)

These methods must **not** be treated as replacements for:

- Executable plants (FX-MCP-*, lock illegal-edge, receipt tamper)  
- Whole-repo coverage oracle / `fail_under`  
- Human Accept on Definition of Ready rows  
- Proof-or-Stop / claim-memory semantics invented from paper titles  
- “Best practice” blog posts re-labeled as formal proofs  

---

## Spec Spike tickets only (Bloom Create — not Implement)

| ID | Spike | Exit |
| --- | --- | --- |
| SPIKE-MATH-AHP | Optional Analytic Hierarchy Process worksheet template next to Decision Framework | One worked MCP or lock matrix with consistency ratio documented |
| SPIKE-MATH-TLA-FRESH | Tiny TLA+ model: stale material ⇒ verify refuse | TLC finds injected bug; model ≤ few hundred states guidance |
| SPIKE-MATH-ALLOY-LOCK | Alloy sigs for package deps + todo fingerprint | Counterexample for cycle / duplicate fingerprint |
| SPIKE-MATH-JMT-LAT | Optional queueing sketch for index vs resolve | Explicitly labeled **sensor**; does not set Quality Attribute Scenario **T** |

---

## Bloom

| Level | Evidence |
| --- | --- |
| 1 | Tool IDs + GitHub/star snapshot 2026-08-10; JMT site; ATAM formal memo |
| 2 | Mapped onto receipts, locks, MCP handles, latency Quality Attribute Scenarios |
| 3 | Spike charters only (above) |
| 4 | Embody/Adopt/Pilot/Could/Refuse table |
| 5 | Refuse list + agent bites |
| 6 | This catalog + Spike IDs — **Implement Refuse** |

---

## Review

Re-score this brainstorm after: first engine Pilot; latency Spike exit; or any proposal to make formal methods Definition of Ready Must.
