# Session log — 2026-07-24

Lead: **Kitchen-sink end-to-end suite; three real bugs found and fixed by it**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 2. Newest at the bottom of this file.

---

## 2026-07-24 ? Kitchen-sink end-to-end suite; three real bugs found and fixed by it



Commit: 065680a at write time ? see `git log` for this entry's commit



Tests: new `test_enterprise_kitchen_sink.py` ? 64 tests, 1 deliberate `expectedFailure`, 6 opt-in skips, ~132s on Windows (~55s of that is the one-time chain in `setUpModule`). All 13 other suites still pass. Non-vacuity verified by neutering `check_pipeline_output.exit_code` and confirming exactly the five gate-catches-defect tests went red.



Assumptions affected:



- `claude/steering-prompts/01-testability-research-prompt.md` ? "real, checked-in tests for its two deterministic scripts ? That's solid" ? [New info, third instance. The gap that actually mattered was not *which* scripts had tests but that every suite tested one script in isolation: nothing ran the documented command series as subprocesses, and no fault injection ever closed the loop to a real process exit code, so every gate was proven only to populate an issues list. Both are now covered. The prompt's item 1 ("a small synthetic Spring Boot repo fixture ? sized to exercise all five agent stages") is delivered a second time, in hostile form.]



- `CONSTRAINTS.md` "Known precision tradeoffs" item 5 ? the byte-determinism entry arguing a re-run-and-diff probe passed against an unfixed scanner while `keys == sorted(keys)` caught it ? [Still accurate, and reinforced: this suite weights invariants over probes for exactly that reason, and asserts sortedness only where the source actually sorts, with a deliberate *inverse* assertion on the DFS-ordered collections.]







Three bugs were found by writing the fixture, not by reading the code. All three are fixed; three further findings are pinned as current behavior rather than fixed.







1. **`partition_repo.build_groups()` could loop forever.** The zero-progress guard only re-checked the hard cap, so a carry that was itself large enough to re-trip the *soft target* looped: same file re-evaluated against an identical group, `i` frozen, `groups` growing without bound (2927 groups and climbing before the probe was killed). Trigger is a single carried file whose tokens land in `[target_per_group, max_tokens)` ? reproduced with a 2916-token file at `--max-tokens 3000`. Guard now re-checks both triggers. This is a hang, not a wrong answer: Stage 0 would never return.



2. **ast-grep's stdout was decoded with the locale codec.** `subprocess.run(..., text=True)` with no `encoding=`; matched source text flows into every evidence row's `match` field. On a cp1252 Windows box a character whose UTF-8 contains `0x81/0x8D/0x8F/0x90/0x9D` (Cyrillic `?`, `Á`) crashed the scan outright, while `é`/`?`/emoji became silent mojibake in cited documentation. Now explicit `encoding="utf-8", errors="replace"`.



3. **Config files were read as `utf-8`, not `utf-8-sig`.** A BOM survived as a literal `\ufeff`, which is category `Cf` and matches neither `\s` nor `\w`, so every `^\s*`-anchored regex failed on line 1 ? dropping that line's key and never flagging a credential on it. Worse when line 1 is a group header: it never enters the indent stack and every descendant key silently loses its prefix, producing a key set that looks plausible and is wrong.







Pinned, not fixed (each with the reasoning at the assertion, and a `[Flagged, not yet resolved]` entry in `CONSTRAINTS.md`): overlap cascading into three groups at small `--max-tokens`, violating an invariant `test_partition_repo_real_world.py` already asserts; `application-dev-local.yml` not matching `CONFIG_NAME_PATTERNS` at all, so a plausibly credential-bearing file is never scanned; and a write into a gitignored path being invisible to the write-scope gate, which is the one control `SKILL.md` describes as needing no cooperation from the agent.







Worth recording for method rather than content: all three bugs and all three findings came from *building a hostile fixture and running the real commands against it*, not from reading the scripts. The encoding bugs in particular were invisible from the output ? the scan reported success and the key set looked reasonable.







Files touched: scripts/test_enterprise_kitchen_sink.py, scripts/partition_repo.py, scripts/spring_signal_scan.py, scripts/run_pipeline_local.py, .github/workflows/ci.yml, CONSTRAINTS.md, MATURITY_ASSESSMENT.md, claude/session-log.md







## 2026-07-24 ? Code-quality ratchet: ruff lint + a committed per-function baseline gate



Commit: 065680a at write time ? see `git log` for this entry's commit



Tests: all suites pass ? 14 fast suites (335 tests) plus `test_enterprise_kitchen_sink.py` (64 tests, 6 skipped, 1 expected failure), 399 total. New `test_check_code_quality.py` is 29/29. Non-vacuity of the new gate verified by injecting three nested `if`s into `citation_coverage._read_lines` and confirming exit code 1 with all three metrics reported, then reverting.



Assumptions affected:



- `claude/steering-prompts/07-ci-scaffold-task-prompt.md` ? `status: not started`, and body text "There is no `.github/workflows/` directory and no CI of any kind, confirmed absent" ? [Resolved ? the frontmatter was stale long before this change; `CONSTRAINTS.md` item 2 has said "Closes 07" since `ci.yml` landed. Corrected the `status:` field in place and recorded that the prompt's *second* deliverable (the `claude/llms/` meta-verification script) is deliberately not coming back, having been deleted in `2f82971` as an RCE vector. Body left as historical record per `CLAUDE.md`.]



- `CONSTRAINTS.md` "Integration gaps" item 2 ? "plus `verify_llms_docs.py` and `check_llms_coverage.py`" ? [Resolved ? false since `2f82971` deleted that script; item 4 of the same file already recorded the deletion, so the file contradicted itself. Corrected in place, drift direction stated.]



- `CONSTRAINTS.md` "Runtime prerequisites" item 4 ? "All three of the above are now version-pinned in a `requirements.txt`" ? [Still accurate. A second file, `requirements-dev.txt`, was added rather than extending this one, precisely so this claim stays true: the runtime prerequisite set is still exactly three.]







What this adds, and the one thing it deliberately does not.







`scripts/check_code_quality.py` records per-function statement count / cyclomatic complexity / nesting depth for every function in `scripts/`, plus type-annotation coverage over production modules only, into a committed `code_quality_baseline.json`, and fails CI on regression. **Statement count, not line span** ? the first draft measured `end_lineno - lineno` and immediately flagged a function that had grown only by an eight-line comment explaining a bug. In a repo that is deliberately 38?54% prose, a metric that reads documenting something as making it worse is a metric that gets the gate deleted; statements measure what the function *does*, which is what "too long" was always a proxy for. Caught by the gate firing on its own author. A fixed threshold was rejected on the usual grounds: on an existing codebase it is either set above everything and enforces nothing, or below something and gets disabled in a week. The ratchet never asks for a refactor; it asks that these numbers not grow.







Annotation coverage counts production modules only. Test methods are never annotated by anyone, so including them would mean *adding a suite lowers the ratio and fails the build* ? a check that penalizes writing tests is a check that gets deleted. Found by writing this file's own test suite and watching the ratio drop.







The measured picture, which is more interesting than the headline: annotation is all-or-nothing per module. `build_cross_group_edges.py` (6/6), `check_llms_coverage.py` (7/7) and `check_pipeline_output.py` (8/8) are fully annotated; every other module is at zero ? 21 of 149 production functions overall. The convention already exists here and was simply never applied backwards, which is why the ratchet measures rather than mandates.







`ruff` (0.16.0, pinned) took `scripts/` from 617 findings to zero. 509 of those were `E501`; the 110-character limit now configured is this repo's own p99.5, not a style-guide default, because 38?54% of the larger modules is deliberate explanatory prose and reflowing it to 79 would be vandalism. Two rule families are ignored *with their counts stated in `.ruff.toml`* rather than silently: `E501`'s residual 58, and `UP006`/`UP035`/`UP045` (66 combined), the latter because they edit exactly the three fully-annotated modules that the typed-cross-stage-artifact work will touch anyway.







`ruff format` is **not** wired. 29 of 33 files would be reformatted; that is one mechanical commit burying every subsequent diff and blame line, so it is its own decision with its own `.git-blame-ignore-revs` entry. Stated in `ci.yml` with the number rather than left as an unexplained absence.







Three of the seven findings ruff could not auto-fix were `zip()` without `strict=`, and they did not have the same answer: `zip(buckets, lists)` in `run_pipeline_local.pick()` is same-length by construction, so `strict=True` documents a real invariant, while the two `zip(xs, xs[1:])` pairwise-adjacent idioms are ragged on purpose and got `strict=False`. The `%r` formatting in `test_enterprise_kitchen_sink.py`'s subprocess probe was `noqa`'d, not converted: that string is *source code*, and `%r` renders a Windows path as a correctly-escaped Python literal where an f-string would emit `C:\Users\...` raw and produce a probe that fails to parse.







Files touched: scripts/check_code_quality.py, scripts/test_check_code_quality.py, scripts/code_quality_baseline.json, .ruff.toml, requirements-dev.txt, .github/workflows/ci.yml, CONSTRAINTS.md, claude/steering-prompts/07-ci-scaffold-task-prompt.md, claude/session-log.md, plus mechanical ruff fixes across scripts/ (unused imports, import order, redundant open modes, missing EOF newlines)







