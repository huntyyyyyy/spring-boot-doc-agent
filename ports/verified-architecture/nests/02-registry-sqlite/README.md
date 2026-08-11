# Nest: SQLite registry

**Owns (when built):** Derived beans/edges schema; rebuildable local DB via
rusqlite from the Rust engine; EDN export feed for nest 05.

**Fail closed:** another language owns registry schema/write path, or Python
registry owner → violates Architecture Decision Record ADR-0002.

**Now:** README + `nest.mdc` only — no schema DDL / crates until Definition of
Ready PASS.

## Open first

1. `docs/adr/adr-0002-sqlite-registry.md`  
2. `docs/c4/02-containers.md`  
3. `08-verification/sor-derived-matrix.md`

## Shared System of Record

- `03-requirements/` · `04-constraints/`  
- `docs/c4/` · `docs/adr/`
