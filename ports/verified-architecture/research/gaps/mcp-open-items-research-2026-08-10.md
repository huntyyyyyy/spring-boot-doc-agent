---
title: Model Context Protocol open items — schemas, snapshot mint, effect fixtures
status: RESEARCH
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
decision_matrix: 07-system-design/decisions/mcp-decision-matrix.md
icd: 07-system-design/icd/mcp-tools.md
adr: docs/adr/adr-0011-mcp-protocol-and-tool-surface.md
digest: research/papers-2026-may-aug/digests/2607.20531-dynamicmcpbench.md
mcp_primary: https://blog.modelcontextprotocol.io/posts/2026-07-28/
protocol: '2026-07-28'
bloom_through: 5
implement: Refuse until Spec Approve + Bloom Create tickets
---

# Model Context Protocol open items research (2026-08-10)

Research-only pass over the three gaps named in the Decision Matrix / Interface
Control Document / Architecture Decision Record 0011: **per-tool JSON Schema**,
**snapshot-mint handle lifecycle**, and **effect-checkpoint fixtures**. Whole
words per `GLOSSARY.md`. Claim tiers on every load-bearing assertion.

**Verdict (one line):** Pin JSON Schema 2020-12 + `structuredContent` object
results; mint `snapshot_id` via a fifth primitive `snapshot_open`; score
Verification and Validation with Tier-1 effect checkpoints and minefields —
DynamicMCPBench algorithm **Embody**, public engine **Refuse / pending**.

**DeepWiki:** Model Context Protocol Ask unavailable in this environment
(no DeepWiki tool server). Compensated with `llms.txt`, Spec pages, Model Context Protocol SEP
raw sources, and official software development kit docs `[Evidenced]`.

---

## Entities (frame)

| Entity | Kind | Product binding |
| --- | --- | --- |
| Tool `inputSchema` / `outputSchema` / `structuredContent` | Protocol fields | Wave-1 primitives + reject envelope |
| Explicit state handle (`snapshot_id`, …) | Tool-design pattern (Model Context Protocol SEP-2567) | ST-1 / ST-5; never transport session |
| Effect checkpoint / equivalence set / minefield / partial order | Benchmark scoring objects (arXiv:2607.20531) | FX-\* plants; Tier-1 Accept |
| Reject class | Harness predicate | Interface Control Document reject list |

---

## Bloom ladder (this memo)

| Level | Evidence |
| --- | --- |
| **1 Remember** | Spec `2026-07-28`; Model Context Protocol SEP-1613, Model Context Protocol SEP-2106, Model Context Protocol SEP-2567, Model Context Protocol SEP-2575, Model Context Protocol SEP-2243; blog mint-handle paragraph; arXiv:2607.20531; TypeScript / Python software development kit tool docs; `llms.txt` |
| **2 Understand** | Digests + restatements below; schemas in product types (`snap_`, `lock_`, receipt path) |
| **3 Apply** | Planned `packages/mcp-server` + `07-system-design/icd/mcp/*.schema.json`; fixture IDs mapped to Accept methods |
| **4 Analyze** | Alternatives scored (mint locus; schema dialect; DynamicMCPBench Adopt vs Pilot) |
| **5 Evaluate** | Adversarial checklist; false-green / false-red; research-depth status |
| **6 Create** | **Deferred** — Spec / epic tickets after human Accept of schemas + mint tool name |

---

## 1) Per-tool JSON Schema (JSON Schema 2020-12)

### Normative protocol `[Evidenced]`

| Source | Claim |
| --- | --- |
| Model Context Protocol SEP-1613 (Final) | Default dialect for embedded schemas is **JSON Schema 2020-12** when `$schema` absent; `inputSchema` **MUST NOT** be `null`; empty-args tools use `{ "type":"object", "additionalProperties": false }` (recommended) |
| Model Context Protocol SEP-2106 (Final) | `inputSchema` keeps root `type: "object"` but allows full 2020-12 keywords (`oneOf`, `$ref`, …); `outputSchema` any valid 2020-12; `structuredContent` any JSON value conforming to `outputSchema` |
| Spec Tools page `2026-07-28` | Same; servers **MUST** conform structured results to `outputSchema`; clients **SHOULD** validate; also emit TextContent JSON for back-compat |
| Model Context Protocol SEP-2106 security | **MUST NOT** auto-dereference network `$ref` (SSRF); bound schema depth / validation time |

