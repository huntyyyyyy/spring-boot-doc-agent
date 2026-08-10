---
title: Definition of Ready — wave before AI product code generation
status: ACTIVE
last_reviewed: '2026-08-10'
honesty_note: >-
  Prior Port Ready language overstated research depth. Row D0 added.
  Zero Implement rows are PASS. See research/gaps/entity-adoption-audit-2026-08-10.md.
---

# Definition of Ready

**Implement Ready** = every row PASS or WAIVED with human signoff.  
**Port Ready** (export the planning folder) is a weaker bar — and even that was
overstated on research depth. See `PORT_READY.md`.

Whole words — `GLOSSARY.md`.

## Honest status (2026-08-10)

| # | Predicate | Evidence | Status | What is still left |
| --- | --- | --- | --- | --- |
| **D0** | Per-entity research: recent papers **understood**, then mapped to **≥5 genuine GitHub repositories** that ship the algorithms (anti-bogus filter) | `research/gaps/entity-adoption-audit-2026-08-10.md` | **FAIL** | Artifact-anchored claim memory and Stateful Tool-Enabled Agentic Deployment equivariance wrappers have **no** verified public algorithm adopters yet; prior memo was title→action mapping, not adoption audit |
| D1 | Product boundary draft Accepted | `01-vision/.../BOUNDARY.md` | **FAIL** for Implement (draft only) | Human Accept in `SIGNOFF_LOG.md` |
| D2 | Wave Must Stakeholder + Software Requirements Specifications named and Accepted | `03-requirements/strs|srs` | **PARTIAL** | Drafts exist; no human Accept; Requirements Traceability Matrix still Draft |
| D3 | Must non-functional requirements as six-part Quality Attribute Scenarios | `03-requirements/qas/` | **PARTIAL** | N-05…N-08 drafted; **N-01/N-02 latency still Spike-blocked**; open question 07 still OPEN |
| D4 | Constraints ledger Accepted | `04-constraints/technical/constraints-wave1.md` | **PARTIAL** | Draft only |
| D5 | `blocks_code` open questions closed or waived | `open-questions/` | **FAIL** | OQ-01…08 all SPIKE or OPEN; every one still `blocks_code: true` |
| D6 | System of Record matrix Accepted | `sor-derived-matrix.md` | **PARTIAL** | Draft; OQ-02 blocks |
| D7 | Ports + Interface Control Document stubs Accepted | `PORTS.md`, `icd/*` | **PARTIAL** | Schemas drafted; no Accept; stability Spikes missing |
| D8 | C4 Context + Container current | `docs/c4/` (legacy) or `07-system-design/` | **PARTIAL** | Still largely legacy; not re-homed / Accepted against Must spine |
| D9 | Architecture Decision Records / brief Accepted | `ARCHITECTURE_BRIEF.md` | **PARTIAL** | Draft; leaders table needs refresh after D0 audit |
| D10 | Receipt schema Accepted + Spike on freshness keys | `icd/receipt.schema.json` | **PARTIAL** | Draft; OQ-05; Proof-or-Stop public engine **not found** as a genuine repo |
| D10b | Artifact-anchored claim specification + schema Accepted | `claim-memory/`, `ea-graph-claims.schema.json` | **PARTIAL** + **research gap** | Spec text exists; **zero genuine public implementations of this algorithm** found; Pilot/Spike required before “Must implement” can be honest |
| D10c | Stateful Tool-Enabled Agentic Deployment constraints in Model Context Protocol Interface Control Document | `stead/`, `mcp-tools.md` | **PARTIAL** + **research gap** | Constraint list drafted; **no public equivariance-wrapper / First-Order Computation Tree Logic STEAD checker adopters**; ST-1…5 are design bets, not Adopt-from-field |
| D11 | Verification and Validation Accept methods + real plants | `vv-plan/` | **PARTIAL** | Fixture *names* only; no plants; no measured Accept |
| D12 | Human wave Approve | `signoff/SIGNOFF_LOG.md` | **FAIL** | All rows pending |

## Counts (do not soft-pass)

- **PASS:** 0  
- **PARTIAL:** most Draft rows  
- **FAIL:** D0, D1 (for Implement), D5, D12  

## What “left” means in practice (ordered)

1. **Close D0 research honesty** — finish entity packs with paper *content* + ≥5 genuine repos *or* explicitly mark algorithm as **Unknown / invent / Pilot** (do not pretend Must = Adopt).
2. **Human Accept** boundary, System of Record matrix, requirements, schemas (D1, D2, D4, D6, D7, D10*).
3. **Close or waive open questions 01–08** (D5) — especially lock Intermediate Representation (04), freshness budgets (06), bounded contexts (08).
4. **Spike latency Quality Attribute Scenarios** or demote latency from Must (D3).
5. **Build plants** and run Accept methods (D11).
6. **Only then** wave Approve (D12) → Implement may start.

**Port Ready** may still mean “folder is coherent enough to export for *more Spec work*.” It does **not** mean research or Definition of Ready is green.
