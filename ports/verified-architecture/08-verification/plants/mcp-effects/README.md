---
title: MCP effect-checkpoint plants (Tier-1 deterministic)
status: DRAFT
date: '2026-08-10'
evidence:
  - arXiv:2607.20531 DynamicMCPBench
  - blog.modelcontextprotocol.io/posts/2026-07-28/
claim_tiers: Evidenced / Confirmed / Unknown
---

# Effect-checkpoint plants

**Embody** DynamicMCPBench scoring shape; **Refuse** scoring final natural-language
answers; **Pilot** our TaskSpec files until a public engine exists
(`[Evidenced — arXiv:2607.20531]` code “will be released upon publication”;
HF dataset is anonymized review dump — **not** Adopt as product dependency).

## Checkpoint kinds (paper)

| Kind | Meaning |
| --- | --- |
| `tool_effect` | Some tool in an equivalence set was called with args satisfying a constraint |
| `value_produced` | A demanded value appears in a tool result (`structuredContent`) |
| `minefield` | Must **not** occur |
| `partial_order` | Effect A before effect B when dependency is real |

Headline Accept uses **Tier-1 only** (deterministic). Tier-2 LLM judge = Refuse
for merge System of Record.

## Plant catalog

| Plant ID | Usage | Required effects | Minefields | Partial order |
| --- | --- | --- | --- | --- |
| FX-MCP-01 | UC-MCP-01 IDE locks→verify | `locks_list` value_produced `lock_set_id`; `verify` value_produced `receipt_path` + file exists | invent `lock_*`; `llm_witness` in receipt | locks_list → verify |
| FX-MCP-02 | UC-MCP-02 resolve | `snapshot_open` → `resolve` with status in enum | free-text bean name arg; invented `snap_` | snapshot_open → resolve |
| FX-MCP-03 | UC-MCP-03 verify harness | receipt file on disk; `result` enum; digests sha256 | model-only “pass” without tool; narrative_pass field | (none) |
| FX-MCP-04 | UC-MCP-04 withdraw | dispositions include allowed enums; `unprovable` allowed | deleting last verified artifact because unprovable | snapshot_open → claim_withdraw |
| FX-MCP-05 | UC-MCP-07 hostile handle | tool returns `isError` + `reject_class=unknown_handle` | accepting invented handle as success | (none) |
| FX-MCP-06 | Stale index | `snapshot_open` with require_index → `index_stale` or rebuild | nearest-upload soft pass | (none) |

## Machine-readable TaskSpec (draft)

See sibling `*.taskspec.json` files. Schema fields mirror the paper’s distillation
output, not a gold tool path.

## Planned code locus (Implement later)

| Concern | Path |
| --- | --- |
| Plants | `08-verification/plants/mcp-effects/` |
| Scorer (Tier-1) | `packages/mcp-server/src/harness/effect_score.ts` or engine test crate |
| Replay world | fixture target repo under `scripts/fixtures/` (future) |

## Anti-bogus note

DynamicMCPBench public **engine** = Unknown / pending publication. We copy the
**algorithm class** (path-agnostic effects + minefields), not a dependency pin.
