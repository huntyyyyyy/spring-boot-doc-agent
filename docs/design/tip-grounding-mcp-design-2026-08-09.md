---
category: Tip-grounding MCP (CGQ probes via isolated read-only tools)
status: DRAFT — SPEC GATE E-GND0 pending Approve of GND1–GND10
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
related:
  - docs/research/process/25-tip-grounding-mcp-2026.md
  - docs/research/process/24-codegen-quality-dimensions-mechanism-depth-2026.md
  - docs/design/codegen-quality-dimensions-design-2026-08-09.md
  - src/doc_engine/query/mcp_tools.py
  - adapters/mcp/server.py
  - docs/research/quality-backlog.md
do_not:
  - Implement before E-CGQ0 + E-GND0 Approve
  - add codegen / write / apply_patch tools
spec_gate: DRAFT E-GND0 (2026-08-09) — GND1–GND10 pending Approve
depends_on: E-CGQ0 Approve before E-GND1 Implement
---

# Design memo: E-GND0 Spec gate

> **DRAFT — awaiting Approve of GND1–GND10.**
>
> Research: [`docs/research/process/25-tip-grounding-mcp-2026.md`](../research/process/25-tip-grounding-mcp-2026.md).
> Depends on: [`codegen-quality-dimensions-design-2026-08-09.md`](codegen-quality-dimensions-design-2026-08-09.md) (E-CGQ0).

| Field | Value |
| --- | --- |
| Problem | Stage-0 query MCP ≠ tip grounding; CGQ4/CGQ5 need enforced probes |
| Fix | Extend isolated MCP with read-only tip tools; fail-closed receipts; refuse codegen host |
| Reuse | ADR S-STF-E; `dispatch_tool`; thin `adapters/mcp` |
| Downstream | E-GND1 Implement after CGQ0 + GND0 Approve |

## Decisions (pending Approve)

| ID | Decision |
| --- | --- |
| **GND1** | Tip-grounding MCP Adopt for CGQ probes — not codegen host |
| **GND2** | Reuse isolation; no caller `root`; read-only |
| **GND3** | Refuse generate/apply/write tools |
| **GND4** | Min tools: probe, depth_row, accept_checklist, list_witnesses, research_map |
| **GND5** | Library dispatch SoR; thin adapter |
| **GND6** | Fail-closed receipt for design-shaped Impl |
| **GND7** | Implement blocked until CGQ0 + GND0 Approved |
| **GND8** | Stage-0 tools stay; tip tools additive |
| **GND9** | MCP SDK pin Deferred; keep thin stdio |
| **GND10** | ≥10k★ / no new runtime SoT floors |

## Exit

On Approve: stamp `APPROVED E-GND0`; backlog P22; schedule E-GND1 only after E-CGQ0 Approved.
