---
segment: 03
title: Scientific dimensions — Structural/Cognitive, Computational/Environmental, Architectural/Operational, Agentic/Probabilistic
branch: wave1-gates-untrusted-tree-hygiene
status: RESEARCH COMPLETE — segment SoT for metric scorecards + gate mapping; no code impl
research date: 2026-08-08
wave: wave1
claim tiers: Evidenced / Confirmed / Unknown
siblings:
  - docs/research/coverage-quality/01-coverage-oracle-climb-solid.md
  - docs/research/process/02-foundational-agentic-se-2026.md
  - docs/research/process/04-implementation-frameworks.md
  - docs/research/process/05-dynamics-neuromorphic.md
related:
  - docs/design/coverage-measure-modes-design-2026-08-08.md
  - docs/agentic-foundational-se-taxonomy-2026-08-08.md
  - CONTRIBUTING.md
do_not:
  - implement dual-mode / MeasureMode
  - add new CI metric tools in this pass
  - weaken fail_under, complexipy ≤5, or size ≤225
---

# Segment 03 — Scientific dimensions & metrics (gate mapping)

> Owns the **four scientific-dimension scorecards** and maps each metric class onto
> **this** product: a Python CLI (`doc_engine`, `stf`) with deterministic quality gates.
> Lens: Formal Methods (predicates / witnesses), Effective Software Testing (Aniche —
> oracles & testability), and Control Theory (sensors vs actuators; boolean floors vs
> continuous feedback). Dual-mode climb/oracle remains **design-only**.

**Claim tiers**

| Tier | Meaning |
| --- | --- |
| `[Evidenced]` | Primary paper, official docs, or verified tool/repo page supports the claim |
| `[Confirmed]` | Local seams agree (CONTRIBUTING, `quality_gate_checks.py`, ratchets, pyproject) |
| `[Unknown]` | ID/source missing, hype transfer, or product choice still open |

**Stance vocabulary:** **Embody** = already true in gates/product · **Adopt** = take next
(process/docs/gates) · **Refuse** = wrong shape for this product (or ungated form is unsafe).

**Out of scope:** taxonomy cells → sibling **02**; framework catalog (DDD/hexagonal/…) →
sibling **04**; PID/neuromorphic metaphors → sibling **05**. A principal memo at
`docs/agentic-foundational-se-taxonomy-2026-08-08.md` may overlap; **this file is SoT for
dimension scorecards + gate mapping** when merging.

---

## 1. Lens — Formal Methods / ESE / Control Theory

How this segment reads metrics before the scorecards.

| Lens | What it demands of a metric | Repo reading |
| --- | --- | --- |
| **Formal Methods** | A gate is a **predicate** with a **witness**. If it cannot be shown to fail, it is not a gate. Termination / stratification matter for agent loops. | `fail_under`, complexipy offender ratchet, size baseline, claims checker, PathCohesion, gate mutators — all produce decidable pass/fail + artifact witness `[Confirmed]`. |
| **ESE (Effective Software Testing)** | Oracles must be explicit; testability prefers small units and clear seams; mutation checks whether the oracle actually bites. | Coverage oracle vs climb sensor; mutation taxonomies (gate mutators ≠ PIT); soft advisory bands ≠ hard ceiling `[Confirmed]` CONTRIBUTING. |
| **Control Theory** | Distinguish **plant sensors** (continuous feedback) from **actuators / setpoints** (hard limits). Controllers that soften a boolean setpoint are misapplied. | Climb Cover% / gap-average / remesure cadence = sensors. Oracle 98.7, complexipy ≤5, LOC ≤225 = setpoints. PID-as-floor → sibling **05** **Refuse**. |

**Synthesis rule:** Probabilistic sensors may steer agents; only deterministic predicates may merge.

---

## 2. Source verification (metrics literature)

Fetched / audited 2026-08-08 unless noted. Do not trust prompt labels blindly.

