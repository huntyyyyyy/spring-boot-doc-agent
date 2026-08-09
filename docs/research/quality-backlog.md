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

## P7 — Suite stalking feature space (2026 research)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P7.0 | **E-RUN0 Spec:** approve **R1–R8** (dimensions D1–D20 map) | **Done** (2026-08-09) | research 08 `spec_gate: APPROVED E-RUN0` + design stub |
| P7.1 | **E-RUN1:** oracle (+ optional ABI) durations + pre-pytest cascade clarity (**D1/D17**) | **Active** (v1 sensors) | CI log / artifact |
| P7.2 | **E-RUN2:** plateau map + optional durations ⋈ gap-average (**D2/D15**) | D2 in E-RUN1 presenter; D15 defer | script or summary section |
| P7.3 | **E-RUN3:** rpytest `--verify-dropin` spike on one `domain_*` (**D3**) | Spike / refuse if &lt;15% or drop-in fail | wall-clock + parity |
| P7.4 | **E-RUN4:** NameRTS-shaped selection + agent card behind `pre_pr` only (**D9/D18**) | Adopt after Spec · never oracle | `pre_pr` receipt |
| P7.5 | **E-RUN5:** advisory flake/job log triage (**D7/D8**) | Defer | non-blocking artifact |

Research: [`docs/research/08-rust-test-runners-bottlenecks.md`](08-rust-test-runners-bottlenecks.md). Prefer **2026** primaries (arXiv 2607/2602/2601/2605/2604; rpytest; OTel CI semconv).

---

## P8 — Test adequacy vs coverage inflation (2026 research)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P8.0 | **E-QA0 Spec:** approve **Q1–Q8** (necessary Cover% ≠ sufficient quality) | **Done** (2026-08-09) | research 09 `spec_gate: APPROVED E-QA0` + design stub |
| P8.1 | **E-QA1:** adequacy sensor ports + CI summary (structural + mutator survivors + metamorphic) | **Done** (2026-08-09) | `adequacy_summary` in python-gates always-summary |
| P8.2 | **E-QA2:** anti-padding Verify — climb packages need kill/metamorphic witness | **Done** (2026-08-09) | CONTRIBUTING Climb Archive / Q2 checklist |
| P8.3 | **E-QA3:** Hypothesis spike on pure helpers (`suite_timing` / fingerprints) | Spike after E-QA1 | focused suite |

Research: [`docs/research/09-test-adequacy-vs-coverage-inflation-2026.md`](09-test-adequacy-vs-coverage-inflation-2026.md). Prefer **2026** primaries (2607.22880, 2603.01409, 2604.01799, 2607.02057, 2605.22175, 2604.10126; mutmut; Hypothesis).

---

## P9 — Kitchen harness modernization (fixtures / ports)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P9.0 | **E-KH0 Spec:** approve **K1–K12** (pytest fixtures SoT; refuse Testcontainers/Spec Kit runtime/DI containers for kitchen) | **Done** (2026-08-09) | research 10 `spec_gate: APPROVED E-KH0` |
| P9.1 | **E-KH1:** `KitchenArtifacts` + session/package fixture; drop chapter `setUpModule`/`_STATE`; scratch copies for faults | **Done** (2026-08-09) | kitchen green; no chapter `setUpModule`; size/complexipy |
| P9.2 | Optional syrupy / Hypothesis — **not** kitchen chapter SoT | Align E-QA3; KH-S2 | spike exit criteria |

Research: [`docs/research/10-kitchen-harness-modernization-2026.md`](10-kitchen-harness-modernization-2026.md). Primaries: pytest fixtures docs + DeepWiki pytest/hypothesis/testcontainers; GitHub activity 2026-08-09; arXiv 2601.06615 (Fixturize), 2404.09398 (FlakyDoctor), 2606.04967 (SDD).

---

