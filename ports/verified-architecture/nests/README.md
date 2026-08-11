# Nests — bounded contexts

Each nest is a bounded context folder with a thin `README.md` and (when active) a
**glob-scoped** `.cursor/rules/nest.mdc`. Path scoping is MDC-only.

**Refuse:** `nests/08-aci-python-peer/` — tombstone README only; no nest rule
(Architecture Decision Record ADR-0001 amended 2026-08-11).

When entering an **active** nest, agents load that nest’s rule if matching files
are in context. Long evidence via Skill `rag-retrieve` and `research/INDEX.md`.

See `docs/DOMAIN_MAP.md` for the nest table.
