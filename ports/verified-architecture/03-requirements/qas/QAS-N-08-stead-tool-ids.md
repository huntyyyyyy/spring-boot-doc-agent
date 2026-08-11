---
id: Quality Attribute Scenario QAS-N-08
title: Harness rejects hallucinated tool entity ids
status: DRAFT
nfr_traces: [REQ-F-09b]
evidence: arXiv:2608.03609
---

# Quality Attribute Scenario QAS-N-08 — Harness rejects hallucinated tool entity ids

| Part | Value |
| --- | --- |
| **Stimulus** | Agent issues Model Context Protocol or command-line interface call whose entity id is absent from the current registry snapshot |
| **Source** | Large language model tool call (untrusted proposer) |
| **Environment** | Harness enforcing Stateful Tool-Enabled Agentic Deployment ST-1…5; Rust-owned accept/reject |
| **Artifact** | Model Context Protocol / command-line interface gateway + Registry |
| **Response** | Reject call before mutation; registry and claim store unchanged |
| **Response measure** | 100% unknown-id calls rejected in harness suite; 0 silent accepts; 0 side-effect rows |
