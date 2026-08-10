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
| ICD-MCP | `icd/mcp-tools.md` | Tool names + JSON shapes **+ STEAD ST-1…5** + usage cases |
| ICD-LSP | `icd/lsp-diagnostics.md` | Diagnostic field mapping |

**MCP decision matrix** (what/when/how/who/where/why, alternatives, planned
code map): `../decisions/mcp-decision-matrix.md` · ADR-0011.

Until schemas + matrices exist as Draft files, Definition of Ready D7 stays FAIL.
