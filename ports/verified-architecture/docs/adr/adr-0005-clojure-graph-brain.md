---
title: 'ADR-0005: Clojure graph brain BC'
status: Proposed
date: '2026-08-10'
---

# ADR-0005: Clojure / Babashka Datascript graph brain

## Context

SQLite optimizes verify joins; architects want recursive Datalog asks. Product
requires Clojure as a **first-class** BC, not a script demo.

## Decision

Clojure BC owns graph query: Babashka+Datascript for fast REPL; full Clojure JVM
service if Spike keep for long-running. Consumes EDN export from registry.
Must not write the merge oracle.

## Status

Proposed.

## Consequences

Positive: distinctive architecture REPL.  
Negative: dual-view drift — require SQL goldens.  
Rejected: Datascript as merge SoR; demoting Clojure to “nice to have.”
