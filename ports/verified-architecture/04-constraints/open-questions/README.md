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

## Seed open questions (wave-1)

| ID | Question | blocks_code |
| --- | --- | --- |
| open question OQ-01 | Single product boundary sentence: local verify engine vs Retrieval-Augmented Generation corpus vs both? | true |
| open question OQ-02 | System of Record vs derived matrix for index, registry, locks, receipts, embeddings | true |
| open question OQ-03 | Spring Dependency Injection envelope: what Source Code Index Protocol cannot resolve → mandatory Unknown taxonomy | true |
| open question OQ-04 | Executable lock IR shape (language-agnostic) before any engine language | true |
| open question OQ-05 | Proof-tour receipt schema (stable step IDs) | true |
| open question OQ-06 | Cache/invalidation / freshness budgets for index | true |
| open question OQ-07 | Which Must non-functional requirements still lack six-part Quality Attribute Scenario measures? | true |
| open question OQ-08 | Wave-1 bounded context set (likely 1–2); rest parked under options/ | true |
