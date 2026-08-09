---
title: Test adequacy vs coverage inflation — 2026 math, criteria, and this repo
status: RESEARCH COMPLETE — Spec gate APPROVED E-QA0 (2026-08-09)
spec_gate: APPROVED E-QA0
date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
prefer_sources: "2026 primary (arXiv / GitHub / DeepWiki); older only as contrast"
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
design: docs/design/test-adequacy-markers-design-2026-08-09.md
siblings:
  - docs/research/coverage-quality/01-coverage-oracle-climb-solid.md
  - docs/research/coverage-quality/03-scientific-dimensions-metrics.md
  - docs/research/coverage-quality/08-rust-test-runners-bottlenecks.md
related:
  - docs/research/quality-backlog.md
  - docs/design/coverage-measure-modes-design-2026-08-08.md
  - docs/design/test-suite-parallel-domains-design-2026-08-08.md
do_not:
  - scrap fail_under=98.7 or replace Cover% with LLM-judge
  - fold three mutation taxonomies into one PIT/mutmut zoo
  - treat domain_* meeting-rate as Cover% proof (or the reverse)
  - promote climb Cover% / gap-average as merge SoT
---

# 09 — Test adequacy vs coverage inflation (2026)

**Question:** What modern mathematics / logic / algorithms should shape a
“quality marker” for this product — so we can **pinpoint high-quality SE
domains** and refuse **lousy tests** that only inflate Cover% without
discriminative analysis?

**Product frame:** Python CLI (`doc-engine`) with boolean oracle
`fail_under=98.7`, climb sensors (16-A), E-TEST domain markers, incident
mutators, metamorphic Arm-1, and non-blocking mutation drivers. Not a K8s
mesh farm.

**Claim tiers:** `[Evidenced]` primary · `[Confirmed]` this repo · `[Unknown]`
needs Spec or measure.

---

## 1. One-page verdict

| Question | Answer |
| --- | --- |
| Scrap Cover% floor / E-TEST / dual-mode? | **No.** Necessary partition + execution SoT remain. |
| Is Cover% alone a quality marker? | **No.** Necessary, not sufficient. `[Evidenced]` 2026 + classical |
| Is “climb to clear gap-average” at risk of lousy padding? | **Yes — Confirmed** incentive on this tip (`ENFORCE=False` mutation). |
| Replace framework with one 2026 product (MIST-RL, Prompt Coverage, …)? | **Refuse** as SoT swap; **Adopt** algorithms as *sensors / Verify steps*. |
| Next Spec? | **E-QA0 approved** — ship **E-QA1/E-QA2**; refuse Cover% padding without witness. |

```text
NECESSARY (execution footprint)     SUFFICIENT (discriminative power)
───────────────────────────────     ────────────────────────────────
Cover% / branch (oracle 98.7)       Mutation kill (surviving mutants)
diff-cover on new code              Metamorphic relations (oracle problem)
E-TEST domain meeting-rate          Property / generative oracles (Hypothesis)
Rule non-vacuity (scanner)          Incident-seeded gate mutators (already here)
```

---

## 2. Mathematics & algorithms (2026 + foundations)

### 2.1 Adequacy as set functions

| Object | Formal shape | Consequence | Tier |
| --- | --- | --- | --- |
| Structural coverage | Monotone set function over executed elements | Greedy climb fills holes; **diminishing returns** do not imply fault detection | Classical + `[Confirmed]` climb process |
| Mutation score | Fraction of non-equivalent mutants *killed* | Closer to discriminative power than line Cover% | Classical (Just et al.; Inozemtseva & Holmes ICSE 2014 contrast) |
| Mutation-score maximization for suite size \(K\) | **Monotone submodular** → Max-Coverage-shaped; **NP-hard** | Greedy marginal-gain ≈ \((1-1/e)\) of OPT (Nemhauser) | `[Evidenced]` MIST-RL **2603.01409**; TestDecision **2604.01799** |
| Test bloat | Redundant tests with near-zero marginal mutant kill | High Cover% + low aggressiveness | `[Evidenced]` 2603.01409 citing Yoo & Harman 2012 |

**Logic for this repo:** gap-average ranks *uncovered lines* (structural). It does
**not** optimize submodular mutation utility. Agents optimizing only gap-average
approximate a different objective than “kill hard mutants.”

### 2.2 Context dependence (2026 replication)

**arXiv:2607.22880** (coverage & mutation vs effectiveness for LLM-generated
tests): usefulness is **context-dependent**.

