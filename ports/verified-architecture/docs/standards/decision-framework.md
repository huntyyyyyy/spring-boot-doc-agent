---
title: Decision Framework — Selection Taxonomy (six vectors)
status: ACTIVE
date: '2026-08-10'
last_reviewed: '2026-08-11'
audience: [stakeholder, product, engineer, agent]
---

# Decision Framework (Selection Taxonomy)

A choice without **usage**, **locus**, and **rejected alternatives** is a
preference, not a decision. Fill **one matrix per significant choice**; link an
Architecture Decision Record for the engineering record. FREEZE: deepen
existing matrices (receipt β/ρ, claim withdrawal, handle lifecycle) only — new
matrix files without human override = reject.

## Three framings (same schema, different audience)

| Audience | Call it | Emphasize |
| --- | --- | --- |
| Stakeholders / product | **Decision Matrix** (analytical) | Evaluation vectors; scored alternatives |
| Engineers | **Architecture Decision Record** companion | Rationale, context, consequences |
| Business / risk | **Governance Framework** | Accountability, lifecycle, security zone |

One row set; three labels — do not invent incompatible schemas.

## Six evaluation vectors

| Vector | Question | Captures |
| --- | --- | --- |
| **Why** (Driver) | Why decide at all? | Pain, business objective, technical limit, threat |
| **What** (Requirement) | What must be true? | Features, constraints, Quality Attribute Scenarios, reject classes |
| **Who** (Stakeholders) | Who owns / uses / decides? | End users, decision-makers, maintainers, harness vs model |
| **How** (Integration) | How does it land? | Deployment, migration, cost, protocol, adapters |
| **When** (Timeline) | When does it apply? | Trigger, implementation window, review / sunset |
| **Where** (Environment) | Where does it live? | Local vs remote, security zone, module / package path |

Every filled matrix **must** also carry:

| Extra column | Purpose |
| --- | --- |
| **Usage case** | Actor + goal + outcome — not a slogan |
| **Code / Spec locus** | File, port, package, or Interface Control Document path where the choice binds |
| **Working hypothesis** | Selected Draft option (not human Accept) |
| **Rejected alternatives** | Named options + **why not** (≥1 serious alternative) |
| **Embody / Adopt / Refuse / Pilot** | Product tier (constitution vocabulary) |
| **Claim tier** | Evidenced / Confirmed / Unknown |
| **Review date** | When to re-score |

## Scoring (optional but preferred)

Score alternatives **0–2** (absent / partial / meets) against **What**. Sum is
a **sensor**, not silent merge proof — human Accept still required where
Definition of Ready names sign-off.

### Optional mathematical layer (brainstorm — not Must)

A later Spike may attach Multi-Criteria Decision Analysis / Analytic Hierarchy
Process weights (pairwise comparisons → consistency ratio). That layer
**quantifies preference**; it does not replace usage cases, loci, or Rejected
alternatives. Formal methods catalogued in
`research/atam-formal/math-decision-methods-brainstorm-2026-08-10.md` are
**not** Definition of Ready Must and **not** substitutes for plants.

### Research-depth gate (before human Accept)

Working hypothesis (Draft) is free. Agents must not treat scores as Chosen
truth for human Accept unless one of:

| Gate | Meaning |
| --- | --- |
| `digest` | Load-bearing paper digested (type + sections + refs) |
| `primary_spec` | Normative industry Spec cited with section or Model Context Protocol specification enhancement proposal |
| `pilot_waiver` | Exact public engines = 0; explicit Pilot invent charter |

See `research/gaps/shallow-decisions-honesty-2026-08-10.md`.

## Anti-patterns (refuse)

1. **Assertion-only Architecture Decision Record** — Decision without Rejected
   alternatives or Usage case.  
2. **Locus TBD forever** — “somewhere in the agent” is not a locus.  
3. **Hidden session state** as “how” when the product claims stateless protocol.  
4. **Model as Who-decides** for verify / lock / claim mutations.  
5. **Copying paper titles** into What without binding Quality Attribute
   Scenarios or reject codes.

## Where matrices live

| Kind | Path |
| --- | --- |
| This standard | `docs/standards/decision-framework.md` |
| Filled matrices | `07-system-design/decisions/<topic>-decision-matrix.md` |
| Engineering record | `docs/adr/adr-NNNN-*.md` (cite the matrix) |
| Tool / schema binding | Matching Interface Control Document under `07-system-design/icd/` |

## Minimal template

```markdown
# <Topic> — Decision Matrix

| Vector | Content |
| --- | --- |
| Why | … |
| What | … |
| Who | … |
| How | … |
| When | … |
| Where | … |

## Alternatives scored
| Option | Why score | What | Who | How | When | Where | Total | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Usage cases
| ID | Actor | Goal | Steps | Locus | Outcome |
| --- | --- | --- | --- | --- | --- |

## Rejected (must list)
| Option | Why rejected |
```