## P10 — CI / script output UX (summary-first)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P10.0 | **E-UX0 Spec:** approve **U1–U7** (summary-first; groups; shared append; refuse rich/LLM) | **Approved 2026-08-09** | research 11 `spec_gate: APPROVED E-UX0` |
| P10.1 | **E-UX1:** quality-gates markdown rollup + `::group::` + coverage/gap → `github_step_summary` | **Done** (#105, 2026-08-09) | step summary has gate table; no overwrite; size/complexipy |
| P10.2 | **E-UX2:** claims / code_quality headline + `<details>` | Later | optional |

Research: [`docs/research/11-ci-output-ux-progressive-disclosure-2026.md`](11-ci-output-ux-progressive-disclosure-2026.md).

---

## P11 — Pipeline / Stage-0 modularity (ports / vertical slices)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P11.0 | **E-MOD0 Spec:** approve **M1–M12** (CLI BCs; hexagonal Protocols; vertical slices; refuse DI/`utils`/mesh) | **Done** (2026-08-09) | research 12 `spec_gate: APPROVED E-MOD0` |
| P11.1 | **E-MOD1:** `mock_stages` split + `MockStageStrategy` Protocol/registry; stable façade; size baseline `--update` (MOD-S1) | **Done** (2026-08-09) | files ≤225; complexipy ≤5; kitchen/pipeline green |
| P11.2 | **E-MOD2:** `capacity_preflight` then drift/partition | **Done** (2026-08-09) | same gates; CLI flags/outputs stable |

Research: [`docs/research/12-pipeline-stage0-modularity-ports-2026.md`](12-pipeline-stage0-modularity-ports-2026.md).

---

## P12 — E-SCAN1 AstGrepBackend modularity

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P12.0 | **E-SCAN1 Spec:** approve **SCAN1-A–J** (astgrep package; hash paths; runner Protocol; structure tests; LEG8) | **Approved 2026-08-09** | research 16 `spec_gate: APPROVED E-SCAN1` |
| P12.1 | **E-SCAN1 Implement:** `scanning/astgrep/` + thin `_scanner_astgrep` façade; size `--update` | **Active** (2026-08-09) | LOC ≤225; poke; complexipy ≤5; stage0 suites |

Research: [`docs/research/16-scan1-astgrep-modularity-2026.md`](16-scan1-astgrep-modularity-2026.md).

---

## Suggested next single stream

**Done (E-CM0–2):** dual-mode Spec/impl/docs.  
**Done (E-TEST0–1):** domain markers + ABI shards.  
**Done (E-CI0–1):** thin `ci.yml` + reusable BCs + LOC/heredoc SoT.  
**Done (E-RUN0–1):** suite-stalking sensors Spec + D1/D2/D17.  
**Done (#105):** oracle stabilize to **98.7** (necessary floor) + E-UX1 summary-first UX.  
**Done (E-QA0–2):** adequacy Spec + sensors + Climb Archive Q2 witness checklist.  
**Done (E-UX0–1):** UX Spec Approve + quality-gates / step-summary append slice.  
**Done (E-KH0):** K1–K12 Approve (2026-08-09).  
**Done (E-KH1):** `KitchenArtifacts` + session fixtures; chapters off `setUpModule`/`_STATE` (2026-08-09).  
**Done (E-MOD0):** M1–M12 Spec Approve (2026-08-09).  
**Done (E-MOD1):** `mock_stages` concept modules + `MockStageStrategy` registry (2026-08-09).  
**Done (E-MOD2):** Stage-0 tool façades — `capacity_preflight` / `spring_drift_check` / `partition_repo` (2026-08-09).  
**Done (E-SCAN1 Spec):** SCAN1-A–J Approve (2026-08-09).  
**Active:** **E-SCAN1** — split `_scanner_astgrep` into `scanning/astgrep/` (research 16).  
**Defer:** E-UX2 (U6); E-QA3 Hypothesis spike; E-RUN2 D15 / E-RUN3–5.  
**Never:** suite-wide xdist/rpytest-n on cov cell; RTS skipping oracle; fuzzy green; LLM-judge as fail_under; scrap Cover%/E-TEST because mutation exists; Testcontainers/Spec Kit WorkflowEngine as kitchen SoT; rich/emoji CI dashboards as SoT; Guice-style DI / pytest-bdd as kitchen SoT; `utils/` grab-bag; raising LOC/complexipy caps.
