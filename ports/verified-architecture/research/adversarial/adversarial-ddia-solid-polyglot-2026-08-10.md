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
  - Treat VA process/50 as complete Spec without SoR matrix + ports + RE Approve
  - Ship dual Cover% or dual claims writers under “Rust engine”
  - Equate Packwerk/tach patterns with Spring DI resolve
  - Approve all polyglot crates as tip deps in one PR
  - Confuse architecture tours with stakeholder requirements
  - Implement without citing REQ-* from the RE package
sources:
  deepwiki_ask:
    - sourcegraph/scip-java · Spring DI / incomplete compile limits
    - tree-sitter/tree-sitter · large files · ERROR nodes · multi-lang ranges
    - model-checking/kani · CBMC/Z3 · concurrency out of scope
    - bytecodealliance/wasmtime · sandbox vs Docker · fuel/epoch limits
    - babashka/babashka · SCI scripts · datascript for file graphs
    - spf13/cobra · CLI lifecycle · plugin naming
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
**requirements engineering** (IEEE 29148-shaped), **DDIA north-star** (SoR vs
derived), **SOLID**, **DRY**, and GoF **creational / structural / behavioral**
patterns. Goal: completeness of **scope**, then a **polyglot research slate**.

**Verdict in one line.** VA’s *pyramid* is directionally right; as a Spec
it was incomplete without RE. **RE package drafted**
([`docs/requirements-2026-08-10.md`](../../design/docs/requirements-2026-08-10.md));
still missing SoR matrix, ports, failure taxonomy, incremental invalidation,
and an honest Spring-DI capability envelope before Cargo.

---

## 0b. Bloom

| Level | Evidence |
| --- | --- |
| **1** | DeepWiki Ask: scip-java, tree-sitter, Kani, wasmtime, Babashka, Cobra; Packwerk / Noumenon primary pages |
| **2** | Restate VA in SoR|derived + Stage-0/claims/coverage types |
| **3** | Map each Pilot to `pre_pr` / corpus / OCS without dual oracle |
| **4** | SOLID/pattern gaps; Embody vs Pilot per language |
| **5** | §3 adversarial + false-green/red |
| **6** | ADV-* + **RE-*** tickets + research slate §5 — Design blocked until SoR matrix **and** StRS/SRS/RTM |

---

## 0c. Requirements engineering (IEEE 29148-shaped) `[Evidenced — ISO 29148]`

process/50 remains an **architecture vision + epic sketch**. The **RE SoR** is
now drafted separately:

**[`docs/requirements/`](../../design/docs/requirements-2026-08-10.md)**
— StRS · SRS (MoSCoW) · NFR · RTM · validation vs verification · change control.

| 29148-shaped item | Was (50 only) | Now |
| --- | --- | --- |
| **Stakeholders / StRS** | Implicit | Named A-OP…A-OWN in RE §1 |
| **Mission need** | Slogan | Measurable intent + goals/constraints |
| **SRS functional** | Tours as features | `REQ-F-01…19` MoSCoW, implementation-free |
| **NFR** | Casual latency | `REQ-N-01…07` with budgets / observability |
| **RTM** | None | Need → REQ → port → Accept method |
| **Validation vs verification** | Collapsed | Separated in RE §4 |
| **Change control** | Lock sync tour only | RE-4 table |

**Still open:** human **Approve** of the RE draft; Design Spec still needs
ADV-1…3. process/50 must not reintroduce implementation-bound “requirements.”

---

## 1. DDIA north-star — SoR vs derived (completeness)

| Artifact (proposed) | Must be | Gap in process/50 |
| --- | --- | --- |
| Target Java sources + build | **SoR** for symbols | Assumed; no plant/index freshness contract |
| `index.scip` | **Derived** from compile | No rebuild rule / stale-index Accept |
| Bean registry SQLite | **Derived** from scan+SCIP+resolve | No single writer; Unknown not a first-class fact |
| Virtual dep graph | **Derived** | Cycle check without provenance |
| `.mdc` / locks | **SoR** (git) | Lock sync tour stated; no schema/version pin |
| LanceDB embeddings | **Derived** sensor | Risk of RAG treated as SoR in ghost tour |
| Proof-tour receipts | **Derived** witness | Schema not specified |
| `coverage.xml` / claims | Existing **SoR** | Must remain sole merge floors |

