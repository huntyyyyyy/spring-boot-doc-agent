---
title: Shallow decisions honesty — freeze, demote, deepen few
status: ACTIVE ALARM
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
audience: [architect, agent, human]
---

# Shallow decisions honesty audit

**User concern (accepted):** too many decisions on thin research; suggestions
worded as “best / Adopt / Chosen”; missing assumptions and gaps.

**Banner:** Port research depth remains **FAIL** (Definition of Ready D0,
Port checklist P3). Volume of Draft artifacts ≠ depth. Prefer **demotion** over
defending prior session output.

Vocabulary scan (this tree, 2026-08-10): **~122** `Adopt`, **~21** `Chosen`,
**~233** `Must`, **~51** `Confirmed` — far more commitment language than paper
digests present (**2** digests under `papers-2026-may-aug/digests/`).

---

## Diagnosis

| Failure mode | What happened | Why it bites |
| --- | --- | --- |
| **Breadth over depth** | Many entities got a Decision Matrix / schema / “verdict” in one day | Agents treat Draft as Accepted |
| **Adopt inflation** | Adjacent GitHub repos labeled **Adopt** for *our* algorithm | Exact engines often **0** (EA-Graph, Proof-or-Stop, STEAD wrap, DynamicMCPBench) |
| **Score theater** | Alternatives tables totaling **12/12 Chosen** | Looks quantitative; still preference without plants / digests |
| **Missing assumptions** | Implicit: local CLI forever; Rust Pilot; Packwerk fidelity enough; MCP host exists; humans will Accept | Not listed as falsifiable assumptions |
| **Suggestion-as-best** | “Recommended topology”, “gold standard” (math brainstorm quoted TLA+) | Heuristic prose smuggled as SoR |

---

## Decision / assertion audit (adversarial)

| Assertion | Where | Research actually present | Honest tier now | Hidden assumption | If agents Implement now |
| --- | --- | --- | --- | --- | --- |
| MCP pin `2026-07-28` | ICD, ADR-0011, matrices | Primary Spec blog + schema.ts `[Evidenced]` | **Adopt wire dialect** (earned) | Hosts speak this revision | Low risk if presentation-only |
| Our five tools + `snapshot_open` semantics | ICD, schemas | STEAD paper constraints; **0** exact product twins | **Pilot invent** | Handles + reject classes sufficient for ST-1…5 | Invented ids / wrong mint |
| FX-MCP TaskSpecs = Accept | plants/ | DynamicMCPBench digest; engine **0** | **Embody shape**; plants = Draft sensors | Tier-1 scorer will exist | False V&V green |
| Packwerk-shaped lock IR | lock-ir schema, matrix | Packwerk docs + ≥5 *adjacent* checkers | **Adopt pattern**; **Pilot** our JSON IR | Constant-edge fidelity enough for Spring | Silent DI / method-call false-green |
| Receipt β/ρ fields | receipt schema, matrix | Proof-or-Stop paper; engine **0** | **Embody** fields; **Pilot** canon | ls-tree exclusions known | Self-invalidating / forgeable digests |
| EA-Graph claim memory Must | STATUS, requirements | 1 digest; **0** public engines | **Pilot invent** (already said — still Must-spine tension) | Synthetic F1 transfers | Wrong withdrawal |
| STEAD ST-1…5 normative | STEAD_CONSTRAINTS | Paper; **0** equivariance library | **Embody** constraints; wrap = Spike | Schema ids ⇒ equivariance | ST-2 false claims |
| Rust owns engine | ADR-0007, brief | Adoption cartography; no Spike measure | **Pilot** language choice | Latency/QAS unknown | Premature lock-in |
| TS owns MCP presentation | ADR-0010 | Ecosystem habit | **Could / Pilot** | Node OK for contributors | Toolchain surprise |
| Decision Matrix 12/12 Chosen | mcp/lock/receipt matrices | Analytical only | Relabel **Working hypothesis** | Scores = truth | Rubber-stamp Accept |
| AHP / TLA+ / JMT catalog | math brainstorm | Explicit brainstorm | **Could Spike** — OK | — | Only bad if promoted Must |
| C4 confidence scores | C4-BRIEF | Sketch numbers | **Sensor** — not Accept | Scores stable | Fake D8 green |
| Monorepo Adopt | ARCHITECTURE_BRIEF | Preference | **Working hypothesis** | Single version line required | Wrong distribution |
| Port CONDITIONAL / Implement NO | STATUS | Honest | **Keep** | — | — |

---

## Missing assumptions (make explicit)

Falsifiable; if false, reopen decisions:

