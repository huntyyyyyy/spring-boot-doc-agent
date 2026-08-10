# Session log — 2026-07-24

Lead: **Correct the mirror-back scope, and record what actually needs mirroring**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 2. Newest at the bottom of this file.

---

## 2026-07-24 ? Correct the mirror-back scope, and record what actually needs mirroring



Commit: e0200df



Tests: not run (markdown-only). Verified instead against `git log` per file and against the repo owner's direct read of the Claude project's `steering-prompts/` folder, which holds `00`?`06` and nothing further.



Assumptions affected:



- `claude/steering-prompts/00-shared-research-standards.md` ? "This file and its siblings (`01` through `12`) are mirrored here from the Claude project's `claude/steering-prompts/` docs" ? [Resolved ? false for six of them, and I introduced it: PR #29 widened the original, correct `01`?`05` to `01`?`12` during a docs sweep without checking what the project contains. Corrected to state the real split. `00`?`06` are mirrored and have a canonical project copy; `07`?`09` were authored in this repo (`03cce58`, `f3af862`, `14f7a91`); `10`?`12` were authored outside the project and landed here in `5bd750b`. This is the "prose winning over reality" anti-pattern `claude/10-architecture-maturation-plan.md` §4.3 lists as one this project has actually committed ? committed again here, and the corrected paragraph says so rather than quietly fixing it.]



- `CLAUDE.md` ? "contains thirteen numbered prompts, plus a canonical copy that also lives in this project's attached Claude project", and "no access to the Claude project where the canonical steering prompts live" ? [Resolved ? both implied all thirteen have a project copy. Scoped to `00`?`06` in each place.]



- `claude/session-log.md`'s own 2026-07-24 entry for PR #29 ? "Mirror-back required ... prompts `00`, `10`, `11`, `12` were edited here. The canonical copies in the Claude project need the same edits" ? [Resolved ? superseded and wrong on both ends. `10`/`11`/`12` have no canonical project copy to update, so three of the four named files need nothing. Conversely the real backlog is wider: every one of `00`?`05` has diverged from the initial import. See the manifest below.]



- **The stated mirror direction is inverted from practice** ? [New info ? `00` says the repo copies are mirrored *from* the project, i.e. the project is canonical. Every substantive edit to `00`?`05` since `8bb2404` has been made here instead, under version control (2?3 commits each); nothing has been observed flowing the other way. So the project copies are probably all stale and the repo is the de facto working copy of record. Recorded in `00` itself, with the caveat that if someone *has* been editing the project copies directly, the two have forked and need reconciliation rather than an overwrite ? that's the one thing this session cannot check.]







**Mirror-back manifest ? repo ? project, for a session with project access.** Only these six exist in the project.







*Corrected in place 2026-07-24, before this entry shipped.* The first version of this table derived its `Action` column from **commit counts since the import** and was wrong in two rows: it told a reader to overwrite `02`, which was already byte-identical, and listed `05` as one revision behind when it was two. Commit count is a proxy for divergence; a content diff is the fact. The column below is now the diff. Corrected rather than annotated because this entry has not merged yet ? there was nothing shipped to supersede.







| Prompt | Project copy vs. repo, by content diff | Action needed |



|---|---|---|



| `00-shared-research-standards.md` | Two revisions behind ? matched *no* repo revision, because the import commit `8bb2404` rewrote it rather than copying it | Overwrite |



| `01-testability-research-prompt.md` | Two revisions behind ? same rewrite-at-import cause | Overwrite |



| `02-pluggability-research-prompt.md` | **Byte-identical to the current repo file** | **None** |



| `03-constraints-research-prompt.md` | One revision behind ? matched exactly at `c65d89e` | Overwrite |



| `04-analytics-logging-research-prompt.md` | One revision behind ? matched exactly at `c65d89e` | Overwrite |



| `05-clarity-delivery-trust-research-prompt.md` | Two revisions behind ? matched *no* repo revision, same rewrite-at-import cause | Overwrite |



| `06-wiredrift-check-task-prompt.md` | Matched modulo a missing final newline, which was absent on the **repo** side, not the project's | None to the project copy ? add the newline in the repo. Its `status: not started` frontmatter was stale in *both* copies; corrected in the entry below, on the fourth flag |







`07`?`12` are deliberately absent from this table: they have no project copy, so there is nothing to mirror. Adding them to the project is a separate, optional decision ? not a sync obligation.



Files touched: CLAUDE.md, claude/steering-prompts/00-shared-research-standards.md, claude/session-log.md







---







## 2026-07-24 ? Execute the mirror-back, and replace inference with a content diff



Commit: 065680a



Tests: not run (markdown-only). Verified instead by reading all seven project copies back after writing and comparing byte-for-byte against the repo files ? `cmp -s` reports MATCH on all seven, `02` included (it needed no write). This is the read-after-write rule `CONTRIBUTING.md` states, applied to `project_write` rather than the device bridge.



Assumptions affected:



- `claude/steering-prompts/00-shared-research-standards.md` ? "the project copies of all six are probably stale", and "if someone *has* been editing the project copies directly ... the two have forked" ? [Resolved ? neither held as stated. Every project copy was diffed against *every* historical revision of its repo counterpart. `02` was byte-identical to the current repo file; `06` matched modulo a missing final newline on the repo side; `03` and `04` matched exactly at `c65d89e`. `00`, `01` and `05` matched no revision at all ? because the import commit `8bb2404` **rewrote** them (condensed, and re-worded "in this project" ? "in this repo"), so those three were never in sync at any point and were two revisions behind, not one. No project copy contains an edit that isn't either an exact ancestor of the repo file or the pre-import original, so nobody has edited the project side since creation: not a fork, and the overwrite was safe.]



- `claude/steering-prompts/00-shared-research-standards.md` ? "Nothing has been observed flowing the other way" ? [New info ? falsified, and the direction is subtler than either previous version of this paragraph. Timestamps put every project doc's creation *before* the repo commit carrying the same content (`02`/`03`/`04` created 20:33Z, committed in `c65d89e` at 20:41Z; `06` created 21:45Z, committed in `f38e8df` at 22:48Z). So all seven originated in the project and flowed *into* the repo. What has never happened is the return leg ? which is what this session performed, for the first time.]



- `claude/steering-prompts/06-wiredrift-check-task-prompt.md` ? `status: not started` ? [Resolved ? corrected on the fourth flag rather than deferred a fourth time. Verified before editing: `README.md:39` has the "On drift detection" section, `skills/document-spring-repo/SKILL.md:52` has "Optional pre-flight: checking for drift before a full re-run", and `.github/workflows/ci.yml:48` runs `test_spring_drift_check.py` but never the tool itself ? so "documented but not CI-triggered" is accurate as written. Also added the missing final newline; it was the only file under `claude/steering-prompts/` without one.]



- The mirror-back manifest in the preceding entry ? [Resolved ? executed, and wrong in two rows while it was open. It inferred "needs overwrite" from commit count: `02` had a commit since import but needed no write, and `05` was listed as one revision behind when it was two. Commit count is a proxy for divergence; the diff is the fact. The table itself is corrected in place ? that entry has not merged, so there was no shipped text to supersede ? carrying a short note that the original inferred from commit counts, so the mistake stays legible without leaving a wrong table standing under a warning label.]







**Mirror-back status: done.** All six project copies now match the repo byte-for-byte, verified by read-back. `07`?`12` remain absent from the project by design.







One unresolved naming mismatch, left deliberately: the repo file is `claude/steering-prompts/06-wiredrift-check-task-prompt.md` (no hyphen between "wire" and "drift"); the project doc is `06-wire-drift-check-task-prompt.md`. The project name is the correct spelling, but six repo files reference the repo spelling (`STATUS.md:17`, `claude/llms/pr-3.md:13`, and four lines in this log), so renaming either side is churn that belongs in its own change. Any future mirror must map the two names explicitly or it will create a duplicate project doc.



Files touched: claude/steering-prompts/00-shared-research-standards.md, claude/steering-prompts/06-wiredrift-check-task-prompt.md, claude/session-log.md







---







