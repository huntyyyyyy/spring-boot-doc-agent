---
title: Adversarial review — plugin kernel / middleware / zoom tests wireframe
status: REVIEW — better shape; still wrong start
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
look_first:
  - research/gaps/review-kernel-wireframe-2026-08-11.md
  - docs/adr/adr-0004-native-then-wasm-lockcheck.md
  - docs/adr/adr-0011-mcp-protocol-and-tool-surface.md
  - 07-system-design/icd/mcp-tools.md
  - STATUS.md
accepted: false
---

# Review: ToolRegistry + middleware + zoom tests

**Question:** Is this refined wireframe a good place to start?

**Short answer:** Better **internal design taste** than the monolithic match
block. Still **not** where this port starts. Patterns ≠ product surface ≠
permission to open crates.

---

## What improved (honest)

**If** tools are registered behind a trait and the dispatch loop is stable,
**then** adding an *implementation* later need not edit a giant `match` — that
is ordinary open/closed for code organization.

**If** policy runs as middleware around `atomic_write` instead of living inside
the write tool, **then** “hands” and “policy” are separable — good for testing
and for swapping a native LockCheck for a later WebAssembly guest.

**If** tests exist for zoom depth and policy rejection, **then** the author is
trying to plant *something* falsifiable — better than diagram-only theater.

Disposition: **Embody** registry + middleware + plant intent as *future* engine
shape notes. Do not treat them as greenlight for `kernel/`.

---

## Entailments that still block

### Gate

**If** FREEZE and Definition of Ready still forbid product crates, **then**
`kernel/src/core.rs` remains Implement theater no matter how SOLID the traits
look.

### Session id on every context

**If** Model Context Protocol **2026-07-28** is session-free at the wire and
application state must be **handles** (snapshot digests), **then**
`McpContext { session_id }` teaches the wrong default. Prefer
`request_id` + optional typed handle fields — not a session string.

Disposition: **Refuse** `session_id` as first-class context field in Spec.

### Open for Extension vs FREEZE / primitives

**If** FREEZE says stop adding tools and the Interface Control Document pins a
small primitive set, **then** “register any new tool without touching the
kernel” is a **liability** for product discipline even when it is good
library design.

**If** Open/Closed applies, **then** apply it to **backends** (index adapters,
language parsers), not to unbounded tool-name sprawl without human Accept.

Disposition: **Embody** plugin *backends*. **Refuse** unbounded tool registry
as the Wave-1 product story.

### WebAssembly middleware as the spine

**If** Architecture Decision Record ADR-0004 requires native LockCheck first,
**then** `SpineGuardMiddleware` that always calls Wasmer on `atomic_write` is
still the sandbox-before-spine mistake — only the call site moved.

**If** validation only sees proposed file `content` text, **then** rejecting
`Database::connect()` in a view file is a string heuristic, not graph+lock
Intermediate Representation LockCheck.

Disposition: middleware should call **native** `LockCheck(proposed_diff,
lock_set, registry_snapshot)` first. WebAssembly guest = later parity plug-in
behind the same middleware trait.

### Wrong tool names vs Interface Control Document

**If** Surface A is `snapshot_open` / `verify` / `resolve` / `claim_withdraw` /
`locks_list`, **then** a kernel whose flagship tools are `zoom_read` and
`atomic_write` is still the filesystem helper product.

Disposition: `zoom_read` = **Could** / presentation. Hash-guarded write =
mutation helper behind harness. Neither replaces verify/claim tools.

### Tests are weak plants

**If** `test_zoom_lens_resolution` only asserts Level-1 string length &lt;
Level-3 length, **then** a stub that returns `"x"` vs `"xxxx"` passes — it does
not prove structural folding.

**If** `test_spine_enforcement` only feeds a forbidden substring and expects
`PolicyViolation`, **then** it plants the heuristic engine, not architectural
LockCheck (no lock manifest, no graph edge, no receipt).

Disposition: **Refuse** these two tests as Definition of Done for the spine.
Rewrite plants: skeleton omits function bodies; lock plant uses fixture
Intermediate Representation + edges.

### Empty post_execute

**If** post-write adversarial audit is a claimed dimension, **then**
`post_execute` that always `Ok(())` is a reserved name, not a feature.

### Receipts disappeared

**If** the prior wireframe at least emitted a toy receipt and the Interface
Control Document requires β/ρ-shaped receipts, **then** this refinement
regressed by showing dispatch without receipt middleware.

Disposition: prefer `ReceiptMiddleware` post_execute that appends/writes
**ICD-shaped** receipts — still Spec-first, not this crate.

---

## Good place to start (same patterns, Spec form)

1. Document “dispatch = registry + middleware” as an Architecture Brief note —
   no `Cargo.toml`.  
2. Draft JSON Schema for `zoom_read` depths 1–4 (Could) beside existing verify
   tools — do not replace them.  
3. Draft middleware **order**: drift check → native LockCheck → write → receipt
   → post-audit plant. WebAssembly slot optional at end of native path.  
4. Replace length/substring tests with fixture plants under
   `08-verification/plants/`.  
5. Drop `session_id`; use handles.

---

## Bottom line

| Piece | Better than v1? | Start here? |
| --- | --- | --- |
| ToolRegistry / `McpTool` | Yes (structure) | No crates |
| Middleware pipeline | Yes (structure) | Native LockCheck behind trait first |
| Zoom as separate tool | Yes (Could) | Schema + real fold plant |
| Wasmer spine middleware | No (same spine error) | No |
| `session_id` | Worse vs 2026-07-28 | Remove |
| Integration tests shown | Theater-prone | Rewrite plants |

**SOLID wiring is not stewardship.** Start with contracts and plants that can
fail Definition of Ready — not with a prettier kernel skeleton.
