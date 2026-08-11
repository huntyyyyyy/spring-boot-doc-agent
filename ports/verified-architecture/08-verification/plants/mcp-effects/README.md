---
title: Model Context Protocol effect-checkpoint plants (Tier-1 deterministic)
status: DRAFT
date: '2026-08-10'
evidence:
  - arXiv:2607.20531 DynamicMCPBench
  - blog.modelcontextprotocol.io/posts/2026-07-28/
claim_tiers: Evidenced / Confirmed / Unknown
---

# Effect-checkpoint plants

**Embody** DynamicMCPBench scoring shape. **Refuse** scoring final NL answers;
**Refuse** Tier-2 LLM judge as merge SoR. Public engine = Unknown pending
publication — copy algorithm class only (`[Evidenced — arXiv:2607.20531]`).

## Checkpoint kinds

| Kind | Predicate | Fail-mode |
| --- | --- | --- |
| `tool_effect` | Tool in equivalence set called with constrained args | Wrong/missing call |
| `value_produced` | Demanded value in `structuredContent` | Absent value |
| `minefield` | Must **not** occur | Minefield present → fail |
| `partial_order` | Effect A before B when dependency real | Order inverted → fail |

Headline Accept = **Tier-1 only** (deterministic).

## Plant catalog

| Plant ID | Required effects | Minefields | Order |
| --- | --- | --- | --- |
| FX-MCP-01 | `locks_list`→`lock_set_id`; `verify`→`receipt_path`+file | invent `lock_*`; `llm_witness` | locks_list → verify |
| FX-MCP-02 | `snapshot_open` → `resolve` status∈enum | free-text bean; invented `snap_` | snapshot_open → resolve |
| FX-MCP-03 | receipt on disk; `result` enum; sha256 digests | model-only pass; `narrative_pass` | — |
| FX-MCP-04 | dispositions∈enums; `unprovable` allowed | delete last verified on unprovable | snapshot_open → claim_withdraw |
| FX-MCP-05 | `isError` + `reject_class=unknown_handle` | invented handle as success | — |
| FX-MCP-06 | `require_index` → `index_stale` or rebuild | nearest-upload soft pass | — |

## Locus (Implement later)

| Concern | Path |
| --- | --- |
| Plants / TaskSpecs | `08-verification/plants/mcp-effects/` |
| Tier-1 scorer | engine test crate or `packages/mcp-server/.../effect_score.ts` |
| Replay world | `scripts/fixtures/` (future) |
