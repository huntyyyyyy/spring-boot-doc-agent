# Session log — 2026-07-24

Lead: **Fix the renumbering breakage in steering prompts 10-12; unstale CLAUDE.md's prompt count**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 3. Newest at the bottom of this file.

---

## 2026-07-24 ? Fix the renumbering breakage in steering prompts 10-12; unstale CLAUDE.md's prompt count



Commit: 5bd750b



Tests: not run (markdown-only change). Verified instead by resolving every backticked repo-internal path in the three new prompts, `CLAUDE.md`, and `README.md`: zero unresolved. The 20 that don't resolve are all correct as written ? `scip.proto` (external artifact) and the pipeline's own output filenames (`architecture.md`, `spring_signals.json`, ...), which don't exist until a run.



Assumptions affected:



- `claude/steering-prompts/12-review-session-launcher.md` §A ? "Copy §A verbatim into a new terminal session" ? [Resolved ? §A instructed a fresh session to read `08-review-persona-and-standards.md` and `09-context-traversal-protocol.md`. Neither exists: `08-` is the dependency-pinning task prompt and `09-` is tool-quirks indexing, both unrelated. The three review-layer files were renumbered on disk to `10`/`11`/`12` without updating their bodies, so all three H1s and every cross-reference still carried the pre-rename numbers. Headers and all cross-references (`11-?` "Pairs with", "§2 of file 08", "per file 08 §4"; `12-?` "file-09 interleave", "file-08 evidence tiers") corrected. The launcher's three paths now all resolve.]



- `claude/steering-prompts/12-review-session-launcher.md` §B ? filename convention cited `archunit-scanner-scoping-2026-07-23.md` as "the existing shape" ? [Resolved ? that file does not exist in this repo. Repointed at `claude/drift-check-manifest-baseline-research-2026-07-25.md`, which does exist and matches the stated `<topic>-<kind>-<date>` shape.]



- `CLAUDE.md` ? "`claude/steering-prompts/` contains five research/scaffold prompts (`00` shared standards, `01`?`05`)" and "read the five prompt files" ? [Resolved ? there are thirteen (`00`?`12`). A session obeying CLAUDE.md literally would never open `06`?`12`, which includes the entire review layer. Rewritten to describe the three actual groups (`00`?`05` research, `06`?`09` implementation tasks, `10`?`12` review), and to say which ones carry repo-state assumptions worth re-checking before a commit.]



- `CLAUDE.md` ? the pre-commit trigger list named `references/` as a plugin-root-level directory, and quoted "`references/` sits as a plugin-root-level sibling of `skills/`" as a live example assumption ? [Resolved ? no root-level `references/` exists; the convention is per-skill (`skills/document-spring-repo/references/`). This was already closed in `02-pluggability-research-prompt.md` and corrected in prompt `03` on 2026-07-25, but CLAUDE.md itself was missed both times. Dropped from the trigger list and the example replaced.]



- `claude/steering-prompts/00-shared-research-standards.md` ? "the five steering prompts", "all five category prompts", "its four siblings (`01` through `05`)" ? [Resolved ? scoped correctly to the five *category* prompts where that's what's meant, and the mirror-sync note widened to `01`?`12`, which is what actually needs mirroring back to the Claude project.]



- `claude/session-log.md`'s own header ? "One entry per commit that plausibly affects an assumption stated in `claude/steering-prompts/01`?`05`" ? [Resolved ? the log's entries have cited `06`, `07`, and `08` for a while; stated scope now matches practiced scope.]



- `README.md:92` ? "`license` is still `"UNLICENSED"`" ? [Resolved ? `.claude-plugin/plugin.json` says `"MIT"` and the root `LICENSE` is MIT. `CONSTRAINTS.md`, `STATUS.md`, `MATURITY_ASSESSMENT.md` and `pr-13.md` all record fixing this stale claim, and all four list only CONSTRAINTS/STATUS ? README was missed by every pass. Also corrected the overstatement that `marketplace.json` carries a license field: it does not, it inherits by reference.]



- `README.md`'s ast-grep install block ? `cargo install ast-grep` with no mention of `requirements.txt` ? [Resolved ? `requirements.txt` pins `ast-grep-cli~=0.45.0` and CI installs from it, so the README was documenting an unpinned path CI doesn't use. Now leads with `pip install -r requirements.txt` and cross-references the `PATH`-shadowing entry in `claude/tool-quirks.md`, which exists precisely because the two install methods can shadow each other.]



