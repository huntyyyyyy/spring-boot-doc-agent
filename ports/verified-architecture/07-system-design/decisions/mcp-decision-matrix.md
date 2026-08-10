---
title: Model Context Protocol surface — Decision Matrix
status: DRAFT
date: '2026-08-10'
standard: docs/standards/decision-framework.md
adr: docs/adr/adr-0011-mcp-protocol-and-tool-surface.md
icd: 07-system-design/icd/mcp-tools.md
claim_tiers: Evidenced / Confirmed / Unknown
---

# Model Context Protocol surface — Decision Matrix

**Framings:** Analytical Decision Matrix · Architecture Decision Record companion
(ADR-0011) · Governance (who may mutate verify state).

**Normative primary:** Model Context Protocol specification **`2026-07-28`**
`[Evidenced — blog.modelcontextprotocol.io/posts/2026-07-28/]`.

---

## Six vectors (chosen shape)

| Vector | Chosen content |
| --- | --- |
| **Why** | Agents hallucinate entity ids and treat chat as verify System of Record; we need a **typed, handle-passing, harness-owned** tool surface that cannot green-wash without receipts. |
| **What** | Primitive tools only (`verify`, `resolve`, `claim_withdraw`, `locks_list`); Stateful Tool-Enabled Agentic Deployment ST-1…5; protocol pin `2026-07-28`; reject classes listed in Interface Control Document; no Roots/Sampling/Logging. |
| **Who** | **Decides:** harness (`LockCheck`, `ReceiptWriter`, `ClaimMemory`). **Proposes:** model / host. **Owns presentation:** TypeScript (ADR-0010). **Owns engine:** Rust Pilot (ADR-0007). **Accepts policy:** human (locks in git). |
| **How** | Local **stdio** MVP; optional Streamable HTTP with required headers; state only as **tool-arg handles** minted by prior results; JSON Schema 2020-12 args/results. |
| **When** | Spec wave now; Implement only after Definition of Ready D7/D10c + per-tool schemas; **review** when MCP Spec revises or first remote host ships. |
| **Where** | Spec: `07-system-design/icd/mcp-tools.md`. Planned code: `packages/mcp-server/` (TypeScript presentation) → stdio/HTTP → `crates/engine/` ports. Never inside agent prompt memory. |

---

## Alternatives scored (0–2 per vector; sensor only)

| Option | Why | What | Who | How | When | Where | Total | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **A. Primitive tools + `2026-07-28` + handles** | 2 | 2 | 2 | 2 | 2 | 2 | **12** | **Chosen** |
| B. Pre-July sessionful MCP (`initialize` + `Mcp-Session-Id`) | 1 | 0 | 1 | 0 | 0 | 1 | 3 | **Refuse** for new work |
| C. HyperTool / mega-tools (“do architecture”) | 1 | 0 | 0 | 1 | 1 | 1 | 4 | **Defer** (Could) |
| D. Free-text bean_name tools | 0 | 0 | 0 | 1 | 1 | 1 | 3 | **Refuse** (ST-1/ST-5) |
| E. CLI-only; no Model Context Protocol | 2 | 1 | 1 | 2 | 2 | 1 | 9 | **Accept as peer**; MCP still needed for IDE hosts |
| F. Remote SaaS MCP with org session store | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **Refuse** MVP (product shape) |

**Why A over E:** command-line interface covers humans and scripts; IDE / agent
hosts expect Model Context Protocol. Same harness, two transports — not two
oracles.

**Why A over B:** Spec `2026-07-28` retires protocol sessions; load-balanced
hosts already behave per-call. Hidden session state dies under concurrent
agents `[Evidenced — SEP-2567 / blog]`.

**Why not C:** Contracts paper (arXiv:2607.08028) — harness owns composition;
primitives first. Mega-tools hide effect checkpoints.

---

## Usage cases (suggested; Spec → planned code)

