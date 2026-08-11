---
title: Open-question template (blocks-code)
status: ACTIVE
---

# Open questions ledger

Each `OQ-NNN.md` must state a **decidable** close criterion and a **concrete**
`invalidate_if` (not “new evidence”). Any `blocks_code: true` must be CLOSED or
WAIVED in the wave charter before AI codegen.

```yaml
id: OQ-000
title: short name
blocks_code: true
wave: wave-1
domain: 04-constraints/open-questions
question: |
  What must we know? (attribute + options, not synonym of title)
invalidate_if: |
  Specific observation that reopens (path, metric, or product pivot).
evidence_needed:
  - Spike | stakeholder sign-off | paper | plant measurement
status: OPEN  # OPEN | SPIKE | CLOSED | WAIVED
```

## Seed open questions (wave-1)

| ID | Decidable question | blocks_code | Status |
| --- | --- | --- | --- |
| open question OQ-01 | Accept or amend the one-liner in `BOUNDARY.md` (local verify vs Retrieval-Augmented Generation corpus vs both)? | true | SPIKE |
| open question OQ-02 | Human Accept of `sor-derived-matrix.md` (esp. Retrieval-Augmented Generation ≠ verify; single oracle)? | true | SPIKE |
| open question OQ-03 | Accept Unknown taxonomy + plant confirmation of Spring Dependency Injection envelope? | true | SPIKE |
| open question OQ-04 | Choose executable lock Intermediate Representation shape before engine language binding? | true | OPEN |
| open question OQ-05 | Accept receipt schema fields + Spike `step_id` stability key? | true | SPIKE |
| open question OQ-06 | Numeric freshness / invalidation budgets for local indexes? | true | OPEN |
| open question OQ-07 | Latency T/U for Quality Attribute Scenarios QAS-N-01 / QAS-N-02 still unset (Spike or demote)? | true | OPEN |
| open question OQ-08 | Name the 1–2 wave-1 bounded contexts; park other languages under `options/`? | true | OPEN |

All eight still block Implement. **Rust** engine host assumed; **Refuse Python** not reopenable here without Architecture Decision Record.
