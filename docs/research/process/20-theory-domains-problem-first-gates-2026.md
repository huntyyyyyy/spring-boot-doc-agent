---
title: Problem-FIRST theory domains A–H → quality gates (SoT vs sensor vs metaphor
  vs Refuse)
status: RESEARCH COMPLETE — informs synthesis; no code impl
date: '2026-08-10'
wave: dynamics-physical-computing
epic_seed: E-DYN1
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/research/process/05-dynamics-neuromorphic.md
- docs/research/process/44-formulas-concepts-dynamics-info-physical-2026-08-10.md
- docs/research/process/43-physical-info-dynamics-computing-2026-08-10.md
- docs/research/process/21-physical-unconventional-computing-2026.md
- docs/research/process/43-physical-info-dynamics-computing-2026-08-10.md
- docs/research/se-quality-synthesis-2026-08-08.md
- docs/research/coverage-quality/03-scientific-dimensions-metrics.md
- docs/design/coverage-measure-modes-design-2026-08-08.md
do_not:
- neuromorphic runtime
- fuzzy/PID green for fail_under
- SoA/ECS product rewrite
- mesh/Backstage theater
- invent arXiv IDs
last_reviewed: '2026-08-10'
---

# Problem-FIRST: theory domains A–H for doc-engine quality gates

Extends segment **05** (saliency / hysteresis / PID metaphors only). This memo asks, for each
classical theory domain: **what failure does the field exist to control**, what laws it names,
what it cannot do, and an **honest transfer** onto a Python CLI with deterministic gates
(`fail_under=98.7`, complexipy ≤5, LOC ≤225, claims checker). Constitution already **Refuses**
neuromorphic runtime, fuzzy/PID green, SoA/ECS rewrite, mesh/Backstage.

**Product:** `doc-engine` — not a continuous plant, not a physics simulator, not a K8s mesh.

**Transfer legend (column 4)**

| Label | Meaning for this product |
| --- | --- |
| **SoT** | May define or justify a boolean / hermetic gate predicate |
| **Sensor** | May inform advisory metrics, targeting, or climb feedback — never silent merge proof |
| **Metaphor-only** | Useful vocabulary for humans/agents; no new gate, no runtime |
| **Refuse** | Wrong category; do not schedule as architecture or SoT softener |

**Claim tiers:** `[Evidenced]` fetched/verified primary · `[Confirmed]` local seams · `[Unknown]` missing transfer proof or open product choice.

**Citation rule:** every arXiv ID below was fetched from `arxiv.org/abs/<id>` (or already verified in synthesis/05). Classic primaries are named by title/year. **No invented IDs.**

---

## 0. Cross-cutting verdict (read first)

| Question | Answer |
| --- | --- |
| Do A–H unlock new SoT gates? | **Almost never.** Existing SoT stays boolean predicates + hermetic corpora. |
| What transfers? | **Sensors** (diversity/uncertainty displays, rate caps, numerical stability of tools) and **metaphors** (attractors→stable green, observability→gate surface). |
| What is refused again? | Continuous dynamics / free-energy / PID / entropy as *replacements* for `fail_under`; neuromorphic; ECS/SoA; mesh/Backstage. |
| Category error #0 | Treating **Cover% time series** as a smooth dynamical system with Lyapunov/PID control is a **predicate→plant** category error (already decisions **25–28**). |

**Embody / Adopt / Refuse (product-level)**

| Stance | Items |
| --- | --- |
| **Embody** | Boolean oracle SoT; dual-mode climb as sensor; size soft/hard dual thresholds; linear-algebra substrate of numpy/scipy/cov math (implicit). |
| **Adopt** | Document A–H as *theory hygiene* next to 05; optional MI/entropy as *advisory* suite-diversity sensors (not floors); rate caps before any controller; condition-number awareness for numeric tooling only if profiled. |
| **Refuse** | Dynamical/thermodynamic/stat-mech “green confidence”; chaos/bifurcation runtimes; Landauer as CI SoT; network-controllability rewrites; PID/fuzzy floor; ECS/mesh. |

---

## A. Nonlinear dynamical systems (attractors, chaos, bifurcations, Lyapunov)

