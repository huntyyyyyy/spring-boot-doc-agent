# Session log — 2026-07-28

Lead: **Pipeline B+A close-out: contracts, validators, orchestrator, repo hygiene**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 5. Newest at the bottom of this file.

---

## 2026-07-28 ? Pipeline B+A close-out: contracts, validators, orchestrator, repo hygiene







Commit: 065680a



Tests: `pytest tests/test_artifact_schemas.py tests/test_pipeline_runner.py tests/test_pipeline_stages.py tests/test_prompt_contracts.py -q` passing; `python3 scripts/check_repo_claims.py` passing



Assumptions affected:



- `claude/steering-prompts/02-pluggability-research-prompt.md` ? inter-stage JSON artifacts "no schema, no validation" ? [Resolved ? Pydantic models in `src/doc_engine/pipeline/artifacts.py`, `scripts/schemas/*.schema.json`, `scripts/validate_artifacts.py`, SKILL.md data contracts section, `scripts/pipeline_validators.py`; `PipelineRunner` + `StageExecutor` in `src/doc_engine/pipeline/`; `run_pipeline_local.py` uses `PipelineRunner`. Residual: CI gates fixture `spring_signals` only, not live pipeline run artifacts.]



- `MATURITY_ASSESSMENT.md` schema scorecard row ? [Resolved ? upgraded to Partially resolved with pointer to validate_artifacts + residual CI gap.]



Files touched: claude/steering-prompts/02-pluggability-research-prompt.md, MATURITY_ASSESSMENT.md, hooks/require_hardened_tests.py, tests/test_prompt_contracts.py, README.md, .github/workflows/ci.yml, claude/session-log.md







---







## 2026-07-28 ? STATUS.md sync + run_pipeline_local artifact gates







Commit: 065680a



Tests: targeted B+A pytest suites passing; `check_repo_claims.py` OK



Assumptions affected:



- `STATUS.md` Pending section ? still listed prompt 02 schema work as not built ? [Resolved ? moved B+A to Done; updated Next concrete action.]



Files touched: STATUS.md, scripts/run_pipeline_local.py, claude/session-log.md







---







## 2026-07-28 ? deterministic-only local run, Windows ast-grep fix, legacy signals compat







Commit: 065680a



Tests: `test_scan_context_wiring.py` 6/6, `test_artifact_schemas.py` 8/8; `check_repo_claims.py` OK



Assumptions affected:



- `skills/document-spring-repo/SKILL.md` ? local E2E via `run_pipeline_local.py` always mocks Stages 1?4 ? [New info ? `--deterministic-only` and `--signals-file` skip generative stages and reuse prior `spring_signals.json`.]



Files touched: scripts/run_pipeline_local.py, src/doc_engine/scanning/_scanner_astgrep.py, src/doc_engine/pipeline/artifacts.py, scripts/schemas/spring_signals.schema.json, tests/test_scan_context_wiring.py, claude/session-log.md







---







## 2026-07-28 ? PR #53: restore ast-grep-cli pin; land pipeline on snapshot branch







Commit: 065680a (pushing with PR #53)



Tests: `ruff check scripts/` pass; `check_code_quality.py` OK after `--update`; `check_repo_claims.py` pending after prompt 08 verify flip



Assumptions affected:



- `claude/steering-prompts/08-dependency-pinning-task-prompt.md` ? claimed `ast-grep-cli` was removed from `requirements.txt` ? [Resolved ? pin restored (`ast-grep-cli~=0.45.0`); verify predicates flipped to `contains`.]



Files touched: requirements.txt, requirements-dev.txt, claude/steering-prompts/08-dependency-pinning-task-prompt.md, CONSTRAINTS.md, scripts/code_quality_baseline.json, scripts/test_*.py, scripts/spring_signal_scan.py, claude/session-log.md







---







## 2026-07-28 ? R3 pipeline in package (local_runner, validators, action dedup)







Commit: 065680a



Tests: 824 passed, 1 xfailed (intentional); `check_repo_claims.py` OK; `check_code_quality.py` OK



Assumptions affected:



- `claude/steering-prompts/02-pluggability-research-prompt.md` ? orchestration in scripts/run_pipeline_local ? [Resolved ? body moved to `src/doc_engine/pipeline/local_runner.py`; `local_run.py` imports package directly without scripts bootstrap.]



Files touched: src/doc_engine/pipeline/local_runner.py, src/doc_engine/pipeline/local_run.py, src/doc_engine/tools/pipeline_validators.py, scripts/run_pipeline_local.py, scripts/pipeline_validators.py, adapters/github/README.md, src/doc_engine/core/protocols.py, src/doc_engine/scanning/_scanner_base.py, src/doc_engine/pipeline/README.md, claude/session-log.md







---







