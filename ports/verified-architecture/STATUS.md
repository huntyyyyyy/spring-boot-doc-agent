---
title: STATUS — single pointer for cold agents
status: ACTIVE
last_reviewed: '2026-08-11'
doc_role: status
freeze_class: read_only
look_first:
  - AGENT_BOOTSTRAP.md
  - research/gaps/shallow-decisions-honesty-2026-08-10.md
  - research/INDEX.md
mcp_tools:
  - spec_status
accepted: false
corpus_version: '2026-08-11'
related:
  - AGENT_BOOTSTRAP.md
  - docs/adr/adr-0001-polyglot-first-product.md
  - research/gaps/anti-tautology-predicate-prose-2026-08-11.md
  - 07-system-design/schemas/va-doc-frontmatter.schema.json
---

# STATUS

## What is true right now

| Fact | Bound | If violated |
| --- | --- | --- |
| Product crates / daemons / extensions | **Forbidden** | Reject the change; cite no-code gate |
| Definition of Ready | **0** rows PASS; **D0 FAIL** | Do not claim Implement Ready |
| Port export | CONDITIONAL — tree usable for Spec only | Do not advertise research-complete |
| Engine + Spec corpus Model Context Protocol host | **Rust** (ADR-0007 / Spike) | Reject Python hosts / ACI revival |
| IDE presentation Model Context Protocol | **TypeScript** (ADR-0010) | Reject Spec corpus server in TS as default |
| WebAssembly LockCheck guest | **Could / Wave-3** (ADR-0004) | Reject as Spec host or Wave-1 Must |

Prose: whole words — `GLOSSARY.md`. Skills when editing: `predicate-prose`,
`whole-words-prose` (no bare acronyms in chat or new Markdown).

**Tip search policy (monorepo SoT):** tip `CLAUDE.md` (2026-08-09+) allows
`Grep`/`rg` for inventory; prefer `ast-grep` for structural citations. Stale
injected “hard-deny Grep” excerpts are **not** tip SoT — do not thrash. Port
does not restate a deny.

## Alarms (uncertainty already reduced — do not re-litigate)

1. Research depth was over-claimed → `research/gaps/entity-adoption-audit-2026-08-10.md`.  
2. Too many Draft Chosen/Adopt on thin digests → FREEZE —
   `research/gaps/shallow-decisions-honesty-2026-08-10.md`.  
3. Wire pin `2026-07-28` is Evidenced; **our** tool argument shapes = Pilot invent
   (0 exact public engines for claim memory / equivariance wrappers).  
4. Stakeholder brownfield / grounding-gap / Eyes-Hands-Wiki stack →
   `research/gaps/stakeholder-discovery-brownfield-mcp-2026-08-11.md` (OQ-01
   pressure; **not** a new Wave-1 tool list under FREEZE).

## FREEZE — allowed edit set

| Allowed | Forbidden |
| --- | --- |
| Deepen receipt freshness β/ρ (`deepen-receipt-beta-rho` + `SPIKE-receipt-fresh`; Fresh still unmeasured) | New Decision Matrices |
| Deepen claim-memory withdrawal | New Architecture Decision Records / Must entities |
| Deepen Model Context Protocol **handle lifecycle** only (host note Draft + `SPIKE-handle-TTL` unmeasured — not DoR PASS) | Math brainstorm → Adopt; Cargo scaffolds |
| Demote overclaim wording; predicate-prose rewrites; **sensor refresh** (DoR / honesty inventory) | Soft-pass D0 via schema file counts |

Optional outside deepen-3: read-only Spec corpus Spike (`SPIKE-SPEC-MCP-0`) —
does **not** unlock product `verify` tools.

## Parked

Everything not in the three deepen rows — including new language lanes and
verify Model Context Protocol Implement.
