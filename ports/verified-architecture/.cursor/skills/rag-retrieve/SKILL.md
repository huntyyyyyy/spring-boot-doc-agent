---
name: rag-retrieve
description: Retrieve the right research pack for the active task without dumping the corpus into context
---

# Skill: RAG retrieve

## When to use

Agent or developer needs evidence from `research/` for the current task.

## Steps

1. Open `research/INDEX.md` and pick the **one** pack that matches the task.
2. Open that pack’s README or newest memo only; skim claim tiers.
3. If a nest is in context, also obey `nests/<bc>/.cursor/rules/nest.mdc`
   research bullets — do not open every nest.
4. Cite paths in answers. Do not paste entire memos into rules or chat.
5. If the answer must become product law, invoke Skill `promote-claim`.

## Pack quick map

| Need | Pack |
| --- | --- |
| Vision / Layers of Truth | `research/layers-of-truth/` |
| Adversarial / RE critique | `research/adversarial/` |
| Languages / peers | `research/polyglot/` |
| QAS / formal | `research/atam-formal/` |
| MDC / context efficiency | `research/mdc-devex/` |
