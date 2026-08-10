---
title: 'ADR-0009: Go owns watch/reindex chassis'
status: Proposed
date: '2026-08-10'
---

# ADR-0009: Go chassis daemon

## Context

Watch → reindex → stamp freshness is a chassis concern. Cobra/fsnotify fit Go’s
CLI/daemon excellence domain.

## Decision

**Go** owns `lie0d` (name TBD): Cobra CLI, file watch, reindex triggers, stamp
publication for the engine. Optional wazero for Go-side WASM. Does not own
resolve/lock business logic (Rust).

## Status

Proposed.

## Consequences

Positive: clear chassis BC.  
Negative: another CI language.  
Rejected: embedding watch loops inside Rust engine as the only option.
