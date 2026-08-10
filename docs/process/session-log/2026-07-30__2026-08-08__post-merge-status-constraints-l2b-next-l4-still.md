# Session log — 2026-07-30 → 2026-08-08

Lead: **Post-merge STATUS/CONSTRAINTS: L2b next; L4 still human**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 15. Newest at the bottom of this file.

---

## 2026-07-30 ? Post-merge STATUS/CONSTRAINTS: L2b next; L4 still human

Commit: 065680a

Tests: n/a (docs)

Assumptions affected:

- PR #73 still open / L1 only on branch ? [Resolved ? merged to main]

- Branch protection unchecked ? [Resolved ? gh api protection 404 confirmed 2026-07-30; remains human L4]

- Next engineering still points at L3 ? [Resolved ? Next = L2b post-summary calibration; L3 after L2/L2b]

Files touched: STATUS.md, CONSTRAINTS.md, claude/session-log.md





## 2026-07-30 ? L2b measured_stage4_inputs (measure, do not invent threshold)

Commit: 065680a

Tests: 28/28 capacity_preflight; 8/8 ddia depth; check_repo_claims OK

Assumptions affected:

- L2b only queued / no post-artifact measure mode ? [Resolved ? --summaries-file ? measured_stage4_inputs + optional proxy comparison; returns still omitted]

- Default stage4 warn threshold should be recalibrated now that DDIA bites ? [Still accurate ? 80000 unchanged until documented mid-size run; cite rel-partition-bounds-fanout / claims-and-status-drift]

- capacity-preflight skill says L2b not implemented ? [Resolved ? Step 2b documents measured mode]

Files touched: src/doc_engine/tools/capacity_preflight.py, tests/doc_engine/test_capacity_preflight.py, skills/capacity-preflight/SKILL.md, adapters/claude/skills/capacity-preflight/SKILL.md, docs/design/ddia-north-star/domains/07-partitioning-and-skew/relationships/partition-bounds-fanout.md, STATUS.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/session-log.md



## 2026-07-30 ? L2b follow-up: STATUS honesty + proxy-source precedence

Commit: 065680a

Tests: 29/29 capacity_preflight

Assumptions affected:

