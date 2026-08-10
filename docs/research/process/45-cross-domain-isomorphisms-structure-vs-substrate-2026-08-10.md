---
title: Cross-domain isomorphisms — when unrelated sciences share structure that CS
  already stole
status: RESEARCH — refines E-DYN1; structure Adopt ≠ substrate tip SoT
date: '2026-08-10'
epic_seed: E-DYN1
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/research/process/43-physical-info-dynamics-computing-2026-08-10.md
- docs/research/process/44-formulas-concepts-dynamics-info-physical-2026-08-10.md
- docs/research/process/20-theory-domains-problem-first-gates-2026.md
- docs/research/process/21-physical-unconventional-computing-2026.md
- docs/research/process/05-dynamics-neuromorphic.md
do_not:
- conflate formal isomorphism with tip hardware runtime
- treat “chemistry stores information” as license to soften fail_under
- invent functorial merge gates without Spec
spec_gate: DRAFT E-DYN1 addendum — isomorphism hygiene
skill: .cursor/skills/cross-domain-isomorphism/SKILL.md
rule: .cursor/rules/cross-domain-isomorphism.mdc
last_reviewed: '2026-08-10'
---

# Cross-domain isomorphisms (your pushback, taken seriously)

**Standing practice.** This memo’s lens is now skill **cross-domain-isomorphism**
(always-on rule + `.cursor/skills/…`) — apply I1–I5 whenever planning across domains,
not only in E-DYN1 research.

**Claim under test.** Unrelated branches of science often share **the same
abstract structure**. When that structure is made precise, CS routinely
**imports it as algorithms / math** — genetic algorithms, Hopfield↔Ising,
CRN↔circuits, reservoir↔random features. That is *not* the same as importing
the **physical substrate** (DNA tubes, Loihi, BZ dishes) as doc-engine tip SoT.

**Refined Refuse.** We refuse **substrate-as-CI-SoT** and **predicate→plant**
category errors — not the idea that isomorphisms exist.

```text
PHYSICAL / BIO DOMAIN
        │  (often)
        ▼
ABSTRACT STRUCTURE  (CRN, energy, fitness, reservoir, code)
        │  ←── formal / empirical isomorphism
        ▼
CS ARTIFACT          (algorithm, circuit semantics, ML model)
        │
        ├─ Adopt as MATH / PATTERN / SENSOR language     ✅ often earned
        └─ Tip HARDWARE / wetware as merge SoT           ❌ still Refuse
```

---

## 0. Verdict

| Question | Answer |
| --- | --- |
| Are there genuine overlaps across “distinct” sciences? | **Yes** `[Evidenced]` — many are already CS primitives. |
| Does that dissolve domain boundaries? | **No** — it *names the shared algebra*, then re-specializes. |
| Does chemistry “already solve” documentation quality? | **No** — capacity to store/process info ≠ correctness predicate for claims. |
| What changes in E-DYN1? | Split **Structure-Adopt** from **Substrate-Refuse**; keep decisions 25–28. |

---

## 1. What an isomorphism must specify

A useful cross-domain map names:

1. **Objects** in domain A and B  
2. **Morphisms / dynamics** preserved  
3. **What is *not* preserved** (units, noise model, hermeticity, semantics)  
4. **Where the map already landed in CS** (if ever)

Without (3)–(4) you get mystical unity; with them you get **earned transfer**.

---

## 2. Earned isomorphisms (structure → CS tools)

### 2.1 Evolution ↔ search (genetic algorithms)

| | |
| --- | --- |
| **Shared structure** | Population of genotypes; fitness \(f\); variation (mutation/crossover); selection |
| **Bio side** | Darwinian evolution / population genetics |
| **CS side** | Holland *Adaptation in Natural and Artificial Systems* (1975); genetic algorithms, evolutionary strategies |
| **Preserved** | Generate–test over a fitness landscape; schema / building-block heuristics (debated) |
| **Not preserved** | Real DNA chemistry, meiosis physics, ecological carrying capacity |
| **Status** | **Adopt** as search *pattern* (already mainstream CS). **Refuse** as tip wet-lab |

