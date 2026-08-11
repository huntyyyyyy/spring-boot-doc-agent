---
id: Quality Attribute Scenario QAS-N-01
title: Warm resolve latency
status: DRAFT — measure via Spike PIL-LAT-1
nfr_traces: [REQ-N-01]
---

# Quality Attribute Scenario QAS-N-01 — Warm resolve latency

| Part | Value |
| --- | --- |
| **Stimulus** | One binding request for a single injection site / type key |
| **Source** | Actor A-OP via command-line interface verb `resolve` |
| **Environment** | Warm registry + Source Code Index Protocol index; plant ≤ declared Java/Boot envelope; swap=0; reference SKU named in Verification and Validation |
| **Artifact** | Resolver + derived SQLite registry (Rust engine write path) |
| **Response** | Returns exactly one of: bound impl symbol **or** Unknown/unprovable with `reason_code`; never ranks silent multi-candidate winners |
| **Response measure** | Wall-clock p95 ≤ T ms over N≥30 calls; zero silent multi-candidate picks. **T filled by Spike PIL-LAT-1** — until then this Quality Attribute Scenario must not drive Design sizing Architecture Decision Records |

Design influence: **blocked** until T set or the non-functional requirement demoted from Must.
