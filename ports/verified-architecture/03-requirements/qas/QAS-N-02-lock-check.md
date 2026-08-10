---
id: Quality Attribute Scenario QAS-N-02
title: Lock check latency + receipt integrity
status: DRAFT — latency via Spike PIL-LAT-2; receipt rules active now
nfr_traces: [REQ-N-02]
---

# Quality Attribute Scenario QAS-N-02 — Lock check

| Part | Value |
| --- | --- |
| **Stimulus** | Changed file outbound edges evaluated against locks |
| **Source** | A-DEV save or `fitness_check` |
| **Environment** | Warm locks+graph; ≤10 concurrent local checks |
| **Artifact** | LockCheck + ReceiptWriter + ClaimMemory |
| **Response** | Violation set or clean; schema-valid receipt; claim anchors written |
| **Response measure** | (a) p95 ≤ U ms — **U via Spike PIL-LAT-2** (latency part blocked for Design). (b) **Active now:** 100% receipts schema-valid; freshness digests present; large language model text absent from witnesses (Proof-or-Stop / EA-Graph) |
