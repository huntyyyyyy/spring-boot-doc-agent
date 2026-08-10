---
id: Quality Attribute Scenario QAS-N-06
title: Deterministic re-verify
status: DRAFT
nfr_traces: [REQ-N-06]
---

# Quality Attribute Scenario QAS-N-06 — Determinism

| Part | Value |
| --- | --- |
| **Stimulus** | Re-run verify twice on identical content digests |
| **Source** | A-CI |
| **Environment** | Clean worktree; same binary digests |
| **Artifact** | Must verify spine |
| **Response** | Identical resolve + witness + claim disposition sets (timestamps stripped) |
| **Response measure** | Canonical JSON byte-identical across 2×5 fixtures |
