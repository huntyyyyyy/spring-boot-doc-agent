# Session log — 2026-07-24 → 2026-07-25

Lead: **Two live defects the quality measurement pass turned up**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 2. Newest at the bottom of this file.

---

## 2026-07-24 ? Two live defects the quality measurement pass turned up



Commit: 065680a at write time ? see `git log` for this entry's commit



Tests: `test_capacity_preflight.py` 15/15 (was 10), `test_spring_signal_scan.py` 51/51 (was 45). Full suite green: 413 tests across 15 suites including the kitchen sink. Both fixes verified non-vacuous by reverting them and confirming the new tests fail ? 3 failures for the path fix, 5 errors (`SystemExit: 1`) for the exception fix.



Assumptions affected:



- `CONSTRAINTS.md` "Runtime prerequisites" item 1 ? `[Resolved, 2026-07-24]`, "`find_ast_grep()` used to call `sys.exit(1)` directly" ? [New info ? corrected to `[Partially resolved]`, then genuinely closed in this commit. The claim was **over-stated when written**, not falsified later: it was true of the one function it examined and was generalized to the file, while `run_ast_grep()` in the same module kept two `sys.exit(1)` calls covering the other ast-grep failure mode. This is the "written ahead of the code" drift direction `CLAUDE.md` names.]



- `claude/steering-prompts/01-testability-research-prompt.md` ? "real, checked-in tests for its two deterministic scripts ? That's solid" ? [Still accurate.]







**Defect 1 ? `capacity_preflight.py` emitted os-native paths into a join that expects forward slashes.** Third occurrence of one bug. `partition_repo.py` carries a seven-line comment recording it being fixed in `spring_drift_check.tier1_scan()` and then in `partition_repo.main()`; this copy was missed both times. It became load-bearing at `cc61fca` ("Point capacity_preflight at the partitioned join it has been ignoring"), which routed these groups into `build_cross_group_edges.build_report()` ? a join by path against `spring_signals.json`'s forward-slash paths. On Windows it matched nothing, and the preflight silently under-reported the fan-out it exists to estimate. Silent because an empty slice is not an error.







Fixed as a *class* rather than an instance, per `10-review-persona-and-standards.md` §1: `partition_repo.to_posix()` / `relpath_posix()` are now the one named home for the rule, both prior sites route through them, and the history lives on the function instead of in a comment asking the next author to remember. A bug fixed three times in three places is the signal that the fix belonged in one place.







Worth recording about the test: a naive "no backslash in the output" assertion is **only non-vacuous on Windows**, since `os.path.relpath` never emits one on POSIX ? it would have passed on CI forever. That is the actual reason the normalization was extracted into a pure function: `to_posix(r"src\main\java\Foo.java")` fails on the pre-fix code on every platform. The existing `test_groups_match_partition_repo_direct_run` had in fact reproduced the buggy line verbatim and compared only counts, which is why it never caught this.







**Defect 2 ? `run_ast_grep()` still called `sys.exit(1)` from library code.** `AstGrepNotFoundError` exists in this exact file because `SystemExit` is a `BaseException` and `unittest`'s `_handleClassSetUp` catches only `Exception`, so a `sys.exit()` under `setUpClass` kills the whole test process with no `Ran N tests` line. That fix converted `find_ast_grep()` only. `scan()` calls `run_ast_grep()`, and three suites call `scan()` from `setUpClass`, so the identical silent death remained reachable whenever ast-grep is *present but fails* ? malformed rule file, bad `--globs`, unparseable output.







Now an `AstGrepError(RuntimeError)` base with `AstGrepNotFoundError` subclassing it, so every existing `except AstGrepNotFoundError` keeps its exact prior meaning; the three CLI entry points catch the base and print the same stderr with the same exit code. Four of the six new tests assert the property that actually matters ? that a plain `except Exception` catches it ? because asserting the exception *type* alone would have been satisfied by `SystemExit` too, which is precisely how this survived the first fix.







Files touched: scripts/capacity_preflight.py, scripts/partition_repo.py, scripts/spring_signal_scan.py, scripts/spring_drift_check.py, scripts/test_capacity_preflight.py, scripts/test_spring_signal_scan.py, scripts/check_code_quality.py, scripts/test_check_code_quality.py, scripts/code_quality_baseline.json, CONSTRAINTS.md, claude/session-log.md







