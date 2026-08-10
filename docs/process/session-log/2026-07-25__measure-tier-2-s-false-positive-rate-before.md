# Session log — 2026-07-25

Lead: **Measure tier 2's false-positive rate before adding anything to it**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 4. Newest at the bottom of this file.

---

## 2026-07-25 ? Measure tier 2's false-positive rate before adding anything to it







Commit: 065680a at time of writing



Tests: `test_drift_normalization.py` 19/19 (new, CI-wired, ~10s); full suite green; `check_code_quality.py` and `check_repo_claims.py` both exit 0



Assumptions affected:



- `claude/steering-prompts/06-wiredrift-check-task-prompt.md` ? "resolved (2026-07-23, PR #3) ? `spring_drift_check.py` is documented as an optional pre-flight check" ? [Still accurate] ? wiring is unchanged. What is new is that the tool's *precision* now has a number attached rather than being assumed from its design.



- `claude/steering-prompts/04-analytics-logging-research-prompt.md` ? "drift detection already built" ? [Still accurate] ? this measures the thing that prompt declared built; it does not move the build/wire claim either way.







**The question was whether to add a Rust/tree-sitter fingerprint to `spring_drift_check`, whose subjects really are Java files** ? the one place the previous session's withdrawn `astsig` proposal might have had an honest home. Measured instead of argued.







**Result: the ceiling on any better fingerprint is 2 wrong verdicts in 208, and a stdlib tokenizer already reaches it.** Comments, reindentation and inserted blank lines each produce zero false positives; only annotations wrapped across lines trip tier 2, only in `api_surface__mapping`. The cause is not a missing parser ? ast-grep already returns the whole match and `_first_line_match()` keeps `splitlines()[0]`, reducing `@RequestMapping(\n "/api/invoices"\n)` to `@RequestMapping(`, which compares equal to nothing. The structural information is in hand and being discarded on the Python side, which is exactly why no parser can beat a tokenizer here: both start from the same string.







**The instrument was wrong first, and that is the transferable part.** The first run said 7/208 across five rules. The perturbation had rewritten annotation-looking text inside comments, broken a doc comment's closing quote, and left the files unparseable ? ast-grep then returned nothing and every citation read as drift. It was measuring the harness, in the direction that would have justified the work under evaluation, and it was caught only by opening the files. So the harness now carries a validity gate (a formatting-only edit must leave the same citation count discoverable by a fresh scan) and **the broken perturbation is kept as a test input**, with `Test00HarnessValidityGate` asserting the gate rejects it. Non-vacuity proved by four injections, including a no-op control; 4/4 behaved as required.







**The fix is deliberately not in this change.** `_first_line_match()` decides both what tier 2 *compares* and what `spring_signals.json` *stores* as human-readable `match` evidence a doc-writer reads. A token sequence joined by `\x1f` is a fine identity and unreadable evidence; separating the two jobs changes the stored schema. `CONSTRAINTS.md` "Known precision tradeoffs" item 9, flagged not resolved.







**Rust, answered:** no for the fingerprint. One real case remains, in the test lane rather than the shipped path ? the validity gate is a proxy (count unchanged) where a direct AST-equivalence oracle would need a Java parser, and `ast-grep` cannot stand in: verified on 0.44.1 that a whole file cannot be a pattern (`Multiple AST nodes are detected`) and `--debug-query` dumps only the query's tree. Stated in the research doc, not acted on, and it should carry its own measurement first ? the 2/208 figure is bounded by the four perturbations one person thought to write, not by the checker.







Files touched: scripts/java_perturbations.py, scripts/drift_match_normalizers.py, scripts/test_drift_normalization.py, .github/workflows/ci.yml, scripts/code_quality_baseline.json, CONSTRAINTS.md, claude/drift-normalization-measurement-2026-07-25.md, claude/session-log.md







## 2026-07-25 - Mandate ast-grep over text search for agents, and add the rule-coverage invariant behind it



Commit: 065680a



Tests: 577/577 passing before this entry (`python3 -m unittest discover -s scripts -p "test_*.py"`), ruff clean, `check_repo_claims.py` clean (16 pre-existing baseline findings), `rule_coverage.py` 29/29 rules fire on fixtures.



Assumptions affected:



