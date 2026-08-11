---
title: Spike charter — receipt Fresh / ls-tree exclusion
status: DRAFT — unmeasured
date: '2026-08-11'
spike_id: SPIKE-receipt-fresh
freeze_class: deepen-3
accepted: false
related:
  - research/gaps/deepen-receipt-beta-rho-2026-08-11.md
  - research/papers-2026-may-aug/digests/2607.14890-proof-or-stop.md
  - 07-system-design/icd/receipt.schema.json
---

# SPIKE-receipt-fresh — Fresh predicate or Pilot invent

## Question

What exact tracked-tree exclusion list and serialization make
`material_digest` / `head_hash` / `policy_digest` / `command_set_digest`
re-derivable so \(\mathrm{Fresh}\) rejects stale receipts without
self-invalidating writeback?

## Exit (decidable)

Pick **one**:

1. **Measured:** document exclusion globs + a tamper plant matrix (stale tree,
   forged step, missing digest) that a future harness must fail closed.  
2. **Pilot invent, Fresh unmeasured:** keep required digests as Embody shapes;
   record that MVP Fresh enforcement is invent until Accept — do not claim
   Proof-or-Stop engine parity.

## Explicit Pilot note on `story_files_hash`

Paper β includes `storyFilesHash`. Product schema omits it. Exit also records
whether MVP **waives** required `story_files_hash` (Pilot) or schedules a
schema amendment under human Accept.

## Out of scope

Implement crates; dual receipt SoT revival; renaming in-toto as Proof-or-Stop.

## Status

**Unmeasured.** Mapping memo Present; plants / Accept absent.
