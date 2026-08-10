# Session log — 2026-07-28 → 2026-07-29

Lead: **Principal review follow-up: certified CI, partition/write-scope fixes, module split**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 5. Newest at the bottom of this file.

---

## 2026-07-28 ? Principal review follow-up: certified CI, partition/write-scope fixes, module split







Commit: 065680a



Tests: compliance + certified integration + partition overlap pass; `check_repo_claims.py` OK; `check_code_quality.py` baseline updated



Assumptions affected:



- Kitchen sink overlap xfail ? [Resolved ? `partition_repo.build_groups` no longer re-carries overlap seed files.]



- Write-scope gate gitignore blind spot ? [Resolved ? `check_pipeline_output.py` uses `git ls-files -o -i`.]



Files touched: .github/workflows/doc-engine.yml, scripts/partition_repo.py, scripts/check_pipeline_output.py, src/doc_engine/pipeline/gates.py, src/doc_engine/pipeline/mock_stages.py, src/doc_engine/pipeline/local_runner.py, tests/test_compliance.py, tests/test_local_runner_certified.py, tests/test_adapter_layout.py, tests/test_partition_repo.py, tests/test_enterprise_kitchen_sink.py, scripts/code_quality_baseline.json, claude/session-log.md







---







## 2026-07-29 ? A+C hybrid: orchestrator-first Claude adapter, plugin path gap closed







Commit: 065680a



Tests: pytest tests/test_scan_parity.py tests/test_adapter_layout.py tests/test_compliance.py tests/test_local_runner_certified.py passing (36); check_repo_claims.py OK



Assumptions affected:



- Adapter skills invoke `${CLAUDE_PLUGIN_ROOT}/scripts/` ? [Resolved ? A+C hybrid: skills use doc-engine pipeline run|gates only; CI bans plugin-local scripts refs; adapters/claude/CONSTRAINTS.md stub resolves under plugin root.]



- Dual stage-graph SoT (SKILL bash vs build_stage_specs()) ? [New info ? skill no longer duplicates per-script Stage 0 bash; --until truncates the graph SoT; residual: generative stages still choreographed in skill prose.]



Files touched: docs/product-architecture.md, adapters/claude/*, src/doc_engine/cli.py, src/doc_engine/pipeline/compliance.py, local_runner.py, live_gates.py, README.md, tests/test_scan_parity.py, test_adapter_layout.py, test_compliance.py, skills/*/SKILL.md, claude/session-log.md







---







## 2026-07-29 ? UTF-8 claims contract: Check G preflight, session-log repair, PowerShell quirks







Commit: 065680a



Tests: test_check_repo_claims.py 96/96; check_repo_claims.py OK



Assumptions affected:



- CLAUDE.md / check_repo_claims reader contract ? strict UTF-8 with no preflight ? [Resolved ? Check G emits Finding (path, byte offset, hint) instead of UnicodeDecodeError traceback; read_utf8 helper; skip unreadable md for later checks.]



- Windows session-log append path ? [New info ? PowerShell Add-Content default encoding can inject cp1252; documented in claude/tool-quirks.md; prefer Python Path.write_text(encoding="utf-8").]



Files touched: scripts/check_repo_claims.py, tests/test_check_repo_claims.py, claude/session-log.md, claude/tool-quirks.md







---







## 2026-07-29 ? Principal gate redesign: size advisory, ruff on src/doc_engine, honest llms coverage







Commit: 065680a



Tests: test_check_code_quality.py 61/61; test_check_llms_coverage.py; ruff scripts/+src/doc_engine clean; check_repo_claims OK



Assumptions affected:



- claude/steering-prompts/13-code-quality-research-prompt.md ? monotonic size/complexity hard ratchet ? [Resolved ? schema v4: size/complexity/depth advisory; hard = annotation coverage + docstring orientation; measure scripts/ + src/doc_engine/.]



- CONSTRAINTS.md ENFORCE=False temporary on check_llms_coverage ? [Resolved ? ENFORCE toggle removed; always advisory.]



- Product package outside lint scope ? [Resolved ? ruff check scripts/ src/doc_engine/.]



Files touched: scripts/check_code_quality.py, scripts/code_quality_baseline.json, scripts/check_llms_coverage.py, tests/test_check_code_quality.py, tests/test_check_llms_coverage.py, .github/workflows/ci.yml, .ruff.toml, CONSTRAINTS.md, STATUS.md, claude/steering-prompts/13-code-quality-research-prompt.md, src/doc_engine/**, claude/session-log.md



## 2026-07-29 ? Portable kernel: product vs meta, Stage 0 package ports, skill SoT



Commit: 065680a



Tests: portable Stage 0 + adapter layout + pipeline runner green locally; full suite pending



Assumptions affected:



- claude/steering-prompts/02-pluggability-research-prompt.md ? package invoke / stage graph ? [Resolved ? deterministic stages and product gates use python -m doc_engine.tools.*; meta CI stays in scripts/; boundary in docs/product-architecture.md]



- Dual generative SoT ? [Resolved ? generative_choreography() on build_stage_specs(); skill cites SoT]



- claude/steering-prompts/07-ci-scaffold-task-prompt.md ? [New info ? CI deterministic_only + artifact schema gate on spring fixture]



Files touched: src/doc_engine/tools/*, pipeline/stages.py, live_gates.py, runner.py, local_runner.py, adapters/claude/skills/*, skills/*, tests/test_portable_stage0.py, test_adapter_layout.py, .github/workflows/ci.yml, STATUS.md, docs/product-architecture.md, claude/session-log.md







