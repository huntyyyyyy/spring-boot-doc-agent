---
title: VA adversarial SE review — DDIA · SOLID · patterns · polyglot slate
status: RESEARCH COMPLETE — Spec companion (feeds VA Design; no Implement)
date: 2026-08-10
epic: VA
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
related:

  - docs/requirements/
  - docs/design/ddia-north-star/domains/01-data-flow-and-truth/concepts/system-of-record-vs-derived.md
  - research/polyglot/

  - research/mdc-devex/
  - docs/research/se-quality-synthesis-2026-08-08.md

do_not:
  - Treat VA process/50 as complete Spec without System of Record matrix + ports + RE Approve
  - Ship dual Cover% or dual claims writers under “Rust engine”
  - Equate Packwerk/tach patterns with Spring Dependency Injection resolve
  - Approve all polyglot crates as tip deps in one PR
  - Confuse architecture tours with stakeholder requirements
  - Implement without citing REQ-* from the RE package
sources:
  deepwiki_ask:
    - sourcegraph/scip-java · Spring Dependency Injection / incomplete compile limits
    - tree-sitter/tree-sitter · large files · ERROR nodes · multi-lang ranges
    - model-checking/kani · CBMC/Z3 · concurrency out of scope
    - bytecodealliance/wasmtime · sandbox vs Docker · fuel/epoch limits
    - babashka/babashka · SCI scripts · datascript for file graphs
    - spf13/cobra · command-line interface lifecycle · plugin naming
  github:
    - https://github.com/Shopify/packwerk
    - https://github.com/sourcegraph/scip-java
    - https://github.com/leifericf/noumenon
  web:
    - https://www.iso.org/standard/72089.html  # ISO/IEC/IEEE 29148 RE
  mcp: https://mcp.deepwiki.com/mcp
---

# Adversarial principal-SE review of VA

**Role.** Adversarial principal SE against
[`process/50`](50-local-first-verified-architecture-agent-2026-08-10.md), using
**requirements engineering** (IEEE 29148-shaped), **DDIA north-star** (System of Record vs
derived), **SOLID**, **DRY**, and GoF **creational / structural / behavioral**
patterns. Goal: completeness of **scope**, then a **polyglot research slate**.

**Verdict in one line.** VA’s *pyramid* is directionally right; as a Spec
it was incomplete without RE. **RE package drafted**
([`docs/requirements-2026-08-10.md`](../../design/docs/requirements-2026-08-10.md));
still missing System of Record matrix, ports, failure taxonomy, incremental invalidation,
and an honest Spring-Dependency Injection capability envelope before Cargo.

---

## 0b. Bloom

| Level | Evidence |
| --- | --- |
| **1** | DeepWiki Ask: scip-java, tree-sitter, Kani, wasmtime, Babashka, Cobra; Packwerk / Noumenon primary pages |
| **2** | Restate VA in System of Record|derived + Stage-0/claims/coverage types |
| **3** | Map each Pilot to `pre_pr` / corpus / OCS without dual oracle |
| **4** | SOLID/pattern gaps; Embody vs Pilot per language |
| **5** | §3 adversarial + false-green/red |
| **6** | ADV-* + **RE-*** tickets + research slate §5 — Design blocked until System of Record matrix **and** Stakeholder Requirements Specification/Software Requirements Specification/Requirements Traceability Matrix |

---

## 0c. Requirements engineering (IEEE 29148-shaped) `[Evidenced — ISO 29148]`

process/50 remains an **architecture vision + epic sketch**. The **RE System of Record** is
now drafted separately:

**[`docs/requirements/`](../../design/docs/requirements-2026-08-10.md)**
— Stakeholder Requirements Specification · Software Requirements Specification (MoSCoW) · non-functional requirement · Requirements Traceability Matrix · validation vs verification · change control.

| 29148-shaped item | Was (50 only) | Now |
| --- | --- | --- |
| **Stakeholders / Stakeholder Requirements Specification** | Implicit | Named A-OP…A-OWN in RE §1 |
| **Mission need** | Slogan | Measurable intent + goals/constraints |
| **Software Requirements Specification functional** | Tours as features | `REQ-F-01…19` MoSCoW, implementation-free |
| **non-functional requirement** | Casual latency | `REQ-N-01…07` with budgets / observability |
| **Requirements Traceability Matrix** | None | Need → REQ → port → Accept method |
| **Validation vs verification** | Collapsed | Separated in RE §4 |
| **Change control** | Lock sync tour only | RE-4 table |

