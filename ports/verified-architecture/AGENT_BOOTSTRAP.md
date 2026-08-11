---
title: Agent bootstrap — cold start with no chat history
status: ACTIVE
audience: [agent, developer]
doc_role: bootstrap
freeze_class: read_only
look_first:
  - STATUS.md
  - GLOSSARY.md
  - research/INDEX.md
  - .cursor/skills/predicate-prose/SKILL.md
mcp_tools:
  - spec_status
accepted: false
corpus_version: '2026-08-11'
related:
  - STATUS.md
  - research/gaps/anti-tautology-predicate-prose-2026-08-11.md
  - 07-system-design/schemas/va-doc-frontmatter.schema.json
---

# AGENT_BOOTSTRAP — read this first

You have **no prior conversation**. Open files in `look_first` order before
browsing.

## Hard facts (information gain)

| Fact | Bound |
| --- | --- |
| Code generation of product crates | **No** until Definition of Ready PASS |
| Prose | Whole words only — `GLOSSARY.md` |
| When editing Spec Markdown | Skill `predicate-prose` (no title-echo / synonym circles) |
| Retrieval | One pack via `research/INDEX.md` — never dump `research/` |

## Must spine (four legs)

If you reduce the product to “graph + locks,” you are wrong for this port:

1. Virtual dependency graph + lock Intermediate Representation  
2. Artifact-anchored claim memory (EA-Graph) — anchors; evidence ≠ freshness;
   disposition `unprovable`  
3. Stateful Tool-Enabled Agentic Deployment tool constraints — typed ids,
   equivariance; no First-Order Computation Tree Logic cosplay  
4. Receipts — witnesses exclude large language model / Retrieval-Augmented
   Generation text  

Details: `08-verification/VERIFY_STACK.md`.

## Stack owners (fail closed)

| Concern | Owner | Reject |
| --- | --- | --- |
| Engine + Spec corpus Model Context Protocol | Rust | Python host/ACI |
| IDE presentation Model Context Protocol | TypeScript | Spec corpus server as TS default |
| LockCheck WebAssembly guest | Could / Wave-3 | Spec host; Wave-1 Must |

## Next

Read `STATUS.md` for FREEZE deepen-3. Skill `cold-start` for the full chain.
Do not invent repo paths outside frontmatter graphs / INDEX / tool results.
