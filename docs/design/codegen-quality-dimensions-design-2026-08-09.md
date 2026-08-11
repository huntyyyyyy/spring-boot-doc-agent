---
category: Codegen-quality dimensions + remedy-mechanism depth
status: APPROVED E-CGQ0 (2026-08-09) — CGQ1–CGQ10
date: '2026-08-09'
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/research/process/24-codegen-quality-dimensions-mechanism-depth-2026.md
- docs/research/process/23-concern-to-solution-remedies-2026.md
- docs/design/ddia-north-star/meta/effective-remedies.md
- docs/research/quality-backlog.md
do_not:
- Accept Specs that only cite DDIA page ids or bare remedy labels
- treat Cover% or LLM-judge as generation proof
- Implement E-GND1 before E-STK1 green cycle
spec_gate: APPROVED E-CGQ0 (2026-08-09) — CGQ1–CGQ10
title: 'Design memo: E-CGQ0 Spec gate'
last_reviewed: '2026-08-10'
---

# Design memo: E-CGQ0 Spec gate

> **APPROVED E-CGQ0 (2026-08-09).**
>
> Research: [`docs/research/process/24-codegen-quality-dimensions-mechanism-depth-2026.md`](../research/process/24-codegen-quality-dimensions-mechanism-depth-2026.md).
>
> Velocity note: tip-grounding MCP (**E-GND0**) demoted; CGQ4/CGQ5 use process + existing tools until after E-STK1.

| Field | Value |
| --- | --- |
| Problem | Remedy/DDIA labels + post-hoc CI are too vague a start for agent codegen |
| Fix | Mechanism depth rows; Spec Accept Concern→Remedy→Depth→Witness; process probe/Verify |
| Downstream | E-STK1 Active; E-COH1 paused; E-GND1 Deferred |

## Decisions (Approved)

| ID | Decision |
| --- | --- |
| **CGQ1** | Pre-generation controls first-class; post-hoc CI necessary≠sufficient |
| **CGQ2** | Depth rows before Embody of new fitness / ETL / characterization |
| **CGQ3** | Accept: Concern → Remedy → Depth cite → Witness → Explicit Defer |
| **CGQ4** | Structural grounding probe required for design-shaped Impl (process/tools until E-GND) |
| **CGQ5** | Independent Verify vs Spec; LLM-judge ≠ SoT |
| **CGQ6** | E-SOL0 remedies catalog = vocabulary until depth cite |
| **CGQ7** | E-COH1 / E-STK1 Active only with CGQ3 Accept rows |
| **CGQ8** | Refuse Spec Kit runtime / Sonar·LLM floors / dual linters / ceiling raises |
| **CGQ9** | ≥10k★ bar; Confirmed vehicles host mechanisms |
| **CGQ10** | Design-shaped research memos need depth subsections or Explicit Defer |

## Exit

Stamp complete. Next tip: **E-STK1**. Do not start E-GND1 until E-STK1 green.
