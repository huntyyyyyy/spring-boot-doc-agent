---
title: 'Architecture Decision Record ADR-0007: Rust owns the engine container'
status: Proposed
date: '2026-08-10'
---

# Architecture Decision Record ADR-0007: Rust owns the engine container

## Context

Engine work (Source Code Index Protocol decode, resolve, lock evaluate, receipts, wasmtime host)
fits Rust’s excellence domain. Polyglot peers integrate via command-line interface/FFI/WIT — not
by making Python the engine.

## Decision

**Rust** owns the primary **engine** container (`crates/`). Other languages
call it (Go daemon, TS IDE, Ruby DX, Clojure queries against exports, optional
PyO3 bridge as peer).

## Status

Proposed.

## Consequences

Positive: clear ownership; path to Verus/Kani on pure cores later.  
Negative: Rust skill floor; FFI surface.  
Rejected: Python-majority engine; engine logic reimplemented per language.
