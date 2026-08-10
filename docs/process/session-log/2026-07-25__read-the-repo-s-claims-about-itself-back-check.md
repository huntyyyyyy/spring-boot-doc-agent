# Session log — 2026-07-25

Lead: **Read the repo's claims about itself back: check_repo_claims.py, verify: predicates, derived: blocks**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 2. Newest at the bottom of this file.

---

## 2026-07-25 ? Read the repo's claims about itself back: check_repo_claims.py, verify: predicates, derived: blocks



Commit: 065680a at write time ? see `git log` for this entry's commit



Tests: `test_check_repo_claims.py` 53/53 (new). Full discovery `python3 -m unittest discover -s scripts -p "test_*.py"` ? 471 tests, 14 skipped, 1 expected failure, all green, including the kitchen sink. `ruff check` clean. `check_code_quality.py` clean (annotation coverage rose, the new module being fully annotated). Every one of the five checks was proven non-vacuous by injecting its defect and confirming a non-zero exit, then reverting ? the same posture `test_check_code_quality.py` takes.



Assumptions affected:



- `CLAUDE.md`'s own "The same check covers `CONSTRAINTS.md`" section ? "Nothing mechanical checks these claims; this pass is the only thing standing between them and silent drift" ? [Resolved for the decidable half ? `scripts/check_repo_claims.py` now resolves prompt `verify:` predicates, `derived:` counts, and repo path/`symbol()` references in the current-state docs, blocking, on every CI run. Deliberately **not** resolved for the other half, and the file now says so: whether a `[Resolved]` is *true* is not decidable, and a tag pointing at a file that exists passes while being wrong about what the file does.]



- `claude/steering-prompts/06-wiredrift-check-task-prompt.md`'s `note:` ? "this field read `not started` ... stale for the whole of that window, and flagged three separate times in `claude/session-log.md` before anyone corrected it" ? [Resolved as a class, not an instance. Every prompt carrying a `status:` now carries a `verify:` list of decidable predicates, evaluated in CI. The direction that bit is the one to write for: a `not started` prompt asserts its deliverable is *absent*. This entry is the design decision that being flagged three times without being fixed is a mechanism problem, not an attention problem.]



- `claude/steering-prompts/05-clarity-delivery-trust-research-prompt.md` ? the write-then-verify rule, and `CONTRIBUTING.md`'s note that the `PostToolUse` hook it names is "documented but not wired in" ? [Still accurate, and untouched. CI cannot observe a write tool's response, so that class genuinely needs a hook; `.claude/` still has none. Stated here rather than left implied as covered ? this change addresses the *document*-state half of that prompt's failure mode, not the tool-response half.]



