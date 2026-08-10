# How to feed this repository to a fresh AI agent

## Minimum prompt (paste into the new repository)

```text
Repository root = this planning corpus. No prior chat.
Port ready = yes; Implement ready = no (see PORT_READY.md + STATUS.md).
Use whole words — see GLOSSARY.md (no bare acronyms in prose).
Read in order:
  AGENT_BOOTSTRAP.md → STATUS.md → AGENT_WALKTHROUGH.md → STRUCTURE.md
  → GLOSSARY.md
  → 08-verification/VERIFY_STACK.md
  → research/papers-2026-may-aug/june-august-2026-port-readiness.md
    (if amending the specification)
Follow Skill cold-start. Do not write product code.
Must spine = graph + locks AND artifact-anchored claim memory
  AND Stateful Tool-Enabled Agentic Deployment tool constraints
  AND freshness-bound receipts.
Next human task: sign SIGNOFF_LOG.md; then work STATUS next tasks.
```

## Repository as Cursor / Cloud root

1. Create empty GitHub repository; push **contents of this folder as root** (`EXPORT.md`).
2. Point the agent environment at that root (not a parent monorepo).
3. Confirm `.cursor/rules/` + `.cursor/skills/` load.
4. If rules fail: `@AGENT_BOOTSTRAP.md` + `@AGENT_WALKTHROUGH.md` on message 1.

## Sequential chain (short)

See diagram + table in `AGENT_WALKTHROUGH.md`. Visual tree in `STRUCTURE.md`.

## Before “build” agents

Definition of Ready green + human signoff. Artifact-anchored claim Accept tests
and Stateful Tool-Enabled Agentic Deployment constraints ST-1…5 in Interface
Control Document schemas are part of Ready — not optional polish.
