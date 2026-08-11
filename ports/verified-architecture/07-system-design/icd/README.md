---
title: Interface Control Document index — contracts before code
status: DRAFT
date: '2026-08-10'
---

# Interface control documents (index)

Schemas and fail-modes land here **before** crates. Cold agents use paths below;
do not invent parallel contracts in prompts.

| ID | Path | Attributes / fail-modes |
| --- | --- | --- |
| ICD-LOCK | `lock-ir.schema.json` | Package Intermediate Representation; silent `update-todo` forbidden |
| ICD-REG | `registry.sql.md` | Derived SQLite DDL; wipe/rebuild OK; never policy System of Record |
| ICD-RCPT | `receipt.schema.json` | β/ρ digests; `llm_text` witness → reject |
| ICD-CLAIM | `ea-graph-claims.schema.json` | Artifact anchors; disposition includes `unprovable` |
| ICD-RESOLVE | `resolve-result.schema.json` | bean \| Unknown \| unprovable — never silent pick |
| ICD-MCP | `mcp-tools.md` + `mcp/*.schema.json` | Primitives + handles; `unknown_handle` / session state refuse |
| ICD-LSP | `lsp-diagnostics.md` | Diagnostic field mapping (Wave-2) |

| Topic | Matrix | Architecture Decision Record |
| --- | --- | --- |
| Model Context Protocol | `../decisions/mcp-decision-matrix.md` | ADR-0011 |
| Lock Intermediate Representation | `../decisions/lock-ir-decision-matrix.md` | ADR-0003 |
| Freshness-bound receipts | `../decisions/receipt-decision-matrix.md` | pending Accept |

Effect plants: `../../08-verification/plants/mcp-effects/`.

Draft schemas **exist**; Definition of Ready D7 stays FAIL until **human Accept**.
Open question 04 (adapter map) and open question 05 (`step_id` / ls-tree canon)
remain open.
