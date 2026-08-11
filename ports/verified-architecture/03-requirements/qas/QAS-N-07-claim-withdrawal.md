---
id: Quality Attribute Scenario QAS-N-07
title: Claim withdrawal under upstream drift
status: DRAFT
nfr_traces: [REQ-F-06c]
evidence: arXiv:2608.04278
---

# Quality Attribute Scenario QAS-N-07 — Claim withdrawal under upstream drift

| Part | Value |
| --- | --- |
| **Stimulus** | Prior claim row exists; anchored file bytes change **or** path becomes unavailable |
| **Source** | Developer edit / incomplete checkout |
| **Environment** | Local claim store + current tree; no network required |
| **Artifact** | ClaimMemory withdrawal query (Artifact-Anchored Verification Memory) |
| **Response** | Disposition becomes `affected` or `unprovable`; engine never invents a new resolve edge to “heal” the claim |
| **Response measure** | On fixture: 100% changed-anchor claims leave `unaffected`; 0 guessed beans / silent winners |
