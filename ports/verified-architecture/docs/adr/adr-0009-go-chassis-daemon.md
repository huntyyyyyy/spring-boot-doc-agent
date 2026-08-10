---
title: 'Architecture Decision Record ADR-0009: Go owns watch/reindex chassis'
status: Proposed
date: '2026-08-10'
---

# Architecture Decision Record ADR-0009: Go chassis daemon

## Context

Watch → reindex → stamp freshness is a chassis concern. Cobra/fsnotify fit Go’s
command-line interface/daemon excellence domain.

## Decision

**Go** owns `lie0d` (name TBD): Cobra command-line interface, file watch, reindex triggers, stamp
publication for the engine. Optional wazero for Go-side WebAssembly. Does not own
resolve/lock business logic (Rust).

## Status

Proposed.

## Consequences

Positive: clear chassis bounded context.  
Negative: another CI language.  
Rejected: embedding watch loops inside Rust engine as the only option.
