---
title: minimum viable product and follow-on waves
status: DRAFT
date: '2026-08-10'
---

# Delivery waves

See also `07-system-design/ARCHITECTURE_BRIEF.md` §6.

| Wave | Name | Ships | Explicitly not |
| --- | --- | --- | --- |
| **W0** | Spec | Boundary, Quality Attribute Scenario, System of Record, ports, Interface Control Document drafts, Definition of Ready | Code |
| **W1** | minimum viable product verify command-line interface | Source Code Index Protocol ingest, SQLite graph, resolve+Unknown/unprovable, locks, receipts (evidence≠freshness) | Language Server Protocol, WebAssembly, Z3, polyglot bell, agent-memory DB |
| **W2** | IDE parity | Language Server Protocol squiggles, proof-tour panel v0, git lock sync docs | Ghost prefetch |
| **W3** | Enrichment | Go watch, bb graph, optional WebAssembly package; optional AgentMemory port | Org SaaS |
| **W4** | Proof+ / polyglot / blueprint | Z3 on lock FOL; Kani on engine; AOCI-like L1 blueprint; Stateful Tool-Enabled Agentic Deployment equivariance Spike | Science hardware |

## minimum viable product Accept (W1)

On a fixture plant: controller→repo lock violation fails CI/command-line interface with receipt
citing lock id + edge witness; multi-impl without qualifier yields Unknown
(not a guessed bean).
