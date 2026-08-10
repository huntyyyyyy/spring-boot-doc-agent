---
title: Problem-first — dynamical systems, information/thermo, physical & unconventional computing
status: RESEARCH — deepens process/05; Spec seed E-DYN1 (metaphor hygiene only)
date: 2026-08-10
epic_seed: E-DYN1
claim_tiers: Evidenced / Confirmed / Unknown
supersedes_partial: docs/research/process/05-dynamics-neuromorphic.md
related:
  - docs/research/process/05-dynamics-neuromorphic.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
  - docs/research/process/42-problem-first-rag-ds-cli-2026-08-10.md
do_not:
  - neuromorphic / molecular / ionic / RD / memristor tip runtime
  - fuzzy / PID / free-energy as fail_under softener
  - SoA/ECS/DOD rewrite of doc_engine
  - treat physical RC accuracy as merge SoT
spec_gate: DRAFT E-DYN1 — research + metaphor hygiene; no Implement of physical substrates
---

# Problem-first: dynamics, information, thermo, and physical computing

**Question.** These fields are *real science* built to solve *physical and mathematical
problems*. What failure modes do they address? Which invariants matter? What
honest transfer (if any) exists for a **Python CLI** with boolean gates
(`fail_under=98.7`), climb sensors, and Stage-0 structure facts — vs category
error / theater?

**Prior.** Segment [`05-dynamics-neuromorphic`](05-dynamics-neuromorphic.md) already
locked decisions **25–28**: hard predicates stay hard; saliency→debounce;
hysteresis on advisory only; refuse SoA/neuromorphic/PID-as-floor. This memo
**deepens** the problem inventory across theory + unconventional computing
without reopening those refuses.

**Lattice.** Sensor ≠ SoT · Metaphor ≠ runtime · Physical substrate ≠ CI predicate ·
Derived ≠ LWW · Human review floor.

```text
FIELD EXISTS TO EXPLAIN/CONTROL X
        │
        ├─ Exact math/physics SoT in its domain
        ├─ Transferable ENGINEERING ANALOGUE (sensor / process)
        └─ Category error if imported as tip SoT / gate softener
```

---

## 0. One-page verdict

| Cluster | Core problem the field solves | Transfer to doc-engine |
| --- | --- | --- |
| **Nonlinear / dynamical systems** | Predict long-term behavior of evolving state; stability vs chaos | **Metaphor:** thrash/bifurcation of tip process. **Refuse** as gate plant |
| **Information theory** | Quantify uncertainty, channel limits, compressibility | **Adopt** Shannon-style *honesty*: distinguish signal from noise in sensors; **Refuse** entropy score as merge SoT |
| **Statistical mechanics / thermo** | Collective behavior from micro laws; irreversibility & work bounds | **Adopt** Landauer/Wolpert *cost of erasure* as Green-AI *language* only; **Refuse** kT ln2 as CI floor |
| **Linear algebra / probability** | Represent transforms; quantify uncertainty & concentration | **Embody** already (matrices in scanners; concentration≈flake rates). Not exotic |
| **Control theory** | Make systems track references despite disturbance | **Adopt** rate caps / observability of CI jobs; **Refuse** Cover% as PID plant (05 / 2109.02514) |
| **Molecular / far-from-eq chem / RD / ionic** | Compute with chemistry / ions when digital von Neumann is wrong shape | **Refuse** tip substrate; optional **metaphor** for parallel search / dissipative “work” |
| **Neuromorphic / PRC / analog / in-memory** | Escape von Neumann bottleneck; exploit physics for temporal/energy | **Refuse** tip runtime; **Adopt** only saliency/debounce & “reservoir→linear readout” *pattern* as climb→oracle split analogy |

**Epic `E-DYN1`:** freeze metaphor-hygiene table; no physical-computing Implement.

---

## 1. Theory domains — problem → invariant → transfer

### 1.1 Nonlinear dynamical systems & DST

| | |
| --- | --- |
| **Failure before** | Linear intuition fails: small parameter changes → qualitative jumps; long-term prediction collapses |
| **Job / invariants** | Flows on manifolds; equilibria; Lyapunov stability; attractors; bifurcations; Lyapunov exponents (avg expansion rates) `[Evidenced]` e.g. continuity via LDT `[2110.10265]`, `[2210.14851]` |
| **Does NOT solve** | What *should* be true (normative SE); discrete boolean SLOs |
| **Transfer** | **Metaphor:** tip thrash ≈ unstable orbit; Spec gate ≈ stabilizing feedback. **Refuse:** treating Cover% trajectory as chaotic plant to “control into” 98.7 |

### 1.2 Information theory

| | |
| --- | --- |
| **Failure before** | No principled measure of uncertainty, redundancy, or channel limit |
| **Job / invariants** | Shannon entropy \(H\); mutual information; channel capacity; Kolmogorov complexity (algorithmic) |
| **Does NOT solve** | Truth of a claim; merge authority |
| **Transfer** | **Adopt:** label sensors vs SoT (information *about* quality ≠ quality predicate). **Refuse:** MI/entropy dashboards as fail_under. Parallel to RAGAS≠merge |

