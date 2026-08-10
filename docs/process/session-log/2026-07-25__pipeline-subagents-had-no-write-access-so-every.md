# Session log — 2026-07-25

Lead: **Pipeline subagents had no Write access, so every stage's output round-tripped through the orchestrator's context**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 2. Newest at the bottom of this file.

---

## 2026-07-25 ? Pipeline subagents had no Write access, so every stage's output round-tripped through the orchestrator's context



Commit: 065680a



Tests: `test_pipeline_stages.py` 17/17 (1 intentional skip) ? the structural suite that validates these five agent prompts. Full suite 289 passing, 10 skips. All five frontmatter blocks re-parsed after edit: `name`/`description`/`tools` intact, `tools` now `Read, Grep, Glob, Write` on each.



Assumptions affected:



- `skills/document-spring-repo/SKILL.md` Stage 1 ? "Collect results into `summaries.json`" ? [New info ? that collection was happening *through the orchestrating thread's context*, because all five subagents declared `tools: Read, Grep, Glob` with no `Write`. A subagent structurally could not persist its own output, so its entire result had to come back as its final message and be re-serialized by the orchestrator. Measured on the first real run (`spring-petclinic`, 49 Java files, 2 groups): **Stage 1 alone returned ~218k subagent tokens** through the orchestrator before Stage 2 dispatched anything. Stage 4's fourteen concurrent doc-writers, each producing a full markdown document, are several times larger again.]



- `skills/capacity-preflight/SKILL.md` ? "estimated group count and total subagent fan-out across all five stages, estimated size of the repo-wide references bucket attached to every Stage-1 dispatch" ? [New info ? every quantity preflight measures is an **input** quantity: group count, fan-out, and the references bucket sent *in*. Nothing estimates the **return** payload. So the ceiling that actually caps repository size is the one preflight does not look at, and a run can pass it cleanly (`petclinic`: "2 groups, 20 dispatches, no thresholds crossed") while still exhausting the orchestrator on what comes back. Not fixed here ? flagged as the more useful preflight metric than any currently computed.]



- `claude/10-architecture-maturation-plan.md` ? the LLM principles section's "context isolation (siblings share nothing, so anything global must be threaded explicitly ? already learned in `architect-merge`)" ? [Still accurate, and this is the same principle's other half. Siblings sharing nothing is what makes the fan-out safe; it is also what forced every result back through the one thread that *can* see everything. Giving each sibling a write path preserves the isolation while removing the funnel.]







Details: added `Write` to all five agent frontmatter `tools:` lines, and rewrote each agent's output contract to write to an absolute `output_path` supplied by its dispatch, returning only a one-line confirmation. `SKILL.md`'s four dispatch sections now hand out paths instead of collecting payloads ? including passing *paths* to upstream artifacts rather than their contents, since every agent has `Read`.







Two guards written into the agent prompts rather than left implicit, because both failure modes are silent: each agent is told to write to exactly the path given and nowhere else (fourteen doc-writers share one `docs/` directory concurrently, so a duplicated or wrong path destroys a sibling's file with nothing downstream to catch it), and each keeps an inline-output fallback if a dispatch supplies no `output_path`, so an orchestrator that has not been updated degrades to the old behavior rather than losing the output entirely.







`SKILL.md` Stage 4 also gains a post-dispatch `ls docs/*.md | wc -l` check: with writers reporting success by confirmation line rather than by returning content, a writer that failed to write is otherwise indistinguishable from one that succeeded.







Files touched: agents/architect-merge.md, agents/architect-segment.md, agents/doc-writer.md, agents/file-summarizer.md, agents/gap-analyzer.md, skills/document-spring-repo/SKILL.md, claude/session-log.md











---







## 2026-07-25 ? Replace three doc-writer prompt instructions with a mechanical Stage-4 gate



Commit: 065680a



Tests: `test_check_pipeline_output.py` 20/20 (new). `test_pipeline_stages.py` 17/17 after moving `resolve_evidenced_citations()` out of it. Full suite 311 passing, 10 skips. Gate smoke-tested both directions against the real petclinic checkout: a docs dir missing one file and citing a nonexistent path exits **1** and names both failures; a complete, resolvable one exits **0** and prints tag totals.



Assumptions affected:



- `agents/doc-writer.md` rule 4 ? "write to exactly the path given and nowhere else" ? [Resolved ? was a prompt instruction, now a check. The target repo is a clean checkout before a run, so `git status --porcelain` afterwards is an exact record of what the fan-out wrote; anything outside the docs directory is a writer that went where it shouldn't, detected without the agent's cooperation. The prompt line stays as guidance, but it is no longer the control.]



- `claude/llms/README.md`'s "Writing the commands" rules, and this log's own 2026-07-25 entry on deleting `verify_llms_docs.py` ? "a convention is the weakest available guard" ? [New info ? **that reasoning was not applied to my own change.** PR #41 gave five LLM-authored agents `Write` and guarded fourteen concurrent writers sharing one directory with a sentence in a prompt: the same class of control this repo had rejected hours earlier, for the same reason. Caught by the repo owner asking whether the approach deserved re-evaluation, not by me. The inconsistency is the finding; the gate is the fix.]



- `skills/document-spring-repo/SKILL.md` Stage 4's `ls docs/*.md | wc -l` check (added in #41) ? [Resolved ? replaced. Counting to fourteen passes the exact failure it was meant to catch: two writers handed the same `output_path` produce fourteen writes with one name duplicated and another missing. `check_file_set()` compares against the taxonomy's name set instead, and `test_duplicate_output_path_shape_is_caught` pins that distinction.]



- `scripts/test_pipeline_stages.py`'s `resolve_evidenced_citations()` ? "opt-in via `PIPELINE_ARTIFACTS_DIR`, skipped otherwise" ? [New info ? the capability existed and was mentioned once in `SKILL.md`, but nothing ran it as part of a pipeline run. Moved to `doc_tag_utils.py` (where `VALID_DOC_FILES` and `TAG_PATTERNS` already live, and for the same stated reason) so a runtime checker can use it without making a test module a dependency of the pipeline.]







Details: new `scripts/check_pipeline_output.py`, wired into `SKILL.md`'s Output stage as a **gate, not a report** ? the wording matters, since this repo already shipped a CI step named as a gate that could not fail. It checks the fourteen files by name, tag well-formedness, citation resolution against the target repo, and write scope via git.







Deliberately out of scope, and stated in the script's own docstring: whether a resolvable citation actually *supports* the sentence attached to it. That needs a model ? `skills/semantic-pipeline-eval/`'s job. Same boundary `test_pipeline_stages.py` draws around itself.







Not CI-wired, for the same reason `check_no_secrets_leaked.py` isn't: this repo's CI has no target-repo run to check the output of. Its unit tests are wired.







Files touched: scripts/check_pipeline_output.py, scripts/test_check_pipeline_output.py, scripts/doc_tag_utils.py, scripts/test_pipeline_stages.py, skills/document-spring-repo/SKILL.md, .github/workflows/ci.yml, claude/session-log.md







---







