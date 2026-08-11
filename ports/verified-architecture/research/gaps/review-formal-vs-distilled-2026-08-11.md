---
title: Adversarial review — high-integrity formal pivot vs distilled structural pipeline
status: REVIEW — both overclaim; distilled closer; neither is start-of-code
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
audience: [architect, stakeholder, agent]
look_first:
  - research/atam-formal/math-decision-methods-brainstorm-2026-08-10.md
  - research/atam-formal/atam-qas-adr-formal-boundaries-2026-08-10.md
  - research/gaps/shallow-decisions-honesty-2026-08-10.md
  - docs/adr/adr-0004-native-then-wasm-lockcheck.md
  - docs/adr/adr-0005-clojure-graph-brain.md
  - 07-system-design/icd/receipt.schema.json
  - 08-verification/sor-derived-matrix.md
  - STATUS.md
accepted: false
---

# Review: formal “High-Integrity Agent OS” + distilled structural synthesis

Two pitches in one message: (A) category theory + capability microkernel +
SMT/Z3 + ISO/IEC 25010 compliance theater; (B) walk-back to Merkle pointers +
structural find/replace + ast-grep deny-list.

**Verdict:** (A) is mostly **category / compliance laundering** — wrong timing,
wrong evidence bar, fights FREEZE. (B) is **closer to honest engineering** and
overlaps Embody-able pieces already in Spec — still **not** the product MVP as
written, still wrong Clojure “SOT,” still not a crate start.

Neither replaces Definition of Ready, digests, or human Accept.

---

## Part A — Formal / high-integrity pivot

### Category theory as System of Truth

**If** objects/morphisms/functors/colimits are asserted without a decidable
encoding, plants, or a theorem that the product actually checks, **then**
“repository as category C” is vocabulary cosplay — it does not make DeepWiki
sound.

**If** DeepWiki is called a colimit “unique global consensus,” **then** that
claims a universal property the product will not compute. Wiki pages are
**advisory** documents; uniqueness of integration is not free.

Disposition: **Refuse** category-theoretic SOT as Wave-1 foundation. Keep
ordinary typed systems of record (git locks, index, derived registry, claims).

### Capability microkernel (seL4 influence)

**If** seL4’s value is a **tiny formally verified kernel** with a real proof
artifact, **then** naming “C-Space / Cap” on a Tokio Model Context Protocol
server does not inherit that assurance.

**If** Model Context Protocol **2026-07-28** already pushes **handles** as
explicit args (session-free wire), **then** capability tokens for
snapshot/path/symbol are an **Embody** of handle discipline — not a reason to
rebuild seL4.

**If** “each session has a private C-Space,” **then** you reintroduce session
state the wire pin removed unless “session” means “agent turn with minted
handles” carefully.

Disposition: **Embody** unforgeable handles (minted, digest-bound, expired).
**Refuse** seL4-equivalence claims without a Trusted Computing Base proof
milestone that this repo will not fund in FREEZE.

### SMT / Z3 as the Guard

**If** the math brainstorm already parks Temporal Logic of Actions / provers as
**Could, not Must**, **then** “ISEE/NFR-compliant ⇒ Z3 in the write path” is
feature-stacking under a lab coat.

**If** Wave-1 LockCheck is policy Intermediate Representation ↔ graph edges,
**then** full symbolic execution + invariant ∀ views ∄ db calls is a **different
predicate** (and often undecidable / too slow for every edit).

**If** large language models struggle to generate precise formal specs, **then**
“extract symbolic path → formula → Z3” is a research Spike, not a compliance
gate.

Disposition: **Could** Spike (bounded invariants, finite domain). **Refuse** as
MVP spine or ISO proof.

### ISO/IEC 25010 and “HIS / ISEE” mapping table

**If** ISO/IEC 25010 is a **quality characteristic vocabulary**, **then** a
table that maps “Availability → CAP theorem” for a **local single-node tool**
is category error (CAP is for distributed partitions).

**If** “Auditability → Merkle receipts” ignores the existing receipt schema
(β/ρ digests, step ρ, ban model text), **then** inventing Merkle-tree provenance
as the SoR forks the Interface Control Document.

**If** naming ISO characteristics does not produce measurable Quality Attribute
Scenarios with plants, **then** the table is **compliance theater**.

Disposition: **Embody** 25010 as vocabulary for Quality Attribute Scenarios
already Draft. **Refuse** “meet ISO by citing category theory.”

