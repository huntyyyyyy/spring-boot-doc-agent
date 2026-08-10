---
title: Quality Attribute Scenarios (Architecture Tradeoff Analysis Method)
status: DRAFT — MEASURE-TBD until Spikes
date: '2026-08-10'
---

# Quality Attribute Scenarios

Gate: incomplete Quality Attribute Scenario must not drive Design. Numeric *T*/*U* filled by Spike.

## Quality Attribute Scenario QAS-N-01 — Warm resolve latency

| Field | Value |
| --- | --- |
| Quality | Performance |
| Stimulus source | A-OP / command-line interface resolve |
| Stimulus | Binding request for one injection site / type |
| Environment | Warm registry+index; plant-scale tree; swap=0; reference SKU declared |
| Artifact | WiringResolver + SQLite registry (containers per C4) |
| Response | Impl symbol or `Unknown` + reason_code |
| Response measure | Wall p95 ≤ *T* ms over N≥30 calls; zero silent multi-candidate picks. *T* = MEASURE-TBD |

## Quality Attribute Scenario QAS-N-02 — Lock check

| Field | Value |
| --- | --- |
| Quality | Performance / Integrity |
| Stimulus source | A-DEV save or fitness_check |
| Stimulus | Changed file outbound edges |
| Environment | Warm locks+graph; peak 10 concurrent local checks |
| Artifact | LockCheck (native path first per Architecture Decision Record) |
| Response | Violation set or clean + receipt |
| Response measure | p95 ≤ *U* ms; 100% receipts schema-valid. *U* = MEASURE-TBD |

## Quality Attribute Scenario QAS-N-05 — Local-first privacy

| Field | Value |
| --- | --- |
| Quality | Security / Privacy |
| Stimulus source | Default config |
| Stimulus | Full Must verify path |
| Environment | Egress denied / offline |
| Artifact | Engine + registry + LockCheck |
| Response | Completes with no outbound sockets |
| Response measure | Deny-net harness: 0 egress; exit 0 |

## Quality Attribute Scenario QAS-N-06 — Determinism

| Field | Value |
| --- | --- |
| Quality | Reliability |
| Stimulus source | A-CI |
| Stimulus | Re-run verify twice on same digests |
| Environment | Clean worktree; same binary digests |
| Artifact | Must spine |
| Response | Identical resolve + witness sets (timestamp stripped) |
| Response measure | Canonical JSON byte-identical across 2×5 fixtures |

## Incomplete (must rewrite before Design influence)

| Legacy | Topic | Status |
| --- | --- | --- |
| N-03 | Unknown-rate observability | incomplete-qas |
| N-04 | Index rebuild cost | incomplete-qas |
| N-07 | Language Server Protocol interactive latency | incomplete-qas |
| N-08 | Reference SKU declaration | incomplete-qas |