**Still open:** human **Approve** of the RE draft; Design Spec still needs
ADV-1…3. process/50 must not reintroduce implementation-bound “requirements.”

---

## 1. DDIA north-star — System of Record vs derived (completeness)

| Artifact (proposed) | Must be | Gap in process/50 |
| --- | --- | --- |
| Target Java sources + build | **System of Record** for symbols | Assumed; no plant/index freshness contract |
| `index.scip` | **Derived** from compile | No rebuild rule / stale-index Accept |
| Bean registry SQLite | **Derived** from scan+Source Code Index Protocol+resolve | No single writer; Unknown not a first-class fact |
| Virtual dep graph | **Derived** | Cycle check without provenance |
| `.mdc` / locks | **System of Record** (git) | Lock sync tour stated; no schema/version pin |
| LanceDB embeddings | **Derived** sensor | Risk of Retrieval-Augmented Generation treated as System of Record in ghost tour |
| Proof-tour receipts | **Derived** witness | Schema not specified |
| `coverage.xml` / claims | Existing **System of Record** | Must remain sole merge floors |

**DDIA fail conditions still open**

1. Two writers for “is this bean wiring true?” (large language model vs resolver) without winner.  
2. Ghost cache / embeddings used as authority for Cmd+K.  
3. No deviation filed if static Spring model disagrees with runtime Dependency Injection.

**Required before Design Approve:** System of Record matrix table in VA-1 with
`single-write-derive` for every new artifact (`sor-vs-derived`).

---

## 2. SOLID — does the pyramid respect ports?

| Principle | VA risk | Remedy |
| --- | --- | --- |
| **S** | “Rust engine” god object (parse+index+resolve+Language Server Protocol+prefetch) | Split crates/modules by **one concept** (COH2): `IndexPort`, `Registry`, `Resolve`, `LockCheck`, `Receipt`, `Prefetch` |
| **O** | Hard-coded Spring rules in engine | Strategy/port: `WiringResolver` with Spring v1; plain-Java later |
| **L** | WebAssembly LockCheck ≠ in-process LockCheck | Same interface; property tests for parity |
| **I** | Fat “analyzer” API | Narrow: `query_symbol`, `resolve_injection`, `check_locks`, `emit_tour` |
| **D** | Python orchestrator importing concrete Source Code Index Protocol paths | Depend on ports; Rust/PyO3 as adapter |

**DRY.** Today: three FM parsers + Stage-0 signals + (future) tree-sitter summaries
risk a fourth annotation taxonomy. **One stereotype vocabulary** shared by sg
rules, registry, and locks — or explicit mapping table (DRY via System of Record, not copy).

---

## 3. Design patterns — what’s missing from scope

### Creational

| Pattern | Use | Gap |
| --- | --- | --- |
| **Factory / Abstract Factory** | `WiringResolver` per framework | Not named |
| **Builder** | Proof-tour step assembly | Not named |
| **Prototype** | Ghost cache entries from cursor region | Invalidation unspec’d |

### Structural

| Pattern | Use | Gap |
| --- | --- | --- |
| **Adapter** | scip-java / tree-sitter / sg → common `SymbolFact` | Critical; absent |
| **Facade** | ACI for large language model (SWE-agent-like) | Named loosely; no public `__all__` bar |
| **Proxy** | WebAssembly sandbox around LockCheck | Good; must not change semantics |
| **Composite** | Lock sets / package packs (Packwerk-like) | Lock versioning only file-level |

### Behavioral

| Pattern | Use | Gap |
| --- | --- | --- |
| **Strategy** | Resolve / LockCheck implementations | Implied |
| **Chain of Responsibility** | sg fast → Source Code Index Protocol → resolve → locks → SMT | Pipeline order stated; **short-circuit / budget** not |
| **Observer** | Language Server Protocol / file watcher → re-resolve | Red squiggle needs it; missing |
| **Command** | Agent edits as reversible commands + verify | ACI incomplete |
| **Interpreter** | Lock DSL / MDC → executable checks | E-MD0 keys ≠ executable lock IR |
| **Mediator** | Prefetch vs Language Server Protocol vs agent sharing cache | Ghost tour implies; no design |

