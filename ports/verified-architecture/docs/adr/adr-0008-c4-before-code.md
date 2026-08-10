---
title: 'ADR-0008: C4 and ADRs before product code'
status: Proposed
date: '2026-08-10'
---

# ADR-0008: C4 + ADRs before product code

## Context

This repository exists to finish requirements, constraints, C4, and ADRs before
coding. Shipping crates early recreates product drift.

## Decision

No product code until CONTRIBUTING gate is green: StRS/SRS/QAS, constraints,
C4 Context+Container (+ Component for touched BC), and Accepted ADRs for
structural choices.

## Status

Proposed.

## Consequences

Positive: planning SoR stays honest.  
Negative: slower “visible code.”  
Rejected: spike folders that become undeclared tip.