| Aspect | Content |
| --- | --- |
| **(1) Failure / problem** | Predict and classify long-term behavior of **nonlinear ODEs/maps** when linearization fails: sensitive dependence, sudden qualitative change (bifurcation), bounded but aperiodic motion (chaos). |
| **(2) Core invariants / laws (named)** | Lyapunov characteristic exponents (Oseledec multiplicative ergodic theorem); attractors / basins; bifurcation diagrams; sensitive dependence on initial conditions; Kaplan–Yorke / Lyapunov dimension (related). |
| **(3) Does NOT solve** | Discrete boolean acceptance of a software artifact; correctness of code; whether coverage ≥ 98.7; agent planning. Does not turn a CI log into a chaotic attractor without a *defined continuous state law*. |
| **(4) Transfer** | **Metaphor-only:** “basin of attraction” ≈ stable green under ratchet; “bifurcation” ≈ policy change that flips pass/fail. **Sensor:** none required for v1. **SoT:** none. **Refuse:** Lyapunov exponents on Cover% as gate softener; chaos-inspired neuromorphic/SNN runtimes (see 05). |
| **Embody/Adopt/Refuse** | **Refuse** as SoT/runtime · **Metaphor-only** for agent language · aligns 05 decisions 25–28. |
| **Citations** | `[Evidenced]` Skokos, *The Lyapunov Characteristic Exponents and their computation*, arXiv:**0811.0882**. `[Evidenced]` Wilkinson, *What are Lyapunov exponents, and why are they interesting?*, arXiv:**1608.02843**. Classic: Lyapunov (1892) *The General Problem of the Stability of Motion*; Lorenz (1963) *Deterministic Nonperiodic Flow*. |

---

## B. Dynamical systems theory (flows, stability, invariant sets)

| Aspect | Content |
| --- | --- |
| **(1) Failure / problem** | Describe continuous-time (or discrete-map) evolution \(\dot x = f(x)\) rigorously: existence/uniqueness of flows, stability of equilibria/orbits, invariant sets that trajectories cannot leave. |
| **(2) Core invariants / laws (named)** | Flow / semi-flow; Lyapunov stability / asymptotic stability; invariant sets; LaSalle invariance principle; Poincaré recurrence (conservative case); topological conjugacy. |
| **(3) Does NOT solve** | Spec→Implement→Verify process integrity; hermetic claim checking; mutation adequacy. Stability of an ODE ≠ stability of a merge gate. |
| **(4) Transfer** | **Metaphor-only:** invariant set ≈ “once oracle green + ratchets hold, stay green under allowed edits”; flow ≈ pipeline stage progression. **Sensor:** none as physics. **SoT:** none. **Refuse:** rewriting gates as continuous flows; SoA/ECS “state vector” product architecture (constitution). |
| **Embody/Adopt/Refuse** | **Refuse** continuous-state rewrite · **Metaphor-only** · **Embody** discrete invariant: oracle XML + fail_under as the only floor SoT `[Confirmed]`. |
| **Citations** | `[Evidenced]` Skokos arXiv:**0811.0882** (LCE as DST tool). Classic: Birkhoff *Dynamical Systems* (1927); Hirsch–Smale–Devaney *Differential Equations, Dynamical Systems, and an Introduction to Chaos* (textbook SoT for flows/stability vocabulary). |
| **Category error** | **A ⊂ B.** A is the nonlinear/chaos specialization of B. Scheduling “A stack” and “B stack” as separate product features doubles the same metaphor. |

---

## C. Information theory (Shannon entropy, mutual info, channel capacity, Kolmogorov complexity)