| Label | Claimed anchor | What it actually is | Tier |
| --- | --- | --- | --- |
| Cyclomatic complexity | McCabe 1976 (\(M = E - N + 2P\)) | Classic CFG edge/node/component count. Still taught; **not** this repo’s primary complexity SoT. | `[Evidenced]` (classic) |
| Cognitive complexity | Campbell / Sonar TechDebt 2018 whitepaper | Human-comprehension-oriented increment rules (breaks, nests, sequences). complexipy implements a Campbell/Sonar-**inspired** metric (not Sonar-affiliated). | `[Evidenced]` (whitepaper) / tool `[Confirmed]` |
| Empirical understandability | arXiv **2007.12520**, **2303.07722** | Cited in CONTRIBUTING quality-gates evidence table as framing for complexity/size policy. | `[Evidenced]` (via CONTRIBUTING audit trail) |
| Semantic density (agentic) | arXiv **2604.07502** | Ustynov, *Beyond Human-Readable…* — agentic semantic-density optimization. Real paper; not a CI metric definition. | `[Evidenced]` |
| Semantic Density Effect (prompts) | arXiv **2604.17659** | Prompt/token density effects; compression can *raise* cost. | `[Evidenced]` |
| Green AI | arXiv **1907.10597** (Schwartz et al.) | Efficiency / cost as first-class evaluation (FPO, price tags). Carbon-aware *schedulers* are a later ops overlay, not this paper. | `[Evidenced]` / schedulers `[Unknown]` value here |
| CoverUp (scoped climb) | arXiv **2403.16218** | Coverage-guided LLM test gen; inner measure-on-missing → outer acceptance. Pattern kin of climb vs oracle. | `[Evidenced]` |
| Package coupling Ca/Ce / \(I\) | Martin package metrics | Afferent/efferent coupling; Instability \(I = C_e/(C_a+C_e)\). Classic design hygiene — not wired as numeric CI thresholds here. | `[Evidenced]` (classic) |
| LCOM | Chidamber & Kemerer et al. | Lack of Cohesion of Methods family. Deferred in CONTRIBUTING — no 2026-maintained Python CI tool selected. | `[Evidenced]` (classic) / gate status `[Confirmed]` deferred |
| SRE error budgets | Google SRE books (secondary) | Budgeted SLO burn for reliability. Analogy only for coverage floor — **not** license to weaken 98.7. | `[Evidenced]` (practice) |
| Issue-resolution Verify | arXiv **2512.22256** | Jiang/Lo/Liu survey — validation/selection bind acceptance. | `[Evidenced]` |
| Self-evolving agents | arXiv **2608.03392** | Zhou et al. survey — feedback reliability / safety risks. | `[Evidenced]` |
| LLM-as-Judge | DeepWiki langchain-ai/openevals | Verified judge-evaluator pattern; advisory only. | `[Evidenced]` |
| “EpO” as Green AI unit | prompt shorthand | Treat as **energy / cost per outcome** vocabulary adjacent to Green AI FPO — not a standardized SI unit in-repo. | `[Unknown]` as formal unit · Green AI paper `[Evidenced]` |
| Recall@K (IR/RAG) | classic IR + RAG lit | Fraction of relevant items in top-K. No formal Recall@K merge gate here; Stage-0 has entity-recall / `RECALL_MISS` seams ≠ IR Recall@K. | `[Evidenced]` (metric family) / product gate `[Unknown]` / absent |

---

## 3. Hard gates already Embodied (SoT table)

Primary table: CONTRIBUTING §“In-repo quality gates” + `doc-engine quality-gates`.
`[Confirmed]` 2026-08-08.

| Gate | Threshold | Tool / witness | Dimension | Formal role |
| --- | --- | --- | --- | --- |
| Whole-repo Cover% | **98.7** `fail_under` | pytest-cov / coverage.py; CI **3.11 only**; cohesive `coverage.xml` | Computational (cost) + Architectural (SLO) | Oracle **setpoint** |
| New-code coverage | **≥98.7%** | diff-cover vs compare ref | Architectural / ESE | Patch oracle |
| Cognitive complexity | **≤5** / function | complexipy `--max-complexity-allowed=5`; offender-count ratchet → 0 | Structural & Cognitive | Hard predicate |
| File LOC | hard **>225**; soft **>150** | `doc-engine size-ratchet` + `size_baseline.json` | Structural & Cognitive | Hard / advisory band |
| Function statements | hard **>50**; soft **>20** | size-ratchet + `check_code_quality.py` growth | Structural & Cognitive | Hard / advisory band |
| Duplication | **≤3%** (`--min-lines=5`) | jscpd on changed package `.py` | Structural | Hard predicate |
| Import cycles | **forbid** | tach `forbid_circular_dependencies` | Architectural (Ca/Ce proxy) | Hard predicate |
| Path cohesion | cohesive tree only | `PathCohesionGuard` in coverage-measure | Architectural / DDIA SoT | Witnessed invariant |
| State claims | predicates resolve | `check_repo_claims.py` | Agentic hygiene (docs-as-spec) | Hard predicate |
| McCabe (C901) | — | ruff C901 **not selected** | Structural | Advisory / deferred as SoT |
| LCOM / Ca·Ce scores | — | **Deferred** (CONTRIBUTING) | Architectural | No fake CI |
| Big-O | — | **Deferred** — ADR/review | Computational | No static gate |
| Mutation score as fail_under | — | mutators report; CI non-blocking until zero-survivor defended | ESE | Witness-in-progress |

