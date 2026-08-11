---
title: Adversarial review — event-sourced capability runtime sketch
status: REVIEW — audit log Embody; event-log-as-only-SoT Refuse; still no crates
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
audience: [architect, stakeholder, agent]
look_first:
  - research/gaps/review-agent-os-mvp-primitives-2026-08-11.md
  - 08-verification/sor-derived-matrix.md
  - docs/adr/adr-0004-native-then-wasm-lockcheck.md
  - docs/adr/adr-0007-rust-owns-engine.md
  - 07-system-design/icd/receipt.schema.json
  - STATUS.md
accepted: false
project_scope: ports/verified-architecture only — not tip doc-engine
---

# Review: event-sourced, capability-based “High-Integrity Agentic Runtime”

Pitch: leave request/response wrappers; Event Sourcing + Merkle-DAG as System
of Truth; async actor reactor in Rust; Clojure as fold/reducer over the log;
Open Policy Agent–style declarative spine; capabilities on every execute.

**Scope:** greenfield verified-architecture / Agent OS Spec only. Tip monorepo
tests and Spring documentation engine are **out of scope**.

**Verdict:** Capability-checked **propose → validate → execute** and an
**immutable action log** are the right *class* of solution. Treating the event
log as the **only** truth, logging every read, and calling string tokens
“cryptographic capabilities” overclaim. Actor/OPA/Merkle-DAG packaging is
Could complexity, not Wave-1 Must. Still **Refuse** opening crates under FREEZE.

---

## What improved vs prior wireframes

**If** the reactor checks capability and policy **before** `state_manager.execute`,
**then** you fixed the mutate-then-gate bug from the earlier MVP sample — keep
that order.

**If** Clojure `apply-event` / `project-sot` is a pure fold over events,
**then** that is a better Brain role than “orchestrator that owns the atom as
truth.” Projections may live in any language; **writers** of the log stay in
the execution layer (Rust per Architecture Decision Record ADR-0007).

**If** DeepWiki / repo map are **projections** of a log, **then** that matches
“advisory views over derived facts” — Embody as framing, not as merge SoR.

---

## Entailments that still bite

### Event log as the only System of Truth

**If** target sources and policy locks live in **git**, **then** the agent’s
event log is an **audit / thought-chain / receipt stream** — a second store —
not a replacement for the repository.

**If** “current state is a liability” means you never materialize a projection,
**then** every query replays the world (cost). Real systems use **log +
snapshots/projections** (command/query split). Deny “only the log, never a
map.”

**If** every Read is an immutable event in a Merkle-DAG, **then** zoom/search
traffic explodes the log and privacy surface. Log **mutations** and
**decisions** first; treat reads as optional telemetry.

Disposition: **Embody** append-only decision/mutation log (align with receipts).
**Refuse** event-log-replaces-git and read-everything-into-the-DAG as MVP.

### Time-travel “Thought-Chain” rollback

**If** code history is already in git, **then** rolling back *files* is git’s
job. Rolling back an *agent episode* without reverting unrelated commits needs
explicit event boundaries and conflict rules — Pilot invent, not free.

Disposition: **Could** Spike (episode id → set of receipts). **Refuse** as
implied free feature of Merkle-DAG.

### Capabilities

**If** Model Context Protocol `2026-07-28` already uses minted handles,
**then** path/symbol-scoped capabilities are the same idea.

**If** `Capability.token` is an opaque `String` with no mint, bind, expiry, or
signature story, **then** “cryptographic capability” is branding.

Disposition: **Embody** digest-bound handles (see deepen handle lifecycle).
**Refuse** crypto claims until mint/verify is specified.

### Actor “micro-kernel”

**If** one Tokio task owns `StateManager` + `GuardEngine` and tools are only
commands on a channel, **then** this is a **single reactor**, not a fleet of
isolated actors with separate failure domains.

**If** the goal is privilege separation, **then** the win is “no raw disk in
the model” + capability check — not mailbox theater.

Disposition: **Could** later for parallelism. **Refuse** equating this sketch
with seL4-class microkernel assurance.

### Policy-as-code (Rego)

**If** invariants are data (deny rules) reviewed in git, **then** that matches
policy System of Record better than DeepWiki auto-mint.

**If** Rego/OPA or “compiled into WebAssembly Guard” is Wave-1 Must,
**then** you add a runtime and skip native LockCheck-first (Architecture
Decision Record ADR-0004).

Disposition: **Embody** declarative lock/deny manifests in git. **Could** OPA
or WebAssembly evaluation later. Native check first.

### Interface permanence (from your DE rules — still true)

**If** the durable product is the **contract** (tool schemas, receipt schema,
event envelope, capability fields), **then** spend design time there — agreed.

**If** that justifies `kernel/src/runtime.rs` now, **then** no — FREEZE /
Definition of Ready still block crates. Schema + plants first.

### Thin thread / calendar

**If** a vertical slice is hash-lock → structural candidate → gate → write →
receipt → projection update, **then** that thread is right.

**If** “2 weeks” is the success criterion, **then** refuse calendar fiction;
sequence by dependency only.

---

## Map onto this Spec (greenfield)

| Pitch piece | Spec landing |
| --- | --- |
| Immutable mutation/decision log | Receipts + claim dispositions (+ optional episode log) |
| Projections (wiki / map) | Derived / advisory — rebuildable |
| Capability on execute | Handle mint/bind/expire |
| Guard before execute | Native LockCheck / deny plants **before** write |
| Brain as reducer | Optional read-side fold over exported events — not oracle writer |
| Actor bus / OPA / Merkle-DAG store | Could — not Wave-1 Must |

---

## Bottom line

**If** you want the class of solution (auditability, privilege separation,
deterministic transitions), **then** keep: capability-checked dispatch, gate
**before** write, append-only receipts/events, pure projections.

**If** you want “Event-Sourced Merkle-DAG Actor Runtime with Rego” as day-one
product shape, **then** that is platform sprawl ahead of Definition of Ready.

**Implement:** still **Refuse**. Next Spec artifacts only: event/receipt
envelope Draft, capability fields on tools, plant for “deny before write.”
No tip-repo testing. No Cargo under this port until Accept/FREEZE waiver.
