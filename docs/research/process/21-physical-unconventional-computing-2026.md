---
title: Physical / unconventional computing — Problem-FIRST transfer bar for doc-engine
status: RESEARCH COMPLETE — informs process hygiene; no code impl
research date: 2026-08-10
wave: dynamics-physical
claim tiers: Evidenced / Confirmed / Unknown
related:
  - docs/research/process/05-dynamics-neuromorphic.md
  - docs/research/process/43-physical-info-dynamics-computing-2026-08-10.md
  - docs/research/process/20-theory-domains-problem-first-gates-2026.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/design/coverage-measure-modes-design-2026-08-08.md
epic_ids: [E-DYN1]
do_not:
  - promote physical/neuromorphic tip as coverage or gate SoT
  - soft-replace fail_under with dissipative / reservoir / analog “green”
  - schedule Loihi/BrainScaleS/DNA/BZ runtimes inside doc_engine
---

# Segment 21: Physical & unconventional computing (domains A–I)

> **Problem-FIRST.** These domains are real science. Transfer into a Python CLI with
> boolean gates (`fail_under=98.7`, complexipy ≤5, size ≤225, claims checker) is
> almost always **metaphor** or **Refuse**. Extends
> [`05-dynamics-neuromorphic`](05-dynamics-neuromorphic.md) beyond SpikeSlicer
> metaphors; does **not** reopen decisions **25–28** (hard predicates, no fuzzy/PID
> tip SoT).
>
> **Companion memos:** umbrella E-DYN1 framing + theory clusters live in
> [`43`](43-physical-info-dynamics-computing-2026-08-10.md); classical theory A–H
> scorecards in [`20`](20-theory-domains-problem-first-gates-2026.md). This file is
> the **deep substrate scorecard** (A–I) with primary papers + GitHub stars.

**Claim tiers:** `[Evidenced]` primary paper/docs · `[Confirmed]` local seams ·
`[Unknown]` missing ID, hype transfer, or product choice still open.

**Legend:** **Embody** = already true here · **Adopt** = take next (docs/process only)
· **Refuse** = wrong shape for this product · **Metaphor** = useful language only,
never a gate predicate · **Sensor** = advisory/derived signal · **SoT** = boolean
oracle / ratchet that may fail the build.

**Product frame:** `doc-engine` is a deterministic documentation / Stage-0 / CI CLI —
not a wet lab, not an ASIC farm, not a von Neumann–bottleneck research chip.

---

## 0. Problem inventory (before any substrate)

| # | Failure / problem in *this* product class | Wrong “physical” leap |
| --- | --- | --- |
| P1 | Agents remesure expensive whole-repo oracle on every micro-edit | “Event-driven ASIC / saliency chip” as runtime |
| P2 | Climb Cover% (or fuzzy score) sold as proof of 98.7 | Reservoir / dissipative / analog “soft green” as tip SoT |
| P3 | Flapping advisory targeting (re-pick same file every 0.01%) | Hysteresis memristor as gate softener |
| P4 | Need reproducible CI on commodity runners | Analog drift, wet chemistry, device variation as “CI backend” |
| P5 | Boolean predicates must be decidable and claim-checkable | Continuous-time / far-from-equilibrium tip as oracle |
| P6 | LOC / complexipy / PathCohesion are discrete ratchets | Pattern-formation or CRN kinetics as size SoT |
| P7 | Research theater dilutes Spec→Impl→Verify | “Adopt Loihi / DNA / BZ” without an engineering analogue |

**North-star filter:** If the substrate’s *value proposition* is energy, latency, or
wet/analog physics under non-ideal devices, it does **not** solve P4–P6. Only
*process analogues* (debounce ≈ saliency; dead-band ≈ flap detection) touch P1–P3 —
already covered in segment **05**.

---

## 1. Cross-cutting SoT vs sensor vs metaphor vs Refuse

