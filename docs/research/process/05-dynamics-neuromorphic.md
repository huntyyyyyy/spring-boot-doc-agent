---
category: Research segment 05 — Dynamics / neuromorphic metaphors vs hard gates
status: RESEARCH COMPLETE — informs synthesis; no code impl
date: '2026-08-08'
wave: wave1
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/design/coverage-measure-modes-design-2026-08-08.md
- docs/research/archive/_wip-coverage-design-audit.md
- docs/research/process/20-theory-domains-problem-first-gates-2026.md
- docs/research/process/21-physical-unconventional-computing-2026.md
- docs/research/process/43-physical-info-dynamics-computing-2026-08-10.md
title: 'Segment 05: Dynamics & neuromorphic metaphors (saliency, hysteresis, SoA,
  PID)'
last_reviewed: '2026-08-10'
---

# Segment 05: Dynamics & neuromorphic metaphors (saliency, hysteresis, SoA, PID)

> Verifies real literature behind “temporal coding / saliency / fuzzy state / SoA /
> PID homeostasis” talk, then maps **only** the transferable engineering analogues
> onto this product: a Python CLI with deterministic coverage oracles
> (`fail_under=98.7`), climb feedback, size/complexipy ratchets. Neuromorphic
> runtimes, fuzzy green, SoA rewrites, and PID floor controllers are **out of
> scope for v1**.

**Claim tiers:** `[Evidenced]` primary paper/docs · `[Confirmed]` local seams agree · `[Unknown]` hype, missing ID, or product choice still open.

**Legend:** **Embody** = already true here · **Adopt** = take next (process/docs/policy) · **Refuse** = wrong shape for this product / v1.

Cross-links: dual-mode decisions **1–12** live in
[`coverage-measure-modes-design`](../design/coverage-measure-modes-design-2026-08-08.md);
taxonomy decisions **17–24** in
[`agentic-foundational-se-taxonomy`](../agentic-foundational-se-taxonomy-2026-08-08.md).
This segment proposes **25–28** for the merge synthesis.

---

## 1. Source verification (literature vs hype)

| User / buzz label | Claimed anchor | What it actually is | Tier |
| --- | --- | --- | --- |
| Temporal coding / event saliency | SpikeSlicer arXiv **2410.02249** | **Exists.** *Spiking Neural Network as Adaptive Event Stream Slicer* (Cao et al., NeurIPS 2024). SNN triggers **adaptive slicing** of DVS event streams for tracking/recognition — real neuromorphic CV, not a software-gate pattern. | `[Evidenced]` |
| “Neuromorphic gates for CI” | — | **Hype leap.** SpikeSlicer (and AICAS/IJCNN event-attention work) assume event cameras, membrane dynamics, SNN↔ANN pipelines. No peer-reviewed bridge to pytest-cov cadence. Useful only as **metaphor**: fire expensive work on salient triggers. | `[Unknown]` as product tech · `[Evidenced]` as CV domain |
| Gradient / fuzzy state | FlexGuard arXiv **2602.23636** | **Exists** in a *different* domain: continuous risk scores (0–100) for LLM content moderation with deployment-time thresholds. Shows continuous scores can be useful **when the decision boundary is policy-tunable**. Coverage floor is not that kind of policy. | `[Evidenced]` (moderation) · **Refuse transfer** to oracle |
| Alert hysteresis / flap | Nagios Core flap detection | **Exists.** High/low percent-state-change thresholds suppress notification storms; classic dual-threshold / dead-band practice. | `[Evidenced]` (ops docs) |
| Soft vs hard quality bands | CONTRIBUTING size / complexipy | **Local.** Soft advisory (>150 LOC / >20 stmts) vs hard fail (>225 LOC / >50 stmts; complexipy offender-count ratchet). | `[Confirmed]` |
| SoA vs AoS | Intel layout notes; arXiv **2405.12507** | **Exists.** SoA wins for SIMD / contiguous field scans; AoS for per-object multi-field access. Real HPC/game/sim concern — not Python AST/object graphs. | `[Evidenced]` |
| DOD / ECS as SE architecture | Mike Acton-style talks; taxonomy §4 | Real for homogeneous numeric hot loops. Taxonomy already **Refuse** DOD/ECS for `doc_engine` gate orchestration. | `[Confirmed]` stance |
| PID homeostasis for services | arXiv **2109.02514** | **Exists.** *Parsimonious Edge Computing…* — PID horizontal autoscaling on request-queue length in K8s/Docker. Also ARIMA-PID and related container papers. Domain = **resource controllers**, not coverage predicates. | `[Evidenced]` |
| PID / fuzzy as coverage SoT | — | **Hype.** Treating Cover% error as a PID plant softens or oscillates a boolean floor. No reputable SE practice makes `fail_under` an error term. | `[Unknown]` / refuse |

