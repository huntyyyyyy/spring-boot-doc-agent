# Nest: Clojure graph brain

**Owns:** Babashka/Datascript (and optional JVM) queries over EDN export

**ADRs:** ADR-0005

**Status:** Planning nest — no product code until repo CONTRIBUTING gate + this nest’s Component C4.

## Look-first research

- `research/polyglot/`
- `docs/adr/adr-0005-clojure-graph-brain.md`

## Shared SoR

- `docs/DOMAIN_MAP.md`
- `docs/requirements/` · `docs/constraints/`
- `docs/c4/02-containers.md`

## Later (post-gate)

This nest may become a git subtree or standalone repo while keeping the same
MDC look-first contract so the “next repository” inherits context without
loading unrelated BCs.
