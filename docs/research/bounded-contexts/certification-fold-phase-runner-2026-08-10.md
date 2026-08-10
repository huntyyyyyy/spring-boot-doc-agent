---
title: E-CERT0 — Certification fold honesty under phase runner (Spec seed)
status: DRAFT Spec — pending Approve of C0-1–C0-8
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: pipeline certification derived view
related:
  - docs/research/cold-product-bc-research-map-2026-08-10.md
  - docs/design/ddia-north-star/deviations/dev-certification-derived-view.md
  - src/doc_engine/pipeline/certification_fold.py
  - src/doc_engine/tools/certification.py
  - src/doc_engine/pipeline/local_runner_phases/
do_not:
  - hand-edit certification.json as SoR
  - LWW-merge certification with facts
  - Implement PIPE1 size cuts that break fold inputs before Approve
  - treat LLM-judge or mock as certified without --allow-mock honesty
spec_gate: DRAFT E-CERT0 (2026-08-10)
human_review_floor: true
---

# Principal memo: certification fold (E-CERT0)

**Question.** `certification.json` is a **derived** view (B2.5). Phase runner
splits and cold fold code risk vacuous `certified: true` or dual-writer drift.
What Spec locks honesty before E-PIPE1?

## Verdict

| Stance | Choice |
| --- | --- |
| **Embody** | SoR = stage/gate facts; certification recomputed; never LWW `[Confirmed]` DDIA deviation |
| **Adopt** | SLSA-like **predicate honesty** (builder/executor labels, subjects, parameters) as schema fields — pattern only `[Evidenced]` slsa.dev |
| **Refuse** | Hand-edit demos; dual-writer; LLM-judge as cert; silent mock-as-live |

## Decisions (C0-1–C0-8) — pending Approve

| ID | Decision |
| --- | --- |
| **C0-1** | Reaffirm B2.5 derived-view; recompute on disagreement |
| **C0-2** | `generative_executor` / mock labeling remain fail-closed for verify |
| **C0-3** | Fold inputs enumerated (which phase artifacts feed fold) — Spec table before PIPE1 chops |
| **C0-4** | No second writer path outside fold regenerator |
| **C0-5** | Human review of certification claims in operator Path B remains floor |
| **C0-6** | SLSA product signing Explicit Defer; honesty fields Adopt optionally |
| **C0-7** | E-PIPE1 may split modules only after C0-3 table lands |
| **C0-8** | Vacuous certified-without-gates is a hard defect class |

## Exit

Approve C0-1–C0-8 in design memo → unblocks safe E-PIPE1 under human review.