---

## 4. Dimension scorecards

### 4.1 Structural & Cognitive

| Topic | Source | Today | Gap | Stance |
| --- | --- | --- | --- | --- |
| CFG / Cyclomatic \(M=E-N+2P\) | McCabe | Soft/optional only (ruff C901 not selected); `check_code_quality` nesting advisory | Keep as secondary signal | **Embody** cognitive as SoT · **Refuse** replacing ≤5 cognitive with raw McCabe alone |
| Cognitive complexity ≤5 | Campbell; complexipy | **Hard fail** + downward offender ratchet `[Confirmed]` | Dual-mode impl must not invent mode-boolean soup (design decision 15) | **Embody** · **Refuse** raising threshold to “land features” |
| Size ≤225 LOC / fn budgets | size-ratchet | Hard >225 LOC / >50 stmts; soft 150/20; tests included | Thin facades for over-budget CLI modules; no utils grab-bags | **Embody** · **Refuse** mega-modules / mechanical `part2` chops |
| Semantic density | arXiv:2604.07502, 2604.17659 | Descriptive names + concept modules (vertical slices) | No formal SDE score in CI | **Embody** naming culture · **Adopt** decision-14-style naming in measure modes · **Refuse** abbreviation theater “for tokens” (papers: cost can *rise*) · **Refuse** SDE CI metric in v1 |
| Naming / mode flags | Clean Code; Hofmeister et al. | CONTRIBUTING + design quality bar | Mandate in dual-mode measure impl | **Refuse** single-letter / `m`/`o`/`c` mode flags |

**Formal/ESE note:** Cognitive ≤5 and size ceilings are **stratification** aids — they bound the human/agent edit surface so Verify stays tractable. They are not proxies for Cover%.

### 4.2 Computational & Environmental

| Topic | Source | Today | Gap | Stance |
| --- | --- | --- | --- | --- |
| Wall-clock / matrix cost | CI layout | Cov cell **Python 3.11 only** — cuts ~3× cov waste `[Confirmed]` | Document climb as time/energy accelerator, not floor | **Embody** 3.11-only cov · **Refuse** cov on every Python version |
| Big-O time/space | classic + CONTRIBUTING deferred | Review/ADR only | Profile before native rewrite | **Refuse** fake static Big-O CI · **Adopt** profiled hot-path notes if measured |
| Green AI / EpO | Schwartz arXiv:1907.10597 | Implicit via fewer cov cells + hermetic fixtures | Optional carbon-aware scheduling later | **Embody** cheap wins · **Adopt** climb scoping for local energy/time (design) · **Refuse** blocking merges on carbon APIs before oracle/climb split |
| Cache / reuse | coverage combine pitfalls; PathCohesion | Fresh measure in one tree; no cross-worktree combine | Distinct climb artifact policy (design decision 16) | **Embody** PathCohesion · **Refuse** cached/stale XML as oracle witness |
| Scoped climb vs full oracle | CoverUp; pytest-cov | Design only | Timed demo after approve | **Refuse** scoped `--cov-fail-under` as 98.7 proof (pytest-cov total is over *measured* sources) |
| Rust / WASM / SlipCover | Rust stack-fit memo | Pick-none default; consume pinned Rust CLIs | Profile before in-tree native | **Refuse by default** (framework detail → sibling **04**) |

**Control-theory note:** Matrix cost and climb cadence are **resource sensors**. They must not retarget the coverage setpoint.

### 4.3 Architectural & Operational

| Topic | Source | Today | Gap | Stance |
| --- | --- | --- | --- | --- |
| Afferent/efferent / \(I=C_e/(C_a+C_e)\) | Martin | tach **circular-deps** hard fail only | No full I dashboard | **Embody** cycle forbid · **Refuse** metrics cathedral of Ca/Ce thresholds |
| LCOM / cohesion suites | CK metrics | **Deferred** — no 2026 tool selected `[Confirmed]` CONTRIBUTING | PathCohesion + concept modules as practical cohesion | **Embody** PathCohesion / single-writer · **Refuse** fake LCOM CI |
| SRE error budgets | SRE books | `fail_under` ≈ coverage SLO | Name oracle as floor/SLO in CONTRIBUTING Oracle-vs-Climb table | **Embody** boolean floor · **Refuse** “error-budget burn” that weakens 98.7 |
| Golden paths / IDP | platform eng | `doc-engine coverage-measure`, `quality-gates`, claims checker | Explicit Oracle vs Climb table | **Embody** CLI golden path · **Refuse** Backstage install for this CLI (→ **04**) |
| jscpd / duplication | CONTRIBUTING | ≤3% on changed files | — | **Embody** |
| Unlabeled metric destination | log-smell adjacency (arXiv:2412.09284) | Banner + distinct climb artifact (design 11/16) | Keep climb Cover% labeled as sensor | **Adopt** labeling discipline · **Refuse** unlabeled Cover% as floor |

