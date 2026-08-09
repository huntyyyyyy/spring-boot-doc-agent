# Design docs

Product and architecture design guidance that is **not** session chronology.

| Tree / file | Role |
|------|------|
| [ddia-north-star/](ddia-north-star/) | DDIA-shaped design SoR: domains, relationships, chapter 5W1H, playbooks, **deviations with evidence** |
| [../product-architecture.md](../product-architecture.md) | doc-engine A+C / kernel / adapters product architecture |
| [rust-stack-fit-memo-2026-08-08.md](rust-stack-fit-memo-2026-08-08.md) | Stack-fit ADR: Rust vs Python — **refuse in-tree Rust by default** (profiled exception only) |
| [coverage-measure-modes-design-2026-08-08.md](coverage-measure-modes-design-2026-08-08.md) | Coverage measure/climb design — **APPROVED** (E-CM0; decisions 1–31, policy 16-A) |
| [test-suite-parallel-domains-design-2026-08-08.md](test-suite-parallel-domains-design-2026-08-08.md) | Test BCs → CI shards — **APPROVED** Spec gate E-TEST0 (T1–T18, policy T-A) |

Dated research and design memos live under **`docs/design/`**, not under `claude/`. Cite north-star `id`s rather than restating them. Older notes may still exist under `claude/research/` until relocated.