- L2b measurement implied as every-run / already on main ? [Resolved ? STATUS/queue: opt-in CLI on PR #74; not Stage 0 pipeline argv]

- Both proxy sources silently preferred stage0 report ? [Resolved ? stage4_proxy_comparison_source warning + skill/CLI help; groups-path proxy excludes signals]

Files touched: src/doc_engine/tools/capacity_preflight.py, tests/doc_engine/test_capacity_preflight.py, skills/capacity-preflight/SKILL.md, adapters/claude/skills/capacity-preflight/SKILL.md, STATUS.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/session-log.md



## 2026-07-30 ? L2b threshold calibration research: retain 80000

Commit: 065680a

Tests: n/a (research note; no default code change)

Assumptions affected:

- May invent/recalibrate 80k from papers alone ? [Resolved ? REFUTED; retain 80000; mid-size measured_stage4_inputs run still required to change]

- Calibration gate blocks all of L3 forever ? [New info ? default decision closed; L3 research may proceed; changing 80k still needs mid-size run]

Files touched: claude/research/l2b-stage4-threshold-calibration-2026-07-30.md, STATUS.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/session-log.md



## 2026-07-30 ? Calib note: Review B = Kimi K3 (2607.24653), retain 80k

Commit: 065680a

Tests: n/a (docs)

Assumptions affected:

- Second independent arXiv review may be Aug 2025 RCR-Router ? [Resolved ? demoted; Review B is summer 2026 Kimi K3 tech report; ContextBudget remains Review A spring]

- 1M context licenses raising Stage-4 warn default ? [Still accurate ? REFUTED; retain 80000]

Files touched: claude/research/l2b-stage4-threshold-calibration-2026-07-30.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/session-log.md



## 2026-07-30 ? L3 claim-symbol entity-identity ADR (research only)

Commit: 065680a

Tests: n/a (ADR docs)

Assumptions affected:

- L3 unscoped / blocked on inventing 80k ? [Resolved ? ADR proposed; default retain closed in PR #75; mid-size run still needed only to change 80k]

- Phase 1 unfinished / maturation §1 executable ? [Still accurate ? ADR REFINE; dual-emit done; identity backlog later amended to principal-complete B]

Files touched: claude/research/claim-symbol-entity-identity-adr-2026-07-30.md, STATUS.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/session-log.md



## 2026-07-30 ? L3 ADR: FQCN (A), reject dual-read as architecture

Commit: 065680a

Tests: n/a (docs)

Assumptions affected:

- L3 research direction D then A (hybrid dual-read landing pad) ? [Resolved ? amended to canonical FQCN (A); D rejected as standing identity; migration = versioned cutover of regenerated facts]

- Facts SoR is durable dual-read store ? [New info ? facts are scan-time projection; dual-read poorly motivated]

Files touched: claude/research/claim-symbol-entity-identity-adr-2026-07-30.md, claude/session-log.md



## 2026-07-30 ? L3 ADR: principal-complete symbol (B), calculated forward risk

Commit: 065680a

Tests: n/a (docs)

Assumptions affected:

- L3 identity D?A or bare FQCN (A) or vague thin B ? [Resolved ? principal-complete SCIP-inspired B; type emit + full grammar/API; bold OK when modest risk prevents second migration]

- Dual-read as architecture ? [Still accurate ? rejected]

Files touched: claude/research/claim-symbol-entity-identity-adr-2026-07-30.md, STATUS.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/session-log.md

## 2026-07-30 — L3 principal-complete claim-symbol identity (code)
Commit: 065680a
Tests: focused identity suite 54 passed (+ ScanDeterminism contested); ocs live MAPS_TO=53 bad=0 Path A simple-name keys; full tests/doc_engine not waited (529 tests; prior stalls were Select-Object buffering)
Assumptions affected:
- L3 ADR research-only / FQCN backlog open — [Resolved — grammar memo + symbol API + type MAPS_TO emit; FACTS_LEDGER_SCHEMA_VERSION=2; Path A simple-name residual]
- Dual-read as standing identity — [Still accurate — rejected; write-time parse bite]
- Tests as emit-mirror theater — [Resolved — deviation-named contracts + grammar goldens]
Files touched: src/doc_engine/scanning/symbol.py, facts.py, java_extract.py, _merge_signals.py, _scanner_*, artifacts.py, scripts/schemas/facts.schema.json, claude/research/claim-symbol-grammar-2026-07-30.md, ADR, facts-ledger-schema, STATUS, queue, CONSTRAINTS, tests/doc_engine/test_symbol.py, test_facts_ledger.py, test_java_extract_package.py, test_artifact_serde_matrix.py, test_spring_signal_scan.py, session-log

## 2026-07-30 - ScanContext inventory argv class closure (own wrong oracle)

Commit: pending

Tests: pytest tests/doc_engine/test_scan_context_wiring.py - 13 passed; pytest tests/ci/test_check_repo_claims.py -k behavior - 3 passed; check_repo_claims.py OK

Assumptions affected:

- 2026-07-28 Windows ast-grep path-list fallback as correct fix - [Resolved - wrong oracle; chunk/bisect preserves ScanContext inventory; behavior:astgrep_inventory_never_widens_to_repo_root forbids inventory->repo-root]

- Wiring tests locking repo-root under pressure - [Resolved - replaced with chunk/equivalence/warning/tombstone + java_files=None legacy-root only]

- tool-quirks alone as SoR for scanner semantics - [New info - CONSTRAINTS Known precision item 14 is product SoR; quirks remains ambient]

Files touched: src/doc_engine/scanning/_scanner_astgrep.py, scripts/ci/check_repo_claims.py, tests/doc_engine/test_scan_context_wiring.py, tests/README.md, CONSTRAINTS.md, STATUS.md, claude/session-log.md, claude/tool-quirks.md



---

## 2026-08-04 — Slim CONSTRAINTS.md to current-state blurbs

Commit: 065680a
Tests: `PYTHONPATH=src python3 scripts/ci/check_repo_claims.py` OK (baseline pruned of 15 obsolete C-missing fingerprints after every remaining bracket claim gained verify:)
Assumptions affected:
- `claude/steering-prompts/03-constraints-research-prompt.md` — "a single CONSTRAINTS.md … structured like doc-taxonomy" / current-state catalog — [Resolved — file rewritten in place as status+fact+residual; diary/addenda removed; pointer-only enterprise duplicates dropped; Enterprise items renumbered 1=RBAC, 2=multi-repo, 3=branch protection]
- `CLAUDE.md` — "CONSTRAINTS.md is a current-state doc, not an append-only log" — [Still accurate — this pass applies that rule]
Files touched: CONSTRAINTS.md, MATURITY_ASSESSMENT.md, STATUS.md, scripts/ratchets/repo_claims_baseline.json, claude/session-log.md

## 2026-08-04 — Non-biting gates (cert forge, covering subset, validate --require, Semgrep SoR)

Commit: d1bec9a
Tests: targeted compliance/covering/validate/semgrep/claims/hooks 10/10; broader related suites green; `PYTHONPATH=src python3 scripts/ci/check_repo_claims.py` OK
Assumptions affected:
- `claude/steering-prompts/07-ci-scaffold-task-prompt.md` — status text still says llms coverage is non-blocking via `ENFORCE = False` — [New info — `ENFORCE` was removed; advisory is always-exit-0 `exit_code()`; check_repo_claims module docstring + CONSTRAINTS item 4 already describe that shape; 07 status frontmatter still names the old flag]
- Profile-required CERTIFIED gates forgeable via `required=False` — [Resolved — `build_certification_report` requires profile gates `required=True` and `ok`]
- Covering receipts with matching garbage subset roots — [Resolved — `verify_covering_proof` recomputes roots from `scope`]
- Stage 0 `validate_artifacts --all` soft-skips missing files — [Resolved — `--require` + CI Stage 0 lists Stage-0 artifacts]
- Semgrep missing recall baseline / empty pack soft-pass — [Resolved — fail-closed; no invented recall baseline file]
- Dead `CI_EXEMPT_SUITES` registry — [Resolved — removed; Check D is scripts/test_*.py wrapper refusal only]
Files touched: src/doc_engine/pipeline/compliance.py, covering.py, validation.py, validate_artifacts.py, .github/workflows/ci.yml, scripts/coverage/semgrep_rule_coverage.py, scripts/ci/check_repo_claims.py, STATUS.md, related tests, comment hygiene on rule_coverage/require_hardened_tests


## 2026-08-05 — PR #92 adversarial-review fixes (Jakarta boundary, ocs gate path, recall arms, harness hardening)

Commit: c7501ce, 3991ff1, 0502351, 6a8fd71, b75faf7
Tests: pytest tests/spring_signals 47/47; mutation driver 10/10 killed; codeql query compile 16/16 (local CLI 2.26.0); codeql test run 18/18; check-invariants.py PASS; check_repo_claims.py OK; bash -n 5/5; full local fixture E2E (Git Bash + Windows codeql + javac --release 17): 31/31 jars digest-verified, extraction delta 0 (set equality), all 54 JSON assertions hold
Assumptions affected:
- steering prompts — none name the spring-signals harness internals these commits change; 08 "CodeQL CLI remains a standalone binary" — [Still accurate]
- run.sh / ocs expectations — "the Messaging=0 gate is ON by default" — [New info — the default invocation always exited 2 (stale-CSV check vs unnamed CSVs); ocs-api-service.json now names all ten wave-1 queries, and tests/spring_signals pins DEFAULT_QUERIES coverage]
- JakartaMigration.ql header — "Every first-party reference to a javax.* namespace" — [New info — was overclaimed; on-demand imports, type arguments, and class literals are now covered, and the header enumerates covered shapes instead]
Files touched: spring-signals/codeql/packs/{java-signals-lib/signals/Schema.qll,spring-signals/{Jakarta.qll,JakartaMigration.ql,OutboundClients.ql,Catalog.qll,NativeSql.ql}}, spring-signals/harness/{check-assertions.py,check-invariants.py,create-db.sh,fixture-repo/fetch-deps.sh,expectations/{fixture-repo.json,ocs-api-service.json}}, spring-signals/docs/SYMBOLS.md, .github/workflows/ci.yml, .gitattributes, tests/spring_signals/test_check_assertions.py, fixture + QL test stubs/expected files, claude/tool-quirks.md

## 2026-08-06 — PR #92 follow-up: transaction.xa + cache + mutation CI

Commit: pending
Tests: codeql test run 18/18 (JakartaMigrationSanity pins xa retained / cache relocated); pytest tests/spring_signals 47/47; mutation_driver 10/10 killed
Assumptions affected:
- Jakarta.qll relocated list as EE-complete vs JDK-retained complement — [New info — javax.transaction.xa was false-positive pending via bare `transaction` slot; split like security.auth; javax.cache added from mappings.adoc]
- mutation_driver as verified gate — [Resolved — wired non-blocking in ci.yml with ENFORCE=False matching mutate.py]
Files touched: spring-signals/codeql/packs/spring-signals/Jakarta.qll, JakartaMigrationSanity.{ql,expected}, spring-signals/harness/fixture-repo/fetch-deps.sh, tests/spring_signals/mutation_driver.py, .github/workflows/ci.yml, claude/session-log.md

## 2026-08-08 — Size ratchet: statement growth hard + file/function ceilings
Commit: 065680a
Tests: pytest tests/ci/test_check_code_quality.py + test_size_ratchet.py + test_run_quality_gates.py 65/65 (earlier full) / 18/18 focused; complexipy =5 on touched modules; check_repo_claims OK; size-ratchet 0/0 hard offenders
Assumptions affected:
- `claude/steering-prompts/13-code-quality-research-prompt.md` — "size/complexity/depth are advisory (schema v4)" — [Resolved — schema v5 hardens statement growth; `doc-engine size-ratchet` hard-fails file LOC >1000 and function statements >50 via `scripts/ratchets/size_baseline.json` in quality-gates; complexity/depth remain advisory here (complexipy owns =5)]
Files touched: src/doc_engine/ci/size_ratchet.py, quality_gates.py, cli.py, spring_drift_{check,common,tier2}.py, scripts/ci/check_code_quality.py, scripts/ratchets/{code_quality_baseline,size_baseline}.json, CONTRIBUTING.md, CONSTRAINTS.md, tests/ci/*, .github/workflows/ci.yml, claude/steering-prompts/13-*.md, claude/session-log.md

