---
title: E-GND0 — Tip-grounding MCP (extend query isolation; refuse remote codegen)
status: DRAFT Spec — pending Approve of GND1–GND10
research date: 2026-08-09
research_window: 2026-06-01 → 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI modular monolith (`doc_engine` + `stf`) + Cursor tip agents
related:
  - docs/research/process/24-codegen-quality-dimensions-mechanism-depth-2026.md
  - docs/design/codegen-quality-dimensions-design-2026-08-09.md
  - docs/research/archive/claude-lore/research/s-stf-e-mcp-isolation-adr-2026-08-08.md
  - docs/research/process/19-watch-stalker-agents-context-lean-2026.md
  - docs/research/process/18-docs-research-taxonomy-claude-consolidation-2026.md
  - src/doc_engine/query/mcp_tools.py
  - adapters/mcp/server.py
  - docs/research/quality-backlog.md
do_not:
  - add generate_code / apply_patch / write_file MCP tools
  - accept caller-supplied root (confused deputy)
  - replace Cursor tip writer with MCP host as default codegen brain
  - Adopt Spec Kit WorkflowEngine runtime
  - Implement tip-grounding tools before E-CGQ0 Approve + this Spec Approve
spec_gate: DRAFT E-GND0 (2026-08-09) — GND1–GND10 pending Approve
depends_on: E-CGQ0 Approve (CGQ1–CGQ10) before E-GND1 Implement
gh_sor_bar: "≥10000★ for new external SoR; Confirmed pins Embody-continue"
---

# Principal memo: tip-grounding MCP (long-term reach)

