---
title: Adversarial review — Agent OS MVP (Merkle-SOT / structural replace / invariant gate)
status: REVIEW — three primitives mostly right; transition order wrong; still no crates
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
look_first:
  - research/gaps/review-formal-vs-distilled-2026-08-11.md
  - research/gaps/review-cybernetic-loop-framing-2026-08-11.md
  - 07-system-design/icd/receipt.schema.json
  - docs/adr/adr-0005-clojure-graph-brain.md
  - docs/adr/adr-0007-rust-owns-engine.md
  - STATUS.md
accepted: false
---

# Review: stripped “symmetric” Agent OS MVP

Pitch: Distinguished-Engineer framing — Content-Addressable Store, Deterministic
State Transition; three primitives (Merkle-SOT, Structural-Query,
Invariant-Gate); Rust kernel + Clojure brain + `/sot` disk; sample code.

**Verdict:** Naming the three primitives is the strongest version of this
thread so far. The sample **state transition is unsafe** (writes before the
gate). “Content-addressable” and “symmetric” overclaim. Clojure-as-SOT and
`/sot` mega-folder remain Refuse. Not a crate start under FREEZE.

---

## Critical entailment — transition order

**If** `structural_replace` calls `fs::write` *inside* the function, and
`verify_spine` runs only on the `Ok(new_code)` path *after* that write,
**then** a `SPINE_VIOLATION` response means the disk **already changed** and
was not rolled back.

**If** a deterministic state transition means “illegal states are unreachable,”
**then** this machine reaches an illegal on-disk state whenever the gate fails
after write.

Disposition: **Refuse** this control flow as MVP. Correct order:

1. drift check (expected hash)  
2. compute candidate bytes in memory (structural replace **without** write)  
3. invariant / LockCheck on candidate (+ graph if required)  
4. atomic replace / write  
5. ICD-shaped receipt (or rollback on post-hash mismatch)

That is the real “Deterministic State Transition.” The slogan does not create it.

---

## Primitive naming vs Spec

### Merkle-SOT / content-addressable

**If** concepts store path + structural anchor + content hash and advance hash
only on success, **then** that is **hash-linked claim / anchor** discipline —
Embody toward existing claim schema.

**If** a Content-Addressable Store means blobs keyed **by** hash (git objects),
**then** an atom keyed by `:user-auth` with a hash *field* is not a CAS — it is
a mutable symbol table with digests. Wrong name.

**If** `/sot` holds EDN + hashes + SCIP as one “Single Source of Truth,”
**then** policy / index / derived / advisory classes collapse again.

Disposition: **Embody** hash-bound anchors. **Refuse** CAS branding and
undifferentiated `/sot`.

### Structural-Query / replace

**If** the protocol is anchor → replacement instead of line numbers, **then**
Embody as Pilot mutation API.

**If** the Kernel holds a `tree_sitter::Parser` but `structural_replace` uses
`str::contains` / `str::replace`, **then** the precision primitive is **not
implemented** — the parser is dead weight and substring replace can hit the
wrong occurrence.

Disposition: **Refuse** “AST-based” claims until the plant uses a real node
match (and defines multi-match failure).

### Invariant-Gate

**If** governance is a structural never-allow on the **candidate** before
commit, **then** Embody as one LockCheck backend / prefilter.

**If** the check is `view_layer` ∧ `Database::connect` string contains,
**then** it is still heuristic theater (and runs too late in this sample).

Disposition: **Embody** gate-before-write. **Refuse** this predicate as
architecture LockCheck.

---

## Topology claims

**If** Architecture Decision Record ADR-0007 says Rust owns oracle writes,
**then** Clojure `defonce sot` + `swap!` on success makes the Brain the durable
transition ledger in process memory — wrong owner and non-durable across crash
unless rebuilt from disk.

**If** the architecture is “symmetric,” **then** Brain generating commands and
Kernel executing them is **asymmetric by design** (orchestrator vs executor) —
and that orchestration belongs in the agent/host + Rust harness, not a second
SOT brain.

Disposition: **Refuse** Clojure SOT. Optional Clojure = query over Rust EDN
export.

### Receipt

**If** success returns only `pre_hash` / `post_hash` / `op`, **then** it still
is not `receipt.schema.json` (head / material / policy / command_set / steps ρ).

Disposition: **Embody** “receipt after successful transition.” **Refuse** this
struct as SoR.

### Language hardcoding

**If** `set_language(tree_sitter_rust::language())` is fixed, **then** brownfield
multi-language ambition is contradicted on line one of the “MVP.”

---

## What to keep (Spec form only)

| Primitive | Keep as | Next Spec artifact |
| --- | --- | --- |
| Hash drift before mutate | Yes | apply / atomic_update contract + plant |
| Structural anchor replace | Yes (real AST) | mutation API Draft + multi-match fail |
| Invariant before commit | Yes | native LockCheck order + fixture plant |
| Receipt after success | Yes | existing ICD schema, not toy struct |

Do **not** create `/agent-os/kernel` in the port tree now.

---

## Bottom line

**If** a Distinguished Engineer implements deterministic transitions, **then**
they do not write first and validate second.

**If** they implement content addressing, **then** they do not rename a feature
atom “CAS.”

**If** these three primitives are the MVP, **then** they map onto **existing**
claim Fresh + structural mutation Pilot + LockCheck — under Definition of Ready
— not a new monorepo with Clojure owning truth.

**Implement:** still **Refuse**. Fix the transition order on paper before any
crate.
