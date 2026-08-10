# Nest: WebAssembly sandbox

**Owns:** Capability LockCheck guest; fuel/epoch; trust-boundary (not unearned proved)

**Architecture Decision Records:** Architecture Decision Record ADR-0004

**Status:** Planning nest — no product code until repo CONTRIBUTING gate + this nest’s Component C4.

## Look-first research

- `research/atam-formal/`
- `docs/adr/adr-0004-native-then-wasm-lockcheck.md`

## Shared System of Record

- `docs/DOMAIN_MAP.md`
- `docs/requirements/` · `docs/constraints/`
- `docs/c4/02-containers.md`

## Later (post-gate)

This nest may become a git subtree or standalone repo while keeping the same
MDC look-first contract so the “next repository” inherits context without
loading unrelated bounded contexts.
