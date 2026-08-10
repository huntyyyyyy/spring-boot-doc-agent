# Session log — 2026-07-29 → 2026-07-30

Lead: **Scope clarity cleanup (post-packaging docs + dead bootstraps)**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 6. Newest at the bottom of this file.

---

## 2026-07-29 ? Scope clarity cleanup (post-packaging docs + dead bootstraps)



Commit: 065680a



Tests: check_repo_claims + ruff + check_code_quality (after staging deletes); targeted pytest if hooks/claims touched



Assumptions affected:



- `claude/10-architecture-maturation-plan.md` Phase 0.1 PORTING/local_ci as current work ? [New info ? banner: superseded by portable-kernel CI; §0 + Phase 1?3 still product thesis]



- `claude/steering-prompts/07-ci-scaffold-task-prompt.md` body as implementable brief ? [Still accurate as historical; body banner added ? do not re-add verify_llms_docs]



- Current-state docs citing root `agents/` / bare `scripts/<product>.py` / `skills/tool-quirks` ? [Resolved ? retargeted to adapters/claude + `python -m doc_engine.tools.*`]



- Unused `scripts/_src_bootstrap.py` / `tools/_bootstrap.py` ? [Resolved ? deleted]



Files touched: README.md, CLAUDE.md, CONSTRAINTS.md, STATUS.md, MATURITY_ASSESSMENT.md, IMPLEMENTATION_HANDOFF.md, docs/product-architecture.md, skills/README.md, skill reference mirrors, claude/10-architecture-maturation-plan.md, claude/steering-prompts/07-*, claude/tool-quirks.md, src/doc_engine/cli.py, scripts/_src_bootstrap.py (deleted), src/doc_engine/tools/_bootstrap.py (deleted), scripts/code_quality_baseline.json, claude/session-log.md







## 2026-07-29 ? Stage 0 scanner voice: default ast-grep; CodeQL opt-in



Commit: 065680a



Tests: check_repo_claims (expected)



Assumptions affected:



- CONSTRAINTS Runtime item 1 "CodeQL hard for Stage 0" ? [Resolved ? default is filesystem+ast-grep; CodeQL via --scanners; capacity_preflight does not require CodeQL]



Files touched: CONSTRAINTS.md, README.md, claude/session-log.md







## 2026-07-29 ? Operator pilot + principal adoption guides



Commit: 065680a



Tests: not run (docs only)



Assumptions affected:



- Cold-start ?how do I run Path A/B on a real repo?? lived only in README/SKILL fragments ? [Resolved ? docs/guides/operator-pilot.md + principal-adoption.md; README + product-architecture linked]



Files touched: docs/guides/operator-pilot.md, docs/guides/principal-adoption.md, README.md, docs/product-architecture.md, claude/session-log.md







## 2026-07-30 ? Pre?Phase 1 fact-store research spike (REFINE)



Commit: 065680a



Tests: not run (research/docs only)



Assumptions affected:



- `claude/steering-prompts/00-shared-research-standards.md` ? primary-confirmation / star+recency bar for GitHub+arXiv ? [Still accurate ? applied in `claude/research/fact-store-prior-art-corpus-2026-07-30.md`]



- `claude/10-architecture-maturation-plan.md` §0?1 / JPA survey as executable Phase 1 specs ? [New info ? outdated relative to portable kernel, packaging pause, contested map, default scanners; thesis revalidated externally; Phase 1 gated on decision memo **REFINE**, thin dual-emit only]



Files touched: claude/research/fact-store-prior-art-corpus-2026-07-30.md, claude/research/fact-store-approaches-collation-2026-07-30.md, claude/research/fact-store-phase1-decision-memo-2026-07-30.md, claude/10-architecture-maturation-plan.md, claude/jpa-hibernate-predicate-vocabulary-survey.md, STATUS.md, claude/session-log.md







## 2026-07-30 ? Phase 1 dual-emit facts.jsonl



Commit: 065680a



Tests: pytest tests/test_facts_ledger.py tests/test_spring_signal_scan.py (expected)



Assumptions affected:



- `claude/10-architecture-maturation-plan.md` Phase 1 / fact-store ?no store yet? ? [New info ? thin sidecar `facts.jsonl` dual-emitted from Stage 0; maps kept; not cert-required]



- Decision memo §3 thin dual-emit ? [Resolved ? `doc_engine.scanning.facts` + CLI write + signal_scan outputs]



Files touched: src/doc_engine/scanning/facts.py, src/doc_engine/tools/spring_signal_scan.py, src/doc_engine/pipeline/stages.py, src/doc_engine/pipeline/runner.py, tests/test_facts_ledger.py, tests/test_spring_signal_scan.py, claude/research/facts-ledger-schema-2026-07-30.md, STATUS.md, claude/10-architecture-maturation-plan.md, claude/session-log.md







## 2026-07-30 ? Dual-emit observability + adoption-blocker queue



Commit: 065680a



Tests: pytest tests/test_facts_ledger.py tests/test_spring_signal_scan.py tests/test_pipeline_runner.py



Assumptions affected:



- Friend PE review adoption blockers vs fact-store Phase 1 ? [New info ? sequenced: dual-emit first; blockers queued in `claude/research/adoption-blockers-queue-2026-07-30.md`, not mixed into dual-emit]



- Operator Path A artifact list omitting facts.jsonl ? [Resolved ? pilot guide names sidecar as non-cert]



Files touched: src/doc_engine/scanning/facts.py, src/doc_engine/tools/spring_signal_scan.py, tests/test_facts_ledger.py, docs/guides/operator-pilot.md, claude/research/facts-ledger-schema-2026-07-30.md, claude/research/adoption-blockers-queue-2026-07-30.md, STATUS.md, claude/session-log.md







