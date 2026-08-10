---
title: MVP and follow-on waves
status: DRAFT
date: '2026-08-10'
---

# Delivery waves

See also `07-system-design/ARCHITECTURE_BRIEF.md` §6.

| Wave | Name | Ships | Explicitly not |
| --- | --- | --- | --- |
| **W0** | Spec | Boundary, QAS, SoR, ports, ICD drafts, DoR | Code |
| **W1** | MVP verify CLI | SCIP ingest, SQLite graph, resolve+Unknown/unprovable, locks, receipts (evidence≠freshness) | LSP, WASM, Z3, polyglot bell, agent-memory DB |
| **W2** | IDE parity | LSP squiggles, proof-tour panel v0, git lock sync docs | Ghost prefetch |
| **W3** | Enrichment | Go watch, bb graph, optional WASM package; optional AgentMemory port | Org SaaS |
| **W4** | Proof+ / polyglot / blueprint | Z3 on lock FOL; Kani on engine; AOCI-like L1 blueprint; STEAD equivariance Spike | Science hardware |

## MVP Accept (W1)

On a fixture plant: controller→repo lock violation fails CI/CLI with receipt
citing lock id + edge witness; multi-impl without qualifier yields Unknown
(not a guessed bean).
