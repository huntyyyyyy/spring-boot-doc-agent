# Session log — 2026-07-30

Lead: **Un-dark-skip drift_normalization; certification Usage docstring**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 8. Newest at the bottom of this file.

---

## 2026-07-30 ? Un-dark-skip drift_normalization; certification Usage docstring



Commit: 2fc19a4



Tests: 37 passed (drift_normalization + live_gates + verify_certification + code_quality baseline)



Assumptions affected:



- `test_drift_normalization` "fixtures or ast-grep unavailable" skip means a real env gap ? [Resolved ? was AttributeError on removed `find_ast_grep`, swallowed into SkipTest while CI had ast-grep; probe is `which` + nested fixture paths]



- Known wrap false-positive pin of 2 / only `api_surface__mapping` ? [New info ? live measure is 12 across annotation-arg rules; semantic arm path labels use nested report paths]



- Runnable `certification.py` docstring contract ? [Resolved ? Usage line for `python -m doc_engine.tools.certification`]



Files touched: tests/ratchets/test_drift_normalization.py, scripts/ratchets/drift_match_normalizers.py, scripts/ratchets/java_perturbations.py, src/doc_engine/tools/certification.py, claude/session-log.md







## 2026-07-30 ? B2.5 certification as derived view (DDIA)



Commit: 49dd7b0



Tests: 62 passed (compliance + live_gates + verify_certification + artifact_schemas)



Assumptions affected:



- Live gates LWW-merges prior stages and stamps generative_executor=live ? [Resolved ? `stages_for_live_certification` keeps deterministic rows, drops generative/mock, appends `generative_external`]



- Stage MOCK status erased to ok with no executor provenance ? [Resolved ? `StageRecord.executor`; additive on schema_version 1]



- Any non-ok stage fails cert (skipped poisons live rewrite) ? [Resolved ? skip fails only if stage required by profile; mock_under_live consistency]



- Adoption-blockers B2.5 open ? [Resolved]



Files touched: src/doc_engine/pipeline/compliance.py, src/doc_engine/pipeline/live_gates.py, scripts/schemas/certification.schema.json, action.yml, tests/doc_engine/test_compliance.py, tests/doc_engine/test_live_gates.py, src/doc_engine/pipeline/adapters.md, claude/research/certification-derived-view-2026-07-30.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/session-log.md







## 2026-07-30 ? B3 strict citations on live gates



Commit: f89edfe



Tests: 38 passed (live_gates + compliance)



Assumptions affected:



- Live gates citation_coverage is worklist-only unless `--strict-citations` ? [Resolved ? certified profile (default / `--compliance-profile certified`) enables `--strict`, shared `citations_are_strict`]



- Adoption-blockers B3 open ? [Resolved]



Files touched: src/doc_engine/pipeline/live_gates.py, src/doc_engine/pipeline/compliance.py, src/doc_engine/pipeline/local_runner.py, src/doc_engine/cli.py, tests/doc_engine/test_live_gates.py, tests/doc_engine/test_compliance.py, claude/research/adoption-blockers-queue-2026-07-30.md, src/doc_engine/pipeline/adapters.md, claude/session-log.md





## 2026-07-30 ? L1 semgrep FP ratchet + DDIA north-star + coverage SoR hygiene

Commit: 1b12600

Tests: 32/32 passed (ddia north-star catalog + semgrep_rule_coverage); check_repo_claims OK

Assumptions affected:

- Semgrep coverage is positive-only / no FP measurement ? [Resolved ? negatives + check_fp_ratchet + semgrep_rule_fp_baseline.json; cite coverage-gates]

- CLAUDE/CONSTRAINTS/tool-quirks say rule_coverage reads rule_fixtures ? [Resolved ? spring_signals + CodeQL denominator; rule_fixtures metamorphic-owned]

- STATUS Next engineering still lists B1?B4 themes ? [Resolved ? B1?B5 done; L1/L2 sequencing; ddia-north-star link]

- Adoption-blockers Explicitly later unnumbered ? [Resolved ? L1 done ? L6 queued]

- DDIA guidance trapped in chat / memory ? [Resolved ? claude/research/ddia-north-star/ catalog for build/review/refactor]

