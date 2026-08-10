---
title: Architecture Decision Records — index
status: ACTIVE — Nygard ADR home for E-LIE0 / tip architecture
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed
related:
  - docs/research/process/54-e-lie0-atam-qas-adr-formal-boundaries-2026-08-10.md
  - docs/design/e-lie0-requirements-2026-08-10.md
  - https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
do_not:
  - Treat diagrams as SoR without citing ADR IDs
  - Reuse ADR numbers
  - Delete superseded ADRs — mark superseded
last_reviewed: '2026-08-10'
---

# Architecture Decision Records

**Format (Nygard):** Title · Context · Decision · Status · Consequences.  
**Rule:** Architecturally significant choices (structure, NFRs, deps, interfaces,
construction) get an ADR before Implement. Methodology:
[`process/54`](../research/process/54-e-lie0-atam-qas-adr-formal-boundaries-2026-08-10.md).

| ID | Title | Status |
| --- | --- | --- |
| [ADR-001](adr-001-sqlite-registry.md) | SQLite as Pilot bean/dep registry | Proposed |
| [ADR-002](adr-002-packwerk-lock-ir.md) | Packwerk-shaped lock IR (pattern) | Proposed |
| [ADR-003](adr-003-native-then-wasm-lockcheck.md) | Native LockCheck first; WASM trust boundary | Proposed |
| [ADR-004](adr-004-bb-datascript-sidecar.md) | bb+Datascript query sidecar | Proposed |
| [ADR-005](adr-005-python-tip-oracle-writer.md) | Python tip remains coverage/claims writer | Proposed |
