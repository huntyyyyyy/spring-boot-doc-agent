---
title: Verification and Validation plan — wave-1 Accept methods
status: DRAFT
date: '2026-08-10'
evidence:
  - arXiv:2607.14890
  - arXiv:2607.20531
---

# V&V plan (wave-1)

## Fixtures (plants TBD)

| ID | Intent (observable) | Fail-mode |
| --- | --- | --- |
| FX-CYCLE | A→B→A injection cycle detected | Cycle soft-pass |
| FX-LAYER | controller→repo lock violation fails | Violation green |
| FX-MULTI | two impls, no qualifier → Unknown | Guessed bean |
| FX-DRIFT | claim then edit anchor → affected/unprovable | Stale green |
| FX-STEAD | MCP call with unknown bean_id → reject | Invented handle OK |
| FX-PRIV | deny-net full verify | Egress during verify |
| FX-DET | two verifies → canonical JSON match | Non-deterministic receipt |

## Accept methods

| REQ / QAS | Method |
| --- | --- |
| F-01…05 | FX-CYCLE, FX-LAYER, FX-MULTI |
| F-06/06b | Receipt JSON Schema; material_digest bind (Proof-or-Stop) |
| F-06c / N-07 | FX-DRIFT |
| F-09b / N-08 | FX-STEAD |
| N-05 | FX-PRIV |
| N-06 | FX-DET |
| N-01/N-02 latency | Spike PIL-LAT-* only — not Design gate yet |

## Rule

Agent “looks green” without matching receipt digests = **fail** (Proof-or-Stop).
