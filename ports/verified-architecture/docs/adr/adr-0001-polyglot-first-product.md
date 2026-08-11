---
title: 'Architecture Decision Record ADR-0001: Polyglot-first product identity'
status: Proposed — amended 2026-08-11 (Python runtime Refuse)
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Record ADR-0001: Polyglot-first product identity

## Context

Planning beside a Python monorepo tip pulled the product toward “Python tip +
sidecars,” then “optional Python ACI peer.” Stakeholders need local-first verify
across Rust, WebAssembly guests, SQLite, Go, Ruby, Clojure, TypeScript
IDE/Model Context Protocol, C when necessary, Zig when earned — without a
Python runtime lane for this port.

## Decision

Every **Accepted** language owns exactly one first-class bounded context (C4
Containers + nest). A language without nest + Architecture Decision Record
fails the no-code gate.

**Refuse (2026-08-11):** Python as Spec Model Context Protocol host, product
ACI container, coverage/oracle writer, or default PyO3 bridge. Nest
`nests/08-aci-python-peer/` stays tombstoned; revival = reject.

## Status

Proposed (amended).

## Consequences

Positive: tip-Python “Why” stops steering container ownership; Rust path for
engine + Spec corpus serving is unblocked.  
Negative: no Python glue — orchestration must stay Rust / Go / TypeScript.  
Rejected: Python-majority product; Python-as-optional-hub; tip
`adapters/mcp` Python as Spec System of Record for this port.
