---
title: 'ADR-0001: Polyglot-first product identity'
status: Proposed
date: '2026-08-10'
---

# ADR-0001: Polyglot-first product identity

## Context

Prior planning lived beside a Python doc-engine and drifted toward
“Python tip + sidecars.” Stakeholders require a **full** polyglot product:
Rust, WASM (+ toolkits), SQLite, Go, Ruby, Clojure, TypeScript, Python as peer,
C when necessary, Zig when earned.

## Decision

We will treat **polyglot-first** as product identity. Each language owns a
first-class bounded context (see C4 Containers). Python is an optional ACI/
glue peer — **not** the majority engine and **not** the identity of the system.

## Status

Proposed.

## Consequences

Positive: matches stakeholder intent; clear ownership.  
Negative: wider toolchain; stricter ADR/CI discipline.  
Rejected: Python-majority doc-engine port as the new tip; demoting Ruby/Clojure/Go to demos.