| Setting | Cover% / mutation as signal | Maps to this product |
| --- | --- | --- |
| Regression / code assumed mostly correct | Can be informative across models | Merge oracle + diff-cover — **keep** |
| Code may be buggy; tests must expose existing bugs | Cover% **unreliable**; standard mutation often **not applicable** as sole judge | Live generative stages / agent patches — need stronger oracles |

`[Evidenced]`

### 2.3 Adjacent 2026 adequacy criteria (Adopt as sensors, not SoT)

| Criterion | Idea | Product fit |
| --- | --- | --- |
| **Prompt Coverage** (2607.02057) | Adequacy over NL requirements / prompts, not only AST lines | Relevant to generative Stage 1–4; **not** Stage-0 / gate Cover% SoT |
| **Metamorphic adequacy** (2412.20692; MR-Coupler 2604.10126) | Cover metamorphic relations + source inputs | We already run Arm-1 metamorphic on `rule_fixtures` — **Embody & extend** |
| **SWE-Mutation** (2605.22175) | Hard mutants fool weak LLM suites | Explains why climb padding without kill pressure is dangerous |
| **MIST-RL / TestDecision** | RL / greedy on marginal mutation utility | Algorithm inspiration for *which* climb tests to write — **not** CI runtime |

---

## 3. Industry / GitHub / DeepWiki heuristics

| Artifact | Signal | Tier |
| --- | --- | --- |
| **mutmut** (boxed/mutmut, ~1.4k★; PyPI **3.7.0** Jul 2026) | Active Python mutation tool; kill-rate gates appear in serious CI notes | `[Evidenced]` |
| **Hypothesis** (~8.8k★) | Property-based oracles; finds bugs Cover% misses | `[Evidenced]` |
| **pytest-cov / coverage.py** (DeepWiki cartography) | Measures *execution*, not assertion strength; `fail_under` is structural | `[Evidenced]` DeepWiki pytest-dev/pytest-cov |
| DeepWiki projects pairing **coverage 100% + mutmut** | Explicit: coverage ≠ logical verification | `[Evidenced]` cartography (e.g. denial / pristan guides) |

**Heuristic used:** high stars **and** 2025–2026 releases/changelogs (mutmut 3.x
through 2026; Hypothesis sustained). Stars alone are insufficient; recent
mutation CI writeups (kill-rate baselines, equivalent-mutant buffers) match our
“measurement-first then ratchet” pattern already used for size/complexipy.

---

## 4. This repo — Confirmed inventory

### 4.1 Already Embodied (do not scrap)

| Mechanism | Role | Merge bite? |
| --- | --- | --- |
| Oracle Cover% 98.7 + 16-A climb split | Execution SoT / sensor split | **Hard** |
| E-TEST `domain_*` + 98.7 *meeting-rate* | Suite BC partition / ABI shards | **Hard** (markers); meeting-rate ratchet |
| Incident gate mutators (`scripts/ratchets/mutate.py`) | Near-miss defects on gates | **Report-only** (`ENFORCE=False`) |
| Assertion mutants (`tests/spring_signals/mutation_driver.py`) | Assertion strength on harness | **Report-only** |
| Metamorphic Arm-1 / churn | Scanner stability under formatting | **Hard** in suite |
| Rule / semgrep non-vacuity | Scanner adequacy ≠ Python Cover% | **Hard** |

### 4.2 Confirmed anti-pattern risk (“lousy tests”)

Climb/gap-average **correctly labeled sensors** still create process pressure:

1. Rank worst files by uncovered units.
2. Add `test_coverage_climb_*` until Cover% moves.
3. Mutation / assertion drivers stay non-blocking.

→ Agents can ship **execution-only** tests (call path, weak asserts) that clear
the floor without raising discriminative power. That is exactly the “high
coverage, low aggressiveness” failure mode in **2603.01409**. `[Confirmed]`

**Do not confuse:** E-TEST `domain_climb_sensor` marks *where* climb tests live;
it does not certify they are non-lousy.

---

## 5. SOLID / DDD / patterns (keep framework, refactor seams)

| Principle | Binding here |
| --- | --- |
| **SRP / DDD** | Separate BCs: `coverage_*` (execution), `mutation_*` / ratchets (discrimination), `test_domain_*` (partition), metamorphic (relations) — already mostly split |
| **OCP** | New adequacy criterion = new **strategy/port** module under `doc_engine.ci` or `scripts/ratchets`; refuse if/elif god in the oracle cell |
| **DIP** | Oracle cell depends on `AdequacyReport` ports, not on mutmut CLI shape |
| **DRY** | One durations parser pattern (E-RUN1); one mutator registry (already); do not duplicate kill accounting in workflow YAML |
| **Creational** | Strategy factory `strategy_for(MeasureMode)` already; mirror for `AdequacyMode` |
| **Behavioral** | Template Method for “apply mutant → run named suite → score”; Strategy for criterion |
| **Structural** | Facade scripts/ci only; no utils bag |

