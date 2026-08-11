---
title: 'ADR-003: Native LockCheck first; WASM as capability trust boundary'
status: Proposed
date: '2026-08-10'
adr: ADR-003
related:
  - docs/design/adr/README.md
  - docs/research/process/54-e-lie0-atam-qas-adr-formal-boundaries-2026-08-10.md
claim_tiers: Evidenced
last_reviewed: '2026-08-10'
---

# ADR-003: Native LockCheck first; WASM trust boundary

## Context

QAS latency vs security isolation tradeoff. WASM has mechanised type soundness
(Watt/WasmCert) and capability-safety research (Iris-MSWasm for MSWasm); Wasmtime
provides engineering fuel/epoch + deny-by-default WASI. Claiming “proved guest”
without in-tree proofs would be false advertising.

## Decision

We will implement **native LockCheck first** (Accept for Must). We will Pilot
a **WASM guest** as a **capability trust boundary** (no FS/net; fuel limits)
with **parity tests** vs native. Diagrams may say `trust-boundary`; they must
**not** say `proved` unless an FML ticket lands machine-checked artifacts.

## Status

Proposed.

## Consequences

Positive: honest security story; latency QAS measurable on native path.  
Negative: dual implementations until parity; WASM may fail keep/drop.  
Rejected: WASM-by-default verify; equating Wasmtime host with Iris proof of our IR.
