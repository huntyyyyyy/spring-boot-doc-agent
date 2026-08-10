---
title: 'Architecture Decision Record ADR-0004: Native LockCheck then WebAssembly trust boundary'
status: Proposed
date: '2026-08-10'
---

# Architecture Decision Record ADR-0004: Native then WebAssembly LockCheck

## Context

Quality Attribute Scenario latency vs isolation. WebAssembly has mechanised soundness literature
(Watt/WasmCert) and capability-safety research (Iris-MSWasm); Wasmtime provides
fuel/epoch. Claiming “proved guest” without artifacts is false.

## Decision

Implement **native LockCheck** (Rust) first for Must Accept. Pilot **WebAssembly guest**
as capability trust boundary with parity tests. Diagrams: `trust-boundary`, not
`proved`, unless FML artifacts land.

## Status

Proposed.

## Consequences

Positive: honest security + measurable latency.  
Negative: dual paths until parity.  
Rejected: WebAssembly-by-default Must; equating host config with Iris proof of our IR.
