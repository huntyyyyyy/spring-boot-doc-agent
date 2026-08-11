---
title: Adversarial review — three-track MVP / interface-first parallelization
status: REVIEW — research-depth FAIL remains; Implement Refuse
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
audience: [architect, stakeholder, agent]
look_first:
  - STATUS.md
  - 00-governance/dor-dod/DEFINITION_OF_READY.md
  - docs/adr/adr-0004-native-then-wasm-lockcheck.md
  - docs/adr/adr-0005-clojure-graph-brain.md
  - docs/adr/adr-0007-rust-owns-engine.md
  - 08-verification/sor-derived-matrix.md
  - research/gaps/stakeholder-discovery-brownfield-mcp-2026-08-11.md
  - research/gaps/four-dimensions-agent-os-spitball-2026-08-11.md
accepted: false
---

# Review: three-track MVP roadmap (interface-first + mocks)

Proposal under review: decouple infrastructure from logic; freeze JSON/EDN
contracts; run Rust/WebAssembly, Clojure, and “SOT/data” tracks in parallel;
ship a “thin thread” (Model Context Protocol shell → structural search → write)
in calendar weeks; integrate mocks later.

**Verdict:** Interface-first contracts are the right *specification* move.
The ticket set is the wrong *product* and the wrong *timing*. If Definition of
Ready still has zero PASS rows and FREEZE forbids product crates, then opening
three Implement tracks is not parallelization — it is soft-passing the gate.

---

## Load-bearing entailments

### Contracts before code

**If** Rust and Clojure must talk through a stable schema, **then** the next
honest work is Interface Control Document + plants + human Accept — which the
port already treats as Draft under FREEZE — **not** three Cargo/Leiningen
scaffolds with mocks.

Disposition: **Embody** interface-first as Spec practice. **Refuse** “mocks
unlock Implement while Definition of Ready is red.”

### Thin thread as MVP

**If** the thin thread is only protocol shell + structural search + write_file,
**then** grounding gap, LockCheck, claim memory, and receipts are absent by
construction — the exact failure mode stakeholder discovery named (guessing
server).

**If** that thin thread is labeled “MVP of *this* product,” **then** it
contradicts BOUNDARY / VERIFY_STACK Must-intent (graph + locks + receipts +
claims).

Disposition: thin thread = **Could** filesystem helper or tip experiment —
**Refuse** as Wave-1 product MVP.

### Clojure as symbolic orchestrator

**If** Architecture Decision Record ADR-0005 says Clojure is read-mostly graph
ask over EDN export, **then** Epic 2 “orchestrator that decides which tools to
call” and “manages DeepWiki” as the cognitive control plane makes Clojure the
mutation brain.

**If** Architecture Decision Record ADR-0007 says Rust alone writes oracles and
owns the engine harness, **then** a Clojure orchestrator loop with a mock kernel
is designing the wrong owner.

Disposition: **Refuse** Epic 2.2 as written. Keep Epic 2.1-shaped **graph schema
EDN** as Could query model after Rust exports facts.

### WebAssembly verify spine in Track A / Epic 4

**If** Architecture Decision Record ADR-0004 requires native Rust LockCheck
first and WebAssembly guest only as Could / Wave-3, **then** Ticket 1.4 + Epic 4
as MVP “Verify Spine” invert the decision (sandbox before native decide).

Disposition: **Refuse** WebAssembly bridge as Epic-1 MVP. Native rule check in
Rust first; WebAssembly parity later.

### “SOT / Data” track

**If** systems of record are typed (policy locks in git ≠ derived index ≠
advisory wiki ≠ receipts), **then** one “SOT/Data” track that mixes Source Code
Index Protocol files, a-priori spine manifests, and environmental data will
launder writer authority.

**If** spine rules are data manifests in git with human Accept, **then** that
slice of Track C is compatible — call them **policy lock Intermediate
Representation**, not a catch-all SOT folder.

