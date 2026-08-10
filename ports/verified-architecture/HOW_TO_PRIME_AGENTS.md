# How to feed this repo to a fresh AI agent

## Minimum prompt (paste)

```text
You are in the Verified Architecture planning corpus (standalone checkout).
No prior chat context. Read AGENT_BOOTSTRAP.md then STATUS.md.
Follow Skill cold-start. Do not write product code. Work the next FAIL
DoR / open blocks_code OQ. Prefer folders 00/–12/ per PRECODE_MAP.md.
Retrieve research via Skill rag-retrieve (one pack only).
```

## Repo as Cursor / Cloud root

1. Export/push this tree as its own GitHub repo (`EXPORT.md`).
2. Point the agent environment root at **this** tree (not a parent monorepo).
3. Ensure `.cursor/rules/` and `.cursor/skills/` are loaded from that root.
4. Attach `@AGENT_BOOTSTRAP.md` on the first message if rules fail to load.

## Still required before “build” agents

Cold-start priming stops wrong codegen. It does **not** finish Spec:

- Close OQ-01…08 / DoR rows in `STATUS.md`
- Fill Must QAS, ports/ICD, receipt schema
- Human wave Approve in `02-stakeholders/signoff/`

Only then switch STATUS phase to Implement and allow Spike charters.
