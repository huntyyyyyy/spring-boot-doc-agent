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
- Real-time / climb / LTL-score as substitute for whole-repo oracle 98.7 (E-RT0)  
- In-tree Rust rewrite for “architecture assertion” without profile (Embody wheels only)  

---

## P5 — Test-suite BCs / CI shards

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P5.0 | **E-TEST0 Spec:** approve **T1–T18** + policy **T-A** | **DONE** (2026-08-08) | design memo APPROVED |
| P5.1 | **E-TEST1:** domain markers + CI shards; serial quarantine; doc_engine meeting ≥**98.7** (debt=`domain_unclassified` only) | **DONE** | marker check + ABI shard jobs |
| P5.2 | **E-TEST2 (optional):** xdist inside one non-oracle shard only | Defer / spike | flake budget; never oracle combine |

Research: [`docs/research/bounded-contexts/06-test-suite-bounded-contexts-parallel.md`](bounded-contexts/06-test-suite-bounded-contexts-parallel.md).

---

## P6 — CI workflow modularity

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P6.0 | **E-CI0 Spec:** approve **C1–C6** + policy **C-A** | **DONE** (2026-08-09) | design memo APPROVED |
| P6.1 | **E-CI1:** reusable workflows + scripts; `ci.yml` ≤200; LOC ratchet | **DONE** (2026-08-09) | `check_workflow_yaml` C4 |

Research: [`docs/research/ci/07-ci-workflow-modularity.md`](ci/07-ci-workflow-modularity.md).

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

Research: [`docs/research/coverage-quality/08-rust-test-runners-bottlenecks.md`](coverage-quality/08-rust-test-runners-bottlenecks.md). Prefer **2026** primaries (arXiv 2607/2602/2601/2605/2604; rpytest; OTel CI semconv).

---

## P8 — Test adequacy vs coverage inflation (2026 research)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P8.0 | **E-QA0 Spec:** approve **Q1–Q8** (necessary Cover% ≠ sufficient quality) | **Done** (2026-08-09) | research 09 `spec_gate: APPROVED E-QA0` + design stub |
| P8.1 | **E-QA1:** adequacy sensor ports + CI summary (structural + mutator survivors + metamorphic) | **Done** (2026-08-09) | `adequacy_summary` in python-gates always-summary |
| P8.2 | **E-QA2:** anti-padding Verify — climb packages need kill/metamorphic witness | **Done** (2026-08-09) | CONTRIBUTING Climb Archive / Q2 checklist |
| P8.3 | **E-QA3:** Hypothesis spike on pure helpers (`suite_timing` / fingerprints) | Spike after E-QA1 | focused suite |

Research: [`docs/research/coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md`](coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md). Prefer **2026** primaries (2607.22880, 2603.01409, 2604.01799, 2607.02057, 2605.22175, 2604.10126; mutmut; Hypothesis).

---

## P9 — Kitchen harness modernization (fixtures / ports)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P9.0 | **E-KH0 Spec:** approve **K1–K12** (pytest fixtures SoT; refuse Testcontainers/Spec Kit runtime/DI containers for kitchen) | **Done** (2026-08-09) | research 10 `spec_gate: APPROVED E-KH0` |
| P9.1 | **E-KH1:** `KitchenArtifacts` + session/package fixture; drop chapter `setUpModule`/`_STATE`; scratch copies for faults | **Done** (2026-08-09) | kitchen green; no chapter `setUpModule`; size/complexipy |
| P9.2 | Optional syrupy / Hypothesis — **not** kitchen chapter SoT | Align E-QA3; KH-S2 | spike exit criteria |

Research: [`docs/research/kitchen/10-kitchen-harness-modernization-2026.md`](kitchen/10-kitchen-harness-modernization-2026.md). Primaries: pytest fixtures docs + DeepWiki pytest/hypothesis/testcontainers; GitHub activity 2026-08-09; arXiv 2601.06615 (Fixturize), 2404.09398 (FlakyDoctor), 2606.04967 (SDD).

---

