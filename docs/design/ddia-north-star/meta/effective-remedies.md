---
id: effective-remedies
kind: taxonomy
completeness: operational
tags: [remedy, fitness, characterization, mutation, sensor, sot]
related: [sor-vs-derived, rel-gate-needs-witness, maintainability-operability-evolvability, coverage-gates, refactor-sequencing]
last_refined: 2026-08-09
path: meta/effective-remedies.md

---

# Effective remedies (north-star companion)

## In one sentence

DDIA concept pages name **concerns**; this page names **mechanisms research and high-adoption practice show work** for those concerns in this product — Spec Accept must cite a mechanism here (or Explicit Defer), not a DDIA `id` alone.

## Why this exists

Human critique (2026-08-09): north-star tables described problems without installing solutions.
Research Spec: [`docs/research/process/23-concern-to-solution-remedies-2026.md`](../../../research/process/23-concern-to-solution-remedies-2026.md) (E-SOL0).

## Remedy mechanisms (default Adopt set)

| Mechanism id | What it installs | Evidence class | Refuse |
| --- | --- | --- | --- |
| **fitness-function** | CI-hard structural invariant (cycles, prelude leak, public surface, claim predicates) | Ford evolutionary architecture; ArchUnit-style rules-as-tests; HICSS 2026 research-software fitness | Drawings / README prose as the only check |
| **single-write-derive** | One SoR mutation; views recompute (outbox/CDC *pattern* transferred to artifacts) | Outbox doctrine; arXiv [2608.00501](https://arxiv.org/abs/2608.00501); policy **16-A** | Parallel authoritative APIs; silent LWW |
| **characterization-net** | Lock behavior before reshape; one seam; then structural verify | Feathers *Working Effectively with Legacy Code*; 2026 agent-refactor practice | “Fix while extracting” without a net |
| **adequacy-witness** | Mutation / metamorphic / planted counterexample proves the gate can fail | Mutmut; metamorphic coverage; E-QA SMS/MC as **sensors** | Cover% or LLM-judge as structural proof |
| **sensor-ledger-spec** | Watch presents gap classes; human Specs; fixer is a separate tip | E-STK0; react-doctor-style stalker pattern | Chat-only “we noticed” without a ledger |

## Concern → remedy (load-bearing map)

| North-star `id` | Primary remedy | Already Embodied (examples) | Next Adopt |
| --- | --- | --- | --- |
| `sor-vs-derived` | single-write-derive | Oracle `coverage.xml` vs climb XML **16-A**; cert derived fold | Every new gate Spec names SoR\|derived |
| `replication-lag-and-lww` | single-write-derive | Certification fold (not LWW merge) | Patch-at-use for doubles; one binding site |
| `rel-gate-needs-witness` | fitness-function + adequacy-witness | `pre_pr`, metamorphic, G2 AST witness, mutmut advisory | E-STK1 G1–G6 sensors |
| `coverage-gates` | adequacy-witness | Positive/FP/recall polarities separated | Keep Cover% necessary≠sufficient |
| `claims-and-status-drift` | fitness-function | `scripts/ci/check_repo_claims.py` | Path pins migrate with SoR moves |
| `maintainability-operability-evolvability` | fitness-function + characterization-net | tach cycles; size/complexipy; E-COH bar | E-COH1 seam map before moves |
| `refactor-sequencing` | characterization-net + sensor-ledger-spec | Spike receipts; finding ledger | Cite SOL remedy ids on reshape Specs |
| `architecture-decision-review` | all five (pick by concern) | Prompt-10 tiers + catalog cite | **Fail** ADRs that only cite DDIA ids |

## Spec Accept shape (non-negotiable once E-SOL0 Approved)

```text
Concern → DDIA id (vocabulary)
       → Remedy mechanism id (this page)
       → Accept = mechanism installed | Explicit Defer + exit criterion
```

## Fail if

- Fail if a Spec Accept row cites only a DDIA page id with no remedy mechanism id from this page (or Explicit Defer).
- Fail if Cover% or LLM-as-judge is offered as proof a **structural** fitness function holds.
- Fail if a reshape starts without a characterization net when the concern is maintainability / refactor.

## See also

- Research: `docs/research/process/23-concern-to-solution-remedies-2026.md`
- Design Spec: `docs/design/concern-to-solution-remedies-design-2026-08-09.md`
- Enrichment: [enrichment-protocol.md](enrichment-protocol.md) (requires `## Effective remedies` on operational concepts / relationships / playbooks)
