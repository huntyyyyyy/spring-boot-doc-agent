# Session log — 2026-07-23 → 2026-07-24

Lead: **Add scripts/test_pipeline_stages.py (structural tests for the four LLM stages)**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 4. Newest at the bottom of this file.

---

## 2026-07-23 ? Add scripts/test_pipeline_stages.py (structural tests for the four LLM stages)



Commit: 3eb1551



Tests: 17/17 passing (`python3 scripts/test_pipeline_stages.py -v`), 1 opt-in test class correctly skipped (PIPELINE_ARTIFACTS_DIR unset)



Assumptions affected:



- `claude/steering-prompts/01-testability-research-prompt.md` ? "The gap": "Nothing tests the four LLM stages... A prompt regression in any of these five agent files is currently invisible except by a human reading generated output and noticing something's wrong." ? [Resolved ? `scripts/test_pipeline_stages.py` adds mechanical structural tests: exact five-form tag-grammar validation (regression-tested against a wrong-dash substitution and a missing-citation case), `[Evidenced ? path:line]` citation resolution against `scripts/test_fixtures/spring_signals/` (the existing fixture, deliberately reused rather than building a second one ? see item 1/4 of `IMPLEMENTATION_HANDOFF.md` for why a second independently-maintained fixture tree is a known drift risk in this project specifically), `file-summarizer`/`gap-analyzer` JSON output-shape validation, and architecture-node traceability. An opt-in real-artifacts pass (`PIPELINE_ARTIFACTS_DIR` env var, same pattern as `test_partition_repo_real_world.py`) validates a real completed run's actual output when available; the default synthetic-data pass requires no LLM calls and no new dependencies.]



- `claude/steering-prompts/01-testability-research-prompt.md` ? research ask (arXiv precedent for structured-claim/citation LLM pipeline eval, GitHub eval-harness survey) ? [New info ? two arXiv papers verified directly at `arxiv.org/abs/<id>`: arXiv:2604.25359 ("The Structured Output Benchmark") shows schema compliance and value accuracy diverge sharply (near-perfect JSON schema conformance vs. 83.0%/67.2%/23.7% value accuracy on text/image/audio) ? direct precedent for why this suite checks citation *resolvability*, not just tag *shape*; arXiv:2605.01604 ("Evaluating Agentic AI in the Wild") names a production-evaluation gap between healthy system metrics and silently degrading quality, matching this project's own reasoning for mechanical-over-LLM-judge checks. GitHub: `promptfoo/promptfoo` confirmed via `gh api` at 23,537 stars, pushed same day as this research ? a real, current, well-maintained precedent for deterministic/schema assertions over LLM-graded ones ? but it's a Node.js tool, so adopting it directly would add exactly the kind of new-dependency/new-service cost `00-shared-research-standards.md`'s "what scaffold and implement means" section says to avoid; built a small stdlib-only Python equivalent tailored to this project's five-tag scheme instead of wiring in the external tool.]



- `claude/steering-prompts/01-testability-research-prompt.md` ? "What to scaffold and implement" item 1, "a small synthetic Spring Boot repo fixture... sized to exercise all five agent stages" ? [New info ? no new fixture was built; `scripts/test_fixtures/spring_signals/` (controller, entities, repositories, security annotation, config, Dockerfile) already covers what citation-resolution testing needs, and reusing it was a deliberate choice, not an oversight, given this project's prior two-sources-of-truth incidents. Worth reconciling explicitly if a future session reads the original prompt text and expects a distinct fixture directory to exist.]



- `STATUS.md` ? "Done, confirmed delivered" and "Next concrete action" sections ? [Resolved ? updated in the same commit to move this item from Pending to Done and repoint the next-action pointer at `02-pluggability-research-prompt.md` / the `CONSTRAINTS.md` close-out order.]



Files touched: scripts/test_pipeline_stages.py, skills/document-spring-repo/SKILL.md, README.md, STATUS.md, claude/steering-prompts/01-testability-research-prompt.md, claude/session-log.md







---







## 2026-07-23 ? Add scripts/verify_llms_docs.py and this repo's first CI workflow



Commit: d54cc8a



Tests: 17/17 passing (`python3 scripts/test_verify_llms_docs.py -v`); `python3 scripts/verify_llms_docs.py` itself reports 46/46 documented `claude/llms/pr-*.md` commands passing, 0 failed, 0 skipped, against the real repo; all four pre-existing suites (`test_spring_signal_scan.py` 32/32, `test_partition_repo.py` 13/13, `test_spring_drift_check.py` 12/12, `test_pipeline_stages.py` 17/17 with 1 correctly skipped) re-run clean locally as a baseline before pushing.



Assumptions affected:



- `claude/steering-prompts/07-ci-scaffold-task-prompt.md` ? the task itself, "scaffold this repo's first CI job, plus a meta-verification script for `claude/llms/`" ? [Resolved ? `scripts/verify_llms_docs.py` parses each `pr-*.md`'s `## Deterministic verification` section, associates each inline-backtick command with its numbered claim, and re-runs it (plain one-liners via `bash -o pipefail`; the `git worktree add && cd && <rest>; cd - && git worktree remove` compound shape decomposed into explicit add/run/remove-in-`finally` steps so a real test failure inside that shape can't be masked by the trailing cleanup's own exit code, or by a `| tail -N` inside `<rest>`). `.github/workflows/ci.yml` runs it, plus the four existing suites, on `pull_request`/`push` to `main`, with `fetch-depth: 0` (most commands read old SHAs via `git show <sha>:path`, which needs full history) and `ast-grep` installed via `pip install ast-grep-cli` rather than a slow `cargo install`. Branch protection requiring this check is deliberately not touched ? see `CONSTRAINTS.md` item 6 for the exact follow-up `gh api` command.]



- `CONSTRAINTS.md` ? "Integration gaps" item 4, "`claude/llms/pr-N.md`'s deterministic-verification commands have no automated re-check ? a meta-drift risk" ? [Resolved, with a stated residual gap ? the new script re-runs every command on each CI run and fails the build on error, but deliberately does not semantically diff real output against each free-text `Expect:` line (an explicit, stated scope boundary, not an oversight, per `01-testability-research-prompt.md`'s "mechanical wherever possible" precedent).]



- `CONSTRAINTS.md` ? "Integration gaps" item 2, "No CI/CD wiring anywhere in this repo" ? [Resolved ? see `.github/workflows/ci.yml` above.]



- `CONSTRAINTS.md` ? "Enterprise-readiness gaps" item 6, "PRs land with zero required status checks..." ? [New info ? a required-check candidate now exists (the CI workflow), narrowing but not closing this gap: nothing yet makes it *required*, and reviews still aren't required either. Marked "partially resolved" with the exact `gh api` command a repo admin would run, not run here.]



- Live drift found and fixed while building this, not merely theoretical: `claude/llms/pr-8.md` and `claude/llms/README.md` still said `state: OPEN`/"still open" for PR #8, which had actually already merged to `main` as `a0acc76` ? repinned all six of that file's commands from the head commit to the merge commit and re-verified each one (confirmed `a0acc76`'s tree is byte-identical to the head commit's, i.e. a true merge, not a squash/rebase, so no command's expected output changed). Concrete evidence for `CONSTRAINTS.md` item 4's premise, not just an argument for it.



- A real, Windows-specific bug found and fixed during manual testing of `verify_llms_docs.py`, worth flagging for any future session touching subprocess+`git worktree` code on this repo: invoking `git worktree add` directly via a list-form `subprocess.run(["git", ...])` resolves a bare `/tmp/...` path differently than `bash -c "git worktree add /tmp/..."` does (native git.exe vs. Git Bash's own MSYS path translation) ? mixing the two silently orphans the worktree (registered in `git worktree list`, but unremovable at the path bash later tries). Fixed by routing every step (`add`, running `<rest>`, `remove`) through the same `bash -c` invocation.



Files touched: scripts/verify_llms_docs.py, scripts/test_verify_llms_docs.py, .github/workflows/ci.yml, claude/llms/pr-8.md, claude/llms/README.md, CONSTRAINTS.md, STATUS.md, claude/session-log.md







---







## 2026-07-24 ? Add scripts/_secret_heuristics.py (redaction_zones + check_no_secrets_leaked.py)



Commit: 04f3ad5



Tests: 13/13 passing (`python3 scripts/test_secret_heuristics.py -v`); all five pre-existing suites re-run clean (`test_spring_signal_scan.py` 32/32, `test_partition_repo.py` 13/13, `test_spring_drift_check.py` 12/12, `test_pipeline_stages.py` 17/17 with 1 correctly skipped, `test_verify_llms_docs.py` 17/17); `verify_llms_docs.py` re-run once more, still 46/46 against the real repo (unaffected by this change, checked anyway since it touches scripts/).



Assumptions affected:



- `CONSTRAINTS.md` ? "Confidentiality/handling rules" item 2, "Secret/credential leakage into generated docs ? a real, currently unmitigated gap... nothing in `agents/*.md` or `doc-taxonomy.md` instructs a subagent to redact a real secret value it encounters" ? [Resolved, heuristically ? not a guarantee. `scripts/_secret_heuristics.py` (new shared module, same single-source-of-truth role `_shared_excludes.py` already plays for excluded dirs) detects secret-shaped `key: value` lines (non-placeholder literal under a password/secret/token/credential-shaped key name) plus two key-agnostic patterns (AWS access key IDs, PEM private-key blocks). `spring_signal_scan.py` now runs it against configuration/deployment files during its existing walk (no second directory pass) and records line+heuristic ? never the matched value ? as a new `redaction_zones` map, bumping `schema_version` to 4. `agents/file-summarizer.md` and `agents/doc-writer.md` are both instructed to never transcribe a flagged line's value (doc-writer needed its own instruction too, not just file-summarizer's ? it has direct `Read` access and can bypass file-summarizer's output entirely by reading a config file itself). `doc-taxonomy.md`'s configuration.md notes now say so explicitly, closing the exact sentence CONSTRAINTS.md quoted ("only says not to fabricate... says nothing about not echoing a real one"). Defense in depth beyond the prompt instruction: `scripts/check_no_secrets_leaked.py` re-applies the same heuristics to a completed run's own output (`summaries.json`, `docs/*.md`) and fails loudly if a credential-shaped value made it through anyway ? documented in `SKILL.md` as an optional post-run check (same posture as `spring_drift_check.py`'s own optional pre-flight section), not CI-wired, since this repo's own CI has no target-repo pipeline output to check.]



- Stated, not silently absent, residual scope on the above: the key-name heuristic only fires when the secret-shaped key is the line's own key (a reproduced config snippet, e.g. in a fenced code block) ? a value transcribed into free-text prose under an unrelated key (e.g. a `"summary"` field mentioning a password inline) is not caught unless it also matches one of the two key-agnostic patterns. Noted in `_secret_heuristics.py`'s own docstring and in its test file, not just asserted here.



Files touched: scripts/_secret_heuristics.py, scripts/check_no_secrets_leaked.py, scripts/test_secret_heuristics.py, scripts/spring_signal_scan.py, agents/file-summarizer.md, agents/doc-writer.md, skills/document-spring-repo/references/doc-taxonomy.md, skills/document-spring-repo/SKILL.md, .github/workflows/ci.yml, CONSTRAINTS.md, STATUS.md, claude/session-log.md







---







## 2026-07-24 ? Add config_key_sets + spring_drift_check.py structural-vs-value-only config drift



Commit: da5785b (same PR/branch as the entry above ? this refines that unmerged change, not a new one)



Tests: 12/12 passing (`python3 scripts/test_config_keys.py -v`); `test_spring_drift_check.py` grew from 12 to 14 (two new cases for the statuses below); all seven suites re-run clean (`test_spring_signal_scan.py` 32/32, `test_partition_repo.py` 13/13, `test_spring_drift_check.py` 14/14, `test_pipeline_stages.py` 17/17 with 1 correctly skipped, `test_secret_heuristics.py` 13/13, `test_config_keys.py` 12/12, `test_verify_llms_docs.py` 17/17).



Assumptions affected:



- Real-world context supplied directly by the repo owner, not derivable from the code: in their actual usage, the config files this pipeline scans are checked-in placeholders/dummies ? real values are injected by an external service at deploy time. Given that, a value-content-based secret heuristic (the prior session-log entry, still kept as a complementary check) matters less than a different signal: whether a config file's *key set* changed (expected ? the config's own schema evolving) versus the exact same keys now holding different values with no structural reason to touch the file at all (anomalous in that architecture, worth a human look). This directly refines how `CONSTRAINTS.md`'s "Secret/credential leakage" entry should be read for repos shaped this way ? noted there explicitly rather than only in this log.



- `spring_signal_scan.py`: added `config_key_sets` (schema_version 4 -> 5), a {file: [dotted.key.path, ...]} map for configuration/deployment files, extracted mechanically via a new `scripts/_config_keys.py` module ? deliberately not a PyYAML dependency (this project has none), an indentation-stack walk that only needs key *paths*, not real YAML value/type parsing. Names only, never values, same posture as `redaction_zones`.



- `spring_drift_check.py`: files with no `rule_id` (config/deployment/migration evidence) previously always fell back to the generic `suspected_drift_content_changed_no_rule_to_recheck` status. Files with a `config_key_sets` entry now get a real tier-2-style recheck instead: `config_structure_changed` (keys added/removed) versus `config_values_only_changed_review_needed` (identical key set, content hash still changed ? a value changed under an unchanged key). Files predating schema_version 5 in their prior scan still get the original generic fallback ? additive, not a hard requirement bump.



- Manually verified end-to-end against a scratch copy of the fixture repo, not just via unit tests: changing `application-local.yml`'s `port` value alone produced `config_values_only_changed_review_needed`; adding a new sibling key produced `config_structure_changed` with the added/removed key names in the detail string.



Files touched: scripts/_config_keys.py, scripts/test_config_keys.py, scripts/spring_signal_scan.py, scripts/spring_drift_check.py, scripts/test_spring_drift_check.py, skills/document-spring-repo/SKILL.md, .github/workflows/ci.yml, CONSTRAINTS.md, STATUS.md, claude/session-log.md



---







