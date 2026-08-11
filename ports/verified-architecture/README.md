# Verified Architecture

Greenfield **specification** tree + claim-tiered research corpus. Product crates
are forbidden until Definition of Ready PASS (`STATUS.md`).

Whole words — [`GLOSSARY.md`](GLOSSARY.md). Edit skill — `predicate-prose`.

## Layers (authority)

| Path | Bound | Fail-mode |
| --- | --- | --- |
| `00/`–`12/` | Preferred Spec System of Record | New Musts outside FREEZE deepen-3 → reject |
| `docs/adr/`, `docs/c4/`, `docs/standards/` | Active Architecture Decision Records / C4 / standards | Duplicate Architecture Decision Record under `07/` → reject |
| `docs/requirements/`, `docs/constraints/` | Pointers only → `03/` / `04/` | Editing pointer as if System of Record → reject |
| `research/` | Evidence — retrieve one pack | Always-loading whole tree → reject |
| `nests/` | Language options; nest 08 Python **REFUSED** | Treating nests as Approved Design → reject |
| `.cursor/rules/` | ≤2 `alwaysApply` | Dumping research into always-on rules → reject |
| `AGENTS.md` | Thin Cloud ingest | Second rule essay here → reject |

## Stack locks

| Concern | Owner | Reject |
| --- | --- | --- |
| Engine + Spec corpus Model Context Protocol | Rust | Python host / ACI |
| IDE presentation Model Context Protocol | TypeScript | Spec corpus server as TypeScript default |
| LockCheck WebAssembly guest | Could / Wave-3 | Spec host; Wave-1 Must |

Must spine ≠ graph + locks alone — claim memory + Stateful Tool-Enabled Agentic
Deployment constraints + receipts (`08-verification/VERIFY_STACK.md`).

## Cold start

[`AGENT_BOOTSTRAP.md`](AGENT_BOOTSTRAP.md) → [`STATUS.md`](STATUS.md) →
[`AGENT_WALKTHROUGH.md`](AGENT_WALKTHROUGH.md) → [`STRUCTURE.md`](STRUCTURE.md) →
[`GLOSSARY.md`](GLOSSARY.md) → [`VERIFY_STACK.md`](08-verification/VERIFY_STACK.md).

Paste: [`HOW_TO_PRIME_AGENTS.md`](HOW_TO_PRIME_AGENTS.md).

## Readiness

| Gate | State | Bound |
| --- | --- | --- |
| Port / export | **CONDITIONAL** | Spec sandbox only — [`PORT_READY.md`](PORT_READY.md) / [`EXPORT.md`](EXPORT.md) |
| Implement | **NO** | Definition of Ready 0 PASS; D0 FAIL — [`STATUS.md`](STATUS.md) |
