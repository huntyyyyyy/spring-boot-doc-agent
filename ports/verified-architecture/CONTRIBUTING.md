# Contributing

## Hard gate

Product crates / daemons / extensions → **reject** until Definition of Ready PASS
(`12-delivery/no-code-gate/README.md`, `00-governance/dor-dod/DEFINITION_OF_READY.md`).
Cold agents: `AGENT_BOOTSTRAP.md` → `STATUS.md`.

Until that gate is green, PRs may touch only planning Markdown (`00/`–`12/`,
`docs/`, `research/`, `.cursor/`) and docs CI. FREEZE deepen-3 still binds —
`STATUS.md`.

## Definition of Ready rows (Implement bar)

| # | Predicate | Fail if |
| --- | --- | --- |
| 1 | Wave Must Stakeholder / Software Requirements Accepted (or Draft Approve) | Boundary TBD |
| 2 | Constraints ledger current; no open `blocks_code` (or WAIVED) | Open question blocks silent |
| 3 | Must non-functionals = six-part Quality Attribute Scenario | TBD measure on Must |
| 4 | System of Record vs derived matrix Draft; ports + Interface Control Document for spike seam | Missing seam stubs |
| 5 | C4 Context + Container reviewed; Component only for touched bounded context | Full Code-level without touch |
| 6 | Relevant Architecture Decision Records Accepted | Soft-Adopt without Accept criterion |
| 7 | Receipt schema + Verification and Validation Accept methods named | Schema file count as PASS |
| 8 | Tradeoff table updated for chosen tactics | Praise-only Consequences |
| 9 | Human wave Approve in `02-stakeholders/signoff/` | Unsigned claim of Ready |

## Draft form (still enforced)

ISO 29148-shaped requirements engineering · Architecture Tradeoff Analysis Method
Quality Attribute Scenario · Nygard Architecture Decision Record · C4.

## Where to write

New artifacts → `00/`–`12/` per `PRECODE_MAP.md`. Legacy `docs/` / `nests/` =
promote-or-leave; nests are not Approved Design. Nest 08 Python = REFUSED.
Stack: Rust Spec host; TypeScript IDE only; WebAssembly LockCheck Could.
