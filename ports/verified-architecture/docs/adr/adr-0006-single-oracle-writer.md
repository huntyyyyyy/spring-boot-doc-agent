---
title: 'ADR-0006: Single deterministic gate writer (language-neutral)'
status: Proposed
date: '2026-08-10'
---

# ADR-0006: Single deterministic gate writer

## Context

Former ADR “Python tip remains coverage writer” encoded **legacy tip history**,
not a polyglot product law. The invariant is **single writer**, not Python.

## Decision

At most **one** process/language writes the merge oracle / deterministic gate
artifacts at a time. Initial writer language is chosen in a follow-on ADR after
engine Spike (likely Rust or a thin façade). Python may write only if explicitly
Accepted — it is **not** the default identity of this repo.

## Status

Proposed. **Supersedes** the planning workspace ADR-005 framing for *this*
product.

## Consequences

Positive: preserves shippability without Python-majority lock-in.  
Negative: cutover must be explicit.  
Rejected: dual Cover%/gate writers; silent Python re-center.