**Scope completeness scorecard (adversarial)**

| Area | process/50 | Needed |
| --- | --- | --- |
| **Requirements (Stakeholder Requirements Specification/Software Requirements Specification/Requirements Traceability Matrix)** | absent in 50 | **RE package drafted** — Approve open |
| L1 index | sketched | Adapter + stale policy |
| L1b Spring wire | sketched | Capability envelope (below) |
| L2 locks | sketched | **Executable IR** + Packwerk-like packages |
| L3 SMT | optional | Keep Defer; don’t block v1 |
| Proof tour | named | JSON schema + step IDs |
| Ghost | named | Predictor + TTL + privacy **+ MoSCoW** |
| Language Server Protocol | named | Observer + incremental **+ MoSCoW** |
| Polyglot bell | named | Bridge System of Record (OpenAPI) first |
| Failure taxonomy | weak | Unknown / ambiguous / stale / conflict |
| Security | WebAssembly only | Supply chain for indexers; fuel limits |
| Team sync | locks in git | Lock schema version; migration |
| Observability | proof tour | Metrics: resolve Unknown rate, cache hit |

---

## 4. Spring Dependency Injection capability envelope `[Evidenced — DeepWiki scip-java]`

scip-java does **not** capture: runtime `@Configuration` wiring richness,
`@Conditional`, AOP proxies, SpEL `@Value`/`@Qualifier` expressions, init order.
Incomplete compiles → partial SemanticDB.

**Therefore L1b Accept must be:**

- Resolve **Unknown** when >1 candidate or conditional.  
- Document **soundness class**: “static stereotype ∪ Source Code Index Protocol impls” ≠ JVM.  
- Never claim “proved beans” without runtime plant or Z3 encoding of a *narrow*
  invariant.

tree-sitter: large-file OK; **ERROR** nodes; incremental edits; multi-lang
ranges — good for summaries, not types `[Evidenced — DeepWiki tree-sitter]`.

---

## 5. Polyglot research slate (next-level tools)

Pilot-before-Refuse; Python tip Source of Truth until cutover Approve.

### Rust (engine)

| Tool | Research question | Embody/Pilot |
| --- | --- | --- |
| **tree-sitter** (+ `tree-sitter-java`) | Surgical summaries; ERROR-tolerant walk | **Pilot** core of java-analyzer |
| **scip crate / scip proto** | Decode `index.scip` → SymbolFact | **Pilot** |
| **PyO3** | Expose Resolve/LockCheck to Python ACI | **Pilot** after hotspot |
| **Kani** | Prove Rust resolver properties (no UB, no panic on malformed Source Code Index Protocol) | **Defer** until crate stable `[Evidenced — Kani/CBMC/Z3]` |
| **wasmtime** host | Fuel/epoch sandbox for validator | **Pilot** harness `[Evidenced — wasmtime]` |

### WebAssembly (sandbox)

| Tool | Research | Stance |
| --- | --- | --- |
| **wasmtime / WASI** | Capability limits vs Docker for agent tools | **Pilot** for LockCheck only |
| Guest = Rust LockCheck | Parity tests vs native | Required |

Not: “WebAssembly proves Spring.”

### Go (chassis)

| Tool | Research | Stance |
| --- | --- | --- |
| **Cobra** | `va-daemon` / indexer watch / plugin bins | **Pilot** local daemon command-line interface `[Evidenced — Cobra]` |
| **go-plugin / hashicorp** | Optional language sidecars | Pattern from process/48 |
| **fsnotify** | Lock + source watch → reindex trigger | With Observer |

### Clojure / Babashka (brain / query)

| Tool | Research | Stance |
| --- | --- | --- |
| **Babashka + Datascript** | Query bean/dep EDN graph; fast scripts | **Pilot** graph REPL `[Evidenced — bb/datascript]` |
| **Noumenon** (experimental) | Codebase → Datomic KG for agents | **Watch / Pattern** — early beta |
| Full JVM Clojure | Long-running KG service | **Defer** |

