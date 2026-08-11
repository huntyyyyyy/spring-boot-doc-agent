---
title: 'Architecture Decision Record ADR-0011: Model Context Protocol 2026-07-28 + dual surfaces'
status: Proposed — amended 2026-08-11 (verify vs Spec corpus; Rust Spec host)
date: '2026-08-10'
last_reviewed: '2026-08-11'
decision_matrix: 07-system-design/decisions/mcp-decision-matrix.md
related:
  - docs/adr/adr-0010-typescript-ide-mcp.md
  - docs/adr/adr-0007-rust-owns-engine.md
  - 07-system-design/icd/mcp-tools.md
  - 12-delivery/spike-charters/SPIKE-SPEC-MCP-0.md
---

# Architecture Decision Record ADR-0011: Model Context Protocol pin and dual surfaces

## Context

Hosts speak Model Context Protocol. Spec revision **`2026-07-28`** is
**stateless** at the protocol layer (handles carry application state). Earlier
drafts collapsed two jobs: **product verify** tools vs **Spec corpus** read
tools. Stateful Tool-Enabled Agentic Deployment forbids free-text entity args.

Companion matrix: `07-system-design/decisions/mcp-decision-matrix.md` (Draft /
FREEZE — deepen handle lifecycle only; new matrices without override = reject).

## Decision

### Shared wire

1. **Pin** Model Context Protocol **`2026-07-28`** (session-free protocol
   layer).  
2. **Handles** minted by tools; never transport session state.  
3. **Harness decides** mutations; model proposes.  
4. **Refuse** Python Model Context Protocol servers for this port — reject.

### Surface A — product verify (Draft Interface Control Document; not Implement)

Primitives (wave-1 hypothesis): `verify`, `resolve`, `claim_withdraw`,
`locks_list` (+ `snapshot_open` per open-items research). Schemas under
`07-system-design/icd/mcp/`. Effects owned by **Rust engine** (Architecture
Decision Record ADR-0007). TypeScript presents (Architecture Decision Record
ADR-0010). Blocked by FREEZE deepen-3 + Definition of Ready — do not Implement
from this Draft alone.

### Surface B — Spec corpus (Spike; read-only)

Tools: `spec_status`, `spec_assumption`, `spec_icd`, `spec_decision`,
`spec_gap`, optional `spec_lookup`. **Rust host** only
(`SPIKE-SPEC-MCP-0`). Frontmatter schema filters; `accepted:false` under
FREEZE. Not a verify oracle; not a shared System of Record with Surface A.
Collapsing Spec corpus into verify tools = reject.

## Status

Proposed (amended). Human Accept pending.

## Consequences

Positive: industry Spec pin; dual surfaces cannot false-train on unfinished
oracles.  
Negative: two servers/packages eventually; per-tool schemas still Draft.  
Rejected: pre-July sessions; HyperTool mega-tools; free-text entity args;
model writes receipts; org SaaS session database; Python host; one mega-tool
surface for verify + Spec.

## Review

Re-open when: next Model Context Protocol Spec release; Spike scheduled; or
Definition of Ready D7 moves toward PASS.