| Layer | Meaning for doc-engine | Physical-computing transfer |
| --- | --- | --- |
| **SoT** | Boolean / discrete gate (`fail_under`, size, complexipy, claims) | **Never** a physical tip. `[Confirmed]` decisions **25**, **16-A** |
| **Sensor** | Climb Cover%, gap-average, advisory bands | May *resemble* reservoir readouts (cheap projection → linear decision) **only as metaphor** |
| **Metaphor** | Debounce, hysteresis, rate caps, “fire on salient events” | Allowed in CONTRIBUTING / agent prompts when tied to P1–P3 |
| **Refuse** | Runtime, hardware port, chemical/ASIC dependency, fuzzy tip SoT | Default for A–I substrates |

---

## 2. Domain scorecards (A–I)

Each domain: (1) failure before the approach · (2) what the substrate claims to compute ·
(3) what it does **not** solve for this CLI · (4) SoT/sensor/metaphor/Refuse ·
(5) ≥2 primary papers + ≥1 GitHub when it exists.

### A. Molecular / DNA computing / molecular information processing

| Aspect | Finding |
| --- | --- |
| (1) Problem (domain) | Digital CMOS cannot cheaply exploit massive molecular parallelism / dense archival DNA storage; wet lab wants programmable chemistry without custom enzymes for every gate. |
| (2) Substrate claim | DNA strand displacement (DSD) and strand cascades implement Boolean / cascade logic and, via CRN compilation, approximate programmed kinetics; DNA storage + in-memory strand ops can run parallel molecular algorithms (e.g. Rule 110). |
| (3) Not for CLI | Does not give reproducible pytest-cov, hermetic CI, or claim-checkable predicates. Latency is chemical (seconds–hours), not CI seconds. |
| (4) Stance | **Refuse** runtime / wet deps. **Metaphor only** if someone says “massive parallel search” — still not a gate. **SoT:** none. |
| (5) Sources | Adleman, *Molecular Computation of Solutions to Combinatorial Problems*, Science **266**, 1021 (1994) `[Evidenced]`. Soloveichik, Seelig & Winfree, *DNA as a universal substrate for chemical kinetics*, PNAS **107**, 5393 (2010) `[Evidenced]`. Qian & Winfree, *Scaling Up Digital Circuit Computation with DNA Strand Displacement Cascades*, Science (2011) / related Nature cascade NN work `[Evidenced]`. Wang et al., *Parallel molecular computation on digital data stored in DNA*, PNAS (2023) `[Evidenced]`. GitHub: domain tools are niche (e.g. `DNA-and-Natural-Algorithms-Group/peppercornenumerator` ~10★) — **no** excellent high-star product repo that maps to CI gates `[Evidenced]` stars · transfer **Refuse**. |

### B. Far-from-equilibrium chemistry (dissipative structures, Prigogine; CRNs)

| Aspect | Finding |
| --- | --- |
| (1) Problem (domain) | Equilibrium chemistry relaxes to boring steady states; life-like computation / self-organization needs continuous energy throughput (open systems). |
| (2) Substrate claim | Dissipative structures and driven CRNs sustain oscillations, bistability, and information-bearing fluxes; thermodynamic bounds relate dissipation to accessible concentration space. |
| (3) Not for CLI | “Keep the build far from equilibrium” is poetry. Oracle pass/fail is **not** an entropy-production plant. |
| (4) Stance | **Refuse** as SoT. **Metaphor:** continuous energy cost of *keeping* quality (CI always-on) ≠ softening the floor. Optional **sensor** language only for “don’t burn remesure budget” (already rate-cap metaphor in **05**). |
| (5) Sources | Prigogine / Glansdorff–Prigogine dissipative-structure program (classic) `[Evidenced]` domain. Dal Cengio et al., *Thermodynamic Space of Chemical Reaction Networks*, arXiv:**2407.11498** `[Evidenced]`. Baltussen et al., *Chemical reservoir computation in a self-organizing reaction network* (formose), Nature **631**, 549 (2024) `[Evidenced]`. Companion code: `huckgroup/Formose_reservoir_computation` (~6★ — paper artifact, not a CI framework) `[Evidenced]`. |

### C. Ionic / iontronic / electrolyte computing

