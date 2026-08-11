---
title: 'Architecture Decision Record ADR-0002: SQLite as derived bean/dep registry'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/02-registry-sqlite
---

# Architecture Decision Record ADR-0002: SQLite derived registry

## Context

After Source Code Index Protocol + stereotype merge, operators need a local
rebuildable bean/edge store. Candidates compared: LanceDB, Kuzu, Neo4j,
Datascript, SQLite. Quality Attribute Scenario determinism/latency and
local-first constrain the choice.

## Decision

**SQLite** holds rebuildable bean/edge rows; schema files are System of Record.
Only the Rust engine writes via **rusqlite**. Other languages use read adapters.
Datascript consumes **EDN export** only (Architecture Decision Record
ADR-0005). A second embedded-graph writer or Python registry owner fails
Architecture Decision Record ADR-0006 / Refuse.

## Status

Proposed.

## Consequences

Positive: single-file rebuild and golden fixtures.  
Negative: recursive / graph queries require export lag contracts.  
Rejected: embeddings as identity; multi-writer embedded graph behind a load
balancer; LanceDB/Kuzu as symbol System of Record; Python-owned registry.
