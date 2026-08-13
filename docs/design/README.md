# Design docs

Product and architecture design guidance that is **not** session chronology.

| Tree / file | Role |
|------|------|
| [ddia-north-star/](ddia-north-star/) | DDIA-shaped design SoR: domains, relationships, chapter 5W1H, playbooks, **deviations with evidence** |
| [../product-architecture.md](../product-architecture.md) | doc-engine A+C / kernel / adapters product architecture |
| [rust-stack-fit-memo-2026-08-08.md](rust-stack-fit-memo-2026-08-08.md) | Stack-fit ADR: Rust vs Python — **refuse in-tree Rust by default** (profiled exception only) |
| [coverage-measure-modes-design-2026-08-08.md](coverage-measure-modes-design-2026-08-08.md) | Coverage measure/climb design — **APPROVED** (E-CM0; decisions 1–31, policy 16-A) |
| [test-suite-parallel-domains-design-2026-08-08.md](test-suite-parallel-domains-design-2026-08-08.md) | Test BCs → CI shards — **APPROVED** Spec gate E-TEST0 (T1–T18, policy T-A) |
| [suite-stalking-sensors-design-2026-08-09.md](suite-stalking-sensors-design-2026-08-09.md) | Suite-stalking sensors — **APPROVED** Spec gate E-RUN0 (R1–R8; D1/D2/D17) |
| [test-adequacy-markers-design-2026-08-09.md](test-adequacy-markers-design-2026-08-09.md) | Test adequacy markers — **APPROVED** Spec gate E-QA0 (Q1–Q8; anti-padding) |
| [ci-workflow-modularity-design-2026-08-09.md](ci-workflow-modularity-design-2026-08-09.md) | CI workflow modularity design |
| [concept-split-cohesion-design-2026-08-09.md](concept-split-cohesion-design-2026-08-09.md) | Cohesion-first concept splits — **APPROVED** Spec gate E-COH0 (COH1–COH12) |
| [code-intel/](code-intel/) | Code intelligence stages — **DRAFT** E-CX0 (S0 Serena adopt + **operator runbook** · S1 resolved facts · S2 verify-loop). No Implement on this tip |
| [intent-kernel-cas-apply-design-2026-08-13.md](intent-kernel-cas-apply-design-2026-08-13.md) | Intent Kernel C4 / SoS / repo tree — **DRAFT** E-IK0; **deferred indefinitely** as program (see E-CX0) |

Dated research and design memos live under **`docs/design/`**, not under `claude/`. Cite north-star `id`s rather than restating them. Older notes may still exist under `claude/research/` until relocated.
