---
id: Quality Attribute Scenario QAS-N-05
title: Local-first privacy — no egress on Must path
status: DRAFT
nfr_traces: [REQ-N-05]
---

# Quality Attribute Scenario QAS-N-05 — Local-first privacy — no egress on Must path

| Part | Value |
| --- | --- |
| **Stimulus** | LockCheck + resolve + receipt write on the fixture plant under default config |
| **Source** | Actor A-CI or default local config (no cloud profile) |
| **Environment** | Network egress denied via deny-net harness; indexes/claims on local disk only |
| **Artifact** | Rust verify engine + registry + LockCheck + claim memory |
| **Response** | Completes with exit 0; opens **zero** outbound sockets; does not call remote model APIs |
| **Response measure** | Deny-net harness: 0 egress attempts recorded; process exit 0 on fixture plant |
