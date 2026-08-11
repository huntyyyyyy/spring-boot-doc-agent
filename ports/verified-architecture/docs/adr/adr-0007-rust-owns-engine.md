---
title: 'Architecture Decision Record ADR-0007: Rust owns the engine container'
status: Proposed — amended 2026-08-11 (engine + Spec corpus MCP; no PyO3 default)
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/01-engine-rust
---

# Architecture Decision Record ADR-0007: Rust owns the engine container

## Context

Source Code Index Protocol decode, resolve, lock evaluate, receipts, and
wasmtime hosting need one language with strong FFI and a path to later formal
cores. Spec corpus indexing (frontmatter validate, digests, read-only Model
Context Protocol) shares those needs. Tip Python and PyO3 were tempting only
because the monorepo tip already used them — not because of product forces.

## Decision

1. **Rust** is the only language allowed to implement engine effects and the
   Spec corpus Model Context Protocol Spike host (`SPIKE-SPEC-MCP-0`).  
2. Go / TypeScript / Ruby / Clojure call the engine across process or export
   boundaries; they do not reimplement verify oracles.  
3. **Refuse** Python engine, Spec host, and default PyO3 bridge for this port.

## Status

Proposed (amended). Human Accept pending.

## Consequences

Positive: one ownership line for digests/schemas; future Verus/Kani possible on
pure cores.  
Negative: higher Rust skill floor; no PyO3 shortcut for ACI glue.  
Rejected: Python-majority engine; “host in tip language because adapters exist.”
