# Nest: Rust engine

**Owns:** Source Code Index Protocol decode, WiringResolver, LockCheck, receipts, wasmtime host

**Architecture Decision Records:** Architecture Decision Record ADR-0007, Architecture Decision Record ADR-0004, Architecture Decision Record ADR-0002

**Status:** Planning nest — no product code until repo CONTRIBUTING gate + this nest’s Component C4.

## Look-first research

- `research/layers-of-truth/`
- `research/polyglot/`
- `research/atam-formal/`
- `docs/c4/03-components.md`

## Shared System of Record

- `docs/DOMAIN_MAP.md`
- `docs/requirements/` · `docs/constraints/`
- `docs/c4/02-containers.md`

## Later (post-gate)

This nest may become a git subtree or standalone repo while keeping the same
MDC look-first contract so the “next repository” inherits context without
loading unrelated bounded contexts.