### 1.3 Statistical mechanics

| | |
| --- | --- |
| **Failure before** | Microscopic laws don’t explain macroscopic phases / fluctuations |
| **Job / invariants** | Ensembles; free energy; phase transitions; fluctuation–dissipation |
| **Does NOT solve** | Software correctness predicates |
| **Transfer** | **Metaphor:** “phase change” when a gate flips from soft advisory→hard fail. **Refuse:** free-energy minimization as architecture SoT |

### 1.4 Linear algebra (computational substrate)

| | |
| --- | --- |
| **Failure before** | Cannot represent/solvesystems of constraints, spectra, compressions |
| **Job / invariants** | Rank, nullspace, eigenvalues, SVD, condition number |
| **Does NOT solve** | Whether a citation supports a claim |
| **Transfer** | **Embody:** already the language of scanners, embeddings (as sensors), numerical checks. Ill-conditioning ≈ fragile thresholds — document, don’t soft-gate |

### 1.5 Probability

| | |
| --- | --- |
| **Failure before** | Deterministic models hide rare events & sampling error |
| **Job / invariants** | Measures; concentration; martingales; large deviations |
| **Does NOT solve** | Replacing a failed boolean gate with “high probability green” |
| **Transfer** | **Adopt:** flake budgets / concentration language for *campaign sensors*. **Refuse:** probabilistic pass of oracle floor |

### 1.6 Thermodynamics (incl. computation)

| | |
| --- | --- |
| **Failure before** | No bound linking logical irreversibility to physical cost |
| **Job / invariants** | 1st/2nd law; Landauer bound \(k_B T\ln 2\) per bit erased `[Evidenced]` review arXiv:2506.10876; stochastic thermo of computation Wolpert `[1905.05669]` |
| **Does NOT solve** | Which tests to run; citation support |
| **Transfer** | **Adopt (language):** Green-AI / remesure *cost* (synthesis decision **23/31** already). **Refuse:** Landauer as CI threshold; “erase coverage debt” thermo theater |

### 1.7 Control theory (beyond PID autoscaling)

| | |
| --- | --- |
| **Failure before** | Open-loop systems can’t reject disturbance or track reference |
| **Job / invariants** | Feedback; controllability/observability; robust / H∞ control |
| **Does NOT solve** | Defining the reference (SLO) itself |
| **Transfer** | **Embody:** boolean feedback (fail→fix→remeasure). **Adopt:** observability of CI (receipts, dual sink); rate limits before fancy controllers. **Refuse:** Cover% error \(e(t)\) under PID (05; `[2109.02514]` domain = queues) |

---

## 2. Physical / unconventional computing — problem → substrate → transfer

### 2.1 Inventory

| ID | Failure before the approach | What the substrate claims | Does NOT solve for doc-engine | Layer |
| --- | --- | --- | --- | --- |
| **M1 Molecular / DNA** | Digital serial search costly for some combinatorial encodings | Massive parallelism in molecular ops (Adleman 1994 Hamiltonian path) `[Evidenced — Science 266:1021]` | CI boolean gates; citation SoT | **Refuse** runtime |
| **M2 Far-from-eq chemistry** | Equilibrium chemistry can’t sustain structure / work continuously | Dissipative structures; self-organizing CRNs as compute (formose RC, Nature 2024) `[Evidenced — doi:10.1038/s41586-024-07567-x]` | Merge predicates | **Refuse**; metaphor: dissipative “work budget” |
| **M3 Ionic / iontronic** | Electron CMOS ≠ wet/soft bio interface | Ions as carriers for logic/memory | Python CLI correctness | **Refuse** |
| **M4 Neuromorphic** | Clocked von Neumann energy/latency for event streams | Event-driven ASICs (Loihi, BrainScaleS); SNNs; SpikeSlicer `[2410.02249]` | pytest-cov SoT | **Refuse** runtime; **Adopt** saliency debounce only (05) |
| **M5 Physical reservoir computing** | Training full RNNs hard; want physics as random feature map | Fixed nonlinear dynamics + linear readout (Jaeger ESN 2001; Maass LSM 2002; memristor RC `[2403.01827]`, `[2310.16331]`; ferrofluid IMC `[2211.08152]`) | Gate truth | **Refuse** hardware; **Adopt pattern only**: fixed rich transform → trained/linear *readout* ≈ climb features → oracle boolean |
| **M6 Analog neural nets** | Discrete digital rounding / clock for continuous dynamics | Continuous-time ODEs as networks | Reproducible CI hermeticity | **Refuse** as tip SoT (non-hermetic) |
| **M7 In-memory neural** | von Neumann bottleneck (data movement energy) | Memristor/crossbar multiply-accumulate in place | Citation / coverage predicates | **Refuse** |
| **M8 Reaction kinetics** | Need law of rates for concentration trajectories | Mass-action ODEs as dynamical “programs” | Spec Approve | **Refuse**; kinetics≈process rates metaphor only |
| **M9 Reaction–diffusion computing** | Spatial pattern / parallel wave compute hard on serial CPUs | BZ / RD media as spatial processors | Hermetic CI | **Refuse** |

