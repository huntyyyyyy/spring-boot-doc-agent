---
title: OCS dual-plant profile — Spec (E-OCS0)
status: APPROVED — SPEC GATE E-OCS0 (2026-08-10)
date: '2026-08-10'
epic: E-OCS0
research: docs/research/ci/36-ocs-dual-plant-profile-2026.md
claim_tiers: Unknown
related: []
last_reviewed: '2026-08-10'
---

# Design Spec: dual plant (fixture + OCS)

Approve **OCS1–OCS8**. Implement under E-OCS1:

1. `spring-signals/harness/plant_profile.py` — resolve plant + preflight
2. `spring-signals/harness/run-plant.sh` — fixture → `create-test-db.sh`; ocs → preflight then create-db+run
3. `scripts/ci/remeasure_ocs_floors.py` — ast-grep floors from `DOC_ENGINE_REAL_REPO` (no Artifactory)
4. Docs: `tests/TESTING.md`, `spring-signals/README.md`, quality-backlog

CI unchanged: fixture only.
