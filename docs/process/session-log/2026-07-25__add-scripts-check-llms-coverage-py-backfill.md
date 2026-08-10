# Session log — 2026-07-25

Lead: **Add scripts/check_llms_coverage.py; backfill claude/llms/pr-9..15.md; fix stale pr-13.md**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 4. Newest at the bottom of this file.

---

## 2026-07-25 ? Add scripts/check_llms_coverage.py; backfill claude/llms/pr-9..15.md; fix stale pr-13.md



Commit: 8ade044



Tests: 7/7 passing (`python3 scripts/test_check_llms_coverage.py -v`); `python3 scripts/check_llms_coverage.py` reports all 15 merged PRs covered against the real repo; `python3 scripts/verify_llms_docs.py` re-run against all 15 `pr-*.md` files, 85/85 commands passing (caught and fixed one bad claim of this session's own, below); full 10-suite local run (`test_spring_signal_scan.py` 32/32, `test_partition_repo.py` 13/13, `test_spring_drift_check.py` 14/14, `test_pipeline_stages.py` 17/17-with-1-skipped, `test_secret_heuristics.py` 13/13, `test_config_keys.py` 12/12, `test_semantic_eval_helpers.py` 19/19, `test_capacity_preflight.py` 9/9, `test_verify_llms_docs.py` 17/17, `test_check_llms_coverage.py` 7/7) ? 153/153.



Assumptions affected:



- `CONSTRAINTS.md` ? "Integration gaps" item 4 (see addendum added in this same commit) ? [New info ? `verify_llms_docs.py` (closed by the 2026-07-23 CI-scaffold entry above) only re-runs commands *inside* files that already exist; it can't notice a `pr-N.md` that was never written, or a stale frontmatter field. A `gh pr list --state merged` audit (prompted by a user question about why `claude/llms/` creation isn't automated) found six merged PRs ? #9, #10, #11, #12, #14, #15 ? with no `pr-N.md` at all, and `pr-13.md` itself stale (`state: OPEN` in frontmatter, though PR #13 had actually merged at `e8dbe89a` ? the same class of bug `pr-8.md` had before the 2026-07-23 entry above, recurring because nothing re-checks frontmatter). All six backfilled, each hand-verified against its real merge commit before being written (per this repo's write-then-verify convention) ? caught one bad claim in the process: `pr-9.md`'s original "Expect: no output" wording for a `grep -v` command didn't match the command's real output (a trailing stat-summary line), fixed and re-verified before finalizing. `pr-13.md`'s `state`/`merge_commit` fields corrected; its existing verification commands were unaffected (`3254d67` is confirmed still an ancestor of the real merge commit). `scripts/check_llms_coverage.py` (new) closes the completeness gap going forward: fails CI if a merged PR has no `pr-N.md`, or if one exists with a `state:` that doesn't match `gh pr list`'s real state, in one `gh` call per run.]



- Deliberately *not* treated as automating `claude/llms/pr-N.md` *creation* ? a design question raised explicitly in this session (whether PR docs should be auto-drafted on merge) was decided against for now: drafting a summary and picking verification claims requires judgment a mechanical CI step doesn't have. This change only makes *absence* and *staleness* visible, matching `claude/llms/README.md`'s existing "hand-verified, not generated" framing ? not a steering-prompt assumption directly, but worth recording so a future session doesn't rediscover the same "should this be automated" question without this context.



- Recursive-coverage note for the next session: this very PR, once merged, gets a new PR number and ? per the convention it just added ? needs its own `pr-N.md`, or `check_llms_coverage.py` will flag it as a gap on the first post-merge CI run. Not written yet (the PR number isn't assigned until the PR is opened); flagged here as the explicit immediate follow-up rather than left implicit.



Files touched: scripts/check_llms_coverage.py, scripts/test_check_llms_coverage.py, claude/llms/pr-9.md, claude/llms/pr-10.md, claude/llms/pr-11.md, claude/llms/pr-12.md, claude/llms/pr-13.md, claude/llms/pr-14.md, claude/llms/pr-15.md, claude/llms/README.md, .github/workflows/ci.yml, CONSTRAINTS.md, claude/session-log.md







---







## 2026-07-25 ? Fix the infinite-regress bug in claude/llms/ coverage enforcement



Commit: 6312d45



Tests: 14/14 passing (`python3 scripts/test_check_llms_coverage.py -v`, up from 7 ? 6 new cases exercising the grace window plus a new `MostRecentlyMergedTest` class); `python3 scripts/check_llms_coverage.py` against the real repo reports clean with the exemption named explicitly (`... PR #17 exempt as the most-recently-merged, per the grace window`); `python3 scripts/verify_llms_docs.py` unaffected (this change touches no `pr-*.md` verification commands), full pass count unchanged; direct simulation (not part of the test suite, run manually) confirmed the exemption actually shifts forward: a synthetic undocumented PR is clean while it's the newest, then correctly flagged the moment a second, newer synthetic PR is added.



Assumptions affected:



- `CONSTRAINTS.md` ? "Integration gaps" item 4's own first addendum (2026-07-25, logged above), which closed the missing-doc/stale-state completeness gap but introduced a new structural bug in doing so ? [Resolved, second addendum added to the same item ? the completeness check itself couldn't be satisfied by the PR that just satisfied a prior gap, since a PR can't document its own merge commit before that commit exists. This happened for real, twice: PR #16 (added the check, backfilled six docs) merged and was immediately flagged red by its own new check; PR #17 (added `pr-16.md` to fix that) merged and was immediately flagged red for the identical reason. `pr-17.md`'s own text named this explicitly as "a structural property of the convention... worth a real design decision... rather than another one-off backfill" ? this entry is that design decision. Two changes, not one: `claude/llms/README.md` now documents a convention (write a PR's own `pr-N.md` in the same PR, pinned to its head commit ? the exact pattern `pr-13.md` already demonstrated before PR #13 merged, just not previously written down as a rule); `check_llms_coverage.py` exempts the single most-recently-merged PR (by `mergedAt`, not PR number ? GitHub PR numbers are assigned at creation and don't strictly track merge order) from both checks, so the real requirement becomes "covered before the next PR merges," not "covered before this PR's own CI run finishes." Deliberately not "relax the check to a warning" or "batch multiple PRs' worth of grace" ? either would have quietly reintroduced the original silent-gap problem `check_llms_coverage.py` was built to close; the fix is sized to exactly the one PR-cycle of unavoidable latency, per `00-shared-research-standards.md`'s "scope down rather than importing complexity for its own sake."]



- No new `pr-N.md` needed for the PR that lands this fix ? under the exemption it introduces, the newest merged PR (this one, once merged) is automatically exempt from both checks. Confirmed this isn't a loophole being exploited silently: `claude/llms/pr-17.md` (itself an instance of the same regress, written before this fix landed) is bundled into this same change, so PR #17 doesn't become newly exposed the moment this fix's PR becomes the new "most recent."



Files touched: scripts/check_llms_coverage.py, scripts/test_check_llms_coverage.py, claude/llms/pr-17.md, claude/llms/README.md, CONSTRAINTS.md, claude/session-log.md







---







## 2026-07-24 ? Add scripts/run_manifest.py (run-level telemetry, closing 04's item 2)



Commit: ff60578



Tests: 31/31 passing (`python3 scripts/test_run_manifest.py -v`, new); `test_pipeline_stages.py` re-run clean after the `doc_tag_utils.py` extraction (17/17 with 1 correctly skipped, unchanged from baseline ? extraction confirmed behavior-preserving, not just "should be"); full 11-suite local run (`test_spring_signal_scan.py` 32/32, `test_partition_repo.py` 13/13, `test_spring_drift_check.py` 14/14, `test_pipeline_stages.py` 17/17-with-1-skipped, `test_secret_heuristics.py` 13/13, `test_config_keys.py` 12/12, `test_semantic_eval_helpers.py` 19/19, `test_capacity_preflight.py` 9/9, `test_verify_llms_docs.py` 17/17, `test_check_llms_coverage.py` 17/17, `test_run_manifest.py` 31/31) ? 194/194; `python3 scripts/verify_llms_docs.py` re-run, 103/103 against the real repo; manual end-to-end CLI smoke test against `scripts/test_fixtures/spring_signals/` (`init` ? two `start-stage`/`end-stage` pairs including a deliberate failed-then-retried `partition` stage ? `finalize --docs-dir --interview-file`), output inspected directly against `run_manifest.schema.json`'s documented shape rather than eyeballed.



Assumptions affected:



- `claude/steering-prompts/04-analytics-logging-research-prompt.md` ? item 2, "a `run_manifest.json`... still not built" ? [Resolved ? `scripts/run_manifest.py` implements the schema `claude/analytics-logging-research-2026-07-24.md` proposed (itself added to this repo this session, prior-art research against MLflow/ML-Metadata/in-toto/dvc.lock, schema proposal only, emitter left unbuilt). Confirmed via a real design-review pass before implementation (not shipped on the first draft): the reviewed design added `target_repo.dirty` (mirroring `spring_signal_scan.py`'s own stated reasoning for content-hashing over a git blob SHA), split Stage 0 into two independently-timed manifest stages (`signal_scan`/`partition`) instead of one lumped stage, added explicit partial/crashed-run handling (`finalize` auto-cancels any stage still `running` and sets a new `status: "partial"`, distinct from `complete`/`failed`, rather than silently misreporting a crashed run as clean), made every manifest write atomic (temp file + `os.replace()` ? new territory for this codebase, which previously only had single-shot-output scripts), and extracted the tag-grammar helpers `run_manifest.py` needed out of `test_pipeline_stages.py` into a new shared `scripts/doc_tag_utils.py` rather than having production code import from a test file. `SKILL.md`'s Stage 0?4 sections now each bracket their dispatch with `start-stage`/`end-stage` calls, with an explicit bolded concurrency contract (called once per named stage, by the orchestrating thread only ? never per subagent or per parallel dispatch) since the read-modify-write design has no locking and a violation would silently lose updates.]



- `claude/steering-prompts/04-analytics-logging-research-prompt.md` (via `MATURITY_ASSESSMENT.md` line 36, read directly and quoted verbatim during design review) ? the "predicted vs. actual fan-out" calibration-loop follow-on this file itself named as a natural next step ? [Resolved ? `finalize --preflight-file capacity_preflight_report.json` ties `capacity_preflight.py`'s predicted per-stage fan-out to `run_manifest.py`'s own recorded actual fan-out. This needed a real fix mid-design: `capacity_preflight.py`'s `stage_fanout` keys (`stage1_file_summarizer`, `stage2_architect_segment`, `stage2_architect_merge`, `stage3_gap_analyzer`, `stage4_doc_writer` ? confirmed via direct read, not assumed) don't match `run_manifest.py`'s own stage names at all, and a naive same-name diff would have silently produced nothing for every single key. Fixed with an explicit `PREFLIGHT_TO_MANIFEST_STAGE` mapping (segment+merge sum into one combined `architect` stage) and a loud warning ? not a silent no-op ? for any preflight key with no mapping entry, covered by two dedicated tests.]



- `claude/steering-prompts/02-pluggability-research-prompt.md` ? "no schema, no validation, just shared understanding documented in prose" across the four inter-stage JSON artifacts ? [Still accurate, with one small, deliberately-scoped exception ? `interview_answers.json` now has a documented list-of-objects shape (`SKILL.md` Stage 3), needed because `run_manifest.py finalize --interview-file` can't compute asked/answered/skipped counts from free prose. This formalizes one existing file's already-informal shape; it does not add schema validation (no `jsonschema` dependency ? `run_manifest.schema.json` is a hand-checked plain-JSON reference used by `test_run_manifest.py`'s own `validate_manifest_shape()`, not an enforced schema) and does not touch the other three artifacts. The broader gap this prompt tracks remains open.]



- `CONSTRAINTS.md` "Integration gaps" item 3 and `MATURITY_ASSESSMENT.md`'s "Observability / telemetry" row ? both updated in this same commit to reflect the above, including the stated residual gap that `run_manifest.json`'s `file_signatures` still can't be fed directly into `spring_drift_check.py` (that script's CLI hardcodes expecting a full `spring_signals.json` shape, including `evidence`/`entity_table_map` fields `run_manifest.json` doesn't carry) ? a real integration gap, not yet closed by this change, stated rather than silently left implied as done.



Files touched: scripts/run_manifest.py, scripts/run_manifest.schema.json, scripts/test_run_manifest.py, scripts/doc_tag_utils.py, scripts/test_pipeline_stages.py, skills/document-spring-repo/SKILL.md, .github/workflows/ci.yml, CONSTRAINTS.md, MATURITY_ASSESSMENT.md, claude/session-log.md







---







## 2026-07-25 ? spring_drift_check.py: add --manifest to use run_manifest.json as the tier-1 baseline



Commit: dec15c4 (branch `drift-check-manifest-baseline`)



Tests: 19/19 passing (`python3 scripts/test_spring_drift_check.py -v`, up from 14 ? 5 new cases: no-manifest default source, manifest overriding tier-1, manifest-plus-signals still required for tier-2, a malformed-manifest rejection, and a CLI round-trip via subprocess); full 11-suite local run unaffected elsewhere (`test_spring_signal_scan.py` 32/32, `test_partition_repo.py` 13/13, `test_pipeline_stages.py` 17/17-with-1-skipped, `test_secret_heuristics.py` 13/13, `test_config_keys.py` 12/12, `test_semantic_eval_helpers.py` 19/19, `test_capacity_preflight.py` 9/9, `test_verify_llms_docs.py` 17/17, `test_check_llms_coverage.py` 17/17, `test_run_manifest.py` 31/31) ? 199/199 total, up from 194.



Assumptions affected:



- `CONSTRAINTS.md` "Integration gaps" item 3's residual gap (added by the 2026-07-24 entry above) ? "`spring_drift_check.py`'s CLI still hardcodes expecting a full `spring_signals.json` ... so feeding a `run_manifest.json` into it directly isn't wired up yet" ? [Resolved ? `spring_drift_check.py` now accepts an optional `--manifest run_manifest.json` flag (and a `manifest=` parameter on `check_drift()`) that uses the manifest's `file_signatures` as the tier-1 baseline instead of `spring_signals.json`'s own. Design grounded in real research (`claude/drift-check-manifest-baseline-research-2026-07-25.md`, arXiv + GitHub prior art against `00-shared-research-standards.md`'s methodology): prefer the manifest as an explicit provenance record of the run that produced the *currently-published* docs, not because it's "more recent" ? the same principle `fiberplane/drift` (a real doc-rot linter) uses for its own multi-baseline resolution. The report's new `file_signatures_baseline` field records which source was used plus the manifest's `run_id`/`commit_hash`/`dirty`.]



- `claude/steering-prompts/04-analytics-logging-research-prompt.md` ? item 2's original framing, "`file_signatures` (feeding `spring_drift_check.py` as its 'prior scan' input directly, **rather than requiring a separate `spring_signals.json` copy**)" ? [New info, not a clean Resolved ? what got built is additive, not a replacement: `spring_signals.json` is still required in every case, because `run_manifest.json` never carries the `evidence`/`entity_table_map` tier-2 needs regardless of which file supplies the tier-1 baseline. The item's literal "rather than requiring a separate copy" framing turned out not to be achievable without changing `run_manifest.json`'s own scope (adding citation-level evidence to it, which `claude/session-log.md`'s 2026-07-24 entry explicitly designed against ? evidence lives in `spring_signals.json` by design). Flagging this explicitly rather than marking the item Resolved on the strength of directional progress alone.]



- `claude/steering-prompts/06-wiredrift-check-task-prompt.md` ? frontmatter says `status: not started`, but its actual ask (steps 3?4: document `spring_drift_check.py` as an optional pre-flight check in `SKILL.md` and `README.md`) is already done ? both files already had "On drift detection"/"Optional pre-flight" sections *before* this session touched them (this session only extended those existing sections with `--manifest` usage, didn't create them from scratch). [New info ? this prompt's status field appears stale from an earlier, unlogged session; not corrected here since re-verifying exactly when/which commit did that original wiring is out of scope for this change, but worth a look next time someone is in this file, so a future session doesn't redo already-done work under the belief nothing has started.]



Files touched: scripts/spring_drift_check.py, scripts/test_spring_drift_check.py, skills/document-spring-repo/SKILL.md, README.md, CONSTRAINTS.md, claude/drift-check-manifest-baseline-research-2026-07-25.md, claude/session-log.md







---







