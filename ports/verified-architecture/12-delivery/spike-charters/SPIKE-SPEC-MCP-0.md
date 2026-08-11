---
title: Spike — Spec corpus Model Context Protocol (read-only, Rust)
status: DRAFT — optional; not Wave-1 Must; not product verify
date: '2026-08-10'
source: research/gaps/spec-corpus-mcp-polyglot-2026-08-10.md
doc_role: spike
freeze_class: deepen
look_first:
  - research/gaps/frontmatter-forced-traversal-mcp-2026-08-10.md
  - 07-system-design/schemas/va-doc-frontmatter.schema.json
  - docs/adr/adr-0007-rust-owns-engine.md
mcp_tools:
  - spec_status
  - spec_gap
accepted: false
corpus_version: '2026-08-10'
related:
  - research/gaps/frontmatter-forced-traversal-mcp-2026-08-10.md
  - 07-system-design/schemas/va-doc-frontmatter.schema.json
  - docs/adr/adr-0007-rust-owns-engine.md
  - research/gaps/spec-corpus-mcp-polyglot-2026-08-10.md
---

# SPIKE-SPEC-Model Context Protocol-0

Read-only Model Context Protocol over the Spec / FREEZE corpus. **Refuse**
product `verify` / writes / WebAssembly LockCheck. **Refuse** tip-Python as
host (circular Why).

| Field | Content |
| --- | --- |
| **Host** | **Rust** stdio via official Model Context Protocol Rust software development kit |
| Crates (Spike plan) | `serde_yaml` + Jekyll-style `---` split (not pulldown-cmark-frontmatter code-block dialect); `jsonschema` vs `va-doc-frontmatter.schema.json`; `blake3` corpus digest; path walk for `look_first`/`related` |
| WebAssembly | Optional Extism/wasmtime **guest** for untrusted parse probes (deny net) — Architecture Decision Record ADR-0004 honesty; **Refuse** as Spec host |
| Cursor layer | Thin `.cursor/rules/projections/*.mdc` — activation only; MD remains corpus SoT |
| Frontmatter SoT | `07-system-design/schemas/va-doc-frontmatter.schema.json` — Rust validates + indexes |
| Tools | `spec_status`, `spec_assumption`, `spec_icd`, `spec_decision`, `spec_gap`, optional `spec_lookup` |
| Tool filter | `mcp_tools` contains tool; `doc_role`; refuse `accepted:true` under FREEZE for decisions |
| Resources | Index rows (path, title, status, doc_role, freeze_class, look_first) — not unbounded `cat` |
| Keep | Same edges Cursor MDC mandates; forged-handle reject plant; content-addressed corpus digest |
| Drop | Python Spec host “because tip has E-MD0”; product verify sneaking in; second catalog |
| Tip Python | E-MD0 `check_md_frontmatter` may stay a **monorepo research gate** — out of scope for this Spike’s runtime |
| FREEZE | No tip `crates/` product scaffold until Spike is scheduled; charter + schema only is OK |
| Later Could | Go `corpus_version` watch sidecar; WebAssembly sandboxed markdown reader plugin |