### 2.2 DeepWiki / Create hygiene

- **Evaluate** physical RC & DNA computing as *domain-correct* for materials/wet labs.
- **Create for us:** a **metaphor register** in research SoR (this memo) — not a Loihi driver, BZ simulator, or memristor dep in `doc_engine`.

---

## 3. Honest engineering analogues (only these)

| Physics / info idea | Allowed analogue in doc-engine | Stance |
| --- | --- | --- |
| Event saliency / spike gating | Remesure oracle on salient triggers only | **Adopt** (05 / decision 26) |
| Hysteresis / bistable switch | Soft vs hard size bands; climb file dead-band | **Adopt** (decision 27) |
| Reservoir → linear readout | Climb/sensors explore; oracle is the boolean readout | **Metaphor** (M5); never invert |
| Channel capacity / noise | Dual sink: human narrative vs machine receipt; don’t overload CI logs | **Adopt** (E-OAS0 family) |
| Landauer / work cost | Prefer fewer full-oracle runs; Green-AI language | **Adopt** language (23/31) |
| Observability | Structured receipts, campaign matrices | **Adopt** |
| Lyapunov / chaos | Tip thrash detection (process stalker G5) | **Metaphor** |
| Concentration / LDT | Flake rate bounds as *sensors* | **Adopt** language |
| Phase transition | Soft advisory → hard fail threshold | **Metaphor** already embodied |

**Everything else in §1–2:** **Refuse** as tip SoT / runtime / gate softener.

---

## 4. Adversarial packet

| # | Attack | Response |
| --- | --- | --- |
| A1 | “Use free energy / Landauer to set coverage policy” | Wrong units; boolean SLO ≠ \(kT\ln2\) |
| A2 | “Physical RC beat ESN on Mackey–Glass — ship memristor CI” | Domain success ≠ product category; hermeticity/repro fail |
| A3 | “DNA computing parallelizes Stage-0” | Adleman solves combinatorial wet-lab instances; not ast-grep |
| A4 | “Analog NN more expressive for claim support” | Non-hermetic; citation needs discrete structure SoT |
| A5 | “Ionic/neuromorphic is the future — refuse is Luddite” | Refuse is *category* for *this* Python CLI tip — not a claim the science is false |
| A6 | “Control theory ⇒ PID the Cover% error” | Already refused (05 / synthesis); plant is wrong |

---

## 5. Embody / Adopt / Refuse (locked for E-DYN1)

| Stance | Content |
| --- | --- |
| **Embody** | Boolean oracle SoT; climb as sensor; decisions **25–28**; AoS/OO domain graphs; saliency remesure cadence |
| **Adopt** | Metaphor register (§3); Green-AI cost language; observability/rate caps; reservoir→readout *analogy* for climb→oracle (docs only) |
| **Refuse** | Neuromorphic/molecular/ionic/RD/memristor/analog tip deps; fuzzy/PID/free-energy/entropy as fail_under; SoA/ECS rewrite; physical RC accuracy as merge proof |

---

## 6. Epic seed — E-DYN1

| Field | Content |
| --- | --- |
| **Goal** | Extend 05 with problem-first depth; lock metaphor hygiene; prevent tip thrash into physical computing |
| **DYN1-1** | Spec: Approve §3 analogues + §5 Refuse table | Acceptance: `spec_gate: APPROVED E-DYN1` |
| **DYN1-2** | Docs: one CONTRIBUTING sentence — “physics metaphors ≠ gate softeners” | After Approve |
| **DYN1-3** | Spike: none required for substrates | Exit: Explicit Defer physical RC/DNA/ionic indefinitely unless product category changes |
| **Exit** | Approve recorded; backlog P20; no Implement |
| **Invariants** | fail_under 98.7; complexipy ≤5; LOC ≤225; policy 16-A; refuse neuromorphic tip |

---

## 7. Source index (selected)

**Dynamics / info / thermo / control.** Lyapunov LDT continuity `[2110.10265]`, `[2210.14851]` · Landauer / thermo of computation `[2506.10876]`, Wolpert `[1905.05669]` · PID edge scaling `[2109.02514]` · SpikeSlicer `[2410.02249]` · FlexGuard `[2602.23636]` · Green AI `[1907.10597]` (synthesis).

**Physical / unconventional.** Adleman DNA computing (Science 1994) · Formose chemical reservoir (Nature 2024, doi:10.1038/s41586-024-07567-x) · Memristor RC `[2403.01827]`, `[2310.16331]` · Ferrofluid in-memory `[2211.08152]` · ESN/LSM lineage (Jaeger 2001; Maass 2002; review arXiv:2504.11757).

**Local.** `05-dynamics-neuromorphic.md` · synthesis decisions **22, 25–28, 23/31**.

---

## 8. Session note

Research SoR for **problem framing and transfer hygiene**. Stars/hardware demos do not reopen tip SoT. Prefer Spec → (docs only) → Archive. One tip stream — do not thrash vs E-COH1 / E-PROB0 without handoff.
