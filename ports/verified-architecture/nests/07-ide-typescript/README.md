# Nest: TypeScript IDE/Model Context Protocol

**Owns:** Language Server Protocol diagnostics, verification panel, Model Context Protocol presentation

**Architecture Decision Records:** Architecture Decision Record ADR-0010

**Status:** Planning nest — no product code until repo CONTRIBUTING gate + this nest’s Component C4.

## Look-first research

- `docs/c4/02-containers.md`
- `docs/adr/adr-0010-typescript-ide-mcp.md`

## Shared System of Record

- `docs/DOMAIN_MAP.md`
- `docs/requirements/` · `docs/constraints/`
- `docs/c4/02-containers.md`

## Later (post-gate)

This nest may become a git subtree or standalone repo while keeping the same
MDC look-first contract so the “next repository” inherits context without
loading unrelated bounded contexts.
