---
title: Inbound AI draft — verified-slice RE-MASTER-001 v0.5.1 (NOT SoR)
status: DRAFT-AI — parked for critique; see process/52 — do not Approve as-is
date: '2026-08-10'
epic: E-LIE0
claim_tiers: Unknown
related:
  - docs/research/process/52-verified-slice-re-master-adversarial-critique-2026-08-10.md
  - docs/design/e-lie0-requirements-2026-08-10.md
do_not:
  - Cite this file as requirements SoR
  - Implement from this draft without Rewrite + Approve
  - Pin Phi-3 or any model identity into Must FRs
note: >-
  Pasted 2026-08-10 from user; truncated mid FR-16. Model choice noted as
  will-change. Critique: process/52.
last_reviewed: '2026-08-10'
---

# Verified Slice / Architecture Intelligence Layer — RE-MASTER-001 (inbound)

> **NOT the requirements system of record.** Working SoR:
> [`docs/design/e-lie0-requirements-2026-08-10.md`](../../design/e-lie0-requirements-2026-08-10.md).  
> Adversarial critique:
> [`process/52-…`](../process/52-verified-slice-re-master-adversarial-critique-2026-08-10.md).

<!--
Original header metadata from AI draft (preserved for audit):
VERSION: 0.5.1 · CREATED: 2026-08-10 · STATUS: DRAFT — pending stakeholder review
Standards named: ISO/IEC/IEEE 29148:2018 · ISO/IEC 25010:2023 · MCP 2026-07-28 · INCOSE SE Handbook 5.0
Corpora named (vapor relative to this repo): VS-corpus-v1 · VS-bench-v1 · VS-eval-v1 · VS-load-v1
NOTE: Author of paste stated model choice will change — Phi-3 pins below are obsolete as REQ text.
PASTE truncated mid FR-16 Knowledge Graph Traversal.
-->

## PART 1 — StRS (inbound)

### Stakeholder identification (inbound)

| ID | Name | Core Concern |
|----|------|--------------|
| SH-01 | Individual Developer | Know lock violations before push; self-correct in IDE |
| SH-02 | Platform / Architecture Team | Enforce contracts without being on critical path of checks |
| SH-03 | Engineering Manager | impact_analysis without meetings |
| SH-04 | Security / Compliance Officer | Immutable proof artefact per commit SHA |

### OpsCon (inbound summary)

**LOCAL:** save Java → LSP `fitness_check` over stdio MCP → tree-sitter → SCIP → Wasmtime `.mdc` eval → RAG + Phi-3 → LSP diagnostics. Budget claim ≤2000 ms p95 warm.

**ORG-WIDE:** Streamable HTTP MCP, claimed stateless; Kuzu + LanceDB; LLM as UI only.

### Business requirements (inbound IDs)

- **BR-01** Pre-commit violation detection  
- **BR-02** Self-service architecture querying  
- **BR-03** Auditable proof of constraint evaluation  
- **BR-04** Horizontally scalable org-wide deployment  

## PART 2 — SRS (inbound FR index)

| ID | Title | Critique pointer (process/52) |
|----|-------|-------------------------------|
| FR-01 | MDC lock file parsing | Keep intent; DSL/ADR-DSL-001 vapor |
| FR-02 | Java AST parsing (tree-sitter, error-node-free) | **Reject** error-node-free Accept |
| FR-03 | Violation detection FN=0 / FP≤2.30% | **Reject** FN=0; vapor corpus |
| FR-04 | LanceDB + Phi-3 symbol indexing | **Reject** as symbol SoR; model pin obsolete |
| FR-05 | SCIP cross-file resolution | Keep intent; “Risk: None” **false** |
| FR-06 | Context-pruned RAG | Suggest path only — not Must verify |
| FR-07 | Ollama Phi-3 inference | **Remove model pin**; Could remediation |
| FR-08 | WASM sandbox | Keep policy intent; rewrite capability Claim |
| FR-09 | Proof tour JSON (5 fields) | Keep intent; fix SHA/ADR/pass semantics |
| FR-10 | LSP diagnostics | Should — aligns e-lie0 |
| FR-11 | IDE verification panel | Could/Should |
| FR-12 | MCP fitness_check stdio | Adopt shape when MCP ships |
| FR-13 | MCP Streamable HTTP + OAuth | Phase-2; headers Evidenced |
| FR-14 | traversal_id + Kuzu/Redis | **Kuzu LB claim fails** research |
| FR-15 | Async tasks/get | Extension mis-specified vs SEP-2663 |
| FR-16 | Knowledge graph traversal | **Truncated in inbound paste** |

## Explicit author note (session)

Specific **model choice will change** — do not treat `phi3:3.8b-mini-instruct-4k-q4_K_M` (or any successor) as a functional requirement. Bind latency/RSS/privacy NFRs to a **provider slot**.
