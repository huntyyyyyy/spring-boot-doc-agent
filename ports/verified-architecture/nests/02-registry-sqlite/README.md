# Nest: SQLite registry

**Owns:** Derived beans/edges schema; rebuildable local DB

**Architecture Decision Records:** Architecture Decision Record ADR-0002

**Status:** Planning nest — no product code until repo CONTRIBUTING gate + this nest’s Component C4.

## Look-first research

- `research/polyglot/`
- `docs/adr/adr-0002-sqlite-registry.md`

## Shared System of Record

- `docs/DOMAIN_MAP.md`
- `docs/requirements/` · `docs/constraints/`
- `docs/c4/02-containers.md`

## Later (post-gate)

This nest may become a git subtree or standalone repo while keeping the same
MDC look-first contract so the “next repository” inherits context without
loading unrelated bounded contexts.