| Aspect | Content |
| --- | --- |
| **(1) Failure / problem** | Quantify **uncertainty**, **shared information**, and **compressible description length** for communication and coding — when naive bit counts mislead. |
| **(2) Core invariants / laws (named)** | Shannon entropy \(H(X)\); mutual information \(I(X;Y)\); channel capacity; source coding theorem; Kolmogorov complexity \(K(x)\) (algorithmic information — related but not Shannon). |
| **(3) Does NOT solve** | Semantic correctness; “is this claim true of the repo”; boolean floor predicates. High entropy ≠ high quality. Low Kolmogorov complexity ≠ good design (can be minified nonsense). |
| **(4) Transfer** | **Sensor (optional later):** suite diversity / redundancy heuristics inspired by MI (test-selection literature exists). **Metaphor-only:** channel capacity ≈ CI wall-clock / flake budget. **SoT:** **Refuse** entropy or MI thresholds as substitutes for fail_under / claims. Kolmogorov complexity of source: **Refuse** as gate (uncomputable in general; proxies are sensors at best). |
| **Embody/Adopt/Refuse** | **Adopt** only as documented advisory sensors if a spike proves value · **Refuse** as SoT · **Embody** nothing new today. |
| **Citations** | Classic: Shannon (1948) *A Mathematical Theory of Communication*. Classic: Kolmogorov (1965) *Three approaches to the quantitative definition of information*. `[Evidenced]` Papadopoulos & Psannis, *Information-Theoretic Measures in AI: A Survey and Practical Decision Framework*, arXiv:**2604.23716** (warns estimator misuse — relevant guardrail). Secondary SE (not required for ≥2): Androulakis et al. ACM SIGSOFT 2010 *Entropy and software systems…* (ACM; not arXiv). |

---

## D. Statistical mechanics (ensembles, free energy, phase transitions, fluctuation-dissipation)

| Aspect | Content |
| --- | --- |
| **(1) Failure / problem** | Connect microscopic degrees of freedom to macroscopic observables when \(N\) is huge: equilibrium ensembles, response to small perturbations, abrupt collective change (phase transition). |
| **(2) Core invariants / laws (named)** | Microcanonical / canonical / grand-canonical ensembles; Helmholtz/Gibbs free energy; partition function; fluctuation–dissipation theorem (FDT; Onsager–Kubo lineage); order parameters at phase transitions. |
| **(3) Does NOT solve** | Single-run deterministic CI predicates; one coverage.xml oracle. Ensemble average ≠ one boolean gate. |
| **(4) Transfer** | **Metaphor-only:** “phase transition” for sudden flake storms or policy flips. **Sensor:** multi-run flake rate / variance displays (already ops practice — not FDT). **SoT:** **Refuse** free-energy or FDT “confidence of green.” **Refuse** treating CI job matrix as a thermodynamic ensemble that softens fail_under. |
| **Embody/Adopt/Refuse** | **Refuse** as SoT · **Metaphor-only** · optional flake variance as **Sensor** without borrowing FDT equations. |
| **Citations** | `[Evidenced]` Marconi et al., *Fluctuation-Dissipation: Response Theory in Statistical Physics*, arXiv:**0803.0719**. `[Evidenced]` Corberi, Lippiello, Zannetti, *Fluctuation-Dissipation relations far from Equilibrium*, arXiv:**0707.0751**. Classic: Gibbs (1902) *Elementary Principles in Statistical Mechanics*. |

---

## E. Linear algebra (spectra, condition number, SVD, nullspace — computational substrate)

| Aspect | Content |
| --- | --- |
| **(1) Failure / problem** | Make finite-dimensional linear maps computable and stable: solve \(Ax=b\), compress, detect rank deficiency, quantify amplification of input error. |
| **(2) Core invariants / laws (named)** | Eigenvalues/spectra; singular value decomposition; rank–nullity; condition number \(\kappa(A)=\|A\|\|A^{-1}\|\) (2-norm: \(\sigma_{\max}/\sigma_{\min}\)); Eckart–Young optimality of truncated SVD. |
| **(3) Does NOT solve** | Software *process* quality; semantic gates; whether docs match code. Ill-conditioned numeric step ≠ “bad architecture” slogan. |
| **(4) Transfer** | **Embody (substrate):** already implicit in coverage aggregation, ranking, any scipy/numpy path — not a product rewrite. **Sensor:** condition/warnings if a numeric estimator is introduced (e.g. MI estimators). **SoT:** none for merge. **Refuse:** “spectral graph / SVD architecture” theater; SoA rewrite justified by BLAS folklore without a profiled hot loop (05 / taxonomy). |
| **Embody/Adopt/Refuse** | **Embody** as ambient math · **Adopt** numeric hygiene if/when sensors need it · **Refuse** LA-as-architecture. |
| **Citations** | `[Evidenced]` Zhang, *The Singular Value Decomposition, Applications and Beyond*, arXiv:**1510.08532**. Classic: Trefethen & Bau *Numerical Linear Algebra* (1997); Turing (1948) *Rounding-off errors in matrix processes*; Golub & Van Loan *Matrix Computations*. |

---

