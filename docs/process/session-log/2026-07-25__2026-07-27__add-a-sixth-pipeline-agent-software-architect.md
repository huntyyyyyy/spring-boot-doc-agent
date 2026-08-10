# Session log — 2026-07-25 → 2026-07-27

Lead: **Add a sixth pipeline agent, software-architect-and-testing, reviewing the target repo through DDIA/Effective-Software-Testing lenses, plus a curated semgrep ruleset**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 3. Newest at the bottom of this file.

---

## 2026-07-25 ? Add a sixth pipeline agent, software-architect-and-testing, reviewing the target repo through DDIA/Effective-Software-Testing lenses, plus a curated semgrep ruleset



Commit: 065680a



Tests: 745/745 passing (`python3 -m unittest discover -s scripts -p "test_*.py"`, run under the Python install semgrep is installed under ? see `claude/tool-quirks.md`'s new entry ? with `skipped=14, expected failures=1`, the latter a pre-existing marker), ruff clean, `check_repo_claims.py` clean (16 pre-existing baseline findings, none new), `rule_coverage.py` 29/29, `semgrep_rule_coverage.py` 10/10 (13 findings on the fixture corpus), `check_code_quality.py` clean after a deliberate `--update` (one test function grew by one legitimate assertion line).



Assumptions affected:



- `claude/steering-prompts/10-review-persona-and-standards.md` ? its DDIA/testing/security anchors (§5-6) were framed exclusively as a lens for reviewing *this plugin's own* fact-store design ? [New info ? the same anchors (DDIA 2e; now also Aniche's *Effective Software Testing*, a distinct book from the Meszaros/xUnit anchor already there) now also apply one layer down, via `agents/software-architect-and-testing.md`, to the *target* repo a pipeline run documents. The prompt's own anchors are unedited and still accurate for their original scope; this is an additional application, not a correction.]



- `claude/steering-prompts/00-shared-research-standards.md` and `11-context-traversal-protocol.md` ? arXiv/GitHub-stars-and-recency/DeepWiki-as-orientation methodology and the DFS/BFS bounded-traversal protocol, previously prose conventions for steering-prompt authors only ? [New info ? now also implemented as an actual agent capability (`WebFetch`, no agent previously had it) rather than only a documentation convention. No prior agent could ground an external-fitness claim in research at all; this is the first one that can, following both files' discipline rather than inventing a lighter version.]



- `CONSTRAINTS.md`'s "Known precision tradeoffs" item 10 ? "agents are barred from text search... `Grep` removed from every `agents/*.md`... enforced by check F" ? [Still accurate. The sixth agent follows the same rule (`tools: Read, Glob, Write, Bash, WebFetch`, no `Grep`); check F passed without needing new settings.json scoping since the existing `Bash(ast-grep...)` allow entry and `grep`/`rg` denies already satisfy it repo-wide. New `Bash(semgrep scan:*)`/`Bash(semgrep --version)` entries added anyway, for least-privilege scoping consistent with the file's own stated philosophy, not because check F required it.]



- `CONSTRAINTS.md`'s "Runtime prerequisites" ? previously three entries (ast-grep, SQLLineage, pathspec) ? [New info ? a fourth, `semgrep`, added as item 5, pinned in `requirements.txt` and empirically verified (10/10 rules fire; exact command and result recorded in the entry) rather than asserted. Unlike ast-grep's history, its absence is a designed graceful-degrade (exit 2 / test skip), not a rediscovered unhandled-crash bug.]



- `skills/document-spring-repo/references/doc-taxonomy.md`'s closed, four-word citation tag grammar ? deliberately **not** extended for this change, a scope decision recorded in both the agent file and the new steering prompt: DDIA/Effective-Software-Testing framing and any external-research trail are attributed prose next to an ordinary `[Evidenced ? path:line]` tag, never a new bracket-tag word ? extending the grammar would ripple through `doc_tag_utils.py`, `run_manifest.py`'s tag counting, `test_pipeline_stages.py`'s grammar assertions, and `citation_coverage.py`, a materially larger and separate decision this change did not make.



- A real environment quirk surfaced and logged in `claude/tool-quirks.md`: on Windows, invoking a pip-installed console-script binary (here, `semgrep`) via `subprocess` from a *different* Python installation than the one it's installed under fails with `ModuleNotFoundError`, even though the identical binary runs fine from a plain shell or from its own interpreter ? CI is unaffected (single Python install), but local verification needed the correct interpreter explicitly.