**Point for you:** genetics didn’t stay “too distinct” — CS stole the *algorithmic*
skeleton decades ago.

### 2.2 Spin glass / Ising ↔ Hopfield associative memory

| | |
| --- | --- |
| **Shared structure** | Binary (or ±1) spins/neurons; pairwise couplings \(W_{ij}\); energy \(E=-\frac12\sum_{ij}W_{ij}s_is_j\); dynamics that descend energy |
| **Physics** | Ising / spin-glass statistical mechanics |
| **CS/neuro** | Hopfield networks (memory as attractors) `[Evidenced — Hopfield lineage; categorical recovery 2006.15136 / 2201.02756]` |
| **Preserved** | Energy landscape, attractors-as-memories, frustration |
| **Not preserved** | Temperature schedule as literal \(k_BT\); magnetic materials |
| **Status** | **Adopt** energy/attractor vocabulary for *optimization / memory models*. **Refuse** as coverage softener (“relax into green basin”) |

### 2.3 Chemical reaction networks ↔ digital circuits / programs

| | |
| --- | --- |
| **Shared structure** | Species = wires/signals; reactions = gates/updates; stoichiometry / rate laws |
| **Chem** | Mass-action CRNs \(\dot c = N v(c)\) |
| **CS / molprog** | Abstract CRNs as a **programming language**; compile to DNA strand displacement `[Evidenced — Soloveichik et al. PNAS 2010 “DNA as universal substrate for chemical kinetics”; Chen–Doty–Soloveichik arXiv:1204.4176]` |
| **Preserved** | Computational expressiveness (with caveats: deterministic CRNs → semilinear; stochastic ≈ more power with error) |
| **Not preserved** | Hermetic CI, bit-exact pytest, citation entailment |
| **Status** | **Adopt** “CRN = IR / circuit IR” *idea* for understanding molecular compute. **Refuse** DNA tubes as Stage-0 |

**Point for you:** chemistry *does* store and transform vast combinatorial information —
via **molecular state spaces**. The isomorphism is to **computation theory**, not to
`check_repo_claims.py`.

### 2.4 Reservoir dynamics ↔ random features / kernels

| | |
| --- | --- |
| **Shared structure** | Fixed nonlinear dynamical map \(F\); train only linear readout \(W\) |
| **Physics / neuro** | Echo-state / liquid-state / physical reservoirs |
| **CS/ML** | Random kitchen sinks / extreme learning / fixed-feature + linear head; ESN universality for fading-memory filters `[Evidenced — Jaeger 2001; reviews e.g. 2507.18467]` |
| **Preserved** | Rich fixed feature map + cheap readout |
| **Not preserved** | Memristor/ferrofluid/formose medium |
| **Status** | **Adopt pattern:** climb/sensors = rich \(r_t\); oracle = constrained readout. **Refuse** physical \(F\) in tip |

### 2.5 Shannon / Kolmogorov ↔ coding & compressibility in SE

| | |
| --- | --- |
| **Shared structure** | Uncertainty \(H\); description length \(K\) |
| **Status** | Already CS; optional **sensor** for suite diversity. **Refuse** as fail_under |

### 2.6 Control / feedback ↔ CI loops

| | |
| --- | --- |
| **Shared structure** | Observe → act → remeasure |
| **Status** | **Embody** boolean feedback. **Refuse** Cover% as continuous plant |

---

## 3. Contested / partial isomorphisms (don’t overclaim)

| Map | Why tempting | Failure mode |
| --- | --- | --- |
| Free energy / predictive coding ↔ agent planning | Same “surprise minimization” talk | Units & SoT unclear; easy mysticism `[Unknown]` as SE SoT |
| Landauer ↔ “don’t erase coverage debt” | Info has thermodynamic cost | Bound is physical heat, not merge policy |
| Network controllability ↔ microservice mesh | Kalman rank on graphs | Wrong product category (constitution Refuse mesh) |
| Category theory / functors ↔ “all science is one” | Functors *do* formalize transfer `[Evidenced — 2006.15136]` | Without concrete categories, “functor” becomes slogan |

