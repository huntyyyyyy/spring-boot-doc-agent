---
id: Quality Attribute Scenario QAS-N-07
title: Claim withdrawal under upstream drift
status: DRAFT
nfr_traces: [REQ-F-06c]
evidence: arXiv:2608.04278
---

# Quality Attribute Scenario QAS-N-07 — EA-Graph withdrawal

| Part | Value |
| --- | --- |
| **Stimulus** | Prior claim exists; anchored file content changes OR becomes unavailable |
| **Source** | Developer edit / incomplete checkout |
| **Environment** | Local claim store + current tree |
| **Artifact** | ClaimMemory withdrawal query |
| **Response** | Disposition `affected` or `unprovable`; never invents a new resolve edge |
| **Response measure** | On fixture: 100% changed-anchor claims leave `unaffected`; 0 guessed beans |