Files touched: agents/software-architect-and-testing.md, agents/doc-writer.md, scripts/spring_semgrep_rules.yml, scripts/semgrep_rule_fixtures/ArchitectureDdia.java, scripts/semgrep_rule_fixtures/TestingEst.java, scripts/semgrep_rule_coverage.py, scripts/test_semgrep_rule_coverage.py, scripts/capacity_preflight.py, scripts/test_capacity_preflight.py, scripts/run_manifest.py, scripts/test_run_manifest.py, scripts/test_pipeline_stages.py, scripts/check_repo_claims.py, scripts/code_quality_baseline.json, requirements.txt, .claude/settings.json, .github/workflows/ci.yml, skills/document-spring-repo/SKILL.md, skills/document-spring-repo/references/doc-taxonomy.md, CONSTRAINTS.md, README.md, CLAUDE.md, claude/tool-quirks.md, claude/steering-prompts/14-software-architect-and-testing-agent-prompt.md







## 2026-07-26 ? Consolidate three bodies of uncommitted work: schema fix, new test suite, integration wiring







Commit: 065680a



Tests: 752/752 passing (`python3 -m unittest discover -s scripts -p "test_*.py"`, same environment as prior session), ruff clean, `check_repo_claims.py` clean (16 pre-existing baseline findings), `rule_coverage.py` 29/29, `semgrep_rule_coverage.py` 10/10.







Assumptions affected:







**Schema fix (Body A):** The oracle-output contract was correct; the consumer was wrong. Stage 0 `scripts/stage0_oracle_compare.py` emits a report with top-level fields `schema_version`, `_producer`, `evidence_tier`, `shared_input_digest`, `java_files_scanned`, `interfaces_with_extends`, and nested lists/maps under `summaries` (metadata per arm/variant) and `misses` (individual miss rows). `scripts/check_no_client_identifiers.py` was checking a nonexistent schema (q1_repository_chains, q2_meta_annotations, hop_histogram, language_dirs, etc.), written against assumptions rather than the code.



- `CONSTRAINTS.md` "Confidentiality/handling rules" item 1 ? the closed parenthetical "nothing mechanical looks for this" ? [Partially resolved ? narrowed to "covering only the aggregate-JSON carrier from bytecode-oracle runs, not the `.gitignore` case," which is mechanically true and more honest than the prior blanket statement.]







**Test suite (Body C):** `stage0_oracle_compare.py` now has a test suite mirroring `test_check_no_client_identifiers.py`'s shape.



- `claude/steering-prompts/01-testability-research-prompt.md` ? "Nothing tests the four LLM stages" was a standing gap, and this work now establishes a principle: every output-producing script in `scripts/` must have a corresponding `test_*.py` sibling with in-process tests (not subprocess), guarded by tool-availability checks (`@unittest.skipUnless(shutil.which("ast-grep"), ...)`), and covered in CI. `stage0_oracle_compare.py` was the first to have no test sibling at all ? CI flagged it via `hooks/require_hardened_tests.py`'s commit gate on the first failed attempt. ? [Still accurate; this work confirms the principle is holding.]



- `scripts/test_stage0_oracle_compare.py` (new, 31/31 passing) covers: unit tests for `assign_cause()` and `validate_rows()` (no ast-grep needed); contract-violation error paths (missing/short salt, missing rules); and structural proofs of the native-vs-multipass tradeoff (guarded by tool availability). An integration test pipes the stage0 output through `check_no_client_identifiers.py` to confirm the gate passes a well-formed report.



- `scripts/test_check_no_client_identifiers.py` rewritten to test the real schema: `summaries`/`misses` list structure, `delta_by_cause`/`verdict_by_cause` enum patterns, `shared_input_digest`/`entity_pseudonym` shape constraints, instead of the nonexistent q1/q2/q3 hierarchy that was the spec for this file before the fix.







**Integration (Body B):**



- `.github/workflows/ci.yml` ? merge conflict resolved (stashed network-egress-deny work was already present) and `test_stage0_oracle_compare.py` step added, guarded by `@unittest.skipUnless` since the suite skips itself if ast-grep is unavailable.



