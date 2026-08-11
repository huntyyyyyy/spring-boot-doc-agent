---
title: 'Architecture Decision Record ADR-0001: Polyglot-first product identity'
status: Proposed — amended 2026-08-11 (Python runtime Refuse)
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Record ADR-0001: Polyglot-first product identity

## Context

Prior planning lived beside a Python monorepo tip and drifted toward
“Python tip + sidecars,” then “optional Python ACI peer.” Stakeholders require a
**polyglot** product **without** a Python runtime lane for this port: Rust engine,
WebAssembly guests, SQLite, Go, Ruby, Clojure, TypeScript IDE/Model Context
Protocol, C when necessary, Zig when earned.

## Decision

**Polyglot-first** is product identity. Each **accepted** language owns a
first-class bounded context (see C4 Containers).

**Refuse (2026-08-11):** Python as Spec Model Context Protocol host, product ACI
container, coverage/oracle writer identity, or default PyO3 bridge for this port.
Nest `nests/08-aci-python-peer/` is tombstoned.

## Status

Proposed (amended).

## Consequences

Positive: ends circular tip-Python Why; Rust owns engine + Spec corpus serving.  
Negative: no Python glue convenience — orchestration stays Rust/Go/TS.  
Rejected: Python-majority product; Python-as-optional-hub; tip `adapters/mcp`
Python as Spec SoT for this port.
