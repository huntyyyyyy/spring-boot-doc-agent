---
title: C4 brief — Context + Container with confidence scores
status: DRAFT — not human Accepted
date: '2026-08-10'
confidence_scale: >-
  0.0–1.0 = how confident we are this entity/relationship is correct for the
  product as specified (not implementation readiness). Tier hint:
  ≥0.75 Evidenced+Confirmed shape; 0.4–0.74 Draft; <0.4 Unknown/Pilot.
---

# C4 brief (so far) + confidence

Not Accepted. ASCII only — replace with formal diagrams under this folder after
signoff. Scores reflect **conceptual confidence**, not “ready to code.”

## Context (Level 1)

```text
                    ┌──────────────────┐
                    │  Developer /     │
                    │  Coding agent    │
                    └────────┬─────────┘
                             │ edits + tool calls
                             ▼
┌──────────────┐    ┌────────────────────┐    ┌─────────────────┐
│ Target git   │───▶│ Verified           │◀───│ Optional remote │
│ repository   │    │ Architecture       │    │ MCP host / IDE  │
│ (sources +   │    │ Engine (local)     │    │ (Streamable HTTP│
│  locks +     │    │                    │    │  2026-07-28)    │
│  index.scip) │    └────────────────────┘    └─────────────────┘
└──────────────┘
```

| Entity | Role | Confidence |
| --- | --- | --- |
| Developer / coding agent | Proposes changes; never sole verifier | **0.85** |
| Target git repository | Policy locks + sources System of Record inputs | **0.80** |
| Verified Architecture Engine | Local command-line interface (+ optional Model Context Protocol server) | **0.75** |
| Optional remote Model Context Protocol host / IDE | May call engine tools over Streamable HTTP | **0.55** (need exists; transport reqs newly identified) |
| Org SaaS / Backstage mesh | Out of scope minimum viable product | **0.90** (Refuse is firm) |

| Relationship | Meaning | Confidence |
| --- | --- | --- |
| Agent → Engine via Model Context Protocol/command-line interface | Propose only; harness decides | **0.70** |
| Engine → Target repo read | Index + locks + sources | **0.80** |
| Engine → Target repo write locks | Policy System of Record — human Approve | **0.65** (process clear; Interface Control Document thin) |
| Host → Engine Streamable HTTP `2026-07-28` | Stateless; headers; handles as args | **0.40** (spec Evidenced; our Interface Control Document stale) |
| Retrieval-Augmented Generation/large language model → Engine witnesses | Forbidden | **0.85** |

## Container (Level 2)

```text
┌──────────────── Verified Architecture Engine (process) ────────────────┐
│                                                                          │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────┐   ┌────────────┐ │
│  │ CLI / MCP   │──▶│ Harness      │──▶│ LockCheck + │──▶│ Receipt +  │ │
│  │ server      │   │ (decide)     │   │ ClaimMemory │   │ Claim store│ │
│  │ 2026-07-28  │   │              │   │             │   │ (SQLite)   │ │
│  └─────────────┘   └──────────────┘   └──────┬──────┘   └────────────┘ │
│         │                                     │                          │
│         │            ┌────────────────────────┘                          │
│         ▼            ▼                                                   │
│  ┌─────────────┐  ┌──────────────┐                                       │
│  │ IndexReader │  │ Registry     │◀── index.scip + sources               │
│  │ (SCIP)      │  │ (graph)      │                                       │
│  └─────────────┘  └──────────────┘                                       │
│                                                                          │
│  ┌─────────────┐                                                         │
│  │ Remediation │  Could — suggestions only; never witness                │
│  │ Assist/RAG  │                                                         │
│  └─────────────┘                                                         │
└──────────────────────────────────────────────────────────────────────────┘
         ▲ locks/*.yml or lock IR files in target git (policy SoR)
```

| Container | Confidence |
| --- | --- |
| command-line interface entrypoint | **0.80** |
| Model Context Protocol server (`2026-07-28` Streamable HTTP or stdio) | **0.35** |
| Harness decide loop | **0.55** |
| IndexReader (Source Code Index Protocol) | **0.70** |
| Registry / graph | **0.65** |
| LockCheck + lock Intermediate Representation | **0.40** (no schema yet) |
| ClaimMemory | **0.30** (Pilot) |
| ReceiptWriter | **0.45** |
| SQLite claim/registry store | **0.60** (plausible; unproven) |
| Remediation Assist / Retrieval-Augmented Generation | **0.75** as Could/non-witness |

| Relationship | Confidence |
| --- | --- |
| Model Context Protocol/command-line interface → Harness | **0.60** |
| Harness → LockCheck | **0.70** |
| LockCheck → Registry | **0.65** |
| LockCheck → ClaimMemory put/withdraw | **0.35** |
| Steps → ReceiptWriter | **0.50** |
| IndexReader → Registry | **0.70** |
| Git locks → LockCheck | **0.55** |
| Retrieval-Augmented Generation → Receipt witnesses | **0.90** (must be absent) |

## Aggregate confidence (honest)

| View | Score | Meaning |
| --- | --- | --- |
| Product shape (local command-line interface, not SaaS) | **0.85** | Stable decision |
| Verify Must spine *intent* | **0.70** | Right threats; weak field Adopt on claims/Stateful Tool-Enabled Agentic Deployment |
| Ready to Implement | **0.15** | Definition of Ready 0 PASS; Model Context Protocol Interface Control Document stale vs `2026-07-28` |
| Research method floor | **0.65** | Digests + API routing exist; few digests filled |

## Next diagram work

1. Formal Context + Container in Structurizr or Mermaid Accepted set.  
2. Tag every trust boundary (policy System of Record vs derived registry vs agent).  
3. Re-score after Model Context Protocol Interface Control Document rewrite and lock Intermediate Representation schema land.
