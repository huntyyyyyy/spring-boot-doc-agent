---
title: DS / analytics / ML-ops tooling — problem-first deep dive for doc-engine
status: RESEARCH COMPLETE — Spec gate OPEN E-DS0 (no code; Embody/Adopt/Refuse only)
epic: E-DS0
date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
prefer_sources: "arXiv primary + GitHub API star snapshot 2026-08-10 + DeepWiki cartography"
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
siblings:
  - docs/research/coverage-quality/01-coverage-oracle-climb-solid.md
  - docs/research/coverage-quality/03-scientific-dimensions-metrics.md
  - docs/research/coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md
related:
  - docs/research/quality-backlog.md
  - docs/design/coverage-measure-modes-design-2026-08-08.md
do_not:
  - install GE/Pandera/Evidently/DVC/MLflow/Feast as product deps without Spec
  - treat dashboard Cover% / climb Cover% as fail_under proof
  - weaken fail_under=98.7, complexipy ≤5, or size ≤225
  - adopt feature-store / A-B platforms as core CLI runtime
---

# 42 — Data science / ML-ops tooling (problem-first) → doc-engine

**Product frame:** Python CLI quality/doc product (`doc-engine`) with boolean
oracle `fail_under=98.7` on cohesive `coverage.xml` (CI **3.11 only**), climb
sensors under policy **16-A** (`coverage.climb.xml`), claim checkers, Stage-0
fixture plants. **Not** a serving ML platform, lakehouse, or experiment SaaS.

**Lens:** For each tool *class*, answer: (1) failure before the class,
(2) job/invariant restored, (3) what it does **not** solve, (4) **SoT vs sensor
vs adapter** for CI/quality.

**Claim tiers:** `[Evidenced]` primary paper/docs/API · `[Confirmed]` this repo ·
`[Unknown]` missing ID / product choice still open.

**Stance:** **Embody** = already true in gates · **Adopt** = take pattern next
(process/docs/gates) · **Refuse** = wrong shape for this product.

---

## 1. One-page verdict

| Question | Answer |
| --- | --- |
| Import a DS stack (GE / MLflow / Feast / Evidently) as core? | **Refuse** as product deps / merge SoT. |
| Steal problem patterns into quality gates? | **Yes — Embody** where already present; **Adopt** thin analogues. |
| Parallel of `coverage.xml` as oracle data product? | **Embody** (already); climb / gap / LLM-judge = **sensors**. |
| Metric theater risk here? | **Confirmed** — Cover% padding, climb-as-floor, pretty CI badges ≠ decision quality (sibling **09**). |
| Next Spec? | **E-DS0** — lock Embody/Adopt/Refuse only; no tool installs until a named ticket needs a witness. |

```text
PROBLEM (DS world)              DOC-ENGINE ANALOGUE                 ROLE
────────────────────────────    ─────────────────────────────────   ────────
Irreproducible notebook         Untagged climb / mock-certified     SoT hygiene
Silent schema/data drift        Fixture plant drift; claim path rot Predicate + plant
Train-test leakage              Eval fixture contamination          Isolation SoT
Metric theater                  Cover% / dashboards without bite    Sensor ≠ SoT
Train/serve feature skew        Dual parsers / dual scan backends   Shared definition
Experiment tracking chaos       Unbound claim ↔ commit/run          Provenance adapter
Expectations / contracts        check_repo_claims + ratchets        SoT predicates
A/B / causal tooling            Gate A/B of thresholds (rare)       Decision sensor
Quality metrics as data         coverage.xml / size_baseline.json   Oracle products
```

---

## 2. SoT vs sensor vs adapter (shared vocabulary)

| Role | Definition for this memo | doc-engine examples `[Confirmed]` |
| --- | --- | --- |
| **SoT (oracle)** | Boolean predicate + durable witness artifact; merge may fail on it | `fail_under=98.7` + `coverage.xml`; complexipy ≤5; size ≤225; `check_repo_claims.py` |
| **Sensor** | Continuous / advisory signal that *steers* work; must not silently rewrite SoT | Climb Cover%; gap-average; LLM-as-judge; domain meeting-rate (≠ floor) |
| **Adapter** | Glue that binds an external system or format without becoming the predicate | pytest-cov XML writer; CI 3.11 cell; PathCohesion wipe; optional MLflow/DVC *if ever* as provenance export |

