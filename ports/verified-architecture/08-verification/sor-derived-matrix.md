---
title: SoR vs derived matrix
status: DRAFT
date: '2026-08-10'
traces: OQ-02
---

# SoR vs derived

| Artifact | Class | Writer | Readers | Notes |
| --- | --- | --- | --- | --- |
| Target sources | SoR (external) | Developers | Indexers, engine | Not ours to mutate as product |
| Lock / MDC / pack manifests | **Policy SoR** | Architects (git) | LockCheck, LSP, CI | Team sync = git |
| `index.scip` | **Index SoR** (derived from sources via scip-java) | Indexer job | Resolve | Rebuildable; don’t sync as team SoR |
| SQLite registry / graph | **Derived** | Engine | LockCheck, queries | Wipe/rebuild OK |
| Proof-tour receipt | **Verify artifact** | Engine | IDE, audit, CI | Immutable per run |
| EA-Graph claims + anchors | **Derived claim store** | Engine | Withdrawal / audit | Digests; not team git SoR |
| RAG embeddings / Lance chunks | **Retrieve-only** | Corpus ingest | Agent assist | **Never** verify witness / anchor |
| LLM remediation text | **Advisory** | Model | Human | Excluded from witnesses |
| MCP/CLI tool args (entity ids) | **Interface** | Harness | Agent | STEAD: typed ids only |
| Coverage / merge oracle | **Gate SoR** (one writer) | Named process | CI | Language-neutral; single writer |

## Rules

1. Promoting derived → SoR requires an ADR.
2. Sensors (RAG, LLM, climb metrics) must not silently become gates.
3. Ambiguous resolve writes Unknown — never invents a SoR edge.