**Question.** Should we extend the existing Stage-0 query MCP into a
**mandatory grounding/verify port** for tip / design-shaped work — and what must
we Refuse so it does not become a remote codegen brain?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Is Stage-0 query MCP already “tip grounding”? | **No.** It reads pipeline run artifacts (`query_*`, `context_packet`). Tip agents need *this repo’s* structure, depth rows, Accept, witnesses. `[Confirmed]` |
| Is extending that MCP the right long-term vehicle for CGQ4/CGQ5? | **Yes — Adopt.** Same isolation ADR; read-mostly tools; auditable calls; fail-closable with hooks. `[Confirmed]` + `[Evidenced]` context-grounding pattern ([2604.05278](https://arxiv.org/abs/2604.05278)) |
| Should codegen move onto the MCP server? | **Refuse.** Generation stays in Cursor tip; MCP probes + verifies. Watch≠fixer; no alternate tip writer. `[Confirmed]` E-STK0 / E-CGQ0 |
| Implement now? | **No.** Spec first; **depends on E-CGQ0 Approve** so tools encode the right Accept contract. |

```text
TODAY (Embodied)              REACH (Adopt after Spec)
─────────────────             ────────────────────────
adapters/mcp + query/*        + tip_probe_* / tip_depth_* / tip_accept_*
Stage-0 run artifacts         + workspace SoR (src, docs/research, catalog)
server-derived root           same (ADR S-STF-E)
read-only                     read-only (+ Explicit Defer on any write)
no generate_code              still no generate_code
```

---

## 1. What already exists (Confirmed)

| Piece | Path | Role |
| --- | --- | --- |
| Isolation ADR | `docs/research/archive/claude-lore/research/s-stf-e-mcp-isolation-adr-2026-08-08.md` | Server-derived root; no caller `root` |
| Dispatch SoR | `src/doc_engine/query/mcp_tools.py` | `dispatch_tool`; OCP via `QueryKindSpec` |
| Kind registry | `src/doc_engine/query/kinds.py` | evidence/facts/routes/… |
| Thin stdio adapter | `adapters/mcp/server.py` | No SDK pin (E3-S1); swap later |
| Look-first hooks | `.cursor/hooks/*research_map*` | Design-write gate ≠ tip structural probe |

**Gap:** no tool returns import/public-surface for a tip module, depth-row text from `process/24` §2, or CGQ3 Accept checklist completeness.

---

## 2. Evidence for the reach

| Claim | Tier | Source |
| --- | --- | --- |
| Phase-scoped discovery + validation reduces context blindness | `[Evidenced]` | arXiv [2604.05278](https://arxiv.org/abs/2604.05278) |
| Confused-deputy / path escape → pin server root | `[Confirmed]` | ADR S-STF-E; PR #94 C1 lineage |
| Soft tools without fail-closed gate = theater | `[Confirmed]` | E-CGQ0 §0; DOC look-first doctrine |
| Remote/auto codegen host as default | **Refuse** | E-STK0 STK6/7/10; process/19 |
| Official MCP Python SDK pin | `[Unknown]` product choice — keep thin stdio until Spike says otherwise | E3-S1 |

---

## 3. Target tool surface (read-only)

Names are Spec vocabulary for Implement; OCP = new `QueryKindSpec` / sibling `GroundKindSpec` registry — **not** if/elif in the adapter.

| Tool (proposed) | CGQ map | Returns (sketch) |
| --- | --- | --- |
| `tip_probe_module` | CGQ4 | Imports, exports, callers (AST/tach-backed); path pinned under server root |
| `tip_load_depth_row` | CGQ2 | Mechanism id → `process/24` §2.x depth fields |
| `tip_accept_checklist` | CGQ3 | Whether Concern/Remedy/Depth/Witness fields present in a Spec path |
| `tip_list_witnesses` | CGQ5 | Test/fixture paths matching Accept witness tokens |
| `tip_research_map` | DOC/CGQ | Pointers: research README, backlog Active, effective-remedies |
| `doc_engine_help` | — | Extend notes: tip tools vs Stage-0 query tools |

**Explicitly out of surface:** `generate_code`, `apply_patch`, `write_file`, `git_commit`, `approve_spec`.

---

## 4. Architecture principles

1. **One dispatch SoR** — tip tools live in `doc_engine.query` (or cohesive `doc_engine.grounding` package ≤225 LOC modules); adapter stays thin.
2. **Same containment** — `require_server_root()`; for tip mode root = workspace checkout env (e.g. `DOC_ENGINE_ROOT` = repo), never caller path escape.
3. **Fail-closed pairing** — Cursor hook (or commit gate) requires receipt that design-shaped Impl called `tip_probe_*` + depth/accept tools — same pattern as research-map receipt (DOC7–9). Soft MCP-only = **Refuse** as sufficient.
4. **Stage-0 and tip coexist** — do not break `query_evidence` / `context_packet`; namespace tip tools; help text distinguishes.
5. **ast-grep remains citation SoR** for live structural `[Evidenced]` claims — MCP returns inventories; agents still cite via structural search mandate.

---

## 5. Spec decisions (GND1–GND10) — pending Approve

| ID | Decision |
| --- | --- |
| **GND1** | Tip-grounding MCP is the **Adopt** long-term vehicle for CGQ4/CGQ5 probes — not a codegen host |
| **GND2** | Reuse ADR S-STF-E isolation; never caller `root`; read-only tip tools |
| **GND3** | **Refuse** `generate_code` / `apply_patch` / write tools on this server |
| **GND4** | Tool set minimally includes probe / depth_row / accept_checklist / list_witnesses / research_map |
| **GND5** | Dispatch logic in library (`doc_engine.*`); `adapters/mcp` stays thin stdio façade |
| **GND6** | Fail-closed Cursor/commit receipt required for design-shaped Impl (soft tools alone insufficient) |
| **GND7** | **E-GND1 Implement** blocked until **E-CGQ0** and **E-GND0** both Approved |
| **GND8** | Stage-0 query tools remain; tip tools are additive (no breaking rename without Spec) |
| **GND9** | Official MCP SDK pin = Explicit Defer / Spike; default keep E3-S1 thin stdio |
| **GND10** | ≥10k★ bar unchanged; no new runtime SoT (Spec Kit engine, Sonar, LLM-judge floors) |

---

## 6. Spikes (before or with first Implement tickets)

| Spike | Question | Exit |
| --- | --- | --- |
| **GND-S1** | Workspace root env vs run_dir dual-mode without confused deputy | Written matrix + test that caller root is ignored |
| **GND-S2** | AST vs tach for `tip_probe_module` v1 | One vehicle chosen; LOC ≤225; complexipy ≤5 |
| **GND-S3** | Hook receipt shape for tip-tool calls | Matches research-map receipt pattern; failClosed true |

---

## 7. Adversarial checklist

- [ ] Tool writes the tree or returns a “patch”? — **Fail GND3.**
- [ ] Implement starts before CGQ Approve? — **Fail GND7.**
- [ ] MCP tools exist but no fail-closed receipt? — **Fail GND6.**
- [ ] Adapter reimplements filters? — **Fail GND5.**
- [ ] Tip MCP replaces E-STK watch≠fixer? — **Fail** STK / GND1.

---

## 8. Epic sketch

### E-GND0 — Spec gate (this memo)

Exit: Approve GND1–GND10; backlog P22.0.

### E-GND1 — Implement (after CGQ0 + GND0 Approve)

| Ticket | Acceptance |
| --- | --- |
| GND1-A | Registry + `tip_probe_module` + characterization tests |
| GND1-B | `tip_load_depth_row` + `tip_accept_checklist` |
| GND1-C | `tip_list_witnesses` + help text split Stage-0 vs tip |
| GND1-D | Fail-closed receipt hook/gate (GND-S3) |
| GND1-V | Verify: isolation tests, size/complexipy, claims if scripts/hooks touched |

---

## 9. Exit

**E-GND0 DRAFT** until human Approve of GND1–GND10.
No tip-grounding Implement in this pass — research + Spec only; pairs with E-CGQ0.