**Category error to refuse:** promoting a sensor (dashboard PSI, climb %, judge score)
into SoT by renaming the file or reusing `fail_under` on a scoped measure
(`[Evidenced]` pytest-cov trap in synthesis).

---

## 3. Problem classes A–F (tool classes)

### A. Irreproducible analysis (same notebook, different answers)

| Slot | Content |
| --- | --- |
| **Failure before** | Out-of-order cells, hidden kernel state, missing data/deps, environment erosion → same `.ipynb` yields different numbers or fails silently. |
| **Job / invariant** | Top-to-bottom (or declared DAG) rerun from empty store reproduces recorded outputs within tolerance; environment + data pinned. |
| **Does not solve** | Scientific validity of the claim; causal identification; whether the metric is the right decision objective. |
| **SoT / sensor / adapter** | **SoT:** lockfile + data digest + clean-run witness. **Sensor:** “ran once on my laptop.” **Adapter:** container / DVC remote / notebook executor. |

**arXiv (≥3) `[Evidenced]`:**

| ID | Role |
| --- | --- |
| [2209.04308](https://arxiv.org/abs/2209.04308) / [2308.07333](https://arxiv.org/abs/2308.07333) | Biomedical Jupyter re-execution at scale — most notebooks fail or diverge |
| [2603.22726](https://arxiv.org/abs/2603.22726) | Nature-2024 scientific notebook quality — 2/19 reproducible in manual sample |
| [2602.07195](https://arxiv.org/abs/2602.07195) | MLE notebook modernization; ~35% score-reproducible on Kaggle corpus |
| [2605.01560](https://arxiv.org/abs/2605.01560) | FlowBook — enforce top-to-bottom reproducibility via read/write sets |

**GitHub exemplars:** DVC ~15.8k (`treeverse/dvc`) — data+pipeline pins
`[Evidenced]` API 2026-08-10. DeepWiki: [iterative/dvc](https://deepwiki.com/iterative/dvc)
(cartography of `Repo` / stages / cache).

**doc-engine map:** **Embody** pinned venv + hermetic fixtures + certification
verify refusing mock without `--allow-mock`. **Adopt** “clean-store rerun”
discipline for any generative stage that emits claim numbers. **Refuse**
notebook-as-CI-SoT.

---

### B. Silent schema / data drift breaking downstream metrics

| Slot | Content |
| --- | --- |
| **Failure before** | Column rename/type widen/null flood/partition empty → dashboards stay green while the measured construct changed (**evaluation blindness**). |
| **Job / invariant** | Contract: schema + semantics + freshness fail closed before consumers update “truth.” |
| **Does not solve** | Concept drift where \(P(Y\|X)\) moves with unchanged \(X\) schema (label-free blind spot). |
| **SoT / sensor / adapter** | **SoT:** expectation suite / Pandera schema that fails the job. **Sensor:** PSI / KS / Evidently reports. **Adapter:** GE checkpoint in orchestrator. |

**arXiv `[Evidenced]`:**

| ID | Role |
| --- | --- |
| [2608.02786](https://arxiv.org/abs/2608.02786) | Evaluation blindness — measurement looks healthy while system fails |
| [2404.18673](https://arxiv.org/abs/2404.18673) | Open-source drift tools in action (Evidently / NannyML use cases) |
| [2604.09163](https://arxiv.org/abs/2604.09163) | Evaluating DQ tools — GE / Evidently / Deequ measurement capabilities |
| [2507.21056](https://arxiv.org/abs/2507.21056) | AI-driven data-contract generation (contracts as first-class) |
| [2604.17836](https://arxiv.org/abs/2604.17836) | Label-free governance evidence degradation — proxy ≠ concept drift |

Classic systems debt (not arXiv): Sculley et al. *Hidden Technical Debt in ML
Systems* (NeurIPS 2015) — data dependencies / undeclared consumers
`[Evidenced]` PDF.

**GitHub:** Great Expectations ~11.7k · Pandera ~4.4k · Evidently ~7.8k.

**doc-engine map:** **Embody** fixture plants under
`scripts/fixtures/spring_signals/` + rule_coverage non-vacuity; claims
`path_exists` / `contains` / `behavior:` predicates. **Adopt** “schema of
claim artifacts” (certification.json fields) as contracts. **Refuse** PSI
dashboards as merge proof; **Refuse** LLM-written contracts as ungated SoT.

---

### C. Leakage / train–test contamination in evaluation

| Slot | Content |
| --- | --- |
| **Failure before** | Eval items appear in train (or near-duplicates) → inflated scores; wrong research conclusions. |
| **Job / invariant** | Disjointness (or declared overlap budget) between training material and evaluation witness; contamination metrics reported with scores. |
| **Does not solve** | Whether the benchmark construct is valid; distribution shift after clean splits. |
| **SoT / sensor / adapter** | **SoT:** held-out fixture corpus + hash denylist / split manifests. **Sensor:** n-gram / CDD peakedness detectors. **Adapter:** eval harness that loads only plant IDs. |

**arXiv `[Evidenced]`:**

| ID | Role |
| --- | --- |
| [2411.03923](https://arxiv.org/abs/2411.03923) | ConTAM — when contamination metrics predict undue advantage |
| [2402.15938](https://arxiv.org/abs/2402.15938) | CDD/TED — contamination via output distribution; mitigate eval inflation |
| [2410.19364](https://arxiv.org/abs/2410.19364) | Train–test leakage in Android malware ML — qualitative conclusion flips |
| [2505.24263](https://arxiv.org/abs/2505.24263) | Simulated leakage on MMLU/HellaSwag — accuracy drops after cleaning |
| [2207.07048](https://arxiv.org/abs/2207.07048) | Kapoor & Narayanan — leakage across 294 papers / 17 fields |

**doc-engine map:** **Embody** Stage-0 positive/negative fixtures separated from
metamorphic corpus; hermetic rule_coverage (no external corpus in CI).
**Adopt** explicit “eval plant must not be generator training seed” for any
LLM stage. **Refuse** live-web scrapes as Stage-0 SoT; **Refuse** treating
Recall@K sensors as contamination proof.

---

### D. Metric theater (pretty dashboards ≠ decision quality)

| Slot | Content |
| --- | --- |
| **Failure before** | Goodhart / Campbell: teams optimize Cover%, AUC, judge score, or audit dashboards while the construct (fault detection, harm, revenue decision) does not improve. |
| **Job / invariant** | Separate **proxy display** from **decision predicate**; require discriminative witnesses (mutation, metamorphic, human IRR) before shipping on the proxy. |
| **Does not solve** | Choosing the right product objective; organizational incentives that still reward theater. |
| **SoT / sensor / adapter** | **SoT:** boolean floors with bite. **Sensor:** dashboards / climb / LLM-judge. **Adapter:** report renderers (Great Tables, Evidently HTML). |

**arXiv `[Evidenced]`:**

| ID | Role |
| --- | --- |
| [2608.00794](https://arxiv.org/abs/2608.00794) | Compounding validity in agentic eval — \(V \le V_1 V_2 V_3\) |
| [2605.06324](https://arxiv.org/abs/2605.06324) | Gaming the metric, not the harm — audit manipulability |
| [2507.05619](https://arxiv.org/abs/2507.05619) | Evaluator stress tests for proxy gaming (RL + LLM) |
| [2603.28063](https://arxiv.org/abs/2603.28063) | Reward hacking as equilibrium (Goodhart vs Campbell regimes) |

**GitHub:** Great Tables ~2.7k — **presentation adapter**, not a quality SoT.

**doc-engine map:** **Embody** Cover% necessary-not-sufficient (sibling **09**);
mutation / metamorphic / gate mutators as discriminative sensors; refuse
LLM-judge as `fail_under`. **Adopt** IRR / stress-test vocabulary for any
agent eval. **Refuse** badge walls / coverage theater as merge SoT; **Refuse**
scoped Cover% labeled as 98.7.

---

### E. Feature / store inconsistency across training and serving

| Slot | Content |
| --- | --- |
| **Failure before** | Dual feature logic (Spark offline vs NumPy online) → training–serving skew; point-in-time leakage. |
| **Job / invariant** | One feature definition; offline historical join is point-in-time correct; online materialization matches; parity tests in CI. |
| **Does not solve** | Concept drift; label delay; whether features are causally meaningful. |
| **SoT / sensor / adapter** | **SoT:** shared FeatureView definitions + parity assertions. **Sensor:** offline/online distribution skew monitors (TFDV). **Adapter:** Feast `FeatureStore` / online store. |

**Evidence `[Evidenced]`:**

| Source | Role |
| --- | --- |
| Google Rules of ML #29/#32/#37 | Log serving features; reuse code; measure skew |
| [2010.02013](https://arxiv.org/abs/2010.02013) | TFX history — production ML platform for consistency |
| TFX/TFDV docs | Schema validation + train/serve skew detection |
| DeepWiki [feast-dev/feast](https://deepwiki.com/feast-dev/feast) | PIT joins, materialize, registry — cartography |

**GitHub:** Feast ~7.2k.

**doc-engine map:** **Embody** single scan path for Stage-0 (filesystem +
ast-grep) shared with CI; no dual “docs say X / scanner says Y” without
claims gate. **Adopt** parity tests when two backends compute the same
signal. **Refuse** Feast/online feature server as product dependency (no
serving ML).

---

### F. Experiment tracking chaos (which model produced which claim)

| Slot | Content |
| --- | --- |
| **Failure before** | Metrics/models float free of code/data commits → cannot answer “which run produced this claim?” |
| **Job / invariant** | Lineage: code SHA ⊕ data digest ⊕ params ⊕ metrics ⊕ artifact → queryable run id. |
| **Does not solve** | Correctness of the metric; contamination; decision quality; full W3C PROV depth (MLflow alone is coarse). |
| **SoT / sensor / adapter** | **SoT:** git commit + certification.json fields that Verify reads. **Sensor:** MLflow UI charts. **Adapter:** MLflow tracking / DVC experiments / PROV exporters. |

**arXiv / pubs `[Evidenced]`:**

| ID | Role |
| --- | --- |
| [2507.01078](https://arxiv.org/abs/2507.01078) | yProv4ML — PROV-JSON lineage with MLflow-like API |
| MLflow2PROV (DEEM@SIGMOD 2023) | Extract W3C PROV from Git + MLflow; EMS provenance gaps |
| DeepWiki [mlflow/mlflow](https://deepwiki.com/mlflow/mlflow) | Tracking / Registry / Evaluation — cartography |

**GitHub:** MLflow ~27.4k · DVC ~15.8k.

**doc-engine map:** **Embody** certification artifacts + git history as claim
anchors; session-log / steering `status:` with verify predicates.
**Adopt** optional run-id fields on generative outputs. **Refuse** MLflow
server as merge gate; **Refuse** replacing `coverage.xml` with experiment UI.

---

## 4. Named tools → problem each solves (class G)

Star counts via GitHub API **2026-08-10** `[Evidenced]`.

| Tool | ~★ | Primary problem solved | Role class | CI/quality role | doc-engine stance |
| --- | --- | --- | --- | --- | --- |
| **Great Expectations** | 11.7k | Silent contract break on batches (schema/nulls/freshness) | B | SoT *if* wired fail-closed; else sensor reports | **Refuse** dep · **Adopt** contract *pattern* |
| **Pandera** | 4.4k | DataFrame schema drift at Python boundary | B | Unit-test SoT for DF APIs | **Refuse** unless DF-heavy module · **Adopt** schema-as-types idea for JSON certs |
| **Evidently** | 7.8k | Detect distribution/quality drift; ML/LLM eval reports | B, D | **Sensor** (PSI/reports); gate only if thresholded | **Refuse** as SoT · **Adopt** “report ≠ proof” culture |
| **DVC** | 15.8k | Irreproducible data/pipeline versions; experiment compare | A, F | Adapter for data pins; SoT when lock is verified | **Refuse** core · **Adopt** digest-pin analogy for fixtures |
| **MLflow** | 27.4k | Lost run provenance; model registry chaos | F | Adapter/sensor; not boolean merge SoT | **Refuse** core · **Adopt** run↔claim binding pattern |
| **Feast** | 7.2k | Train/serve feature inconsistency | E | SoT for feature defs in ML platforms | **Refuse** (no serving features) |
| **Great Tables** | 2.7k | Ugly/inconsistent tabular *presentation* | D (surface) | **Adapter** for humans | **Refuse** as quality gate · optional docs polish only |

**Cross-tool truth:** none of these restore *decision* quality alone; stacking
them without predicates recreates metric theater (class D).

---

## 5. Statistical testing / A/B / causal tooling (class H)

| Slot | Content |
| --- | --- |
| **Decision problem** | “Did intervention \(T\) *cause* outcome \(Y\) for population \(P\)?” — not “is AUC higher on this split?” Prediction accuracy ≠ decision quality when allocation/OR follows. |
| **Failure before** | Confounding, peeking, underpowered tests, optimizing predictive loss while harming expected outcome under a budget. |
| **Job / invariant** | Identified estimand + design (RCT / quasi) + uncertainty + **refutation**; for HTE, out-of-sample causal scoring. |
| **Does not solve** | Engineering SoT for code coverage; schema contracts; train/serve skew. |
| **SoT / sensor / adapter** | **SoT:** pre-registered primary metric + sample size / sequential boundary. **Sensor:** secondary dashboards, uplift models. **Adapter:** DoWhy / EconML / experiment platform APIs. |

**arXiv `[Evidenced]`:**

| ID | Role |
| --- | --- |
| [2011.04216](https://arxiv.org/abs/2011.04216) | DoWhy — model → identify → estimate → **refute** |
| [2501.07722](https://arxiv.org/abs/2501.07722) | ML-assisted randomization tests for complex A/B effects |
| [2510.19517](https://arxiv.org/abs/2510.19517) | Bi-DFCL — prediction–decision misalignment; OBS vs RCT bias–variance |

**GitHub:** DoWhy ~8.3k (`py-why/dowhy`).

**doc-engine map:** **Refuse** A/B platforms / causal libraries as product core.
**Adopt** *refutation* mindset for gate changes (change threshold only with
predeclared witness + rollback). **Embody** “don’t soften 98.7 because a
sensor looked green.”

---

## 6. Coverage / quality metrics as data products (class I)

Parallel to DS “metrics tables” — treat quality artifacts as **versioned
products** with producers, contracts, and consumers.

| Artifact | Role | Producer | Consumer | Drift failure if… |
| --- | --- | --- | --- | --- |
| `coverage.xml` | **Oracle SoT** | pytest-cov whole-repo 3.11 | `fail_under`, gap tools (read-only) | climb writes same path (policy **16-A** forbids) |
| `coverage.climb.xml` | **Sensor product** | climb mode | agents / humans | promoted to floor claim |
| `size_baseline.json` / complexipy offenders | **Oracle / ratchet SoT** | size-ratchet / complexipy | CI | baseline rewrite without Spec |
| Rule/fixture plants | **Plant SoT** | `scripts/fixtures/…` | rule_coverage | plant missing → vacuous green |
| Claims / CONSTRAINTS | **Claim SoT** | humans + checker | CI | status lies while paths resolve |

**arXiv on oracle quality (SE, not DS) `[Evidenced]`:**

| ID | Role |
| --- | --- |
| [2212.06118](https://arxiv.org/abs/2212.06118) | Survey — structural Cover% ignores oracle quality (checked coverage) |
| [2510.03071](https://arxiv.org/abs/2510.03071) | State field coverage — oracle quality ↔ mutation score |
| Sibling **09** + CoverUp [2403.16218](https://arxiv.org/abs/2403.16218) | Adequacy vs inflation; climb ≠ floor |

**doc-engine map:** **Embody** dual-mode productization (oracle vs climb paths).
**Adopt** document each quality XML/JSON as a data product (schema, owner,
fail-closed consumer). **Refuse** combining climb into oracle; **Refuse**
dashboard-only Cover% without `fail_under` witness.

---

## 7. Master Embody / Adopt / Refuse (doc-engine)

### Embody (already / keep hard)

| Pattern | Why |
| --- | --- |
| Boolean oracle floor 98.7 + cohesive `coverage.xml` | Class I SoT — DS “metrics warehouse” but with bite |
| Climb / gap / LLM-judge as **sensors** only (16-A) | Class D anti-theater |
| Hermetic fixture plants + rule non-vacuity | Class B/C — contracts + no contamination from external corpus |
| `check_repo_claims.py` predicates | Class B/F — claim schema drift fails closed |
| Shared Stage-0 scan path in CI | Class E — one definition |
| Certification verify refuses mock without flag | Class A — reproducibility of “certified” |

### Adopt (thin analogues — no platform install by default)

| Pattern | Ticket shape |
| --- | --- |
| Explicit **data-product cards** for quality artifacts (schema, path, SoT vs sensor) | Docs / CONTRIBUTING only |
| Digests / lock semantics for fixture corpora (DVC-shaped, not DVC) | Optional spike |
| Run-id / commit binding on generative claim packets (MLflow-shaped) | Generative stages |
| Refutation checklist when changing gate thresholds (DoWhy-shaped) | Process |
| Parity tests when two implementations emit one signal | Backend splits |

### Refuse

| Item | Why |
| --- | --- |
| GE / Pandera / Evidently / DVC / MLflow / Feast as **required** product deps | Wrong category — Python CLI doc/quality, not ML platform |
| Feature store / online serving | No train/serve ML product |
| A/B or causal stack as CI core | Decision tooling ≠ code oracle |
| Dashboard / PSI / climb Cover% as 98.7 proof | Metric theater |
| LLM-generated contracts without human Spec | Evaluation blindness risk |
| Great Tables / Evidently HTML as gate witnesses | Presentation adapters |

---

## 8. Unknowns

| ID | Question | Exit |
| --- | --- | --- |
| U1 | Ever pin large binary fixtures with content-addressable store (DVC-lite)? | Spike only if fixture size becomes a real CI pain |
| U2 | Bind generative stage outputs to a lightweight run ledger (file-based, not MLflow server)? | Spec if Stage-1–4 claims need audit |
| U3 | Pandera (or pydantic) schemas for `certification.json` / claim packets? | Size/complexipy preflight first |
| U4 | Publish DeepWiki Evaluate for GE/Pandera (cartography only)? | Optional; not blocking E-DS0 |
| U5 | Any customer-facing “analytics” surface that would justify Evidently-like reports? | Product choice — default **no** |

---

## 9. Epic stub — E-DS0 (research lock only)

| Field | Content |
| --- | --- |
| **Epic goal** | Lock problem-first DS/ML-ops Embody/Adopt/Refuse for doc-engine; no platform deps. |
| **DS0-1** | Human Approve of §7 table (or explicit subset) — Acceptance: note in this file `spec_gate: APPROVED E-DS0` |
| **DS0-2** | CONTRIBUTING one-pager: quality artifacts as data products (oracle vs climb) — Acceptance: claims path resolves |
| **DS0-3** | Optional spikes U1–U3 only after DS0-1 — Acceptance: spike memo with refuse-by-default |
| **Exit** | Spec approved; backlog row; **no** GE/MLflow/Feast installs on tip |
| **Invariants** | fail_under 98.7 · complexipy ≤5 · LOC ≤225 · 16-A · no utils bag |

---

## 10. Source verification snapshot

| Label | Result | Tier |
| --- | --- | --- |
| Notebook repro arXiv set | 2209.04308 / 2308.07333 / 2603.22726 / 2602.07195 / 2605.01560 exist | `[Evidenced]` |
| Drift / blindness | 2608.02786 / 2404.18673 / 2604.09163 exist | `[Evidenced]` |
| Contamination | 2411.03923 / 2402.15938 / 2410.19364 / 2505.24263 / 2207.07048 exist | `[Evidenced]` |
| Metric theater | 2608.00794 / 2605.06324 / 2507.05619 exist | `[Evidenced]` |
| TFX / skew | 2010.02013 + Google Rules of ML | `[Evidenced]` |
| Provenance | 2507.01078 + MLflow2PROV pub | `[Evidenced]` |
| Causal | 2011.04216 / 2501.07722 / 2510.19517 exist | `[Evidenced]` |
| Oracle adequacy | 2212.06118 / 2510.03071 exist | `[Evidenced]` |
| DeepWiki MLflow / Feast / DVC | Indexed overviews fetched 2026-08-10 | `[Evidenced]` cartography |
| Star counts | GitHub API 2026-08-10 (table §4) | `[Evidenced]` snapshot |
| Local dual-mode / claims / fixtures | CONTRIBUTING + synthesis + scripts | `[Confirmed]` |