## F. Probability (measure, concentration, martingales, large deviations)

| Aspect | Content |
| --- | --- |
| **(1) Failure / problem** | Reason under uncertainty with axioms; bound how far sample means/estimators stray from expectations; describe rare-event rates. |
| **(2) Core invariants / laws (named)** | Kolmogorov probability axioms; concentration of measure (Hoeffding, Azuma–Hoeffding, McDiarmid); martingale convergence; large-deviation rate functions (Cramér–Chernoff). |
| **(3) Does NOT solve** | Replacing a hermetic oracle with a probabilistic “likely green.” Concentration bounds need a well-specified random model — CI noise is often adversarial/non-i.i.d. |
| **(4) Transfer** | **Sensor:** flake / retry statistics; confidence intervals on *advisory* metrics (e.g. estimated suite diversity) if modeled honestly. **Metaphor-only:** “large deviation” for rare catastrophic CI failures. **SoT:** **Refuse** probabilistic softeners of fail_under. Climb Cover% remains a **different predicate** (synthesis / pytest-cov trap) — not a concentration estimator of the oracle. |
| **Embody/Adopt/Refuse** | **Embody** deterministic SoT · **Adopt** honest uncertainty language on sensors · **Refuse** martingale/PID green. |
| **Citations** | `[Evidenced]` Raginsky & Sason, *Concentration of Measure Inequalities in Information Theory, Communications and Coding*, arXiv:**1212.4663**. `[Evidenced]` Sason, *On Refined Versions of the Azuma-Hoeffding Inequality…*, arXiv:**1111.1977**. Classic: Kolmogorov *Foundations of the Theory of Probability*; Hoeffding (1963); Azuma (1967). |

---

## G. Thermodynamics (1st/2nd law, irreversibility, Landauer principle)

| Aspect | Content |
| --- | --- |
| **(1) Failure / problem** | Constrain energy/entropy exchange for physical processes; explain irreversibility; bound minimum heat of logically irreversible bit erasure (Landauer). |
| **(2) Core invariants / laws (named)** | First law (energy balance); second law (entropy of isolated system non-decreasing); Clausius inequality; Landauer bound \(\langle W\rangle \ge k_B T \ln 2\) per bit erased (idealized). |
| **(3) Does NOT solve** | Whether a PR may merge; documentation fidelity; coverage floors. Macroscopic CI machines sit many orders of magnitude above Landauer — bound is not an ops knob. |
| **(4) Transfer** | **Metaphor-only:** irreversible baseline edits; “don’t erase SoT casually.” **Sensor:** wall-clock / compute cost of remesure (Green AI efficiency as *criterion*, not floor) — already synthesis cites Green AI. **SoT:** **Refuse** Landauer or 2nd-law rhetoric as gate policy. **Refuse** neuromorphic “thermodynamic computing” runtime. |
| **Embody/Adopt/Refuse** | **Refuse** thermo-SoT · **Adopt** cost/saliency cadence metaphors (05) · **Embody** decision 5 remesure policy. |
| **Citations** | Classic: Landauer (1961) *Irreversibility and Heat Generation in the Computing Process*. Classic: Bennett (1982) *The thermodynamics of computation—a review*. `[Evidenced]` Chattopadhyay et al., *Landauer Principle and Thermodynamics of Computation*, arXiv:**2506.10876**. `[Evidenced]` Buffoni, Coghi, Gherardini, *Generalized Landauer bound from absolute irreversibility*, arXiv:**2310.05449**. Related efficiency (not thermo law): `[Evidenced]` Schwartz et al., *Green AI*, arXiv:**1907.10597**. |

---

## H. Control theory (feedback, observability, controllability, robust control — beyond PID)

