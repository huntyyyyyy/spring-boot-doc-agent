# Session log — 2026-07-27

Lead: **Build-file structural signals (Gradle/Groovy/Maven/version catalogs) close CONSTRAINTS §11**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 4. Newest at the bottom of this file.

---

## 2026-07-27 ? Build-file structural signals (Gradle/Groovy/Maven/version catalogs) close CONSTRAINTS §11



Commit: f0be9de



Tests: scripts/test_build_signal_extract.py 12/12; scripts/test_spring_signal_scan.py BuildFileClassificationTest 6/6; scripts/test_spring_drift_check.py 41/41; scripts/test_enterprise_kitchen_sink.py Ch04EncodingTest 17/17; check_repo_claims.py OK; check_code_quality.py OK after deliberate --update.



Assumptions affected:



- `claude/steering-prompts/03-constraints-research-prompt.md` ? build-file heuristics now a real signal source, not just filename classification ? [Resolved ? `scripts/_build_signal_extract.py` added, wired into `spring_signal_scan.py`, with five `deployment__build_*` rule ids and drift tier-2 re-verification.]



- `CONSTRAINTS.md` §11 ? "Gradle build scripts get filename-level classification only" ? [Resolved ? now **Partially resolved**: deterministic plugin/dependency/module/toolchain/catalog extraction; dynamic Groovy and full task graph remain out of scope.]



- `skills/document-spring-repo/references/doc-taxonomy.md` ? operations.md / local_development.md now prefer `deployment__build_*` rows over an agent's own reading of build scripts. ? [Resolved ? evidence section updated.]



- `agents/file-summarizer.md` ? build `rule_id` rows treated as ground truth like other Stage 0 hits. ? [Resolved ? step 2 example updated.]



Files touched: scripts/_build_signal_extract.py, scripts/spring_signal_scan.py, scripts/spring_drift_check.py, scripts/test_build_signal_extract.py, scripts/test_spring_signal_scan.py, scripts/test_enterprise_kitchen_sink.py, .github/workflows/ci.yml, CONSTRAINTS.md, skills/document-spring-repo/references/doc-taxonomy.md, agents/file-summarizer.md, claude/session-log.md, scripts/code_quality_baseline.json, scripts/repo_claims_baseline.json







---







## 2026-07-27 ? Stage 0 CodeQL adoption: content-addressed result cache and fast-mode test suites



Commit: 065680a



Tests: test_spring_signal_scan.py fast mode 55/55 OK (5 skipped); test_spring_drift_check.py fast mode 41/41 OK (27 skipped); test_rule_coverage.py 13/13; rule_coverage.py 28/28 rules fired; check_repo_claims.py OK (14 pre-existing baseline findings unchanged).



Assumptions affected:



- `claude/steering-prompts/08-dependency-pinning-task-prompt.md` ? "`requirements.txt` added at plugin root pinning `ast-grep-cli~=0.45.0`" ? [Resolved ? `ast-grep` replaced by CodeQL CLI (standalone binary, not a Python package); `requirements.txt` no longer contains `ast-grep-cli`; `verify:` predicate updated to `not_contains:requirements.txt:ast-grep-cli`.]



- `CONSTRAINTS.md` "Runtime prerequisites" item 1 ? "`ast-grep` binary on `PATH`" and `find_ast_grep()`/`run_ast_grep()` references ? [Resolved ? CodeQL CLI on `PATH`; `_codeql_runner.py` raises `CodeQLError`/`CodeQLScannerError`; CLI entry points catch and exit 1 cleanly.]



- `MATURITY_ASSESSMENT.md` "Dependency reproducibility" ? residual `find_ast_grep()` reference ? [Resolved ? row updated to CodeQL CLI and current `requirements.txt` contents.]



- `.claude/skills/verify-state-claims/SKILL.md` historical example ? `run_ast_grep()` reference ? [Resolved ? updated to CodeQL runner analogy.]



