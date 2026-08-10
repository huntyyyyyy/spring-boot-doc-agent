# Verified Architecture Engine

**Status:** Requirements · Constraints · C4 · ADR planning only — **no product code yet.**

Polyglot local-first **verified architecture** system (Spring/Java wiring +
architecture locks + proof-tour receipts). Languages are first-class peers:

**Rust · WASM · SQLite · Go · Ruby · Clojure · TypeScript · Python (peer) · C · Zig (earned)**

This repository is the **planning SoR**. Implementation lands only after the
gates in [`CONTRIBUTING.md`](CONTRIBUTING.md) pass.

## Start here

| Order | Read |
| --- | --- |
| 1 | [`docs/standards/no-code-gate.md`](docs/standards/no-code-gate.md) |
| 2 | [`docs/requirements/strs.md`](docs/requirements/strs.md) |
| 3 | [`docs/constraints/constraints.md`](docs/constraints/constraints.md) |
| 4 | [`docs/requirements/qas.md`](docs/requirements/qas.md) |
| 5 | [`docs/c4/`](docs/c4/README.md) |
| 6 | [`docs/adr/`](docs/adr/README.md) |

## Provenance

Ported and **re-scoped** from research on
[`huntyyyyyy/spring-boot-doc-agent`](https://github.com/huntyyyyyy/spring-boot-doc-agent)
(PR #120 process/50–55 + ADRs). That repo remains the historical doc-engine /
kitchen plant. **This** repo does **not** assume Python owns the majority of the
engine.

## Explicit non-goals (until gates clear)

- Shipping application code under `crates/`, `go/`, etc.
- Treating C4 diagrams as decisions without ADRs
- Dual merge oracles
- LLM/RAG as verify witnesses