| Aspect | Content |
| --- | --- |
| **(1) Failure / problem** | Drive a dynamical system to a desired trajectory/state despite limited actuators/sensors and model uncertainty — decide *what can be steered* and *what can be inferred*. |
| **(2) Core invariants / laws (named)** | Feedback; Kalman controllability rank / Hautus test; observability duality; stabilizability / detectability; robust control (uncertainty sets, margins); separation principle (LQG lineage). PID is one *controller form*, not the field. |
| **(3) Does NOT solve** | Defining the *reference* itself when the reference is a boolean SoT. Controllability of a K8s queue ≠ legitimacy of softening 98.7. |
| **(4) Transfer** | **Metaphor-only:** observability ≈ “gates surface the state that matter”; controllability ≈ “agents can act on failing files.” **Sensor / Adopt (narrow):** rate limits, concurrency caps, hysteresis on *targeting* (05) — discrete ops control, not continuous Cover% PID. **SoT:** **Refuse** PID/robust-control error \(e(t)=98.7-\mathrm{Cover\%}\) as pass criterion. **Refuse** complex-network controllability rewrite of the CLI (mesh theater adjacent). |
| **Embody/Adopt/Refuse** | **Embody** boolean reference + discrete ratchets · **Adopt** simple caps/hysteresis · **Refuse** floor-as-plant (05 / decisions 25–28) · **Refuse** mesh/Backstage. |
| **Citations** | Classic: Kalman (1960/1963) controllability/observability. `[Evidenced]` Nguyen, *A short introduction to the control theory in finite-dimensional spaces*, arXiv:**2505.02423**. `[Evidenced]` Liu & Barabási, *Control Principles of Complex Networks*, arXiv:**1508.05384** (network controllability — **Refuse transfer** to doc-engine architecture). `[Evidenced]` Simon et al., *Parsimonious Edge Computing…* (PID microservice scaling), arXiv:**2109.02514** — domain = queue length, **not** coverage (05). |

---

## Master transfer table (A–H)

| Domain | SoT | Sensor | Metaphor-only | Refuse |
| --- | --- | --- | --- | --- |
| **A** Nonlinear DS | — | — | basins / bifurcations language | LCE/chaos runtime; Cover% Lyapunov softener |
| **B** DST flows | — | — | invariant set ≈ ratchet lock | continuous-state / ECS rewrite |
| **C** Info theory | — | optional MI/entropy diversity | channel = CI budget | entropy/MI/Kolmogorov as fail_under |
| **D** Stat mech | — | flake variance (ops, not FDT) | “phase change” jargon | free-energy / FDT green |
| **E** Linear algebra | — | numeric κ warnings if needed | — | SVD/SoA architecture theater |
| **F** Probability | — | CIs on advisory metrics | rare-event language | probabilistic fail_under |
| **G** Thermo / Landauer | — | remesure cost / Green AI efficiency | irreversibility of baseline edits | Landauer as CI SoT; thermo computers |
| **H** Control | boolean *reference* stays SoT (not from H) | rate caps, targeting hysteresis | observability/controllability vocabulary | PID/robust Cover% plant; network-control mesh |

---

## Category errors (explicit)

| Error | Why it is wrong here |
| --- | --- |
| **Predicate → plant** | Mapping `fail_under` gap to \(e(t)\) for PID/robust control confuses a **boolean SoT** with a **regulated continuous output** (05, synthesis 25). |
| **A vs B as two products** | Nonlinear DS is a specialization of DST; duplicate “dynamics stacks” are taxonomy theater. |
| **Ensemble → one oracle** | Stat-mech ensembles average many microstates; `coverage.xml` is one hermetic artifact (policy 16-A). |
| **Shannon H → quality** | Entropy measures uncertainty/diversity, not correctness or floor compliance (C). |
| **Landauer → merge policy** | Physical bit-erasure bound does not license or forbid PR merge (G). |
| **Network controllability → CLI architecture** | Liu–Barabási network control assumes dynamical node states on graphs — not AST/doc pipelines (H). |
| **Climb Cover% → oracle estimator** | Scoped `--cov` is a **different predicate**, not a concentration estimator of whole-repo 98.7 (synthesis). |
| **Neuromorphic / SoA / mesh** | Already constitution-refused; citing SpikeSlicer or SoA papers does not reopen them (05). |

---

## Unknowns (honest)

| ID | Unknown | Why it matters |
| --- | --- | --- |
| U1 | Whether MI-based suite-diversity sensors beat simpler set-cover / mutation proxies **in this repo** | Block **Adopt** of C-sensors until a spike with exit criterion; default stay Refuse-as-SoT. |
| U2 | Whether flake processes are well-modeled enough for Azuma/Hoeffding-style bounds | Without a model, probability tools stay Metaphor-only. |
| U3 | Profiled numeric hot path needing κ/SVD hygiene | Until profiled, E stays substrate Embody only — no SoA rewrite. |
| U4 | Job-concurrency plant (queue depth) ever needing more than rate caps | 05 leaves PID-for-concurrency as later Unknown; still **never** for Cover% floor. |
| U5 | DeepWiki / popular secondary “thermo computing for CI” pages | Treat as `[Unknown]` / hype unless primary IDs verify — do not invent. |

