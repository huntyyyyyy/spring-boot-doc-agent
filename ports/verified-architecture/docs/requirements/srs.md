---
title: SRS — Software Requirements Specification (MoSCoW)
status: DRAFT
date: '2026-08-10'
---

# SRS — Functional requirements

Implementation-free. Language choices live in ADRs / C4, not REQ text.

## Must (v1)

| ID | Statement |
| --- | --- |
| **REQ-F-01** | Query injection/type → bound impl **or** `Unknown` + reason code |
| **REQ-F-02** | Multi-candidate under static model ⇒ `Unknown` (no silent winner) |
| **REQ-F-03** | Build virtual dependency graph from resolved edges + lock package edges |
| **REQ-F-04** | Detect cycles; report offending edge sets |
| **REQ-F-05** | Evaluate architecture locks; report violations with lock IDs |
| **REQ-F-06** | Every verify/deny emits proof-tour receipt with required witness IDs |
| **REQ-F-07** | Failure taxonomy includes at least: unknown, ambiguous, stale, conflict |
| **REQ-F-08** | Locks are versioned text under git; no index blob distribution required |
| **REQ-F-09** | Exactly one deterministic merge-gate writer at a time (language per ADR) |

## Should

| ID | Statement |
| --- | --- |
| **REQ-F-10** | Refuse verify when index digest ≠ declared source revision (strict) |
| **REQ-F-11** | Packwerk-like package deps + public API folders as executable checks |
| **REQ-F-12** | Human editors get same lock violations (LSP/diagnostics) |
| **REQ-F-13** | Proof tours render as clickable steps |

## Could

| ID | Statement |
| --- | --- |
| **REQ-F-14** | Ghost prefetch without treating embeddings as SoR |
| **REQ-F-15** | Cross-language impact via bridge SoR (e.g. OpenAPI) |
| **REQ-F-16** | Capability-sandboxed lock-check guests (WASM) |
| **REQ-F-20** | NL remediation suggestions via configurable local inference (not a witness) |
| **REQ-F-21** | Org-wide query API if shared-state SoR is explicit |

## Won’t (this wave)

| ID | Statement |
| --- | --- |
| **REQ-F-17** | SMT “proof” of Spring bean wiring as Must |
| **REQ-F-18** | Vector/RAG recall as proof of a binding |
| **REQ-F-19** | Two concurrent merge-oracle writers |
