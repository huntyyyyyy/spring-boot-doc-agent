---
title: MCP / CLI tools ICD — primitives + STEAD + 2026-07-28 transport
status: DRAFT — STALE vs MCP 2026-07-28 until amended
date: '2026-08-10'
evidence:
  - arXiv:2608.03609
  - arXiv:2607.08028
  - arXiv:2606.13663
  - https://blog.modelcontextprotocol.io/posts/2026-07-28/
---

# ICD-MCP — primitive tools (wave-1)

HyperTool-style composition blocks = **Could** later. MVP exposes **primitives**
with schemas; harness is code-owned (Contracts 2607.08028).

## Transport requirement (NEW — was missing)

**Normative remote dialect:** Model Context Protocol specification **`2026-07-28`**.

| Requirement | Detail |
| --- | --- |
| Stateless core | No `initialize` handshake; no `Mcp-Session-Id` (SEP-2575, SEP-2567) |
| Per-request `_meta` | Protocol version, client info, client capabilities on every call |
| Streamable HTTP headers | `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name` required; reject mismatch |
| Discovery | Optional `server/discover` (not handshake) |
| Application state | **Explicit handles as tool arguments** (`snapshot_id`, `lock_set_id`, …) — never hidden transport session |
| List caching | Honor `ttlMs` / `cacheScope` on list/read results when present |
| Deprecated | Roots, Sampling, Logging; legacy HTTP+SSE — do not design new features on them |

Local **stdio** remains valid for IDE-embedded servers; behavior must still be
**session-free at the protocol layer** (handles in args).

See `research/gaps/shallow-approvals-deep-dive-2026-08-10.md`.

## STEAD constraints (normative)

See `08-verification/stead/STEAD_CONSTRAINTS.md` ST-1…5.

- Entity parameters (`bean_id`, `symbol`, `edge_id`, `claim_id`, `file`) MUST
  match ids present in the current snapshot or the call is rejected.
- No free-text “bean name from the model” parameters.
- Handles (`snapshot_id`, …) MUST be minted by prior tool results, not invented.

## Tools

| Tool | Args (typed) | Effect checkpoint |
| --- | --- | --- |
| `verify` | `target_root: path`, `lock_set_id: id` | receipt written; exit code reflects result |
| `resolve` | `injection_site_id: id`, `snapshot_id: id` | resolve_result schema; Unknown allowed |
| `claim_withdraw` | `snapshot_id: id` | dispositions[] returned |
| `locks_list` | `snapshot_id: id` (optional scope) | returns lock ids from git SoR |

## Reject classes (harness)

unknown_id · stale_receipt · llm_witness_forbidden · schema_invalid ·
header_body_mismatch · unknown_handle · protocol_version_unsupported

## Still missing before Implement

Per-tool JSON Schema files; effect-checkpoint fixtures; auth story if remote;
migration note if any client still speaks pre-`2026-07-28`.
