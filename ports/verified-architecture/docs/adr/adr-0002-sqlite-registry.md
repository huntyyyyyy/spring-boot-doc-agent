---
title: 'ADR-0002: SQLite as derived bean/dep registry'
status: Proposed
date: '2026-08-10'
---

# ADR-0002: SQLite derived registry

## Context

Need a local rebuildable store after SCIP + stereotype merge. Candidates:
LanceDB, Kuzu, Neo4j, Datascript, SQLite. QAS determinism/latency + local-first
apply. Tradeoff: SQL joins vs recursive graph ask.

## Decision

**SQLite** is the derived registry for beans/edges. Schema is SoR; accessed via
rusqlite (Rust), and other language bindings as adapters. Datascript consumes
**EDN export** (ADR-0005). Not LanceDB/Kuzu as symbol SoR.

## Status

Proposed.

## Consequences

Positive: single-file rebuild; goldens.  
Negative: recursive queries via export.  
Rejected: embeddings as identity; multi-writer embedded graph behind LB.
