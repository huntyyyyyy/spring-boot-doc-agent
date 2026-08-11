---
title: 'Architecture Decision Record ADR-0006: Single deterministic gate writer (language-neutral)'
status: Proposed — amended 2026-08-11 (writer ≠ Python)
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Record ADR-0006: Single deterministic gate writer

## Context

Former framing (“Python tip remains coverage writer”) encoded **legacy tip
history**, not a polyglot product law. The invariant is **single writer**.

## Decision

At most **one** process/language writes the merge oracle / deterministic gate
artifacts at a time. Writer language is chosen after engine Spike — **Working
hypothesis: Rust** (align Architecture Decision Record ADR-0007).

**Refuse:** Python as default or silent coverage/oracle writer for this port.

## Status

Proposed (amended). **Supersedes** planning-workspace “Python remains writer”
framing for *this* product.

## Consequences

Positive: language-neutral invariant; cutover explicit.  
Negative: must implement Rust (or Accepted façade) writer before merge gates.  
Rejected: dual Cover%/gate writers; Python re-center.