---

## Relation to segment 05 & synthesis

| Prior decision | This memo |
| --- | --- |
| 25 Hard predicates stay hard | Reinforced by A/B/D/F/H Refuse of continuous softeners |
| 26 Saliency / debounce remesure | G/H support cost-aware cadence as Metaphor/Adopt, not Landauer SoT |
| 27 Hysteresis on advisory/targeting only | H Adopt narrow; still not oracle |
| 28 SoA / neuromorphic / PID theater refused | Reaffirmed; A–H do not reopen |
| Policy 16-A climb artifact path | Untouched — climb remains sensor/derived |

**No new Spec gate.** No implementation. Optional future spike only for U1 (MI diversity sensor) with explicit non-SoT acceptance.

---

## One-page adversarial checklist

- [ ] Any proposal uses Lyapunov / free energy / Landauer / MI / PID as **merge SoT**? → reject.
- [ ] Any proposal cites an arXiv ID not fetchable on abs? → mark Unknown; do not invent.
- [ ] Any proposal conflates climb Cover% with oracle fail_under? → reject (pytest-cov trap).
- [ ] Any proposal schedules ECS/SoA/mesh/Backstage/neuromorphic from these domains? → reject.
- [ ] Any “control” change first tries **rate caps + hysteresis on targeting**? → required before controllers.
- [ ] Linear algebra invoked as **architecture** rather than numeric substrate? → reject.

---

## References (verified IDs only + classics)

**arXiv (fetched 2026-08-10 unless noted prior-verified in synthesis/05):**

| ID | Title |
| --- | --- |
| 0811.0882 | Skokos — *The Lyapunov Characteristic Exponents and their computation* |
| 1608.02843 | Wilkinson — *What are Lyapunov exponents, and why are they interesting?* |
| 2604.23716 | Papadopoulos & Psannis — *Information-Theoretic Measures in AI…* |
| 0803.0719 | Marconi et al. — *Fluctuation-Dissipation: Response Theory in Statistical Physics* |
| 0707.0751 | Corberi et al. — *Fluctuation-Dissipation relations far from Equilibrium* |
| 1510.08532 | Zhang — *The Singular Value Decomposition, Applications and Beyond* |
| 1212.4663 | Raginsky & Sason — *Concentration of Measure Inequalities…* |
| 1111.1977 | Sason — *On Refined Versions of the Azuma-Hoeffding Inequality…* |
| 2506.10876 | Chattopadhyay et al. — *Landauer Principle and Thermodynamics of Computation* |
| 2310.05449 | Buffoni et al. — *Generalized Landauer bound from absolute irreversibility* |
| 1907.10597 | Schwartz et al. — *Green AI* (prior synthesis) |
| 2505.02423 | Nguyen — *A short introduction to the control theory in finite-dimensional spaces* |
| 1508.05384 | Liu & Barabási — *Control Principles of Complex Networks* |
| 2109.02514 | Simon et al. — *Parsimonious Edge Computing…* (PID scaling; prior 05) |
| 2410.02249 | SpikeSlicer (prior 05; neuromorphic CV — Refuse transfer) |

**Classics:** Shannon 1948; Kolmogorov 1965; Lyapunov 1892; Lorenz 1963; Gibbs 1902; Landauer 1961; Bennett 1982; Kalman 1960/63; Turing 1948; Trefethen & Bau 1997; Hoeffding 1963; Azuma 1967.

**Local:** `docs/research/process/05-dynamics-neuromorphic.md`; `docs/research/se-quality-synthesis-2026-08-08.md`; decisions 25–28; policy 16-A.

---

## Segment verdict

| Question | Answer |
| --- | --- |
| Problem-FIRST across A–H done? | **Yes** — tables above. |
| New SoT from physical theory? | **No.** |
| Safe Embody/Adopt? | Metaphor hygiene + optional future non-SoT sensors (U1); rate caps (H). |
| Refuse list grown? | Explicit master table; no reopen of 05 constitution refuses. |
