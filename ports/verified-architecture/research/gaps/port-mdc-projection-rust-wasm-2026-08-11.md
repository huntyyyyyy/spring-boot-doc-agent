---
title: Port-only MDC projection + Rust/WASM stack (not whole monorepo)
status: RESEARCH — Adopt for ports/verified-architecture; FREEZE-aware
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
related:
  - research/mdc-devex/cursor-mdc-activation-algebra.md
  - research/gaps/frontmatter-forced-traversal-mcp-2026-08-10.md
  - 12-delivery/spike-charters/SPIKE-SPEC-MCP-0.md
  - 07-system-design/schemas/va-doc-frontmatter.schema.json
  - docs/adr/adr-0007-rust-owns-engine.md
  - docs/adr/adr-0004-native-then-wasm-lockcheck.md
  - research/mdc-devex/mdc-projection-inventory-2026-08-11.md
do_not:
  - Rename all research/*.md to .mdc outside .cursor/rules (Cursor ignores them)
  - Mass alwaysApply projections
  - Tip-Python Spec host
  - Product verify Model Context Protocol in this Spike
last_reviewed: '2026-08-11'
doc_role: gap
freeze_class: deepen
look_first:
  - STATUS.md
  - .cursor/rules/README.md
  - research/mdc-devex/mdc-projection-inventory-2026-08-11.md
mcp_tools:
  - spec_gap
accepted: false
corpus_version: '2026-08-11'
bloom_gate: required-through-create
bloom_mcp:
  - llms_txt
sources:
  llms_txt:
    - https://cursor.com/llms.txt
  primary_docs:
    - https://cursor.com/docs/rules.md
  arxiv:
    - '2607.17598'
  github:
    - https://github.com/pulldown-cmark/pulldown-cmark
    - https://github.com/extism/extism
---

# Port MDC reformatting — what Cursor owns vs what Rust/WASM adds

**Scope lock:** `ports/verified-architecture/` only. Parent tip E-MD0 / monorepo
research trees are out of scope for this conversion.

## 0. Verdict (one page)

| Claim | Decision |
| --- | --- |
| “Rename every port `.md` → `.mdc` for traversal” | **Refuse as bulk rename** — Cursor Project Rules only activate `.mdc` under `.cursor/rules/` `[Evidenced — cursor.com/docs/rules.md]`. A `.mdc` under `research/` is just a renamed file. |
| “Many port docs need MDC metadata + pointers” | **Adopt as projections** — thin `.cursor/rules/projections/*.mdc` (or topic lenses) with `description` / `globs` / `look_first` pointing at the Markdown SoT. |
| Unique MDC features vs MD | **Only** Cursor activation: `alwaysApply`, `globs`, `description` (+ `@` file refs). Body is still Markdown. |
| Shared corpus metadata (`doc_role`, `related`, …) | Lives in **Markdown YAML frontmatter** (schema) — same keys Rust Spec MCP indexes. |
| Rust on top | **Adopt (Spike)** — frontmatter parse, JSON Schema validate, corpus digest, Spec MCP tools. |
| WebAssembly on top | **Could** — sandboxed untrusted reader plugin (deny net/FS except corpus); **Refuse** as Spec host / proof (Architecture Decision Record ADR-0004 honesty). |

## 1. Bloom ladder

| Level | Evidence |
| --- | --- |
| 1 Remember | Cursor rules docs: `.md` in `.cursor/rules` **ignored**; three FM fields → four modes. arXiv `2607.17598` progressive disclosure. `pulldown-cmark`; Extism. |
| 2 Understand | Activation ≠ storage. Port has ~159 `.md` + 21 `.mdc` (12 root rules + 9 nests). |
| 3 Apply | Projection inventory + pilot projections under `.cursor/rules/projections/`. |
| 4 Analyze | Embody Cursor activation; Adopt Rust Spec stack; Refuse bulk rename; Refuse WASM host. |
| 5 Evaluate | False-green: renaming research to `.mdc` and claiming “rules work.” False-red: refusing all MDC growth when lenses are missing. |
| 6 Create | Inventory file + Spike Rust crate charter fields; projections landed for Wave-0 set. |

## 2. What MDC adds that MD does not (port)

| Feature | Where it works | Port use |
| --- | --- | --- |
| `alwaysApply: true` | `.cursor/rules/*.mdc` | ≤2: constitution + forced pointing |
| `globs` auto-attach | same | Path lenses when agent opens `07-` / `research/` / `08-` |
| `description` agent-request | same | Topic cards (Architecture Tradeoff Analysis Method, polyglot, Model Context Protocol) |
| Manual `@rule` | same | Formal honesty |
| `@path` include | rule body | Point at STATUS / INDEX / schema — do not paste memos |
| Nested nest.mdc + dual globs | `nests/*/.cursor/rules/` | Bounded context — already Adopt |

**Not** an MDC feature: claim tiers, Bloom, `look_first`, Spec tool filters — those are **our** frontmatter schema, served by **Rust**.

## 3. Progressive disclosure research (corpus scale)

arXiv **2607.17598** (*Is Progressive Disclosure All You Need for Long-Context Agents?*): on a *single* long doc, strong harnesses already navigate; at **multi-book / library** scale, **one-level** disclosure helps; deeper hierarchical routing often fails `[Evidenced — Atom + HTML abstract/methods]`.

**Port implication:** one projection level (MDC description/globs → open MD SoT) — do **not** nest projection→projection→memo indefinitely.

## 4. Rust + WebAssembly feature map (port Spec surface)

| Capability | Rust (Spike host) | WebAssembly guest |
| --- | --- | --- |
| Parse `---` YAML frontmatter | `serde_yaml` / gray-matter-style split (**not** pulldown-cmark-frontmatter’s code-block dialect — different shape) | Same logic compiled to guest |
| Validate `va-doc-frontmatter.schema.json` | `jsonschema` crate | Guest validate under fuel limit |
| Walk `look_first` / `related` | Native path resolve + existence | Guest returns edges only |
| Corpus digest / `corpus_version` | `blake3` tree hash | N/A |
| Spec MCP stdio | Official Rust Model Context Protocol software development kit | **Refuse** as host |
| Untrusted agent-generated parse probes | Host calls guest | Extism/wasmtime deny-net — Architecture Decision Record ADR-0004 pattern |
| Product LockCheck | Engine nest (later) | Wave-3 Could — not Spec v0 |

**Rejected:** growing tip Python E-MD0 into the port Spec server (circular Why).

## 5. Conversion policy (port)

| Kind | Action |
| --- | --- |
| Mandate / cold-start / FREEZE / verify spine | Thin **MDC projection** + keep short MD SoT **or** MDC-only if ≤150 lines and no human essay need |
| QAS / ADR / ICD / Decision Matrix bodies | Stay **MD** + frontmatter; glob lens already attaches |
| Long research memos / digests | Stay **MD**; never always-on MDC |
| README indexes | Stay **MD** |
| Nest READMEs | Stay **MD**; nest.mdc already points |

Full matrix: `research/mdc-devex/mdc-projection-inventory-2026-08-11.md`.

## 6. Exit

- Inventory lists Wave-0 projections (landed) vs Wave-1 backlog.
- Spike `SPIKE-SPEC-MCP-0` remains Rust host + this schema.
- No product `crates/` scaffold until Spike scheduled (FREEZE).
