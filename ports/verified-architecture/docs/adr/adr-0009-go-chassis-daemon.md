---
title: 'Architecture Decision Record ADR-0009: Go owns watch/reindex chassis'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/04-chassis-go
---

# Architecture Decision Record ADR-0009: Go chassis daemon

## Context

File watch, reindex triggers, and stamp invalidation need a long-running
process beside the Rust engine — not inside the IDE and not in Python.

## Decision

**Go** runs the watch/reindex chassis: watches the target tree, triggers engine
index/verify, may later mint Spec `corpus_version` / snapshot freshness
sidecars. Writing verify oracle artifacts from the chassis fails Architecture
Decision Record ADR-0006 / ADR-0007. Folding chassis into the TypeScript
extension or a Python watchdog fails this Architecture Decision Record.

## Status

Proposed.

## Consequences

Positive: mature daemon/watch ecosystem.  
Negative: another language in the monorepo to staff and CI.  
Rejected: Python watchdog as product chassis; chassis inside TypeScript
extension.
