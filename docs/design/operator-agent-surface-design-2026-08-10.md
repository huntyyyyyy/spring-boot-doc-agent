---
category: Operator/agent surface (CLI grade + MCP + structured retrieval)
status: DRAFT — SPEC GATE E-OAS0 pending Approve of OAS1–OAS16
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
  - unattended AI merge / full AI adoption
  - phone/device-farm or “universal OS emulator” as CLI SoT
spec_gate: DRAFT E-OAS0 (2026-08-10) — OAS1–OAS16 pending Approve
---

# Design memo: E-OAS0 Spec gate

> **DRAFT — awaiting Approve of OAS1–OAS16.**
>
> Research: [`docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md`](../research/process/37-operator-agent-surface-cli-mcp-rag-2026.md).

| Field | Value |
| --- | --- |
| Problem | Grade/MCP surfaces lack shared context, structured receipts, and actionable remediation; modern MCP/RAG bar demands dual human/agent observability without new SoT theater or unattended AI |
| Fix | Shared `RunContext` ports + dual sinks + OCP step modules; thin grade CLI; MCP stderr discipline; Embody Stage-0 packets; human review floor; campaign OS×shell matrix |
| Reuse | `dispatch_tool`, plant_profile exit taxonomy, pre_pr receipt schema ideas, E-UX0 summary-first |
| Downstream | E-OAS1 Implement grade; E-OAS2 MCP parity; E-OAS4 shell matrix; E-GND0 remains separate DRAFT |

## Decisions (pending Approve)

| ID | Decision |
| --- | --- |
| **OAS1–OAS14** | As in research memo (RunContext, dual sinks, doctor, Typer-grade-only, Refuse rich/OTel/embedding SoTs, …) |
| **OAS15** | Human review is the floor — Spec Approve, operator `--write`, certification, merge SoR; MCP/agents assist only; Refuse unattended AI adoption |
| **OAS16** | Campaign OS×shell matrix (ubuntu/bash, windows/bash, windows/pwsh, optional cmd); Refuse phone farms / universal emulator as CLI SoT |

## Operator unblock (no Spec — do now)

```text
source .venv/Scripts/activate
./scripts/ci/run_local_grading_pack.sh doctor   # must show .venv prefix
# set artifactory_user + artifactory_password for P3
./scripts/ci/run_local_grading_pack.sh p2       # offline floors OK at exit 3 plant
./scripts/ci/run_local_grading_pack.sh p3       # only after Artifactory + venv
```

## Exit

Human Approve of OAS1–OAS16 flips this file to APPROVED and unblocks E-OAS1.