### Ruby (locks DSL / boundaries)

| Tool | Research | Stance |
| --- | --- | --- |
| **Packwerk** | Package deps + privacy + cycle; `package_todo` bankruptcy | **Adopt pattern** for lock *packages* (not tip Ruby) `[Evidenced — Shopify]` |
| Sorbet signatures | Constants as typed edges | Pattern only |
| Arch-style DSL | `controllers.may_depend → services` | Inform **MDC lock IR** |

### MDC / locks (policy System of Record)

| Tool / practice | Research | Stance |
| --- | --- | --- |
| Cursor `.mdc` activation algebra (E-MDC0) | Globs vs alwaysApply vs agent-requested | **Embody** |
| E-MD0 closed FM | Machine keys for research; separate **lock IR** | **Embody** + extend |
| Packwerk-like `locks/*.yml` | `enforce_dependencies`, public API folders | **Pilot** schema |
| claims `verify:` | Path/predicate gates already exist | **Embody** as lock backend #0 |

---

## 6. Adversarial checklist (false green / red)

| Attack | Effect | Control |
| --- | --- | --- |
| Stale Source Code Index Protocol | Wrong “proof tour” | Index sha vs HEAD gate |
| Ambiguous Dependency Injection → silent pick | False green wiring | Unknown hard-fail under strict locks |
| large language model cites embedding as fact | Ghost lies | Retrieval-Augmented Generation labeled derived |
| WebAssembly/native LockCheck drift | False green in CI | Property parity suite |
| Lock file without IR | Theater MDC | Executable checks only |
| Polyglot tip thrash | Dual Cover% | Constitution 16-A |

---

## 7. Create — ADV tickets (amend VA)

| ID | Ticket | Acceptance |
| --- | --- | --- |
| **RE-1** | Stakeholder Requirements Specification — stakeholders, goals, constraints, OpsCon | **Drafted** in `docs/requirements` §1 — Approve open |
| **RE-2** | Software Requirements Specification — MoSCoW functional + non-functional requirement | **Drafted** §2–3 (`REQ-F-*` / `REQ-N-*`) |
| **RE-3** | Requirements Traceability Matrix — need → REQ → design port → verify | **Drafted** §5 — every Must has Accept method |
| **RE-4** | Req change control for locks | **Drafted** §6 |
| **ADV-1** | System of Record\|derived matrix for all LIE artifacts | Spec table; single writer each |
| **ADV-2** | Ports + adapters (`SymbolFact`, `WiringResolver`, `LockCheck`) | ≤225 LOC modules; no god engine |
| **ADV-3** | Spring capability envelope + Unknown taxonomy | Documented; tests for multi-candidate |
| **ADV-4** | Executable lock IR (Packwerk-inspired) | MDC/YAML → Check AST; controller→repo demo |
| **ADV-5** | Chain budget: sg → Source Code Index Protocol → resolve → locks | Latency SLOs from **RE-2 non-functional requirement** |
| **ADV-6** | Proof-tour JSON schema | Step IDs required or fail |
| **ADV-7** | Research Spikes (non-tip): Packwerk pattern, bb+Datascript, Cobra, wasmtime, scip-java | Keep/drop each |
| **ADV-8** | Design Spec only after **RE-1…3** + ADV-1…3 | Gate for Implement |

---

## 8. Recommended research order (next level)

1. **RE-1…3** — requirements before architecture fashion.  
2. **ADV-1…3** (paper) — System of Record + ports + Dependency Injection envelope.  
3. **scip-java corpus Spike** + SymbolFact adapter.  
4. **Lock IR** from Packwerk lessons + MDC/claims.  
5. **bb+Datascript** query over graph EDN.  
6. **Cobra daemon** watch → reindex.  
7. **wasmtime** wrap LockCheck.  
8. Ghost / Language Server Protocol / Z3 only if MoSCoW Says Must/Should after graph+locks green.

---

## 9. Status

Adversarial companion to VA **amended**; **RE-1…4 drafted** in
`docs/requirements/`. process/50 remains Spec Draft;
**Design incomplete** until RE **Approve** + ADV-1…3. Polyglot slate is
**research/Pilot**, not tip rewrite.
