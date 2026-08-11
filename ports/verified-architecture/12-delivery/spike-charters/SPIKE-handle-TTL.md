---
title: Spike charter — Model Context Protocol handle TTL / expiry
status: DRAFT — unmeasured
date: '2026-08-11'
spike_id: SPIKE-handle-TTL
freeze_class: deepen-3
accepted: false
related:
  - research/gaps/deepen-mcp-handle-lifecycle-2026-08-11.md
  - research/gaps/mcp-handle-host-integration-note-2026-08-11.md
  - 07-system-design/icd/mcp/snapshot_open.output.schema.json
---

# SPIKE-handle-TTL — measure expiry or record Pilot invent

## Question

Does wall-clock `expires_at` alone suffice, or must digest re-check kill a
`snap_` when the tree moves underneath a still-young TTL?

## Exit (decidable)

Pick **one**:

1. **Measured:** a Draft plant shows (a) TTL expiry → `expired_handle`, and
   (b) digest drift before TTL → reject with `digest_mismatch` / `index_stale`.  
2. **Pilot invent, unmeasured TTL:** record next to `expires_at` that MVP uses
   invent defaults (e.g. 1h) without a measured plant — Accept still blocked.

## Out of scope

New tools; FO-CTL checker; Implement crates; Chosen scoreboards.

## Status

**Unmeasured.** Host note Draft exists; TTL remains Hypothesis.
