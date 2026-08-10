---
title: Agent bootstrap — cold start with no chat history
status: ACTIVE
audience: [agent, developer]
---

# AGENT_BOOTSTRAP — read this first

You have **no prior conversation**. This file is the priming packet.

## Who you are / where you are

You are working in a **planning + RAG corpus** for a verified polyglot
architecture product. Progressive disclosure (MDC + Skills + INDEX) is part
of the product.

**Product Must spine (wave-1 intent):** local virtual dep/DI **graph** +
**lock IR** + **proof-tour receipts** + honest **Unknown** — not chat
invention, not embeddings-as-symbol-truth, not org-wide social graph SaaS.

**Not ready:** emitting Rust/Go/Python/WASM **product** code, `Cargo.toml`
trees, or treating language folders as decided Design.

## Open these five (in order) — then stop browsing

1. This file (`AGENT_BOOTSTRAP.md`)
2. `STATUS.md` — current mode + next task
3. `PRECODE_MAP.md` — BFS domain tree `00/`…`12/`
4. `12-delivery/no-code-gate/README.md` — codegen Refuse until green
5. `04-constraints/open-questions/` — any `blocks_code: true` OQ

Only then retrieve from `research/INDEX.md` for the **one** pack the task needs.

## Operating mode (today)

| Mode | Value |
| --- | --- |
| Phase | **Spec / fill gaps** — not Implement |
| Allowed edits | Markdown under `00/`–`12/`, `docs/`, `research/`, `.cursor/` |
| Forbidden | Product source trees, mass language scaffolds, “just a spike crate” |
| Authority | `00/`–`12/` preferred; flat `docs/` + `nests/` are **legacy** until promoted |
| Science | Locked transfers only — `11-science-transfer/locked-transfers/` |

## Hard refuses (agents fail these without priming)

1. **Do not** generate product code until no-code gate is green.
2. **Do not** treat RE-MASTER / Phi / LanceDB / Kuzu org-graph drafts as Spec — see `research/pre-code-bfs/re-master-ai-draft-critique-2026-08-10.md`.
3. **Do not** rewrite Must NFRs as bare latency numbers — use six-part QAS (`03-requirements/qas/TEMPLATE.md`).
4. **Do not** confuse constraints with requirements.
5. **Do not** equate SCIP with runtime Spring DI; Unknown required when ambiguous.
6. **Do not** equate WASM sandbox with mathematical proof.
7. **Do not** use RAG/LLM text as a verify witness.
8. **Do not** always-load `research/` — retrieve one pack.
9. **Do not** put languages at the tip — candidates live in `07-system-design/options/`.
10. **Do not** promote neuromorphic / physical RC / IMC hardware into tip SoT.

## Correct work loop (until Implement Approve)

```text
STATUS.md → ARCHITECTURE_BRIEF.md if shape unclear
  → pick next OPEN/PARTIAL gap
  → edit only that domain folder under 00–12
  → if research needed: Skill rag-retrieve → one pack
  → close or waive OQ; update STATUS.md
  → never open Cargo/pyproject product trees
```

## Skills

| Skill | Use when |
| --- | --- |
| `cold-start` | Session start / lost context |
| `rag-retrieve` | Need evidence from `research/` |
| `promote-claim` | Research claim → authoritative docs |
| `fill-wave-gap` | Close a `blocks_code` OQ or write a QAS |

## Success for a cold agent

You are primed correctly if you can answer without chat history:

- What phase are we in? → Spec / gap-fill
- May I write engine code? → **No**
- What is the product shape? → Local CLI tool; monorepo after Spec (`ARCHITECTURE_BRIEF.md`)
- Where do new artifacts go? → `00/`–`12/` per `PRECODE_MAP.md`
- What blocks codegen? → Open OQs + incomplete Must QAS + no-code gate
