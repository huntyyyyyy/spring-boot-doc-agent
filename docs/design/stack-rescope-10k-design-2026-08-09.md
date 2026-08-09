---
category: Stack rescope under ≥10k★ SoR
status: DRAFT — SPEC GATE E-STACK0 pending Approve of STACK1–STACK12
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
related:
  - docs/research/process/22-stack-rescope-10k-star-bar-2026.md
  - docs/research/process/21-post-merge-gate-repair-cohesion-2026.md
  - docs/research/modularity/20-tach-dependency-blueprint-2026.md
  - docs/research/quality-backlog.md
do_not:
  - Implement tool swaps before Approve
  - delay E-HOT1 gate repair for stack theater
  - promote Sonar/Spec Kit/Nx to boolean or runtime SoT
spec_gate: DRAFT E-STACK0 (2026-08-09) — STACK1–STACK12 pending Approve
---

# Design memo: E-STACK0 Spec gate (stack rescope)

> **DRAFT — awaiting Approve of STACK1–STACK12.**
>
> Research: [`docs/research/process/22-stack-rescope-10k-star-bar-2026.md`](../research/process/22-stack-rescope-10k-star-bar-2026.md).

| Field | Value |
| --- | --- |
| Decisions | **STACK1–STACK12** pending |
| Bar | ≥10000★ for *new* external SoR; Confirmed pins Embody-continue |
| Order | E-HOT1 green → stack Spec → E-COH1; no tool rip in hotfix |

## Verdict

Keep ruff/pytest/ast-grep/semgrep/mkdocs. Keep coverage/tach-cycles/complexipy/CodeQL as Confirmed despite ★. Steal **Nx boundary patterns** for seam maps; re-base E-TACH0 off tach★. Refuse Spec Kit runtime, Sonar-as-floor, dual linters.

## Exit

On Approve: stamp APPROVED; backlog P19; amend E-TACH0 draft ★ justification in a follow-up docs commit (not depends_on Implement).
