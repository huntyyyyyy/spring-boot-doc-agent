# Nests — bounded contexts

Each nest is a bounded context folder with a thin `README.md` and a **glob-scoped**
`.cursor/rules/nest.mdc`. Path scoping is MDC-only (no nested `AGENTS.md`).

When entering a nest, agents load that nest’s rule automatically if matching
files are in context. Long evidence is retrieved via Skill `rag-retrieve` and
`research/INDEX.md` — nests point at packs; they do not inline them.

See `docs/DOMAIN_MAP.md` for the nest table.
