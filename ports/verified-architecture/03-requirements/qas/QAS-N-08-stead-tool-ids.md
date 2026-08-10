---
id: QAS-N-08
title: Harness rejects hallucinated tool entity ids
status: DRAFT
nfr_traces: [REQ-F-09b]
evidence: arXiv:2608.03609
---

# QAS-N-08 — STEAD-typed tool ids

| Part | Value |
| --- | --- |
| **Stimulus** | Agent issues MCP/CLI call with entity id not present in current snapshot |
| **Source** | LLM tool call |
| **Environment** | Harness enforcing ST-1…5 |
| **Artifact** | MCP/CLI gateway + Registry |
| **Response** | Reject call; no side effects on registry/claims |
| **Response measure** | 100% unknown-id calls rejected in harness suite; 0 silent accepts |
