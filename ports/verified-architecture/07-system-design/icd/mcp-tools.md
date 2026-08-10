---
title: MCP / CLI tools ICD — primitives, STEAD, 2026-07-28, usage cases
status: DRAFT
date: '2026-08-10'
decision_matrix: 07-system-design/decisions/mcp-decision-matrix.md
adr: docs/adr/adr-0011-mcp-protocol-and-tool-surface.md
evidence:
  - arXiv:2608.03609
  - arXiv:2607.08028
  - https://blog.modelcontextprotocol.io/posts/2026-07-28/
---

# ICD-MCP — primitive tools (wave-1)

HyperTool-style composition = **Could** later. Minimum viable product exposes
**primitives** with schemas; harness is code-owned (Contracts arXiv:2607.08028).

**Decision record:** `decisions/mcp-decision-matrix.md` (what/when/how/who/where/why
+ usage cases + rejected alternatives). Do not edit tool semantics here without
updating that matrix.

## Transport (normative)

**Remote dialect:** Model Context Protocol **`2026-07-28`**.

| Requirement | Detail | Why over alternative |
| --- | --- | --- |
| Stateless core | No `initialize`; no `Mcp-Session-Id` | Session middleware breaks load-balanced hosts (SEP-2575/2567) |
| Per-request `_meta` | Version, clientInfo, capabilities | Replaces handshake |
| Streamable HTTP headers | `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name` required | Gateway routing; reject mismatch |
| Discovery | Optional `server/discover` | Not a session bootstrap |
| Application state | Handles as **tool arguments** | Explicit > hidden transport state |
| List caching | `ttlMs` / `cacheScope` when present | Tools are fixed → cacheable |
| Deprecated | Roots, Sampling, Logging; legacy HTTP+SSE | Do not design new features on them |

Local **stdio** remains the MVP transport for IDE-embedded servers; still
**session-free** at the protocol layer.

## STEAD constraints (normative)

See `08-verification/stead/STEAD_CONSTRAINTS.md` ST-1…5.

- Entity parameters MUST be ids from the current snapshot — not free-text names.
- Handles MUST be minted by prior tool results, not invented by the model.

## Tools

| Tool | Args (typed) | Effect checkpoint | Primary usage |
| --- | --- | --- | --- |
| `snapshot_open` | `target_root: path`, `require_index?: bool` | mints `snapshot_id`; binds tree/index digests | UC-MCP-02/04 prelude |
| `verify` | `target_root: path`, `lock_set_id: id`, `snapshot_id?: id` | receipt written; exit reflects result | UC-MCP-03 |
| `resolve` | `injection_site_id: id`, `snapshot_id: id` | resolve_result; Unknown allowed | UC-MCP-02 |
| `claim_withdraw` | `snapshot_id: id`, `claim_id?: id` | dispositions[] | UC-MCP-04 |
| `locks_list` | `snapshot_id?: id` or `target_root` | returns `lock_set_id` + lock ids from git System of Record | UC-MCP-01 |

### Schema files (JSON Schema 2020-12)

Directory: `icd/mcp/` — see `tools.catalog.json`. Shared handle/reject defs in
`common.schema.json`. Research: `research/gaps/mcp-open-items-research-2026-08-10.md`.

### Effect plants (Tier-1)

`08-verification/plants/mcp-effects/` — FX-MCP-01/03/05 TaskSpecs (DynamicMCPBench
shape; engine not Adopted).

### Planned code map (Implement later — Spec binding now)

| Layer | Planned path | Port / role |
| --- | --- | --- |
| MCP presentation | `packages/mcp-server/src/tools/*.ts` | ADR-0010 TypeScript |
| Transport stdio | `packages/mcp-server/src/transport/stdio.ts` | UC-MCP-05 |
| Transport HTTP | `packages/mcp-server/src/transport/streamable_http.ts` | UC-MCP-06 |
| Reject harness | `packages/mcp-server/src/harness/reject.ts` | ST-5; UC-MCP-07 |
| Engine | `crates/engine/` (Pilot) | `LockCheck`, `Resolver`, `ReceiptWriter`, `ClaimMemory` |
| Schemas | `07-system-design/icd/*.schema.json` → copied into package at build | Single dialect |

Until those packages exist, **this Interface Control Document + decision matrix
are the System of Record** for tool behavior. Agents must not invent a second
tool list in prompts.

## Usage cases (summary)

Full table: `decisions/mcp-decision-matrix.md`.

| ID | One-line |
| --- | --- |
| UC-MCP-01 | IDE: list locks then verify → receipt path |
| UC-MCP-02 | Agent: resolve one injection site with snapshot handle |
| UC-MCP-03 | Agent: verify; only harness writes receipt |
| UC-MCP-04 | After edit: claim withdraw → unprovable allowed |
| UC-MCP-05 | CI: same tools over stdio |
| UC-MCP-06 | Optional remote: Streamable HTTP headers |
| UC-MCP-07 | Invented handle → reject |
| UC-MCP-08 | Governance: audit matrix + ADR |

## Reject classes (harness)

unknown_id · unknown_handle · expired_handle · stale_receipt ·
llm_witness_forbidden · schema_invalid · header_body_mismatch ·
protocol_version_unsupported · equivariance_reject (when wrap ships)

## Chosen vs rejected (short)

| Chosen | Rejected | Why |
| --- | --- | --- |
| Primitives + handles | Mega “architecture” tools | Effect checkpoints stay visible |
| `2026-07-28` | Sessionful pre-July dialect | Normative Spec; concurrent hosts |
| Typed entity ids | Free-text bean names | ST-1 / ST-5 failure mode |
| Harness decides | Model stamps pass | Contracts / Aria-shaped loop |
| stdio MVP + optional HTTP | Org SaaS session store | Local-first product shape |

## Still missing before Implement

- [x] Per-tool JSON Schema 2020-12 files under `icd/mcp/` (Draft)  
- [x] Explicit snapshot-mint tool (`snapshot_open`)  
- [x] Effect-checkpoint fixtures (FX-MCP-* Draft plants)  
- [ ] Live replay world + Tier-1 scorer implementation  
- [ ] Auth story if remote HTTP ships  
- [ ] Migration note if any client still speaks pre-`2026-07-28`  
- [ ] Human Accept of schemas + plants