- **Mirror-back required** (per `00-shared-research-standards.md`'s "Mirrored copy ? keep in sync"): prompts `00`, `10`, `11`, `12` were edited here. The canonical copies in the Claude project need the same edits, or the next Cowork session will re-introduce the broken numbering.



- `claude/10-architecture-maturation-plan.md` ? [New info ? left untouched deliberately, per the repo owner's call. Its Phase 0 has three items that no longer match reality (§0.2's unbounded loop was guarded in `5b8e8c8` with a named regression test *before* the plan's own date; §0.4.2's `AstGrepInvocationError` shipped as `AstGrepNotFoundError`; §0.1.4 asserts zizmor is "already wired into `_python-checks.yml`", a file that does not exist), and nine referenced files are missing, two of which it tells you to read. Its filename was also kept as-is rather than moved out of the `NN-` namespace it shares with `steering-prompts/10-`: two of the new prompts cite it by that exact path, so renaming would break more than the cosmetic collision it fixes. Needs a look by whoever owns it.]



Files touched: CLAUDE.md, README.md, claude/session-log.md, claude/steering-prompts/00-shared-research-standards.md, claude/steering-prompts/10-review-persona-and-standards.md, claude/steering-prompts/11-context-traversal-protocol.md, claude/steering-prompts/12-review-session-launcher.md, claude/10-architecture-maturation-plan.md (added, unmodified), claude/jpa-hibernate-predicate-vocabulary-survey.md (added, unmodified), claude/hibernate-jakarta-fact-verification-2026-07-24.md (added, unmodified)







---







## 2026-07-24 ? Sweep stale numbers and self-contradictions out of the living snapshots



Commit: 2d68e64



Tests: full suite 231 passing, 6 intentional skips (`python -m unittest discover -s scripts -p "test_*.py"`) ? unchanged by this commit, which touches prose plus one CI step *name*. `.github/workflows/ci.yml` re-parsed with `yaml.safe_load` after the edit (17 steps, valid). Every backfilled session-log SHA verified to resolve and to match its entry's heading.



Assumptions affected:



- `STATUS.md` ? "`test_semantic_eval_helpers.py` 12/12" ? [Resolved ? the suite has 19 tests and has had since the commit that created it (`3254d67`); `claude/session-log.md` recorded 19/19 correctly three separate times while `STATUS.md` kept the 12 from an early draft.]