## 2026-07-25 ? Docstring orientation: a stated contract, an enforced check, and the three worst offenders



Commit: 065680a at write time ? see `git log` for this entry's commit



Tests: `test_check_code_quality.py` 46/46 (was 32). Full suite green. Both new checks proven able to fail: renaming a compliant module's `Run with:` marker produced `runnable module, but its 6-line docstring never says how to run it` and exit 1; an untracked probe file was confirmed absent from `measure_tree()`'s output.



Assumptions affected:



- `claude/steering-prompts/13-code-quality-research-prompt.md` ? "the expressiveness work itself ? is scoped below and NOT done" ? [Still accurate. This closes none of `13`'s four open items; docstring orientation was not among them. Worth noting it as a fifth, now done.]



- `CONTRIBUTING.md` ? previously had no statement about code at all, only write-then-verify and a status pointer ? [New info: it now carries a code convention. Anything that assumed CONTRIBUTING.md is purely about process is stale.]







A review reported `scripts/` as hard to follow. The useful part of that review was that it is **not** sloppiness ? it is density, with justification placed before mechanism. Measured across 35 module docstrings: 1,481 lines, mean 42; `spring_drift_check.py` ran to 202 lines with its usage block at line 194, `spring_signal_scan.py` to 152 with none at all. Nine modules had no usage block; fourteen buried it past line 20.







**The density is an asset and is deliberately preserved.** `.ruff.toml` sets the line limit from this repo's own prose distribution on purpose. Nothing here deletes reasoning ? it is reordered, and the change was verified as a move: every substantive sentence of the three restructured docstrings still appears verbatim, except the one-line summaries, which the contract asks to be rewritten. `spring_signal_scan.py` lost zero sentences.







**One argument from the review was rejected.** It proposed moving the essays to `docs/`. This repo's dominant failure mode is prose drifting from code ? prompt `07`'s stale `status:`, `CONSTRAINTS.md` citing a deleted script, `12` naming files that did not exist ? so a standalone rationale doc is the highest-drift-risk location available. Keep it in the file; invert the order. Refined further in discussion: split prose by claim type ? mechanism-explaining comments stay adjacent to code because drift there is a correctness bug, while incident history already has a home in this log and in `CONSTRAINTS.md` and should be referenced rather than restated.







**A defect this work introduced, caught before it shipped.** `measure_tree()` globbed `scripts/*.py`, so regenerating the baseline while a concurrent session's untracked files sat in the tree captured 93 of their functions and raised the annotation floor to 35.4% against a committed tree measuring 23.4%. That fails CI on the first run and blames files that were never committed. Fixed at the cause: the baseline describes the committed tree, so `measure_tree()` now reads `git ls-files`, falling back to the glob outside a checkout. Three regression tests pin it.







**On the threshold, stated honestly because it would be easy to over-trust.** `USAGE_WITHIN_LINES = 20` sits in an 11-line gap in this repo's own bimodal distribution (twelve modules orient by line 18; thirteen bury it at 29+; nothing between). In the threshold-derivation literature's terms that is *unsupervised natural-breaks clustering on a single system, n=25* ? the weakest available basis. The canonical unsupervised method (Alves, Ypma & Visser, ICSM 2010) aggregates across ~100 systems precisely because single-system thresholds are unstable; supervised methods (e.g. `arxiv.org/abs/2602.06831`, 2026) key the cut to a labelled outcome this repo does not have. The only outcome signal here is n=1. So it is recorded as a fact about the current population with a re-derivation command in `CONTRIBUTING.md`, not as a constant to defend.







Not done, deliberately: `scripts/check_repo_claims.py` is another session's untracked work and was **not edited**. Findings for its author ? including a confirmed byte-identical duplicated 8-tuple at `:123-126`/`:137-140`, in the one file whose purpose is preventing exactly that ? are in `claude/check-repo-claims-review-2026-07-25.md`.







Files touched: CONTRIBUTING.md, scripts/check_code_quality.py, scripts/test_check_code_quality.py, scripts/code_quality_baseline.json, scripts/citation_coverage.py, scripts/spring_signal_scan.py, scripts/spring_drift_check.py, claude/check-repo-claims-review-2026-07-25.md, claude/session-log.md







---