### 4.4 Agentic & Probabilistic

| Topic | Source | Today | Gap | Stance |
| --- | --- | --- | --- | --- |
| Plan-Act-Verify loops | arXiv:2512.22256 | Agents + pytest / quality-gates | Explicit: climb iterations = **loop metric**, not floor | **Embody** partial · **Adopt** Verify = deterministic gates for climb batches · **Refuse** autonomous merge without Verify |
| Verification-loop convergence | CoverUp; control analogue | Remesure oracle after batch / before PR (design decision 5) | Debounce / saliency language (→ **05**) | **Embody** cadence policy · treat “iterations to oracle green” as process metric only |
| Hallucination / LLM-judge | openevals; semantic-pipeline-eval | Citation tags; Stage-0 deterministic; skill-level Jaccard / spot-check heuristics | Keep judge advisory | **Refuse** LLM-judge / hallucination % as `fail_under` |
| Context Recall@K | IR/RAG lit; MSR-LM | Context packets / Stage-0; entity-recall seams ≠ Recall@K | No formal Recall@K merge gate | **Refuse** packet freshness / Recall@K as coverage SoT · **Unknown** whether to Adopt advisory Recall@K later |
| Self-evolution of gates | arXiv:2608.03392 | Steering prompts + human session log | — | **Refuse** ungated CONSTRAINTS / baseline / `fail_under` self-rewrite |
| SDD one-stream | arXiv:2606.04967 | Desired process | Encode Spec→Impl→Verify | **Adopt** (owned primarily by sibling **02**) |

---

## 5. Gate ↔ dimension map (quick reference)

```text
Structural & Cognitive     Computational & Environmental
─────────────────────      ─────────────────────────────
complexipy ≤5              fail_under 98.7 (oracle cost)
size ≤225 / stmts ≤50      CI cov on 3.11 only
jscpd ≤3%                  climb = cheap sensor (design)
C901 McCabe (soft/off)     Green AI / EpO (implicit)
semantic density (culture) Big-O (deferred / ADR)

Architectural & Operational   Agentic & Probabilistic
───────────────────────────   ───────────────────────
tach cycles (Ca/Ce proxy)     climb loop iterations
PathCohesionGuard             LLM-judge / hallucination (advisory)
diff-cover 98.7               Recall@K (no merge gate)
error-budget analogy≠burn     Verify binds to deterministic oracles
claims checker                refuse ungated self-evolution
```

---

## 6. Embody / Adopt / Refuse (summary)

| Idea | Stance | Mapping |
| --- | --- | --- |
| Cognitive complexity ≤5 (complexipy) | **Embody** | Hard gate; never raise to land features |
| Size ≤225 / stmts ≤50 | **Embody** | Hard ratchet; soft advisory bands OK |
| Oracle Cover% 98.7 + diff-cover 98.7 | **Embody** | Boolean setpoint; CI 3.11 witness |
| PathCohesion + no cross-worktree combine | **Embody** | Cache/dilution refusal |
| tach cycle forbid | **Embody** | Minimal coupling gate |
| Climb as verification-loop sensor | **Adopt** (design) | CoverUp-style inner loop; not floor |
| Semantic density via names/modules | **Embody** culture · **Refuse** SDE CI v1 | Decision **24** |
| Green-Ops cheap wins / climb energy | **Embody** 3.11-only · **Optional** carbon later | Aligns decision **23** (framework sibling may restated) |
| Ca/Ce numeric dashboards / LCOM CI | **Refuse** (v1) | Deferred; no metrics cathedral |
| Error-budget burn under 98.7 | **Refuse** | SRE analogy ≠ license to soften |
| McCabe as sole complexity SoT | **Refuse** | Cognitive remains SoT |
| Big-O static CI | **Refuse** | ADR/review only |
| Recall@K / packet freshness as Cover% SoT | **Refuse** | Advisory research only |
| LLM-judge / hallucination rate as merge gate | **Refuse** | Advisory (openevals / semantic-eval) |
| PID / fuzzy green on floor | **Refuse** | Sibling **05** decisions 25–28 |

