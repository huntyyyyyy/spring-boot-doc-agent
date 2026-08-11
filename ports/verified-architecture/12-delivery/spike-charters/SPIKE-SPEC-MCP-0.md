---
title: Spike — Spec corpus Model Context Protocol (read-only, Rust only)
status: DRAFT — optional; not Wave-1 Must; not product verify
date: '2026-08-10'
last_reviewed: '2026-08-11'
source: research/gaps/spec-corpus-mcp-polyglot-2026-08-10.md
doc_role: spike
freeze_class: deepen
look_first:
  - research/gaps/port-mdc-projection-rust-wasm-2026-08-11.md
  - 07-system-design/schemas/va-doc-frontmatter.schema.json
  - docs/adr/adr-0007-rust-owns-engine.md
mcp_tools:
  - spec_status
  - spec_gap
accepted: false
corpus_version: '2026-08-11'
related:
  - research/gaps/frontmatter-forced-traversal-mcp-2026-08-10.md
  - research/gaps/port-mdc-projection-rust-wasm-2026-08-11.md
  - 07-system-design/schemas/va-doc-frontmatter.schema.json
  - docs/adr/adr-0007-rust-owns-engine.md
  - docs/adr/adr-0001-polyglot-first-product.md
---

# SPIKE-SPEC-MCP-0

Read-only MCP over Spec / FREEZE corpus. **Not** product `verify`.

| Field | Predicate | Fail-mode |
| --- | --- | --- |
| **Host** | **Rust** stdio via official MCP Rust SDK — only | Any Python/TS Spec host → reject |
| Crates (plan) | `serde_yaml` + `---` split; `jsonschema` vs `va-doc-frontmatter.schema.json`; `blake3` digest; `look_first`/`related` walk | Second catalog / unverified index → reject |
| WebAssembly | Could: Extism/wasmtime **guest** for untrusted parse probes | WASM as Spec **host** → **Refuse** |
| Cursor layer | Thin `.cursor/rules/projections/*.mdc` — activation only | MDC as corpus SoT → reject (MD remains SoT) |
| Frontmatter SoT | `07-system-design/schemas/va-doc-frontmatter.schema.json` — Rust validates + indexes | Schema drift without Rust revalidate → reject |
| Tools | `spec_status`, `spec_assumption`, `spec_icd`, `spec_decision`, `spec_gap`, optional `spec_lookup` | Product verify tools sneaking in → drop |
| Tool filter | `mcp_tools` contains tool; `doc_role`; refuse `accepted:true` under FREEZE for decisions | Unfiltered tool → reject |
| Drop | Python Spec path; product verify; second catalog | — |
| FREEZE | Charter + schema OK; no tip `crates/` product scaffold until Spike scheduled | Premature scaffold → reject |
| Later Could | Go `corpus_version` watch sidecar; WASM sandboxed markdown reader plugin | — |
