---
id: Quality Attribute Scenario QAS-N-01
title: Warm resolve latency
status: DRAFT — measure via Spike PIL-LAT-1
nfr_traces: [REQ-N-01]
---

# Quality Attribute Scenario QAS-N-01 — Warm resolve latency

| Part | Value |
| --- | --- |
| **Stimulus** | One binding request for a single injection site / type |
| **Source** | A-OP via command-line interface `resolve` |
| **Environment** | Warm registry+index; plant ≤ declared envelope; swap=0; reference SKU in Verification and Validation |
| **Artifact** | Resolver + Registry |
| **Response** | Impl symbol **or** Unknown/unprovable + reason_code; never silent multi-pick |
| **Response measure** | Wall p95 ≤ T ms over N≥30 calls; zero silent multi-candidate picks. **T filled by Spike PIL-LAT-1** — until then this Quality Attribute Scenario must not drive Design sizing Architecture Decision Records |

Design influence: **blocked** until T set or non-functional requirement demoted from Must.