Files touched: claude/research/ddia-north-star/**, claude/research/coverage-sor-derived-blindspot-2026-07-30.md, claude/research/adoption-blockers-queue-2026-07-30.md, scripts/coverage/semgrep_rule_coverage.py, scripts/coverage/semgrep_rule_fixtures_negative/**, scripts/coverage/semgrep_rule_fp_baseline.json, tests/coverage/test_semgrep_rule_coverage.py, tests/research/test_ddia_north_star_catalog.py, CLAUDE.md, CONSTRAINTS.md, STATUS.md, claude/tool-quirks.md, claude/steering-prompts/10-review-persona-and-standards.md, .github/workflows/ci.yml, claude/session-log.md



## 2026-07-30 ? Relocate DDIA north-star to docs/design; deepen + deviations

Commit: 065680a

Tests: 13/13 passed (ddia north-star catalog); check_repo_claims OK

Assumptions affected:

- DDIA catalog lives under claude/research (LLM-concentrated) ? [Resolved ? moved to docs/design/ddia-north-star/; claude path is redirect stub]

- Chapter atlases are title-thin ? [Resolved ? ch01?ch14 have who/what/when/where/why/how + principal questions; honest partial where thin]

- Project DDIA deviations are blind spots ? [Resolved ? deviations/ registry with upstream check + rejected band-aids; three seed entries]

- Flat concepts/playbooks/chapters layout hard to navigate ? [Resolved ? six nested domains + relationships]

Files touched: docs/design/**, claude/research/ddia-north-star/README.md (stub), STATUS.md, docs/product-architecture.md, claude/steering-prompts/10-review-persona-and-standards.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/research/coverage-sor-derived-blindspot-2026-07-30.md, scripts/coverage/semgrep_rule_coverage.py, tests/research/test_ddia_north_star_catalog.py, claude/session-log.md



## 2026-07-30 ? DDIA thorough campaign waves A?E + L2 capacity upper_bound

Commit: 065680a

Tests: 39/39 passed (ddia depth+catalog + capacity_preflight Stage4 polarity)

Assumptions affected:

- Capacity preflight under-states Stage-4 after cross-group edges ? [Resolved ? stage4_*_upper_bound fields, VALID_DOC_FILES fan-out, signals wiring, polarity tests; cite domain 07 / rel-partition-bounds-fanout]

- North-star thin / incomplete domains 07?10 and outline chapters ? [Resolved ? domains 07?10; ch01?ch14 operational with section digests; honest partial only for domain 06 + two lite concepts]

- Operational completeness Goodhartable by line count ? [Resolved ? depth gate Fail-if + epub/repo anchors + section digests + operational_count_baseline ratchet]

- Prior art / SoR hierarchy / cite-or-deviate unstated ? [Resolved ? meta/prior-art.md; README hierarchy; prompt-10 + catalog path check]

Files touched: src/doc_engine/tools/capacity_preflight.py, tests/doc_engine/test_capacity_preflight.py, tests/research/test_ddia_north_star_*.py, docs/design/ddia-north-star/**, STATUS.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/steering-prompts/10-review-persona-and-standards.md, claude/session-log.md



## 2026-07-30 ? Honesty unblock: partial_proxy + demote hollow + anti-Goodhart depth

Commit: 065680a

Tests: 44/44 passed (ddia depth+catalog + capacity_preflight Stage4 proxy honesty)

Assumptions affected:

- L2 Stage-4 capacity risk closed / upper_bound of full Stage-4 input ? [New info ? rejected; metric_kind is partial_proxy_pre_stage4 with interview/architecture/returns omitted; cite rel-partition-bounds-fanout]

- Operational completeness certifiable by shared Fail-if boilerplate / hollow domains ? [Resolved ? demote ch04/ch10/domains 08/10; Fail-if uniqueness N=5; domain must own local concepts/]

- STATUS/queue claimed campaign/L2 done ahead of merge ? [Resolved ? L2 open; N-wave honesty pass required; cite claims-and-status-drift]

Files touched: src/doc_engine/tools/capacity_preflight.py, tests/doc_engine/test_capacity_preflight.py, tests/research/test_ddia_north_star_*.py, docs/design/ddia-north-star/**, STATUS.md, claude/research/adoption-blockers-queue-2026-07-30.md, claude/session-log.md



## 2026-07-30 ? UTF-8 session-log + capacity skill partial_proxy + L2b queue

Commit: 065680a

Tests: check_repo_claims OK after cp1252?utf-8 rewrite

Assumptions affected:

- session-log append via PowerShell Add-Content is UTF-8 safe ? [Resolved ? false; rewrite as UTF-8; never Add-Content default]

- capacity-preflight skill still describes magic 14 / no Stage-4 proxy ? [Resolved ? partial_proxy_pre_stage4 + L2b follow-up named]

- N-wave Wave E not done vs honesty pass ? [Resolved ? honesty pass for slice; campaign still open for hollow domains]

Files touched: claude/session-log.md, claude/research/adoption-blockers-queue-2026-07-30.md, skills/capacity-preflight/SKILL.md, adapters/claude/skills/capacity-preflight/SKILL.md



