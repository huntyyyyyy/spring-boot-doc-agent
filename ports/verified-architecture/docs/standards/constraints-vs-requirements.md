---
title: Constraints vs requirements
status: ACTIVE
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Constraints vs requirements

| Kind | Stakeholder value | Change process | Fail-mode |
| --- | --- | --- | --- |
| **Requirement** | Capability/quality under MoSCoW | Amend Software Requirements Specification / Quality Attribute Scenario + Requirements Traceability Matrix | Silent scope creep in prose |
| **Constraint** | Fixed for this wave; not casually traded | Architecture Decision Record + risk note | Trading a constraint in a chat without an Architecture Decision Record |

Examples of constraints (ledger binds them): single deterministic gate writer;
local-first default; polyglot bounded-context ownership; no large language
model as verify witness.

Ledger: [`../constraints/constraints.md`](../constraints/constraints.md).
