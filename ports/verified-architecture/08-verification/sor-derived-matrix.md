---
title: System of Record vs derived matrix
status: DRAFT
date: '2026-08-10'
traces: open question OQ-02
---

# System of Record vs derived

| Artifact | Class | Writer | Readers | Notes |
| --- | --- | --- | --- | --- |
| Target sources | System of Record (external) | Developers | Indexers, engine | Not ours to mutate as product |
| Lock / MDC / pack manifests | **Policy System of Record** | Architects (git) | LockCheck, Language Server Protocol, CI | Team sync = git |
| `index.scip` | **Index System of Record** (derived from sources via scip-java) | Indexer job | Resolve | Rebuildable; don’t sync as team System of Record |
| SQLite registry / graph | **Derived** | Engine | LockCheck, queries | Wipe/rebuild OK |
| Proof-tour receipt | **Verify artifact** | Engine | IDE, audit, CI | Immutable per run |
| EA-Graph claims + anchors | **Derived claim store** | Engine | Withdrawal / audit | Digests; not team git System of Record |
| Retrieval-Augmented Generation embeddings / Lance chunks | **Retrieve-only** | Corpus ingest | Agent assist | **Never** verify witness / anchor |
| large language model remediation text | **Advisory** | Model | Human | Excluded from witnesses |
| Model Context Protocol/command-line interface tool args (entity ids) | **Interface** | Harness | Agent | Stateful Tool-Enabled Agentic Deployment: typed ids only |
| Coverage / merge oracle | **Gate System of Record** (one writer) | Named process | CI | Language-neutral; single writer |

## Rules

1. Promoting derived → System of Record requires an Architecture Decision Record.
2. Sensors (Retrieval-Augmented Generation, large language model, climb metrics) must not silently become gates.
3. Ambiguous resolve writes Unknown — never invents a System of Record edge.