Disposition: **Embody** indexer + lock-manifest authoring as Spec/data prep.
**Refuse** undifferentiated SOT track naming.

### Receipts only at final integration

**If** receipts are the create-metric spine for grounding gap ≈ 0, **then**
parking “Audit: receipt generation” as the last wiring step trains every earlier
ticket to ship without Fresh / witnesses.

Disposition: **Refuse** receipts-as-afterthought. Receipt schema + Fresh plants
belong in the same dependency band as LockCheck, not the champagne cork.

### Calendar “1–2 weeks” / phase weeks

**If** agents must not commit calendar delivery fiction, **then** “Time to Thin
Thread MVP: 1–2 weeks” is process theater.

Disposition: **Refuse** week counts. Sequence by dependency only.

### Three agents in parallel on Implement

**If** FREEZE allows deepen-only on β/ρ, claim withdrawal, handle lifecycle
(plus sensor demotion), **then** three parallel Implement agents on Kernel /
Brain / Guard violate the freeze regardless of how clean the JSON contract is.

Disposition: **Refuse** parallel crate work now. **Embody** parallel *Spec*
work: schema tickets, plant tickets, lock-manifest Draft, zoom API Draft —
still no Cargo.

---

## What would make a three-track plan honest

Rewrite tracks as **specification contracts**, not build epics:

| Track | Allowed now (Spec) | Forbidden now |
| --- | --- | --- |
| A — Engine interface | JSON Schema for verify tools; receipt schema; structural-search *query shape*; hash-guard write *contract* | `mcp_server.rs`, wasmtime loaders |
| B — Graph / wiki | EDN **export** schema from registry; wiki page schema with content digests; no orchestrator | Clojure process that calls tools / writes oracles |
| C — Index / policy | Source Code Index Protocol consume notes; lock Intermediate Representation Draft in git; indexer runbook | “SOT” mega-folder; DeepWiki-minted policy |

**Thin thread (honest):** one plant that proves “search → resolve id → receipt
fields filled” on a fixture — still Spec/plant, or tip Spike outside this port’s
no-code gate — not product MVP.

**Integration (honest):** human Accept of contracts → then **one** tip writer
opens Rust engine; Clojure query brain only after EDN export exists; WebAssembly
only after native LockCheck plants pass.

---

## Dependency map (corrected)

```text
 human Accept (boundary Q1–Q4 + Definition of Ready band)
        │
        ▼
 Interface Control Document contracts (tools · locks · receipts · claims · EDN export)
        │
        ├──────────────────────┬────────────────────────┐
        ▼                      ▼                        ▼
 native Rust engine      lock manifests (git)     index consume runbook
 (search · registry ·         │                        │
  LockCheck · receipts ·      └──────────┬─────────────┘
  claims · hash write)                   │
        │                                │
        ▼                                ▼
 EDN export ──► Clojure query brain (read-mostly)     wiki pages (advisory + digests)
        │
        ▼
 WebAssembly LockCheck guest (parity)     post-write audit plants
```

Brain does **not** sit above Kernel as orchestrator. Guard does **not** depend
on Brain for policy — Guard depends on **git lock manifests**.

---

## Bottom line

| Proposal slogan | After entailment |
| --- | --- |
| Interface-first unlocks parallel build | Unlocks parallel **Spec**; not parallel crates under FREEZE |
| Three-track MVP | Wrong owners (Clojure orchestrator, WebAssembly spine) |
| Thin thread in 1–2 weeks | Wrong product + forbidden calendar claim |
| Receipts at the end | Inverts Must-intent spine |
| Mocks isolate Brain | Fine for query brain; fatal if Brain mutates |

**Implement:** still **Refuse**. Next useful edit to this roadmap: strip epics to
contract tickets that falsify Definition of Ready rows — or Accept boundary
Q1–Q4 and explicitly waive FREEZE in `SIGNOFF_LOG.md` before any crate.
