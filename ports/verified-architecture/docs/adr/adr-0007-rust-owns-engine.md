---
title: 'Architecture Decision Record ADR-0007: Rust owns the engine container'
status: Proposed — amended 2026-08-11 (no PyO3 peer default)
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Record ADR-0007: Rust owns the engine container

## Context

Engine work (Source Code Index Protocol decode, resolve, lock evaluate, receipts,
wasmtime host) and Spec corpus Model Context Protocol (frontmatter index, digests)
fit Rust’s excellence domain. Polyglot peers integrate via command-line interface /
FFI / WIT — **not** by making Python the engine or the default bridge.

## Decision

**Rust** owns the primary **engine** container and the **Spec corpus Model
Context Protocol** Spike host (`SPIKE-SPEC-MCP-0`). Other accepted languages call
it (Go daemon, TypeScript IDE, Ruby DX, Clojure queries against exports).

**Refuse:** Python-majority engine; PyO3 as default planning bridge; Spec host in
tip Python.

## Status

Proposed (amended).

## Consequences

Positive: clear ownership; path to Verus/Kani on pure cores later; one stack for
engine + Spec digest.  
Negative: Rust skill floor; FFI surface without PyO3 convenience.  
Rejected: Python-majority engine; engine logic reimplemented per language; tip
Python Spec server.
