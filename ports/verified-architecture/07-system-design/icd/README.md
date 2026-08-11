---
title: Interface Control Document index — contracts before code
status: DRAFT
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Interface control documents (index)

Schemas and fail-modes land here **before** crates. Cold agents use paths below;
do not invent parallel contracts in prompts.

| ID | Path | Attributes / fail-modes |
| --- | --- | --- |
| ICD-LOCK | `lock-ir.schema.json` | Package Intermediate Representation; silent `update-todo` forbidden |
| ICD-REG | `registry.sql.md` | Derived SQLite **sketch** (non-normative vs claim enums); wipe/rebuild OK; never policy System of Record |
| ICD-RCPT | `receipt.schema.json` | β/ρ digests; `llm_text` witness → reject — **receipt SoT** |
| ICD-CLAIM | `ea-graph-claims.schema.json` | Artifact anchors; disposition includes `unprovable` |
| ICD-MCP | `mcp-tools.md` + `mcp/*.schema.json` | Primitives + handles; `unknown_handle` / session state refuse |
| ICD-RESOLVE | *(Wave-2 — not on disk)* | Planned: bean \| Unknown \| unprovable — never silent pick |
| ICD-LSP | *(Wave-2 — not on disk)* | Planned: diagnostic field mapping |

| Topic | Matrix | Architecture Decision Record |
| --- | --- | --- |
| Model Context Protocol | `../decisions/mcp-decision-matrix.md` | ADR-0011 |
| Lock Intermediate Representation | `../decisions/lock-ir-decision-matrix.md` | ADR-0003 |
| Freshness-bound receipts | `../decisions/receipt-decision-matrix.md` | pending Accept |

Effect plants: `../../08-verification/plants/mcp-effects/` (Draft TaskSpecs; no Tier-1 Accept).

Draft schemas **exist**; Definition of Ready **D7 = PARTIAL** until **human Accept**
(same predicate as DoR — not a second FAIL). Open question 04 (adapter map) and
open question 05 (`step_id` / ls-tree canon) remain open.