Files touched: scripts/_codeql_runner.py, scripts/spring_signal_scan.py, scripts/test_spring_signal_scan.py, scripts/test_spring_drift_check.py, requirements.txt, CONSTRAINTS.md, MATURITY_ASSESSMENT.md, .claude/skills/verify-state-claims/SKILL.md, claude/steering-prompts/08-dependency-pinning-task-prompt.md, claude/session-log.md







---







## 2026-07-27 ? Unified signal framework, doc_engine SDK, and GitHub Action for product architecture



Commit: 065680a



Tests: test_spring_signal_scan.py 58/58 passing (with and without SPRING_SIGNAL_USE_SNAPSHOT); multi-scanner run on an external Spring service checkout (filesystem+ast-grep) produced 629 Java files, 53 entities, 4,224 evidence rows; doc_engine SDK scan/docs/site smoke test passed; check_repo_claims.py OK (14 pre-existing baseline findings unchanged).



Assumptions affected:



- `claude/steering-prompts/02-pluggability-research-prompt.md` ? "Stage 0 is a single monolithic scanner" ? [Resolved ? `spring_signal_scan.py` now orchestrates pluggable backends via `_orchestrator.py`: `FilesystemBackend`, `CodeQLBackend`, `AstGrepBackend`, merged by `SpringSignalMerger`, lineage resolved by `SpringLineageResolver`. New scanners can implement the `Scanner` protocol in `_signal_framework.py`.]



- `CONSTRAINTS.md` Known precision items 2, 7, 11 ? verify predicates that anchored to `scripts/spring_signal_scan.py` ? [Resolved ? predicates updated to `_merge_signals.py`, `_resolve_lineage.py`, and `_scanner_filesystem.py` after code was extracted; no claim semantics changed, only the file that now hosts the evidence.]



- `claude/steering-prompts/08-dependency-pinning-task-prompt.md` ? "CodeQL CLI on PATH" ? [Still accurate ? CodeQL remains the production default scanner, but the SDK and CI workflows default to `filesystem,ast-grep` where a compatible Java toolchain is not available, so the product works out of the box while CodeQL is opt-in via `--scanners filesystem,codeql,ast-grep`.]



- New product architecture assumptions (not in steering prompts): [Resolved ? created `doc_engine/` package (`Engine`, `Config`, CLI `scan`/`docs`/`site`), `pyproject.toml`, and reusable GitHub Action `action.yml` plus workflow `.github/workflows/doc-engine.yml`.]



Files touched: scripts/_signal_framework.py, scripts/_orchestrator.py, scripts/_scanner_registry.py, scripts/_scanner_filesystem.py, scripts/_scanner_codeql.py, scripts/_scanner_astgrep.py, scripts/_merge_signals.py, scripts/_resolve_lineage.py, scripts/spring_signal_scan.py, scripts/test_spring_signal_scan.py, scripts/regenerate_fixture_snapshot.py, doc_engine/__init__.py, doc_engine/config.py, doc_engine/engine.py, doc_engine/scanner.py, doc_engine/generation.py, doc_engine/site.py, doc_engine/cli.py, pyproject.toml, action.yml, .github/workflows/doc-engine.yml, CONSTRAINTS.md, claude/session-log.md







---







## 2026-07-27 ? doc_engine SDK follow-up: config loader, tests, CI wiring



Commit: 065680a



Tests: test_doc_engine.py 6/6; test_spring_signal_scan.py 58/58; test_spring_drift_check.py 41/41; check_repo_claims.py OK.



Assumptions affected:



- Product plan item `.doc-engine.yml` repo config ? [Resolved ? `doc_engine/config_loader.py` reads `.doc-engine.yml`/`.doc-engine.json`; CLI merges repo config with flags.]



- Product plan item CLI as distribution channel ? [Resolved ? `doc-engine scan|docs|site` entry point in `pyproject.toml`; wired in CI and GitHub Action.]



Files touched: doc_engine/config_loader.py, doc_engine/cli.py, doc_engine/doc-engine.example.yml, scripts/test_doc_engine.py, .github/workflows/ci.yml, .github/workflows/doc-engine.yml, action.yml, pyproject.toml, scripts/_merge_signals.py, claude/session-log.md







---







