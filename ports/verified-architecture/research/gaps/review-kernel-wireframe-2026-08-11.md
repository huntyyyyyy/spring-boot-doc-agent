---
title: Adversarial review — rough Rust/Clojure/WebAssembly wireframe
status: REVIEW — good idea seeds; bad start-of-code
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
look_first:
  - 07-system-design/icd/receipt.schema.json
  - docs/adr/adr-0004-native-then-wasm-lockcheck.md
  - docs/adr/adr-0005-clojure-graph-brain.md
  - docs/adr/adr-0007-rust-owns-engine.md
  - research/gaps/review-three-track-mvp-2026-08-11.md
  - STATUS.md
accepted: false
---

# Review: rough kernel / brain / guard wireframe

**Question:** Is this a good place to start?

**Short answer:** It is a useful **sketch of intents** (hash-guarded write, zoom
depth, status enum, receipt *idea*). It is a **bad place to start coding** for
this port — wrong owner, wrong spine, toy receipt, and it soft-passes FREEZE /
Definition of Ready.

---

## Entailments

### Timing / gate

**If** Definition of Ready has zero PASS rows and FREEZE forbids product crates,
**then** `kernel/src/main.rs` + Wasmer + Clojure atoms is not a start — it is
Implement theater.

Disposition: **Refuse** as first commit of product code.

### Hash-guarded write

**If** `AtomicWrite` requires `expected_hash` and returns `DriftError` on
mismatch, **then** that matches the stakeholder “state drift” contract and
should live in the Interface Control Document — not only in sample Rust.

Disposition: **Embody** as schema/plant. Do not need this file to capture it.

### “Cryptographic proof” receipt

**If** `Receipt` is only `pre_hash` / `post_hash` / `timestamp` / `operation`,
**then** it is a **file mutation log**, not the product receipt
(`head_hash`, `material_digest`, `policy_digest`, `command_set_digest`, step
ρ fields, ban on model text as witness) in `icd/receipt.schema.json`.

**If** there is no signature / producer authorization, **then** calling it
cryptographic *proof* overclaims — content hashing ≠ Proof-or-Stop Admissible.

Disposition: **Embody** “emit a receipt on mutation.” **Refuse** this struct as
the receipt System of Record.

### WebAssembly on the write path first

**If** Architecture Decision Record ADR-0004 says native LockCheck first and
WebAssembly guest Could / Wave-3, **then** `validate_via_wasm` before every
atomic write as the policy gate inverts the decision.

**If** `validate(len)` only sees a byte length / content blob without graph
edges, lock Intermediate Representation, or snapshot digests, **then**
“Dependency Inversion” checks that `content.contains("database_connection")`
are slogan heuristics — not architectural LockCheck.

Disposition: **Refuse** Wasmer-first guard as MVP spine. Native check against
git lock manifests + registry; WebAssembly parity later. Runtime choice
(Wasmer vs wasmtime) is unsettled and secondary.

### Three commands as the kernel surface

**If** the draft Interface Control Document lists `snapshot_open`, `verify`,
`resolve`, `claim_withdraw`, `locks_list`, **then** a kernel that only exposes
`ZoomRead` / `AtomicWrite` / `QuerySot` is a different product (filesystem +
symbol lookup helper).

Disposition: Zoom + hash write = **Could** tools or presentation helpers.
**Refuse** replacing Surface A with this trio.

### Clojure `repo-state` atom as managed System of Truth

**If** the registry is wipe/rebuild derived SQLite owned by Rust, and policy
locks live in git, **then** a process-local Clojure `atom` that `update-sot!`
mutates is a third, non-durable “truth” that dies on restart and invites dual
writers.

**If** Architecture Decision Record ADR-0005 says read-mostly query brain,
**then** `process-agent-intent` calling the kernel and updating SOT is an
orchestrator/oracle — rejected owner.

Disposition: **Refuse** atom-as-SOT and brain-as-orchestrator. Keep EDN **import
of exports** from Rust if Clojure exists at all.

### Double brain

**If** the Model Context Protocol host (IDE / agent) already plans tool calls,
**then** a Clojure layer that also “determines which tools to call” stacks two
planners. That adds latency and a second place for wrong plans without adding a
deterministic decide step.

Disposition: **Refuse** as default topology. Agent → TypeScript presentation →
Rust engine (decide). Clojure optional for interactive graph ask.

### Panic / unwrap style

**If** this is a long-lived server, **then** `expect("Disk I/O Failure")` /
`unwrap` on missing exports turns disk errors into process death instead of
`SystemError` responses.

Disposition: style defect even as a Spike — use `Result` end-to-end in any
future crate.

### Tokio + Mutex&lt;Instance&gt;

**If** Wasmer instances and linear memory are not trivially shareable across
tasks, **then** `Arc&lt;Mutex&lt;Instance&gt;&gt;` is a research Spike, not settled
enterprise design. Secondary to the spine-order problem.

Disposition: **Unknown** — do not bikeshed runtime before native LockCheck
exists.

---

## What *is* a good place to start (same ideas, Spec form)

1. Add/adjust Interface Control Document drafts: `ZoomRead` depth enum (1–4);
   `AtomicWrite` / apply_diff with `expected_hash` → `DriftError`; response
   status vocabulary.  
2. Keep receipt work on **existing** `receipt.schema.json` + Fresh Spike — map
   pre/post file hash into `steps[]` or material binding, do not fork a toy
   struct.  
3. One **plant**: “hash mismatch → no write”; one plant: “lock violation → no
   write” (native).  
4. Do **not** open `kernel/` / `brain/` / `guard/` trees until Definition of
   Ready and FREEZE waiver or PASS.

---

## Bottom line

| Wireframe piece | Keep as idea? | Start coding it now? |
| --- | --- | --- |
| `expected_hash` drift | Yes | No — schema/plant first |
| Zoom depth | Yes | No — API Draft first |
| Receipt on write | Yes (real schema) | No — deepen ICD, not this stub |
| Wasmer validate on write | No as MVP spine | No |
| Clojure atom SOT + orchestrator | No | No |
| Three-command kernel | Partial Could | No as product Surface A |

**Good place to start:** contracts + plants that falsify Definition of Ready.
**This wireframe as first code:** **Refuse**.