- `07-ci-scaffold-task-prompt.md` - line 24 lists text search among the "commands safe to auto-run" alongside `git show` and read-only git plumbing - [New info - that is no longer true for agents in this repo. `.claude/settings.json` now denies it through `Bash`, `hooks/deny_text_search.py` blocks it at runtime, and `check_repo_claims.py` check F fails the build if an `agents/*.md` declares the `Grep` tool. The prompt's wider point about separating read-only from side-effecting commands still stands; only that one example is now wrong.]



- `09-tool-quirks-indexing-research-prompt.md` - line 27 proposes text search against a consistent per-entry `Tags:` line as the lightweight way to do structured search over markdown - [New info - that option is now denied for agents, and the obvious substitute does not work. Measured: `ast-grep -l markdown` matches broad block nodes, reporting 35 hits on `README.md` where only 8 lines contain the literal string. Recorded in `claude/tool-quirks.md`. If this research still gets done, the live options are a structured index file or `Glob`+`Read`, not either search tool.]



- `08-dependency-pinning-task-prompt.md` - "`ast-grep-cli` pinned in requirements.txt", status `[Resolved - 2026-07-25]` - [Still accurate, but weaker than it read. The pin was never enforced at runtime: CI ran `ast-grep --version` and discarded the answer. On this dev machine the pin resolves 0.45.0 while the binary on `PATH` is 0.44.1 - the shadowing already logged in `tool-quirks.md`, live while that step was green. The CI step now reads the pin from `requirements.txt` and fails on a major/minor mismatch.]



- `00-shared-research-standards.md` - line 24, "no new infrastructure or dependencies beyond what the plugin already assumes (Python stdlib, `ast-grep` on `PATH`, no new services)" - [Still accurate - nothing added but stdlib Python and rules for the ast-grep already required. A rule-catalog *microservice* was explicitly rejected on this constraint.]



- `02-pluggability-research-prompt.md` - line 21, "the JSON shape was kept stable specifically so a scanner rewrite (regex to ast-grep) wouldn't require touching the rest of the pipeline" - [Still accurate - the six new rules were deliberately placed in the existing `persistence` and `references` buckets rather than a new one, precisely so `spring_signals.json`'s shape and the fourteen-file taxonomy are untouched.]



Files touched: agents/*.md (all five), .claude/settings.json, hooks/hooks.json, hooks/deny_text_search.py, scripts/check_repo_claims.py, scripts/test_check_repo_claims.py, scripts/rule_coverage.py, scripts/test_rule_coverage.py, scripts/test_deny_text_search.py, scripts/rule_fixtures/, scripts/rule_coverage_baseline.json, scripts/spring_ast_grep_rules.yml, scripts/drift_match_normalizers.py, .github/workflows/ci.yml, CLAUDE.md, CONSTRAINTS.md, claude/tool-quirks.md







## 2026-07-25 - Classify Gradle/Groovy build files, and fix the quoted-placeholder false positive they exposed



Commit: 065680a



Tests: 6 new `BuildFileClassificationTest` cases plus 4 new secret-heuristic cases; all three mutations of the new branch verified to turn the suite red (branch disabled, `.kts` guard loosened, `gradle.properties` pattern removed).



Assumptions affected:



- `03-constraints-research-prompt.md` - carries the ast-grep-vs-other-analysis tradeoff as the standing statement of what source-text analysis can and cannot resolve - [New info - that tradeoff was written about Java precision. It now has a harder edge: ast-grep has no Groovy grammar at all, so `.gradle` files are not a precision tradeoff but a total absence of structural analysis. Recorded as `CONSTRAINTS.md` item 11.]



- `00-shared-research-standards.md` - "no new infrastructure or dependencies beyond what the plugin already assumes" - [Still accurate - filename classification in Python, no new dependency.]



Files touched: scripts/spring_signal_scan.py, scripts/_secret_heuristics.py, scripts/test_spring_signal_scan.py, scripts/test_secret_heuristics.py, .github/workflows/ci.yml, CONSTRAINTS.md, CLAUDE.md, claude/tool-quirks.md







## 2026-07-25 - A testing layer that classifies change, mechanises non-vacuity, and gates the commit



Commit: 5f7ad5c, 267b4be, 94f2337, 5f84d20



Tests: 680 passing (was 589 at the start of this work). ruff, check_code_quality.py, check_repo_claims.py, rule_coverage.py all exit 0. mutate.py reports 7/7 killed, 0 survivors.



Assumptions affected:



- `01-testability-research-prompt.md` - its original scope was mechanical + judgment testing, both automated, and `STATUS.md` records it as "partially resolved, not fully closed" - [New info - the mechanical half moved substantially. Four things landed that did not exist: an expectation algebra over the evidence set (`set_delta.py`), metamorphic relations across input type and velocity (`test_metamorphic.py`), a sandboxed mutation harness (`mutate.py`), and a commit-time gate (`hooks/require_hardened_tests.py`). The judgment half is untouched and still manual.]



- `10-review-persona-and-standards.md` - "This project's rule that a gate that cannot be shown to fail is not a gate is currently satisfied by hand... That is mutation testing performed manually, once, with no artifact proving it occurred." - [Resolved - `mutate.py` produces the artifact. Seven mutations, each naming the suite that should catch it, applied to a copy of the tracked tree and never the working tree. The prompt's advice to judge proposals against `mutmut` was followed and the answer was to not adopt it as the foundation: it mutates Python, and four of the seven defects live in markdown frontmatter, YAML and CI config, where it scores zero.]



- `claude/drift-normalization-measurement-2026-07-25.md` - states two bounds: "Only Java is perturbed" and "No encoding or line-ending perturbation" - [Resolved for the set-level invariants - `test_metamorphic.py` covers .gradle and .properties inputs, CRLF, and a UTF-8 BOM. The drift comparator's own false-positive rate is unchanged; this measures the scanner, not the comparator.]



- `CONSTRAINTS.md`'s flagged tier-2 first-line defect - [Still accurate, and now independently reproduced. `test_metamorphic.test_wrapping_annotation_args_still_moves_the_set` asserts the defect in the direction that is true today, so it fails if the defect is fixed rather than silently passing forever.]



Files touched: scripts/prompt_contracts.py, scripts/test_prompt_contracts.py, scripts/set_delta.py, scripts/test_set_delta.py, scripts/test_metamorphic.py, scripts/mutate.py, scripts/test_mutate.py, scripts/mutation_baseline.json, scripts/test_require_hardened_tests.py, scripts/test_pipeline_stages.py, hooks/require_hardened_tests.py, .claude/settings.json, .github/workflows/ci.yml, scripts/code_quality_baseline.json







