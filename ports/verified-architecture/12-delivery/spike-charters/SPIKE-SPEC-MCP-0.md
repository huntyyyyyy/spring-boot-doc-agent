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

# SPIKE-SPEC-Model Context Protocol-0

Read-only Model Context Protocol over the Spec / FREEZE corpus. **Refuse**
product `verify` / writes. **Refuse Python** (host, ACI, or “tip convenience”).

| Field | Content |
| --- | --- |
| **Host** | **Rust** stdio via official Model Context Protocol Rust software development kit — only |
| Crates (Spike plan) | `serde_yaml` + Jekyll-style `---` split; `jsonschema` vs `va-doc-frontmatter.schema.json`; `blake3` corpus digest; `look_first`/`related` walk |
| WebAssembly | Optional Extism/wasmtime **guest** for untrusted parse probes — **Refuse** as Spec host |
| Cursor layer | Thin `.cursor/rules/projections/*.mdc` — activation only; MD remains corpus SoT |
| Frontmatter SoT | `07-system-design/schemas/va-doc-frontmatter.schema.json` — Rust validates + indexes |
| Tools | `spec_status`, `spec_assumption`, `spec_icd`, `spec_decision`, `spec_gap`, optional `spec_lookup` |
| Tool filter | `mcp_tools` contains tool; `doc_role`; refuse `accepted:true` under FREEZE for decisions |
| Drop | Any Python Spec path; product verify sneaking in; second catalog |
| FREEZE | No tip `crates/` product scaffold until Spike is scheduled; charter + schema only is OK |
| Later Could | Go `corpus_version` watch sidecar; WebAssembly sandboxed markdown reader plugin |