**Applied category theory** is the honest meta-language for *what you asked*:
structure-preserving maps between domains. It does **not** auto-solve product
gates — it forces you to name objects and morphisms.

---

## 4. “Chemistry stores so much information” — precise reading

True statements:

1. Molecular state spaces are **astronomically large** (sequence space \(4^L\),
   CRN configuration counts).  
2. Strand-displacement / CRN systems can implement **logic and dynamics** with
   formal compilers to abstract reaction programs `[Evidenced]`.  
3. Biology already does information processing (replication, proofreading,
   regulation) under thermodynamic constraints.

False leaps:

4. Therefore molecular compute **is** a documentation citation SoT.  
5. Therefore fail_under can be a free-energy or concentration threshold.  
6. Therefore tip should depend on wetware / neuromorphic ASICs.

**(1)–(3) ⇒ Adopt structure. (4)–(6) ⇒ Refuse substrate-as-SoT.**

Same pattern as genetic algorithms: steal the **search algebra**, leave the
**organism**.

---

## 5. Isomorphism test (use before claiming “solved by just being”)

| # | Question | Pass ⇒ |
| --- | --- | --- |
| I1 | Name objects + morphisms on both sides | Formal map possible |
| I2 | Cite where CS already imported it (or why not) | Earned vs speculative |
| I3 | State what the map **does not** preserve | Avoid category error |
| I4 | Land on a **typed** artefact (algorithm, sensor, docs) | Structure-Adopt |
| I5 | Does it change a **boolean merge predicate**? | Only if Spec explicitly redefines SoT — default **no** |

If I5 is “yes, Cover% becomes continuous plant,” fail the test (decision 25).

---

## 6. Embody / Adopt / Refuse (updated)

| Stance | Content |
| --- | --- |
| **Embody** | Boolean oracle SoT; climb sensors; discrete feedback; LA/probability as ambient math |
| **Adopt (structure)** | GA/evolutionary search patterns; energy/attractor language for *optimization discussion*; CRN-as-IR literacy; reservoir→readout analogy for climb→oracle; Shannon sensors if spiked; **isomorphism hygiene (I1–I5)** in research |
| **Refuse (substrate / bad type)** | DNA/CRN/ionic/Loihi/BZ/memristor tip deps; Landauer/FDT/PID/entropy as fail_under; “unity of science” without I1–I5 |

---

## 7. Adversarial

| Attack | Response |
| --- | --- |
| “Isomorphisms mean Refuse was wrong” | Refuse was **substrate/type**, not **structure** — this memo splits them |
| “CRNs are Turing-powerful so replace Stage-0” | Expressiveness ≠ hermetic citation support; wrong artefact type |
| “Hopfield energy ⇒ soft green basins” | Attractors in spin models ≠ merge SoT |
| “Category theory unifies everything so Spec is optional” | Functors need named categories; Spec *is* naming the product category |

---

## 8. Sources

Holland 1975 · Hopfield / Ising lineage · Soloveichik–Seelig–Winfree PNAS 2010 ·
Chen–Doty–Soloveichik `1204.4176` · Jaeger 2001 · ESN dynamics `2507.18467` ·
Manin–Marcolli / categorical Hopfield `2006.15136`, `2201.02756` · Shannon ·
local `05` / `20` / `21` / `43` / `44`.

---

## 9. Bottom line

Your instinct is right about **overlap via structure**. Genetic theories *did*
enter CS; chemical kinetics *did* get a programming-language semantics; spin
glasses *did* become associative memory. The mistake is collapsing that into
“therefore the wet/physical instance already *is* our quality SoT.”

Steal the **algebra**. Keep the **boolean predicate**. Leave the **dish / chip**
off the tip — unless Spec deliberately changes the product category.
