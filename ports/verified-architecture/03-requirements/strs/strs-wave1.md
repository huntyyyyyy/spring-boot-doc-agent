---
title: Stakeholder Requirements Specification — Stakeholder requirements (wave-1)
status: DRAFT — awaiting human Accept
date: '2026-08-10'
standard: ISO/IEC/IEEE 29148-shaped
evidence:
  - research/papers-2026-may-aug/june-august-2026-port-readiness.md
---

# Stakeholder Requirements Specification — wave-1

## Purpose

What the Verified Architecture Engine must achieve for stakeholders **without**
binding implementation language. Software Requirements Specification/C4 derive from this.

## Actors

| ID | Actor | Concern |
| --- | --- | --- |
| A-OP | Agent / tool operator | Wiring/architecture answers without hallucinated bindings |
| A-ARCH | Architect | Author locks once; humans + AI share enforcement |
| A-DEV | Developer (IDE) | Same violation signal as agent path |
| A-CI | CI / merge steward | Deterministic gate; single oracle writer; **receipt-gated done** (Proof-or-Stop) |
| A-OWN | Target-repo owner | Local-first; Unknown/unprovable > wrong |

## Mission need

Traceable answers about architecture/wiring **anchored to index + locks +
claim digests**, not chat invention. Agents may propose; harness decides.

## Goals

| ID | Goal |
| --- | --- |
| G1 | Virtual dep/Dependency Injection graph + lock checks on realistic plants |
| G2 | Same lock policy for agent and human paths |
| G3 | Explainable verify (receipt + EA-Graph dispositions) |
| G4 | Tool surface refuses hallucinated entity ids (Stateful Tool-Enabled Agentic Deployment) |

## Out of scope (wave-1)

- Full JVM fidelity as “proved”
- Embeddings/Retrieval-Augmented Generation as binding authority
- Org-wide social knowledge-graph SaaS
- FO-CTL model checking of the agent deployment
