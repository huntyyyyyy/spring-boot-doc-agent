---
title: Adversarial review — 2035 autopilot horizon vs DE near-term principles
status: REVIEW — horizon Could; near-term schema/receipt/thin-thread Embody with corrections
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
look_first:
  - research/gaps/review-agent-os-mvp-primitives-2026-08-11.md
  - research/gaps/review-formal-vs-distilled-2026-08-11.md
  - research/gaps/stakeholder-discovery-brownfield-mcp-2026-08-11.md
  - 08-verification/sor-derived-matrix.md
  - docs/adr/adr-0001-polyglot-first-product.md
  - STATUS.md
accepted: false
---

# Review: 2028–2035 “Software Autopilot” + DE principles for now

Two layers: (A) paradigm shifts to behavioral digital twin, emergent
invariants, latent/IR synthesis; (B) near-term DE rules — schema-first,
externalized data, receipts, thin thread, dumb kernel / disposable brain.

**Verdict:** (A) is mostly **horizon Could / Unknown** — useful as a refuse
list for what *not* to Build Now, dangerous if used to skip Accept. (B) is the
strongest practical advice in this thread — with three corrections (typed SoR
not one SOT; gate-before-write in the thin thread; disposable intelligence is
the **model/host**, not a Clojure oracle).

Neither unlocks crates under FREEZE / Definition of Ready.

---

## Part A — 2035 paradigm shifts

### Behavioral digital twin

**If** today’s map is structural (index, graph, claims on digests), **then**
adding execution traces is a **new product surface** (observability / profiling
twin) — not a free upgrade of the same System of Record.

**If** the AI “looks at behavioral traces instead of code” to edit Auth under
load, **then** you need privacy, sampling, and false-causal risk (correlation of
latency ≠ permission to rewrite).

**If** the twin is called the system’s “physics,” **then** that overclaims —
traces are sensors, not laws.

Disposition: **Could** Wave-N observability port. **Refuse** as Wave-1 SOT
replacement.

### Emergent governance (IRL → auto spine)

**If** invariants are inferred from “successful commits” vs “bug fixes,”
**then** whatever shipped without crashing can become “correct architecture”
— including debt that merely has not failed yet.

**If** policy System of Record is human-Accepted locks in git, **then**
auto-synthesized spine rules without Accept reopen open question OQ-02 and
stakeholder trust.

**If** the pitch is “removes the human bottleneck,” **then** it fights
brownfield governance (humans own locks; agents propose).

Disposition: **Refuse** auto-minted policy as SoR. **Could** later: *suggest*
candidate deny-patterns for human Accept.

### Latent / direct AST–IR synthesis

**If** text→AST→binary is lossy, **then** operating on CST/IR can reduce
syntax-class errors — research frontier already parked as Could.

**If** “bugs become logical contradictions caught before generation,” **then**
that assumes a complete formal semantics of the business domain — false for
brownfield.

**If** `.rs` files become “mere views,” **then** git blame, review, and
human Accept workflows break unless projection round-trips are perfect.

Disposition: **Unknown / Could**. **Refuse** as current MVP identity.

### Autopilot framing

**If** the product manages “entropy across decades” without human Accept,
**then** it is a different company thesis than local verified architecture +
grounding gap ≈ 0.

Disposition: keep as **vision memo Could**. Do not retitle Spec to Software
Autopilot.

---

## Part B — DE near-term principles

### Interface is the product

**If** tools behind `structural_replace` / verify / claim APIs may be swapped,
**then** versioned Model Context Protocol / JSON Schema contracts are the
durable artifact — matches Interface Control Document-first reviews.

Disposition: **Embody**. Spend design effort on schemas + plants. Still not
“80% schema / 20% code” as a cargo-cult ratio — effort follows Definition of
Ready gaps.

### Data anchor / portable SOT

**If** knowledge must survive brain/language swaps, **then** externalize
**typed** artifacts (SCIP, lock manifests, claim records, receipts) in boring
formats — Embody.

**If** that is labeled one “SOT” folder interchangeable with a “Python brain,”
**then** (1) SoR classes collapse, (2) Python host revival fights Architecture
Decision Record ADR-0001 Refuse.

Disposition: **Embody** portable files. **Refuse** single-SOT slogan and Python
brain swap as earned path.

**Pure function `(SOT, Intent) → (New_SOT, Action)`:** good *shape* if SOT means
**disk snapshots** and New_SOT is written only by the **Rust** derive/receipt
path — not a Clojure atom.

### Symmetry / receipts day one

**If** the Brain only trusts receipts, **then** hash-lock + ICD-shaped receipt
belong in the first **contract**, not the last integration toast — Embody.

**If** “cryptographic” means SHA-256 of file bytes only, **then** keep saying
**content digest + Fresh**, not proof theater.

Disposition: **Embody** receipt-in-v1-contract. Align to `receipt.schema.json`.

### Thin thread

**If** the vertical slice is: hash → structural replace → **gate on candidate**
→ write → receipt → update **derived** anchors, **then** that is a legitimate
Spike shape for the mutation loop.

**If** the slice still writes before gate, or parks receipts, or lets Clojure
own the hash map as truth, **then** it fails prior reviews.

**If** “2 weeks or architecture too complex,” **then** calendar fiction —
Refuse. Complexity is judged by dependency and false-green risk, not a
stopwatch.

Disposition: **Embody** thin thread as **Spec plant sequence**. **Refuse**
week ultimatums and Brain-owned SOT updates.

### Dumb kernel / disposable brain

**If** the kernel is fast, safe, capability-checked execution, **then** Embody
(Rust engine).

**If** “smart disposable logic” means the **large language model + host
planner**, **then** Embody.

**If** it means a long-lived Clojure orchestrator that is “disposable” yet holds
SOT, **then** contradiction — disposable layers must not be the durability
tier.

Disposition: **Dumb Rust yes. Disposable = model/plans. Durable = disk
artifacts + Rust writers.**

---

## Replaceability without predicting 2035

| Horizon idea | What to freeze now | What not to build now |
| --- | --- | --- |
| Twin / traces | Port seam: “TraceObserver” Could | Runtime VM integration |
| Emergent rules | Plant format for *proposed* invariants | Auto-enforce without Accept |
| Latent / IR edit | `structural_replace` contract stable | LLVM thought-compiler |
| Autopilot | Dual surfaces + receipts + claims | Remove human Accept |

**If** schemas are stable and SoR classes typed, **then** future synthesizers
can replace backends — that is the real future-proofing, not digital-twin
mythology today.

---

## Bottom line

**2035 essay:** park as Could vision; do not drive Wave-1.

**DE checklist:** schema-first, external typed artifacts, receipts in the first
contract, thin vertical **plant**, dumb safe executor — **yes**, with the
corrections above.

**Implement:** still **Refuse** until Definition of Ready / FREEZE allow.
