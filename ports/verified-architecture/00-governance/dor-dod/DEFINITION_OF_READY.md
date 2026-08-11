---
title: Definition of Ready — wave before AI product code generation
status: ACTIVE
last_reviewed: '2026-08-11'
honesty_note: >-
  Prior Port Ready language overstated research depth. Row D0 added.
  Zero Implement rows are PASS. Sensor refresh 2026-08-11: digest count and
  MCP schema/plant paths updated — D0 still FAIL on exact adopters / missing
  Must-spine digests. See research/gaps/entity-adoption-audit-2026-08-10.md.
---

# Definition of Ready

| Bar | Predicate | Bound |
| --- | --- | --- |
| **Implement Ready** | Every row below PASS or WAIVED with human signer in `SIGNOFF_LOG.md` | **0 PASS today** → product crates forbidden |
| **Port Ready** | Folder coherent enough to export for *more* specification work | Does **not** imply research-complete or D0 green — see `PORT_READY.md` |

Whole words — `GLOSSARY.md`. FREEZE: deepen receipt β/ρ, claim withdrawal, handle lifecycle only — new Must entities / Decision Matrices → reject.

## Honest status (2026-08-11)

| # | Predicate | Evidence | Status | What is still left |
| --- | --- | --- | --- | --- |
| **D0** | Per-entity research: paper **digests** (type key + sections + related walk) then ≥5 genuine GitHub algorithm adopters | `research/papers-2026-may-aug/digests/` (**4** files: 2607.14890, 2607.20531, 2608.03609, 2608.04278) + adoption audit + shallow-decisions-honesty | **FAIL** | Digests landed for Proof-or-Stop / DynamicMCPBench / STEAD / EA-Graph; still **Absent**: 2607.08028, 2607.20972, 2607.06341 (and others if Design-pressure). Exact public engines = **0** for claim memory / Proof-or-Stop product / STEAD wrap → keep Pilot invent; FREEZE deepen-3 |
| D1 | Product boundary draft Accepted | `01-vision/.../BOUNDARY.md` | **FAIL** for Implement (draft only) | Human Accept in `SIGNOFF_LOG.md` |
| D2 | Wave Must Stakeholder + Software Requirements Specifications named and Accepted | `03-requirements/strs\|srs` | **PARTIAL** | Drafts exist; no human Accept; Requirements Traceability Matrix still Draft |
| D3 | Must non-functional requirements as six-part Quality Attribute Scenarios | `03-requirements/qas/` | **PARTIAL** | N-05…N-08 drafted; **N-01/N-02 latency still Spike-blocked**; open question OQ-07 still OPEN |
| D4 | Constraints ledger Accepted | `04-constraints/technical/constraints-wave1.md` | **PARTIAL** | Draft only |
| D5 | `blocks_code` open questions closed or waived | `open-questions/` | **FAIL** | open question OQ-01…08 all SPIKE or OPEN; every one still `blocks_code: true` |
| D6 | System of Record matrix Accepted | `sor-derived-matrix.md` | **PARTIAL** | Draft; open question OQ-02 blocks |
| D7 | Ports + Interface Control Document stubs Accepted | `PORTS.md`, `icd/*` | **PARTIAL** | ICD drafts + JSON Schemas on disk; **no human Accept**; stability Spikes missing. (Same predicate as ICD README: PARTIAL until Accept — not a second FAIL.) |
| D8 | C4 Context + Container current | `07-system-design/c4/C4-BRIEF-CONFIDENCE.md` (+ legacy `docs/c4/`) | **PARTIAL** | Draft + confidence scores = shape sensors only; not human Accepted; scores ≠ Implement readiness |
| D8b | Model Context Protocol transport requirements gathered | `icd/mcp-tools.md` + `icd/mcp/*.schema.json` + `decisions/mcp-decision-matrix.md` | **PARTIAL** | Schemas + UC-Model Context Protocol-01…08 **present**; still missing human Accept + Tier-1 live scorer |
| D9 | Architecture Decision Records / brief Accepted | `ARCHITECTURE_BRIEF.md` | **PARTIAL** | Draft; leaders table needs refresh after D0 audit |
| D10 | Receipt schema Accepted + Spike on freshness keys | `icd/receipt.schema.json` (SoT) | **PARTIAL** | ICD schema has β/ρ-shaped fields; open question OQ-05; Proof-or-Stop public engine **0**; draft markdown is pointer-only |
| D10b | Artifact-anchored claim specification + schema Accepted | `claim-memory/`, `ea-graph-claims.schema.json` | **PARTIAL** + **research gap** | Specification text exists; **zero genuine public implementations of this algorithm** found; Pilot/Spike required before “Must implement” can be honest |
| D10c | Stateful Tool-Enabled Agentic Deployment constraints in Model Context Protocol Interface Control Document | `stead/`, `mcp-tools.md`, digest `2608.03609` | **PARTIAL** + **research gap** | ST-1…5 + handle schemas **present**; equivariance wrap engines = **0**; Spike charter only |
| D11 | Verification and Validation Accept methods + real plants | `vv-plan/` + `plants/mcp-effects/` FX-MCP-01…06 | **PARTIAL** | Draft TaskSpecs **on disk**; Tier-1 scorer / measured Accept **absent** |
| D12 | Human wave Approve | `signoff/SIGNOFF_LOG.md` | **FAIL** | All rows pending |

## Counts (do not soft-pass)

- **PASS:** 0  
- **PARTIAL:** most Draft rows  
- **FAIL:** D0, D1 (for Implement), D5, D12  

## Ordered next actions (cold agent)

1. Close D0 honesty — paper *content* digests + ≥5 genuine repos **or** mark Unknown/invent/Pilot (no Must=Adopt fiction).  
2. Human Accept: boundary, System of Record matrix, requirements, schemas (D1, D2, D4, D6, D7, D10*).  
3. Close or waive open questions OQ-01…08 (D5) — lock Intermediate Representation (OQ-04), freshness budgets (OQ-06), bounded contexts (OQ-08).  
4. Spike latency Quality Attribute Scenarios **or** demote latency from Must (D3).  
5. Build plants; run Accept methods (D11).  
6. Wave Approve (D12) → only then may Implement start (**Rust** engine; **Refuse Python** hosts).