### Verification milestones (TLA+ → TCB → Z3)

**If** FREEZE forbids new Must math Spikes and product crates, **then** four
“verification milestones” as the build plan soft-passes both.

Disposition: **Refuse** as current roadmap. Keep formal methods in the
brainstorm catalog.

---

## Part B — Distilled “Merkle + structural protocol + deny-list”

### Merkle / hash-bound wiki pointers

**If** every wiki/claim concept stores `(content_digest, artifact_id)` and
invalidates on digest drift, **then** that **is** Artifact-Anchored Verification
Memory / claim Fresh — already Must-intent in Spec.

**If** “just a hash-map, no theory required” is the pitch, **then** stop selling
colimits in the same breath — good. Still need disposition enum
(`affected` / `unprovable`), not only “invalidated.”

Disposition: **Embody** hash-bound anchors. Map to existing claim schema — do
not invent parallel “Merkle-Repo” product name as SoR.

### Structural pattern → structural replacement

**If** the model emits line-number edits, **then** drift and rename break
writes. Structural find/replace via ast-grep-class patterns **reduces** that
class of error.

**If** the only protocol is “pattern → replace,” **then** you still lack
LockCheck on architecture edges, receipts with β/ρ, and claim memory — grounding
gap is not solved by better diffs alone.

**If** Groovy / some languages lack structural grammar, **then** “AST is the
only query language” fails closed for those lanes — need explicit fallback
policy.

Disposition: **Embody** structural edit protocol as **Could / Pilot** mutation
API. **Refuse** as the entire product surface.

### Invariant gate = forbidden structural patterns

**If** architecture “never-allow” is encoded as structural patterns over a
proposed tree, **then** you get a fast deny-list — valuable, **heuristic**, not
“90% of formal verification.”

**If** that deny-list is claimed to replace LockCheck Intermediate
Representation + graph, **then** you lose package-layer / DI-edge fidelity the
port already scoped.

Disposition: **Embody** structural deny plants as **one** LockCheck backend or
prefilter. **Refuse** “1% complexity = 90% of Z3” (unmeasured slogan).

### Distinguished architecture (thin Rust + Clojure map + Model Context Protocol)

**If** Rust only runs structural search/replace + SHA-256 + deny-list, **then**
Clojure “state-manager SOT” again becomes the durable brain — contradicts
Architecture Decision Record ADR-0005/0007 (Rust owns oracles; Clojure
read-mostly).

**If** “only state is disk + Clojure hash-map,” **then** the atom/map is a
second System of Truth that dies or drifts unless it is **derived rebuild** from
disk — say that explicitly.

**If** this is labeled the correct shipping architecture for *this* port,
**then** it still skips verify/claim/receipt Interface Control Document tools
and FREEZE deepen rows.

Disposition: **Embody** thin native path: structural ops + hash drift +
**native** policy check. **Refuse** Clojure as SOT owner. Receipts/claims stay
in Rust-derived stores per Spec.

---

## Cross-cutting honesty

| Move | Formal essay (A) | Distilled (B) | Port Spec |
| --- | --- | --- | --- |
| Hash-bound docs/claims | Buried under colimits | Clear | **Embody** → claim schema |
| Structural edits | Ignored | Central | **Could / Pilot** |
| Policy | Z3 proofs | ast-grep deny-list | Native LockCheck IR + optional structural plants |
| Capabilities / handles | seL4 cosplay | Absent | **Embody** MCP handles |
| ISO 25010 | Table theater | Dropped | QAS vocabulary only |
| Start coding now | No | No | FREEZE / Definition of Ready |

**Rhetorical failure:** A sells “Engineer-grade theory”; B says “no theory
required.” Pick one honesty mode. Prefer B’s reduction **as a working
hypothesis for mutation + anchors**, then attach it to existing receipts/claims
— do not oscillate prestige.

---

## Bottom line

**If** the goal is ISO-sounding assurance without plants, **then** Part A
fails closed.

**If** the goal is a shippable deterministic mutation pipeline, **then** Part B
names three real primitives (hash anchors, structural edits, structural
deny-list) — **subset** of stewardship, not the whole verify product.

**Start:** Spec plants for (1) claim invalidation on digest drift, (2)
structural apply with expected hash, (3) forbidden-pattern reject on fixture —
under existing ICD paths. **Do not** open TLA+/Z3/seL4/Cargo from this review.

**Implement:** still **Refuse**.
