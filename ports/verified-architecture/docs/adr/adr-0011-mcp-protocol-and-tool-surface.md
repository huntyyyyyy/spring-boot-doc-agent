---
title: 'ADR-0011: Model Context Protocol 2026-07-28 + primitive tool surface'
status: Proposed
date: '2026-08-10'
decision_matrix: 07-system-design/decisions/mcp-decision-matrix.md
related:
  - docs/adr/adr-0010-typescript-ide-mcp.md
  - 07-system-design/icd/mcp-tools.md
---

# ADR-0011: Model Context Protocol protocol pin and primitive tools

## Context

IDE and agent hosts speak Model Context Protocol. Spec revision **`2026-07-28`**
makes the core **stateless** (no protocol session id; Streamable HTTP header
routing; application state as explicit handles). Our earlier tool list assumed
a pre-July mental model. Separately, Stateful Tool-Enabled Agentic Deployment
constraints forbid free-text entity parameters. Without a recorded choice,
agents reintroduce sessions, mega-tools, or model-stamped “verify passed.”

Companion analytical record: `07-system-design/decisions/mcp-decision-matrix.md`
(six vectors, scored alternatives, usage cases UC-MCP-01…08).

## Decision

1. **Pin** Model Context Protocol **`2026-07-28`** for any remote/HTTP surface;
   local stdio MVP must remain session-free at the protocol layer.  
2. Expose **primitive** tools only in wave-1: `verify`, `resolve`,
   `claim_withdraw`, `locks_list` — schemas in ICD-MCP.  
3. **Handles** (`snapshot_id`, `lock_set_id`, …) are minted by tools and passed
   as arguments — never stored as transport session state.  
4. **Harness decides** mutations (locks/receipts/claims); the model proposes.  
5. TypeScript owns presentation (ADR-0010); engine ports own effects
   (ADR-0007).

## Status

Proposed (human Accept pending).

## Consequences

Positive:

- Aligns with industry Spec; load-balanced hosts work.  
- Traceable usage cases and rejected alternatives (matrix).  
- Same reject classes for CLI and Model Context Protocol.

Negative:

- Per-tool JSON Schema and snapshot-mint tool still outstanding before Implement.  
- Equivariance wrap remains Spike (ST-2).

## Rejected

| Alternative | Why rejected |
| --- | --- |
| Pre-July `initialize` + `Mcp-Session-Id` | Retired by Spec; concurrent agent death |
| HyperTool mega-tools as MVP | Hides effect checkpoints; Contracts paper |
| Free-text entity name args | ST-1 / ST-5; paper 2608.03609 failure mode |
| Model writes receipts / todos | Violates propose/decide; Proof-or-Stop adversary |
| Org SaaS MCP with server-side session DB | Fights local-first product shape |

## Review

Re-open when: next Model Context Protocol Spec release; first production remote
host; or Definition of Ready D7 moves toward PASS.
