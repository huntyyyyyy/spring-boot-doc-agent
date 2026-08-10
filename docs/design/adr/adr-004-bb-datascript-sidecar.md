---
title: 'ADR-004: Babashka + Datascript as query sidecar'
status: Proposed
date: '2026-08-10'
adr: ADR-004
related:
  - docs/design/adr/README.md
  - docs/research/process/53-e-lie0-pilot-mental-models-polyglot-lanes-2026-08-10.md
  - docs/design/adr/adr-001-sqlite-registry.md
claim_tiers: Evidenced
last_reviewed: '2026-08-10'
---

# ADR-004: bb + Datascript query sidecar

## Context

SQLite (ADR-001) optimizes deterministic verify joins; architects still want
recursive “who depends on X?” asks. Datascript offers in-memory EAV+Datalog;
Babashka offers fast script host with optional Datascript feature. Tradeoff:
rich queries vs dual-view drift.

## Decision

We will Pilot **EDN export from SQLite → Babashka Datascript** as a **sidecar
brain**, with golden tests that Datalog answers match SQL for a fixed query
set. Sidecar must not write coverage/claims.

## Status

Proposed.

## Consequences

Positive: unique architecture REPL without Neo4j.  
Negative: binary/feature availability Unknown until Spike; drift risk.  
Rejected: Datascript as merge SoR; full JVM Clojure service in v1.