- `claude/steering-prompts/07-ci-scaffold-task-prompt.md` ? "the meta-verification part deliberately withdrawn ... do not re-add it" ? [New info ? that decision is now enforced rather than remembered. `07`'s `verify:` carries `path_absent:scripts/verify_llms_docs.py`, so re-adding the deleted script fails the build.]







Details. Three mechanisms, all deterministic and AI-free.







**`derived:` blocks.** A number in prose becomes an HTML-comment-delimited block naming a derivation key (see `CLAUDE.md` for the literal syntax ? writing it out here would make this line a live claim, which is how the checker first caught its own author, twice); the checker recomputes it and fails on mismatch, `--fix` rewrites. The key charset is `[a-z0-9_]+` and is looked up in a `DERIVATIONS` dict ? markdown can *select* a derivation, never define one. This is deliberate distance from `2f82971`: `verify_llms_docs.py` was deleted for extracting spans from LLM-authored markdown and running them through `bash -c` with `GH_TOKEN` in scope, and `ci.yml` still carries the "do not re-add it" tombstone. `TestNoShellExecution` pins the property four ways, including an AST assertion that every `subprocess` argv in the module is a literal list.







**`verify:` predicates.** Closed vocabulary ? `path_exists:`, `path_absent:`, `contains:<path>:<literal>` ? and an unrecognized predicate fails rather than being skipped, for the same reason.







**Scoping is what makes check B usable, and it took two corrections.** A first run produced 78 findings, nearly all noise: globs, `path:line` anchors, and `pr-N.md` placeholders were being resolved literally, and append-only records were being checked at all. An append-only log correctly cites files that existed when it was written ? `verify_llms_docs.py` was real for 19 PRs ? so check B is scoped to *current-state* docs. A tombstone (`~~struck~~`, or "deleted"/"not in this repo" on the same line) is exempt by kind rather than by baseline, because a baseline entry means "known, unfixed" and that is the wrong label for a sentence which is correct.







**Backtesting is what caught the real design flaw**, and it is the part worth repeating. Reconstructing the renumbering incident ? `12-review-session-launcher.md` telling fresh sessions to read two prompt files where "neither exists" ? showed the checker missing it entirely. Two reasons, both mine: the launcher's payload is one fenced block, which the first draft exempted wholesale, and its paths are bare rather than backticked. Corrected to "a fence hides a *value*, never a *path*", plus a bare-path branch. `TestBacktest` pins both. A checker that passes its own unit tests while missing every historical instance is mis-aimed, and that is invisible from synthetic fixtures.







`ruff` also caught a genuine latent bug in the first draft: a closure defined inside a loop capturing `spans` by reference (B023), correct today only because `sub()` runs in the same iteration.







The baseline (`scripts/repo_claims_baseline.json`) is **empty**. The ratchet exists so adoption need not be a repo-wide prose sweep, but the checks were narrowed until every finding was real rather than accepting a backlog ? worth stating, since an empty baseline and a swallowed one look identical at the green checkmark.







Deliberately out of scope, each stated rather than silently absent: branch protection is still off (`Checks: 0`), so every blocking step here remains advisory until a repo admin runs the `gh api` command `CONSTRAINTS.md` item 6 has carried since 2026-07-23 ? that is the highest-leverage item left. `check_llms_coverage.py` still ships `ENFORCE = False` and `claude/llms/` is several merged PRs behind; check E now at least enforces that its step name says "non-blocking". `baseline-reference/` holds five frozen forks of live files with no documented sync mechanism and nothing checking them.







Files touched: scripts/check_repo_claims.py, scripts/test_check_repo_claims.py, scripts/repo_claims_baseline.json, .claude/skills/verify-state-claims/SKILL.md, .claude/settings.json, .github/workflows/ci.yml, CLAUDE.md, CONSTRAINTS.md, claude/steering-prompts/01..09,13 (verify: frontmatter), claude/session-log.md







## 2026-07-25 ? Content fingerprints with the normalization level in the data, and a directional-tests skill



Commit: 065680a at write time ? see `git log` for this entry's commit



Tests: `test_ast_signature.py` 13/13 new, CI-wired. Full suite green. Non-vacuity proven by injecting three mutations ? `t2` no longer stripping docstrings, the default reverted to `t1`, and an unknown level accepted silently ? each of which turns the suite red; restoring returns it to green.



Assumptions affected:



- `claude/steering-prompts/01-testability-research-prompt.md` ? `status:` claimed `test_pipeline_stages.py` was "(17/17 passing)" ? [Resolved ? stale by 12; the suite runs 29. Replaced with the command, per `CLAUDE.md`'s own prescribed fix.]



- `claude/steering-prompts/04-analytics-logging-research-prompt.md` ? `status:` claimed `test_run_manifest.py` was "(31/31)" ? [Still accurate as of 2026-07-25, and replaced with the command anyway. A hardcoded count that happens to be true today is the same latent defect as `01`'s, one commit earlier in its life.]



- Swept `00`?`13` for the same shape: **`07`?`13` carry no hardcoded counts at all.** The defect is confined to the mirrored range, which is consistent with `CLAUDE.md`'s rule postdating those files.







**MIRROR OBLIGATION ? this session cannot discharge it.** `01` and `04` are both in the `00`?`06` mirrored range, so their canonical copies in the Claude project ("Plugin For Asynchronous Documentation Creation") now differ from this repo. A project-connected session should copy both `status:` fields back. Flagged here because `claude/session-log.md` is the only channel that crosses that gap ? a CLI session has git but no project access, and the reverse for a Cowork session.







**The substance: a digest is not comparable to anything unless its normalization travels with it.**







`scripts/_ast_signature.py` returns `level:digest`, never a bare hash. Three levels, named after the clone-detection taxonomy (Zhang & Saber, `arXiv:2506.14470` §II-A, opened and quoted rather than paraphrased): `raw` (bytes), `t1` (Type-1 ? `ast.dump(include_attributes=False)`, so comments and formatting vanish), `t2` (`t1` plus docstrings, which are string literals and therefore a deliberately *partial* Type-2).







Measured across 14 modules here, `t1` and `t2` agree on **zero**. So a stored digest with no level attached cannot be interpreted, and if a default ever changed, every existing digest would silently become incomparable while the checker kept reporting confidently. That is the reason the level is in the data rather than in a flag.







**The default was reversed by measurement, which is the part worth keeping.** The first draft defaulted to `t1` on the principled grounds that it is the standard equivalence class and that module docstrings here are user-facing (12 scripts pass `description=__doc__` to argparse, so a module docstring *is* the `--help` text). Then PR #49 was measured properly: 18, 12 and 11 changed lines across three modules, with **zero** changed lines outside the docstring in all three. Under `t1` that single PR stales every claim about those modules for a change that altered nothing executable ? and 15 more modules are queued for identical treatment by the docstring contract. Error costs are asymmetric: a false positive does not cost one wasted check, it costs the checker, because someone switches it off. Default is `t2`; `t1` stays available and named.







`skills/directional-tests/SKILL.md` codifies the discipline behind those tests: name the property rather than the function, prove the gate can fail by injection, assert the exit code rather than an internal issues list, prefer an invariant to a probe, and ? the rule this repo keeps re-learning ? ensure the assertion is non-vacuous on every platform it runs on, and no wider than its own name. Every rule is tied to a real incident here rather than a principle borrowed from a book.







Two things caught me while doing it, both worth recording. `check_repo_claims.py`'s check D failed the build because `test_ast_signature.py` existed but was not wired into `ci.yml` ? rule 9 of the skill enforced on its author within minutes of writing it. And the annotation-coverage floor moved 37.9% ? 39.0%, re-baselined so the gain cannot silently regress.







Files touched: scripts/_ast_signature.py, scripts/test_ast_signature.py, skills/directional-tests/SKILL.md, .github/workflows/ci.yml, scripts/code_quality_baseline.json, claude/steering-prompts/01-testability-research-prompt.md, claude/steering-prompts/04-analytics-logging-research-prompt.md, claude/session-log.md







