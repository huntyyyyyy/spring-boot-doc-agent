---
title: 'Architecture Decision Record ADR-0006: Single deterministic gate writer (language-neutral)'
status: Proposed — amended 2026-08-11 (writer ≠ Python)
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Record ADR-0006: Single deterministic gate writer

## Context

Former framing (“Python tip remains coverage writer”) encoded tip history, not
a polyglot product law. Parallel Cover%/gate writers make merge proof
ambiguous.

## Decision

At most **one** process writes merge-oracle / deterministic gate artifacts at a
time. Writer language follows the engine Spike — **Working hypothesis: Rust**
(Architecture Decision Record ADR-0007). Dual writers or a silent Python
coverage writer fail this Architecture Decision Record.

**Refuse:** Python as default or silent coverage/oracle writer for this port.

## Status

Proposed (amended). **Supersedes** planning-workspace “Python remains writer”
for *this* product.

## Consequences

Positive: language-neutral invariant; cutover must be explicit.  
Negative: Rust (or Accepted façade) writer must land before merge gates can
turn green.  
Rejected: dual Cover%/gate writers; Python re-center.