### Official software development kit conventions `[Evidenced]`

| software development kit | Convention | Product implication |
| --- | --- | --- |
| **TypeScript** (`registerTool`) | Zod / Standard Schema → advertised JSON Schema; validates args before handler; validates `structuredContent` against `outputSchema`; schema failures → tool result `isError: true` (handler never runs for bad input) | Presentation layer (Architecture Decision Record 0010) should mirror: Zod at edge, copy Interface Control Document JSON Schema into package |
| **Python** (structured output docs) | Return annotation **is** `output_schema`; Pydantic models stay unwrapped objects; **scalars/lists wrapped** in `{ "result": ... }` today | Prefer **object-rooted** `outputSchema` for all wave-1 tools so TypeScript and Python hosts agree; avoid relying on bare-array `structuredContent` until both Tier-1 software development kits match Model Context Protocol SEP-2106 without wrappers |

**Confirmed:** Industry direction is schema-validated structured tool results.
**Unknown:** Exact wire behavior of every host against non-object `structuredContent` on day-zero of `2026-07-28` — mitigate by object roots + TextContent fallback.

### Reject / error shape (proposed product)

Harness rejects are **not** free-form model prose. Two channels:

1. **Protocol:** `isError: true` + TextContent explaining the reject (software development kit-aligned).  
2. **Structured:** optional `structuredContent` matching `toolError` (`reject_class`, `message`, optional `hint`) — **no** `llm_text` / `rag_chunk` / `narrative_pass` keys (`not` constraint).

Reject classes (Interface Control Document + common schema): `unknown_id`, `unknown_handle`,
`expired_handle`, `stale_receipt`, `llm_witness_forbidden`, `schema_invalid`,
`header_body_mismatch`, `protocol_version_unsupported`, `equivariance_reject`,
`index_missing`, `index_stale`, `search_fallback_forbidden`.

### Handle / id prefix rules (proposed)

| Prefix | Kind | Minted by | Pattern |
| --- | --- | --- | --- |
| `snap_` | Snapshot handle | `snapshot_open` | `^(snap\|lock\|run\|site\|claim)_[A-Za-z0-9._-]{6,120}$` with kind prefix |
| `lock_` | Lock-set handle | `locks_list` | same |
| `run_` | Verify run | `verify` | same |
| `site_` | Injection site | catalog / graph query (future list tool) | same |
| `claim_` | Claim id | claim store | `^claim_[A-Za-z0-9._-]{6,120}$` |
| `bean_` | Bean id (resolve success only) | resolver | `^bean_[A-Za-z0-9._-]{3,120}$` |

Opaque entropy after the prefix preferred `[Confirmed — SEP-2567 guidance]`.
Possession ≠ authorization when remote auth exists; local stdio treats handle as
capability with short TTL `[Evidenced — SEP-2567 Security]`.

### Exact vs adjacent GitHub adopters (schema-constrained tools)

| Repository / product | Exact or adjacent | Why |
| --- | --- | --- |
| `modelcontextprotocol/typescript-sdk` | **Exact** | `inputSchema`/`outputSchema` + runtime validate `structuredContent` |
| `modelcontextprotocol/python-sdk` | **Exact** | Return-type → `output_schema`; validates before emit |
| `PrefectHQ/fastmcp` | **Exact / adjacent** | Popular schema-first framework; historically wrapped non-object outputs (Model Context Protocol SEP-2106 motivation) |
| Official “everything” server Model Context Protocol SEP-2106 demos | **Exact** | Array/primitive `structuredContent` reference tools |
| `anthropics/skills` mcp-builder Node guide | **Adjacent** | Documents `registerTool` + Zod + `structuredContent` pattern |
| Linear / Notion / GitHub / Stripe remote Model Context Protocol | **Adjacent** (handles, not our schemas) | Create→id→operate pattern cited in Model Context Protocol SEP-2567 |

