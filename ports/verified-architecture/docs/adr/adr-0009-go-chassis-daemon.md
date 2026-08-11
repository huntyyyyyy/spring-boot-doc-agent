---
title: 'Architecture Decision Record ADR-0009: Go owns watch/reindex chassis'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/04-chassis-go
---

# Architecture Decision Record ADR-0009: Go chassis daemon

## Context

File watch, reindex triggers, and stamp invalidation fit a long-running chassis
beside the Rust engine — not inside the IDE and not in Python.

## Decision

**Go** owns the watch/reindex chassis daemon. Triggers engine work; may later
mint Spec `corpus_version` / snapshot freshness sidecars. Not the verify oracle
writer (Architecture Decision Record ADR-0006 / ADR-0007).

## Status

Proposed.

## Consequences

Positive: solid daemon ecosystem.  
Negative: extra language in the monorepo.  
Rejected: Python watchdog as product chassis; folding chassis into TS extension.
