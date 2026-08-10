---
title: RTM — Requirements Traceability Matrix
status: DRAFT
date: '2026-08-10'
---

# RTM

| Need | REQ | Design / ADR | Accept method |
| --- | --- | --- | --- |
| No hallucinated beans | F-01, F-02, F-07 | Resolver + Unknown; ADR-0002 | Multi-impl → Unknown |
| Graph cycles/layers | F-03, F-04 | Registry + graph; C4 Component | Cycle fixture fails gate |
| Shared policy | F-05, F-08, F-12 | Lock IR ADR-0003; LSP later | Same violation ID CLI/IDE |
| Explainable deny | F-06, F-13 | Receipt schema | Missing witness → fail |
| Stale honesty | F-07, F-10 | Index freshness | Digest mismatch → stale |
| Single oracle | F-09, F-19 | ADR-0006 | One writer in CI |
| Package locks | F-11 | ADR-0003 | controller→repo red |
| Latency | QAS-N-01/02 | Tradeoffs ADR | Spike fills *T*/*U* |
| Privacy | QAS-N-05 | Local-first CON | Deny-net harness |
| Sandbox Could | F-16 | ADR-0004 | Native↔WASM parity |
| Suggest ≠ verify | F-20 | Remediation adapter | Witnesses exclude model text |
