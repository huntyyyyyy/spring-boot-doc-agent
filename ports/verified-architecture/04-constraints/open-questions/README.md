---
title: Open-question template (blocks-code)
status: ACTIVE
---

# Open questions ledger

Copy rows into `OQ-NNN.md` files. Any `blocks_code: true` must be closed or
explicitly waived in the wave charter before AI codegen.

```yaml
id: OQ-000
title: short name
blocks_code: true
wave: wave-1
domain: 04-constraints/open-questions
question: |
  What must we know?
invalidate_if: |
  Observation that would reopen this even after close.
evidence_needed:
  - Spike | stakeholder sign-off | paper | plant measurement
status: OPEN  # OPEN | SPIKE | CLOSED | WAIVED
```

## Seed OQs (wave-1)

| ID | Question | blocks_code |
| --- | --- | --- |
| OQ-01 | Single product boundary sentence: local verify engine vs RAG corpus vs both? | true |
| OQ-02 | SoR vs derived matrix for index, registry, locks, receipts, embeddings | true |
| OQ-03 | Spring DI envelope: what SCIP cannot resolve → mandatory Unknown taxonomy | true |
| OQ-04 | Executable lock IR shape (language-agnostic) before any engine language | true |
| OQ-05 | Proof-tour receipt schema (stable step IDs) | true |
| OQ-06 | Cache/invalidation / freshness budgets for index | true |
| OQ-07 | Which Must NFRs still lack six-part QAS measures? | true |
| OQ-08 | Wave-1 BC set (likely 1–2); rest parked under options/ | true |
