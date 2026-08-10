# Session log — 2026-07-25

Lead: **Delete verify_llms_docs.py: markdown?`bash -c` execution with GH_TOKEN in CI**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 2. Newest at the bottom of this file.

---

## 2026-07-25 ? Delete verify_llms_docs.py: markdown?`bash -c` execution with GH_TOKEN in CI



Commit: 065680a



Tests: 219 passing, 6 intentional skips (`python -m unittest discover -s scripts -p "test_*.py"`) ? the 236 baseline minus exactly the 17 tests in the deleted `test_verify_llms_docs.py`, no other suite affected. `.github/workflows/ci.yml` re-parsed with `yaml.safe_load`: 15 steps (was 17), no `run:` mentions `verify_llms_docs`, and `GH_TOKEN` now appears on exactly one step (`check_llms_coverage.py`), which calls the `gh` API and executes nothing derived from markdown. Confirmed no script anywhere still pipes text to a shell (`grep -rn 'bash", "-o\|bash", "-c\|shell=True' scripts/` ? no matches).



Assumptions affected:



- `claude/10-architecture-maturation-plan.md` scrap item 2 ? "`verify_llms_docs.py`'s markdown?`bash -c` execution. Delete the mechanism; keep the intent." ? [Resolved ? done as specified. `claude/llms/pr-*.md` survives as a human-read convention; only the automation is gone.]



- `claude/10-architecture-maturation-plan.md` 0.1.3 ? "The C1 exposure is closed by omission. The new workflow never invokes `verify_llms_docs.py`" ? [Resolved, by a different route than specified. 0.1.3 assumed the exposure would close when a *new* workflow landed without the script (0.1.1, not yet built). Removing the step from the *existing* workflow reaches the same end state now rather than waiting on a rewrite. The "do not re-add it" instruction still governs whatever 0.1.1 eventually lands.]



- `claude/10-architecture-maturation-plan.md` 0.1.6 ? the `shlex.split()` ? `subprocess.run(argv, shell=False)` rewrite with a `git log -1; touch /tmp/pwned` regression fixture ? [Resolved ? moot. 0.1.6 is explicitly "conditional on 0.1.5 keeping the script." It was not kept, so the rewrite and its fixture disappear with it.]



- `claude/steering-prompts/07-ci-scaffold-task-prompt.md` ? scaffold item 1, "`scripts/verify_llms_docs.py` ? stdlib-only, matching this repo's existing scripts' dependency discipline" ? [New info ? the prompt's own deliverable is deleted, not replaced by a better version. It was built as specified and behaved as specified; the specification was the problem. The prompt's other deliverable, the CI workflow, stands. Read item 1 as history, not as work to do.]



- `claude/steering-prompts/08-dependency-pinning-task-prompt.md` ? "Re-run all nine existing test suites plus the meta-verification script" ? [New info ? eight suites now, and there is no meta-verification script. The listed commands are otherwise unchanged.]



- `CONSTRAINTS.md` "Integration gaps" item 4 ? "[Resolved, with a stated residual gap] ... now have an automated re-check" ? [New info ? reopened deliberately, marked in place rather than deleted. The gap is real again: nothing notices a drifted verification command.]







Details: the script extracted backtick-fenced spans matching `^(git|gh)\s` from `claude/llms/pr-*.md` and passed each to `bash -o pipefail -c` with `GH_TOKEN` in scope, on every `pull_request` and `push` to `main`. Because the match was on prefix, any `;` inside a span was arbitrary code execution ? reproduced against HEAD: `git log -1; echo INJECTED > <path>` was graded PASS and the file was written. These files are LLM-authored, so the realistic path is not an attacker but an agent, and it fired benignly during this session: prose in a `pr-N.md` draft merely *named* a git subcommand in backticks, and CI executed it three times, leaving a stray `.git/rebase-apply` until it was aborted by hand.







Deletion rather than hardening, because every mitigation (`shlex.split`, argument allowlist, positional marking) hardens a parser that should not exist, and one is impossible in principle: distinguishing a command from the *name* of a command in prose is undecidable. An audit taken while sizing the alternative found the automation was also buying very little ? of 160 extracted commands, 143 read pinned objects whose output cannot change, 9 re-run test suites at old commits against a *present-day* environment (one via `pip install` inside the worktree), and 3 hit the live GitHub API. About 20 terminate in a stage that cannot fail at all.







Files touched: scripts/verify_llms_docs.py (deleted), scripts/test_verify_llms_docs.py (deleted), .github/workflows/ci.yml, claude/llms/README.md, STATUS.md, CONSTRAINTS.md, claude/session-log.md







---







## 2026-07-25 ? partition_repo.py emitted OS-native paths, silently emptying Stage 1's evidence slices



Commit: 065680a



Tests: `test_partition_repo.py` 13 ? 15 (two new cases in `EmittedPathSeparatorTest`). Negative control run against `git show HEAD:scripts/partition_repo.py`: pre-fix emits `src\main\java\com\example\T.java` (1 path containing a backslash), post-fix emits `src/main/java/com/example/T.java` (0). Full suite green.



Assumptions affected:



- **This plugin had never been run end-to-end against a real Spring Boot repository.** ? [Resolved ? first real run performed, against `spring-projects/spring-petclinic` at `f182358` (49 Java files, 130 tracked). Stage 0 completes and its deterministic output is accurate where hand-checkable: all six `entity_table_map` entries correct (`Vet?vets`, `Specialty?specialties`, `Pet?pets`, `PetType?types`, `Visit?visits`, `Owner?owners`), `security: 0` correct for a repo with no Spring Security, and `redaction_zones` correctly flags `k8s/db.yml:14` as a password-shaped key without transcribing its value.]



- `claude/session-log.md`'s 2026-07-23 entry ? "a real Windows path-separator bug in `spring_drift_check.py`'s `tier1_scan()` (raw `os.path.relpath()` instead of normalizing to forward slashes like `spring_signal_scan.py` does everywhere else)" ? [New info ? **third instance of the same bug class**, now in `partition_repo.py`. The repo has fixed this twice and reintroduced it a third time, which argues it is a missing invariant rather than three coincidences: any path a script *emits* must be forward-slash normalized, because these JSON artifacts are joined by path across scripts. Worth a shared helper or a lint, not a third point fix.]



- `skills/document-spring-repo/SKILL.md` Stage 1 ? "give each one its group's file list **and** the relevant slice of `spring_signals.json` (matches whose `file` field falls in that group) so it isn't rediscovering annotations the ast-grep pass already found" ? [New info ? on Windows this slice was **empty for every dispatch** before this fix, and failed silently. `groups.json` carried `src\main\...` while `spring_signals.json` carried `src/main/...`, so 54 of 55 cited files matched no group. The stage would still complete ? subagents read files themselves ? while doing exactly the rediscovery the design exists to prevent. After the fix: 0 unmatched, 61 evidence items distributed across the two groups.]







Details: `partition_repo.py` already had a `_relpath()` helper (line ~149) that normalizes, but it is used only for gitignore matching. The emitted path at line ~305 used a raw `os.path.relpath()`. Twelve lines apart.







The failure mode is the notable part: no error, no warning, no empty-output signal. The pipeline completes and produces plausible documentation built on an evidence slice that silently contained nothing. Only a real end-to-end run surfaced it ? no unit test covered the *emitted* path format, and the structural suites all pass either way.







Files touched: scripts/partition_repo.py, scripts/test_partition_repo.py, claude/tool-quirks.md, claude/session-log.md







---







