---
title: 'Architecture Decision Record ADR-0004: Native LockCheck then WebAssembly trust boundary'
status: Proposed — amended 2026-08-11 (WASM guest = Could / Wave-3)
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/06-sandbox-wasm
---

# Architecture Decision Record ADR-0004: Native then WebAssembly LockCheck

## Context

Quality Attribute Scenario latency fights isolation. WebAssembly has
mechanised soundness literature; Wasmtime offers fuel/epoch. Labeling a guest
“proved” without formal artifacts is false. Spec corpus Model Context Protocol
must not depend on a WebAssembly host.

## Decision

1. **Must path:** native **LockCheck** in Rust (Architecture Decision Record
   ADR-0007) ships first.  
2. **WebAssembly guest** LockCheck = **Could / Wave-3** capability boundary
   with parity tests — not Pilot-as-Must, not Spec day-one.  
3. Diagrams may say `trust-boundary` only; `proved` requires landed formal
   artifacts.  
4. **Refuse:** WebAssembly as Spec corpus Model Context Protocol host —
   reject the change.

## Status

Proposed (amended).

## Consequences

Positive: security claims stay honest; Spec Model Context Protocol stays
Rust-native and measurable.  
Negative: dual LockCheck paths exist only after Wave-3 earns the guest.  
Rejected: WebAssembly-by-default Must; Pilot tone implying near-term Must;
equating host config with Iris proof of our Intermediate Representation;
WebAssembly Spec Model Context Protocol host.
