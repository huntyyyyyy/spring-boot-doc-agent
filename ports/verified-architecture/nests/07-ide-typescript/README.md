# Nest: TypeScript IDE / presentation

**Owns (when built):** Language Server Protocol diagnostics, verification
panel, Model Context Protocol **client** wiring to the engine. Not Spec corpus
Model Context Protocol host; not merge oracle.

**Fail closed:** Spec corpus MCP host or verify oracle in TypeScript/Python →
violates Architecture Decision Record ADR-0010 / ADR-0007.

**Now:** README + `nest.mdc` only — no extension package until Definition of
Ready PASS.

## Open first

1. `docs/adr/adr-0010-typescript-ide-mcp.md`  
2. `docs/adr/adr-0011-mcp-protocol-and-tool-surface.md`  
3. `docs/c4/02-containers.md`

## Shared System of Record

- `03-requirements/` · `04-constraints/`  
- `docs/c4/` · `docs/adr/`
