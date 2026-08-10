---
title: DS / analytics / ML-ops tooling — problem-first map for doc-engine
status: RESEARCH COMPLETE — Spec gate OPEN E-DS0 (no code; Embody/Adopt/Refuse only)
epic: E-DS0
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
prefer_sources: arXiv primary + GitHub API star snapshot 2026-08-10 + DeepWiki cartography
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
siblings:
- docs/research/process/42-problem-first-rag-ds-cli-2026-08-10.md
- docs/research/coverage-quality/01-coverage-oracle-climb-solid.md
- docs/research/coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md
related:
- docs/research/quality-backlog.md
do_not:
- install GE/Pandera/Evidently/DVC/MLflow/Feast as product deps without Spec
- treat dashboard Cover% / climb Cover% as fail_under proof
- weaken fail_under=98.7, complexipy ≤5, or size ≤225
- adopt feature-store / A-B platforms as core CLI runtime
last_reviewed: '2026-08-10'
---

# Data science / ML-ops tooling (problem-first) → doc-engine

**Product frame:** Python CLI quality/doc product with boolean oracle
`fail_under=98.7` on cohesive `coverage.xml` (CI **3.11 only**), climb sensors
under policy **16-A**, claim checkers, Stage-0 fixture plants. **Not** a
serving ML platform.

**Lens:** (1) failure before the class, (2) job restored, (3) what it does
**not** solve, (4) **SoT vs sensor vs adapter**.

---

## 1. Verdict

| Question | Answer |
| --- | --- |
| Import GE / MLflow / Feast / Evidently as core? | **Refuse** as product deps / merge SoT |
| Steal problem patterns into quality gates? | **Yes** — Embody present; Adopt thin analogues |
| Parallel of `coverage.xml` as oracle data product? | **Embody** (already); climb/gap/judge = sensors |
| Metric theater risk? | **Confirmed** — Cover% padding / climb-as-floor (sibling **09**) |
| Next Spec? | **E-DS0** — lock Embody/Adopt/Refuse; no installs until named ticket |

```text
PROBLEM (DS world)              DOC-ENGINE ANALOGUE                 ROLE
Irreproducible notebook         Untagged climb / mock-certified     SoT hygiene
Silent schema/data drift        Fixture plant drift; claim path rot Predicate + plant
Train-test leakage              Eval fixture contamination          Isolation SoT
Metric theater                  Cover% / dashboards without bite    Sensor ≠ SoT
Train/serve feature skew        Dual parsers / dual scan backends   Shared definition
Experiment tracking chaos       Unbound claim ↔ commit/run          Provenance adapter
Expectations / contracts        check_repo_claims + ratchets        SoT predicates
Quality metrics as data         coverage.xml / size_baseline.json   Oracle products
```

---

## 2. SoT vs sensor vs adapter

| Role | Definition | Examples `[Confirmed]` |
| --- | --- | --- |
| **SoT** | Boolean predicate + durable witness | fail_under 98.7 + coverage.xml; complexipy; size; claims |
| **Sensor** | Advisory signal; must not rewrite SoT | Climb Cover%; gap-average; LLM-judge |
| **Adapter** | Glue without becoming the predicate | pytest-cov XML writer; optional future MLflow export |

**Category error:** promoting sensor into SoT by renaming files or reusing
`fail_under` on scoped measure (pytest-cov trap).

---

## 3. Problem classes → tools

| ID | Failure before | Job restored | Does NOT solve | Layer | Logos / papers |
| --- | --- | --- | --- | --- | --- |
| **D1** Silent schema/null drift | Pipelines succeed while types/nulls flip | Contracts fail-closed at boundaries | Concept drift of labels | SoT-shaped when boolean | GX ~12k★ (expectations + Data Docs); Pandera ~4.3k★ (schema-as-code) |
| **D2** Irreproducible artifacts | Same notebook, different answers | Dataset + pipeline lineage | Leakage inside a versioned bad split | Identity SoT for inputs | DVC ~16k★; data-centric ML `[2506.16051]` |
| **D3** Experiment identity chaos | Which params produced a claim? | Run/experiment tracking | Correctness of metric choice | Adapter + run identity | MLflow ~27k★ `[DeepWiki]` |
| **D4** Distribution / concept drift | Train green → silent prod degrade | Detect shift before/as performance dies | Auto-fixing labels | Sensor | Evidently ~7.8k★; Uber adv. validation `[2004.03045]`; D3Bench `[2404.18673]` |
| **D5** Train/serve skew | Features differ online vs offline | Feature-store consistency | Upstream quality | Adapter + contract | Feast ~7.2k★ |
| **D6** Leakage / contamination | Test info in train → metric theater | Separation + detection + info sheets | “More logging” alone | Process SoT + sensors | `[2207.07048]` (17 fields / 294 papers); `[2311.04179]` |
| **D7** Stakeholder-invisible quality | Only engineers see pytest | Human-readable validation docs | Machine merge without boolean gate | Dual sink | GX Data Docs |

Kapoor & Narayanan: leakage causes reproducibility crisis; model info sheets as
mitigation `[Evidenced — 2207.07048]`. Parallel local story: **pretty metrics
that are the wrong predicate**.

---

## 4. Mapping onto doc-engine

| DS pattern | Local analogue | Stance |
| --- | --- | --- |
| Expectation suite / fail closed | fail_under + check_repo_claims | **Embody** |
| Schema-as-code (Pandera) | Fixture schemas; typed packets | **Adopt** |
| Drift dashboard (Evidently) | Climb / gap / RAGAS-like judges | **Sensor only** |
| Experiment tracking (MLflow) | Certification / run manifests as **derived** | **Adopt** identity; **Refuse** LWW |
| DVC lineage | Fixture corpus + baseline digests | **Embody** plant≠campaign |
| Feature store | N/A tip | **Defer** |
| Leakage info sheets | Claim tiers Evidenced/Confirmed/Unknown | **Embody** |

---

## 5. Refuse

1. Dashboard green = decision quality
2. Climb / scoped Cover% = whole-repo 98.7
3. More logging ⇒ no leakage
4. GE Cloud / SaaS as required IDP

**Epic:** `E-DS0` — Spec Embody/Adopt/Refuse only. Umbrella:
[`process/42-…`](../process/42-problem-first-rag-ds-cli-2026-08-10.md).
