---
title: Four dimensions + Agent OS spitball — adversarial map
status: RESEARCH — Working hypothesis / Could catalog (not Accept; not Implement)
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
audience: [architect, stakeholder, agent]
freeze_class: sensor
look_first:
  - 07-system-design/c4/ARCHITECTURE_VISUALIZATION.md
  - 08-verification/VERIFY_STACK.md
  - 08-verification/sor-derived-matrix.md
  - docs/adr/adr-0004-native-then-wasm-lockcheck.md
  - docs/adr/adr-0005-clojure-graph-brain.md
  - docs/adr/adr-0007-rust-owns-engine.md
  - research/gaps/stakeholder-discovery-brownfield-mcp-2026-08-11.md
  - research/atam-formal/math-decision-methods-brainstorm-2026-08-10.md
accepted: false
---

# Four dimensions + Agent OS spitball (2026-08-11)

Stakeholder spitball: move past a one-way pipeline; add **temporal**,
**resolution**, **dynamic policy**, and **post-write adversarial** loops; keep
science frontiers modular; propose an `/agent-os` monorepo and phased build.

**Banner:** This memo is a **sensor**. It does **not** Authorize crates, reopen
nest 08 (Python), make WebAssembly the Wave-1 spine, or make DeepWiki the policy
System of Record. Definition of Ready still has zero PASS rows.

Whole words — root `GLOSSARY.md`. No calendar-week estimates — sequence by
**dependency**, not slogans.

---

## 1. Engineering truth we keep

A linear “input → analysis → write” diagram under-sells the product. Brownfield
stewardship needs **feedback loops** (freshness, claims, audit) and **more than
two zoom levels**. That pressure is real and compatible with the draft verify
stack — if systems of record stay honest.

---

## 2. Four nuances — Embody / Pilot / Refuse

### 2.1 Temporal — “semantic git archaeology”

| Claim | Adjudication |
| --- | --- |
| Git history is a first-class input for “why,” not only today’s tree | **Embody intent** — brownfield grounding often lives in commits |
| Index commit narratives; link “architectural pivot” commits to wiki | **Pilot invent** — no Wave-1 schema yet; treat as Could corpus |
| Clojure brain owns history as query surface | **Could** as **read** over derived EDN (Architecture Decision Record ADR-0005) — not oracle writer |
| History citations replace guessing | **Embody** into grounding-gap / claim anchors (commit id + path digest) |

**Fail-mode:** treating commit-message prose as a verify witness (same ban as
model text). History is **evidence for answers**; LockCheck still decides
policy.

### 2.2 Resolution — multi-level zoom

| Level (stakeholder) | Port mapping | Verdict |
| --- | --- | --- |
| Global topology | Source Code Index Protocol | **Embody** — already Navigate leg |
| Module skeleton (signatures only) | Missing intermediate projection | **Pilot / Spike** — high value for token efficiency |
| Structural fold (fn + deps, collapse noise) | Adjacent to structural search + index | **Pilot** |
| Atomic raw lines | `read` / receipt plants | **Embody** |

**If** the engine only exposes “whole file or nothing,” **then** context-window
efficiency metrics stay bad. Zoom is a **presentation/query** concern owned by
Rust (or TypeScript presentation calling Rust) — not a reason to put the
orchestrator in Clojure.

### 2.3 Dynamic — “living spine” from DeepWiki → WebAssembly

| Claim | Adjudication |
| --- | --- |
| Architecture rules evolve; 2025 truth can be 2026 anti-pattern | **Embody** — locks/policy must be versioned and reviewable |
| DeepWiki becomes System of Record for the guard | **Refuse** — collapses advisory wiki into policy System of Record (open question OQ-02 class). Policy locks stay **in git** as human-Accepted manifests |
| Clojure generates policy manifest fed to WebAssembly | **Refuse as Wave-1 path** — (1) WebAssembly LockCheck is **Could / Wave-3** (Architecture Decision Record ADR-0004); native Rust LockCheck is Must-intent first; (2) Clojure must not write oracles (Architecture Decision Record ADR-0005 / ADR-0006) |
| Honest dynamic spine | **Working hypothesis:** humans (or harness with Accept) update **git lock Intermediate Representation**; engine reloads; wiki **explains** the rule, does not silently mint it |

### 2.4 Adversarial — post-write shadow audit

| Claim | Adjudication |
| --- | --- |
| Pre-write check is not enough; interactions appear after write | **Embody** — matches post-change claim withdraw / re-verify |
| Shadow agent tries to falsify the change (cycles, new contradictions) | **Pilot invent** — plant shape exists in effect TaskSpecs; no shadow-agent product yet |
| “Challenged and survived” before final | **Embody** into Definition of Done / Verification and Validation — not a second model with free shell |