**≥5 exact-or-strong for “schema-constrained Model Context Protocol tools”:** yes (software development kit + FastMCP +
everything demos + builder guide). **Exact adopters of our five-tool Interface Control Document:**
**0** — Pilot our schemas; do not claim industry Adopt of `verify`/`resolve`
semantics.

### Embody / Adopt / Refuse

| Piece | Tier |
| --- | --- |
| JSON Schema 2020-12 + `$schema` explicit on Interface Control Document files | **Adopt** |
| Object-rooted `outputSchema` + TextContent JSON twin | **Adopt** |
| Zod at TypeScript presentation validating Interface Control Document shapes | **Adopt** |
| Bare-array `structuredContent` as wave-1 default | **Refuse** (interop risk) |
| External `$ref` fetch in validators | **Refuse** |

---

## 2) Snapshot-mint / handle lifecycle

### Spec / blog intent `[Evidenced]`

Official blog `2026-07-28`: dropping protocol sessions does **not** force
application statelessness — “mint an explicit handle from a tool and have the
model pass it back as an argument.”

Model Context Protocol SEP-2567 (Final): sessions removed; **explicit state handles are a tool-design
pattern, not a wire type**; guidance — opaque ids, create tool returns id in
`structuredContent`, operate tools take id, document durability, clear expiry
errors, possession ≠ auth.

### Design proposal (chosen)

| Field | Choice |
| --- | --- |
| **Mint tool name** | `snapshot_open` (preferred over `snapshot_create` / `index_bind` — “open” signals binding a consistent view, not mutating the tree) |
| **Who may call** | Any host / agent over stdio; later HTTP principal with read scope on `target_root` |
| **Binds** | `tree_sha` (material), `index_sha` (Source Code Index Protocol digest), optional `registry_epoch`, `indexer_name`/`indexer_version`, `built_at`, `expires_at` |
| **Returns** | `snapshot_id` (`snap_…`) in `structuredContent` |
| **Required by** | `resolve`, `claim_withdraw`; optional on `locks_list` / `verify` for digest pinning |
| **Expiry** | Wall-clock TTL (default proposal: 1 hour idle) **or** earlier if tree/index digests drift → `expired_handle` / `index_stale` |
| **Refresh** | Call `snapshot_open` again; old id rejected; no silent upgrade |
| **Who decides mint** | Harness / engine (`IndexLoad`); model only proposes args |

### Alternatives scored (0–2 × six vectors; sensor only)

| Option | Why | What | Who | How | When | Where | Total | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **A. `snapshot_open` tools/call mint** | 2 | 2 | 2 | 2 | 2 | 2 | **12** | **Working hypothesis (Draft)** — Pilot invent |
| B. Implicit cwd / process session | 0 | 0 | 1 | 0 | 0 | 1 | 2 | **Refuse** (Model Context Protocol SEP-2567; concurrent agents) |
| C. `resource://snapshot/{id}` only | 1 | 1 | 1 | 1 | 1 | 1 | 6 | **Defer** as Could companion (read metadata); mint still via tool |
| D. Auto-mint inside every `verify` | 1 | 1 | 1 | 1 | 2 | 1 | 7 | **Defer** — hides checkpoint for resolve-only flows |
| E. Client-invented `snap_` strings | 0 | 0 | 0 | 0 | 1 | 0 | 1 | **Refuse** (ST-5) |

### Usage cases ↔ mint

| ID | How `snapshot_id` appears |
| --- | --- |
| UC-Model Context Protocol-01 | Optional: `snapshot_open` → `locks_list(snapshot_id)` → `verify` |
| UC-Model Context Protocol-02 | **Required:** prior `snapshot_open` → `resolve(..., snapshot_id)` |
| UC-Model Context Protocol-03 | Optional pin on `verify`; mint not mandatory if only lock_set used — **recommend** mint for material bind |
| UC-Model Context Protocol-04 | **Required:** `claim_withdraw(snapshot_id)` |
| UC-Model Context Protocol-05 | Same mint over stdio |
| UC-Model Context Protocol-06 | Same; headers unrelated to handle |
| UC-Model Context Protocol-07 | Invented `snap_…` → `unknown_handle` |
| UC-Model Context Protocol-08 | Matrix/Architecture Decision Record audit trail |

