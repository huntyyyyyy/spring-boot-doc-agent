---
title: STATUS — single pointer for cold agents
status: ACTIVE
last_reviewed: '2026-08-10'
---

# STATUS

## Phase

**Specification / gap-fill** — product implementation = Refuse.  
**Port ready:** YES — see `PORT_READY.md` (export the specification corpus).  
**Implement ready:** NO.

Use whole words in all edits — see `GLOSSARY.md`.

## Research basis (June–August 2026)

`research/papers-2026-may-aug/june-august-2026-port-readiness.md`

Papers that shaped readiness (full titles):

- Proof-or-Stop: Don't Trust the Agent, Trust the Evidence
- From Prompts to Contracts: Harness Engineering for Auditable Enterprise LLM Agents
- Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property
- EA-Graph: Artifact-Anchored Verification Memory for Coding Agents under Upstream Drift
- Formal Verification of Agentic Systems over Operational Data (Stateful Tool-Enabled Agentic Deployments)
- Harnessing Code Agents for Automatic Software Verification (Aria)
- Bridging Requirements and Architecture (multi-agent orchestration)
- HyperTool; DynamicMCPBench

## Must spine

Graph + locks **and** artifact-anchored claim memory **and** Stateful
Tool-Enabled Agentic Deployment tool constraints **and** freshness-bound
receipts — see `08-verification/VERIFY_STACK.md`.

## Next tasks after port

1. Human sign `BOUNDARY.md` + `VERIFY_STACK.md` + wave-1 Stakeholder and Software Requirements Specifications in `SIGNOFF_LOG.md`
2. Spike for Quality Attribute Scenario N-01/N-02 latency measures (or demote latency from Must)
3. Build fixture plants named in `vv-plan/`
4. Only then consider Implement Approve

## Do not do next

- Treat Port ready as Implement ready
- Shrink Must spine
- Cargo scaffolds