**Hype filter (one line):** Real papers ≠ transferable product architecture. SpikeSlicer, FlexGuard, and PID autoscalers are `[Evidenced]` *in their domains*; claiming them as doc-engine design primitives without an engineering analogue is theater.

---

## 2. Topic scorecards → this repo

### 2.1 Temporal coding & saliency filters

| Aspect | Finding |
| --- | --- |
| Real science | Event cameras emit asynchronous spikes; SpikeSlicer uses an SNN to decide *when* to slice the stream so downstream ANNs see informative windows `[Evidenced]` arXiv:2410.02249. |
| Honest map | Agent / CI “event storms” = many low-value remesure triggers. Saliency ≈ **debounce / rate-limit** expensive full-oracle runs; fire on batch end, pre-PR, empty/stale targeting inventory. |
| Already designed | Coverage-measure decision **5**: remesure oracle after climb batch / before PR / when targeting from stale XML — not every file edit `[Confirmed]`. |
| Embody | Documented cadence policy; climb as cheap inner loop vs oracle as expensive outer verification (CoverUp-style split). |
| Adopt | Explicit debounce language in CONTRIBUTING Oracle-vs-Climb table; agent prompts: “do not remesure oracle per micro-edit.” |
| Refuse | Neuromorphic runtime, spike membranes, DVS pipelines, SNN libraries inside `doc_engine`. |

### 2.2 Gradient / fuzzy state + hysteresis

| Aspect | Finding |
| --- | --- |
| Real science / ops | Continuous scores (FlexGuard) and flap hysteresis (Nagios high/low thresholds) are legitimate where **policy thresholds** or **notification storms** are the problem `[Evidenced]`. |
| Local embody | Size soft advisory vs hard >225; complexipy ratchet toward 0 while ≤5 remains the policy target `[Confirmed]` CONTRIBUTING. |
| Adopt | Hysteresis for **climb targeting thrash** and optional advisory bands near the floor (e.g. don’t re-pick the same file on every 0.01% delta). Dead-band on *which file to touch*, not on whether the oracle passed. |
| Refuse | Fuzzy “confidence of green” replacing oracle pass/fail. Continuous Cover% as a *display* metric is fine; as a *gate predicate* it must collapse to boolean `≥ fail_under`. |
| Hard invariant | `fail_under=98.7` (and certified oracle floor) stay **hard boolean SoT**. Climb must not apply whole-repo fail_under (decision **3**). |

### 2.3 SoA vs AoS (and DOD)

| Aspect | Finding |
| --- | --- |
| Real science | SoA pays when kernels stream one field across many instances (SIMD/cache); AoS pays when code touches several fields of one object `[Evidenced]` Intel / arXiv:2405.12507. |
| Honest map | Stage-0 hits, AST nodes, `MeasureRun` records are **heterogeneous object graphs** with random access — classic AoS/OO territory. |
| Embody | Current Python domain models (dicts/dataclasses/objects); taxonomy refuse of DOD/ECS for measure work (decision **22**). |
| Adopt | None for v1. If a profiled numeric hot path ever appears (large homogeneous float/int scan), reconsider layout *locally* — not as an architecture slogan. |
| Refuse | SoA/DOD rewrite of `doc_engine` / `stf` graphs; ECS entity stores for gates; “data-oriented” refactors without a measured bottleneck. |

### 2.4 PID / homeostatic control

| Aspect | Finding |
| --- | --- |
| Real science | PID (and fuzzy-PID) controllers successfully regulate continuous plants — queue length, UAV attitude, servo position `[Evidenced]` arXiv:2109.02514 + control lit. |
| Honest map | Coverage floor is a **predicate / SLO**, not a plant to drive with proportional error. Softening 98.7 via integral windup or “error budget burn” is the opposite of ratchet discipline. |
| Embody | Boolean gates: fail_under, complexipy ratchet, size baseline, claims checker, PathCohesion. |
| Adopt (narrow, optional later) | Simple **rate caps / concurrency limits** for CI or agent remesure storms *first*. Revisit PID only if caps fail and the controlled variable is continuous (queue depth, parallel jobs) — never Cover% floor. |
| Refuse for v1 | PID (or fuzzy-PID) as coverage-floor controller; treating oracle delta as \(e(t)\) that may pass under 98.7 “temporarily.” |

