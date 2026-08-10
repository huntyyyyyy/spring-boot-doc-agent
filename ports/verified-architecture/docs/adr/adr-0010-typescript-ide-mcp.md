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

**TypeScript** owns IDE extension / MCP presentation containers. Talks to engine
via stdio/HTTP MCP or local protocol. Not the merge oracle writer.

## Status

Proposed.

## Consequences

Positive: natural DevEx surface.  
Negative: Node toolchain for extensions only.  
Rejected: forcing all IDE UX through Python.
