---
title: 'ADR-001: SQLite as Pilot bean/dep registry'
status: Proposed
date: '2026-08-10'
adr: ADR-001
related:
  - docs/design/adr/README.md
  - docs/research/process/54-e-lie0-atam-qas-adr-formal-boundaries-2026-08-10.md
  - docs/research/process/53-e-lie0-pilot-mental-models-polyglot-lanes-2026-08-10.md
claim_tiers: Evidenced / Confirmed
last_reviewed: '2026-08-10'
---

# ADR-001: SQLite as Pilot bean/dep registry

## Context

E-LIE0 needs a local derived store for beans/edges after SCIP+stereotype merge.
Candidates included LanceDB (vectors), Kuzu (embedded graph), Neo4j (server),
Datascript (ephemeral EAV), and SQLite. QAS latency/determinism and
constraint “local-first, rebuildable derived data” apply. ATAM tradeoff:
query flexibility vs deterministic verify joins.

## Decision

We will use **SQLite** as the Pilot **derived** registry for beans and
dependency edges. Datascript may consume an **EDN export** as a query sidecar
(ADR-004). We will **not** use LanceDB or Kuzu as symbol/verify SoR.

## Status

Proposed.

## Consequences

Positive: single-file rebuild; SQL goldens; tip-friendly.  
Negative: less natural recursive graph ask in-SQL; need EDN export for bb.  
Neutral: aligns with SCIP “transmission → consumer store” mental model.  
Rejected: LanceDB (cosine ≠ identity); Kuzu multi-instance LB (unsuitable).
