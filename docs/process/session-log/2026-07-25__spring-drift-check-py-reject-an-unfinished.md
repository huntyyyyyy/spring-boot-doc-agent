# Session log — 2026-07-25

Lead: **spring_drift_check.py: reject an unfinished/empty run_manifest.json as --manifest baseline**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 5. Newest at the bottom of this file.

---

## 2026-07-25 ? spring_drift_check.py: reject an unfinished/empty run_manifest.json as --manifest baseline



Commit: f629496 (branch `drift-check-manifest-baseline`, follow-up to `dec15c4` above, from PR review)



Tests: 22/22 passing (`python3 scripts/test_spring_drift_check.py -v`, up from 19 ? 3 new cases: a manifest still at `status: "running"` is rejected, a `"complete"` manifest with an empty `file_signatures` map and no `target_repo.path` is rejected, and a `"complete"` manifest with an empty map whose `target_repo.path` genuinely has zero trackable files is accepted, not rejected). `test_run_manifest.py` unaffected: 31/31.



Assumptions affected:



- `claude/drift-check-manifest-baseline-research-2026-07-25.md` ? that research covered *which* baseline to prefer (manifest vs. `spring_signals.json`) but not *whether a given manifest is trustworthy at all* ? [New info ? added a standard for the latter question. `scripts/run_manifest.py`'s `build_init_manifest()` sets `file_signatures: {}` and `status: "running"`; only `finalize_manifest()` ever changes either, and only overwrites `file_signatures` if actually given some. So a manifest passed to `--manifest` before `finalize` ran (or finalized without ever recording signatures) has an empty `file_signatures` map, which `check_drift()` would previously treat as "zero prior files" ? classifying every current file as `added` and every citation as `STATUS_UNKNOWN_NO_SIGNATURE`, a full-report degradation with no clear error pointing at the actual cause. `load_manifest()` now rejects both cases upfront with an explicit error. Modeled on OpenLineage's run-lifecycle spec (https://openlineage.io/docs/spec/run-cycle/): RunState events START/RUNNING are non-terminal and not something a consumer should treat as a finished fact, only COMPLETE/FAIL/ABORT are ? the same distinction `run_manifest.json`'s own `status` field already draws (`"running"` vs. `"complete"`/`"failed"`/`"partial"`), just not previously enforced by `spring_drift_check.py`'s reader. Caught in review: a repo with genuinely zero trackable files at scan time also finalizes with an empty `file_signatures` map, and "everything is newly added" is the *correct* report for that case, not a misreport ? the blanket empty-map rejection would have falsely rejected it. Fixed by re-walking the manifest's own recorded `target_repo.path` live via `spring_signal_scan.dfs_walk()`: if that path still exists and is still genuinely empty, the manifest is accepted as a real (if unusual) empty-repo baseline instead of erroring.]



- `CONSTRAINTS.md` "Integration gaps" item 3's `[Resolved]` tag from the entry above ? [Still accurate ? the `--manifest` integration itself is unaffected; this hardens input validation on top of it, doesn't change what got wired up.]



Files touched: scripts/spring_drift_check.py, scripts/test_spring_drift_check.py, claude/session-log.md







---







## 2026-07-25 ? Sync STATUS.md and steering-prompt frontmatter to actual repo state



Commit: 824b3b7



Tests: not run (markdown-only change)



Assumptions affected:



- `STATUS.md` (not a steering prompt, but the "single current-state doc" `05-clarity-delivery-trust-research-prompt.md` scoped) ? "Last updated: 2026-07-23," with a Pending section listing dependency pinning, run-manifest telemetry, and (implicitly, via `01`) LLM-stage test coverage as not-yet-done ? [Resolved ? rewritten to move dependency pinning, run-manifest/audit-trail telemetry, and `claude/llms/` coverage backfill into "Done, confirmed delivered," reflecting `claude/session-log.md` entries already on record for 2026-07-24/2026-07-25 that this file had not caught up to. "Next concrete action" repointed at `02-pluggability-research-prompt.md`'s still-open JSON-schema-validation gap.]



- `claude/steering-prompts/08-dependency-pinning-task-prompt.md` ? frontmatter `status: not started` ? [Resolved ? `requirements.txt` exists (`ast-grep-cli~=0.45.0`, `sqllineage~=1.5.8`, `pathspec~=1.1.1`), `.github/workflows/ci.yml` installs from it, per this file's own entry above from 2026-07-25 and `CONSTRAINTS.md` item 4. Frontmatter updated to say so; task body left as historical record, not rewritten.]



- `claude/steering-prompts/04-analytics-logging-research-prompt.md` ? frontmatter said drift-check wiring (item 1) was done but didn't mention item 2 (the run-manifest) was also done ? [Resolved ? frontmatter updated to note `scripts/run_manifest.py` (31/31 tests, CI-wired) and the 2026-07-25 `--manifest` baseline flag both landed.]



- `claude/steering-prompts/03-constraints-research-prompt.md` line 26 ? "structured like `references/doc-taxonomy.md`," an unqualified path implying a root-level `references/` ? [Resolved ? corrected to the real path, `skills/document-spring-repo/references/doc-taxonomy.md`, confirmed by direct directory listing (no root-level `references/` exists in this repo).]



- `claude/steering-prompts/01-testability-research-prompt.md` ? frontmatter status ? [Still accurate ? verified against `scripts/test_pipeline_stages.py` (17/17, CI-wired) and `skills/semantic-pipeline-eval/` (manually invoked, not CI-integrated); no change needed.]



Files touched: STATUS.md, claude/steering-prompts/03-constraints-research-prompt.md, claude/steering-prompts/04-analytics-logging-research-prompt.md, claude/steering-prompts/08-dependency-pinning-task-prompt.md, claude/session-log.md







---







## 2026-07-25 ? Fix find_ast_grep() SystemExit-in-setUpClass process-killing bug



Commit: 824b3b7



Tests: `test_spring_signal_scan.py` 32/32, `test_spring_drift_check.py` 22/22, `test_capacity_preflight.py` 9/9, `test_pipeline_stages.py` 17/17-with-1-skipped ? all pass with `ast-grep` present. Empirically re-reproduced the original bug with `ast-grep` hidden from `PATH` (`PATH` narrowed to just the Python interpreter's own directory): before this fix, the process died silently with no `Ran N tests` line; after, `test_spring_signal_scan.py` now reports a clean `Ran 12 tests in 0.479s / FAILED (errors=4)` summary, with `setUpClass`'s `AstGrepNotFoundError` traceback reported per-class like any other setUpClass failure. Also confirmed the CLI itself (`python scripts/spring_signal_scan.py <dir>` with `ast-grep` hidden) still prints the same one-line friendly error and exits 1 ? no raw traceback leaked to a real user.



Assumptions affected:



- `CONSTRAINTS.md` "Runtime prerequisites" item 1's `[Known residual gap, confirmed 2026-07-24]` sub-note ? "`find_ast_grep()` calls `sys.exit(1)`... `SystemExit` raised inside `setUpClass`... is never caught, killing the whole test process" ? [Resolved ? `find_ast_grep()` now raises `AstGrepNotFoundError(RuntimeError)`, an ordinary `Exception` subclass `unittest._handleClassSetUp` does catch, instead of calling `sys.exit(1)` directly. The three CLI entry points that call it or `scan()`/`check_drift()` (`spring_signal_scan.py`, `spring_drift_check.py`, `capacity_preflight.py`, all in `scripts/`) each gained an explicit `except AstGrepNotFoundError` around the call site to preserve the exact prior CLI behavior (friendly stderr message, exit 1) ? this was a change to failure-mode reporting, not to what happens when the binary really is missing.]



Files touched: scripts/spring_signal_scan.py, scripts/spring_drift_check.py, scripts/capacity_preflight.py, CONSTRAINTS.md, claude/session-log.md







---







## 2026-07-25 ? Resolve bounded single-entity JPQL lineage via entity_table_map



Commit: 824b3b7



Tests: `test_spring_signal_scan.py` 40/40 (up from 32 ? 8 new: 1 updated fixture-integration test replacing the old "JPQL never gets lineage" assertion, 7 new unit tests against `resolve_jpql_to_lineage()` directly covering the happy path and each out-of-scope case). Full suite unaffected elsewhere: `test_spring_drift_check.py` 22/22, `test_pipeline_stages.py` 17/17-with-1-skipped, `test_capacity_preflight.py` 9/9, `test_partition_repo.py` 13/13, `test_secret_heuristics.py` 13/13, `test_config_keys.py` 12/12, `test_semantic_eval_helpers.py` 19/19, `test_verify_llms_docs.py` 17/17, `test_check_llms_coverage.py` 17/17, `test_run_manifest.py` 31/31. Manually verified against the real fixture (`scripts/test_fixtures/spring_signals/InvoiceRepository.java`'s JPQL entry): `resolve_jpql_to_lineage()` now resolves `Invoice` -> `billing_invoice`, matching the native query's own lineage for the same table.



Assumptions affected:



- `CONSTRAINTS.md` "Known precision tradeoffs" item 2 ? "JPQL queries never get SQL-lineage extraction... a known, fundamental limitation" ? [Resolved for the bounded common case ? research (arXiv/GitHub/DeepWiki, three parallel passes) found no published technique or usable open-source tool for JPQL/HQL-to-SQL lineage translation exists (`reata/sqllineage#461` is open and unresolved, corroborating the gap is real and unaddressed industry-wide), but also that this scanner already builds the one piece such a resolution needs (`entity_table_map`) and just never used it for JPQL. `resolve_jpql_to_lineage()` (`scripts/spring_signal_scan.py`) now closes the single-entity/no-join case; multi-entity FROM, association traversal, JPQL-only functions, `@Entity(name=...)` overrides, polymorphic FROM, and embedded/composite keys remain explicitly, permanently out of scope ? stated in the function's own docstring, not silently dropped.]



- `README.md`'s "Native-query lineage" section's closing sentence ? same stale "fundamental... not a gap to close later" framing as CONSTRAINTS.md ? [Resolved ? rewritten to describe the bounded resolver and cite the same research.]



- `skills/document-spring-repo/references/doc-taxonomy.md`'s `database.md` entry ? "JPQL generally can't be [resolved], reliably" ? [Resolved ? updated to describe the new bounded resolution and point to CONSTRAINTS.md for the exact boundary, so doc-writer's `database.md` output no longer inherits the stale framing.]



Files touched: scripts/spring_signal_scan.py, scripts/test_spring_signal_scan.py, CONSTRAINTS.md, README.md, skills/document-spring-repo/references/doc-taxonomy.md, claude/session-log.md







---







## 2026-07-25 ? Fix JPQL-lineage drift-check blind spot: model derived citations as provenance, not a special case



Commit: 2cfb4e0



Tests: `test_spring_drift_check.py` 36/36 (up from 22 ? 14 new: 4 real-repo integration tests in `SpringDriftCheckTest` plus 10 isolated unit tests in a new `JpqlLineageProvenanceTest` class against `_raw_query_entries_with_resolved_entity()`/`_reverify_jpql_lineage_provenance()` directly). `test_spring_signal_scan.py` 42/42 (up from 40 ? 2 new tests for `lineage.resolved_via_entity`). Full suite unaffected elsewhere (11 suites, 225 tests total, all passing). Coverage (`coverage.py`, installed transiently, not added to `requirements.txt`) confirms every new line is exercised except pre-existing/unrelated `main()` CLI plumbing.



Assumptions affected:



- `CONSTRAINTS.md`'s JPQL precision-tradeoff entry (added the same day, prior entry above) didn't account for a real gap it introduced ? [Resolved ? a JPQL citation's `lineage` depends on two files (its own, and the entity's, via `entity_table_map[entity]["file"]`), which `spring_drift_check.py`'s per-file tier-1/tier-2 model couldn't see: a table rename in the entity's file alone would leave the JPQL citation reporting `unchanged` while its lineage silently went stale. Design deliberately rejected two narrower alternatives (a `STATUS_DEPENDENT_ENTITY_CHANGED` status plus a reverse-lookup index from drifted entities to dependent queries; a fully generalized `depends_on` schema field for all citation types) in favor of naming the actual invariant ? "a citation is fresh iff every file in its provenance is unchanged," which every existing rule already followed implicitly with provenance = {own file} ? and widening it honestly for the one citation type that has two inputs. `resolve_jpql_to_lineage()` (`scripts/spring_signal_scan.py`, schema_version 6) now stamps `lineage.resolved_via_entity`; `_reverify_jpql_lineage_provenance()` (`scripts/spring_drift_check.py`) re-derives freshness from all provenance files in one post-loop pass, reusing `_recheck_entities()`'s already-computed fresh entity data (`_recheck_entities`/`tier2_recheck_file` both now return that data as a second value, not just their results list) ? zero extra `ast-grep` invocations, and reuses `STATUS_CONFIRMED`/`STATUS_DRIFTED` rather than new vocabulary. Verified the false-positive-avoidance case explicitly (entity file edited but table mapping unchanged -> `STATUS_CONFIRMED`, not `STATUS_DRIFTED`) and that a citation's own more-specific tier-2 verdict is never overwritten.]



Files touched: scripts/spring_signal_scan.py, scripts/spring_drift_check.py, scripts/test_spring_signal_scan.py, scripts/test_spring_drift_check.py, CONSTRAINTS.md, claude/session-log.md







---