| ID | Actor | Goal | Steps (logical) | Spec locus | Planned code locus | Why this shape |
| --- | --- | --- | --- | --- | --- | --- |
| **UC-MCP-01** | Developer in IDE | Check locks before commit | Host calls `locks_list` → optional `verify` → shows receipt path | `icd/mcp-tools.md` tools table; ICD-RCPT | `packages/mcp-server/src/tools/locks_list.ts` → engine `LockCheck`; `ReceiptWriter` | List before mutate; handle from snapshot, not invented |
| **UC-MCP-02** | Coding agent | Resolve one injection site | Agent receives `snapshot_id` from prior tool → `resolve(injection_site_id, snapshot_id)` | ST-1/ST-5; resolve-result schema (to add) | `packages/mcp-server/src/tools/resolve.ts` → port `Resolver` | Typed ids only; Unknown/unprovable allowed |
| **UC-MCP-03** | Coding agent | Run full verify | `verify(target_root, lock_set_id)` → harness writes receipt; agent **must not** invent pass | ICD-RCPT; Proof-or-Stop field gaps G-R1 | `packages/mcp-server/src/tools/verify.ts` → `LockCheck` + `ReceiptWriter` | Propose/decide split: model never stamps receipt |
| **UC-MCP-04** | Agent after edit | Withdraw stale claims | `claim_withdraw(snapshot_id)` → dispositions including `unprovable` | ICD-CLAIM; QAS-N-07 | `packages/mcp-server/src/tools/claim_withdraw.ts` → `ClaimMemory` | Leaf anchors; no chat-memory substitute |
| **UC-MCP-05** | CI / headless | Same tools over stdio | Same tool names; no HTTP headers; still session-free | Transport section of ICD | `packages/mcp-server/src/transport/stdio.ts` | One schema; two transports |
| **UC-MCP-06** | Remote host (optional later) | Call over Streamable HTTP | Send `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name`; handles in body | ICD transport; SEP-2243 | `packages/mcp-server/src/transport/streamable_http.ts` | Headers required; reject mismatch |
| **UC-MCP-07** | Hostile / buggy agent | Invent `snapshot_id` / bean id | Harness reject `unknown_handle` / `unknown_id` | Reject classes; ST-5 | `packages/mcp-server/src/harness/reject.ts` + engine | Possession ≠ auth; mint-only handles |
| **UC-MCP-08** | Product owner | Audit why MCP chosen | Read this matrix + ADR-0011 | `decisions/` + `docs/adr/` | N/A (governance) | Traceability; prevents drift back to sessions |

### Sequence (UC-MCP-03) — decide plane

```text
[Host / model] --tools/call verify(lock_set_id)--> [mcp-server TS]
        |                                              |
        |                                              v
        |                                     [engine LockCheck]
        |                                              |
        |                                              v
        |                                     [ReceiptWriter] --> receipt.json
        |                                              |
        <------------- structuredContent(run_id, receipt_path, result) ---
```

Model may **narrate**; only harness **writes** the receipt. Narrative is never
a witness (`llm_witness_forbidden`).

---

## Handle inventory (state as args)

| Handle | Minted by | Required by | Expiry / reject |
| --- | --- | --- | --- |
| `snapshot_id` | **`snapshot_open`** | `resolve`, `claim_withdraw`, scoped `locks_list`; optional on `verify` | `expired_handle`, `unknown_handle` |
| `lock_set_id` | `locks_list` or git-derived list | `verify` | `unknown_id` |
| `run_id` / `receipt_path` | `verify` | follow-up audit (Could) | `stale_receipt` if material digest drifts |
| `injection_site_id` | resolve catalog / graph query (future) | `resolve` | `unknown_id` |
| `claim_id` | claim store list (future) | withdraw variants | `unknown_id` |

**Refused:** storing these in server memory keyed by connection / session.

---

## Governance (business framing)

| Control | Rule |
| --- | --- |
| Accountability | Engine maintainers own reject classes; IDE maintainers own presentation; humans own lock policy in git |
| Alignment | Local-first product — remote HTTP is optional, not org SaaS |
| Urgency | Interface Control Document must be `2026-07-28`-honest before Implement |
| Review | Re-open matrix on next Model Context Protocol Spec release or first production remote host |

---

## Still open (not silent Accept)

| Gap | Blocks |
| --- | --- |
| Live Tier-1 scorer + replay world | G-M2 Implement |
| Auth for remote HTTP | Only if remote ships |
| `injection_site` catalog mint tool | Spike |

---

## Bloom (this matrix)

| Level | Evidence |
| --- | --- |
| 1 Remember | Spec `2026-07-28`; SEPs 2575/2567/2243; ADR-0010/0011 |
| 2 Understand | Six vectors + usage cases above |
| 3 Apply | Planned `packages/mcp-server` + engine ports |
| 4 Analyze | Alternatives A–F scored |
| 5 Evaluate | Reject classes; ST-1…5; false-green bites |
| 6 Create | This matrix + ADR-0011 + ICD rewrite — **Implement still Refuse** |
