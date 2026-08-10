---
title: Decision Framework — Selection Taxonomy (six vectors)
status: ACTIVE
date: '2026-08-10'
audience: [stakeholder, product, engineer, agent]
---

# Decision Framework (Selection Taxonomy)

Assertions without **usage**, **locus**, and **rejected alternatives** are not
decisions — they are preferences. This standard turns “what / when / how / who /
where / why” into a **repeatable schema** so procurement, architecture, and
tool-surface choices stay traceable and bias-resistant.

Use **one filled matrix per significant choice**. Link an Architecture Decision
Record for the engineering record; keep the matrix as the analytical surface
humans and agents can score against.

## Three framings (same schema, different audience)

| Audience | Call it | Emphasize |
| --- | --- | --- |
| Stakeholders / product | **Decision Matrix** (analytical) | Evaluation vectors; repeatable selection; scored alternatives |
| Engineers | **Architecture Decision Record** companion | Rationale, context, consequences; prevents architectural drift |
| Business / risk | **Governance Framework** | Accountability, alignment, lifecycle, security zone |

Do not invent three incompatible schemas. **One row set; three labels.**

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
| **Usage case** | Concrete scenario (actor + goal + outcome) — not a slogan |
| **Code / Spec locus** | File, port, package, or Interface Control Document path where the choice binds |
| **Working hypothesis** | The selected Draft option (not human Accept) |
| **Rejected alternatives** | Named options + **why not** (at least one serious alternative) |
| **Embody / Adopt / Refuse / Pilot** | Product tier (constitution vocabulary) |
| **Claim tier** | Evidenced / Confirmed / Unknown |
| **Review date** | When to re-score (stops stale rubber-stamps) |

## Scoring (optional but preferred)

For each alternative, score vectors **0–2** (absent / partial / meets) against
**What**. Sum is a **sensor**, not a silent merge proof — human Accept still
required for Definition of Ready gates that name human sign-off.

### Optional mathematical layer (brainstorm — not Must)

To reduce scoring bias, a later Spike may attach **Multi-Criteria Decision
Analysis / Analytic Hierarchy Process** weights to the six vectors or to the
alternatives table (pairwise comparisons → consistency ratio). That layer
**quantifies preference**; it does not replace usage cases, loci, or Rejected
alternatives. Formal methods (Temporal Logic of Actions, Alloy, queueing
models, Monte Carlo) are catalogued as ideas in
`research/atam-formal/math-decision-methods-brainstorm-2026-08-10.md` — **not**
Definition of Ready Must and **not** substitutes for plants.

### Research-depth gate (before human Accept)

A matrix may say **Working hypothesis (Draft)** freely. It must **not** be
proposed for human Accept, and agents must not treat scores as Chosen truth,
unless one of:

| Gate | Meaning |
| --- | --- |
| `digest` | Load-bearing paper digested (type + sections + refs) |
| `primary_spec` | Normative industry Spec cited with section/SEP |
| `pilot_waiver` | Exact public engines = 0; explicit Pilot invent charter |

See `research/gaps/shallow-decisions-honesty-2026-08-10.md`. Score totals are
**sensors** only.

## Anti-patterns (refuse)

1. **Assertion-only ADR** — Decision without Rejected alternatives or Usage case.  
2. **Locus TBD forever** — “somewhere in the agent” is not a locus.  
3. **Hidden session state** as “how” when the product claims stateless protocol.  
4. **Model as Who-decides** for verify / lock / claim mutations.  
5. **Copying paper titles** into What without binding Quality Attribute Scenarios or reject codes.

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
