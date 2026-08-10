---
title: E-COH1 — Public-surface fitness for provisional façades (2026)
status: APPROVED — Spec delta for Active E-COH1 slice (2026-08-09)
date: '2026-08-09'
epic: E-COH1
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/design/concept-split-cohesion-design-2026-08-09.md
- docs/research/process/22-stack-rescope-10k-star-bar-2026.md
- docs/research/process/23-concern-to-solution-remedies-2026.md
- docs/research/process/24-codegen-quality-dimensions-mechanism-depth-2026.md
do_not:
- expand tach.toml depends_on/interfaces before E-TACH0 Approve + cycle-break
- treat LOC clearance as cohesion Accept
- re-introduce support/helpers/inventory_drift residual bins
last_reviewed: '2026-08-10'
---

# Process research: public-surface fitness (E-COH1 bite)

## 1. Problem (Confirmed)

MOD-S1 left **provisional** façades whose primary job is re-exporting private
`_` callables (`local_runner_phases.support`, `semantic_eval_helpers`, tool
façades). Size gates pass; COH2–COH4 do not. Without a **standing fitness
function**, reshape regresses on the next climb poke.

## 2. Modern landscape (2026-08-09)

| Approach | Surface | Stance here |
| --- | --- | --- |
| **tach `[[interfaces]]` expose** ([docs](https://docs.gauge.sh/usage/interfaces/)) | Confirmed pin `tach~=0.35`; ~2.8k★ | **Embody pattern**; **Defer** wiring into `tach.toml` until E-TACH0 Approve (cycles still block `depends_on`) |
| **Nx `enforce-module-boundaries` / tags** | ≥29k★ | **Adopt pattern only** — public vs deep import discipline |
| **Packwerk public API** | Ruby; ~1.9k★ | **Adopt pattern only** |
| **ArchUnit / fitness functions** (Ford) | Evidenced | **Embody** — continuous objective check of public-surface invariant |
| **import-linter contracts** | ≥1k★ | **Defer** dual-gate (LEG-S1 / COH11) |

## 3. Verdict

**Embody** architecture fitness for curated façades: `__all__` must not export
leading-`_` names; residual bin **path basenames** (`support`, `*_helpers`,
`inventory_drift`, `*_basic`) are forbidden under listed packages.

**Refuse** expanding tach interfaces this slice. **Adopt** characterization
migration of climb/patch-at-use callers onto concept modules (SOL5 + SOL2).

## 4. CGQ3 Accept (this slice)

| Concern | Remedy | Depth | Witness |
| --- | --- | --- | --- |
| maintainability / façade dual-write of import SoR | `fitness-function` (SOL2) + `characterization-net` (SOL5) | process/24 §2.1 structural fitness; §2.3 characterization | `tests/ci/test_public_surface_policy.py` + `check_public_surface` in `pre_pr` |
| residual bins (`support`, `helpers`, `inventory_drift`) | concept split (COH2–COH3) | process/24 §2.1 | path_absent ratchet in policy; packages import concept modules |

## 5. Seam map (before moves)

| Module | Responsibility | Allowed deps |
| --- | --- | --- |
| `runner_argv` | `py_mod` argv builder | stdlib |
| `artifact_inventory` | out-dir file inventory log | stdlib |
| `drift_check_phase` | optional spring_drift_check phase | `runner_argv` |
| `stage_recording` / `certification_finish` / `runner` / `runner_log` | unchanged concepts | existing |
| `tools.semantic_eval` | public CLI + public eval API | confirmed / mermaid / scan / paths |
| ~~`support.py`~~ / ~~`inventory_drift.py`~~ | **deleted** | — |
