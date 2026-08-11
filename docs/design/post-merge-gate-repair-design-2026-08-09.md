---
category: Post-merge gate repair under cohesion bar
status: APPROVED — SPEC GATE E-HOT0 (2026-08-09) — HOT1–HOT13
date: '2026-08-09'
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/research/process/21-post-merge-gate-repair-cohesion-2026.md
- docs/research/findings/2026-08-09-statement-split-cascade.md
- docs/design/concept-split-cohesion-design-2026-08-09.md
- docs/research/quality-backlog.md
do_not:
- resume mechanical LOC/statement thrash
- weaken constitution gates
- expand tach depends_on in the hotfix tip
- cite &lt;10000★ GitHub trees as *new* implement SoR on this stream
- push before local full-gate green
spec_gate: APPROVED E-HOT0 (2026-08-09) — HOT1–HOT13
title: 'Design memo: E-HOT0 Spec gate (post-merge CI red)'
last_reviewed: '2026-08-10'
---

# Design memo: E-HOT0 Spec gate (post-merge CI red)

> **APPROVED — SPEC GATE E-HOT0 (2026-08-09)**
>
> Research SoT: [`docs/research/process/21-post-merge-gate-repair-cohesion-2026.md`](../research/process/21-post-merge-gate-repair-cohesion-2026.md).

**Spec record**

| Field | Value |
| --- | --- |
| Decisions | **HOT1–HOT13** Approved |
| Research SoT | process/21; **gh_sor_bar ≥10000★** for new external SoR |
| Prior Spec | E-COH0 Approved (hotfix carve-out COH1); E-DOC1 Done |
| Branch | `cursor/local-ci-gate-fix-61f3` |
| Backlog | P18.0 Approved → P18.1 E-HOT1 Active |

## Exit

E-HOT1 Implement next; local `pre_pr --full` before push.
