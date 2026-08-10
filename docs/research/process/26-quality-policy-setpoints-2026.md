---
title: Quality policy setpoints — central discoverability without god files
status: APPROVED — SPEC GATE E-KNOB0 (2026-08-09)
date: 2026-08-09
epic: E-KNOB0
claim_tiers: Evidenced / Confirmed / Unknown
related:
  - docs/design/quality-policy-setpoints-design-2026-08-09.md
  - docs/research/quality-backlog.md
  - .cursor/rules/se-quality-constitution.mdc
  - docs/design/concept-split-cohesion-design-2026-08-09.md
do_not:
  - dump all thresholds into quality_knobs.py / ci/utils.py
  - treat sensors (gap-average, stalker, adequacy) as fail_under owners
  - weaken 98.7 / complexipy ≤5 / LOC ≤225 while consolidating
---

# Process research: quality policy setpoints (E-KNOB0)

## 1. Question

Process and gate **knobs** (floors, ceilings, advisory bars) are tunable but
scattered. How do we give tip writers a **central place to discover and change
setpoints** without creating a god module that violates COH / constitution?

## 2. Claim inventory

| Claim | Tier | Note |
| --- | --- | --- |
| Constitution forbids `utils/` grab-bags and requires concept-named modules | Confirmed | `se-quality-constitution.mdc` |
| Cover% floor already has a concept owner (`coverage_artifact_policy.DEFAULT_FLOOR`) | Confirmed | tip inventory |
| `COMPLEXITY_MAX=5` and `98.7` are re-literal’d in multiple modules | Confirmed | `quality_gate_checks`, `complexipy_ratchet`, adequacy echo |
| A single `quality_knobs.py` would hit LOC≤225 / complexipy≤5 and conflate SoT vs sensor | Evidenced | constitution + COH1–COH4 |
| OCP prefers strategy/policy ports over if/elif gods | Evidenced | synthesis decisions; existing `MeasureStrategy` |

## 3. Alternatives

| Option | Embody / Adopt / Refuse |
| --- | --- |
| One mega `quality_knobs.py` owning every number | **Refuse** — god file; SoT/sensor conflation; blast radius |
| Doc-only table with no code owners | **Defer alone** — discoverable but drift-prone |
| **One setpoint owner per concern** + design registry table | **Embody** |
| Thin re-export façade of all knobs | **Refuse** as primary SoT — becomes private warehouse (COH) |
| External config YAML/JSON for all floors | **Refuse** v1 — second SoT next to pyproject/CI; weakening hazard |

## 4. Verdict

**Embody** concept-named `*_policy` modules (or keep ownership on an existing
concept module such as `size_ratchet`). **Adopt** a design memo as the human
registry (path → owner → mirror). **Refuse** mega-config and utils bags.
Non-Python mirrors (`pyproject.toml` `fail_under`, `COV_FAIL_UNDER`) stay
**declared mirrors** of `DEFAULT_FLOOR`, never independent SoT.

## 5. Spec gate

See [`docs/design/quality-policy-setpoints-design-2026-08-09.md`](../../design/quality-policy-setpoints-design-2026-08-09.md)
(**KNOB1–KNOB10**). Implement stream **E-KNOB1** (green slice) then return tip
to **E-COH1**.
