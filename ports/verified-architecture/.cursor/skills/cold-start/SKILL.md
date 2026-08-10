---
name: cold-start
description: Prime a new agent session with no chat history — read bootstrap, status, gates, then pick next gap
---

# Skill: Cold start

## When to use

Session start, resumed chat without context, or any agent that has not
read `AGENT_BOOTSTRAP.md` in this session.

## Steps

1. Read `AGENT_BOOTSTRAP.md` fully.
2. Read `STATUS.md` — obey **Next tasks** and **Do not do next**.
3. Skim `12-delivery/no-code-gate/README.md` and
   `00-governance/dor-dod/DEFINITION_OF_READY.md`.
4. List open `blocks_code: true` files under `04-constraints/open-questions/`.
5. Announce: phase, whether codegen is allowed (almost always **no**), and
   the single next task you will take.
6. Do **not** browse the entire repo. Retrieve one research pack only if
   the next task requires evidence (`rag-retrieve`).

## Exit

You may proceed only after stating the next task ID (e.g. OQ-01) and the
exact file you will edit.
