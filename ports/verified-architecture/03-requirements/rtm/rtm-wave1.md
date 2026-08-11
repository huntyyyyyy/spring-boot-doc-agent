---
title: Requirements Traceability Matrix — wave-1
status: DRAFT
date: '2026-08-10'
---

# Requirements Traceability Matrix wave-1

| Need | REQ | Design | Accept | Gap |
| --- | --- | --- | --- | --- |
| No hallucinated beans | F-01, F-02, F-07 | Resolver; Unknown taxonomy | Multi-impl → Unknown | OPEN plants |
| Graph cycles / layers | F-03, F-04, F-05 | Registry + LockCheck | Fixture fails controller→repo | OPEN Interface Control Document ICD-LOCK |
| Explainable + fresh | F-06, F-06b | Receipt schema | Schema-valid + digest bind | PARTIAL draft |
| Claim drift honesty | F-06c | Artifact-Anchored Verification Memory ClaimMemory | Quality Attribute Scenario QAS-N-07 | PARTIAL specification draft |
| Typed tools | F-09b, F-09c | Stateful Tool-Enabled Agentic Deployment + harness Interface Control Document | Quality Attribute Scenario QAS-N-08 | PARTIAL specification draft |
| Shared policy | F-08, F-12 | Locks in git; Language Server Protocol later | Same violation ID | OPEN Wave 2 |
| Single oracle | F-09 | Architecture Decision Record ADR-0006 | One writer in CI (**Rust**) | PARTIAL Architecture Decision Record |
| Privacy | Quality Attribute Scenario QAS-N-05 | Local-first CON-03 | Deny-net harness | Measures ready; awaiting Accept |
| Determinism | Quality Attribute Scenario QAS-N-06 | Must spine | Canonical JSON 2×5 | Measures ready; awaiting Accept |
| Latency Must | Quality Attribute Scenario QAS-N-01 / QAS-N-02 | — | Spike PIL-LAT-* | **blocks Design** |

Fail-mode: marking a Gap READY without the Accept column’s method existing on disk → reject soft-pass.
