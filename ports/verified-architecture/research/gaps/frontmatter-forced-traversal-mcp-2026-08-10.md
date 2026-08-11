---
title: Forced traversal via MDC + frontmatter schemas (Rust Spec Model Context Protocol SoT)
status: RESEARCH — Adopt for Spec corpus routing; Rust serves index; NOT product verify
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
related:
  - research/gaps/spec-corpus-mcp-polyglot-2026-08-10.md
  - 12-delivery/spike-charters/SPIKE-SPEC-MCP-0.md
  - 07-system-design/schemas/va-doc-frontmatter.schema.json
  - docs/adr/adr-0007-rust-owns-engine.md
  - research/mdc-devex/cursor-mdc-activation-algebra.md
do_not:
  - Mass-convert Markdown into always-on .mdc
  - Any Python Spec / ACI / host path for this port
  - Soft-pass Definition of Ready with richer metadata alone
  - Tip Cargo product scaffolds under FREEZE — Spike charter only until scheduled
last_reviewed: '2026-08-10'
doc_role: gap
freeze_class: deepen
look_first:
  - STATUS.md
  - research/INDEX.md
  - docs/adr/adr-0007-rust-owns-engine.md
mcp_tools:
  - spec_status
  - spec_gap
accepted: false
corpus_version: '2026-08-10'
---

# Forced traversal — MDC points; Rust serves the graph

**User challenge (accepted):** Forced pointing + frontmatter schemas are right;
**serving** that graph for agents/Model Context Protocol is a **Rust** job
(Architecture Decision Record ADR-0007 engine DNA / Spec digest), not another
Python tip convenience layer.

## 0. Verdict

| Layer | Owns | Stack |
| --- | --- | --- |
| Cursor `.mdc` | Mandate the walk (`look_first` → `related`) | Activation algebra — not a catalog SoT |
| Markdown frontmatter | Edge data + route keys | Closed schema (JSON Schema file) |
| Spec corpus Model Context Protocol | Answer agent queries from that graph | **Rust** (Spike) — parse FM, index, filter tools, digests |
| Tip monorepo E-MD0 gate | Outside this port | Not a port runtime — do not import |
| Product verify Model Context Protocol | Later; separate System of Record | Rust engine — out of Spec Spike scope |

Mass `.md` → `.mdc` remains **Refuse**. Progressive disclosure without machine
edges remains **insufficient** — Adopt forced pointing.

## 1. What MDC forces (and what it cannot)

Always-on rules can **mandate** a protocol; they cannot execute walks. Globs
attach lenses; Skills do depth; hooks deny. **Force** = mandate + edges in
frontmatter + a **query surface** that returns those edges. That query surface
is Spec Model Context Protocol — **Rust**.

## 2. Frontmatter features → schema → Rust

| Feature | Job |
| --- | --- |
| `related` / `look_first` | Forced pointer lists |
| `doc_role` / `mcp_tools` | Tool routing |
| `freeze_class` / `accepted` / `corpus_version` | FREEZE stamps |
| `claim_tiers` / Bloom / `blocks_code` | Honesty gates |

Schema SoT: `07-system-design/schemas/va-doc-frontmatter.schema.json`.  
Spike SoT: `SPIKE-SPEC-MCP-0` — Rust validates schema, builds index, serves tools.

## 3. Forced pointing protocol (≤5 opens / turn)

1. Frontmatter of active file first.
2. `look_first` in order.
3. `related` until budget.
4. Prefer Spec tools when live (Rust server).
5. Refuse invented paths.

## 4. Rejected

- Python Spec host because tip E-MD0 / `adapters/mcp` already exist (**circular Why**).
- WebAssembly as Spec host (sandbox guest Could only).
- Product verify tools as planning corpus SoT.

## Claim tiers

- **Evidenced** — Cursor rule modes; E-MD0 tip gate; ADR-0007 Proposed; MCP Rust SDK exists.
- **Confirmed** — Soft “prefer INDEX” underperforms without edges + query.
- **Unknown** — Spike schedule vs deepen-3 handle lifecycle ordering.
