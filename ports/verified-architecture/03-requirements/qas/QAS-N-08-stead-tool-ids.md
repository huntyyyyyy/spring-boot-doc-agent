---
id: Quality Attribute Scenario QAS-N-08
title: Harness rejects hallucinated tool entity ids
status: DRAFT
nfr_traces: [REQ-F-09b]
evidence: arXiv:2608.03609
---

# Quality Attribute Scenario QAS-N-08 — Stateful Tool-Enabled Agentic Deployment-typed tool ids

| Part | Value |
| --- | --- |
| **Stimulus** | Agent issues Model Context Protocol/command-line interface call with entity id not present in current snapshot |
| **Source** | large language model tool call |
| **Environment** | Harness enforcing ST-1…5 |
| **Artifact** | Model Context Protocol/command-line interface gateway + Registry |
| **Response** | Reject call; no side effects on registry/claims |
| **Response measure** | 100% unknown-id calls rejected in harness suite; 0 silent accepts |
