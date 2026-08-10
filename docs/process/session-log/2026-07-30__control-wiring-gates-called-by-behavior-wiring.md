# Session log — 2026-07-30

Lead: **Control-wiring gates (called_by / behavior / wiring tests)**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 6. Newest at the bottom of this file.

---

## 2026-07-30 ? Control-wiring gates (called_by / behavior / wiring tests)



Commit: 8dfe156 (PR #64)



Tests: 107 passed (test_check_repo_claims + test_control_wiring + test_pipeline_runner); check_repo_claims OK



Assumptions affected:



- `CLAUDE.md` / check_repo_claims closed verify: vocabulary (five forms only) ? [Resolved ? seven forms: added `called_by:` + closed `behavior:<key>`; documents still cannot supply shell/pytest]



- Controls that sit one layer from where they bite ? [New info ? `tests/test_control_wiring.py` seeds already-true dual-emit/missing-output bites; Phase B stays separate]



Files touched: scripts/check_repo_claims.py, scripts/mutate.py, tests/test_check_repo_claims.py, tests/test_control_wiring.py, CLAUDE.md, claude/session-log.md, claude/research/adoption-blockers-queue-2026-07-30.md







## 2026-07-30 ? Stale-claims hygiene (B5 before Phase B)



Commit: stale-claims-hygiene (this PR)



Tests: kitchen-sink + drift + check_repo_claims (see PR)



Assumptions affected:



- `CONSTRAINTS.md` CI enumerates suites by hand / overlap still Flagged / ENFORCE=False in STATUS ? [Resolved ? corrected against `pytest tests/` + `carried_in_paths` + advisory llms coverage]



- Drift tier-2 documented as per-file ast-grep ? [Resolved ? docstring/README match full-scan-then-filter]



- Decision memo §5 ?no Phase 1 emitter until ask? ? [Resolved ? gate closed; dual-emit PR #63]



- Glean prior-art corpus stale ? [Still accurate as mechanism cite ? no star re-measure; post-dual-emit banner added]



- Ordinal claim keys churn C-missing baseline on every CONSTRAINTS edit ? [Resolved ? content-stable digest keys + refuse-revival tombstone for absent globs]



Files touched: scripts/check_repo_claims.py, scripts/repo_claims_baseline.json, tests/test_check_repo_claims.py, CLAUDE.md, CONSTRAINTS.md, STATUS.md, README.md, src/doc_engine/tools/spring_drift_check.py, tests/test_enterprise_kitchen_sink.py, claude/research/fact-store-phase1-decision-memo-2026-07-30.md, claude/research/fact-store-prior-art-corpus-2026-07-30.md, claude/research/fact-store-approaches-collation-2026-07-30.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/10-architecture-maturation-plan.md, claude/jpa-hibernate-predicate-vocabulary-survey.md, claude/session-log.md







## 2026-07-30







## 2026-07-30 ? Schema coverage research + facts closed contract (slice 1)



Commit: 065680a



Tests: 33 passed, 1 skipped (test_artifact_schemas + test_artifact_serde_matrix + test_facts_ledger); check_repo_claims OK



Assumptions affected:



- External review schema coverage residual ? [New info ? corpus+collation+REFINE memo; slice 1 closes facts ledger]



- deterministic-boundary note as sequencing SoT ? [Resolved ? superseded for order by schema-contracts-decision-memo]



- facts.jsonl prose-only contract ? [Resolved ? Fact forbid + facts.schema.json + JSONL validate]



Files touched: claude/research/schema-*.md, src/doc_engine/pipeline/artifacts.py, validation.py, scanning/facts.py, scripts/schemas/facts.schema.json, tests/test_artifact_*.py, claude/session-log.md







## 2026-07-30 ? Schema slices 2?4 + B4 Stage 5 wire



Commit: 065680a



Tests: 98 passed, 4 skipped (artifact schemas/serde + pipeline_stages + compliance); check_repo_claims OK



Assumptions affected:



- Schema memo slices 2?4 / review without gate bite ? [Resolved ? cert/edges/gaps/review registered+exported; run_stage5_gate validates architecture_testing_review (B4)]



- Adoption-blockers B4 open ? [Resolved ? Stage5ArchitectureTestingReviewGateTest]



Files touched: src/doc_engine/pipeline/artifacts.py, src/doc_engine/tools/pipeline_validators.py, src/doc_engine/tools/certification.py, scripts/schemas/*.schema.json, tests/test_artifact_schemas.py, tests/test_artifact_serde_matrix.py, tests/test_pipeline_stages.py, claude/research/*, claude/session-log.md







## 2026-07-30 ? scripts/ subdirectory layout



Commit: 065680a



Tests: 38 passed (live_gates + compliance) (check_repo_claims/check_code_quality baselines regenerated; targeted pytest next)



Assumptions affected:



- STATUS product vs meta scripts boundary ? [Still accurate ? product stays in doc_engine; meta nested under scripts/{ci,ratchets,coverage,fixtures,schemas}]



- Flat scripts/*.py invoke paths in CI/hooks/verify: ? [Resolved ? recursive path updates; no dual-home shims]



Files touched: scripts/** (layout), src/doc_engine/paths.py, tests/conftest.py, .github/workflows/*, adapters/claude/hooks/require_hardened_tests.py, CLAUDE.md, CONSTRAINTS.md, STATUS.md, steering verify predicates, scripts/README.md, claude/session-log.md