1. **A-LOCAL** — Primary users run a local CLI against a git checkout (not multi-tenant SaaS).  
2. **A-HUMAN-LOCK** — Humans own lock policy and todo bankruptcy; agents must not `update-todo`.  
3. **A-SCIP** — Source Code Index Protocol dumps exist or can be rebuilt for Must languages.  
4. **A-HARNESS** — A non-model harness process can write receipts and reject tool calls.  
5. **A-ACCEPT** — Humans will Accept schemas before Implement (not agents alone).  
6. **A-FIDELITY** — Packwerk-class edges (not full DI/method graph) are *enough* for Wave-1 value.  
7. **A-TRANSFER** — EA-Graph / Proof-or-Stop ideas transfer outside synthetic plants (Unknown).  
8. **A-MCP-HOST** — At least one host will call our tools with `2026-07-28` semantics.  
9. **A-DEPTH** — “Draft schema exists” ≠ “research done” (process assumption — keep FAIL).

---

## Missing gaps (under-named)

| Gap | Why under-named |
| --- | --- |
| G-ASSUME | No living assumption register until this memo |
| G-DEPTH-QUEUE | No cap on parallel research topics → shallow flood |
| G-DIGEST-DEBT | Must papers without digests: Proof-or-Stop 2607.14890, STEAD 2608.03609, Contracts 2607.08028, … |
| G-SCORE | Decision Matrix scores lack Analytic Hierarchy Process *and* lack “depth gate” before Chosen |
| G-IMPL-SEAM | Planned paths (`packages/mcp-server`) asserted without repo layout Accept |
| G-PLANT-EXEC | TaskSpecs without replay world / scorer |
| G-OQ-STALE | Open questions still `blocks_code: true` while schemas proliferate |

---

## FREEZE policy (effective now)

### Freeze (do not expand)

- New Decision Matrices / Architecture Decision Records / “Chosen” vernacular  
- New math Spikes scheduled as Must  
- New language-lane ADRs  
- New Must-spine entities  
- Promoting brainstorm → Adopt  

### Allowed

- **Demote** wording (this pass)  
- **Deepen at most three** topics (below) with paper digests + exact-adopter honesty  
- Fix contradictions when depth proves Draft wrong  
- Human Accept only after deepen  

### Deepen next (max 3) — park everything else

| # | Topic | Why this one | Done when |
| --- | --- | --- | --- |
| 1 | **Receipt freshness β/ρ** | Merge SoR; PoS engine 0; canon Unknown | Digest 2607.14890 + ls-tree canon Spike + tamper plants executable *or* explicit Pilot invent charter |
| 2 | **Claim memory withdrawal** | Must spine; 0 engines; enum under-specified | Digest already exists — finish Pilot charter + evidence lattice schema align + FX-claim plants |
| 3 | **MCP handle lifecycle only** | Schemas exist; semantics Pilot | One host-integration note + snapshot TTL Spike measure; **stop** adding tools |

**Parked (brainstorm / Could only):** AHP, TLA+, Alloy, JMT, Monte Carlo, C4 Accept, Rust/Go/Clojure lane identity, latency **T**, HyperTool, org SaaS MCP.

---

## Required wording demotions

| From (avoid) | To (use) |
| --- | --- |
| **Chosen** (matrices) | **Working hypothesis (Draft)** |
| **Adopt** our tool semantics / IR JSON / STEAD wrap | **Pilot invent** or **Embody constraints** |
| **Adopt** adjacent repo for *exact* algorithm | **Adopt pattern (adjacent)** — exact = 0 if so |
| Artifact-anchored claim memory **Adopt** specification | **Pilot specification** |
| Monorepo **Adopt for product source** | **Working hypothesis after Spec Approve** |
| Score total **12** as decision | Score = **sensor**; Accept = human |
| Plants **landed** implying V&V PASS | **Draft TaskSpecs** — scorer absent |
| Research “in progress closing D0” | **D0 FAIL until digests + exact adopters or Pilot waivers** |

---

## Process correction

1. **One tip writer** for research depth — no parallel “Adopt” floods.  
2. Decision Framework: add gate **research_depth: digest|primary_spec|pilot_waiver** before any Working hypothesis may be proposed for human Accept.  
3. Prefer **Unknown** over polite Adopt.  
4. Session log: if we only added schemas without digests, say **shallow** explicitly.

---

## Bloom (this audit)

| Level | Evidence |
| --- | --- |
| 1 | Vocabulary counts; file pointers |
| 2 | Table mapping assertion → depth |
| 3 | Freeze + deepen-3 applied in STATUS |
| 4 | Demotion table |
| 5 | Adversarial: prior session breadth criticized |
| 6 | This memo + demotions — not more features |

Implement remains **Refuse**. Port export remains **CONDITIONAL**.