---

## 7. Decisions owned by this segment

Reconcile with dual-mode **1–16**, taxonomy/layers **17–21**, frameworks **18/22–23**,
dynamics **25–28**. Numbers stable for merge:

| # | Decision | Stance |
| --- | --- | --- |
| **24** | **Semantic density:** prefer descriptive names and vertical/concept modules over token-compression refactors; **do not** add an SDE CI metric in v1 | Embody / Refuse SDE gate |
| **29** | **Metric layering:** only CONTRIBUTING hard gates (table §3) are merge SoT; climb Cover%, gap-average, LLM-judge, Recall@K, carbon, Ca/Ce/LCOM scores are sensors/advisory/deferred — never silent promotions | Embody / Refuse promotion |
| **30** | **Complexity SoT:** Campbell-style cognitive via complexipy ≤5 remains the complexity predicate; McCabe/C901 stays optional/soft; do not dual-SoT | Embody / Refuse McCabe takeover |
| **31** | **Environmental accounting:** keep cov-only-3.11; treat EpO/Green AI as documentation + scoping incentive; never block oracle correctness on carbon APIs in v1 | Embody / Optional later |

**Cross-links (not owned here):** oracle vs climb SoT hygiene → **01**; layer binding /
ungated evolution / judge-not-fail_under / SDD → **02** (17, 19–21); hexagonal / Green-Ops
restatement / mesh refuse → **04** (18, 22–23); PID/fuzzy/hysteresis → **05** (25–28).

---

## 8. Segment verdict

| Question | Answer |
| --- | --- |
| Which metrics are merge SoT today? | Cover% / diff-cover **98.7**, complexipy **≤5**, size **≤225** / stmts **≤50**, jscpd **≤3%**, tach cycles, PathCohesion, claims checker. |
| What must agents not confuse? | Climb Cover%, gap-average, judge scores, Recall@K, error-budget talk ≠ oracle floor. |
| Formal/ESE/control takeaway? | Predicates need witnesses; oracles stay explicit; continuous sensors must not retarget boolean setpoints. |
| Safe contribution to dual-mode approve? | Decisions **24, 29–31** strengthen the quality bar; they do not implement dual-mode. Still need **1–16** + layer/framework/dynamics siblings. |
| Code impl in this pass? | **No.** |

**Handoff to coordinator:** Merge with siblings 01/02/04/05 into
`docs/research/se-quality-synthesis-2026-08-08.md`; de-dupe principal taxonomy memo §3.

---

## 9. References

### Papers / classics
- McCabe, cyclomatic complexity (CFG \(M = E - N + 2P\))
- Campbell, *Cognitive Complexity* (SonarSource / TechDebt 2018 lineage)
- Ustynov, *Beyond Human-Readable…*, [arXiv:2604.07502](https://arxiv.org/abs/2604.07502)
- *Semantic Density Effect…*, [arXiv:2604.17659](https://arxiv.org/abs/2604.17659)
- Schwartz et al., *Green AI*, [arXiv:1907.10597](https://arxiv.org/abs/1907.10597)
- CoverUp, [arXiv:2403.16218](https://arxiv.org/abs/2403.16218)
- Jiang, Lo, Liu, *Agentic Software Issue Resolution…*, [arXiv:2512.22256](https://arxiv.org/abs/2512.22256)
- Zhou et al., *Self-Evolving Coding Agents*, [arXiv:2608.03392](https://arxiv.org/abs/2608.03392)
- Understandability framing cited in CONTRIBUTING: [arXiv:2007.12520](https://arxiv.org/abs/2007.12520), [arXiv:2303.07722](https://arxiv.org/abs/2303.07722)
- Martin package metrics (Ca/Ce/I); Chidamber & Kemerer LCOM family
- Google SRE (error budgets — secondary practice)

### Tools / local SoT
- complexipy, diff-cover, jscpd, tach, pytest-cov / coverage.py — CONTRIBUTING evidence table
- DeepWiki: [langchain-ai/openevals LLM-as-Judge](https://deepwiki.com/langchain-ai/openevals/2.1-llm-as-judge-evaluators)
- Local: `src/doc_engine/ci/quality_gate_checks.py`, `coverage_path_cohesion.py`,
  `scripts/ratchets/*_baseline.json`, `pyproject.toml` `fail_under`, coverage-measure design
  decisions 1–16