**Interface Control Document change implication (not applied in this research-only pass):** add
`snapshot_open` to the tools table (fifth primitive) or document it as
wave-1.5 **blocking** resolve/claim. Decision Matrix already lists mint as
open gap.

---

## 3) Effect-checkpoint fixtures

### Paper digest summary `[Evidenced — arXiv:2607.20531 HTML + Atom]`

See `research/papers-2026-may-aug/digests/2607.20531-dynamicmcpbench.md`.

- **Primary type:** benchmark `[Inferred]`.  
- **Core objects:** tool-effect checkpoints (equivalence sets + arg predicates),
  `value_produced` checkpoints, **minefields**, **partial order**.  
- **Tier-1:** deterministic; headline leaderboard. **Tier-2:** large-language-model
  judge may only upgrade failed tool-effect equivalence — never grades final
  answer.  
- **False-green bite for us:** narrative “verify passed” without receipt /
  disposition effects.

### Public code status — exact engine = 0 / pending `[Evidenced / Unknown]`

| Artifact | Status 2026-08-10 |
| --- | --- |
| arXiv HTML/PDF | Public |
| Hugging Face `anonsubmitter/DynamicMCPBench` | Public dataset (specs/traces/leaderboards); lastModified 2026-06-17; points at anonymous code |
| `https://anonymous.4open.science/r/DynamicMCPBench-4243/` | **HTTP 403** from this research environment — contents **Unknown** here |
| Non-anonymous GitHub product engine | **Not found** → **exact engine adopters = 0** |
| Paper text | Still says code/data “will be released upon publication” in places — treat shipped HF as **partial**, engine as **pending** |

**Verdict:** **Embody** scoring ideas; **Pilot** plant fixtures in-repo;
**Refuse** depending on anonymous.4open as CI System of Record.

### Our plant fixtures (propose)

| Fixture ID | Tool under test | Effect checkpoints (Tier-1) | Equivalence set | Minefields | Partial order | Maps to |
| --- | --- | --- | --- | --- | --- | --- |
| **FX-Model Context Protocol-VERIFY-RECEIPT** | `verify` | (1) tool-effect `verify` called with known `lock_set_id`; (2) **value_produced:** filesystem path in `receipt_path` exists; (3) receipt JSON `result` ∈ {pass,fail,unknown}; (4) `material_digest` present | singleton `{verify}` | `llm_witness` field in receipt; narrative-only pass without file | mint/list before verify if using snapshot pin | F-06/06b; N-06; UC-Model Context Protocol-03 |
| **FX-Model Context Protocol-RESOLVE-UNKNOWN** | `resolve` | `resolve` with minted `snapshot_id` + known `site_…`; status ∈ {resolved, unknown, unprovable} | singleton | free-text bean name arg; invented `snap_` | `snapshot_open` ≺ `resolve` | F-01…05; UC-Model Context Protocol-02 |
| **FX-Model Context Protocol-CLAIM-DISP** | `claim_withdraw` | dispositions[] length ≥1; each `disposition` ∈ {unaffected, affected, unprovable}; freshness present | singleton | inventing `unprovable` without harness; chat-memory substitute | `snapshot_open` ≺ `claim_withdraw` | F-06c / N-07; UC-Model Context Protocol-04 |
| **FX-Model Context Protocol-MINE-WITNESS** | any mutating | — | — | structuredContent or receipt contains `llm_text` / `rag_chunk` / `narrative_pass` → fail (`llm_witness_forbidden`) | — | FX-Stateful Tool-Enabled Agentic Deployment family; ST-5 |
| **FX-Model Context Protocol-MINE-HANDLE** | `resolve` / `claim_withdraw` | — | — | invented handle / wrong prefix → expect `unknown_handle` reject (success = reject observed) | — | FX-Stateful Tool-Enabled Agentic Deployment; UC-Model Context Protocol-07; F-09b / N-08 |

### Map to Verification and Validation Accept methods