**Prefer:** deterministic re-LockCheck + claim Fresh + structural contradiction
plants **before** a second large language model persona. A shadow *model* is
Could; a shadow *checker* is Must-intent.

---

## 3. Research frontier vs engineering vessel

Already parked as brainstorm (not Must): Temporal Logic of Actions, Alloy,
Lean/Coq/Verus — see `math-decision-methods-brainstorm-2026-08-10.md`.

| Frontier | Honest tier for this port |
| --- | --- |
| Formal proofs in the loop (Lean / Coq / Temporal Logic of Actions) | **Could** — slow; large language models weak at proof gen; keep modular seam |
| Neuro-symbolic merge (graph inside weights) | **Unknown / out of product** — watch papers; do not block Wave-1 |
| Latent world models / simulate repo before write | **Unknown** — cost; keep interface as “propose → check” |
| Continuous weight adaptation / on-the-fly LoRA | **Refuse for MVP identity** — catastrophic forgetting; product is local tools + external memory, not training loop |

**Modular vessel claim (swap spine later):** **Confirmed as design taste** only if
ports stay stable (LockCheck port, claim store port, receipt port). Swapping a
science module does **not** excuse wrong System of Record today.

---

## 4. Proposed `/agent-os` tree — map, do not Adopt

| Spitball path | Port reality | Verdict |
| --- | --- | --- |
| `/kernel` Rust (protocol, eyes, hands, indexer) | Engine nest + Interface Control Document tools | **Shape OK** as *future* layout after Definition of Ready — not now |
| `/brain` Clojure orchestrates Rust and WebAssembly | ADR-0005 = **query** brain, not orchestrator | **Demote:** orchestrator = Rust harness; Clojure = read-mostly graph ask |
| `/guard` Rust→WebAssembly as a-priori rules | ADR-0004 = native first; WebAssembly Could | **Demote:** `/guard` native in kernel first; wasm build script later |
| `/sot` one folder for index + graph + wiki + receipts | Multiple **classes** of truth (policy vs derived vs advisory) | **Refuse slogan** “single source of truth directory.” Keep **typed** subtrees with writer rules from `sor-derived-matrix.md` |
| Phase-1 = read/write/search Model Context Protocol only | Skips locks/claims/receipts; recreates grounding gap | **Refuse as product MVP path** — filesystem helper is Could, not Phase-1 of *this* product |
| Calendar phase weeks | Autonomous agents must not use day/week estimates | **Refuse** — sequence by dependency instead (below) |

### Dependency sequence (technical, not calendar)

1. **Schemas + plants + human Accept** (Definition of Ready) — still blocking.  
2. **Rust engine:** index consume → registry → native LockCheck → receipts → claims.  
3. **Zoom projections** (skeleton / fold) as query APIs.  
4. **History corpus** (commit narrative index) as retrieve + claim anchors.  
5. **Post-write deterministic audit** plants.  
6. **Clojure** EDN query brain (read).  
7. **WebAssembly** LockCheck guest parity.  
8. **Science seams** only when plants exist.

---

## 5. Feedback-loop picture (replace linear-only thinking)

```text
                    ┌── claim withdraw / Fresh ──────────────────┐
                    ▼                                              │
 intent → index map → zoom → local truth → LockCheck → receipt → write
            │              │                  │                      │
            │              └── token budget ──┘                      │
            │                                                        ▼
            └──────── stale fragment / index lag sensors ◄── post-write audit
                              ▲
                              │
                         git history corpus (why) ──► answers / wiki (advisory)
                              │
                         policy locks in git ◄── human Accept (not wiki auto-mint)
```

Linear pipeline = one happy path. Stewardship = the **back-edges**.

---

## 6. What agents must not do with this memo

- Open `Cargo.toml` / Clojure project / WebAssembly crate under the port.  
- Add DeepWiki → policy compiler as Must.  
- Replace Architecture Decision Record ADR-0007 with “Clojure orchestrator.”  
- Publish week-based roadmaps as commitments.  
- Soft-pass Definition of Ready because the spitball sounds like stewardship.

---

## 7. Bottom line

**Keep:** feedback loops; multi-resolution zoom; git archaeology as *answer*
evidence; post-write **deterministic** audit; modular ports for future science.

**Refuse / demote:** DeepWiki as guard System of Record; WebAssembly as Wave-1
spine; Clojure as orchestrator/oracle; one undifferentiated `/sot` bucket;
Phase-1 = bare read/write/search as the product; calendar-week delivery fiction.

**Still waiting on you:** product-boundary Q1–Q4 (stakeholder discovery memo).
Without that, this stays a richer diagram — not a build plan.
