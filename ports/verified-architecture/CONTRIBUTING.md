# Contributing

## Hard gate (no product code yet)

See `12-delivery/no-code-gate/README.md` and
`00-governance/dor-dod/DEFINITION_OF_READY.md`.

Agents with no chat history: start at `AGENT_BOOTSTRAP.md` + `STATUS.md`.

PRs may change planning Markdown (`00/`–`12/`, `docs/`, `research/`,
`.cursor/`) and docs CI only until DoR is green for the active wave:

1. Product boundary + wave Must StRS/SRS Accepted (or explicit Draft Approve)
2. Constraints ledger current; no open `blocks_code` OQs (or WAIVED)
3. Must NFRs are complete ATAM six-part QAS (no TBD measure on Must)
4. SoR vs derived matrix Draft; ports + ICD stubs for the spike seam
5. C4 Context + Container reviewed; Component only for touched BC
6. Relevant ADRs Accepted; others stay in `options/` / Proposed
7. Receipt schema + V&V Accept methods named
8. Tradeoff table updated for chosen tactics
9. Human wave Approve in `02-stakeholders/signoff/`

## Working draft

Content may be Draft/Proposed while still obeying **ISO 29148-shaped RE**,
**ATAM QAS**, **Nygard ADR**, and **C4** form.

## Where to write

Prefer `00/`–`12/` per `PRECODE_MAP.md`. Legacy `docs/` and `nests/` remain
until promoted — do not treat language nests as Approved Design.