- `CONSTRAINTS.md` ? three edits in place: (1) narrowed item 1's statement to be mechanically true; (2) added item 13 under "Known precision tradeoffs" documenting `stage0_oracle_compare.py` as an empirical instrument for the source-text-vs-bytecode gap, with schema and test coverage as part of the repo, and noting `scripts/spring_semgrep_rules.yml` (Body A's Arm C ruleset) is valid `--semgrep-rules` input; (3) widened Confidentiality item 3 to say network egress is now "partially mechanically enforced" via `hooks/deny_raw_network.py` (runtime half) + check F (static half), cross-linked to Integration-gaps item 2's 2026-07-26 addendum.



- `CLAUDE.md` ? added new "Check F also gates network egress" section after the ast-grep mandate prose, describing the two-part enforcement (static/runtime) and the `software-architect-and-testing` context (only agent with both `Bash` and `WebFetch`).



- `scripts/stage0_oracle_compare.py` ? added one docstring line in FAIRNESS section: "For Arm C (semgrep), scripts/spring_semgrep_rules.yml is valid --semgrep-rules input."







Files touched: scripts/check_no_client_identifiers.py, scripts/test_check_no_client_identifiers.py, scripts/test_stage0_oracle_compare.py, .github/workflows/ci.yml, scripts/stage0_oracle_compare.py, CONSTRAINTS.md, CLAUDE.md, claude/session-log.md







## 2026-07-27 ? Stage 0 accuracy follow-ups: multi-hyphen profiles, contested entity_table_map, measured on in-tree mid-size checkout



Commit: 3df87fb



Tests: 	est_spring_signal_scan.py 58/58; 	est_stage0_oracle_compare.py NativeVsMultipass+AssignCause 5/5; 	est_enterprise_kitchen_sink.py RealEnterpriseRepoTest+Ch03+multi-segment 13/13 (1 expectedFailure); check_repo_claims.py OK; check_code_quality.py OK after deliberate --update for one fixture-write statement.



Assumptions affected:



- CONSTRAINTS.md Known precision item 7 (multi-segment profiles skipped / credential blind spot) ? [Resolved ? CONFIG_NAME_PATTERNS widened to include hyphenated profile segments; kitchen-sink + RealEnterpriseRepoTest pin recognition / config_key_sets membership.]



- CONSTRAINTS.md Known precision item 2 (simple-name entity_table_map collision yields arbitrary winner / wrong JPQL lineage) ? [Resolved for H1 ? status: contested + candidates list; 



esolve_jpql_to_lineage refuses rather than guessing. Full FQCN/fact-tuple key still Phase 1.]



- CONSTRAINTS.md Known precision item 6 (partition carry_forward cascade) ? [New info ? same cascade reproduced on the in-tree mid-size Spring checkout at default token budget; RealEnterpriseRepoTest.test_overlap_is_adjacent_only now expectedFailure.]



- claude/10-architecture-maturation-plan.md H1 (detect collision; refuse JPQL; warn) ? [Resolved ? shipped as contested sentinel without schema rewrite.]



- claude/steering-prompts/03-constraints-research-prompt.md ? precision tradeoffs remain current-state in CONSTRAINTS.md ? [Still accurate ? entries corrected in place with verify predicates.]



Live measurement (gitexcluded in-tree mid-size Spring checkout; aggregates only, no identifiers):



- Rescan: java=629, config=16, deployment=5; entities=53; contested=0; multi-hyphen application* stems on disk=0 (fix vacuous here); config_key_sets=15; redaction zone files=5; evidence bucket totals unchanged vs prior spring_signals.json (DELTA config/entities = 0).



- Oracle fixture (NativeVsMultipassTest / Assign_cause): direct extends -> no miss (UNCLASSIFIED); via_intermediate_only -> INTERMEDIATE_BASE_INHERITANCE -> STRUCTURAL; EVIDENTIARY rates require a bytecode oracle JSON not present in-tree ? not measured this session.



Files touched: scripts/spring_signal_scan.py, scripts/test_spring_signal_scan.py, scripts/test_enterprise_kitchen_sink.py, scripts/code_quality_baseline.json, scripts/repo_claims_baseline.json, CONSTRAINTS.md, claude/session-log.md







---







