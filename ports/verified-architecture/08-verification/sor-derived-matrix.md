---
title: System of Record vs derived matrix
status: DRAFT
date: '2026-08-10'
traces: open question OQ-02
---

# System of Record vs derived

| Artifact | Class | Writer | Fail-mode |
| --- | --- | --- | --- |
| Target sources | SoR (external) | Developers | Product mutates target as SoR → reject |
| Lock / MDC / pack manifests | **Policy SoR** | Architects (git) | Team sync outside git → reject |
| `index.scip` | **Index SoR** (derived via scip-java) | Indexer job | Sync index as team SoR → reject |
| SQLite registry / graph | **Derived** | Rust engine | Multi-writer / Python owner → reject |
| Proof-tour receipt | **Verify artifact** | Rust engine | LLM text inside `witness` → invalid |
| EA-Graph claims + anchors | **Derived claim store** | Rust engine | Git-sync claim DB as team SoR → reject |
| RAG embeddings / Lance chunks | **Retrieve-only** | Corpus ingest | Used as verify witness/anchor → reject |
| LLM remediation text | **Advisory** | Model | Inside witnesses → reject |
| MCP/CLI tool args (entity ids) | **Interface** | Harness | Free-text / non-equivariant ids → reject |
| Coverage / merge oracle | **Gate SoR** (one writer) | Named process | Multi-writer / language-identity oracle → reject |

## Rules

1. Derived → SoR promotion needs an Architecture Decision Record.
2. Sensors (RAG, LLM, climb) must not silently become gates.
3. Ambiguous resolve → Unknown — never invent a SoR edge.
