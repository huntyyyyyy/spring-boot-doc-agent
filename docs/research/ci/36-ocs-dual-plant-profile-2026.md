---
title: E-OCS0 — Dual plant (fixture merge SoT + OCS campaign profile)
status: APPROVED — SPEC GATE E-OCS0 (2026-08-10) — OCS1–OCS8
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine + spring-signals harness
related:
- spring-signals/docs/CAMPAIGN.md
- tests/TESTING.md
- docs/research/ci/17-codeql-signals-skip-fingerprint-2026.md
- docs/research/process/35-control-plane-closed-loop-2026.md
do_not:
- make Artifactory-required OCS DB the CI merge SoT
- dual-write a second assertion engine
- rewrite pytest domains / oracle Cover% for OCS
- pretend OCS green without checkout or credentials
spec_gate: APPROVED E-OCS0 (2026-08-10) — OCS1–OCS8
last_reviewed: '2026-08-10'
---

# Principal memo: OCS plant profile without Artifactory-as-CI

## 0. Verdict

| Question | Answer |
| --- | --- |
| Redo testing framework for OCS? | **Refuse.** |
| Make OCS CodeQL DB required in CI? | **Refuse** (Artifactory-gated; non-hermetic). |
| What to land? | Named **plant=fixture\|ocs** profile; fixture = merge SoR; OCS = campaign/opt-in. |
| Without Artifactory today? | Preflight fail-closed; offline **ast-grep floor remeasure** against local checkout when `DOC_ENGINE_REAL_REPO` is set; CodeQL DB create stays work-VPN only. |

## 1. Decisions (OCS1–OCS8)

| ID | Decision |
| --- | --- |
| **OCS1** | Fixture plant (`create-test-db.sh` + `fixture-repo.json`) remains the only CI/merge CodeQL evaluation SoR |
| **OCS2** | OCS plant uses same `check-assertions.py` engine + `ocs-api-service.json` — never a second SoR API |
| **OCS3** | `SPRING_SIGNALS_PLANT=fixture\|ocs` (default fixture); `run-plant.sh` is the unified entry |
| **OCS4** | OCS preflight requires resolvable checkout via `DOC_ENGINE_REAL_REPO` / `local-runs/real-repo.path` / `SPRING_SIGNALS_OCS_REPO` |
| **OCS5** | OCS `create-db` requires Artifactory env; without it exit non-zero with explicit reason — never soft-skip as green |
| **OCS6** | Offline floor remeasure (ast-grep) may propose expectation deltas without Artifactory; writing JSON is operator-reviewed |
| **OCS7** | CI `codeql-signals` stays fingerprint-gated fixture only; no required OCS job |
| **OCS8** | Refuse full test-framework / QL rewrite for one client tree |

## 2. CGQ3 Accept

| Concern | Remedy | Depth | Witness |
| --- | --- | --- | --- |
| OCS vs fixture conflation | single-write-derive (two expectation files) | CAMPAIGN dual plant | `plant_profile` tests |
| Artifactory absent → fake green | fail-closed preflight | create-db.sh precondition | `test_plant_profile.py` |
| Floor drift without VPN | characterization remeasure | OCS6 | `remeasure_ocs_floors.py` dry-run |

## 3. Exit

Implement E-OCS1 on this tip: profile + preflight + offline remeasure + docs.
Artifactory DB create remains operator-only on work network.
