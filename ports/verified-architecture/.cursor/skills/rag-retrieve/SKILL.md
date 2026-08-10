---
name: rag-retrieve
description: Retrieve the right research pack for the active task without dumping the corpus into context
---

# Skill: RAG retrieve

## When to use

Agent or developer needs evidence from `research/` for the current task.
If you have no session context, run Skill `cold-start` first.

## Steps

1. Confirm the task from `STATUS.md` (do not retrieve “generally”).
2. Open `research/INDEX.md` and pick the **one** pack that matches the task.
3. Open that pack’s README or newest memo only; skim claim tiers.
4. If a nest is in context, also obey `nests/<bc>/.cursor/rules/nest.mdc`
   research bullets — do not open every nest.
5. Cite paths in answers. Do not paste entire memos into rules or chat.
6. If the answer must become product law, invoke Skill `promote-claim`.

## Pack quick map

| Need | Pack |
| --- | --- |
| Cold taxonomy / RE critique | `research/pre-code-bfs/` |
| May–Aug 2026 papers | `research/papers-2026-may-aug/` |
| Vision / Layers of Truth | `research/layers-of-truth/` |
| Adversarial / RE critique | `research/adversarial/` |
| Languages / peers | `research/polyglot/` |
| QAS / formal | `research/atam-formal/` |
| MDC / context efficiency | `research/mdc-devex/` |
