---
id: Quality Attribute Scenario QAS-N-05
title: Local-first privacy — no egress on Must path
status: DRAFT
nfr_traces: [REQ-N-05]
---

# Quality Attribute Scenario QAS-N-05 — Local-first privacy

| Part | Value |
| --- | --- |
| **Stimulus** | Full Must verify path invoked |
| **Source** | Default config / A-CI |
| **Environment** | Network egress denied (deny-net harness) |
| **Artifact** | Engine + registry + LockCheck + claim memory |
| **Response** | Completes offline; no outbound sockets |
| **Response measure** | Deny-net harness: 0 egress attempts; process exit 0 on fixture plant |
