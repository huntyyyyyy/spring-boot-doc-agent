---
title: D4/D5/D6 cold BC research — static join · drift/capacity · operator CLI
status: DRAFT research — Spec seeds for E-CQLJ0 / E-TOOL4 slice / E-OAS16; no Implement
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine + Stage-0 CodeQL/ast-grep + spring-signals dual plant
related:
  - docs/research/cold-product-bc-research-map-2026-08-10.md
  - docs/research/ci/36-ocs-dual-plant-profile-2026.md
  - docs/research/ci/17-codeql-signals-skip-fingerprint-2026.md
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
  - docs/research/coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md
  - src/doc_engine/scanning/_scanner_codeql.py
  - src/doc_engine/tools/spring_drift_check.py
  - src/doc_engine/tools/capacity_preflight.py
do_not:
  - make Artifactory OCS CodeQL DB the merge SoR
  - dual-write a second assertion engine
  - treat capacity / Stage-4 proxy / Cover% climb as fail_under 98.7 proof
  - rich / OTel as CI SoT; unattended AI merge
  - implement before Spec Approve
spec_gate: DRAFT — CQLJ / TOOL4 / OAS16 tickets pending Approve
stars_as_of: 2026-08-10 (GitHub API)
deepwiki: Evidenced via WebFetch deepwiki.com (cross-domain synthesis in cold-bc-domain-subdomain-taxonomy-2026-08-10.md)
---

# Principal memo: D4 Static analysis join · D5 Drift & capacity · D6 Operator CLI

**Question.** For cold product BCs (CodeQL/OpenAPI join, drift+capacity, operator CLI),
what external SoR (arXiv + GitHub) should doc-engine Embody / Adopt / Refuse —
holding **fixture = CI merge SoR**, **OCS = campaign**, **same assertion engine**,
and **capacity ≠ Cover% proof**?

**Method.** WebSearch/WebFetch of arXiv + GitHub primaries; claim tiers; map to
this Python CLI. DeepWiki cartography: **Evidenced** (see taxonomy memo §4).

---

## 0. One-page verdict

| Domain | Embody | Adopt | Refuse |
| --- | --- | --- | --- |
| **D4** Static join | Dual plant (fixture CI SoR / OCS campaign); same `check-assertions` engine; hermetic CodeQL pack + ast-grep Stage-0 | Explicit join contracts (QL CSV/SARIF ↔ OpenAPI ↔ facts); pack ports (OCP); SARIF as *export* shape not merge SoR | Artifactory DB as CI SoT; second assertion engine; LLM-synthesized QL as merge SoR; soft-green Messaging/OpenAPI |
| **D5** Drift & capacity | Characterization plants before threshold rewrite; proxy labels on Stage-4 / capacity | Spec↔code drift sensors (oasdiff-class); wall-clock/scale estimators as **preflight sensors** | Capacity / climb Cover% / LLM-judge as 98.7 proof; Goodharted single proxy as gate |
| **D6** Operator CLI (brief) | Dual sink (headline + JSON receipt); fail-closed actionable errors | Typer thin façade (≥10k★); finite GHA OS×shell **campaign** matrix | rich as CI SoT; universal OS/terminal emulator as merge proof; boiling all `scripts/ci` into one megacli |

**Locked product rules (all three):** fail_under **98.7** · complexipy **≤5** · LOC **≤225** · no `utils/` · policy **16-A** · Spec → Implement → Verify → Archive · human review floor.

---

## D4 — Static analysis join (CodeQL / OpenAPI / multi-backend)

**Confirmed seams:** `_scanner_codeql.py` + `support/_codeql_*`; dual packs
(CI `spring-signals/codeql` vs Stage-0 `codeql/spring-signals`); E-OCS0 plant
profile; OpenAPI QL / P33.5 join evidence; fingerprint skip (E-CQL0).

