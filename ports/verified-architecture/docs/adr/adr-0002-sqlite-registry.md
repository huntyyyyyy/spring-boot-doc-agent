---
title: 'Architecture Decision Record ADR-0002: SQLite as derived bean/dep registry'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/02-registry-sqlite
---

# Architecture Decision Record ADR-0002: SQLite derived registry

## Context

Need a local rebuildable store after Source Code Index Protocol + stereotype
merge. Candidates: LanceDB, Kuzu, Neo4j, Datascript, SQLite. Quality Attribute
Scenario determinism/latency + local-first apply.

## Decision

**SQLite** is the derived registry for beans/edges. Schema is System of Record;
accessed via **rusqlite (Rust engine)**. Other languages use adapters only.
Datascript consumes **EDN export** (Architecture Decision Record ADR-0005).
Not LanceDB/Kuzu as symbol System of Record. **Refuse** Python as registry
owner.

## Status

Proposed.

## Consequences

Positive: single-file rebuild; goldens.  
Negative: recursive queries via export.  
Rejected: embeddings as identity; multi-writer embedded graph behind load
balancer; Python-owned registry.
