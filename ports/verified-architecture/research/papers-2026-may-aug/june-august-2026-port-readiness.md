---
title: June–August 2026 research → port-readiness findings
status: SUPERSEDED ON DEPTH — see entity-adoption-audit + shallow-decisions-honesty
date: '2026-08-10'
window: 2026-06-01 .. 2026-08-10
claim_tiers: Evidenced / Confirmed / Unknown
---

# June–August 2026 findings (before port readiness work)

**Historical / evidence — not product SoT.** Superseded on research depth by
`research/gaps/entity-adoption-audit-2026-08-10.md` and
`research/gaps/shallow-decisions-honesty-2026-08-10.md`. Keep as title→action
table only — do **not** treat as D0 PASS or Implement green.

## Papers that change how we get “ready”

| ID | Paper (full title) | Published | Finding we Embody/Adopt | Port-ready action |
| --- | --- | --- | --- | --- |
| J1 | [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence](https://arxiv.org/abs/2607.14890) | Jul 16 | “Done” needs **freshness-bound authenticated receipts**, not agent assertion; evidence-gated lifecycle | Receipt schema: bind digests + reject stale; Verification and Validation Accept = receipt re-derives |
| J2 | [From Prompts to Contracts: Harness Engineering for Auditable Enterprise large language model Agents](https://arxiv.org/abs/2607.08028) | Jul 9 | **Code-owned harness checks** beat prompts; contracts auditable under model swap | Harness Interface Control Document; Stateful Tool-Enabled Agentic Deployment ST-* as code-owned; Aria-shaped propose/decide |
| J3 | [Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents](https://arxiv.org/abs/2607.20972) | Jul 23 | Working memory = **delivery** by harness, not hoping agent stores | Keep ClaimMemory ≠ AgentMemory; cue injection Could later |
| J4 | [EA-Graph: Artifact-Anchored Verification Memory for Coding Agents under Upstream Drift](https://arxiv.org/abs/2608.04278) | Aug 4 | Anchors; evidence independent of freshness; **unprovable** | Already Must — finish Interface Control Document + Accept fixture text |
| J5 | [Formal Verification of Agentic Systems over Operational Data](https://arxiv.org/abs/2608.03609) (Stateful Tool-Enabled Agentic Deployments) | Aug 4 | Agent + tools First-Order Computation Tree Logic undecidable; equivariance | ST-1…5 in Model Context Protocol Interface Control Document; Spike charter |
| J6 | [Harnessing Code Agents for Automatic Software Verification](https://arxiv.org/abs/2607.06341) (Aria) | Jul 7 | Agent + harness; kernel decides | VERIFY_STACK harness loop |
| J7 | [Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory](https://arxiv.org/abs/2606.01385) | May 31* | Agents draft requirements engineering / architecture; Evaluator / Architecture Tradeoff Analysis Method; humans remain | Promote Stakeholder and Software Requirements Specifications + Quality Attribute Scenarios; human signoff required |
| J8 | [HyperTool: Beyond Step-Wise Tool Calls for Tool-Augmented Agents](https://arxiv.org/abs/2606.13663) | Jun 11 | Model Context Protocol composition blocks; primitives keep schemas | Model Context Protocol Interface Control Document lists **primitive** tools first; HyperTool = Could |
| J9 | [DynamicMCPBench: A Trace-Grounded, Effect-Scored Benchmark for large language model Agents over Live Model Context Protocol Servers](https://arxiv.org/abs/2607.20531) | Jul 10 | Effect-scored Model Context Protocol tasks; typed checkpoints | Verification and Validation: effect checkpoints for verify tools |

\*Late-May; included as June-adjacent requirements engineering / Architecture Tradeoff Analysis Method evidence.

## Explicit refuses reinforced

| Temptation | Paper pressure | Verdict |
| --- | --- | --- |
| Prompt-only “be careful with identifiers” | J2 | Refuse — code-owned checks |
| Agent says verify done | J1 | Refuse — receipt gate |
| Collapse claim store into chat memory | J3 | Refuse |
| Free-text Model Context Protocol entity arguments | J5 | Refuse |
| Latency adjectives without six-part Quality Attribute Scenario | J7 / Architecture Tradeoff Analysis Method | Refuse Design influence |

## Port versus Implement

**Historical title→action only.** These findings name papers that *pressured*
Must-intent rows; they do **not** make the planning corpus export-green, do
**not** entail Definition of Ready PASS, and do **not** authorize Cargo.
Treat this file as a superseded sensor — Authority: entity-adoption-audit +
shallow-decisions-honesty + STATUS.
