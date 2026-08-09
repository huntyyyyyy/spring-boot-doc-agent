---
category: Post-merge gate repair under cohesion bar
status: DRAFT — SPEC GATE E-HOT0 pending Approve of HOT1–HOT13
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
related:
  - docs/research/process/21-post-merge-gate-repair-cohesion-2026.md
  - docs/research/findings/2026-08-09-statement-split-cascade.md
  - docs/design/concept-split-cohesion-design-2026-08-09.md
  - docs/research/quality-backlog.md
do_not:
  - Implement product fixes before Approve of HOT1–HOT13
  - resume mechanical LOC/statement thrash
  - weaken constitution gates
  - expand tach depends_on in the hotfix tip
  - cite &lt;10000★ GitHub trees as *new* implement SoR on this stream
spec_gate: DRAFT E-HOT0 (2026-08-09) — HOT1–HOT13 pending Approve
---

# Design memo: E-HOT0 Spec gate (post-merge CI red)

> **DRAFT — awaiting Approve of HOT1–HOT13.**
>
> Research SoT: [`docs/research/process/21-post-merge-gate-repair-cohesion-2026.md`](../research/process/21-post-merge-gate-repair-cohesion-2026.md).
> This memo is the merge-facing Spec record; do not Implement until Approved.

**Spec record**

| Field | Value |
| --- | --- |
| Decisions | **HOT1–HOT13** pending Approve |
| Research SoT | process/21 (2026-08-09); **gh_sor_bar ≥10000★** for new external SoR |
| Prior Spec | E-COH0 Approved (hotfix carve-out COH1); E-DOC1 Done; E-STK0 Approved / E-STK1 Deferred |
| Branch | `cursor/local-ci-gate-fix-61f3` |
| Backlog | P18.0 Draft |

## Problem (one line)

`main` is red after `#112` merge-with-failures; local inventory shows G2 NameErrors, façade patch miss, CQ scope skew, collapsed soft band, obsolete metamorphic ratchet, and docs path drift — Spec-shaped, not typo-shaped.

## Verdict

Prefer **bounded hotfix epic E-HOT1** under HOT1–HOT13 after Approve; then resume **E-COH1** reshape. Refuse thrash, ceiling raises, tach-map expansion in the hotfix tip, and **new** &lt;10k★ framework Adopts.

## Decisions

See research memo §6 (HOT1–HOT13). Copy locked here on Approve.

## Adversarial

See research memo §8. Re-check before Approve.

## Exit

On Approve: stamp `spec_gate: APPROVED E-HOT0`, backlog P18.0 Approved, then E-HOT1 Implement with local `pre_pr --full` before any push.
