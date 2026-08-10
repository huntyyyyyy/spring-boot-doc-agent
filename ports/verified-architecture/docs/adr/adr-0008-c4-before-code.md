---
title: 'Architecture Decision Record ADR-0008: C4 and Architecture Decision Records before product code'
status: Proposed
date: '2026-08-10'
---

# Architecture Decision Record ADR-0008: C4 + Architecture Decision Records before product code

## Context

This repository exists to finish requirements, constraints, C4, and Architecture Decision Records before
coding. Shipping crates early recreates product drift.

## Decision

No product code until CONTRIBUTING gate is green: Stakeholder Requirements Specification/Software Requirements Specification/Quality Attribute Scenario, constraints,
C4 Context+Container (+ Component for touched bounded context), and Accepted Architecture Decision Records for
structural choices.

## Status

Proposed.

## Consequences

Positive: planning System of Record stays honest.  
Negative: slower “visible code.”  
Rejected: spike folders that become undeclared tip.
