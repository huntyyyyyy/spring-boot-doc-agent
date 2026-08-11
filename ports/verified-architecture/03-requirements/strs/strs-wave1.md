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

Stakeholder-visible outcomes the Verified Architecture Engine must deliver
**without** binding runtime language. Software Requirements Specification and C4
derive downward; this file does not restate folder names.

## Actors

| ID | Actor | Concern (attribute) |
| --- | --- | --- |
| A-OP | Agent / tool operator | Wiring answers anchored to index+locks — never hallucinated bindings |
| A-ARCH | Architect | Author locks once; humans + AI share the same enforcement path |
| A-DEV | Developer (IDE) | Same violation IDs as the agent / command-line interface path |
| A-CI | CI / merge steward | Deterministic gate; single oracle writer; **receipt-gated done** (Proof-or-Stop) |
| A-OWN | Target-repo owner | Local-first; Unknown/unprovable preferred over wrong |

## Mission need

Answers about architecture/wiring are **traceable to index digests + lock IDs +
claim digests**. Agents may propose; the harness decides accept/reject.

## Goals

| ID | Goal | Bound |
| --- | --- | --- |
| G1 | Virtual dependency / Dependency Injection graph + lock checks | Realistic plants named in Verification and Validation |
| G2 | Same lock policy for agent and human paths | Shared violation IDs |
| G3 | Explainable verify | Receipt + Artifact-Anchored Verification Memory dispositions |
| G4 | Tool surface refuses hallucinated entity ids | Stateful Tool-Enabled Agentic Deployment ST-1…5 |

## Out of scope (wave-1)

- Full JVM fidelity marketed as “proved”
- Embeddings / Retrieval-Augmented Generation as binding authority
- Org-wide social knowledge-graph SaaS
- First-Order Computation Tree Logic model checking of the agent deployment
- **Python** engine or Specification corpus host (Architecture Decision Record ADR-0001)

Fail-mode: human Accept missing in `SIGNOFF_LOG.md` → Definition of Ready D2 stays PARTIAL.