**DDIA fail conditions still open**

1. Two writers for “is this bean wiring true?” (LLM vs resolver) without winner.  
2. Ghost cache / embeddings used as authority for Cmd+K.  
3. No deviation filed if static Spring model disagrees with runtime DI.

**Required before Design Approve:** SoR matrix table in VA-1 with
`single-write-derive` for every new artifact (`sor-vs-derived`).

---

## 2. SOLID — does the pyramid respect ports?

| Principle | VA risk | Remedy |
| --- | --- | --- |
| **S** | “Rust engine” god object (parse+index+resolve+LSP+prefetch) | Split crates/modules by **one concept** (COH2): `IndexPort`, `Registry`, `Resolve`, `LockCheck`, `Receipt`, `Prefetch` |
| **O** | Hard-coded Spring rules in engine | Strategy/port: `WiringResolver` with Spring v1; plain-Java later |
| **L** | WASM LockCheck ≠ in-process LockCheck | Same interface; property tests for parity |
| **I** | Fat “analyzer” API | Narrow: `query_symbol`, `resolve_injection`, `check_locks`, `emit_tour` |
| **D** | Python orchestrator importing concrete SCIP paths | Depend on ports; Rust/PyO3 as adapter |

**DRY.** Today: three FM parsers + Stage-0 signals + (future) tree-sitter summaries
risk a fourth annotation taxonomy. **One stereotype vocabulary** shared by sg
rules, registry, and locks — or explicit mapping table (DRY via SoR, not copy).

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
| **Facade** | ACI for LLM (SWE-agent-like) | Named loosely; no public `__all__` bar |
| **Proxy** | WASM sandbox around LockCheck | Good; must not change semantics |
| **Composite** | Lock sets / package packs (Packwerk-like) | Lock versioning only file-level |

### Behavioral

| Pattern | Use | Gap |
| --- | --- | --- |
| **Strategy** | Resolve / LockCheck implementations | Implied |
| **Chain of Responsibility** | sg fast → SCIP → resolve → locks → SMT | Pipeline order stated; **short-circuit / budget** not |
| **Observer** | LSP / file watcher → re-resolve | Red squiggle needs it; missing |
| **Command** | Agent edits as reversible commands + verify | ACI incomplete |
| **Interpreter** | Lock DSL / MDC → executable checks | E-MD0 keys ≠ executable lock IR |
| **Mediator** | Prefetch vs LSP vs agent sharing cache | Ghost tour implies; no design |

**Scope completeness scorecard (adversarial)**

| Area | process/50 | Needed |
| --- | --- | --- |
| **Requirements (StRS/SRS/RTM)** | absent in 50 | **RE package drafted** — Approve open |
| L1 index | sketched | Adapter + stale policy |
| L1b Spring wire | sketched | Capability envelope (below) |
| L2 locks | sketched | **Executable IR** + Packwerk-like packages |
| L3 SMT | optional | Keep Defer; don’t block v1 |
| Proof tour | named | JSON schema + step IDs |
| Ghost | named | Predictor + TTL + privacy **+ MoSCoW** |
| LSP | named | Observer + incremental **+ MoSCoW** |
| Polyglot bell | named | Bridge SoR (OpenAPI) first |
| Failure taxonomy | weak | Unknown / ambiguous / stale / conflict |
| Security | WASM only | Supply chain for indexers; fuel limits |
| Team sync | locks in git | Lock schema version; migration |
| Observability | proof tour | Metrics: resolve Unknown rate, cache hit |

---

## 4. Spring DI capability envelope `[Evidenced — DeepWiki scip-java]`

scip-java does **not** capture: runtime `@Configuration` wiring richness,
`@Conditional`, AOP proxies, SpEL `@Value`/`@Qualifier` expressions, init order.
Incomplete compiles → partial SemanticDB.

**Therefore L1b Accept must be:**

- Resolve **Unknown** when >1 candidate or conditional.  
- Document **soundness class**: “static stereotype ∪ SCIP impls” ≠ JVM.  
- Never claim “proved beans” without runtime plant or Z3 encoding of a *narrow*
  invariant.

tree-sitter: large-file OK; **ERROR** nodes; incremental edits; multi-lang
ranges — good for summaries, not types `[Evidenced — DeepWiki tree-sitter]`.

---

