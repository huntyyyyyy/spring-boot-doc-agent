---
title: 'Architecture Decision Record ADR-0005: Clojure graph brain bounded context'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/05-graph-clojure
---

# Architecture Decision Record ADR-0005: Clojure / Babashka Datascript graph brain

## Context

Architects need interactive graph ask over derived facts without making the
embedded graph the multi-writer System of Record.

## Decision

**Clojure / Babashka + Datascript** owns the graph-brain bounded context over
**EDN export** from the SQLite registry (Architecture Decision Record ADR-0002).
Read-mostly; not the merge oracle.

## Status

Proposed.

## Consequences

Positive: strong query DX.  
Negative: export lag / sync contract.  
Rejected: Neo4j-as-SoR; Python notebook as graph SoT.
