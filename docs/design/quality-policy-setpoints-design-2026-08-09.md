---
category: Quality policy setpoints / central discoverability
status: APPROVED — SPEC GATE E-KNOB0 (2026-08-09) — merge Approve of KNOB1–KNOB10
date: '2026-08-09'
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/research/process/26-quality-policy-setpoints-2026.md
- docs/research/quality-backlog.md
- docs/design/concept-split-cohesion-design-2026-08-09.md
- src/doc_engine/ci/coverage_artifact_policy.py
do_not:
- create quality_knobs.py / ci/utils.py dumping all thresholds
- move sensor bars into Cover% SoT modules
- weaken fail_under / complexipy / LOC while consolidating
- treat pyproject or COV_FAIL_UNDER as independent SoT
spec_gate: APPROVED E-KNOB0 (2026-08-09) — KNOB1–KNOB10
title: 'Design memo: quality policy setpoints (no god file)'
last_reviewed: '2026-08-10'
---

# Design memo: quality policy setpoints (no god file)

> **APPROVED — SPEC GATE E-KNOB0 (2026-08-09)**
>
> Merge Approve of **KNOB1–KNOB10**. Tip writers discover knobs via this registry
> table; each number has **one concept owner**. Implement **E-KNOB1** green slice
> then return Active tip to **E-COH1**.

## 1. Problem

Gate and process knobs (Cover% floor, complexipy max, LOC hard/soft, jscpd %,
workflow LOC, stalker tip count) live in many modules. Tip writers either
re-literal thresholds or invent a mega-config — both fail constitution / COH.

## 2. One-page verdict

| Question | Answer |
| --- | --- |
| Central place? | **This design registry** + concept `*_policy` (or existing concept) owners |
| One Python dump of all knobs? | **Refuse** |
| Where to change 98.7? | `coverage_artifact_policy.DEFAULT_FLOOR` (mirrors: pyproject, CI env) |
| Where to change complexipy ≤5? | `complexity_policy.COMPLEXITY_MAX` |
| Sensors own floors? | **No** — they import / echo only |

## 3. Registry (human SoT for discoverability)

| Knob | Owner module | Role | Mirrors / consumers |
| --- | --- | --- | --- |
| Cover% floor `98.7` | `coverage_artifact_policy.DEFAULT_FLOOR` | Oracle SoT constant | `pyproject` fail_under; `COV_FAIL_UNDER`; diff-cover / gap-average argv; adequacy echo |
| Climb XML names | `coverage_artifact_policy` | Policy 16-A | measure modes, gap refuse |
| Complexity max `5` | `complexity_policy.COMPLEXITY_MAX` | Hard gate + ratchet | `quality_gate_checks`, `complexipy_ratchet` |
| Complexity baseline path | `complexity_policy.DEFAULT_BASELINE` | Ratchet SoR path | gate + ratchet CLI |
| Package roots (gates) | `package_scope.PACKAGE_ROOTS` | Scope for Python gates | complexity, duplication, size measure |
| Duplication % / min-lines | `duplication_policy` | jscpd hard gate | `gate_duplication` |
| File LOC / fn stmts | `size_ratchet` (existing) | Size policy | size measure; soft advisories |
| Workflow YAML LOC | `workflow_size` (existing) | CI YAML bars | workflow checks |
| Active tip count `1` | `stalker_sensors.parallel_tip` | Process sensor | backlog G5 |
| Hard vs advisory suites | `pre_pr` (extract later) | Local verify catalog | E-COH / later KNOB |

## 4. Locked decisions (KNOB1–KNOB10)

| ID | Decision |
| --- | --- |
| KNOB1 | One setpoint owner per concern; consumers import, never re-literal SoT numbers |
| KNOB2 | Design registry table is the **discoverability** hub — not a code mega-module |
| KNOB3 | **Refuse** `quality_knobs.py`, `ci/utils.py`, and re-export warehouses of private helpers |
| KNOB4 | Cover% SoT remains `DEFAULT_FLOOR`; sensors may echo `str(DEFAULT_FLOOR)` only |
| KNOB5 | `pyproject` / `COV_FAIL_UNDER` are **mirrors** — must match `DEFAULT_FLOOR`; never weaken via mirror alone |
| KNOB6 | Complexity SoT is `complexity_policy`; delete duplicate `COMPLEXITY_MAX=5` literals |
| KNOB7 | Duplication SoT is `duplication_policy`; gate strategies stay in `quality_gate_checks` |
| KNOB8 | Size SoT stays on `size_ratchet` until that module needs a cohesive split (≤225) |
| KNOB9 | E-KNOB1 green slice: wire floor + complexity + duplication + package_scope; tests assert shared owners |
| KNOB10 | After E-KNOB1 Done, Active tip returns to **E-COH1** (no Spec pile-up) |

## 5. CGQ3 Accept (E-KNOB1)

| Concern | Remedy id | Depth cite | Witness |
| --- | --- | --- | --- |
| Drifted / duplicated floors | KNOB1 + KNOB4–KNOB6 | process/26 §3–4; process/24 §2 Accept shape | `ast-grep` single def of `COMPLEXITY_MAX`; tests import owners |
| God-file temptation | KNOB2 + KNOB3 | COH2–COH4; constitution no utils | No `quality_knobs.py`; modules ≤225 / complexipy ≤5 |
| SoT vs sensor conflation | KNOB4 | constitution dual-mode / 16-A | adequacy imports floor echo; never asserts fail_under |

## 6. Out of scope (Defer)

- Extracting `pre_pr` suite catalogs into `pre_pr_suites` (still oversized façade)
- Auto-sync rewriting `pyproject.toml` from Python (mirror check test only)
- New stalker G7 for literal drift (optional later; unit test suffices for KNOB9)
