---
category: Operator/agent surface (CLI grade + MCP + structured retrieval)
status: DRAFT — SPEC GATE E-OAS0 pending Approve of OAS1–OAS14
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
related:
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
  - docs/research/ci/11-ci-output-ux-progressive-disclosure-2026.md
  - docs/research/process/25-tip-grounding-mcp-2026.md
  - docs/process/local-grading-pack.md
  - src/doc_engine/query/mcp_tools.py
  - adapters/mcp/server.py
do_not:
  - Implement before E-OAS0 Approve
  - rich / OTel / embedding as CI or citation SoT
  - MCP write/codegen tools
  - rewrite all scripts/ci to Typer in one tip
spec_gate: DRAFT E-OAS0 (2026-08-10) — OAS1–OAS14 pending Approve
---

# Design memo: E-OAS0 Spec gate

> **DRAFT — awaiting Approve of OAS1–OAS14.**
>
> Research: [`docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md`](../research/process/37-operator-agent-surface-cli-mcp-rag-2026.md).

| Field | Value |
| --- | --- |
| Problem | Grade/MCP surfaces lack shared context, structured receipts, and actionable remediation; modern MCP/RAG bar demands dual human/agent observability without new SoT theater |
| Fix | Shared `RunContext` ports + dual sinks + OCP step modules; thin grade CLI; MCP stderr discipline; Embody Stage-0 packets as retrieval |
| Reuse | `dispatch_tool`, plant_profile exit taxonomy, pre_pr receipt schema ideas, E-UX0 summary-first |
| Downstream | E-OAS1 Implement grade; E-OAS2 MCP parity; E-GND0 remains separate DRAFT |

## Decisions (pending Approve)

| ID | Decision |
| --- | --- |
| **OAS1** | Shared `RunContext` ports across grade CLI and MCP |
| **OAS2** | Dual sink: headline + schema_versioned JSONL receipt |
| **OAS3** | MCP stdio diagnostics on stderr only |
| **OAS4** | Doctor fail-closed on venv / pin path before toolchain steps |
| **OAS5** | Actionable `next_actions[]` for known Windows/operator failures |
| **OAS6** | OCP step strategies; scalable modules ≤225 LOC |
| **OAS7** | Typer only for optional local `doc-engine grade` — not all CI |
| **OAS8** | Refuse rich as CI SoT; optional TTY + `NO_COLOR` only |
| **OAS9** | Defer structlog hard pin; stdlib + JSONL unless Spike |
| **OAS10** | Refuse OTel as tip SoT; future exporter port needs Spec |
| **OAS11** | Embody Stage-0 + context_packet retrieval; Refuse embedding citation SoT |
| **OAS12** | Refuse MCP write/codegen; tip-grounding stays on E-GND0 |
| **OAS13** | One tip stream — grade surface before GND Implement thrash |
| **OAS14** | Synthesis memo in process/; no third nesting level |

## Operator unblock (no Spec — do now)

```text
source .venv/Scripts/activate
./scripts/ci/run_local_grading_pack.sh doctor   # must show .venv prefix
# set artifactory_user + artifactory_password for P3
./scripts/ci/run_local_grading_pack.sh p2       # offline floors OK at exit 3 plant
./scripts/ci/run_local_grading_pack.sh p3       # only after Artifactory + venv
```

## Exit

Human Approve of OAS1–OAS14 flips this file to APPROVED and unblocks E-OAS1.
