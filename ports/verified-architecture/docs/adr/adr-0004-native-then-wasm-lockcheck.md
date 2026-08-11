---
title: 'Architecture Decision Record ADR-0004: Native LockCheck then WebAssembly trust boundary'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/06-sandbox-wasm
---

# Architecture Decision Record ADR-0004: Native then WebAssembly LockCheck

## Context

Quality Attribute Scenario latency vs isolation. WebAssembly has mechanised
soundness literature; Wasmtime provides fuel/epoch. Claiming “proved guest”
without artifacts is false. Spec corpus Model Context Protocol must **not**
require a WebAssembly host.

## Decision

Implement **native LockCheck** (Rust) first for Must Accept. Pilot **WebAssembly
guest** as capability trust boundary with parity tests. Diagrams:
`trust-boundary`, not `proved`, unless formal artifacts land.

**Refuse:** WebAssembly as Spec corpus Model Context Protocol host.

## Status

Proposed.

## Consequences

Positive: honest security + measurable latency.  
Negative: dual paths until parity.  
Rejected: WebAssembly-by-default Must; equating host config with Iris proof of
our Intermediate Representation; WASM Spec MCP host.
