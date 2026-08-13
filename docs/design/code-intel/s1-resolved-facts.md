---
title: E-CX0-S1 — Spring-resolved fact extractor
status: DRAFT Spec — parked; no Implement until Approve + S0 miss + #119/E-COH1
research date: 2026-08-13
spec_gate: DRAFT E-CX0-S1
bloom_gate: required-through-create
parent: docs/design/code-intel/README.md
relates: E-FACT0 (slice, not warehouse)
do_not:
  - flip metaResolutionEnabled() without Probe.ql on a real DB
  - add MCP write tools
  - treat CodeQL --build-mode none as compiled-DB equality
  - invent a Fact Store / SPO graph
  - start before S0 go/no-go names a miss
sources:
  primary:
    - spring-signals/codeql/packs/java-signals-lib/signals/Annotations.qll
    - spring-signals/codeql/packs/spring-signals/Probe.ql
    - spring-signals/codeql/packs/spring-signals/SpringMetaEdges.qll
    - src/doc_engine/scanning/facts_core.py
    - src/doc_engine/query/mcp_tools.py
---

# S1 — Spring-resolved fact extractor

**Goal:** Emit **resolved** Spring facts this repo’s ast-grep scan cannot see,
as `[Evidenced — path:line]` rows on the existing `facts.jsonl` ledger.

**Authorize only if** S0 CX0-S0-4 names a recurring miss (inherited/meta
`@Transactional`, effective mappings, or equivalent).

```text
Iso: CodeQL Datalog facts ≅ resolved types | I3: compiled DB ≠ hermetic
fixture ≠ --build-mode none | I5: Probe.ql stays the boolean for the
discovered-meta switch
```

## Bloom

| Level | Evidence |
| --- | --- |
| Remember | `metaResolutionEnabled()` is `none()` `[Confirmed — Annotations.qll:112]`. Flip only after `Probe.ql` on a real DB `[Confirmed — Probe.ql:15–20, CAMPAIGN.md trust gate]`. `SpringMetaEdges.qll` is hardcoded Spring contract, always on `[Confirmed — SpringMetaEdges.qll:14–20]`. `Fact` is an eight-field closed record `[Confirmed — facts_model.py]`. |
| Understand | ast-grep = source-text. This stage **extends the pack + scan emit**, not a new BC. Tags in `qualifiers` are human provenance, not model trust (S2 ablation). |
| Apply | CLI first: `doc-engine` / `spring_signal_scan --scanners …,codeql` already exists (`--allow-codeql-build` required) `[Confirmed — spring_signal_scan.py:119–130]`. New predicates ride `fact()`; `query_facts` already filters `--predicate`. |
| Analyze | **Embody** pack + ledger + `dispatch_tool` root pin. **Refuse** warehouse, embeddings, LLM extraction as SoR (E-FACT0 D3.1). Optional MCP **after** CLI is used; default **zero new tools**. |
| Evaluate | § False-green |
| Create | Tickets below |

## Seams (no `utils/`)

| Concern | Module |
| --- | --- |
| Queries / meta graph | `spring-signals/codeql/packs/spring-signals/` (+ lib `Annotations.qll`) |
| DB create / BQRS | `doc_engine.scanning.support._codeql_runner` |
| CLI flags | `doc_engine.tools.spring_signal_scan` (word flags, not `m`/`o`/`c`) |
| Ledger emit | `doc_engine.scanning.facts_core.fact` → `facts_emit.write_facts_jsonl` |
| Read path | existing `query_facts` / MCP `query_facts` |

New files: concept-named (`resolved_annotations.py`, pack `.ql`), each ≤225 LOC.

## Predicates (additive; closed `Fact` shape)

Reuse the eight keys. Do not add columns. Suggested predicates (names are
the contract; implementers must not silently alias):

| Predicate | Object | When |
| --- | --- | --- |
| `ANNOTATED_WITH` | annotation FQCN | resolved, including inherited/meta **the extractor actually proved** |
| `EFFECTIVE_MAPPING` | HTTP method + path | class+method composition |
| `TRANSACTIONAL_ON` | isolation/propagation or `true` | type or method after inheritance |
| `WIRES_BEAN` | bean id / type | constructor/field injection the DB can see |

`qualifiers.provenance` ∈ `exact` \| `spring_meta_edge` \| `probe_gated` \|
`unproven`. Humans read it. Models must not be assumed to weight it.

Citation: `file` + `line` ≥ 1 (`Fact` validator). Docs still use
`[Evidenced — path:line]`.

## FR / NFR

| ID | Requirement | Acceptance |
| --- | --- | --- |
| **FR-S1-01 Fixture** | Hermetic Java fixture with ≥1 meta/inherited case **ast-grep misses** and the extractor cites. | Test compares ast-grep empty vs extractor row. |
| **FR-S1-02 CLI** | Operator can emit JSONL without MCP. | `pytest` + CLI help uses words. |
| **FR-S1-03 Probe** | `metaResolutionEnabled()` stays `none()` until `Probe.ql` PASS on a real DB is committed in the **same** PR as the flip. | Pack + probe output in that PR. |
| **FR-S1-04 Ledger** | Rows validate as `Fact` (`extra=forbid`). | `write_facts_jsonl` round-trip. |
| **FR-S1-05 MCP** | Default: **no** new tools. If Approve later: ≤5, read-only, `args.pop("root", None)` then `_server_root()` `[Confirmed — mcp_tools.py:145–153]`. | Test: caller `root` ignored. |
| **NFR-S1-01** | LOC ≤225, complexipy ≤5, whole-repo `fail_under` 98.7. | CI. |
| **NFR-S1-02** | `--build-mode none` (if used) is a **sensor**. Equality to a compiled OCS DB is an E-OCS operator claim, not CI green. | Spec text + test does not assert plant equality. |
| **NFR-S1-03** | Sub-2s queries on the hermetic fixture ledger. | Timed test, labeled probe not SLO. |

## Tickets

| ID | Title | Acceptance |
| --- | --- | --- |
| **CX0-S1-1** | Hermetic fixture + ast-grep miss oracle | FR-S1-01 |
| **CX0-S1-2** | Pack query + CLI emit to `facts.jsonl` | FR-S1-02, FR-S1-04, NFR-S1-01 |
| **CX0-S1-3** | Probe.ql gate documented; no speculative flip | FR-S1-03 |
| **CX0-S1-4** | `query_facts` reads new predicates (zero new MCP) | FR-S1-05 default |
| **CX0-S1-5** | Sensor note for none-build vs compiled DB | NFR-S1-02, NFR-S1-03 |

## False-green

| Failure | Bite |
| --- | --- |
| Flip meta switch without Probe.ql | FR-S1-03 |
| Fixture that ast-grep already hits | FR-S1-01 |
| New MCP before CLI is used | FR-S1-05 |
| `--build-mode none` sold as OCS-equal | NFR-S1-02 |
| Tags claimed to raise model accuracy | belongs to S2 ablation; out of S1 DoD |
| Scoped `--cov` as 98.7 | constitution |

## Definition of Done

CLI + fixture test + probe policy. MCP optional and default-off. **Does not**
close E-FACT0. **Does not** authorize kernel writes.
