# Session log — 2026-07-29

Lead: **CI workflow YAML parse gate; next arc = fact-store Phase 1**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 5. Newest at the bottom of this file.

---

## 2026-07-29 ? CI workflow YAML parse gate; next arc = fact-store Phase 1



Commit: 065680a



Tests: test_check_workflow_yaml.py 3/3; check_workflow_yaml.py OK on committed workflows



Assumptions affected:



- CI workflow validity ? [Resolved ? scripts/check_workflow_yaml.py + CI step; closes PR #57 unquoted-colon class]



- Packaging arc next step ? [New info ? STATUS locks next engineering investment as fact-store Phase 1; packaging paused]



Files touched: scripts/check_workflow_yaml.py, tests/test_check_workflow_yaml.py, requirements-dev.txt, .github/workflows/ci.yml, STATUS.md, claude/session-log.md







## 2026-07-29 ? Delete product scripts/ shims; one invoke surface



Commit: 065680a



Tests: pytest tests/ (excl. kitchen-sink/real-world) 770 passed, 24 skipped; check_repo_claims OK; check_code_quality OK; rule_coverage OK



Assumptions affected:



- docs/product-architecture.md / STATUS ? dual-home thin scripts/ product aliases until organic zero-use ? [Resolved ? product tools invoke only via python -m doc_engine.tools.* / doc-engine; 25 thin scripts/ product shims deleted; meta CI stays under scripts/]



- claude/steering-prompts/02-pluggability-research-prompt.md ? path_exists scripts/validate_artifacts.py / pipeline_validators.py ? [Resolved ? verify: retargeted to src/doc_engine/tools/]



- claude/steering-prompts/03-constraints-research-prompt.md ? path_exists scripts/spring_drift_check.py ? [Resolved ? verify: retargeted to src/doc_engine/tools/spring_drift_check.py]



- claude/steering-prompts/04-analytics-logging-research-prompt.md ? path_exists scripts/run_manifest.py ? [Resolved ? verify: retargeted to src/doc_engine/tools/run_manifest.py]



- claude/steering-prompts/06-wiredrift-check-task-prompt.md ? contains spring_drift_check.py string forms ? [Still accurate ? verify already cites doc_engine.tools.spring_drift_check]



Files touched: scripts/ (product shims deleted), src/doc_engine/tools/*, tests/*, .github/workflows/ci.yml, docs-site.yml, STATUS.md, CONSTRAINTS.md, README.md, MATURITY_ASSESSMENT.md, docs/product-architecture.md, skills/*, adapters/claude/skills/*, adapters/claude/hooks/require_hardened_tests.py, claude/steering-prompts/02-04+06, claude/session-log.md







## 2026-07-29 ? Drop scripts/test_*.py wrappers; remove .vs and baseline-reference



Commit: 065680a



Tests: check_repo_claims + require_hardened + targeted pytest (see session)



Assumptions affected:



- claude/steering-prompts/01-testability-research-prompt.md ? path_exists scripts/test_pipeline_stages.py ? [Resolved ? verify: path_exists:tests/test_pipeline_stages.py; wrappers deleted]



- claude/steering-prompts/14-software-architect-and-testing-agent-prompt.md ? path_exists scripts/test_semgrep_rule_coverage.py ? [Resolved ? verify: path_exists:tests/test_semgrep_rule_coverage.py]



- STATUS/README ? run suites via scripts/test_*.py ? [Resolved ? pytest tests/; CI already discovery-based]



- baseline-reference/ as live Step 0 ? [Resolved ? deleted; IMPLEMENTATION_HANDOFF Step 0 marked historical; git history is the archive]



- Accidental .vs/ in git ? [Resolved ? removed; .vs/ gitignored]



Files touched: scripts/test_*.py (deleted), .vs/ (deleted), baseline-reference/ (deleted), .gitignore, IMPLEMENTATION_HANDOFF.md, STATUS.md, README.md, CONSTRAINTS.md, MATURITY_ASSESSMENT.md, skills/*, adapters/claude/skills/*, adapters/claude/hooks/require_hardened_tests.py, scripts/check_repo_claims.py, tests/*, claude/steering-prompts/01+14, claude/session-log.md







## 2026-07-29 ? Suite layout SoT (pyproject testpaths); no legacy suite paths



Commit: 065680a



Tests: test_suite_layout + test_require_hardened_tests + test_check_repo_claims 122 passed; check_repo_claims OK



Assumptions affected:



- Suite root dual-home via ci.yml "pytest tests/" sniff ? [Resolved ? scripts/suite_layout.py reads pyproject testpaths; Check D refuses scripts/test_*.py revival]



- Legacy scripts/test_* as valid suites in hooks/claims ? [Resolved ? deleted; no dual-path acceptance]



- Pydantic/SPI fold into hygiene ? [Still accurate deferred ? STATUS sequencing lock; research note claude/deterministic-boundary-schemas-spi-research-2026-07-29.md]



Files touched: scripts/suite_layout.py, scripts/check_repo_claims.py, adapters/claude/hooks/require_hardened_tests.py, tests/test_suite_layout.py, tests/test_check_repo_claims.py, tests/test_require_hardened_tests.py, STATUS.md, claude/deterministic-boundary-schemas-spi-research-2026-07-29.md, claude/session-log.md







## 2026-07-29 ? Mutate harness resolves suites under tests/ (PR #60 CI)



Commit: 4e66634



Tests: 23/23 test_mutate.py passed; CI green then merge



Assumptions affected:



- mutate.py expected_caught_by under scripts/ ? [Resolved ? resolve via suite_layout + pytest; false "killed" when suite path missing]



Files touched: scripts/mutate.py, tests/test_mutate.py, claude/session-log.md







