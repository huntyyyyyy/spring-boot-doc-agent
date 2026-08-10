---
title: ICD index — contracts before code
status: DRAFT
date: '2026-08-10'
---

# Interface control documents (index)

Each ICD is a schema + invariants file. **Write schemas here before code.**

| ICD | Path (to create) | Covers |
| --- | --- | --- |
| ICD-LOCK | `icd/lock-ir.schema.json` | Lock IR / MDC→IR compile |
| ICD-REG | `icd/registry.sql.md` | SQLite DDL + meaning of tables |
| ICD-RCPT | `icd/receipt.schema.json` | Proof-tour receipt |
| ICD-CLAIM | `icd/ea-graph-claims.schema.json` | EA-Graph claim + anchor + disposition |
| ICD-RESOLVE | `icd/resolve-result.schema.json` | bean \| Unknown \| unprovable |
| ICD-MCP | `icd/mcp-tools.md` | Tool names + JSON shapes **+ STEAD ST-1…5** |
| ICD-LSP | `icd/lsp-diagnostics.md` | Diagnostic field mapping |

Until these exist as Draft files, DoR D7 stays FAIL.
