---
title: 'Architecture Decision Record ADR-0010: TypeScript owns IDE and Model Context Protocol presentation'
status: Proposed — amended 2026-08-11 (presentation only; Spec corpus ≠ TS)
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Record ADR-0010: TypeScript IDE / Model Context Protocol presentation

## Context

Language Server Protocol diagnostics and verification panels live in editor
ecosystems. Model Context Protocol **clients** are often TypeScript. Engine
effects and Spec corpus indexes remain Rust.

## Decision

**TypeScript** owns IDE extension surfaces and Model Context Protocol
**presentation** (panels, client wiring) talking to the engine via stdio/HTTP
or local protocol. It must not write merge oracle artifacts.

**Out of scope for TypeScript:** Spec corpus Model Context Protocol **server**
(Architecture Decision Record ADR-0007 + Spike `SPIKE-SPEC-MCP-0` — **Rust**).
Shipping Spec host in TypeScript as default = reject.

Protocol pin, verify-tool primitives, and handles: Architecture Decision
Record ADR-0011 + `07-system-design/decisions/mcp-decision-matrix.md`.

## Status

Proposed (amended).

## Consequences

Positive: natural editor developer-experience surface.  
Negative: Node toolchain required for extensions only.  
Rejected: IDE UX through Python; verify oracle in TypeScript; Spec corpus
Model Context Protocol host in TypeScript as default.
