---
title: 'Architecture Decision Record ADR-0003: Packwerk-shaped lock IR with Ruby bounded context'
status: Proposed
date: '2026-08-10'
---

# Architecture Decision Record ADR-0003: Packwerk-shaped lock IR (Ruby bounded context)

## Context

Locks must be executable, gradual (`todo` bankruptcy), honest about FN/FP.
Packwerk supplies the mental model. Product is polyglot — Ruby owns lock UX;
engine evaluation may be Rust for speed.

## Decision

Ruby bounded context owns Packwerk-compatible or Packwerk-shaped package manifests and DX.
Executable checks may run in Rust (`packs`-like) and/or Ruby; IR schema is
shared. Not prose-only markdown theater.

## Status

Proposed.

## Consequences

Positive: real modularization playbook; Ruby excellence domain used.  
Negative: dual tooling until IR stabilizes.  
Rejected: “pattern essay only”; requiring tip Ruby runtime for all CI.
