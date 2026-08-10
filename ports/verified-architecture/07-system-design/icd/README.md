---
title: ICD index — contracts before code
status: DRAFT
date: '2026-08-10'
---

# Interface control documents (index)

Each Interface Control Document is a schema + invariants file. **Write schemas
here before code.**

| ICD | Path | Covers |
| --- | --- | --- |
| ICD-LOCK | `icd/lock-ir.schema.json` | Lock Intermediate Representation (Draft) |
| ICD-REG | `icd/registry.sql.md` | SQLite DDL + meaning of tables |
| ICD-RCPT | `icd/receipt.schema.json` | Proof-tour receipt (+ β/ρ Draft) |
| ICD-CLAIM | `icd/ea-graph-claims.schema.json` | Artifact-anchored claim + disposition |
| ICD-RESOLVE | `icd/resolve-result.schema.json` | bean \| Unknown \| unprovable |
| ICD-MCP | `icd/mcp-tools.md` + `icd/mcp/*.schema.json` | Tools + STEAD + JSON Schema 2020-12 |
| ICD-LSP | `icd/lsp-diagnostics.md` | Diagnostic field mapping |

**Decision matrices:**

| Topic | Matrix | Architecture Decision Record |
| --- | --- | --- |
| Model Context Protocol | `../decisions/mcp-decision-matrix.md` | ADR-0011 |
| Lock Intermediate Representation | `../decisions/lock-ir-decision-matrix.md` | ADR-0003 |
| Freshness-bound receipts | `../decisions/receipt-decision-matrix.md` | (pending Accept) |

**Effect plants:** `../../08-verification/plants/mcp-effects/`.

Draft schemas **exist**; Definition of Ready D7 stays FAIL until **human Accept**.
Open question 04 (adapter map) and open question 05 (step_id / ls-tree canon)
remain open.
