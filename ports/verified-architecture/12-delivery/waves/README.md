---
title: minimum viable product and follow-on waves
status: DRAFT
date: '2026-08-10'
---

# Delivery waves

Detail: `07-system-design/ARCHITECTURE_BRIEF.md` §6.

| Wave | Ships (Accept surface) | Explicitly not | Fail closed |
| --- | --- | --- | --- |
| **W0** Spec | Boundary, QAS, SoR, ports, ICD drafts, Definition of Ready | Product code | Code before gate → reject |
| **W1** MVP verify CLI | SCIP ingest, SQLite graph, resolve+Unknown, locks, receipts (evidence≠freshness) | LSP, WASM Must, Z3, polyglot bell, agent-memory DB | Soft-pass without receipt digests → fail |
| **W2** IDE parity | LSP squiggles, proof-tour panel v0, git lock sync docs | Ghost prefetch | — |
| **W3** Enrichment | Go watch, bb graph, optional WASM guest; optional AgentMemory port | Org SaaS | WASM guest ≠ Spec MCP host |
| **W4** Proof+ | Z3 lock FOL; Kani; AOCI-like L1; STEAD equivariance Spike | Science hardware | FO-CTL claims without Spike exit → refuse |

## W1 Accept (predicate)

On fixture plant: controller→repo lock violation fails CI/CLI with receipt
citing lock id + edge witness; multi-impl without qualifier → Unknown (not a
guessed bean).
