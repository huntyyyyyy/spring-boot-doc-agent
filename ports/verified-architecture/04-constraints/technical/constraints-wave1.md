---
title: Constraints ledger (wave-1)
status: DRAFT
date: '2026-08-10'
---

# Constraints

Distinct from REQs: a CON change requires an Architecture Decision Record before
Implement may proceed. Violating a CON without that record → reject the change.

| ID | Constraint | Bound / fail-mode |
| --- | --- | --- |
| CON-01 | Exactly one deterministic merge-gate / oracle writer at a time | Second writer → fail Architecture Decision Record ADR-0006 |
| CON-02 | Polyglot stays under `options/`; **Refuse Python** runtime for this port | Python host / ACI nest revival → reject (Architecture Decision Record ADR-0001 amended) |
| CON-03 | Local-first default; locks in git; indexes/claims local-derived | Cloud-required Must path → fail Quality Attribute Scenario QAS-N-05 |
| CON-04 | Java 17/21 · Boot 3.2/3.3 plant envelope until reopened | Outside envelope without open-question reopen → Unknown, not “proved” |
| CON-05 | No large language model / Retrieval-Augmented Generation output as verify witness or claim anchor | Witness field containing model text → receipt invalid |
| CON-06 | No product code until Definition of Ready green + signoff | Crates/daemons before D12 → reject |
| CON-07 | Must non-functional requirements influencing Design must be complete Quality Attribute Scenarios (latency Spikes OK) | Incomplete measure still sizing Design → demote or block |
| CON-08 | C4 structural claims cite Architecture Decision Record IDs | Untied C4 claim → reject merge of that doc |
| CON-09 | WebAssembly / Rust = trust-boundary engineering until formal artifacts exist | WebAssembly as Specification corpus host → reject |
| CON-10 | Prefer Unknown/unprovable over wrong | Silent winner under multi-candidate → fail REQ-F-02 |
| CON-11 | Evidence ⊥ freshness for claims (Artifact-Anchored Verification Memory) | Stale digest treated as fresh → fail Proof-or-Stop |
| CON-12 | Model Context Protocol / command-line interface entity ids typed from stores (Stateful Tool-Enabled Agentic Deployment); harness code-owned | Unknown id accepted → fail Quality Attribute Scenario QAS-N-08 |
| CON-13 | Proof-or-Stop: done requires freshness-bound receipt, not agent assertion | “Done” without receipt → reject |
| CON-14 | ClaimMemory ≠ AgentMemory | Cue / chat memory used as claim anchor → reject |
| CON-15 | Science: locked transfers only | Free-form “science” folder edits without transfer record → reject |

Engine + Specification corpus Model Context Protocol host: **Rust**. FREEZE still limits new Must entities.
