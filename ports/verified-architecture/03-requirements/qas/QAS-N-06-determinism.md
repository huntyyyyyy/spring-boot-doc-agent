---
id: Quality Attribute Scenario QAS-N-06
title: Deterministic re-verify
status: DRAFT
nfr_traces: [REQ-N-06]
---

# Quality Attribute Scenario QAS-N-06 — Deterministic re-verify

| Part | Value |
| --- | --- |
| **Stimulus** | Two consecutive verify runs on byte-identical content digests |
| **Source** | Actor A-CI |
| **Environment** | Clean worktree; same engine binary digests; timestamps stripped from compare set |
| **Artifact** | Must verify spine (resolve + LockCheck + ReceiptWriter + ClaimMemory) |
| **Response** | Identical resolve edges, witness sets, and claim disposition triples across runs |
| **Response measure** | Canonical JSON byte-identical across 2×5 fixtures; any byte drift → fail gate |
