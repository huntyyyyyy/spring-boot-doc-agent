---
title: 'Architecture Decision Record ADR-0004: Native LockCheck then WebAssembly trust boundary'
status: Proposed — amended 2026-08-11 (WASM guest = Could / Wave-3)
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

1. **Must path:** native **LockCheck** in Rust (Architecture Decision Record
   ADR-0007) first.  
2. **WebAssembly guest** LockCheck = **Could / Wave-3** capability trust
   boundary with parity tests — **not** Pilot-as-Must, **not** Spec day-one.  
3. Diagrams: `trust-boundary`, not `proved`, unless formal artifacts land.  
4. **Refuse:** WebAssembly as Spec corpus Model Context Protocol host.

## Status

Proposed (amended).

## Consequences

Positive: honest security + measurable latency; Spec MCP stays Rust-native.  
Negative: dual paths only if/when Wave-3 earns the guest.  
Rejected: WebAssembly-by-default Must; Pilot tone implying near-term Must;
equating host config with Iris proof of our Intermediate Representation;
WASM Spec MCP host.