## P10 — CI / script output UX (summary-first)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P10.0 | **E-UX0 Spec:** approve **U1–U7** (summary-first; groups; shared append; refuse rich/LLM) | **Approved 2026-08-09** | research 11 `spec_gate: APPROVED E-UX0` |
| P10.1 | **E-UX1:** quality-gates markdown rollup + `::group::` + coverage/gap → `github_step_summary` | **Done** (#105, 2026-08-09) | step summary has gate table; no overwrite; size/complexipy |
| P10.2 | **E-UX2:** claims / code_quality headline + `<details>` | Later | optional |

Research: [`docs/research/ci/11-ci-output-ux-progressive-disclosure-2026.md`](ci/11-ci-output-ux-progressive-disclosure-2026.md).

---

## P11 — Pipeline / Stage-0 modularity (ports / vertical slices)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P11.0 | **E-MOD0 Spec:** approve **M1–M12** (CLI BCs; hexagonal Protocols; vertical slices; refuse DI/`utils`/mesh) | **Done** (2026-08-09) | research 12 `spec_gate: APPROVED E-MOD0` |
| P11.1 | **E-MOD1:** `mock_stages` split + `MockStageStrategy` Protocol/registry; stable façade; size baseline `--update` (MOD-S1) | **Done** (2026-08-09) | files ≤225; complexipy ≤5; kitchen/pipeline green |
| P11.2 | **E-MOD2:** `capacity_preflight` then drift/partition | **Done** (2026-08-09) | same gates; CLI flags/outputs stable |
| P11.3 | **E-MOD3:** `run_manifest` + `citation_coverage` wave 2 (ports + façades; MOD-S1) | **Done** (2026-08-09) | files ≤225; climb monkeypatch DIP; `-m` stable |
| P11.4 | **E-FAC0 / E-RES0 / E-CUR0:** façade poke + design-research + Cursor-native hooks | **Done** (2026-08-09) | poke gate; research hook; `.cursor/hooks.json` |

Research: [`docs/research/bounded-contexts/12-pipeline-stage0-modularity-ports-2026.md`](bounded-contexts/12-pipeline-stage0-modularity-ports-2026.md),
[`docs/research/bounded-contexts/13-tools-wave2-modularity-2026.md`](bounded-contexts/13-tools-wave2-modularity-2026.md),
[`docs/research/process/14-facade-poke-research-hooks-2026.md`](process/14-facade-poke-research-hooks-2026.md).

---

## P12 — Legacy size-offender remediation (grandfather → zero)

Do **not** leave `size_baseline.json` >225 files forever. Remediations are product
work: MOD-S1 + poke + intentionality bar (separate asserts, `monkeypatch`, one-act
`raises`). Never raise `FILE_LOC_HARD` / complexipy.

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P12.0 | **E-LEG0 Spec:** approve **LEG1–LEG10** (debt ledger; 2026 ports/tach/SDD; intentionality; refuse DI/LLM-MAS SoT) | **Approved 2026-08-09** | research 15 `spec_gate: APPROVED E-LEG0` |
| P12.1 | **E-SCAN1:** scanning vertical modularity (`scanning/astgrep/` + façade) | **Done** (2026-08-09) | size offender ↓; poke; complexipy ≤5; LEG8 on touched tests |
| P12.2 | **E-TOOL4 → E-PIPE1 → E-QUERY1 → E-STF1** | Later (ordered) | same gates; one BC tip at a time |
| P12.3 | **LEG-S1** (optional): tach vs import-linter measured gap on scanning | Spike / Defer | measured gap or Defer dual-SoT |

Research: [`docs/research/process/15-legacy-size-remediation-2026-frameworks.md`](process/15-legacy-size-remediation-2026-frameworks.md),
[`docs/research/bounded-contexts/16-scan1-astgrep-modularity-2026.md`](bounded-contexts/16-scan1-astgrep-modularity-2026.md).

---

## P13 — CodeQL signals CI skip (fingerprint)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P13.0 | **E-CQL0 Spec:** approve **CQ1–CQ9** (fingerprint skip; job `if:`; refuse paths-on-required / cache-as-SoR / overlay) | **Approved** (2026-08-09, merge) | research 17 `spec_gate: APPROVED E-CQL0` |
| P13.1 | **E-CQL1 Implement:** `codeql_signals_change_gate.py` + `codeql-signals.yml` gate; align `pre_pr` / CONTRIBUTING | **Done** (2026-08-09) (after E-DOC1) | expensive jobs skip when corpus unchanged; invariants always; fail-closed |

Research: [`docs/research/ci/17-codeql-signals-skip-fingerprint-2026.md`](ci/17-codeql-signals-skip-fingerprint-2026.md).

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
**Done (E-MOD3):** tools wave 2 — `run_manifest` / `citation_coverage` (2026-08-09).  
**Done (E-FAC0 / E-RES0):** façade poke gate + design-research hook (2026-08-09).  
**Done (E-LEG0):** legacy size-remediation Spec LEG1–LEG10 (2026-08-09).  
**Done (E-SCAN1 Spec + Implement):** SCAN1-A–J + `scanning/astgrep/` façade (2026-08-09).  
**Done (E-CQL0 Spec):** CQ1–CQ9 Approve (2026-08-09).  
**Done (E-DOC0 Spec):** DOC1–DOC12 Approve (2026-08-09).  
**Done (E-DOC1):** domain map + look-first hooks + `claude/`→`docs/` migrate (2026-08-09).  
**Done (E-STK0 Spec):** STK1–STK10 Approve (2026-08-09).  
**Done (E-COH0 Spec):** COH1–COH12 Approve (2026-08-09).  
**Combined tip (this PR):** fold `origin/cursor/local-ci-gate-fix-61f3` (PR #113) into REPO+CTX tip — nests (`semantic_eval`/`docs_site`), agent-context Spec drafts (26–28), and #113 local-CI / stalker / vacuity / cold-BC research.  
**Paused Active (stream note):** **E-COH1** reshape — CGQ3 Accept rows required (Concern→Remedy→Depth→Witness); resume after combined tip lands.  
**Shipped on combined tip:** **E-REPO1-A** nest + shims; **E-CTX0** research drafts (P36/P37).  
**Done slice (2026-08-09):** E-COH1 public-surface fitness + delete `support`/`inventory_drift` warehouses; `semantic_eval` public façade.  
**Done Spec + Implement:** **E-HOOK2** — local oracle Cover% remesure on push when src/tests change (2026-08-09); stalker/path-parity tests lift tip to ≥98.7.  
**Done Spec + Implement:** **E-CQL1** — CodeQL signals content-fingerprint skip of compile/runtime (2026-08-09).  
**Done Spec + Implement:** **E-TEL2** — path-parity sensors G8–G10 (2026-08-09).  
**Done Spec + Implement:** **E-SEL0 / E-SEL1** — fine ABI file paths + path→domain pre_pr pytest select (2026-08-09).  
**Done Spec + Implement:** **E-TEL0 / E-TEL1** — mutation_driver regression + local telemetry ETL + G7 (2026-08-09).  
**Done Spec + Implement:** **E-HOOK0 / E-HOOK1** — pre-push install/chain + local quality-gates; optional Sonar advisory (2026-08-09).  
**Done Spec + Implement:** **E-KNOB0 / E-KNOB1** — one setpoint owner per concern; no `quality_knobs` god file (2026-08-09).  
**Done Implement:** **E-STK1** — G1–G6 advisory sensors + ledger writer + `pre_pr` wire (2026-08-09).  
**Done Implement:** **E-HOT1** — G2 return/pass + AST witness; CQ HOT5; size soft test; cert patch-at-use; docs path; wrap ratchet retained.  
**Paused/Defer next:** cycle-focus rotator / LLM ranker (STK3) — not required for G1–G6 Accept.  
**Docs Spec Approved:** **E-STACK0** — stack rescope under ≥10k★ (Backstage scoped: corp IDP supported; CLI runtime Refuse).  
**Spec Approved:** **E-CGQ0** — CGQ1–CGQ10; probe via process/tools until E-GND.  
**Spec draft (parked):** **E-SOL0** — vocabulary landed; not tip-blocking.  
**Spec draft (demoted — later):** **E-GND0** — tip-grounding MCP; after E-COH1 has a green slice.  
**Spec draft (not Active tip):** **E-TACH0** — amend ★ justification (P19.1).  
**Spec draft (not Active tip):** **E-RT0** — realtime architecture/logic assertion envelope (P27.0); research 32.
**Spec draft (not Active tip):** **E-RUST0** — Rust quality toolscape BFS/DFS (P28.0); research 33. **E-POLY0 / E-POLY0b / E-LANG0** — polyglot + pilot-before-refuse + excellence domains (P28.2–4); process/39–41.
**Done Spec + Implement:** **E-SEARCH0** — allow ripgrep/Grep; prefer ast-grep for citations (2026-08-09).  
**Defer:** E-COH2 / E-TACH1–2; E-UX2; E-QA3; E-RUN2–5; **E-GND1**; **E-RT1** until E-RT0 Approve; **E-RUST1** until E-RUST0 Approve.  
**Never:** suite-wide xdist/rpytest-n on cov cell; RTS skipping oracle; fuzzy green; LLM-judge as fail_under; Testcontainers/Spec Kit WorkflowEngine as kitchen/runtime SoT; Guice-style DI; `utils/` grab-bag; `quality_knobs.py` mega-config; raising LOC/complexipy caps; forever-grandfather without remediation stream; workflow `paths` on required CI; chat-dump research SoT; DDIA-shaped nesting under `docs/research/`; mechanical LOC chops that fail E-COH0; push while local full-gate is red; **Backstage as doc-engine runtime / merge SoT**; ★-wash &lt;10k tools as new Adopt; Sonar/Spec Kit/Nx as boolean or runtime SoT; **Specs without CGQ3 Accept**; **MCP generate_code tip writer**; **parallel Active Spec drafts that pause Implement**; **climb/LTL/RT score as Cover% SoT**; **sibling tip branches for the same PR stream**; **in-tree Rust/WASM-by-default without profiled Spec**.

---

## P15 — Watch / stalker agents (findings → research → refactor, context-lean)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P15.0 | **E-STK0 Spec:** approve **STK1–STK10** (sensor-first ledger; rotating focus; chat reset; no oracle dilution) | **Approved** (2026-08-09) | research 19 `spec_gate: APPROVED E-STK0` |
| P15.1 | **E-STK1 Implement:** G1–G6 sensors + ledger writer + `pre_pr` advisory | **Done** (2026-08-09) | `stalker_scan --no-ledger`; tests/ci/test_stalker_sensors.py; complexipy ≤5 |

**E-STK1 acceptance sensors** (from incident ledger [`findings/2026-08-09-statement-split-cascade.md`](findings/2026-08-09-statement-split-cascade.md); Spec delta only until Active):

| ID | Kind | Detect |
| --- | --- | --- |
| G1 | `ratchet_schema_skew` | code `SCHEMA_VERSION` vs committed ratchet JSON |
| G2 | `split_scope_break` | prelude/core siblings with unpassed Names |
| G3 | `facade_api_regress` | consumers load `module._attr` missing from façade |
| G4 | `collect_or_syntax` | touched-path compile + collect on 3.10 and 3.12 |
| G5 | `process_parallel_tip` | backlog Active vs second tip writer |
| G6 | `policy_verify_incomplete` | schema bump without baseline `--update` + ABI smoke |

Research: [`docs/research/process/19-watch-stalker-agents-context-lean-2026.md`](process/19-watch-stalker-agents-context-lean-2026.md) §5.1 / §8 addendum. **Embody** sensors+ledger+react-doctor pattern; **Spike** headroom/loopx/gh-aw proposer; **Defer** claude-mem; **Refuse** agentmemory dep, context-mode (ELv2), alternate hosts. GH inventory still ≥1k★+14-day push for research SoR.

---

## P16 — Tach dependency-map-as-blueprint (BC layers → depends_on)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P16.0 | **E-TACH0 Spec:** approve **TACH1–TACH10** (deps as primary structure; tach-only fitness; layers then depends_on+interfaces; no sync-as-architecture) | **Draft** (2026-08-09) | research 20 `spec_gate` → APPROVED |
| P16.1 | **E-TACH1 Implement:** break BC cycles + add `layers` | After Approve; one stream | `tach check` green; one-way BC edges |
| P16.2 | **E-TACH2 Implement:** `depends_on` + `[[interfaces]]` | After E-TACH1 | undeclared/deep imports fail CI |

Research: [`docs/research/bounded-contexts/20-tach-dependency-blueprint-2026.md`](bounded-contexts/20-tach-dependency-blueprint-2026.md) (window **2026-06→08**). **Embody** tach cycles; **Adopt** layers→depends_on+interfaces; **Defer** import-linter dual-gate; **Refuse** pytestarch/grimp (&lt;1k★) and foreign runtimes as deps.

---

## P17 — Cohesion-first concept splits (design pass after MOD-S1 tip audit)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P17.0 | **E-COH0 Spec:** approve **COH1–COH12** (pause thrash; concept bar; façade≠private warehouse; seam map before moves) | **Approved** (2026-08-09) | design memo `spec_gate: APPROVED E-COH0` |
| P17.1 | **E-COH1 Implement:** reshape provisional tip modules under COH bar | **Active** (2026-08-09); public-surface slice Done | COH2–COH4 on touch; CGQ3 Accept; `check_public_surface` hard |
| P17.2 | **E-COH2:** align reshape with E-TACH1/2 layers + interfaces | After E-TACH0 Approve | `tach check`; public `expose` only |

Design: [`docs/design/concept-split-cohesion-design-2026-08-09.md`](../design/concept-split-cohesion-design-2026-08-09.md). Research: bounded-contexts/20. **Refuse** mechanical cut-and-paste that only clears LOC/statement gates.

---

## P18 — Post-merge gate repair (COH1 hotfix carve-out)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P18.0 | **E-HOT0 Spec:** approve **HOT1–HOT13** (G2 return/pass; patch-at-use; CQ slash-free scope; local-full before push; no tach-map / no E-STK1; **≥10k★** new external SoR) | **Approved** (2026-08-09) | research 21 + design memo `APPROVED E-HOT0` |
| P18.1 | **E-HOT1 Implement:** F1–F6 repairs only; `pre_pr --full` green before push | **Done** (2026-08-09) | focused suites + `pre_pr --full` overall=pass; G2 AST witness |

Research: [`docs/research/process/21-post-merge-gate-repair-cohesion-2026.md`](process/21-post-merge-gate-repair-cohesion-2026.md). Design: [`docs/design/post-merge-gate-repair-design-2026-08-09.md`](../design/post-merge-gate-repair-design-2026-08-09.md). Finding: [`findings/2026-08-09-statement-split-cascade.md`](findings/2026-08-09-statement-split-cascade.md).

---

## P19 — Stack rescope under ≥10k★ SoR

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P19.0 | **E-STACK0 Spec:** approve **STACK1–STACK12** (keep ≥10k pins; Confirmed exempt; Nx patterns for boundaries; tach cycles-only until re-Spec; Backstage = corp IDP OK / CLI runtime Refuse; no Sonar/Spec Kit runtime SoT) | **Approved** (2026-08-09) | research 22 + design memo `APPROVED E-STACK0` |
| P19.1 | Amend E-TACH0 draft ★ justification (Nx patterns + Confirmed tach vehicle) | After STACK Approve; docs only | research 20 frontmatter/verdict updated |
| P19.2 | Optional tool Spike (in-repo depends_on vs tach expansion) | After E-HOT1 green + human ask | Spike exit criteria |

Research: [`docs/research/process/22-stack-rescope-10k-star-bar-2026.md`](process/22-stack-rescope-10k-star-bar-2026.md). Design: [`docs/design/stack-rescope-10k-design-2026-08-09.md`](../design/stack-rescope-10k-design-2026-08-09.md).

---

## P20 — Concern→solution remedies (DDIA vocabulary → effective mechanisms)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P20.0 | **E-SOL0 Spec:** approve **SOL1–SOL12** (Accept requires named remedy vocabulary; SOL12 = depth via E-CGQ0 before Embody) | **Draft** (2026-08-09) | research 23 + design → APPROVED |
| P20.1 | E-COH1 / E-STK1 / E-TACH0 Specs cite SOL remedy ids **and** CGQ3 depth/witness | After E-CGQ0 + E-SOL0 Approve | Spec tables include Concern→Remedy→Depth→Accept |
| P20.2 | North-star companion `meta/effective-remedies.md` + page sections + depth fitness (SOL11) | **Landed** (2026-08-09) vocabulary pending CGQ | `test_ddia_north_star_depth` Effective remedies |

Research: [`docs/research/process/23-concern-to-solution-remedies-2026.md`](process/23-concern-to-solution-remedies-2026.md). Design: [`docs/design/concern-to-solution-remedies-design-2026-08-09.md`](../design/concern-to-solution-remedies-design-2026-08-09.md).

---

## P21 — Codegen-quality dimensions + remedy-mechanism depth

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P21.0 | **E-CGQ0 Spec:** approve **CGQ1–CGQ10** (pre-generation controls; depth rows; Accept Concern→Remedy→Depth→Witness; process probe until E-GND) | **Approved** (2026-08-09, velocity stamp) | research 24 + design `APPROVED E-CGQ0` |
| P21.1 | E-COH1 / E-STK1 Activate only with CGQ3 Accept rows | **Satisfied** (E-STK1 Done; E-COH1 Active) | Spec Accept cites process/24 §2 |

Research: [`docs/research/process/24-codegen-quality-dimensions-mechanism-depth-2026.md`](process/24-codegen-quality-dimensions-mechanism-depth-2026.md). Design: [`docs/design/codegen-quality-dimensions-design-2026-08-09.md`](../design/codegen-quality-dimensions-design-2026-08-09.md).

---

## P22 — Tip-grounding MCP (extend Stage-0 query isolation)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P22.0 | **E-GND0 Spec:** approve **GND1–GND10** (tip MCP grounding) | **Draft — demoted** (2026-08-09); after E-STK1 green | research 25 + design → APPROVED |
| P22.1 | **E-GND1 Implement:** tip tools + receipt hook | **Defer** until after E-STK1 (+ preferably E-COH1 slice) | isolation tests; no write tools |

Research: [`docs/research/process/25-tip-grounding-mcp-2026.md`](process/25-tip-grounding-mcp-2026.md). Design: [`docs/design/tip-grounding-mcp-design-2026-08-09.md`](../design/tip-grounding-mcp-design-2026-08-09.md).

---

## P23 — Quality policy setpoints (central discoverability, no god file)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P23.0 | **E-KNOB0 Spec:** approve **KNOB1–KNOB10** (one owner per concern; design registry; refuse mega-config) | **Approved** (2026-08-09) | research 26 + design `APPROVED E-KNOB0` |
| P23.1 | **E-KNOB1 Implement:** `complexity_policy` / `duplication_policy` / `package_scope`; wire floor echo | **Done** (2026-08-09) | `tests/ci/test_quality_setpoints.py`; no duplicate SoT literals |

Research: [`docs/research/process/26-quality-policy-setpoints-2026.md`](process/26-quality-policy-setpoints-2026.md). Design: [`docs/design/quality-policy-setpoints-design-2026-08-09.md`](../design/quality-policy-setpoints-design-2026-08-09.md). **Refuse** `quality_knobs.py` / `utils/` dump.

---

## P24 — Local pre-push hook as first-line quality (no remote required)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P24.0 | **E-HOOK0 Spec:** approve **HOOK1–HOOK12** (force-push pre-push; install/chain; local quality-gates; Sonar advisory; modern landscape ★ table; act/pre-commit Spikes) | **Approved** (2026-08-09, amended) | research 27 + design `APPROVED E-HOOK0` |
| P24.1 | **E-HOOK1 Implement:** `install_git_hooks` + wire `in_repo_quality_gates` + sonar-local advisory | **Done** (2026-08-09) | `install_git_hooks --check`; suite tests; pre_pr green |

Research: [`docs/research/process/27-local-pre-push-hook-2026.md`](process/27-local-pre-push-hook-2026.md). Design: [`docs/design/local-pre-push-hook-design-2026-08-09.md`](../design/local-pre-push-hook-design-2026-08-09.md).

---

## P25 — Local stalker telemetry ETL + mutation_driver remote-red

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P25.0 | **E-TEL0 Spec:** approve **TEL1–TEL10** (suite log ETL; G7 masked advisory; mutation_driver hard) | **Approved** (2026-08-09) | research 28 + design `APPROVED E-TEL0` |
| P25.1 | **E-TEL1 Implement:** fix driver import; regression tests; telemetry store; G7 | **Done** (2026-08-09) | `tests/ci/test_mutation_driver_entrypoint.py`; `test_stalker_telemetry.py` |

Research: [`docs/research/process/28-local-stalker-telemetry-etl-2026.md`](process/28-local-stalker-telemetry-etl-2026.md). Design: [`docs/design/local-stalker-telemetry-design-2026-08-09.md`](../design/local-stalker-telemetry-design-2026-08-09.md).

---

## P26 — Domain pytest select + fine ABI shards (local speed that bites)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P26.0 | **E-SEL0 Spec:** approve **SEL1–SEL10** (fine paths; path→domain pre_pr; refuse testmon/oracle xdist) | **Approved** (2026-08-09) | research 29 + design `APPROVED E-SEL0` |
| P26.1 | **E-SEL1 Implement:** mixed-dir file paths; `pytest_domain_select`; pre_pr wire + junit timing | **Done** (2026-08-09) | `test_pytest_domain_select.py`; climb paths are `.py` files |

Research: [`docs/research/process/29-local-domain-pytest-select-2026.md`](process/29-local-domain-pytest-select-2026.md). Design: [`docs/design/local-domain-pytest-select-design-2026-08-09.md`](../design/local-domain-pytest-select-design-2026-08-09.md).

---

## P27 — Real-time architecture & logic assertion (agents) — Spec only

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P27.0 | **E-RT0 Spec:** approve **RT0-1–RT0-8** (layered RT envelope; tool receipts; incremental fitness; refuse fake Cover%) | **DRAFT** (2026-08-09) — pending human Approve | research 32; no implement until Approve |
| P27.1 | **E-RT1 Implement** | Deferred | only after E-RT0 + E-TACH0/E-COH deps |

Research: [`docs/research/coverage-quality/32-realtime-architecture-assertion-agents-2026.md`](coverage-quality/32-realtime-architecture-assertion-agents-2026.md). **Embody** oracle≠climb + tach/ruff/ast-grep wheels; **Adopt** Spec-gated edit-time pack + receipts; **Refuse** LLM-judge SoT, in-tree Rust, climb-as-floor.

---

## P28 — Rust quality toolscape (BFS→DFS) — Spec only

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P28.0 | **E-RUST0 Spec:** approve **RUST0-1–RUST0-8** (Embody wheels; Adopt sensors; Refuse in-tree rewrite / climb-as-floor) | **DRAFT** (2026-08-09) — pending human Approve | research 33; no implement until Approve |
| P28.1 | **E-RUST1 Implement** slices | Deferred | only after E-RUST0 Approve + constitution gates |
| P28.2 | **E-POLY0 Spec:** polyglot CLI toolkit BFS (Rust/WASM/Go/TS/PyO3) — amends E-RUST0; Bloom Create lanes; Spike-only WASM/helpers | **DRAFT** (2026-08-10) — pending human Approve | [`process/39-polyglot-cli-toolkit-bfs-2026-08-10.md`](process/39-polyglot-cli-toolkit-bfs-2026-08-10.md) |
| P28.3 | **E-POLY0b Spec:** open marketplace BFS + **Pilot-before-Refuse** doctrine (Ruby, JVM, Elixir, PHP, Datalog, enterprise clusters; ranked pilots w/ keep/drop) | **DRAFT** (2026-08-10) — pending human Approve | [`process/40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md`](process/40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md) |
| P28.4 | **E-LANG0 Spec:** deep excellence domains→subdomains for Rust/Go/Ruby/Clojure/WASM + logo exemplars | **DRAFT** (2026-08-10) — pending human Approve | [`process/41-language-excellence-domains-subdomains-2026-08-10.md`](process/41-language-excellence-domains-subdomains-2026-08-10.md) |
| P28.5 | **E-POLY1 / E-LANG1** Spikes from Pilot-now queue (one tip stream) | Deferred | only after POLY0b + LANG0 Approve + keep/drop exits |

Research: [`docs/research/coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md`](coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md). Supersedes narrow gaps in research 32.

---

## P29 — Text search allow (ripgrep) — Done

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P29.0 | **E-SEARCH0 Spec + Implement:** allow Grep/rg; prefer ast-grep for citations; keep network deny | **Done** (2026-08-09) | research 34; `deny_text_search` allow; settings deny lifted; check F network half |

Research: [`docs/research/process/34-text-search-allow-ripgrep-2026.md`](process/34-text-search-allow-ripgrep-2026.md).

---

## P30 — Control-plane closed-loop (evidence-gated gates) — Spec

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P30.0 | **E-CPL0 Spec:** approve **CPL1–CPL12** (receipts; HEAD-bound harness; overall=pass admission; refuse TEE/daemon SoT) | **DRAFT** (2026-08-09) — pending human Approve | research 35 + design `DRAFT E-CPL0` |
| P30.1 | **E-CPL1 Implement:** CPL-G* fitness + TEL empty-log repair + harness HEAD pin | Deferred | only after E-CPL0 Approve (CPL1-1 tee repair may land under E-TEL0) |

Research: [`docs/research/process/35-control-plane-closed-loop-2026.md`](process/35-control-plane-closed-loop-2026.md). Design: [`docs/design/control-plane-closed-loop-design-2026-08-09.md`](../design/control-plane-closed-loop-design-2026-08-09.md). **Embody** Ford fitness + vacuous-witness fail-closed; **Adopt** Proof-or-Stop/Nidus *semantics*; **Refuse** Nix/TEE/SLSA-L3/daemon tip SoT.

---

## P31 — Tailored ast-grep packs (fixture + OCS + Python vacuity) — Spec

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P31.0 | **E-AST0 Spec:** approve **AST0-A–H** (three packs; vocabulary B1/B2 lock; OCS overlay campaign-only; vacuity hybrid) | **DRAFT** (2026-08-10) — pending human Approve | research `stage0/astgrep-tailored-packs-fixture-ocs-2026.md` + design stub |
| P31.1 | **E-AST1 Implement:** vacuity pack hard in `pre_pr` (AST0-E) even before B1/B2 | **Done** (2026-08-10) | `python -m doc_engine.ci.vacuity`; `vacuous_tests` hard suite |
| P31.2 | **E-AST2 Implement:** `sgconfig` + utils + vocabulary B1/B2 + Stage-0 id migrate | Deferred | only after E-AST0 Approve; no OCS merge SoT |

Research: [`docs/research/stage0/astgrep-tailored-packs-fixture-ocs-2026.md`](stage0/astgrep-tailored-packs-fixture-ocs-2026.md). Design: [`docs/design/astgrep-tailored-packs-design-2026-08-10.md`](../design/astgrep-tailored-packs-design-2026-08-10.md). Related: E-OCS0, E-SCAN1, RULE_ID_MIGRATION. **Embody** relational idioms + dual `@Name`/`@Name($$$)`; **Adopt** `sgconfig`/`utilDirs` + `vacuous` certain; **Refuse** rg-as-SoT / Artifactory CI SoT / in-tree Rust.

---

## P33 — OCS dual plant (E-OCS0/1) — Implement

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P33.0 | **E-OCS0 Spec** OCS1–OCS8 | **Approved** (2026-08-10) | research ci/36 + design |
| P33.1 | `plant_profile` + `run-plant.sh` fail-closed | **Done** (2026-08-10) | `test_plant_profile.py` |
| P33.2 | `remeasure_ocs_floors.py` + campaign `astgrep_ocs_floors.yml` | **Done** (2026-08-10) | dry-run default; `--write` opt-in; `test_remeasure_ocs_floors.py` |
| P33.3 | Live remeasure on operator checkout (Windows/VPN) | **In progress** | grading pack `docs/process/local-grading-pack.md` |
| P33.4 | Align campaign ast-grep `path_prefix` with CodeQL class-level predicate; keep plant floor **35** (revert false 45) | **Done** (2026-08-10) | rule `not inside method_declaration`; expectations note |
| P33.5 | Full `run-plant.sh ocs` + OpenAPI join + Messaging=0 evidence | Operator | P3 blocked until venv + Artifactory (see P34 live grade) |

---

## P34 — Operator/agent surface (CLI grade + MCP + structured retrieval) — Spec

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P34.0 | **E-OAS0 Spec:** approve **OAS1–OAS16** (RunContext; dual sinks; doctor; Typer grade-only; **human-review floor**; campaign OS×shell matrix; Refuse rich/OTel/embedding SoTs + unattended AI + universal emulator) | **DRAFT** (2026-08-10) — pending human Approve | research `process/37-operator-agent-surface-cli-mcp-rag-2026.md` + design stub |
| P34.1 | **E-OAS1 Implement:** grade surface (context + JSONL receipt + remediation) | Deferred | only after E-OAS0 Approve |
| P34.2 | **E-OAS2** MCP parity envelopes / stderr structured events | Deferred | after OAS1; MCP SDK pin still Deferred (GND9) |
| P34.3 | **E-OAS3** retrieval eval harness (campaign) | Optional | never embedding citation SoT |

Research: [`docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md`](process/37-operator-agent-surface-cli-mcp-rag-2026.md). Design: [`docs/design/operator-agent-surface-design-2026-08-10.md`](../design/operator-agent-surface-design-2026-08-10.md). Related: E-UX0, E-GND0 (separate DRAFT), E-OCS0. **Embody** RunContext + dual sinks + Stage-0 packets + **human-review floor**; **Adopt** clig.dev + actionable errors + Typer-for-grade-only + campaign OS×shell matrix; **Refuse** rich CI SoT / OTel tip SoT / embedding citation SoT / MCP codegen / **unattended AI merge** / **universal OS+terminal+phone emulator as CLI SoT**.

---

## P35 — Cold product BC portfolio (beyond E-OAS0) — Spec seeds

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P35.0 | Portfolio map: prioritize cold BCs (query, cert fold, facts, CodeQL/OpenAPI join, drift/capacity) | **Done** (research 2026-08-10) | [`cold-product-bc-research-map-2026-08-10.md`](cold-product-bc-research-map-2026-08-10.md) |
| P35.1 | **E-QUERY0 Spec** Q0-1–Q0-10 (packet/MCP isolation before QUERY1) | **DRAFT** | [`stage0/query-packet-bc-research-2026-08-10.md`](stage0/query-packet-bc-research-2026-08-10.md) + full D1 packet |
| P35.2 | **E-CERT0 Spec** C0-1–C0-8 (fold honesty before PIPE1) | **DRAFT** | [`bounded-contexts/certification-fold-phase-runner-2026-08-10.md`](bounded-contexts/certification-fold-phase-runner-2026-08-10.md) + D2 packet |
| P35.3 | **E-FACT0 / E-CQLJ0** Spec seeds (promote archive fact-store; OpenAPI↔facts join) | **DRAFT research** (D3/D4 packets) | design stubs still after QUERY0/CERT0 Approve order |
| P35.4 | **D1–D6 domain/subdomain taxonomy** (≥3 arXiv + ~10k★ repos + DeepWiki Evaluate/Create) | **Done** (research 2026-08-10) | [`cold-bc-domain-subdomain-taxonomy-2026-08-10.md`](cold-bc-domain-subdomain-taxonomy-2026-08-10.md) |
| P35.5 | **Dimensional mental map** (subdomain→dimensions; DDD/SOLID/patterns; CLI a11y/DX; RAG-later SoT/sensor/adapter/refuse) | **Done** (research 2026-08-10) | [`cold-bc-dimensional-mental-map-2026-08-10.md`](cold-bc-dimensional-mental-map-2026-08-10.md) + [`process/38-cli-dx-a11y-dual-sinks-2026-08-10.md`](process/38-cli-dx-a11y-dual-sinks-2026-08-10.md) |
| P35.6 | Implement any cold BC | **Blocked** | human Spec Approve per epic; DIM0 lattice coverage; one tip stream; no unattended AI |

**Embody** Stage-0 query + derived certification; **Adopt** structure-first retrieval patterns + SLSA honesty fields (pattern); **Refuse** embedding citation SoT / LWW cert / Spec Kit runtime / parallel tip thrash.

---

## P32 — Harn / Nimbus / noprop release scan (2026-08-10) — stance only

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P32.0 | Record Embody/Adopt/Refuse for Harn 0.10.69, Nimbus 0.2.1, noprop 0.0.4 vs E-RUST0 | **Done** (research) — **Refuse** all as product deps; pattern-only for receipts/seeds | [`coverage-quality/harn-nimbus-noprop-release-scan-2026.md`](coverage-quality/harn-nimbus-noprop-release-scan-2026.md) |
| P32.1 | Implement Harn runtime / Nimbus vault / noprop in tip | **Refuse** | no epic unless Evidenced gap vs denylist/Hypothesis/plant_profile |

---

## P14 — Docs research taxonomy + claude consolidation + look-first

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P14.0 | **E-DOC0 Spec:** approve **DOC1–DOC12** (domains ≤2 deep; migrate `claude/` valuables; Cursor hooks look-first; keep adapter) | **Approved** (2026-08-09, merge) | research 18 `spec_gate: APPROVED E-DOC0` |
| P14.1 | **E-DOC1 Implement:** domain map + hooks + migrate + claims rewrite | **Done** (2026-08-09) | claims green; design writes denied without research-map Read; marketplace intact |

Research: [`docs/research/process/18-docs-research-taxonomy-claude-consolidation-2026.md`](process/18-docs-research-taxonomy-claude-consolidation-2026.md).

---

## P36 — DDD repository structure (quality + future-capability backcast) — E-REPO

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P36.0 | **E-REPO0 Spec:** approve **REPO1–REPO24** (packet **21–24**) | **Draft** research; Wave 0–0.5 orientation shipped | DOMAIN_MAP + inventory + behavior |
| P36.1 | **E-REPO1-A Implement:** nest `semantic_eval` + `docs_site` + shims (memo **25**) | **This tip** | `-m` shim; pytest; poke; inventory `nested` |
| P36.2 | **E-REPO1-B:** cycle-break → scanning/gates nests; larger partition | After A merges | one-way edges; tach |
| P36.3 | Spikes + **root `skills/` retire Spec** | Spike | equality rewrite + go/no-go |

Research: [`21`](bounded-contexts/21-ddd-repository-structure-options-2026.md)–[`24`](bounded-contexts/24-ddd-repo-structure-landing-gaps-2026.md) · [`25`](bounded-contexts/25-e-repo1-first-nest-prune-2026.md). **Orientation SoT:** [`DOMAIN_MAP.md`](../../DOMAIN_MAP.md).

---

---

## P37 — Agent context hygiene (huge markdown / working set) — E-CTX

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P37.0 | **E-CTX0 Spec:** approve **CTX1–CTX26** (working set; ★ discernment; **algorithm-first build/orchestrate**; mask≻token-prune≻viral MCP) | **Draft** (2026-08-10) | research **26+27+28** → APPROVED |
| P37.1 | **E-CTX1 Implement:** tip-brief + `ObservationMaskPolicy` port (Complexity Trap / AGORA floor) + AGENTS blurb | After Approve | claims; complexipy≤5; CTX-S1 |
| P37.2 | **CTX-S1/S2** token measure + optional StarScout/heuristic audit | Spike | numbers + integrity flags |

Research: [`26`](process/26-agent-context-markdown-bloat-2026.md) · [`27`](process/27-agent-context-repo-discernment-2026.md) · [`28`](process/28-agent-context-algorithm-first-2026.md). **Embody** algorithm+Accept; **Adopt** observation/step masking we own; **Refuse** ★-products, token-prune of actions, CompactionRL-as-SoT, summary-as-SoR.



<!-- combined: includes #117 RAG/DS/CLI research -->
