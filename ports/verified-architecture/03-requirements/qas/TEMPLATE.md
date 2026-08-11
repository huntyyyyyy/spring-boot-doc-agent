---
id: Quality Attribute Scenario QAS-N-00
title: short name
status: DRAFT
nfr_traces: []
---

# Quality Attribute Scenario — six-part (required before Design influence)

Each cell must add an attribute **not** already in `title` / `id`. Prefer: quantity, path, actor id, exit code, or fail-mode.

| Part | Value (shape, not synonym of title) |
| --- | --- |
| **Stimulus** | Observable event + count/size (e.g. “1 binding request”, “N≥30 calls”) |
| **Source** | Named actor or tool (`A-OP`, `fitness_check`, deny-net harness) |
| **Environment** | Preconditions with bounds (warm registry, plant envelope, concurrency) |
| **Artifact** | Concrete component under stress (Resolver, LockCheck, ReceiptWriter) |
| **Response** | Observable outputs + forbidden behaviors (Unknown + reason_code; never silent multi-pick) |
| **Response measure** | Pass/fail metric with number or Spike id (no TBD on Must that still influences Design) |

Incomplete measures ⇒ demote the non-functional requirement out of Design influence **or** block Design sizing Architecture Decision Records until Spike exits.
