---
title: Critique — inbound RE-MASTER-001 AI draft (v0.5.1)
status: RESEARCH COMPLETE
date: '2026-08-10'
---

# Critique — RE-MASTER-001 (severe)

Inbound AI draft is **not** Spec. Extract concerns; rewrite Must spine.

## Keep (concern-level)

- Pre-commit / IDE-visible architectural violation signal
- Self-service architecture questions without architect on critical path
- Auditable proof artefact of constraint evaluation
- Stakeholder IDs as starting actors (rename into StRS)

## Reject / demote

| Draft claim | Failure | Disposition |
| --- | --- | --- |
| Phi-3 + Ollama pinned FR | Model choice will change; impl leakage | Could / config — never Must FR |
| LanceDB embeddings as symbol index | Not SCIP; wrong SoR | Refuse as symbol SoT |
| Org-wide Kuzu social graph Must | Scope + local-first conflict | Phase-N Pilot after local wave |
| Bare p95 budgets | Not six-part QAS | Rewrite as QAS or drop |
| VS-corpus / VS-bench IDs | Corpora not in-repo | Unknown until plants exist |
| WASM deny-list = proof | Engineering ≠ formal semantics | trust-boundary label only |
| Priority score formula theater | Fake precision | MoSCoW + stakeholder Approve |

## Required rewrite before Design

Must = virtual dep/DI graph + lock IR + receipts + Unknown taxonomy.  
RAG/LLM = remediation assist, never verify witness.  
Every NFR → ATAM QAS. Constraints separate.
