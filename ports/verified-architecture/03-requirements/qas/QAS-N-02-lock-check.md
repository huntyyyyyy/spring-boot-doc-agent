---
id: Quality Attribute Scenario QAS-N-02
title: Lock check latency + receipt integrity
status: DRAFT — latency via Spike PIL-LAT-2; receipt rules active now
nfr_traces: [REQ-N-02]
---

# Quality Attribute Scenario QAS-N-02 — Lock check latency + receipt integrity

| Part | Value |
| --- | --- |
| **Stimulus** | Changed-file outbound edges evaluated against in-repo architecture locks |
| **Source** | Actor A-DEV save path or command-line interface `fitness_check` |
| **Environment** | Warm locks + graph; ≤10 concurrent local checks; clean worktree |
| **Artifact** | LockCheck + ReceiptWriter + ClaimMemory (Rust oracle writer only) |
| **Response** | Emits violation set **or** clean; writes schema-valid receipt; persists claim anchors; large language model text never enters witnesses |
| **Response measure** | (a) p95 ≤ U ms — **U via Spike PIL-LAT-2** (latency part blocked for Design). (b) **Active now:** 100% receipts schema-valid; freshness digests present; 0 large-language-model strings in witness fields (Proof-or-Stop / Artifact-Anchored Verification Memory) |
