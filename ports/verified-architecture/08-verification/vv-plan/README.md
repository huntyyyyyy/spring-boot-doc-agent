---
title: Verification and Validation plan — wave-1 Accept methods
status: DRAFT
date: '2026-08-10'
evidence:
  - arXiv:2607.14890
  - arXiv:2607.20531
---

# Verification and Validation plan (wave-1)

## Fixtures (names — plants TBD)

| ID | Intent |
| --- | --- |
| FX-CYCLE | A→B→A injection cycle |
| FX-LAYER | controller→repo lock violation |
| FX-MULTI | two impls, no qualifier → Unknown |
| FX-DRIFT | claim then edit anchor → affected/unprovable |
| FX-Stateful Tool-Enabled Agentic Deployment | Model Context Protocol call with unknown bean_id → reject |
| FX-PRIV | deny-net full verify |
| FX-DET | two verifies → canonical JSON match |

## Accept methods

| REQ / Quality Attribute Scenario | Method |
| --- | --- |
| F-01…05 | FX-CYCLE, FX-LAYER, FX-MULTI |
| F-06/06b | Receipt JSON Schema validate; material_digest bind (Proof-or-Stop) |
| F-06c / N-07 | FX-DRIFT |
| F-09b / N-08 | FX-Stateful Tool-Enabled Agentic Deployment |
| N-05 | FX-PRIV |
| N-06 | FX-DET |
| N-01/N-02 latency | Spike PIL-LAT-* only — not Design gate yet |

## Rule

Agent “looks green” without matching receipt digests = **fail** (Proof-or-Stop).