## 5. Polyglot research slate (next-level tools)

Pilot-before-Refuse; Python tip SoT until cutover Approve.

### Rust (engine)

| Tool | Research question | Embody/Pilot |
| --- | --- | --- |
| **tree-sitter** (+ `tree-sitter-java`) | Surgical summaries; ERROR-tolerant walk | **Pilot** core of java-analyzer |
| **scip crate / scip proto** | Decode `index.scip` → SymbolFact | **Pilot** |
| **PyO3** | Expose Resolve/LockCheck to Python ACI | **Pilot** after hotspot |
| **Kani** | Prove Rust resolver properties (no UB, no panic on malformed SCIP) | **Defer** until crate stable `[Evidenced — Kani/CBMC/Z3]` |
| **wasmtime** host | Fuel/epoch sandbox for validator | **Pilot** harness `[Evidenced — wasmtime]` |

### WASM (sandbox)

| Tool | Research | Stance |
| --- | --- | --- |
| **wasmtime / WASI** | Capability limits vs Docker for agent tools | **Pilot** for LockCheck only |
| Guest = Rust LockCheck | Parity tests vs native | Required |

Not: “WASM proves Spring.”

### Go (chassis)

| Tool | Research | Stance |
| --- | --- | --- |
| **Cobra** | `va-daemon` / indexer watch / plugin bins | **Pilot** local daemon CLI `[Evidenced — Cobra]` |
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

### MDC / locks (policy SoR)

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
| Stale SCIP | Wrong “proof tour” | Index sha vs HEAD gate |
| Ambiguous DI → silent pick | False green wiring | Unknown hard-fail under strict locks |
| LLM cites embedding as fact | Ghost lies | RAG labeled derived |
| WASM/native LockCheck drift | False green in CI | Property parity suite |
| Lock file without IR | Theater MDC | Executable checks only |
| Polyglot tip thrash | Dual Cover% | Constitution 16-A |

---

## 7. Create — ADV tickets (amend VA)

| ID | Ticket | Acceptance |
| --- | --- | --- |
| **RE-1** | StRS — stakeholders, goals, constraints, OpsCon | **Drafted** in `docs/requirements` §1 — Approve open |
| **RE-2** | SRS — MoSCoW functional + NFR | **Drafted** §2–3 (`REQ-F-*` / `REQ-N-*`) |
| **RE-3** | RTM — need → REQ → design port → verify | **Drafted** §5 — every Must has Accept method |
| **RE-4** | Req change control for locks | **Drafted** §6 |
| **ADV-1** | SoR\|derived matrix for all LIE artifacts | Spec table; single writer each |
| **ADV-2** | Ports + adapters (`SymbolFact`, `WiringResolver`, `LockCheck`) | ≤225 LOC modules; no god engine |
| **ADV-3** | Spring capability envelope + Unknown taxonomy | Documented; tests for multi-candidate |
| **ADV-4** | Executable lock IR (Packwerk-inspired) | MDC/YAML → Check AST; controller→repo demo |
| **ADV-5** | Chain budget: sg → SCIP → resolve → locks | Latency SLOs from **RE-2 NFR** |
| **ADV-6** | Proof-tour JSON schema | Step IDs required or fail |
| **ADV-7** | Research Spikes (non-tip): Packwerk pattern, bb+Datascript, Cobra, wasmtime, scip-java | Keep/drop each |
| **ADV-8** | Design Spec only after **RE-1…3** + ADV-1…3 | Gate for Implement |

---

## 8. Recommended research order (next level)

1. **RE-1…3** — requirements before architecture fashion.  
2. **ADV-1…3** (paper) — SoR + ports + DI envelope.  
3. **scip-java corpus Spike** + SymbolFact adapter.  
4. **Lock IR** from Packwerk lessons + MDC/claims.  
5. **bb+Datascript** query over graph EDN.  
6. **Cobra daemon** watch → reindex.  
7. **wasmtime** wrap LockCheck.  
8. Ghost / LSP / Z3 only if MoSCoW Says Must/Should after graph+locks green.

---

## 9. Status

Adversarial companion to VA **amended**; **RE-1…4 drafted** in
`docs/requirements/`. process/50 remains Spec Draft;
**Design incomplete** until RE **Approve** + ADV-1…3. Polyglot slate is
**research/Pilot**, not tip rewrite.
