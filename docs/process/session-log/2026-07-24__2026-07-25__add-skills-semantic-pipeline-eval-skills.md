# Session log — 2026-07-24 → 2026-07-25

Lead: **Add skills/semantic-pipeline-eval/, skills/capacity-preflight/, and MATURITY_ASSESSMENT.md**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 4. Newest at the bottom of this file.

---

## 2026-07-24 ? Add skills/semantic-pipeline-eval/, skills/capacity-preflight/, and MATURITY_ASSESSMENT.md



Commit: 3254d67



Tests: 19/19 passing (`python3 scripts/test_semantic_eval_helpers.py -v`); 9/9 passing (`python3 scripts/test_capacity_preflight.py -v`); all seven pre-existing suites re-run clean (`test_spring_signal_scan.py` 32/32, `test_partition_repo.py` 13/13, `test_spring_drift_check.py` 14/14, `test_pipeline_stages.py` 17/17 with 1 correctly skipped, `test_secret_heuristics.py` 13/13, `test_config_keys.py` 12/12, `test_verify_llms_docs.py` 17/17); `verify_llms_docs.py` re-run once more, still 46/46 against the real repo.







**Self-review catch, worth recording since it's exactly the failure mode this project's own conventions exist to prevent**: the design pass that produced this change's plan named `check_mermaid_syntax()`'s scope as "bracket/edge-balance + undefined-node-ref checks," but the first implementation only shipped bracket/paren/brace/subgraph/quote balance ? the undefined-node-ref check was silently dropped between plan and code, with `SKILL.md`, `eval-rubric.md`, and the function's own docstring all independently describing only the narrower three-check scope as if it were the full original intent. Caught in review before this entry was finalized, not after: `find_undefined_node_refs()` was added (flags an edge endpoint identifier that never receives a real label anywhere in the diagram ? deliberately distinct from `test_pipeline_stages.py`'s `find_untraceable_nodes()`, which checks whether an *existing* label is a real file/class name), wired into `check_mermaid_syntax()`'s findings, and covered by 5 new tests (all-labeled passes, never-labeled endpoint flagged, label-appears-later-in-diagram not flagged, fabricated-but-present label correctly left to the separate traceability check, plus 4 fuzzy-match-threshold boundary tests for `find_unmatched_confirmed_tags()` added in the same pass: exactly-at-threshold not flagged, just-below flagged, and a test confirming the `overlap_threshold` parameter is actually load-bearing). `SKILL.md`, `eval-rubric.md`, and the module docstring all updated to describe the real, now-complete scope.



Assumptions affected:



