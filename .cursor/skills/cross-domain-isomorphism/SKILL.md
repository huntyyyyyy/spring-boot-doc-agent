---
name: cross-domain-isomorphism
description: >-
  Apply a structure-vs-substrate isomorphism lens when planning, researching,
  designing, or comparing ideas across domains (science, SE, tools, product). Use
  whenever framing a problem, weighing Adopt/Refuse, importing patterns from another
  field, or the user mentions analogy, isomorphism, genetics/chemistry/physics→CS,
  or “unrelated branches of science.” Prefer this over dismissing distant fields as
  irrelevant OR collapsing them into tip wetware/runtime. Project rule
  cross-domain-isomorphism.mdc is agent-requested (not alwaysApply); this skill holds depth.
---

# Cross-domain isomorphism (planning lens)

Use this skill when analogy / cross-domain Adopt-Refuse is in play — not only
when the user names physics or biology. Pair with **se-quality-constitution** and,
for design-shaped work, **principal-se-research-epic**. Rule file is a thin trigger;
keep procedure here.

## Core distinction (never collapse)

```text
DOMAIN A  ──structure-preserving map──►  DOMAIN B
              │
              ├─ STRUCTURE (algebra, dynamics, info, search)  → may Adopt
              └─ SUBSTRATE (wetware, ASIC, medium, product instance) → usually Refuse as tip SoT
```

- **Structure-Adopt:** shared objects/morphisms → algorithms, typed patterns, sensors, docs vocabulary.
- **Substrate-Refuse:** physical/product instance as merge/citation/CI SoT without Spec that changes product category.
- Mystical unity without named maps is as wrong as siloed refusal of all analogy.

## When planning (checklist — run mentally every time)

Before Embody / Adopt / Refuse / Implement:

1. **Name the problem** in *this* product’s types (predicate, sensor, adapter, process).
2. **Ask:** does another field already solve an *isomorphic* problem?
3. If yes, run **I1–I5** (below) before importing or refusing.
4. Land the map on a **typed artefact** — never on “vibes.”
5. Keep boolean SoTs boolean unless Spec explicitly retypes them (constitution).

## Isomorphism test (I1–I5)

| ID | Question | Fail means |
| --- | --- | --- |
| **I1** | Name **objects** and **morphisms/dynamics** on both sides | Hand-wavy analogy |
| **I2** | Cite where the structure already landed in CS/SE (or why not) | Unearned novelty theater |
| **I3** | State what the map **does not** preserve (units, hermeticity, semantics) | Category error |
| **I4** | Choose landing: algorithm · pattern · sensor · adapter · docs — not substrate tip SoT by default | Wetware-as-product |
| **I5** | Does this change a **boolean merge/citation predicate**? Default **no** | Predicate→plant / soft green |

## Earned exemplars (remember these exist)

| Structure | Bio/phys side | CS landing |
| --- | --- | --- |
| Fitness + variation + selection | Evolution / genetics | Genetic algorithms (Holland) |
| Energy + couplings + attractors | Ising / spin glass | Hopfield nets |
| Species + reactions | CRN / mass-action | Circuit IR; DNA strand-displacement compilers |
| Fixed rich dynamics + linear readout | Reservoir / LSM | Random features / ESN pattern |
| Uncertainty / description length | Thermo / info | Shannon coding; Kolmogorov (sensors only) |
| Observe → act → remeasure | Control | CI feedback loops (boolean reference stays SoT) |

## Anti-patterns

| Anti-pattern | Do instead |
| --- | --- |
| “Too distinct — ignore” | Run I1–I5; often structure transfers |
| “Chemistry stores info ⇒ it’s our SoT” | Capacity ≠ predicate type |
| “Free energy / Landauer / PID ⇒ soften fail_under” | Wrong type (constitution) |
| “Functor / isomorphism ⇒ skip Spec” | Functors *require* named categories — Spec names them |
| Duplicate “dynamics stacks” for A⊂B | One structure, one landing |

## Research SoR (this repo)

- Depth memo: `docs/research/process/45-cross-domain-isomorphisms-structure-vs-substrate-2026-08-10.md`
- Formulas: `docs/research/process/44-formulas-concepts-dynamics-info-physical-2026-08-10.md`
- Theory A–H / physical A–I: `process/20-…`, `process/21-…`, umbrella `process/43-…`
- Prior metaphor locks: `process/05-dynamics-neuromorphic.md` (decisions 25–28)

## Output habit

When a plan borrows from another field, write one line:

```text
Iso: <A structure> ≅ <B structure> → land as <artefact type> | non-preserved: <…> | I5: no SoT retype
```

If I1–I5 cannot be filled, do not Adopt; mark Unknown or Refuse.