| Accept method (vv-plan) | Fixture |
| --- | --- |
| F-01…05 | FX-Model Context Protocol-RESOLVE-UNKNOWN (+ FX-CYCLE/LAYER plants for engine) |
| F-06/06b | FX-Model Context Protocol-VERIFY-RECEIPT |
| F-06c / N-07 | FX-Model Context Protocol-CLAIM-DISP |
| F-09b / N-08 | FX-Model Context Protocol-MINE-HANDLE (+ FX-Stateful Tool-Enabled Agentic Deployment) |
| N-06 | FX-Model Context Protocol-VERIFY-RECEIPT (two runs → canonical compare) |
| Agent “looks green” without receipt digests | **fail** (existing vv-plan rule) |

Tier-2 large-language-model judge: **sensor only**, never Definition of Ready
boolean System of Record `[Confirmed — constitution]`.

---

## Adversarial checklist (Bloom Evaluate)

| Attack | Expected harness behavior |
| --- | --- |
| Model invents `snap_deadbeef` | `unknown_handle` |
| Model pastes expired snapshot | `expired_handle` / `index_stale` |
| Model claims verify pass in prose only | No Accept; FX-Model Context Protocol-VERIFY-RECEIPT fails without file |
| Receipt embeds large language model witness | `llm_witness_forbidden`; fixture minefield |
| Client omits `Mcp-Method` on HTTP | `header_body_mismatch` |
| Schema uses draft-07 `dependencies` only | Fail dialect review; pin 2020-12 |
| Treat DynamicMCPBench HF as merge gate | Refuse — engine pending; use our FX-\* |

---

## Research-depth status

| Gate | Status |
| --- | --- |
| A1 Paper digest (DynamicMCPBench) | **PASS** — digest file written |
| A2 Related walk | **PARTIAL** — τ-bench / Contracts / Stateful Tool-Enabled Agentic Deployment named; full digests optional |
| A3 ≥5 exact algorithm adopters | **PASS** for Model Context Protocol schema+handle *patterns*; **FAIL / Pilot** for our tool semantics and DynamicMCPBench *engine* (0) |
| DeepWiki Ask | **WAIVED** — tool absent this run |
| Bloom 6 Create | **Not started** (research-only) |

---

## Recommendations (for Spec, not Implement)

1. Promote `07-system-design/icd/mcp/*.schema.json` drafts (below) into Interface Control Document System of Record; cite ST-1…5.  
2. Add `snapshot_open` to Interface Control Document tools table + Decision Matrix handle inventory.  
3. Author FX-Model Context Protocol-\* under `08-verification/` as plant specs before `packages/mcp-server`.  
4. Keep DynamicMCPBench as literature Embody until non-anonymous engine + Spike exit.  
5. Re-open on next Model Context Protocol Spec revision or first remote host.

---

## Draft JSON Schema file contents

Target directory: `07-system-design/icd/mcp/`. Dialect JSON Schema 2020-12.
These drafts may already exist on disk from a parallel Spec pass — treat this
section as the research-authored System of Record text for review.

