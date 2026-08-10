# Session log — 2026-08-08 → 2026-08-10

Lead: **Size ratchet includes tests/; cohesive test modularization ≤225**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 25. Newest at the bottom of this file.

---

## 2026-08-08 — Size ratchet includes tests/; cohesive test modularization ≤225
Commit: 229e517
Tests: size-ratchet exit 0 (0 test file offenders; 38 src legacy baselined); focused pytest 27/27 (size_ratchet + climb covering/query/build_cmd + support)
Assumptions affected:
- `claude/steering-prompts/13-code-quality-research-prompt.md` — size ceilings / package roots — [New info — FILE_LOC_HARD 225; SIZE_ROOTS now src/doc_engine + src/stf + tests/; CONTRIBUTING cohesion bar applies to tests]
Files touched: CONTRIBUTING.md, CONSTRAINTS.md, scripts/ci/check_code_quality.py, scripts/ratchets/size_baseline.json, scripts/ratchets/code_quality_baseline.json, src/doc_engine/ci/size_*, src/doc_engine/cli*, src/doc_engine/scanning/support/_codeql_*, tests/** modularization, tests/support/**


## 2026-08-09 — E-CI: thin ci.yml + reusable BC workflows + LOC/heredoc SoT
Commit: 6a56818
Tests: check_workflow_yaml OK (LOC/heredoc green); verify_tool_pins OK; pytest tests/ci workflow/size/summary/pins 23/23; check_repo_claims OK; check_code_quality OK; emit_abi_matrix OK
Assumptions affected:
- `claude/steering-prompts/08-dependency-pinning-task-prompt.md` — CI installs/verifies pins via `ci.yml` — [Resolved — install in `.github/actions/setup-python-repo`; pin verify in `python-gates.yml` via `scripts/ci/verify_tool_pins.py`; verify predicates retargeted]
- `claude/steering-prompts/14-software-architect-and-testing-agent-prompt.md` — `semgrep_rule_coverage.py` wired in `ci.yml` — [Resolved — step lives in `python-gates.yml`; verify predicate retargeted]
- `CONSTRAINTS.md` Integration item 2 / Runtime item 4 / Known precision item 10 — gate strings in `ci.yml` — [Resolved — prose + verify HTML comments point at `python-gates.yml` / setup action under policy C-A]
Files touched: .github/workflows/{ci,python-gates,codeql-signals,quality-gates,sonar}.yml, scripts/ci/{verify_tool_pins,coverage_run_summary,check_workflow_yaml}.py, src/doc_engine/ci/workflow_size.py, tests/ci/test_*, CONTRIBUTING.md, CONSTRAINTS.md, docs/research/{07-ci-workflow-modularity,quality-backlog}.md, docs/design/ci-workflow-modularity-design-2026-08-09.md, claude/steering-prompts/{08,14}-*.md, claude/session-log.md


## 2026-08-09 — Fix CI: continue-on-error invalid on reusable-workflow caller
Commit: 88c0653
Tests: check_workflow_yaml OK; check_code_quality OK; pytest tests/ci workflow_size + check_workflow_yaml 17/17
Assumptions affected:
- E-CI sonar soft job — `continue-on-error` on `ci.yml` caller — [Resolved — moved onto `sonar.yml` called job; Actions rejects caller-level continue-on-error with 0-job failure]
- `check_workflow_yaml` / `workflow_size` — LOC/heredoc only — [New info — hard-fails continue-on-error on reusable-workflow caller jobs]
Files touched: .github/workflows/{ci,sonar}.yml, src/doc_engine/ci/workflow_size.py, scripts/ci/check_workflow_yaml.py, tests/ci/test_workflow_size.py, CONTRIBUTING.md, claude/session-log.md

## 2026-08-09 — E-RUN1: suite-stalking sensors (D1/D2/D17) on oracle cell
Commit: 641887a
Tests: pytest tests/ci/test_suite_timing*.py 8/8; ruff OK; check_repo_claims OK; check_workflow_yaml OK; check_code_quality OK; complexipy ≤5 on suite_timing; oracle argv still fail_under=98.7
Assumptions affected:
- `claude/steering-prompts/08-dependency-pinning-task-prompt.md` — python-gates owns cov cell — [Still accurate — added `--junitxml` + `suite_timing_summary.py` sensor only; fail_under argv untouched]
- E-CI C3 / coverage_run_summary pattern — [New info — sibling façade `scripts/ci/suite_timing_summary.py` over `doc_engine.ci.suite_timing`; D17 cascade when coverage.xml missing]
Files touched: src/doc_engine/ci/suite_timing/*, scripts/ci/suite_timing_summary.py, tests/ci/test_suite_timing*.py, .github/workflows/python-gates.yml, docs/research/{08,quality-backlog}.md, docs/design/suite-stalking-sensors-design-2026-08-09.md, claude/session-log.md

## 2026-08-09 — Oracle tip: pytest green blockers + size splits
Commit: 947de95
Tests: pipeline_runner_stages 5/5; domain_marker_cli + suite_timing 20/20; kitchen_sink ch12 9/9; lineage 20/20; size-ratchet exit 0; domain markers OK
Assumptions affected:
- `docs/research/pr-94-followup-oracle-stabilize.md` — green 3.11 goal — [New info — tip 3.11 completed: 1 FAIL real_repo missing --allow-mock; 5 ERROR missing @pytest.fixture; Cover% 93%; size offenders split]
Files touched: tests/doc_engine/test_kitchen_sink_*, test_pipeline_runner_stages.py, test_spring_signal_scan_*, tests/ci/test_domain_marker_cli_coverage.py, CONSTRAINTS.md, claude/session-log.md

## 2026-08-09 — E-QA1/E-QA2: adequacy sensors + climb Q2 witness checklist
Commit: 6602087
Tests: pytest tests/ci/test_adequacy_*.py 16/16; ruff OK; complexipy ≤5 on adequacy; size-ratchet exit 0; check_repo_claims OK; check_workflow_yaml OK; oracle argv still fail_under=98.7
Assumptions affected:
- E-QA0 design / P8.1–P8.2 Active — [Resolved — `doc_engine.ci.adequacy` + `adequacy_summary.py` wired in python-gates always-summary; CONTRIBUTING Climb Archive Q2; backlog P8.1/P8.2 Done]
- `claude/steering-prompts/08-dependency-pinning-task-prompt.md` — python-gates owns cov cell — [Still accurate — adequacy sensor only; fail_under argv untouched]
- Cover% / ENFORCE=False honesty — [Still accurate — sensors echo ENFORCE + floor text; no suite-wide ENFORCE=True]
Files touched: src/doc_engine/ci/adequacy/*, scripts/ci/adequacy_summary.py, tests/ci/test_adequacy_*.py, .github/workflows/python-gates.yml, CONTRIBUTING.md, docs/research/quality-backlog.md, claude/session-log.md

## 2026-08-09 — Kitchen-sink correctness: restore real-repo opt-in skip
Commit: 2fccac6
Tests: kitchen-sink focused 31 passed / 9 skipped (real_repo); domain markers OK; check_repo_claims OK
Assumptions affected:
- RealEnterpriseRepoTest opt-in hermetic skip — [Resolved — restored skipUnless; forbid cwd fallback; domain_live_optin classifier; --allow-mock only on configured Spring tree]
- CONSTRAINTS.md §8 gitignored write blind — [Resolved — product already fixed; claim + verify predicates retargeted to list_ignored_untracked + ch12 fail-path]
- NestedEntity plant "characterized by the test" — [New info — pinned scavenger quirk: NestedEntityHolder maps to nested_inner today]
Files touched: tests/doc_engine/test_kitchen_sink_*, src/doc_engine/ci/test_domain_rules.py, CONSTRAINTS.md, deleted test_enterprise_kitchen_sink.py

## 2026-08-09 — Cover% climb batch B4: tools drift/manifest
Commit: 5a8a129
Tests: 29/29 climb B4 suites passing; scoped cover spring_drift_tier2 100% / spring_drift_check 100% / run_manifest 97% stmt
Assumptions affected:
- E-QA2 Climb Archive Q2 — [New info — B4 archives `mutmut_slice` for `doc_engine.tools` drift/manifest (not Arm-1; not scan formatting)]
- Cover% climb high-miss tools inventory — [Resolved — hermetic `domain_climb_sensor` suites close tier2/check/manifest gaps]
Files touched: tests/doc_engine/test_coverage_climb_drift_tier2_recheck.py, test_coverage_climb_drift_check_{process,load}.py, test_coverage_climb_run_manifest_{core,cli}.py, CONTRIBUTING.md, claude/session-log.md

## 2026-08-09 — Cover% climb batch B5: Stage-0 scan CodeQL/gap/recall
Commit: 1a9c3a0
Tests: 21/21 climb B5 suites passing; LOC≤225 complexipy≤5; climb sensor cache/runner/recall/collision 100%
Assumptions affected:
- E-QA2 Climb Archive Q2 — [New info — B5 archives metamorphic Arm-1 (`tests/ratchets/test_metamorphic_formatting.py` + churn / `HarnessIsNotVacuousTest`) for Stage-0 scan surfaces]
- Cover% climb scan-related below-floor inventory — [Resolved — hermetic `domain_climb_sensor` suites close `_codeql_*`, `recall_delta`, `gap_probe/{join,symbol_collision}`, residual `symbol`/`facts` gaps]
Files touched: tests/doc_engine/test_coverage_climb_b5_{codeql_cache,codeql_db,codeql_runner_facade,gap_recall,symbol_facts}.py, CONTRIBUTING.md, claude/session-log.md

## 2026-08-09 — Cover% climb B5 follow-up: LOC split + runner main
Commit: 2c30c12
Tests: 21/21 climb B5; complexipy≤5; LOC≤225
Assumptions affected:
- E-QA2 Climb Archive Q2 — [Still accurate — Arm-1 witness unchanged]
Files touched: tests/doc_engine/test_coverage_climb_b5_codeql_{db,runner_facade}.py (deleted codeql_db_runner), claude/session-log.md

## 2026-08-09 — Oracle Cover% closed to 99.04 (fail_under 98.7)
Commit: 625e03e
Tests: oracle remesure whole_repo_cover=99.04% (exit 0 on climb branch remesure); kitchen-sink real-repo opt-in restored earlier
Assumptions affected:
- Active tip oracle stabilize to 98.7 — [Resolved — tip Cover% 99.04 after B1–B9 climb + kitchen-sink correctness; fail_under argv untouched]
- E-QA2 Climb Archive Q2 — [Still accurate — climb modules carry mutmut_slice / Arm-1 witnesses; gap-average alone not treated as proof]
Files touched: tests/doc_engine/test_coverage_climb_b{7,8,9}_*, tests/ci/test_coverage_climb_*, tests/doc_engine/test_kitchen_sink_*, CONSTRAINTS.md, test_domain_rules.py

## 2026-08-09 — Debug chapter+CodeQL after rescope: cache-key fail-closed + climb hygiene
Commit: 492a7c7
Tests: codeql invalidation+hygiene+climb 40/40; ch10 10/10; domain markers OK; check_repo_claims OK
Assumptions affected:
- CodeQL cache keys after module split — [Resolved — incomplete ScanContext no longer hashes to empty digest; discriminative invalidation tests; climb CodeQL F401 wallpaper cleaned]
- Kitchen-sink chapter vs CodeQL — [Still accurate — chain pinned filesystem,ast-grep; ch10 asserts codeql absent from covering receipts]
Files touched: _codeql_cache_keys.py, test_codeql_cache_key_invalidation.py, kitchen_sink chain/ch10, climb codeql ruff hygiene, code_quality_baseline.json


## 2026-08-09 — E-MOD2 Stage-0 tool façades (capacity / drift / partition)
Commit: 62e5e06
Tests: capacity/drift/partition characterization + kitchen ch01–03 + mock strategy — 127 passed (scoped); complexipy 0 offenders; size baseline ratcheted to 32 file offenders
Assumptions affected:
- `claude/steering-prompts/04-analytics-logging-research-prompt.md` — "`spring_drift_check.py` gained optional `--manifest`" — [New info — `--manifest` CLI flag now lives in `spring_drift_cli.py`; façade `spring_drift_check` re-exports `main`; verify predicate updated]
- `CONSTRAINTS.md` Integration gaps item 3 / Known precision item 6 — path needles for `--manifest` / partition overlap comments — [Resolved — verify paths retargeted to `spring_drift_cli.py` / `partition_repo_groups.py` after vertical split]
Files touched: CONSTRAINTS.md, claude/steering-prompts/04-analytics-logging-research-prompt.md, src/doc_engine/tools/capacity_preflight*.py, spring_drift_*.py, partition_repo*.py, scripts/ratchets/size_baseline.json, docs/research/12-*, quality-backlog.md

## 2026-08-09 — E-MOD3 tools wave 2 (run_manifest / citation_coverage)
Commit: 0368487
Tests: climb run_manifest + citation + live_gates citations + ports + ci run_manifest suites passing (scoped); complexipy 0; size baseline ratcheted (file offenders 30)
Assumptions affected:
- `claude/steering-prompts/04-analytics-logging-research-prompt.md` — "`path_exists:src/doc_engine/tools/run_manifest.py`" — [Still accurate — thin façade path retained; concept modules `run_manifest_*` hold io/stages/finalize/cli]
- E-MOD2 Stage-0 tool façades playbook — [New info — same façade + Protocol + late-import DIP applied to analytics `run_manifest` and `citation_coverage`]
Files touched: docs/research/13-tools-wave2-modularity-2026.md, docs/research/12-*, quality-backlog.md, src/doc_engine/tools/run_manifest*.py, citation_coverage*.py, tests/doc_engine/test_tools_wave2_ports.py, scripts/ratchets/size_baseline.json, claude/session-log.md

## 2026-08-09 — Debug E-MOD3 CI: façade json DIP + domain markers + pre_pr gap
Commit: 7183f01
Tests: kitchen Ch07 atomic write + climb run_manifest + ports + markers + pre_pr suites green; full ruff green
Assumptions affected:
- Local pre-push mirrors CI hard gates — [New info — `pre_pr` standard now includes `test_domain_markers`; AGENTS.md requires `--auto` before push; tool-quirks documents scoped-pytest false green]
- E-MOD3 thin façade monkeypatch surface — [Resolved — re-export `json` for kitchen Ch07 `patch.object(run_manifest.json, "dump")`]
Files touched: run_manifest.py / run_manifest_io.py, test_pipeline_tools_wave2_ports.py, scripts/ci/pre_pr.py, tests/ci/test_pre_pr_classify_bypass.py, AGENTS.md, claude/tool-quirks.md, session-log

## 2026-08-09 — E-FAC0/E-RES0: façade poke gate + design-research hook
Commit: b93921b
Tests: facade poke + design-research hook + pre_pr BuildSuites + markers + full ruff green
Assumptions affected:
- Research-before-design was skill-only — [Resolved — `require_design_research` commit hook + memo 14 RES1–RES3; Spec needs arXiv+GitHub URLs]
- God-file split characterization inventory — [Resolved — `check_facade_poke_surface` wired into pre_pr standard + python-gates]
Files touched: docs/research/14-*, quality-backlog, scripts/ci/check_facade_poke_surface.py, pre_pr.py, python-gates.yml, adapters/claude/hooks/*, .claude/settings.json, AGENTS.md, tests/ci/test_facade_poke_and_design_research.py

## 2026-08-09 — E-SCAN1 AstGrepBackend → scanning/astgrep/
Commit: b2a6a23
Tests: 20/20 structure+basic+chunk+destructive+climb edges; claims OK; poke OK; complexipy ≤5; size baseline 30 file offenders (astgrep+spring off hard list)
Assumptions affected:
- `docs/research/16-scan1-astgrep-modularity-2026.md` SCAN1-A–J — [Resolved — package + façade + structure tests + LEG8 monkeypatch + AstGrepRunner landed]
- `CONSTRAINTS.md` item 14 inventory/chunk needles — [Resolved — verify paths include `scanning/astgrep/argv.py`; behavior predicate still on façade `_run_ast_grep`]
- Size ratchet `_scanner_astgrep.py` 514 LOC offender — [Resolved — thin façade ≤225; concept modules under `scanning/astgrep/`]
Files touched: src/doc_engine/scanning/astgrep/*, _scanner_astgrep.py, spring.py, scripts/ci/check_facade_poke_surface.py, scripts/ratchets/size_baseline.json, CONSTRAINTS.md, tests/doc_engine/test_scan_context_astgrep_*, test_covering_hard_stops_destructive.py, docs/research/quality-backlog.md, claude/session-log.md

## 2026-08-09 — E-DOC1 research taxonomy + claude→docs + look-first hooks
Commit: 887b8ed
Tests: claims OK; look-first + claims fixture suites 123 passed; complexipy ≤5 on hooks
Assumptions affected:
- `docs/process/steering-prompts/` live under `claude/` — [Resolved — migrated to `docs/process/steering-prompts/`; claims MIRRORED_PROMPT_GLOB + CLAIM_CORPORA retargeted]
- Research look-first was soft skill only — [Resolved — `.cursor/hooks.json` inject + Read receipt + fail-closed design writes; `docs/research/README.md` domain map]
- `claude/` as process SoR — [Resolved — tombstone + archive under `docs/research/archive/claude-lore/`; adapter packaging kept]
Files touched: docs/research/**, docs/process/**, .cursor/hooks*, scripts/ci/check_repo_claims.py, check_llms_coverage.py, CONTRIBUTING.md, STATUS.md, tests/ci/test_research_map_look_first.py, claude/README.md

## 2026-08-09 — E-COH1 public-surface fitness + residual-bin reshape
Commit: 36bd64b6
Tests: 131 focused passed; complexipy 0 offenders; claims OK; public_surface hard in pre_pr
Assumptions affected:
- MOD-S1 provisional façades may re-export private `_` indefinitely — [Resolved — `check_public_surface` hard in `pre_pr`; `support.py`/`inventory_drift.py` deleted; `semantic_eval` public façade]
- Cohesion Accept was LOC-only — [Still accurate bar; [New info — CGQ3 Accept + fitness witness for public `__all__`]]
Files touched: public_surface_policy.py, check_public_surface.py, pre_pr.py, local_runner_phases/*, semantic_eval*.py, tests/ci/test_public_surface_policy.py, modularity/21-*, concept-split design appendix, quality-backlog, session-log

## 2026-08-09 — E-HOOK2/E-CQL1/E-TEL2: local oracle + CodeQL fingerprint + path parity
Commit: a1314d17
Tests: 34 focused ci passed; complexipy 0; claims OK
Assumptions affected:
- HOOK6 local push skips Cover% oracle — [Resolved — `oracle_coverage` hard remesure when src/tests change; quality-gates reads coverage.xml]
- CodeQL signals always wipe+rebuild — [Resolved — fingerprint gate skips compile/runtime when corpus unchanged; wipe remains on dirty path]
- Stalker only G1–G7 tip hygiene — [New info — G8–G10 path-parity sensors for oracle/CodeQL/suite map]
Files touched: oracle_push_policy.py, pre_pr.py, codeql_signals_change_gate.py, codeql-signals.yml, stalker_path_parity/*, process/30–31, quality-backlog, session-log

## 2026-08-09 — E-SEARCH0: allow ripgrep / Grep; keep network deny + ast-grep prefer
Commit: 4ca8b551
Tests: adapters deny_text_search + bridge + check F suites (pending run in same commit)
Assumptions affected:
- `CLAUDE.md` / `CONSTRAINTS.md` §10 / `adapters/claude/SEARCH.md` — hard "never text search" / Grep denied — [Resolved — text search allowed; prefer ast-grep for structural citations; check F network half unchanged]
- `docs/process/steering-prompts/` — no status field assumed Grep deny as deliverable absent — [Still accurate]
Files touched: adapters/claude/hooks/deny_text_search.py, .claude/settings.json, scripts/ci/check_repo_claims.py, CLAUDE.md, AGENTS.md, CONSTRAINTS.md, SEARCH.md, agent prompts, tests/adapters/test_deny_text_search.py, tests/ci/test_repo_claims_*, docs/research/process/34-text-search-allow-ripgrep-2026.md

## 2026-08-09 — E-CPL0 research + TEL empty-log tee repair
Commit: e153f5c1
Tests: tests/ci/test_stalker_telemetry.py 9/9 passing; check_repo_claims OK
Assumptions affected:
- `docs/research/process/28-local-stalker-telemetry-etl-2026.md` — suite log ETL non-empty bodies — [New info — tip runs still had 0-byte suite logs; live sink + post-with getvalue repair; E-CPL0 Spec DRAFT for standing closed-loop fitness]
- Steering prompts — no Grep/rg deny revival — [Still accurate]
Files touched: docs/research/process/35-control-plane-closed-loop-2026.md, docs/design/control-plane-closed-loop-design-2026-08-09.md, docs/research/quality-backlog.md, docs/research/README.md, scripts/ci/pre_pr.py, src/doc_engine/ci/stalker_telemetry/run_store.py, tests/ci/test_stalker_telemetry.py, docs/process/session-log.md


## 2026-08-09 — Non-vacuous receipt hook on test writes
Commit: e153f5c1
Tests: test_nonvacuous_receipt_witness + test_inject_nonvacuous_test_witness + hardened 39 passing
Assumptions affected:
- E-TEL / E-CPL0 — empty telemetry counted as observed — [Resolved — postToolUse inject on tests/** + commit-time witness markers on control-plane stage]
Files touched: .cursor/hooks/inject_nonvacuous_test_witness.py, .cursor/hooks.json, adapters/claude/hooks/nonvacuous_receipt_witness.py, adapters/claude/hooks/require_hardened_tests.py, tests/adapters/test_nonvacuous_receipt_witness.py, tests/ci/test_inject_nonvacuous_test_witness.py, docs/design/control-plane-closed-loop-design-2026-08-09.md


## 2026-08-10 — Empty-telemetry fail-closed + CodeQL skip corpus fix
Commit: e153f5c1
Tests: stalker/oracle/nonvacuity suites green; gate run_expensive=false vs origin/main
Assumptions affected:
- E-TEL / E-CPL — empty suite log still overall=pass — [Resolved — hard suite empty tee → fail]
- E-CQL1 — fingerprint skip — [New info — Path.glob(**) yielded dirs only so corpus was near-empty; rglob fix; workflow YAML removed from corpus; single expensive job]
- Adequacy sensors as proof tests are non-vacuous — [Still accurate — advisory only; new AST check-free ratchet for tests/ci+adapters]
Files touched: scripts/ci/pre_pr.py, scripts/ci/codeql_signals_change_gate.py, .github/workflows/codeql-signals.yml, tests/ci/test_*, adapters/claude/hooks/nonvacuous_receipt_witness.py, docs/research/ci/17-*.md
## 2026-08-10 — E-REPO1-A: nest semantic_eval + docs_site; prune dead mkdocs finder
Commit: b99aa0d
Tests: 46 nest-related pytest green; claims OK; CQ OK; facade poke OK; size OK; complexipy ≤5 on new pkgs
Assumptions affected:
- First tools nest waits on cycle-break — [Resolved — nested `doc_engine.semantic_eval` + `doc_engine.docs_site`; tools `-m` shims]
- Dead `_find_mkdocs_yml` path — [Resolved — climb-compat stub on shim; logic pruned from builder]
- Root `skills/` delete this tip — [Still accurate — equality gate retained; README marks retire]
Files touched: src/doc_engine/semantic_eval/*, src/doc_engine/docs_site/*, tools shims, tools_bc_inventory.json, DOMAIN_MAP.md, memo 25, quality-backlog, code_quality_baseline.json, check_facade_poke_surface.py, skills/README.md, session-log

