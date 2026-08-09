---
title: Quality backlog — ordered SDD next actions
status: ACTIVE — one stream at a time
date: 2026-08-08
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
rule: Spec → Implement → Verify → Archive; no parallel SoT thrash
---

# Quality backlog (ordered)

Process for each item: **Spec** (point at decision bullets) → **Implement** (single
stream) → **Verify** (deterministic gates) → **Archive** (CONTRIBUTING / claims as needed).

**Hard invariants:** do not weaken `fail_under=98.7`, complexipy ≤5, or size ≤225.
**Dual-mode code** only after human approve of synthesis decisions **1–31** (min subset
**13–17, 19–21, 25–26, 29**).

---

## P0 — Unblock size / facade debt (LOC-first)

Do these **before** dual-mode if size ratchet fails on touched modules.

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P0.1 | Thin `cli.py` / coverage parsers toward ≤225 (existing `_add_coverage_cli_parsers` or sibling — **no utils bag**) | Embody decision **10** | size-ratchet; complexipy ≤5 |
| P0.2 | Any new measure module starts ≤225 LOC; prefer vertical `doc_engine.ci.coverage_*` slices | Embody DDD / vertical slicing | size + tach |

---

## P1 — Design approval (no code) — DONE E-CM0

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P1.1 | Human approve synthesis decisions **1–31** (or explicit subset) | Strategic | Recorded Approve in design memo |
| P1.2 | Record climb artifact policy **16**: **(A)** distinct XML path **or** **(B)** refuse writing `coverage.xml` | Adopt | **16-A** locked (`coverage.climb.xml`) |
| P1.3 | Update `docs/design/coverage-measure-modes-design-2026-08-08.md` status to approved + point at synthesis | Archive | status APPROVED E-CM0 |

---

## P2 — Dual-mode implement (only after P1)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P2.1 | `MeasureMode.ORACLE \| CLIMB` strategies / hexagonal ports; shared wipe + PathCohesion | Adopt **13**, **18** | unit tests; complexipy ≤5; no if/elif god |
| P2.2 | Climb: scoped `--cov`, **no** whole-repo fail_under; stderr banner **11** | Adopt **2–3**, **11**, **17** | tests assert refuse floor claim |
| P2.3 | Implement artifact policy from P1.2 | Adopt **16** | gap-average still reads oracle XML only |
| P2.4 | Naming bar: `scope_package`, `fail_under_floor`, … — no `m`/`o`/`c` | Adopt **14**, **24** | review |
| P2.5 | CONTRIBUTING table: Oracle vs Climb vs Gap vs diff-cover + saliency cadence | Adopt **5**, **26** | claims paths resolve |

---

## P3 — Process / agent hygiene — DONE E-CM2

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P3.1 | Agent prompts / steering: climb ≠ floor; remesure oracle only on salient triggers | Adopt **17**, **26** | CONTRIBUTING saliency cadence |
| P3.2 | Encode SDD one-stream in wave1 PR template / CONTRIBUTING note | Adopt **21** | CONTRIBUTING + `.github/pull_request_template.md` |
| P3.3 | Explicit refuse: ungated CONSTRAINTS/baseline rewrite; LLM-judge as fail_under | Refuse **19**, **20** | CONTRIBUTING refuse table + Rust memo link |

---

## P4 — Optional later (not prerequisites)

| # | Action | Stance | Notes |
| --- | --- | --- | --- |
| P4.1 | Climb targeting hysteresis (dead-band file re-pick) | Adopt **27** | Advisory only |
| P4.2 | xdist on climb | Refuse v1 / defer **8** | After modes stable; also after E-TEST shards if ever |
| P4.3 | Carbon-aware CI scheduling | Optional **23**, **31** | Never block oracle work |
| P4.4 | Profiled Rust helper (not default) | Refuse unless profiled **22** | Linked from CONTRIBUTING / design index |
| P4.5 | Simple CI/agent remesure rate caps | Adopt if storms persist **28** | Before any PID |

---

## Explicit Refuse (do not schedule)

- Scoped Cover% or LLM-judge as 98.7 proof  
- PID / fuzzy “confidence of green” on oracle floor  
- SoA / DOD / ECS / neuromorphic runtime rewrites of `doc_engine`  
- Service mesh, Backstage-required IDP, Argo/Flux product deps  
- Spec Kit WorkflowEngine as mandatory runtime  
- Cross-worktree `coverage combine`  
- Cov cells on every Python version  
- Parallel tip thrash on SoT files  
- Suite-wide pytest-xdist before E-TEST domain shards (policy **T-A**)  
- Cross-job `coverage combine` to parallelize the oracle cell  

---

## P5 — Test-suite BCs / CI shards

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P5.0 | **E-TEST0 Spec:** approve **T1–T18** + policy **T-A** | **DONE** (2026-08-08) | design memo APPROVED |
| P5.1 | **E-TEST1:** domain markers + CI shards; serial quarantine; doc_engine meeting ≥**98.7** (debt=`domain_unclassified` only) | **DONE** | marker check + ABI shard jobs |
| P5.2 | **E-TEST2 (optional):** xdist inside one non-oracle shard only | Defer / spike | flake budget; never oracle combine |

Research: [`docs/research/06-test-suite-bounded-contexts-parallel.md`](06-test-suite-bounded-contexts-parallel.md).

---

## P6 — CI workflow modularity

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P6.0 | **E-CI0 Spec:** approve **C1–C6** + policy **C-A** | **DONE** (2026-08-09) | design memo APPROVED |
| P6.1 | **E-CI1:** reusable workflows + scripts; `ci.yml` ≤200; LOC ratchet | **DONE** (2026-08-09) | `check_workflow_yaml` C4 |

Research: [`docs/research/07-ci-workflow-modularity.md`](07-ci-workflow-modularity.md).

---

## Suggested next single stream

**Done (E-CM0–2):** dual-mode Spec/impl/docs.  
**Done (E-TEST0–1):** domain markers + ABI shards.  
**Done (E-CI0):** Spec approve **C1–C6** + policy **C-A**.  
**Done (E-CI1):** thin `ci.yml` + reusable BCs + LOC/heredoc SoT.  
**Never:** suite-wide xdist before shards; fuzzy green; Spec Kit WorkflowEngine as CI runtime.
