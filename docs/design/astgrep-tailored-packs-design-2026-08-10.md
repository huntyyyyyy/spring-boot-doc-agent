---
title: Design stub — E-AST0 tailored ast-grep packs
status: DRAFT (awaits Spec Approve of docs/research/stage0/astgrep-tailored-packs-fixture-ocs-2026.md)
date: '2026-08-10'
claim_tiers: Unknown
related: []
last_reviewed: '2026-08-10'
---

# Design stub: fixture Stage-0 + OCS overlay + Python vacuity

## Intent

Three ast-grep packs, one engine (`ast-grep-cli~=0.45.0`):

1. **spring_stage0** — hermetic Stage-0 / `rule_coverage` fixtures  
2. **ocs_overlay** — campaign floors / offline remeasure (never merge SoT)  
3. **python_vacuity** — doc-engine fail-closed vacuity (hybrid with `vacuous` + telemetry)

Shared **YAML** utilities via `utilDirs` + `matches` (not a Python `utils/` package).

## Non-goals

- Artifactory OCS DB as CI merge SoT  
- Bare ripgrep as citation proof  
- In-tree Rust  

## Open product lock

**AST0-B:** hard-migrate Stage-0 ids to wave-1 vocabulary (B1) vs dual-emit adapter (B2).

## Impl order (after Approve)

1. Vacuity pack + `pre_pr` hard suite (can proceed under AST0-E even while B is open)  
2. `sgconfig` scaffold + utils  
3. Vocabulary B1/B2 tip  
4. OCS overlay + `remeasure_ocs_floors.py`  

## Witnesses

- Fixture: `scripts/fixtures/spring_signals/` + expectation JSON  
- OCS: `harness/expectations/ocs-api-service.json` (operator)  
- Vacuity: planted fixtures under `scripts/fixtures/vacuity/` + empty hard-log test  
