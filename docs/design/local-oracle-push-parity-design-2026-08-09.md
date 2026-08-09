---
category: Local oracle push parity
status: APPROVED — SPEC GATE E-HOOK2 (2026-08-09)
research: docs/research/process/30-local-oracle-push-parity-2026.md
spec_gate: APPROVED E-HOOK2
---

# Design: local oracle Cover% on pre_pr

**HOOK2-1.** `oracle_push_policy.should_remesure_oracle(mode, changed_paths)` —
true for `full`/`actions_outage`, or `standard` when any path under
`src/doc_engine/`, `src/stf/`, or `tests/` changed; false when
`PRE_PR_SKIP_ORACLE=1`; force true when `PRE_PR_FORCE_ORACLE=1`.

**HOOK2-2.** When true, `pre_pr` hard suite `oracle_coverage` runs
`python -m doc_engine.ci.coverage_measure_cli` (default oracle floor) and
**omits** bare `pytest` (oracle already runs full `tests/`).

**HOOK2-3.** `in_repo_quality_gates` uses `skip_coverage=False` when
`coverage.xml` exists after the suite; else skip (docs-only).

**Refuse:** domain-select as floor proof; climb XML; lowering 98.7.
