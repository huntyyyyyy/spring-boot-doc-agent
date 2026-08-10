---
title: MCP / CLI tools ICD — primitives + STEAD
status: DRAFT
date: '2026-08-10'
evidence:
  - arXiv:2608.03609
  - arXiv:2607.08028
  - arXiv:2606.13663
---

# ICD-MCP — primitive tools (wave-1)

HyperTool-style composition blocks = **Could** later. MVP exposes **primitives**
with schemas; harness is code-owned (Contracts 2607.08028).

## STEAD constraints (normative)

See `08-verification/stead/STEAD_CONSTRAINTS.md` ST-1…5.

- Entity parameters (`bean_id`, `symbol`, `edge_id`, `claim_id`, `file`) MUST
  match ids present in the current snapshot or the call is rejected.
- No free-text “bean name from the model” parameters.

## Tools

| Tool | Args (typed) | Effect checkpoint |
| --- | --- | --- |
| `verify` | `target_root: path`, `lock_set_id: id` | receipt written; exit code reflects result |
| `resolve` | `injection_site_id: id` | resolve_result schema; Unknown allowed |
| `claim_withdraw` | `snapshot_id: id` | dispositions[] returned |
| `locks_list` | none | returns lock ids from git SoR |

## Reject classes (harness)

unknown_id · stale_receipt · llm_witness_forbidden · schema_invalid
