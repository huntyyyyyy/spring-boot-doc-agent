---
title: June–August 2026 research → port-readiness findings
status: RESEARCH COMPLETE
date: '2026-08-10'
window: 2026-06-01 .. 2026-08-10
claim_tiers: Evidenced / Confirmed / Unknown
---

# June–August 2026 findings (before port readiness work)

Published timestamps verified via arXiv Atom API (2026-08-10).

## Papers that change how we get “ready”

| ID | Paper | Pub | Finding we Embody/Adopt | Port-ready action |
| --- | --- | --- | --- | --- |
| J1 | [Proof-or-Stop 2607.14890](https://arxiv.org/abs/2607.14890) | Jul 16 | “Done” needs **freshness-bound authenticated receipts**, not agent assertion; evidence-gated lifecycle | Receipt schema: bind digests + reject stale; V&V Accept = receipt re-derives |
| J2 | [Prompts→Contracts 2607.08028](https://arxiv.org/abs/2607.08028) | Jul 9 | **Code-owned harness checks** beat prompts; contracts auditable under model swap | Harness ICD; STEAD ST-* as code-owned; Aria-shaped propose/decide |
| J3 | [Cue-anchored WM 2607.20972](https://arxiv.org/abs/2607.20972) | Jul 23 | Working memory = **delivery** by harness, not hoping agent stores | Keep ClaimMemory ≠ AgentMemory; cue injection Could later |
| J4 | [EA-Graph 2608.04278](https://arxiv.org/abs/2608.04278) | Aug 4 | Anchors; evidence⊥freshness; **unprovable** | Already Must — finish ICD + Accept fixture text |
| J5 | [STEAD 2608.03609](https://arxiv.org/abs/2608.03609) | Aug 4 | Agent+tools FO-CTL undecidable; equivariance | ST-1…5 in MCP ICD; Spike charter |
| J6 | [Aria 2607.06341](https://arxiv.org/abs/2607.06341) | Jul 7 | Agent + harness; kernel decides | VERIFY_STACK harness loop |
| J7 | [MAAD 2606.01385](https://arxiv.org/abs/2606.01385) | May 31* | Agents draft RE/arch; Evaluator/ATAM; humans remain | Promote StRS/SRS/QAS; human signoff required |
| J8 | [HyperTool 2606.13663](https://arxiv.org/abs/2606.13663) | Jun 11 | MCP composition blocks; primitives keep schemas | MCP ICD lists **primitive** tools first; HyperTool = Could |
| J9 | [DynamicMCPBench 2607.20531](https://arxiv.org/abs/2607.20531) | Jul 10 | Effect-scored MCP tasks; typed checkpoints | V&V: effect checkpoints for verify tools |

\*Late-May; included as June-adjacent RE/ATAM evidence.

## Explicit refuses reinforced

| Temptation | Paper pressure | Verdict |
| --- | --- | --- |
| Prompt-only “be careful with ids” | J2 | Refuse — code-owned checks |
| Agent says verify done | J1 | Refuse — receipt gate |
| Collapse claim store into chat memory | J3 | Refuse |
| Free-text MCP entity args | J5 | Refuse |
| Latency adjectives without six-part QAS | J7 / ATAM | Refuse Design influence |

## Port vs Implement

These findings make the **planning corpus** ready to export with a coherent Must spine and Accept methods. They do **not** by themselves green DoR human Accept or authorize Cargo.
