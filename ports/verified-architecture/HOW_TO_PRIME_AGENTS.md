# How to feed this repo to a fresh AI agent

## Minimum prompt (paste into the new repository)

```text
Repo root = this planning corpus. No prior chat.
Port Ready = yes; Implement Ready = no (see PORT_READY.md + STATUS.md).
Read in order:
  AGENT_BOOTSTRAP.md → STATUS.md → AGENT_WALKTHROUGH.md → STRUCTURE.md
  → 08-verification/VERIFY_STACK.md
  → research/papers-2026-may-aug/june-august-2026-port-readiness.md (if amending Spec)
Follow Skill cold-start. Do not write product code.
Must spine = graph+locks ∧ EA-Graph ∧ STEAD ∧ freshness-bound receipts.
Next human task: sign SIGNOFF_LOG.md; then work STATUS next tasks.
```

## Repo as Cursor / Cloud root

1. Create empty GitHub repo; push **contents of this folder as root** (`EXPORT.md`).
2. Point the agent environment at that root (not a parent monorepo).
3. Confirm `.cursor/rules/` + `.cursor/skills/` load.
4. If rules fail: `@AGENT_BOOTSTRAP.md` + `@AGENT_WALKTHROUGH.md` on message 1.

## Sequential chain (short)

See mermaid + table in `AGENT_WALKTHROUGH.md`. Visual tree in `STRUCTURE.md`.

## Before “build” agents

DoR green + human signoff. EA-Graph claim Accept tests + STEAD ST-1…5 in ICD
schemas are part of Ready — not optional polish.
