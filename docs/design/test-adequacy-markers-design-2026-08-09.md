---
category: CI / test adequacy markers / anti-padding Verify
status: APPROVED — SPEC GATE E-QA0 (2026-08-09)
date: '2026-08-09'
approved_policies: Q1-Q8
implement_now: E-QA1 E-QA2
claim_tiers: Evidenced / Confirmed / Unknown
research: docs/research/coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
title: 'Design memo: test adequacy markers (E-QA)'
related: []
last_reviewed: '2026-08-10'
---

# Design memo: test adequacy markers (E-QA)

> **APPROVED — SPEC GATE E-QA0 (2026-08-09)**
>
> Principal / implementer chat recorded **Approve** of policies **Q1–Q8**.
> Implement epics **E-QA1** (adequacy sensor ports + CI summary) and **E-QA2**
> (anti-padding Verify for climb) are unblocked. Does not reopen fail_under
> **98.7**, policy **16-A**, E-TEST domain partition, or scrap of Cover%.

**Spec record**

| Field | Value |
| --- | --- |
| Policies | **Q1–Q8** Approved |
| Implement now | **E-QA1** structural + mutator-survivor + metamorphic sensors · **E-QA2** climb adequacy witness |
| Defer / refuse this stream | Suite-wide mutmut hard gate · Prompt Coverage as floor · PIT zoo · LLM-judge fail_under · scrap Cover%/E-TEST |
| Research | [`docs/research/coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md`](../research/09-test-adequacy-vs-coverage-inflation-2026.md) |
| Backlog | [`docs/research/quality-backlog.md`](../research/quality-backlog.md) P8 |

---

## 1. Problem

Cover% and gap-average correctly measure **execution footprint** but do not
measure **discriminative power**. Process pressure to clear below-floor files
can ship lousy climb tests (execute lines, weak asserts) while gate/assertion
mutators remain `ENFORCE=False`. `[Confirmed]` research **09**; math:
mutation-score suite selection is monotone submodular / NP-hard
(`[Evidenced]` 2603.01409, 2604.01799).

---

## 2. Locked product shape (v1)

| Concern | Choice |
| --- | --- |
| Necessary merge SoT | Whole-repo Cover% **98.7** + diff-cover (unchanged) |
| Partition SoT | E-TEST `domain_*` (not adequacy proof) |
| Adequacy sensors | Distinct ports: structural summary · gate-mutator survivors · metamorphic vacuity |
| Climb Archive | Package Cover% uplift requires mutation or metamorphic **witness** (Q2) |
| Mutation taxonomies | Gates / assertions / optional mutmut stay **three** mechanisms (Q3) |
| Hard `ENFORCE` | Measurement-first baselines only (Q8) |

Sensors never claim the Cover% floor.

---

## 3. Package sketch (SOLID / DDD) — E-QA1

Concept package `doc_engine.ci.adequacy` (not `utils/`):

| Module | SRP |
| --- | --- |
| `criterion_ports` | Protocol / value objects for an adequacy report slice |
| `structural_summary` | Reuse oracle/climb Cover% facts as one sensor row |
| `mutator_survivors` | Read gate-mutator / assertion-driver scores (report-only until Spec amends) |
| `metamorphic_vacuity` | Point at Arm-1 / harness vacuity status |
| `github_adequacy_summary` | Markdown presenter for `$GITHUB_STEP_SUMMARY` (OCP sinks = new modules) |

Thin `scripts/ci/adequacy_summary.py` façade. LOC ≤225 / complexipy ≤5; TDD
under `tests/ci/test_adequacy_*.py`.

---

## 4. Anti-padding Verify — E-QA2

When a climb batch raises Cover% on package \(P\):

1. Name the witness (scoped incident mutants and/or mutmut slice and/or
   metamorphic relation that bites \(P\)).
2. Record witness in climb Archive / CONTRIBUTING checklist.
3. Do **not** treat gap-average green alone as Archive proof.

---

## 5. Non-goals

- Replacing Cover% with mutation score as sole merge SoT
- Folding three mutation taxonomies into one PIT/mutmut zoo
- Prompt Coverage / MIST-RL as Stage-0 CI runtime
- Weakening fail_under, LOC, or complexipy ceilings