### `common.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/common-0.1.json",
  "title": "McpCommonDefs",
  "$defs": {
    "handleId": {
      "type": "string",
      "minLength": 8,
      "maxLength": 128,
      "pattern": "^(snap|lock|run|site|claim)_[A-Za-z0-9._-]{6,120}$",
      "description": "Minted handle; prefix encodes kind. Models must not invent these."
    },
    "snapshotId": {
      "allOf": [
        { "$ref": "#/$defs/handleId" },
        { "pattern": "^snap_" }
      ]
    },
    "lockSetId": {
      "allOf": [
        { "$ref": "#/$defs/handleId" },
        { "pattern": "^lock_" }
      ]
    },
    "runId": {
      "allOf": [
        { "$ref": "#/$defs/handleId" },
        { "pattern": "^run_" }
      ]
    },
    "injectionSiteId": {
      "allOf": [
        { "$ref": "#/$defs/handleId" },
        { "pattern": "^site_" }
      ]
    },
    "claimId": {
      "type": "string",
      "pattern": "^claim_[A-Za-z0-9._-]{6,120}$"
    },
    "absolutePath": {
      "type": "string",
      "minLength": 1,
      "description": "Absolute filesystem path under the trusted target root"
    },
    "sha256Hex": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$"
    },
    "rejectClass": {
      "type": "string",
      "enum": [
        "unknown_id",
        "unknown_handle",
        "expired_handle",
        "stale_receipt",
        "llm_witness_forbidden",
        "schema_invalid",
        "header_body_mismatch",
        "protocol_version_unsupported",
        "equivariance_reject",
        "index_missing",
        "index_stale",
        "search_fallback_forbidden"
      ]
    },
    "toolError": {
      "type": "object",
      "required": ["reject_class", "message"],
      "additionalProperties": false,
      "properties": {
        "reject_class": { "$ref": "#/$defs/rejectClass" },
        "message": { "type": "string", "maxLength": 500 },
        "hint": { "type": "string", "maxLength": 500 }
      },
      "not": {
        "required": ["llm_text", "rag_chunk", "narrative_pass"]
      }
    }
  }
}
```

### `snapshot_open.input.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/snapshot-open-input-0.1.json",
  "title": "snapshot_open.input",
  "description": "Mint a snapshot_id bound to tree + index digests. Required before resolve / claim_withdraw / scoped locks_list.",
  "type": "object",
  "additionalProperties": false,
  "required": ["target_root"],
  "properties": {
    "target_root": {
      "$ref": "common.schema.json#/$defs/absolutePath"
    },
    "require_index": {
      "type": "boolean",
      "default": true,
      "description": "If true, reject when index missing or stale vs tree"
    }
  }
}
```

### `snapshot_open.output.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/snapshot-open-output-0.1.json",
  "title": "snapshot_open.output",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "snapshot_id",
    "tree_sha",
    "index_sha",
    "indexer_name",
    "indexer_version",
    "built_at",
    "expires_at"
  ],
  "properties": {
    "snapshot_id": { "$ref": "common.schema.json#/$defs/snapshotId" },
    "tree_sha": { "$ref": "common.schema.json#/$defs/sha256Hex" },
    "index_sha": { "$ref": "common.schema.json#/$defs/sha256Hex" },
    "indexer_name": { "type": "string", "minLength": 1 },
    "indexer_version": { "type": "string", "minLength": 1 },
    "registry_epoch": { "type": "integer", "minimum": 0 },
    "built_at": { "type": "string", "format": "date-time" },
    "expires_at": { "type": "string", "format": "date-time" }
  }
}
```

### `verify.input.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/verify-input-0.1.json",
  "title": "verify.input",
  "type": "object",
  "additionalProperties": false,
  "required": ["target_root", "lock_set_id"],
  "properties": {
    "target_root": { "$ref": "common.schema.json#/$defs/absolutePath" },
    "lock_set_id": { "$ref": "common.schema.json#/$defs/lockSetId" },
    "snapshot_id": {
      "$ref": "common.schema.json#/$defs/snapshotId",
      "description": "Optional; when present, material digests must match snapshot"
    }
  }
}
```

### `verify.output.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/verify-output-0.1.json",
  "title": "verify.output",
  "type": "object",
  "additionalProperties": false,
  "required": ["run_id", "receipt_path", "result", "material_digest", "policy_digest"],
  "properties": {
    "run_id": { "$ref": "common.schema.json#/$defs/runId" },
    "receipt_path": { "$ref": "common.schema.json#/$defs/absolutePath" },
    "result": { "enum": ["pass", "fail", "unknown"] },
    "material_digest": { "$ref": "common.schema.json#/$defs/sha256Hex" },
    "policy_digest": { "$ref": "common.schema.json#/$defs/sha256Hex" }
  },
  "not": {
    "required": ["llm_text", "narrative_pass"]
  }
}
```

### `resolve.input.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/resolve-input-0.1.json",
  "title": "resolve.input",
  "type": "object",
  "additionalProperties": false,
  "required": ["injection_site_id", "snapshot_id"],
  "properties": {
    "injection_site_id": { "$ref": "common.schema.json#/$defs/injectionSiteId" },
    "snapshot_id": { "$ref": "common.schema.json#/$defs/snapshotId" }
  }
}
```

### `resolve.output.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/resolve-output-0.1.json",
  "title": "resolve.output",
  "type": "object",
  "additionalProperties": false,
  "required": ["status"],
  "properties": {
    "status": { "enum": ["resolved", "unknown", "unprovable"] },
    "bean_id": { "type": "string", "pattern": "^bean_[A-Za-z0-9._-]{3,120}$" },
    "witness": {
      "type": "object",
      "additionalProperties": false,
      "required": ["file", "line", "column"],
      "properties": {
        "file": { "type": "string" },
        "line": { "type": "integer", "minimum": 1 },
        "column": { "type": "integer", "minimum": 0 },
        "symbol": { "type": "string" }
      },
      "not": { "required": ["llm_text", "rag_chunk"] }
    }
  }
}
```

### `claim_withdraw.input.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/claim-withdraw-input-0.1.json",
  "title": "claim_withdraw.input",
  "type": "object",
  "additionalProperties": false,
  "required": ["snapshot_id"],
  "properties": {
    "snapshot_id": { "$ref": "common.schema.json#/$defs/snapshotId" },
    "claim_id": {
      "$ref": "common.schema.json#/$defs/claimId",
      "description": "Optional; omit to withdraw all anchors invalidated by snapshot"
    }
  }
}
```

### `claim_withdraw.output.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/claim-withdraw-output-0.1.json",
  "title": "claim_withdraw.output",
  "type": "object",
  "additionalProperties": false,
  "required": ["dispositions"],
  "properties": {
    "dispositions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["claim_id", "disposition", "freshness"],
        "properties": {
          "claim_id": { "$ref": "common.schema.json#/$defs/claimId" },
          "disposition": { "enum": ["unaffected", "affected", "unprovable"] },
          "freshness": { "enum": ["fresh", "stale", "unknown"] },
          "artifact_disposition": {
            "enum": ["retain", "withdraw"],
            "description": "Independent of claim disposition (Artifact-Anchored Verification Memory DISP)"
          }
        }
      }
    }
  }
}
```

### `locks_list.input.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/locks-list-input-0.1.json",
  "title": "locks_list.input",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "snapshot_id": { "$ref": "common.schema.json#/$defs/snapshotId" },
    "target_root": { "$ref": "common.schema.json#/$defs/absolutePath" }
  },
  "anyOf": [
    { "required": ["snapshot_id"] },
    { "required": ["target_root"] }
  ]
}
```

### `locks_list.output.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://verified-architecture.local/schemas/mcp/locks-list-output-0.1.json",
  "title": "locks_list.output",
  "type": "object",
  "additionalProperties": false,
  "required": ["lock_set_id", "locks"],
  "properties": {
    "lock_set_id": { "$ref": "common.schema.json#/$defs/lockSetId" },
    "locks": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["lock_id", "path"],
        "properties": {
          "lock_id": { "type": "string", "minLength": 1 },
          "path": { "type": "string", "minLength": 1 },
          "mode": { "enum": ["strict", "gradual"] }
        }
      }
    },
    "policy_digest": { "$ref": "common.schema.json#/$defs/sha256Hex" }
  }
}
```

---

## Sources

- https://blog.modelcontextprotocol.io/posts/2026-07-28/
- https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- https://modelcontextprotocol.io/llms.txt
- https://modelcontextprotocol.org/seps/1613-establish-json-schema-2020-12-as-default-dialect-f
- https://modelcontextprotocol.org/seps/2106-json-schema-2020-12
- https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/seps/2567-sessionless-mcp.md
- https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/docs/servers/tools.md
- https://py.sdk.modelcontextprotocol.io/servers/structured-output/
- https://arxiv.org/abs/2607.20531 · https://arxiv.org/html/2607.20531
- https://huggingface.co/datasets/anonsubmitter/DynamicMCPBench
- Port: Decision Matrix, Interface Control Document ICD-MCP, Architecture Decision Record ADR-0011, `STEAD_CONSTRAINTS` (Stateful Tool-Enabled Agentic Deployment constraints), vv-plan, decision-framework