| Aspect | Finding |
| --- | --- |
| (1) Problem (domain) | Solid-state neuromorphic still uses electrons; brain uses ions in water — bio-interface and multimodal (elec/chem/mech) synapses are hard in CMOS alone. |
| (2) Substrate claim | Fluidic nanochannels / conical pores act as volatile memristors via salt concentration polarization; networks can do reservoir-style classification and multimodal physical learning. |
| (3) Not for CLI | No electrolyte in GitHub Actions. Device timescales and drift ≠ boolean cov XML. |
| (4) Stance | **Refuse** hardware. Honest **metaphor** only: ionic *hysteresis* ≈ flap detection / dead-band (Nagios-style) — **Adopt** already in **05**/**27**, not via iontronics libs. |
| (5) Sources | Kamsma et al., *Brain-inspired computing with fluidic iontronic nanochannels*, arXiv:**2309.11438** / PNAS (2024) `[Evidenced]`. Kamsma et al., *Iontronic Neuromorphic Signaling with Conical Microfluidic Memristors*, PRL **130**, 268401 (2023) `[Evidenced]`. *Multimodal Physical Learning in Brain-Inspired Iontronic Networks*, arXiv:**2511.04209** `[Evidenced]`. Excellent general-purpose GitHub for *iontronic CI*: **absent** `[Unknown]` / N/A — research code only. |

### D. Neuromorphic computing (beyond SpikeSlicer — Loihi, BrainScaleS, event ASICs)

| Aspect | Finding |
| --- | --- |
| (1) Problem (domain) | Dense ANN inference on von Neumann CPUs/GPUs wastes energy on sparse, event-like, real-time sensory workloads; need spike routing + local learning at low power. |
| (2) Substrate claim | Digital (Loihi) and analog/hybrid (BrainScaleS-2) chips emulate SNNs with event-driven communication; NeuroBench aims to benchmark algorithms/systems fairly. |
| (3) Not for CLI | pytest-cov is batch, dense, deterministic. No Loihi in the coverage cell. SpikeSlicer remains DVS/SNN CV — not a gate primitive (segment **05**). |
| (4) Stance | **Refuse** Lava/Nengo/Loihi as product runtime or tip SoT. **Metaphor:** event saliency → remesure debounce (**Embody** decision **5** / **Adopt** **26**). DeepWiki cartography of Lava/Nengo is **vocabulary only**. |
| (5) Sources | Davies et al., *Advancing Neuromorphic Computing With Loihi…*, Proc. IEEE (2021) `[Evidenced]`. Pehle et al., *The BrainScaleS-2 Accelerated Neuromorphic System…*, Front. Neurosci. (2022) `[Evidenced]`. Yik et al., *NeuroBench…*, arXiv:**2304.04640** `[Evidenced]`. Cao et al., SpikeSlicer, arXiv:**2410.02249** `[Evidenced]` (already in **05**). GitHub: `lava-nc/lava` ~739★; `nengo/nengo` ~939★; DeepWiki Evaluate useful for *what the frameworks are* — not for gate design `[Evidenced]`. |

### E. Physical reservoir computing (echo-state / liquid-state on physical media)

| Aspect | Finding |
| --- | --- |
| (1) Problem (domain) | Training full RNNs is hard; want fixed nonlinear dynamical “reservoir” + cheap linear readout for temporal tasks. |
| (2) Substrate claim | Physical media (photonics, spintronics, colloids, chemistry, memristors) supply high-dimensional fading memory; only readout is trained (ESN / LSM lineage). |
| (3) Not for CLI | Climb metrics are **not** a physical reservoir whose linear readout may declare green. Random dynamical projection ≠ certified `coverage.xml`. |
| (4) Stance | **Refuse** as SoT. **Sensor metaphor (narrow):** climb = cheap high-dim feedback; oracle = trained/authoritative readout — **already** dual-mode language; do **not** import ESN libraries to score gates. |
| (5) Sources | Jaeger, ESN technical report (2001); Maass, Natschläger & Markram, *Real-time computing without stable states* (LSM), Neural Computation **14** (2002) `[Evidenced]`. Cucchi et al. / intro surveys e.g. arXiv:**2412.13212** `[Evidenced]`. Formose chemical RC, Nature (2024) above `[Evidenced]`. GitHub: `reservoirpy/reservoirpy` ~651★ (software ESN — excellent *in-domain*, **Refuse** for gates). |

### F. Analog neural networks / continuous-time NN

| Aspect | Finding |
| --- | --- |
| (1) Problem (domain) | Discrete deep nets + digital MAC burn power; continuous-time dynamics (Neural ODEs) and Kirchhoff physics can embody depth in circuit time. |
| (2) Substrate claim | Analog circuits / memristive ODE solvers evolve hidden state in continuous time; Equilibrium Propagation trains energy-based analog nets; KirchhoffNet ties KCL to continuous-depth models. |
| (3) Not for CLI | Continuous Cover% trajectories must still **collapse** to boolean ≥ floor. Analog non-idealities are the opposite of hermetic CI. |
| (4) Stance | **Refuse** analog tip / Neural-ODE gate controller. **Metaphor:** “continuous climb progress display” is fine; gate remains discrete (**Refuse** fuzzy green). |
| (5) Sources | Chen et al., *Neural Ordinary Differential Equations*, arXiv:**1806.07366** / NeurIPS 2018 `[Evidenced]`. Kendall et al., *Training End-to-End Analog Neural Networks with Equilibrium Propagation*, arXiv:**2006.01981** `[Evidenced]`. Gao et al., *KirchhoffNet…*, arXiv:**2310.15872** `[Evidenced]`. GitHub: `rtqichen/torchdiffeq` ~6472★ (ODE training — **Refuse** as coverage SoT). |

### G. In-memory / compute-in-memory (memristor, crossbar)

| Aspect | Finding |
| --- | --- |
| (1) Problem (domain) | Von Neumann bottleneck: shuttling weights between DRAM and compute dominates DNN energy. |
| (2) Substrate claim | Crossbars perform analog MVM via Ohm + Kirchhoff where weights live; CIM macros target inference (and research training) efficiency. |
| (3) Not for CLI | Stage-0 / AST / claims are irregular graph work, not dense GEMM. Device variation ≠ deterministic oracle XML. |
| (4) Stance | **Refuse** CIM runtime and “in-memory green.” No honest SE analogue beyond “don’t thrash the expensive oracle artifact” (already cadence policy). |
| (5) Sources | *Memory Is All You Need: … CIM … LLM Inference*, arXiv:**2406.08413** `[Evidenced]`. Aguirre et al., *Hardware implementation of memristor-based ANNs*, Nature Communications (2024) `[Evidenced]`. Huang et al., *Memristor-based hardware accelerators for AI*, Nat Rev Electr Eng (2024) `[Evidenced]`. GitHub: `IBM/aihwkit` ~494★; `coreylammie/MemTorch` ~188★ — simulators for *analog HW research*, **Refuse** for doc-engine. |

### H. Reaction kinetics as computational dynamics

| Aspect | Finding |
| --- | --- |
| (1) Problem (domain) | Need a programming model for molecular controllers that is naturally analog and concurrent — CRNs as the “assembly language” of chemistry. |
| (2) Substrate claim | Finite CRNs can compute (stochastic CRN theory); DNA implements CRN kinetics; rates and topology program dynamical behaviors (oscillators, consensus, memories). |
| (3) Not for CLI | Rate equations do not decide `fail_under`. Treating coverage error as a kinetic ODE reopens PID/fuzzy theater (**Refuse** **25**). |
| (4) Stance | **Refuse** kinetic SoT. **Honest metaphor only:** *rate limits* on remesure ≈ bounding reaction propensity — same as saliency caps, not a new controller class. |
| (5) Sources | Soloveichik et al., *Computation with finite stochastic chemical reaction networks*, Natural Computing (2008) `[Evidenced]`. Soloveichik et al., PNAS 2010 (DNA↔CRN) `[Evidenced]`. Chen et al., *Programmable chemical controllers made from DNA*, Nature Nanotech (2013) `[Evidenced]`. GitHub: CRN/DSD toolchains exist but are lab compilers — not CI SoT `[Evidenced]` niche. |

### I. Reaction–diffusion computing (BZ, pattern formation as compute)

| Aspect | Finding |
| --- | --- |
| (1) Problem (domain) | Want massive spatial parallelism and collision-based logic without a clocked CPU fabric. |
| (2) Substrate claim | Belousov–Zhabotinsky (and related RD media) encode bits in wave-fragments; collisions implement gates/adders; native oscillating chemistry can recognize languages (chemical TM sketches). |
| (3) Not for CLI | Pattern formation does not emit JUnit/pytest XML. Spatial bistability ≠ PathCohesion. |
| (4) Stance | **Refuse** entirely as product tech. No Adopt beyond “don’t romanticize emergence as a substitute for Spec.” |
| (5) Sources | Adamatzky et al., *Computational Modalities of Belousov-Zhabotinsky Encapsulated Vesicles*, arXiv:**1009.2044** `[Evidenced]`. Dueñas-Díez & Pérez-Mercader, *Native Chemical Computation… BZ*, Front. Chem. (2021) `[Evidenced]`. Adamatzky, *Binary full adder… BZ*, Phys. Rev. E **92**, 032811 (2015) `[Evidenced]`. Excellent high-star GitHub productizing BZ compute: **absent** `[Unknown]` — literature + lab setups dominate. |

---

## 3. Tool / substrate → doc-engine response matrix

| Domain | If proposed as… | Response |
| --- | --- | --- |
| A DNA / molecular | Gate backend or “parallel proof” | **Refuse** |
| B Dissipative / CRN thermo | Soft floor / error-budget plant | **Refuse** (reaffirms **25**) |
| C Iontronic | Hysteresis library for oracle | **Refuse** HW; **Embody** Nagios-style dead-band on *advisory* only |
| D Loihi / BrainScaleS / Lava | doc_engine runtime | **Refuse**; DeepWiki = cartography only |
| E Physical / software RC | Climb as reservoir ⇒ green | **Refuse** as SoT; dual-mode already covers cheap vs oracle **without** ESN |
| F Analog / Neural ODE | Continuous confidence of green | **Refuse** |
| G Memristor CIM | Accelerate Stage-0 / cov | **Refuse** (wrong workload + non-determinism) |
| H Kinetic ODEs | PID/rate SoT on Cover% | **Refuse**; **Adopt** simple remesure **rate caps** only |
| I BZ / RD | Emergent architecture | **Refuse** |

**Honest analogues worth keeping (from 05 + this pass):**

| Physical phrase | Honest SE analogue | Not allowed |
| --- | --- | --- |
| Event saliency / spikes | Debounce / rate-limit oracle remesure | SNN runtime |
| Memristive / ionic hysteresis | Flap detection; climb file dead-band | Soft fail_under |
| Reservoir + linear readout | Climb sensors + separate oracle predicate | Readout declares floor |
| Dissipation / open system | CI always costs energy — schedule carbon-aware later (**31**) | Entropy as coverage SoT |
| Far-from-equilibrium | — | Theater |

---

## 4. Embody / Adopt / Refuse (summary)

| Idea | Stance | Notes |
| --- | --- | --- |
| Physical / wet / ASIC tip as coverage or claims SoT | **Refuse** | Category error |
| Neuromorphic frameworks (Lava, Nengo, Loihi bindings) in product | **Refuse** | Segment **05** + this |
| ESN/RC libraries scoring gates | **Refuse** | `reservoirpy` is fine science, wrong product |
| CIM / memristor / analog ODE solvers | **Refuse** | Wrong bottleneck |
| DNA / CRN / BZ / iontronic dependencies | **Refuse** | |
| Saliency → oracle cadence | **Embody** / **Adopt** | Decisions **5**, **26** |
| Hysteresis on advisory / targeting | **Adopt** | Decision **27**; iontronic papers are citations for *hygiene*, not impl |
| Boolean `fail_under` / oracle XML | **Embody** | Decisions **25**, **16-A** |
| DeepWiki Evaluate of Lava/Nengo | **Adopt as research habit** | Cartography only — never architecture SoT |
| Formose / BZ “emergence” as Spec substitute | **Refuse** | |

---

## 5. Unknowns

| ID | Unknown | Why it matters |
| --- | --- | --- |
| U1 | Whether any future *profiled* numeric hot path in doc-engine ever resembles dense MVM enough to revisit CIM — today **no** `[Confirmed]` profile demand | Constitution: no unprofiled accelerator theater |
| U2 | Carbon-aware CI scheduling (**31**) timing — orthogonal to physical computing | Optional P4; never blocks oracle |
| U3 | High-star open iontronic / BZ *product* stacks | Currently absent; absence ≠ “invent in-tree” |
| U4 | Whether agent prompts still over-index SpikeSlicer / “neuromorphic gates” language | Process hygiene — fix prompts if found; no new runtime |

---

## 6. What agents must not do

- Cite Loihi, BrainScaleS, DNA strand displacement, formose RC, BZ, memristor crossbars, or Neural ODEs as **reasons to soften** `fail_under` or to skip Spec.
- Add Lava, Nengo, aihwkit, MemTorch, reservoirpy, torchdiffeq, or wet-lab SDKs as doc-engine dependencies for quality gates.
- Treat DeepWiki (or any LLM wiki) as primary evidence over arXiv/IEEE/Nature.
- Equate climb Cover% or gap-average with a “reservoir state” that proves the floor.
- Propose dissipative-structure or CRN-thermodynamic controllers for coverage.

---

## 7. Segment verdict

| Question | Answer |
| --- | --- |
| Are A–I real science? | **Yes** — primary literature and (where noted) serious GitHub/DeepWiki artifacts `[Evidenced]`. |
| Do they belong in doc-engine tip / CI SoT? | **No — Refuse** substrates and tip SoTs. |
| Any Adopt? | Process only: keep **05** saliency/hysteresis analogues; use DeepWiki as cartography when exploring frameworks; reinforce Refuse list in backlog. |
| Reopen dual-mode / fuzzy green? | **No.** Strengthens **25–28**; no new product decisions required for impl. |
| Impl epic? | **None.** Research-complete; archive as process SoR. |

---

## 8. References (selected)

**DNA / molecular:** Adleman Science 1994; Soloveichik–Seelig–Winfree PNAS 2010; Qian–Winfree DNA cascades; Wang et al. PNAS 2023 parallel molecular computation on DNA storage.

**Far-from-equilibrium / CRN:** Prigogine dissipative structures; arXiv:2407.11498; Baltussen et al. Nature 2024 formose RC; `huckgroup/Formose_reservoir_computation`.

**Iontronic:** arXiv:2309.11438; PRL 130:268401 (2023); arXiv:2511.04209.

**Neuromorphic:** Davies et al. Proc. IEEE 2021 (Loihi); BrainScaleS-2 Front. Neurosci. 2022; NeuroBench arXiv:2304.04640; SpikeSlicer arXiv:2410.02249; `lava-nc/lava` (~739★), `nengo/nengo` (~939★); DeepWiki Evaluate: lava-nc/lava, nengo/nengo.

**Reservoir:** Jaeger ESN 2001; Maass et al. LSM 2002; arXiv:2412.13212; `reservoirpy/reservoirpy` (~651★).

**Analog / CT NN:** Neural ODEs arXiv:1806.07366; EqProp analog arXiv:2006.01981; KirchhoffNet arXiv:2310.15872; `rtqichen/torchdiffeq` (~6472★).

**CIM:** arXiv:2406.08413; Nat Commun 2024 memristive ANN hardware; `IBM/aihwkit` (~494★); `coreylammie/MemTorch` (~188★).

**Kinetics / RD:** Soloveichik stochastic CRN 2008; Chen et al. Nat Nanotech 2013; Adamatzky BZ arXiv:1009.2044; Front. Chem. 2021 native chemical computation; PRE 92:032811 BZ adder.

**Local:** `05-dynamics-neuromorphic.md`; synthesis decisions **25–28**; `fail_under=98.7`; policy **16-A**.
