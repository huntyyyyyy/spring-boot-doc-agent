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

Research: [`docs/research/modularity/06-test-suite-bounded-contexts-parallel.md`](modularity/06-test-suite-bounded-contexts-parallel.md).

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

Research: [`docs/research/modularity/12-pipeline-stage0-modularity-ports-2026.md`](modularity/12-pipeline-stage0-modularity-ports-2026.md),
[`docs/research/modularity/13-tools-wave2-modularity-2026.md`](modularity/13-tools-wave2-modularity-2026.md),
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
[`docs/research/modularity/16-scan1-astgrep-modularity-2026.md`](modularity/16-scan1-astgrep-modularity-2026.md).

---

## P13 — CodeQL signals CI skip (fingerprint)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P13.0 | **E-CQL0 Spec:** approve **CQ1–CQ9** (fingerprint skip; job `if:`; refuse paths-on-required / cache-as-SoR / overlay) | **Approved** (2026-08-09, merge) | research 17 `spec_gate: APPROVED E-CQL0` |
| P13.1 | **E-CQL1 Implement:** `codeql_signals_change_gate.py` + `codeql-signals.yml` gate; align `pre_pr` / CONTRIBUTING | **Deferred** (after E-DOC1) | expensive jobs skip when corpus unchanged; invariants always; fail-closed |

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
**Active:** **E-COH1** reshape — **paused** until **E-CGQ0** Approve + CGQ3 Accept rows (characterization depth + structural probe); must not Spec from DDIA/remedy labels alone.  
**Done Implement:** **E-HOT1** — G2 return/pass + AST witness; CQ HOT5; size soft test; cert patch-at-use; docs path; wrap ratchet retained.  
**Docs Spec Approved:** **E-STACK0** — stack rescope under ≥10k★ (Backstage scoped: corp IDP supported; CLI runtime Refuse).  
**Active Spec draft:** **E-CGQ0** — codegen-quality dimensions + remedy-mechanism depth ([`process/24-…`](process/24-codegen-quality-dimensions-mechanism-depth-2026.md)); Approve **CGQ1–CGQ10**.  
**Spec draft (paired):** **E-SOL0** — concern→solution vocabulary ([`process/23-…`](process/23-concern-to-solution-remedies-2026.md)); Approve **SOL1–SOL12** (SOL12 = vocabulary until CGQ depth). Catalog companion landed; depth fitness = section presence only.  
**Spec draft (not Active tip):** **E-TACH0** — amend ★ justification (P19.1) before depends_on Approve.  
**Defer:** E-CQL1 (ready); E-STK1 (ready — after CGQ3); E-COH2 / E-TACH1–2; E-UX2 (U6); E-QA3; E-RUN2–5; E-CQL cache accel (CQ-S1).  
**Never:** suite-wide xdist/rpytest-n on cov cell; RTS skipping oracle; fuzzy green; LLM-judge as fail_under; Testcontainers/Spec Kit WorkflowEngine as kitchen/runtime SoT; Guice-style DI; `utils/` grab-bag; raising LOC/complexipy caps; forever-grandfather without remediation stream; workflow `paths` on required CI; chat-dump research SoT; DDIA-shaped nesting under `docs/research/`; mechanical LOC chops that fail E-COH0; push while local full-gate is red; **Backstage as doc-engine runtime / merge SoT** (corp IDP + optional catalog metadata OK); ★-wash &lt;10k tools as new Adopt; Sonar/Spec Kit/Nx as boolean or runtime SoT; **Specs that only cite DDIA page ids or bare remedy labels without depth-row cite (SOL1 / CGQ3)**; **Embody new fitness from catalog ids before E-CGQ0 Approve (CGQ2/CGQ6)**.

---

## P15 — Watch / stalker agents (findings → research → refactor, context-lean)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P15.0 | **E-STK0 Spec:** approve **STK1–STK10** (sensor-first ledger; rotating focus; chat reset; no oracle dilution) | **Approved** (2026-08-09) | research 19 `spec_gate: APPROVED E-STK0` |
| P15.1 | **E-STK1 Implement:** finding schema + cycle CLI/hook + backlog presenter | Deferred (ready; pick as Active) | context resets; claims green; LOC/complexipy; **first sensors G1–G6** (below) |

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

Research: [`docs/research/modularity/20-tach-dependency-blueprint-2026.md`](modularity/20-tach-dependency-blueprint-2026.md) (window **2026-06→08**). **Embody** tach cycles; **Adopt** layers→depends_on+interfaces; **Defer** import-linter dual-gate; **Refuse** pytestarch/grimp (&lt;1k★) and foreign runtimes as deps.

---

## P17 — Cohesion-first concept splits (design pass after MOD-S1 tip audit)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P17.0 | **E-COH0 Spec:** approve **COH1–COH12** (pause thrash; concept bar; façade≠private warehouse; seam map before moves) | **Approved** (2026-08-09) | design memo `spec_gate: APPROVED E-COH0` |
| P17.1 | **E-COH1 Implement:** reshape provisional tip modules under COH bar | **Paused** (until E-HOT1 green) | COH2–COH4 on touch; claims green |
| P17.2 | **E-COH2:** align reshape with E-TACH1/2 layers + interfaces | After E-TACH0 Approve | `tach check`; public `expose` only |

Design: [`docs/design/concept-split-cohesion-design-2026-08-09.md`](../design/concept-split-cohesion-design-2026-08-09.md). Research: modularity/20. **Refuse** mechanical cut-and-paste that only clears LOC/statement gates.

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
| P21.0 | **E-CGQ0 Spec:** approve **CGQ1–CGQ10** (pre-generation controls; depth rows before Embody; Accept Concern→Remedy→Depth→Witness; structural probe; independent Verify; E-SOL0 vocabulary Amend) | **Draft** (2026-08-09) — **Active Spec draft** | research 24 + design → APPROVED |
| P21.1 | E-COH1 / E-STK1 Activate only with CGQ3 Accept rows | After Approve | Spec tables cite process/24 §2 |

Research: [`docs/research/process/24-codegen-quality-dimensions-mechanism-depth-2026.md`](process/24-codegen-quality-dimensions-mechanism-depth-2026.md). Design: [`docs/design/codegen-quality-dimensions-design-2026-08-09.md`](../design/codegen-quality-dimensions-design-2026-08-09.md).

---

## P14 — Docs research taxonomy + claude consolidation + look-first

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P14.0 | **E-DOC0 Spec:** approve **DOC1–DOC12** (domains ≤2 deep; migrate `claude/` valuables; Cursor hooks look-first; keep adapter) | **Approved** (2026-08-09, merge) | research 18 `spec_gate: APPROVED E-DOC0` |
| P14.1 | **E-DOC1 Implement:** domain map + hooks + migrate + claims rewrite | **Done** (2026-08-09) | claims green; design writes denied without research-map Read; marketplace intact |

Research: [`docs/research/process/18-docs-research-taxonomy-claude-consolidation-2026.md`](process/18-docs-research-taxonomy-claude-consolidation-2026.md).