### D4.1 Multi-backend scanners / query packs

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2504.16057](https://arxiv.org/abs/2504.16057) | Neuro-symbolic Static Analysis with LLM-generated Vulnerability Patterns | LLM-generated vuln patterns + symbolic backends — pattern for pack ports / overlays, not merge SoR `[Evidenced]` title verified 2026-08-10 |
| [2511.08462](https://arxiv.org/abs/2511.08462) | QLCoder: A Query Synthesizer For Static Analysis of Security Vulnerabilities | Agentic CodeQL query synthesis from CVE metadata; F1≪hand packs on general suites → **Refuse** LLM-QL as CI SoR; **Adopt** as campaign research sensor |
| [2405.17238](https://arxiv.org/abs/2405.17238) | IRIS: LLM-Assisted Static Analysis for Detecting Security Vulnerabilities | LLM taint specs + CodeQL dataflow; shows backend stays symbolic while LLM fills *spec gaps* — aligns with “engine fixed, overlays optional” |
| [2601.10865](https://arxiv.org/abs/2601.10865) | Multi-Agent Taint Specification Extraction for Vulnerability Detection (SemTaint) | External CSV predicates into CodeQL without recompilation — **Adopt** shape for join inputs (facts/OpenAPI rows as external relations) |

#### GitHub repos

| Repo | ★ (2026-08-10) | Recency / notes | Fit |
| --- | --- | --- | --- |
| [semgrep/semgrep](https://github.com/semgrep/semgrep) | **16163** | Active 2026-08-10; multi-lang pattern SAST | **Embody-continue** pin (already Stage-0 twin); pack discipline |
| [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) | **15461** | Pushed 2026-08-09 | **Embody** structural Stage-0 |
| [github/codeql](https://github.com/github/codeql) | **9923** (~10k bar) | Pushed 2026-08-07; QL libs + query packs | **Embody** CI fixture pack; pack versioning SoR |
| [joernio/joern](https://github.com/joernio/joern) | **3404** (elegant smaller) | Active 2026-08-08; CPG multi-lang | **Refuse** as second merge engine; campaign-only if ever |

#### Embody / Adopt / Refuse

| Stance | Detail |
| --- | --- |
| **Embody** | Named query/rule packs per plant; CodeQL+ast-grep+semgrep as complementary backends with **one** assertion consumer |
| **Adopt** | External-predicate / CSV overlay pattern (SemTaint); MoCQ-style DSL validation *for campaign query authoring* |
| **Refuse** | Joern/IRIS/QLCoder as merge SoR; auto-synthesized queries without fixture expectation + `rule_coverage` |

---

### D4.2 Cross-artifact joins (QL results ↔ OpenAPI ↔ facts)

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2410.23873](https://arxiv.org/abs/2410.23873) | Generating Accurate OpenAPI Descriptions from Java Source Code (AutoOAS) | Source→OpenAPI for Spring; ground-truth comparison — join needs **audited** OpenAPI rows, not LLM OAS alone |
| [2601.12735](https://arxiv.org/abs/2601.12735) | OpenAI for OpenAPI / OOPS: Automated generation of REST API specification via LLMs | LLM OAS generation; F1 high but **Refuse** as citation/merge SoT for Stage-0 |
| [2504.16833](https://arxiv.org/abs/2504.16833) | LRASGen: LLM-based RESTful API Specification Generation | Spec↔impl sync problem statement; complements Respector (ICSE’24, **no arXiv id** — DOI `10.1145/3597503.3639137`) |
| [2403.05986](https://arxiv.org/abs/2403.05986) | Integrating Static Code Analysis Toolchains | Tool-agnostic SCA exchange + traceability — join *contracts* not a second oracle |
| [2306.05057](https://arxiv.org/abs/2306.05057) | SmartBugs 2.0 (SARIF multi-tool aggregation) | SARIF as interchange for multi-tool findings + taxonomy map — **Adopt** export; not assertion SoR |

*Respector (Huang et al., ICSE 2024):* static/symbolic OAS from Java — primary for Spring OpenAPI joins; arXiv id **Unknown** (ACM-only).

#### GitHub repos

| Repo | ★ | Recency / notes | Fit |
| --- | --- | --- | --- |
| [OpenAPITools/openapi-generator](https://github.com/OpenAPITools/openapi-generator) | **26659** | Active 2026-08-10 | **Adopt** OAS ecosystem patterns; not a dep for Stage-0 |
| [oasdiff/oasdiff](https://github.com/oasdiff/oasdiff) | **1309** (elegant; domain-best) | Pushed 2026-08-09; breaking-change diff | **Adopt** for OpenAPI version joins / drift sensors |
| [microsoft/sarif-sdk](https://github.com/microsoft/sarif-sdk) | **224** (elegant; OASIS companion) | Pushed 2026-08-05 | **Adopt** SARIF schema literacy; **Refuse** as Python merge SoR |

#### Embody / Adopt / Refuse

| Stance | Detail |
| --- | --- |
| **Embody** | Explicit join keys (rule_id / path / method / fingerprint) into **same** assertion engine; human-reviewed floors |
| **Adopt** | SARIF/CSV as *wire* formats; oasdiff-class structural OpenAPI diff as sensor |
| **Refuse** | Soft-green empty OpenAPI/Messaging floors; Artifactory-backed join as CI SoT; LLM OAS as fact SoR |

---

### D4.3 Campaign vs merge-SoR corpora / fixture plants

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2309.06229](https://arxiv.org/abs/2309.06229) | PreciseBugCollector: Extensible, Executable and Precise Bug-fix Collection | Distinguishes curated precise corpora vs mined imprecise — maps to fixture vs campaign |
| [2403.09219](https://arxiv.org/abs/2403.09219) | An Extensive Comparison of Static Application Security Testing Tools | Juliet as labeled SAST bench — synthetic plant ≠ production campaign |
| [2402.02961](https://arxiv.org/abs/2402.02961) | GitBug-Java: A Reproducible Benchmark of Recent Java Bugs | Reproducible env packaging for campaign plants |
| [2410.00752](https://arxiv.org/abs/2410.00752) | TestGenEval: A Real World Unit Test Generation and Test Completion Benchmark | Real-project corpus vs lite — dual-plant analogy |

#### GitHub repos

| Repo | ★ | Recency / notes | Fit |
| --- | --- | --- | --- |
| [rjust/defects4j](https://github.com/rjust/defects4j) | **986** (elegant; SE SoR) | Canonical real-fault DB | **Adopt** dual-corpus *discipline* (curated vs campaign) |
| [github/codeql](https://github.com/github/codeql) (qltest fixtures) | **9923** | Pack-local `test/` trees | **Embody** hermetic fixture plant in-repo |
| [iris-sast/iris](https://github.com/iris-sast/iris) (CWE-Bench-Java) | small | Campaign vulnerability corpus | Campaign-only pattern |

#### Embody / Adopt / Refuse

| Stance | Detail |
| --- | --- |
| **Embody** | Fixture plant = merge SoR (E-OCS0 OCS1); OCS = campaign (OCS2–7); same assertion engine |
| **Adopt** | Characterization / remeasure proposing expectation deltas (operator-reviewed write) |
| **Refuse** | Promoting OCS Artifactory DB to required CI; rewriting pytest/oracle Cover% for one client tree |

---

## D5 — Drift detection & capacity preflight

**Confirmed seams:** `spring_drift_*` two-tier façade; `capacity_preflight_*`
with Stage-4 proxy honesty modules; dual-plant floors; constitution 16-A climb
artifact path.

### D5.1 Semantic / API drift detection

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2008.12808](https://arxiv.org/abs/2008.12808) | A First Look at the Deprecation of RESTful APIs: An Empirical Study (RADA) | OpenAPI deprecation / breaking-change mining — deprecation ≠ removed |
| [2311.08175](https://arxiv.org/abs/2311.08175) | Microservice API Evolution in Practice | Industry strategies; openapi-diff / regression testing as drift nets |
| [2605.24397](https://arxiv.org/abs/2605.24397) | Breaking Changes in Software Ecosystems: A Systematic Literature Review | Syntactic vs **behavioral** breaks; SemVer systematically violated — behavioral drift **Unknown**/hard |
| [2605.28148](https://arxiv.org/abs/2605.28148) | DeltaMCP: Incremental Regeneration via Spec-Aware Transformation for MCP servers | oasdiff-driven incremental MCP regen — Adopt for *operator surface* drift, not Stage-0 SoR |

#### GitHub repos

| Repo | ★ | Recency / notes | Fit |
| --- | --- | --- | --- |
| [oasdiff/oasdiff](https://github.com/oasdiff/oasdiff) | **1309** | Active; breaking-change CLI + GHA | **Adopt** OpenAPI semantic/structural drift sensor |
| [OpenAPITools/openapi-generator](https://github.com/OpenAPITools/openapi-generator) | **26659** | Spec ecosystem | Spec↔client drift patterns |
| In-repo `spring_drift_*` | — | Two-tier hash + citation recheck `[Confirmed]` | **Embody** signal-doc drift |

#### Embody / Adopt / Refuse

| Stance | Detail |
| --- | --- |
| **Embody** | Tiered drift (hash → structural recheck); fail-closed unknown signatures |
| **Adopt** | oasdiff-class API contract diff; characterization before threshold rewrite |
| **Refuse** | Runtime traffic fingerprinting as CI SoT; LLM “explain drift” as merge authority |

---

### D5.2 Capacity / scale estimation for analysis pipelines

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2308.09660](https://arxiv.org/abs/2308.09660) | Incrementalizing Production CodeQL Analyses (iQL) | Sub-minute incremental updates; high init RAM — capacity is **resource**, not correctness |
| [2401.01571](https://arxiv.org/abs/2401.01571) | Principles and Practices of Large-Scale Code Analysis at Ant Group… | Compile vs non-compile extraction cost; scale budgets `[Evidenced]` title verified 2026-08-10 |
| [2501.03440](https://arxiv.org/abs/2501.03440) | CI at Scale: Lean, Green, and Fast | Speculative scheduling / thresholds — **Adopt** as CI capacity sensor pattern |
| [2604.12673](https://arxiv.org/abs/2604.12673) | Intelligent resource prediction for SAP HANA continuous integration build workloads | Quantile memory prediction — pattern for preflight estimates |
| [2605.07900](https://arxiv.org/abs/2605.07900) | Longitudinal Analyses of SAST Tools: A CodeQL Case Study | Runtime distributions; incrementalization timeline — informs CodeQL capacity honesty |

#### GitHub repos

| Repo | ★ | Recency / notes | Fit |
| --- | --- | --- | --- |
| [github/codeql](https://github.com/github/codeql) | **9923** | DB create = long pole `[Confirmed]` E-CQL0 | Capacity subject |
| [actions/runner](https://github.com/actions/runner) | **6172** | GHA runner economics | Matrix cost awareness |
| In-repo `capacity_preflight*` | — | Stage-0 scale + Stage-4 proxy modules `[Confirmed]` | **Embody** preflight façade |

#### Embody / Adopt / Refuse

| Stance | Detail |
| --- | --- |
| **Embody** | Preflight estimates + fingerprint skip of unchanged CodeQL inputs |
| **Adopt** | Documented wall-clock / memory / pack-size sensors; optional ML predictors as *sensors only* |
| **Refuse** | Capacity green ⇒ quality green; capacity numbers as Cover% / fail_under proof |

---

### D5.3 Threshold honesty / proxy metrics vs SoT

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [1803.04585](https://arxiv.org/abs/1803.04585) | Categorizing Variants of Goodhart's Law | Proxy over-optimization taxonomy — SoT vs sensor vocabulary |
| [2309.02395](https://arxiv.org/abs/2309.02395) | Mind the Gap: The Difference Between Coverage and Mutation Score Can Guide Testing Efforts | Oracle gap: Cover% ≠ adequacy — maps to climb vs oracle |
| [2212.06118](https://arxiv.org/abs/2212.06118) | A Brief Survey on Oracle-based Test Adequacy Metrics | Coverage alone is weak proxy |
| [2310.09144](https://arxiv.org/abs/2310.09144) | Goodhart's Law in Reinforcement Learning | Formal proxy over-optimization — refuse single proxy gates |
| [2608.03535](https://arxiv.org/abs/2608.03535) | CodeAssay: A Multi-Metric Benchmark with Audited Ground Truth | Audited GT changes labels — **Embody** fixture audit discipline |

#### GitHub repos

| Repo | ★ | Notes | Fit |
| --- | --- | --- | --- |
| Repo constitution + `coverage.xml` oracle | — | fail_under 98.7; climb `coverage.climb.xml` (16-A) `[Confirmed]` | **Embody** distinct artifact paths |
| Mutation / adequacy tooling (in-repo vacuity / STF) | — | Sensor suites | **Adopt** as sensors; never oracle substitute |

#### Embody / Adopt / Refuse

| Stance | Detail |
| --- | --- |
| **Embody** | Label every Stage-4 / capacity / climb metric as **proxy**; oracle Cover% sole fail_under SoR |
| **Adopt** | Multi-metric honesty (oracle gap thinking); characterization plants before threshold moves |
| **Refuse** | Fuzzy/PID green; scoped `--cov` conflated with whole-repo 98.7; LLM-judge as quality SoT |

---

## D6 — Operator CLI (brief)

Cross-ref: E-OAS0 (`process/37-…`). Subdomains only.

### D6.1 Actionable CLI errors

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [1608.08219](https://arxiv.org/abs/1608.08219) | NoFAQ: Synthesizing Command Repairs from Examples | Classic actionable CLI repair from error+command |
| [2210.11630](https://arxiv.org/abs/2210.11630) | Using Large Language Models to Enhance Programming Error Messages | Enhanced PEMs; LLM rewrite is **sensor**, not SoT |
| [2307.10793](https://arxiv.org/abs/2307.10793) | Addressing Compiler Errors: Stack Overflow or Large Language Models? | Error+code context → fix guidance |
| [2209.07365](https://arxiv.org/abs/2209.07365) | Do Cloud Developers Prefer CLIs or Web Consoles? | CLI remains CRUD/debug SoR for operators |
| [2605.31104](https://arxiv.org/abs/2605.31104) | Extending the UXR Point of View Playbook… | Actionable error messages ↔ support cost — product UX bar |

#### GitHub repos

| Repo | ★ | Recency / notes | Fit |
| --- | --- | --- | --- |
| [pallets/click](https://github.com/pallets/click) | **17617** | Active 2026-08-09 | Ecosystem SoR; Typer vendors Click |
| [fastapi/typer](https://github.com/fastapi/typer) | **19881** | 0.27.0 (2026-07-15) | **Adopt** thin `doc-engine grade` façade |
| [Textualize/rich](https://github.com/Textualize/rich) | **57044** | TTY polish | **Adopt** optional TTY; **Refuse** as CI SoT (E-UX0) |
| [clig.dev](https://clig.dev/) (guide, not a ★ repo) | — | Human+machine dual output | **Embody** dual-sink doctrine |

#### Embody / Adopt / Refuse

| Stance | Detail |
| --- | --- |
| **Embody** | Structured error code + next-step remediation + JSON receipt; stderr-only on stdio MCP |
| **Adopt** | Typer façade; NoFAQ-shaped repair hints; clig.dev dual output |
| **Refuse** | Traceback-as-UX in grading pack; rich tables as merge proof |

---

### D6.2 Multi-shell matrix testing

#### arXiv (≥3)

| ID | Title | Relevance |
| --- | --- | --- |
| [2212.00908](https://arxiv.org/abs/2212.00908) | Test Flakiness' Causes, Detection, Impact and Responses: A Multivocal Review | Environment/order flakiness — matrix surfaces shell variance |
| [2111.03382](https://arxiv.org/abs/2111.03382) | Discerning Legitimate Failures From False Alerts (Chromium CI) | Classify vs blind rerun — cost honesty for matrix |
| [2401.15788](https://arxiv.org/abs/2401.15788) | 230,439 Test Failures Later: An Empirical Evaluation of Flaky Failure Classifiers | Flaky vs real at CI scale |
| [2602.02307](https://arxiv.org/abs/2602.02307) | Understanding and Detecting Flaky Builds in GitHub Actions | Rerun cost in GHA (years of compute) — **Refuse** infinite matrix |

#### GitHub repos

| Repo | ★ | Notes | Fit |
| --- | --- | --- | --- |
| [actions/runner](https://github.com/actions/runner) | **6172** | GHA matrix execution | Matrix vehicle |
| GHA `strategy.matrix` (docs.github.com) | — | OS × shell × Python | **Adopt** finite campaign matrix (OAS16) |
| [pallets/click](https://github.com/pallets/click) / [fastapi/typer](https://github.com/fastapi/typer) | ≥17k | CLI surface under test | Smoke subjects |

#### Embody / Adopt / Refuse

| Stance | Detail |
| --- | --- |
| **Embody** | Finite campaign OS×shell matrix for grade smoke; fixture CI stays hermetic Linux |
| **Adopt** | `fail-fast: false`; flaky classifiers over blind 5× rerun; job-level `if:` not path-skip on required checks |
| **Refuse** | Matrix as Cover% SoR; phone/device-farm as CLI SoT; unbounded OS×shell×Python explosion |

---

## Cross-cutting Unknown

| Item | Why Unknown |
| --- | --- |
| Live star-count drift after 2026-08-10 snapshot | API snapshot only |
| Respector arXiv id | ICSE’24 ACM-only in searched primaries |
| Live OCS OpenAPI↔QL join hit rates on tip | No `ocs-api-service` checkout / Artifactory |
| Whether behavioral API drift (SLR 2605.24397) is tractable for Stage-0 | Product Spike if Spec asks |
| Exact GHA minute cost of proposed OAS16 matrix | Needs budget spike |

---

## Spec seed tickets (DRAFT — not Approve)

| ID | Title | Acceptance (sketch) |
| --- | --- | --- |
| **CQLJ1** | Join contract schema (QL row ↔ OpenAPI ↔ fact) | Documented keys; same assertion engine; fixture floors unchanged |
| **CQLJ2** | Pack port boundary (CI vs Stage-0) | No dual-write; fingerprint inputs include join artifacts |
| **TOOL4-D** | Drift honesty labels | Tier statuses + proxy vs SoT in report schema |
| **TOOL4-C** | Capacity ≠ Cover% | Schema field `is_proxy: true`; tests refuse conflation |
| **OAS16** | Finite shell matrix | Campaign workflow only; not required merge SoR |

**Exit:** Spec Approve per epic → one Implement stream → Verify (ruff, size, complexipy, claims, cov oracle 3.11) → Archive.

---

## Adversarial checklist

- [ ] Did any paper get treated as merge SoR without fixture plant?
- [ ] Is OCS still campaign-only?
- [ ] Is capacity/Stage-4 explicitly non-oracle?
- [ ] Is rich still barred from CI SoT?
- [ ] Were ★ counts stamped with date?
- [ ] Were Unknowns marked (DeepWiki, Respector arXiv, live OCS)?