- `claude/steering-prompts/01-testability-research-prompt.md` ? "What to scaffold" originally deferred a "narrow, LLM-as-judge fallback for genuinely qualitative judgments" beyond the mechanical suite it asked for ? [New info, partially resolved ? `skills/semantic-pipeline-eval/` now scaffolds exactly that: samples `[Evidenced]` claims for truthfulness, flags unmatched `[Confirmed]` tags and Mermaid syntax issues via a new mechanical pre-pass (`scripts/semantic_eval_helpers.py`), checks for cross-doc/cross-diagram contradiction, and routes findings through a two-lane human sign-off (always-escalate certain finding types, plus a random confidence spot-check over the judge's own non-escalated "Supported" verdicts, sized `clamp(ceil(0.10*count), min=3, max=12)` ? not a bare `min(3, ...)`, which would cap the spot-check at exactly 3 regardless of run size and defeat the point of catching a systematic judge bias at scale). This is a manually-invoked skill, not a CI-integrated check (it requires a live LLM-driven session), so the prompt's frontmatter status is updated to "partially resolved" rather than fully closed ? see that file's own status line.]



- `claude/steering-prompts/02-pluggability-research-prompt.md` ? "no schema, no validation, just shared understanding documented in prose" across the four inter-stage JSON artifacts ? [Still accurate ? both new scripts (`semantic_eval_helpers.py` reading `interview_answers.json`/doc output, `capacity_preflight.py` reading `groups.json`/`spring_signals.json`) are two more consumers of these unschema'd contracts, raising the cost of ever changing their shape without a schema, but the schema/validation gap itself is untouched by this change.]



- `claude/steering-prompts/03-constraints-research-prompt.md` (via `CONSTRAINTS.md`'s "Known precision tradeoffs" item 3 and `SKILL.md`'s own "worth confirming against a real repo's actual size" note on the `references` bucket) ? [New info ? `skills/capacity-preflight/` and `scripts/capacity_preflight.py` now compute this as a concrete, per-repo number (group count, total subagent fan-out = `2*num_groups + 16`, references-bucket-tokens × num_groups) instead of leaving it as an unmeasured assumption. Only run against the small `scripts/test_fixtures/spring_signals/` fixture so far (1 group, 18 dispatches, ~783 est. tokens) ? not yet validated against a real large/monorepo target, so the warning thresholds themselves remain stated guesses, not calibrated values.]



- `claude/steering-prompts/04-analytics-logging-research-prompt.md` ? item 2, a `run_manifest.json` recording per-stage timing/pass-fail/evidence-tag counts, still not built ? [New info, not resolved ? `capacity-preflight` is a pre-run estimate only; it doesn't close this gap, but a future `run_manifest.json` should record its predicted numbers (group count, fan-out, references-bucket tokens) alongside the run's actual observed values, closing a calibration loop this prompt didn't previously name. Worth folding into that prompt's scope if it's picked up next.]



- `CONSTRAINTS.md` ? "Enterprise-readiness gaps" item 1 stated the license as `"UNLICENSED"` ? [Resolved, and this was stale documentation, not a new decision: `.claude-plugin/plugin.json`'s `license` field already reads `"MIT"`, confirmed directly against the live file during this audit. Corrected in `CONSTRAINTS.md` and `STATUS.md`'s "Pending" section, which both still said `UNLICENSED`. Exactly the kind of doc/reality drift this project's own tooling (`verify_llms_docs.py`, `spring_drift_check.py`) exists to catch elsewhere ? caught here by direct inspection instead, since neither tool covers plugin.json's own fields.]



- `MATURITY_ASSESSMENT.md` (new, root level) ? a maturity scorecard (testing depth, scalability, schema/contract rigor, observability, security/governance, dependency reproducibility, documentation quality), a drift-from-modern-practice section (schema-validated contracts, semantic-eval harnesses, enforced branch protection, dependency lockfiles ? all named as baseline practice this repo falls short of, with citations back to `CONSTRAINTS.md` and this project's own prior arXiv/GitHub research), and an adoption gate checklist, cross-linked from `README.md` and `STATUS.md`.



Files touched: skills/semantic-pipeline-eval/SKILL.md, skills/semantic-pipeline-eval/references/eval-rubric.md, scripts/semantic_eval_helpers.py, scripts/test_semantic_eval_helpers.py, skills/capacity-preflight/SKILL.md, scripts/capacity_preflight.py, scripts/test_capacity_preflight.py, MATURITY_ASSESSMENT.md, .github/workflows/ci.yml, README.md, STATUS.md, CONSTRAINTS.md, claude/steering-prompts/01-testability-research-prompt.md, claude/session-log.md







---







## 2026-07-24 ? Add skills/tool-quirks/ + claude/tool-quirks.md, and claude/llms/pr-13.md



Commit: 23fb730



Tests: not applicable ? no scripts/agents/*.md logic touched; verified claude/llms/pr-13.md's own claims directly against commit `3254d67` (git show/grep for each numbered claim, plus a `git worktree add` re-run of `test_spring_signal_scan.py` 32/32, `test_partition_repo.py` 13/13, `test_pipeline_stages.py` 17/17-with-1-skipped) before writing the file, not after.



Assumptions affected:



- `claude/steering-prompts/05-clarity-delivery-trust-research-prompt.md` ? this prompt's own motivating incidents (a device-bridge write reporting success while the file's actual content stayed unchanged; a stray-scaffolding-commit/stale-branch-assumption incident) are the same class of bug as a new one caught this session: `gh pr create --title ... --body ...` produced a PR whose stored title/body didn't match what was passed (a truncated title, the raw commit message as the body). ? [New info ? this is a fresh, concrete instance of the exact "tool reports success, real state differs" pattern this prompt's write-then-verify rule already exists for, now recorded in a new, dedicated, searchable index (`claude/tool-quirks.md`, via `skills/tool-quirks/SKILL.md`) rather than only living as one-off incident prose in this log or in `CONTRIBUTING.md`. Root cause of the `gh pr create` incident specifically stayed unresolved after a real investigation (no local/global git hooks, no repo webhooks, no installed GitHub Apps, and this repo's own prior 5 merged PRs didn't show the same pattern in the same non-TTY environment) ? logged as `[Unresolved ? needs research]`, not force-resolved.]



- Separately, a read-only Cowork session (no git/gh access) tried to review PR #13 via GitHub's web "Files changed" tab and got an incompletely-loaded diff (JS-rendered progressive loading; 8 of 12 files never resolved past "Loading?"), which it correctly declined to treat as a full review. Logged as a second `claude/tool-quirks.md` entry, resolved via two fixes needing no new tooling: GitHub's REST API / `raw.githubusercontent.com` return plain JSON/text (not JS-rendered) for the same content; and `claude/llms/pr-N.md` (confirmed directly against `scripts/verify_llms_docs.py` and `claude/llms/README.md`) already supports pinning to a still-open PR's head commit, not only a merged one ? so `claude/llms/pr-13.md` was added now, before merge, giving any reader (including a raw-URL fetch) a single non-JS-dependent summary of this same PR. Not a steering-prompt assumption directly, but the same underlying "verify what actually happened, don't trust the interface" discipline those prompts already encode.



Files touched: skills/tool-quirks/SKILL.md, claude/tool-quirks.md, claude/llms/pr-13.md, claude/llms/README.md, CLAUDE.md, README.md, claude/session-log.md







---







## 2026-07-24 ? CONSTRAINTS.md/MATURITY_ASSESSMENT.md: fresh-environment dependency failure empirically confirmed



Commit: 13553ba



Tests: not applicable ? no code touched; this entry records a reviewer's real-environment test run, not a change to test logic



Assumptions affected:



- `claude/steering-prompts/03-constraints-research-prompt.md` (via `CONSTRAINTS.md`'s "Runtime prerequisites" items 1/2/4) ? the unpinned-dependency gap was previously stated as a theorized risk ("would surface as a silent behavior change") ? [New info ? a reviewer's fresh-environment run reproduced it directly: `test_capacity_preflight.py` failed outright without `ast-grep` on `PATH`, and `test_spring_signal_scan.py` failed 7/32 without `sqllineage` installed (item 2's own text had understated this as a silent field-level degrade, not an actual test failure ? corrected in the same edit). Installing both brought every suite to a clean pass. Confirmed not a defect in PR #13 itself: `spring_signal_scan.py` isn't touched by that PR (`git diff --name-only main 3254d67`). `MATURITY_ASSESSMENT.md`'s "Dependency reproducibility" scorecard row and its adoption-gate checklist item both updated to cite this concrete reproduction and reclassified as blocking rather than aspirational.]



Files touched: CONSTRAINTS.md, MATURITY_ASSESSMENT.md, claude/session-log.md







---







## 2026-07-25 ? Pin ast-grep-cli, sqllineage, pathspec via requirements.txt



Commit: 1b5a5ea



Tests: 9/9 suites passing normally (32, 13, 14, 17-with-1-skipped, 13, 12, 19, 9, 17) plus `scripts/verify_llms_docs.py`'s exact literal summary line, `58 passed, 0 failed, 0 skipped out of 58 commands across 9 file(s)` (this machine has `gh` installed and authenticated, so none of the `gh pr view`-dependent claims hit that script's own "gh CLI not found on PATH" skip path ? a machine without `gh` on `PATH` would show fewer passed/more skipped for the same commit, not a real discrepancy); re-run in a clean venv with none of the three packages preinstalled and no `ast-grep` on `PATH`, installing only via `pip install -r requirements.txt` (confirmed the pinned `ast-grep-cli~=0.45.0` script lands on `PATH` at `0.45.0`) ? identical pass counts, confirming the fix actually closes the 2026-07-24 fresh-environment finding rather than just adding a file.



Assumptions affected:



- `claude/steering-prompts/03-constraints-research-prompt.md` (via `CONSTRAINTS.md`'s "Runtime prerequisites" item 4, and the previous 2026-07-24 entry above) ? "None of the above are version-pinned anywhere in the repo" ? [Resolved ? added `requirements.txt` at the plugin root pinning all three (`ast-grep-cli~=0.45.0`, `sqllineage~=1.5.8`, `pathspec~=1.1.1`) via `~=` compatible-release specifiers; `.github/workflows/ci.yml`'s "Install Python dependencies" step now runs `pip install -r requirements.txt` instead of the previous bare `pip install ast-grep-cli sqllineage pathspec`. `MATURITY_ASSESSMENT.md`'s "Dependency reproducibility" scorecard row and adoption-gate checklist item both updated from blocking to done.]



- Incidental finding from this task's fresh-environment verification, not the pinning work itself: also ran the combined all-three-absent case (no `ast-grep` on `PATH`, `sqllineage`/`pathspec` not installed at all) to check severity before writing it up. `test_spring_signal_scan.py`'s `SpringSignalScanTest.setUpClass` calls `find_ast_grep()`, which does `sys.exit(1)` when the binary is missing; unlike `SystemExit` raised inside an ordinary test method (which `unittest` catches cleanly as a per-test `ERROR`), `SystemExit` raised inside `setUpClass` runs outside that wrapper and kills the whole process uncaught. Confirmed directly: 3 of 32 tests (`ReferencesBucketTest`/`RespectGitignoreOptInTest`) get a clean per-test `ERROR`, then the process exits (code 1) with the remaining 29 tests never attempted and no `Ran N tests` summary line at all ? a CI log in that state would read as "3 errors," not "most of the suite silently never executed." Pre-existing robustness gap in `find_ast_grep()`, not fixed here (pinning doesn't change what happens when the binary is simply absent) ? documented as a new sub-note under `CONSTRAINTS.md`'s "Runtime prerequisites" item 1 rather than silently left out of this task's verification report.



Files touched: requirements.txt, .github/workflows/ci.yml, CONSTRAINTS.md, MATURITY_ASSESSMENT.md, claude/session-log.md







---







