---
title: MDC projection inventory — ports/verified-architecture only
status: ACTIVE — Wave-0 projections landed; Wave-1 backlog
date: '2026-08-11'
doc_role: index
freeze_class: read_only
look_first:
  - ../gaps/port-mdc-projection-rust-wasm-2026-08-11.md
  - ../../.cursor/rules/README.md
mcp_tools:
  - spec_lookup
accepted: false
corpus_version: '2026-08-11'
related:
  - ../gaps/port-mdc-projection-rust-wasm-2026-08-11.md
  - cursor-mdc-activation-algebra.md
---

# MDC projection inventory (port only)

**Rule:** Markdown SoT for evidence; `.cursor/rules/**/*.mdc` for Cursor
activation. Do not rename `research/**` to `.mdc`.

## Wave-0 — land now (projections)

| Projection `.mdc` | Mode | Points at (MD SoT) | Why |
| --- | --- | --- | --- |
| `projections/status-freeze.mdc` | globs `STATUS.md` + honesty gap | `STATUS.md`, honesty memo | FREEZE when status open |
| `projections/bootstrap.mdc` | agent-requested | `AGENT_BOOTSTRAP.md` | Cold start without dumping |
| `projections/glossary.mdc` | globs when editing port md | `GLOSSARY.md` | Whole words |
| `projections/dor.mdc` | globs `00-governance/**` | `DEFINITION_OF_READY.md` | 0 PASS honesty |
| `projections/verify-stack.mdc` | agent-requested (dup thin) | `08-verification/VERIFY_STACK.md` | Must spine pointer |
| `projections/decision-framework.mdc` | globs standards/decisions | `docs/standards/decision-framework.md` | Six-vector |
| `projections/spec-mcp-spike.mdc` | agent-requested | Spike + FM schema | Rust Spec MCP |
| `projections/architecture-brief.mdc` | globs brief | `ARCHITECTURE_BRIEF.md` | Shape without paste |

Existing lenses (`00`–`11`, nests) stay — projections **add** pointing, not replace.

## Wave-1 — backlog (not mass rename)

| MD cluster | Projection style | Notes |
| --- | --- | --- |
| Each `docs/adr/adr-*.md` | Optional one agent-requested “ADR lens” already covered by `03-architecture-docs` | No per-ADR `.mdc` unless Agent repeats mistakes |
| Each QAS | Covered by `02` + `06` globs | Bodies stay MD |
| `research/gaps/*.md` | One agent-requested `projections/gaps-honesty.mdc` | Not one MDC per gap |
| Digests | Stay MD; Rust indexes FM | |
| Nest READMEs | nest.mdc only | |

## Refuse list

- `*.md` → `*.mdc` under `research/`, `03-requirements/`, `docs/adr/` bodies
- alwaysApply projections
- Duplicate full memo text into projection bodies
