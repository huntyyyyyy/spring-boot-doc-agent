---
title: E-CX0 — C4 of what the research adopted (not the kernel)
status: DRAFT visualization — parked; not Approve; not Implement
parent: docs/design/code-intel/README.md
schema: docs/design/code-intel/adopted-entities-schema-2026-08-13.md
research date: 2026-08-13
spec_gate: DRAFT E-CX0 map
bloom_gate: required-through-create
claim tiers: Evidenced / Confirmed / Unknown
do_not:
  - treat this as Approve to code S1 or the kernel
  - collapse doc-engine and intent-kernel into one box
  - draw SPO / index / LiteLLM as in-scope
---

# What is going on (C4)

One sentence: **this plugin scans Spring and writes docs; Serena is a laptop
IDE for the Java tree; a write-kernel is a different repo we are not
building now.**

| Stamp | Meaning |
| --- | --- |
| **Adopt (operator)** | Serena + jdtls on OCS. Not in `requirements.txt`. |
| **Embody (this repo)** | Existing `facts.jsonl` + CodeQL pack. S1 only after a **named miss**. |
| **Adopt later (skill)** | S2: agent **runs** gates we already have. |
| **Defer** | `intent-kernel` CAS write (D-00=B). Other C4: `intent-kernel-cas-apply-design-2026-08-13.md`. |
| **Refuse** | Custom index, SPO graph, planner, OPA, LiteLLM-in-front, S1 on this OCS log. |

S0 grep log: [`s0-ocs-run-log-2026-08-13.md`](s0-ocs-run-log-2026-08-13.md)
— **S1 not authorized**. Schema:
[`adopted-entities-schema-2026-08-13.md`](adopted-entities-schema-2026-08-13.md).

## Bloom

| Level | Evidence |
| --- | --- |
| Remember | Serena `find_symbol` `[Evidenced — oraios tools]`. `Fact` eight keys `[Confirmed — facts_model.py:13-29]`. |
| Understand | Scan SoR ≠ LSP session ≠ CAS write. |
| Apply | S0 = MCP on OCS; S1 = extra predicates on same JSONL; S2 = invoke `pipeline gates`. |
| Analyze | Two homes. Cut list in parent README. |
| Evaluate | Drawing S1 as always-on false-greens the kill rule. |
| Create | This map + schema file. No `src/` tickets. |

```text
Iso: observe→act→remeasure ≅ S2 invoke | I3: pass-rate ≠ fail_under
| I5: facts.jsonl stays closed eight-field SoR
```

## L1 — System context

Solid = now. Dashed = deferred or not authorized.

```mermaid
C4Context
  title L1 — Adopted landscape (2026-08-13)
  Person(op, "You", "Laptop; OCS unzip")
  System_Ext(host, "Claude / Cursor", "MCP client")
  System_Ext(serena, "Serena 1.7.0", "jdtls; not a pip dep")
  System_Ext(ocs, "ocs-api-service", "Java 17 plant")
  System(docs, "spring-boot-doc-agent", "Scan + certify fourteen views")
  System_Ext(kernel, "intent-kernel", "CAS apply — DEFERRED other repo")
  Rel(op, host, "chat")
  Rel(host, serena, "stdio MCP planning")
  Rel(serena, ocs, "find_symbol / grep")
  Rel(op, docs, "doc-engine CLI")
  Rel(docs, ocs, "ast-grep / optional CodeQL")
  Rel(op, kernel, "not this program")
```

## L2 — Containers (this repo + laptop)

```mermaid
C4Container
  title L2 — Where bits live
  Person(op, "You")
  Container(mcp, "Serena MCP", "laptop", "S0 navigation")
  Container(scan, "scanning BC", "Python", "spring_signal_scan")
  Container(pack, "spring-signals pack", "CodeQL", "SpringMetaEdges always on")
  ContainerDb(ledger, "facts.jsonl", "JSONL", "eight-field Fact SoR")
  Container(gates, "pipeline gates", "Python", "S2 invoke target")
  Container_Ext(jdtls, "eclipse.jdt.ls", "JRE 21 + project JDK 17")
  Rel(op, mcp, "S0")
  Rel(mcp, jdtls, "LSP")
  Rel(op, scan, "CLI")
  Rel(scan, pack, "optional --allow-codeql-build")
  Rel(scan, ledger, "write Fact rows")
  Rel(op, gates, "S2 skill/CLI")
```

S1 would be **more rows in the same ledger**, not a new database. Idle until
a miss exists.

## L3 — Scan emit (code)

```mermaid
C4Component
  title L3 — facts emit (already in tree)
  Component(core, "facts_core.fact", "facts_core.py")
  Component(model, "Fact DTO", "facts_model.py")
  Component(emit, "write_facts_jsonl", "facts_emit.py")
  Component(query, "query_facts", "handlers/facts.py")
  Rel(core, model, "eight keys extra=forbid")
  Rel(core, emit, "JSONL")
  Rel(query, emit, "read / filter predicate")
```

`KNOWN_PREDICATES` today: `MAPS_TO`, `UNPROVEN`, `REFERENCES`, `DECLARES`,
`EXTENDS`, `IMPLEMENTS`, `ANNOTATED_WITH`, `X`
`[Confirmed — handlers/facts.py:9-20]`.

## Sequence (operator)

```mermaid
flowchart LR
  S0[S0 Serena laptop] -->|grep log 2026-08-13| NoS1[S1 off]
  S0 -.->|only if named miss| S1[S1 extra predicates]
  NoS1 --> S2[S2 run existing gates]
  S1 -.-> S2
  K[intent-kernel] -.->|D-00=B deferred| X[not here]
```
