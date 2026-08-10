---
title: 'ADR-0010: TypeScript owns IDE and MCP presentation'
status: Proposed
date: '2026-08-10'
---

# ADR-0010: TypeScript IDE / MCP presentation

## Context

LSP diagnostics and verification panels live in editor ecosystems. MCP clients
for org-wide tools are often TS. Engine remains Rust.

## Decision

**TypeScript** owns IDE extension / Model Context Protocol **presentation**
containers. Talks to engine via stdio/HTTP or local protocol. Not the merge
oracle writer.

**Protocol pin, tool primitives, and handle rules** live in **ADR-0011** and
`07-system-design/decisions/mcp-decision-matrix.md` — this ADR does not define
tool semantics.

## Status

Proposed.

## Consequences

Positive: natural developer-experience surface.  
Negative: Node toolchain for extensions only.  
Rejected: forcing all IDE UX through Python; putting verify oracle logic in TS.