---

## 3. Embody / Adopt / Refuse (summary table)

| Idea | Stance | Mapping to this repo |
| --- | --- | --- |
| Neuromorphic / SNN / DVS runtime | **Refuse** | Wrong product domain; keep SpikeSlicer as citation for metaphor hygiene only. |
| Saliency → debounce remesure storms | **Adopt** (docs/process); **Embody** decision 5 | Oracle remesure on salient triggers only; climb for micro-loops. |
| Climb as cheap temporal filter | **Embody** (design) | Dual-mode climb vs oracle; no climb fail_under substitute. |
| Nagios-style hysteresis on advisory / targeting | **Adopt** | Dead-band climb file selection; size soft vs hard already embodies dual thresholds. |
| Fuzzy / gradient “green confidence” | **Refuse** | No continuous gate replacing boolean oracle. |
| FlexGuard-style continuous scores | **Refuse as SoT** | Fine for moderation-like advisory systems; not for Cover% floor. |
| SoA / DOD / ECS rewrite | **Refuse** (v1 and default) | Matches taxonomy decision 22; AoS/OO fits AST/signal graphs. |
| PID autoscaling for containers | **Refuse for coverage**; **Unknown / later** for job concurrency | Real for K8s queues `[Evidenced]`; irrelevant to fail_under. |
| Oracle `fail_under` as boolean predicate | **Embody** | Hard invariant — never PID/fuzzy softener. |

---

## 4. Proposed design decisions (25–28)

Pending merge into the wave1 synthesis; confirm alongside taxonomy **17–24** and dual-mode **1–12**:

25. **Hard predicates stay hard:** `fail_under` / oracle certified floor are boolean SoT; no PID, fuzzy membership, or “confidence of green” softening.  
26. **Saliency for climb cadence:** rate-limit / debounce full oracle remesure; climb batches fire on salient triggers only (aligns decision **5**).  
27. **Hysteresis allowed only on advisory bands / targeting:** size soft-band, climb “almost green” thrash control — never on oracle pass/fail.  
28. **SoA / neuromorphic / PID theater refused** for `doc_engine` domain models and coverage SoT in v1; simple rate caps before any control-theoretic concurrency controller.

---

## 5. What agents must not do

- Remesure whole-repo oracle on every file touch during a climb batch.  
- Report climb Cover% (or any fuzzy score) as proof of 98.7.  
- Propose SoA/DOD/SNN/PID refactors as prerequisites for dual-mode climb.  
- Weaken `fail_under` via error-budget language borrowed from SRE without an explicit human + claims-checker change.

---

## 6. References

- Cao et al., *Spiking Neural Network as Adaptive Event Stream Slicer* (SpikeSlicer), arXiv:2410.02249 / NeurIPS 2024  
- FlexGuard, *Continuous Risk Scoring for Strictness-Adaptive LLM Content Moderation*, arXiv:2602.23636  
- Nagios Core docs, *Detection and Handling of State Flapping*  
- Banchelli et al. / related, *Parsimonious Edge Computing…* (PID microservice scaling), arXiv:2109.02514  
- Springer / related container work: ARIMA-PID autoscaling (secondary)  
- Intel Developer Zone, *Memory Layout Transformations* (AoS↔SoA); arXiv:2405.12507 (AoS↔SoA views)  
- CoverUp, arXiv:2403.16218 (scoped climb vs full oracle pattern)  
- Local: CONTRIBUTING size soft/hard + complexipy ratchet; `pyproject.toml` `fail_under=98.7`; coverage-measure design decisions 3 & 5  

---

## 7. Segment verdict

| Question | Answer |
| --- | --- |
| Is neuromorphic literature real? | Yes — SpikeSlicer et al. `[Evidenced]`. |
| Does it belong in doc-engine v1? | No — **Refuse** runtime; **Adopt** debounce/saliency *analogue* only. |
| Fuzzy green for oracle? | **Refuse.** |
| SoA / PID for v1? | **Refuse** (SoA always for domain graphs; PID for floor always; PID for concurrency only if simple caps fail later). |
| Safe contribution to dual-mode approve? | Decisions **25–28** strengthen the deterministic/probabilistic split; they do not unblock impl alone — still need taxonomy bar **13–24**. |