- `STATUS.md` and `CONSTRAINTS.md` ? CI "runs all four existing test suites" / a five-suite list, "with `ast-grep` installed via `pip install ast-grep-cli`" ? [Resolved ? `ci.yml` runs every `scripts/test_*.py` except the opt-in `test_partition_repo_real_world.py`, and installs from `requirements.txt`. Both docs now say so, and both now warn that the workflow enumerates suites by hand rather than discovering them, so a new `test_*.py` silently doesn't run in CI until someone adds it ? the failure mode that made the old count wrong in the first place.]



- `CONSTRAINTS.md` "Integration gaps" item 1 ? "not triggered by CI (there is no CI at all ? see next item)" ? [Resolved ? item 2, the very next line, describes the CI that exists and has since `d54cc8a`. `spring_drift_check.py` is in fact run by CI. Item 1 now says what is actually still true: it isn't invoked by the pipeline itself.]



- `CONSTRAINTS.md` item 1's "(12/12 passing)" ? [Resolved ? replaced with the command that produces the current number rather than a new hardcoded one. This count has changed with nearly every PR touching the tool (12 -> 14 -> 19 -> 22 -> 36 -> 41); restating it here just re-arms the same trap. Same reasoning applied where possible elsewhere: state the reproducing command, keep a literal count only where it is evidence for a specific historical claim.]



- `claude/llms/README.md` ? "a bounded grace window, not a hole ... nothing stays undocumented past one PR cycle" ? [Resolved ? falsified by seven PRs. #21-#27 all merged with no `pr-N.md`; `python3 scripts/check_llms_coverage.py` prints all seven today. The window's logic is sound only while the check can fail, and `ENFORCE = False` removed that. The table now carries a row per undocumented PR instead of stopping at #21, and the paragraph states the three real options rather than asserting a bound that did not hold.]



- `.github/workflows/ci.yml` ? step named "check_llms_coverage.py (fails on a merged PR with no claude/llms/pr-N.md)" ? [Resolved ? renamed to say "reports ... non-blocking", because with `ENFORCE = False` the step cannot fail. `claude/steering-prompts/10-review-persona-and-standards.md` §4 lists "a gate that is not a gate" as an anti-pattern this project has actually committed; this was the instance. `ENFORCE` itself is left `False` ? flipping it is a policy call that should be made together with backfilling #21-#27, not smuggled into a docs sweep.]



- `claude/llms/pr-28.md` frontmatter ? `state: OPEN` ? [Resolved ? PR #28 merged as `03c16dd` during this session. Set to `MERGED` with the merge commit recorded, and its index row updated. Its `head_commit` also moved to `9d15ed3`, the branch's real head, rather than the mid-branch `2cfb4e0` it had pinned.]



- `claude/session-log.md`'s own `Commit:` field ? 21 of 23 entries read `uncommitted` ? [Resolved for 19 ? every one now carries a real short SHA, each verified to resolve and to match its entry's heading. Two are deliberately left: the 2026-07-23 stray-scaffolding entry and this one, which are an incident record and a pre-commit entry respectively, exactly the case the `CLAUDE.md` template's "or 'uncommitted' if writing before commit" wording covers. Note three consecutive entries correctly share `824b3b7` ? that single commit carried three separate work items.]



- `STATUS.md` ? "Last updated: 2026-07-25", one day ahead of every commit it describes ? [Resolved for this file, and a stated convention added: dates are the commit's own local date. The other 38 future-dated occurrences across `CONSTRAINTS.md`, `claude/session-log.md`, `claude/tool-quirks.md`, `MATURITY_ASSESSMENT.md` and `check_llms_coverage.py` are deliberately left alone ? rewriting dates inside an append-only log to fix an off-by-one is worse than the off-by-one, and one of them is load-bearing inside a SHA-pinned verification command in `pr-28.md`.]



- `claude/session-log.md` ordering ? the `ff60578` run-manifest entry (2026-07-24) sits after three 2026-07-25 entries, against this file's own "Newest entries at the bottom" ? [New info ? left in place. Moving an entry in an append-only log to fix a date that is itself off by one would compound two problems. Flagged rather than silently reordered.]



Files touched: STATUS.md, CONSTRAINTS.md, .github/workflows/ci.yml, claude/llms/README.md, claude/llms/pr-28.md, claude/session-log.md







---







## 2026-07-24 ? Close two gate misses in the JPQL-provenance pass PR #28 added



Commit: 570a55a (entry added in ee9ba06)



Tests: full suite 236 passing, 6 intentional skips (`python -m unittest discover -s scripts -p "test_*.py"`). `test_spring_drift_check.py` 41/41, up from 36 ? 2 real-repo integration tests plus 3 isolated unit tests in `JpqlLineageProvenanceTest`. `test_spring_signal_scan.py` 42/42, unchanged. All eight `claude/llms/pr-30.md` verification commands re-run against the rebased head `570a55a` and confirmed matching their stated expectations.



Assumptions affected:



- `claude/steering-prompts/06-wiredrift-check-task-prompt.md` ? "`scripts/spring_drift_check.py` already exists ? a real, working two-tier drift detector" ? [New info ? still true, and more nearly true than it was. The provenance pass PR #28 introduced stated the correct invariant ("a citation is fresh iff every file in its provenance is unchanged") but its gate enforced a narrower one, in two ways that both yielded a confidently wrong verdict rather than a loud failure. (a) It skipped any citation whose own-file verdict was not `STATUS_UNCHANGED`, but `_recheck_queries()` returns `STATUS_CONFIRMED` when a query's file changed and its text is intact ? and text presence says nothing about lineage accuracy, so an entity `@Table` rename plus any unrelated edit in the repository file reported `confirmed_still_present` over stale lineage. (b) It keyed on `changed_set` only, while `classify_files()` reports deletes (and moves, as a delete of the old path) in `deleted`, so deleting an entity's file left the dependent JPQL citation at tier-1 `STATUS_UNCHANGED`. Guard widened to `(STATUS_UNCHANGED, STATUS_CONFIRMED)`, `deleted_set` threaded through with a delete-specific detail, and the statuses still deliberately skipped now carry an inline reason each rather than hiding behind one blanket condition. No new status constant.]



- `claude/steering-prompts/06-wiredrift-check-task-prompt.md` frontmatter ? `status: not started` ? [New info ? still stale, and now flagged for the third time (see the 2026-07-25 entry, and the note in PR #29's entry). `STATUS.md` records the wiring as done. Left uncorrected again to keep this commit to the correctness fix; it wants its own change. Needs a look.]



- `scripts/spring_signal_scan.py`'s module docstring ? pointed at `_query_citations_depending_on_entity()` and `_flag_stale_jpql_lineage()` in `spring_drift_check.py` ? [Resolved ? neither name has existed at any commit; they read like a design draft committed after the implementation was renamed. Corrected to the real names, `_raw_query_entries_with_resolved_entity()` and `_reverify_jpql_lineage_provenance()`. Same stale reference also fixed in `test_spring_signal_scan.py`.]



- `scripts/spring_signal_scan.py`'s own `schema_version` history notes ? [Resolved ? two comments dated bounded JPQL resolution to `schema_version 3` and called it the same release as native-query lineage. It shipped under 5; native-query lineage was 3; and the same file already said 6 for `resolved_via_entity`, so the module contradicted itself. The emitted value is untouched at 6 ? this corrects prose, it does not bump the contract.]



Files touched: scripts/spring_drift_check.py, scripts/spring_signal_scan.py, scripts/test_spring_drift_check.py, scripts/test_spring_signal_scan.py, claude/llms/pr-30.md, claude/llms/README.md, claude/session-log.md







---







