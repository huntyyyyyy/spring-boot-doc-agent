---
title: E-QUERY0 — Query / context-packet BC + MCP isolation (Spec seed)
status: DRAFT Spec — pending Approve of Q0-1–Q0-10
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Stage-0 typed query + thin MCP
related:
  - docs/research/cold-product-bc-research-map-2026-08-10.md
  - docs/research/archive/claude-lore/research/query-seam-audit-e4-2026-08-07.md
  - docs/research/process/25-tip-grounding-mcp-2026.md
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
  - src/doc_engine/query/
  - adapters/mcp/
do_not:
  - Implement size chops or new MCP tools before Approve
  - add write/codegen MCP tools
  - treat packet completeness as Cover% or merge SoR
  - unattended AI adoption
spec_gate: DRAFT E-QUERY0 (2026-08-10)
human_review_floor: true
---

# Principal memo: query / packet BC (E-QUERY0)

**Question.** `query/` and thin MCP are the agent-facing Stage-0 surface but are
**cold** post-import while LOC offenders remain (`packet`, `providers`, `rank`).
What Spec locks the BC before E-QUERY1 size work or E-OAS/GND Implement?

## Verdict

| Stance | Choice |
| --- | --- |
| **Embody** | `dispatch_tool` library SoR; server-derived root; envelope + nested caps; stderr-only MCP stdio |
| **Adopt** | Structure-first retrieval doctrine (typed kinds over raw dumps) `[Evidenced]` code-KG/MCP patterns; dual human/JSON sinks when OAS lands |
| **Refuse** | Caller `root`; write/codegen tools; packet as quality floor; embedding citation SoT; SDK pin without Spike (GND9) |

## Decisions (Q0-1–Q0-10) — pending Approve

| ID | Decision |
| --- | --- |
| **Q0-1** | Packet vs full-signal kinds stay explicit; no silent full-corpus dumps |
| **Q0-2** | Token/rank budgets remain fail-closed (truncate with honesty labels) |
| **Q0-3** | Freshness labels stay on envelopes (`live`/`stale`/…) |
| **Q0-4** | MCP tools ⊆ library surface; adapter stays thin stdio |
| **Q0-5** | Isolation ADR S-STF-E remains binding |
| **Q0-6** | E-QUERY1 size splits follow ports/strategies — no utils bag |
| **Q0-7** | Tip-grounding tools stay on E-GND0 (not this epic) |
| **Q0-8** | Human review of agent citations remains floor |
| **Q0-9** | Official MCP SDK Explicit Defer until Spike |
| **Q0-10** | ≥10k★ bar for any new query runtime SoR |

## Exit

Approve Q0-1–Q0-10 in a design memo → unblocks E-QUERY1 (P12.2) under human review.
