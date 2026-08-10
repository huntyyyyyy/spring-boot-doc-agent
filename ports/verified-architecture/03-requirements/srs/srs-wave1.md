---
title: SRS — MoSCoW wave-1
status: DRAFT — awaiting human Accept
date: '2026-08-10'
---

# SRS — Functional requirements (wave-1)

Implementation-free. Languages live in ADRs / options/, not REQ text.

## Must

| ID | Statement |
| --- | --- |
| REQ-F-01 | Query injection/type → bound impl **or** Unknown/unprovable + reason code |
| REQ-F-02 | Multi-candidate under static model ⇒ Unknown (no silent winner) |
| REQ-F-03 | Build virtual dependency graph from resolved + lock package edges |
| REQ-F-04 | Detect cycles; report offending edge sets |
| REQ-F-05 | Evaluate architecture locks; report violations with lock IDs |
| REQ-F-06 | Every verify emits proof-tour receipt with required witnesses (**no LLM/RAG in witnesses**) |
| REQ-F-06b | Receipts are freshness-bound to content digests; stale/tampered receipts rejected (Proof-or-Stop) |
| REQ-F-06c | Persist EA-Graph claims with anchors; withdrawal → unaffected\|affected\|unprovable |
| REQ-F-07 | Failure taxonomy includes: unknown, ambiguous, stale, conflict, unprovable |
| REQ-F-08 | Locks versioned in git; no index/claim-DB blob as team SoR |
| REQ-F-09 | Exactly one deterministic merge-gate writer at a time |
| REQ-F-09b | MCP/CLI entity parameters are typed ids from Registry/SCIP/claims — harness rejects unknowns (STEAD ST-1…5) |
| REQ-F-09c | Harness decides accept/reject; agent proposes only (Aria / Contracts) |

## Should

| ID | Statement |
| --- | --- |
| REQ-F-10 | Refuse verify when index digest ≠ declared source revision |
| REQ-F-11 | Packwerk-like package deps as executable checks |
| REQ-F-12 | LSP diagnostics = same violation IDs as CLI |
| REQ-F-13 | Proof tours clickable in IDE |

## Could

| ID | Statement |
| --- | --- |
| REQ-F-14 | Ghost prefetch (embeddings not SoR) |
| REQ-F-15 | Cross-language bridges via explicit SoR |
| REQ-F-16 | WASM sandbox guests |
| REQ-F-20 | NL remediation (non-witness) |
| REQ-F-22 | HyperTool-style MCP composition blocks over primitive schemas |
| REQ-F-23 | Cue-anchored working-memory delivery (≠ claim store) |

## Won’t (wave-1)

| ID | Statement |
| --- | --- |
| REQ-F-17 | SMT proof of Spring DI as Must |
| REQ-F-18 | Vector/RAG as proof of binding |
| REQ-F-19 | Two concurrent merge-oracle writers |
| REQ-F-24 | FO-CTL “proved agent” without STEAD Spike exit |