**Refuse scrap:** replacing this stack with Spec Kit WorkflowEngine, PIT operator
zoo, or “mutation score replaces Cover%” as sole merge SoT (synthesis **29**,
ESE witness-in-progress).

---

## 6. Embody / Adopt / Refuse

| Stance | Item |
| --- | --- |
| **Embody** | Cover% oracle 98.7; 16-A; E-TEST domains; metamorphic Arm-1; incident mutator taxonomy; complexipy/size |
| **Adopt (v1 Spec)** | Adequacy **ports**: structural + mutation-kill + metamorphic-vacuity as distinct sensors; **anti-padding Verify** on packages touched by climb (named suite must kill incident mutants / scoped mutmut) |
| **Adopt (v1.5)** | Graduate gate `ENFORCE` after zero-survivor baseline defended; optional Hypothesis on pure functions (paths, fingerprints, plateau buckets) |
| **Adopt (algorithm only)** | Greedy marginal mutant-kill when choosing next climb target (submodular framing) — human/agent card, not RL CI |
| **Defer** | Prompt-coverage as Stage-1–4 sensor; full mutmut merge gate suite-wide; SWE-Mutation agentic mutant farm |
| **Refuse** | Scrap Cover% or domain markers; LLM-judge as fail_under; climb XML as floor; single PIT-like mega-mutator; MIST-RL as CI runtime |

---

## 7. Policies for Spec gate **E-QA0** — **APPROVED** (2026-08-09)

| ID | Policy |
| --- | --- |
| **Q1** | Cover% remains **necessary** merge SoT; never sufficient alone |
| **Q2** | Climb/gap-average remain **sensors**; any climb batch that raises Cover% on a package must attach an **adequacy witness** (mutation or metamorphic) before Archive |
| **Q3** | Three mutation taxonomies stay distinct (gates / assertions / optional mutmut) |
| **Q4** | Domain markers stay **partition** SoT — not adequacy proof |
| **Q5** | No adequacy criterion may weaken `fail_under`, LOC, or complexipy ceilings |
| **Q6** | New criteria land as OCP strategies under concept packages — no `utils/adequacy.py` |
| **Q7** | LLM-generated climb tests are held to the same witnesses as human tests |
| **Q8** | Measurement-first: mutation kill-rate baselines before hard `ENFORCE=True` |

**Spec record:** Q1–Q8 approved; design stub
[`test-adequacy-markers-design-2026-08-09.md`](../design/test-adequacy-markers-design-2026-08-09.md).
Implement **E-QA1** (adequacy sensor ports + CI summary) then **E-QA2**
(anti-padding Verify). Do not scrap Cover%/E-TEST; do not fold mutator taxonomies.

---

## 8. Epic sketch **E-QA** — Adequacy without Cover% theater

| Field | Content |
| --- | --- |
| **Epic** | Suite adequacy markers that refuse lousy coverage padding |
| **E-QA0** | Spec approve **Q1–Q8** |
| **E-QA1** | `AdequacyCriterion` ports + CI summary section (sensor): structural + gate-mutator survivors + metamorphic vacuity |
| **E-QA2** | Anti-padding Verify: climb packages require scoped kill witness (incident mutants and/or mutmut slice) |
| **E-QA3** | Spike: Hypothesis on pure `doc_engine.ci.suite_timing` / fingerprint helpers |
| **Exit** | Spec recorded; climb process docs require witness; oracle 98.7 unchanged |
| **Invariants** | 98.7 · 16-A · ≤5 · ≤225 · T-A · no LLM-judge floor |

---

## 9. Adversarial checklist

- [ ] Collapsed adequacy into “add more climb tests”?
- [ ] Proposed scrap of Cover% or E-TEST because mutation exists?
- [ ] Treated mutmut kill-rate as silent merge green without Spec?
- [ ] Foldeed gate + assertion + Python mutators into one zoo?
- [ ] Used Prompt Coverage / MIST-RL as Stage-0 Cover% replacement?
- [ ] Ignored already-shipped metamorphic + incident mutators?
- [ ] Claimed domain meeting-rate proves test quality?

---

## 10. Relation to active tip (#105 / E-RUN)

Finishing **98.7 green** remains a **necessary** oracle Verify. This memo does
**not** authorize pausing the floor. It **does** authorize refusing further
climb batches that only execute lines without an adequacy witness once **E-QA0**
is approved — and it reframes “next after sensors” as **E-QA** alongside optional
E-RUN2/D15, not endless Cover% padding.
