---
title: 'Architecture Decision Record ADR-0005: Clojure graph brain bounded context'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/05-graph-clojure
---

# Architecture Decision Record ADR-0005: Clojure / Babashka Datascript graph brain

## Context

Architects need interactive graph ask over derived facts without making an
embedded graph the multi-writer System of Record.

## Decision

**Clojure / Babashka + Datascript** queries **EDN export** from the SQLite
registry (Architecture Decision Record ADR-0002). Read-mostly. Writing merges
or oracle artifacts from the graph brain fails Architecture Decision Record
ADR-0006.

## Status

Proposed.

## Consequences

Positive: strong interactive query developer experience.  
Negative: export lag / sync contract must be explicit.  
Rejected: Neo4j-as-System-of-Record; Python notebook as graph System of
Record.
