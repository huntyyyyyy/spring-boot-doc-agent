---
title: Principal architecture brief — leaders, adoption, shape, MVP, math, gaps
status: DRAFT — Spec (human Approve pending)
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
audience: [architect, principal-se, agent, rag]
bloom_gate: required-through-create
---

# Principal architecture brief

**Authors’ stance:** principal software engineer + principal architect.  
**Purpose:** replace slogan-docs with *where to look*, *who ships*, *what we
build first*, and *what is still missing*.  
**Stars / push dates:** GitHub API snapshot **2026-08-10** `[Evidenced]`.

---

## 0. Executive decisions (read these first)

| Decision | Choice | Why | Still needed |
| --- | --- | --- | --- |
| **Product shape** | **Local developer tool** (CLI + optional LSP/MCP) that reads a **target repo** | Matches local-first verify; not a SaaS knowledge graph | OQ-01 human Accept |
| **Distribution** | **Monorepo of crates/plugins** *after* Spec; ship as **one CLI binary + optional side cars** | One version line for locks↔engine; sidecars stay optional | Ports/ICD before Cargo |
| **Not** | Multi-tenant org services / Backstage mesh as MVP | Explodes OpsCon, auth, SoR | Phase-3+ only |
| **Not** | “Import a library into Spring apps” as primary | Wrong customer; we analyze their tree, we don’t become their runtime | Could later as SDK |
| **MVP verify** | Virtual graph + lock IR + receipts + Unknown/**unprovable** | High ROI; Jul–Aug EA-Graph reinforces anchors | Schemas + plants |
| **Harness loop** | Agent **proposes**; LockCheck+receipt **decides** (Aria-shaped) | Jul 2026 Aria: kernel/harness is trust anchor | ACI docs |
| **RAG** | Corpus/retrieve for *this planning product* and later assist | Never verify witness | Retrieval contract |
| **Memory split** | `Registry` (verify) ≠ `AgentMemory` (optional later) | Neo4j-class memory ≠ merge locks; Kuzu deprecated in ecosystems | Port boundary |
| **Languages** | Rust engine **Pilot after ports**; Go/Clojure/Ruby/TS **Pilot lanes**; Python **peer ACI** | Adoption exists per lane; tip identity ≠ nine languages day one | Wave-1 BC set (OQ-08) |

**Jul–Aug 2026 adversarial pass:** nothing OVERTURNS this table; amendments in
`research/adversarial/july-august-2026-overturn-review.md`.

---

## 1. What the system actually is (architecture)

### 1.1 C4 one-liner

A **local Verified Architecture Engine** consumes a target codebase’s sources +
`index.scip` (+ lock files in git), builds a **derived** registry/graph, evaluates
**policy locks**, and emits **diagnostics + proof-tour receipts**. Humans and
agents share the same checker.

### 1.2 Recommended deployment topology

```text
[Target git repo]  --locks.mdc / pack manifests (SoR policy)--+
       |                                                     |
       | sources                                             v
       |                              +-------- Engine (Rust Pilot) ----+
       +-- scip-java (external) --> index.scip --> | decode | resolve |  |
                                                   | LockCheck | receipt|
                                                   +-----+------+-------+
                                                         |
                          SQLite registry (derived) <----+
                                                         |
                    optional: Go watch daemon, TS LSP, bb graph queries
                                                         |
                                              IDE diagnostics / CLI / MCP
```

| Topology option | Verdict |
| --- | --- |
| **Monorepo (engine + specs + plugins)** | **Adopt for product source** after Spec Approve — single lock/engine version |
| **Multi-service org platform** | **Refuse MVP** — wrong scale |
| **Library embedded in customer apps** | **Defer** — secondary SDK; primary is out-of-process tool |
| **Pure SaaS** | **Refuse MVP** — fights local-first + privacy QAS |

### 1.3 Where artifacts land (schemas / modeling / integrations)

| Concern | Lands in (planning now → code later) | Runtime SoR? |
| --- | --- | --- |
| Requirements / QAS / RTM | `03-requirements/` | N/A |
| Constraints / OQs | `04-constraints/` | N/A |
| Ubiquitous language + BC map | `06-domain/` | N/A |
| C4 + ADR + ports/ICD | `07-system-design/` | N/A |
| Lock DSL / JSON Schema for locks | `07-system-design/icd/` → later `specs/` | **Policy SoR** (git) |
| Registry schema (SQL DDL) | `06-domain/information-model/` → engine migrations | **Derived** |
| SCIP protobuf / symbol IDs | External `scip` — we **consume** | Index SoR for symbols |
| Receipt / proof-tour JSON Schema | `08-verification/receipts/` | Verify artifact |
| MCP/LSP tool schemas | `07-system-design/icd/` + TS IDE Pilot | Interface |
| RAG chunk manifests | `10-rag-corpus/` | Retrieve only |
| Science metaphors | `11-science-transfer/` | Never merge SoT |

---

## 2. Theory, standards, frameworks — who leads vs who ships

### 2.1 Requirements & architecture method (pre-code law)

| Topic | Theory / standard | Leading entity | Where to look | Adoption / implementers |
| --- | --- | --- | --- | --- |
| RE document family | ISO/IEC/IEEE **29148** | ISO/IEC/IEEE | ISO store; INCOSE SE Handbook | Process standard — not a GitHub product |
| Quality in RE | ISO/IEC **25010** | ISO | ISO 25010:2023 | Characteristics vocabulary |
| Architecture tradeoffs | **ATAM** | **SEI / CMU** | sei.cmu.edu ATAM collection | Method; LLM-ATAM papers exist — **not** SoT |
| Decisions | **Nygard ADR** | Michael Nygard (blog/practice) | “Documenting architecture decisions” | Widely Adopted pattern; adr-tools etc. |
| Diagrams | **C4** | **Simon Brown** | [c4model.com](https://c4model.com/) | Structurizr / many renderers |
| Views classic | 4+1 (Kruchten) | Philippe Kruchten | IEEE Software 1995 | Background for MAAD etc. |

**Agent rule:** cite these for *form*. Do not invent Phi-pinned FRs and call it 29148.

### 2.2 Code intelligence & parsing (L1)

| Piece | Problem | Research / protocol lead | Shipping implementation (GitHub) | Stars* | Role here |
| --- | --- | --- | --- | --- | --- |
| **tree-sitter** | Incremental CST | Max Brunsfeld / tree-sitter org | [tree-sitter/tree-sitter](https://github.com/tree-sitter/tree-sitter) | ~26.6k | Grammar/CST foundation |
| **ast-grep** | Structural pattern search | ast-grep org (built on tree-sitter) | [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) | ~15.5k | Fast “shape fire” |
| **SCIP** | Precise cross-file symbols | Sourcegraph → **scip-code** | [scip-code/scip](https://github.com/scip-code/scip) | ~0.7k | Index format SoR |
| **scip-java** | JVM indexer | Sourcegraph / scip-code | [scip-code/scip-java](https://github.com/scip-code/scip-java) (~131★; active 2026-08) | niche but **production indexer** | Produce `index.scip` |
| **LSP** | Editor protocol | Microsoft + community | [microsoft/language-server-protocol](https://github.com/microsoft/language-server-protocol) | ~13.0k | Squiggle surface |
| **Glean** | Org-scale semantic facts | Meta (internal; public docs/talks) | Not a drop-in OSS clone | — | **Pattern only** — local SQLite is our small Glean |

\*Stars = popularity signal, **not** correctness. scip-java’s value is **compiler-backed indexing**, not star count.

### 2.3 Policy / modular boundaries (L2)

| Piece | Lead | GitHub | Stars* | Transfer |
| --- | --- | --- | --- | --- |
| **Packwerk** | Shopify | [Shopify/packwerk](https://github.com/Shopify/packwerk) | ~1.9k | **Adopt pattern** (packages, todo bankruptcy) — Refuse Ruby tip kernel |
| packs (Rust Packwerk-like) | community (e.g. alexevanczuk/packs) | see Packwerk README ecosystem | — | Optional Pilot later |
| MDC / Cursor rules | Cursor | cursor.com/docs/context/rules | — | Activation algebra for *this* corpus |

### 2.4 Graph / query brain (enrichment)

| Piece | Lead | GitHub | Stars* | Transfer |
| --- | --- | --- | --- | --- |
| **DataScript** | Nikita Prokopov (tonsky) | [tonsky/datascript](https://github.com/tonsky/datascript) | ~5.8k | In-memory Datalog **Pilot** — not merge SoT |
| **Babashka** | borkdude | [babashka/babashka](https://github.com/babashka/babashka) | ~4.6k | Ops binary / EDN queries Pilot |

### 2.5 Sandbox & proof (L3 — optional)

| Piece | Lead | GitHub | Stars* | Honest role |
| --- | --- | --- | --- | --- |
| **Wasmtime** | Bytecode Alliance | [bytecodealliance/wasmtime](https://github.com/bytecodealliance/wasmtime) | ~18.5k | Run WASM guests; **isolation ≠ proof** |
| **Extism** | Extism | [extism/extism](https://github.com/extism/extism) | ~5.7k | Friendlier plugin host over WASM |
| **Z3** | Microsoft Research | [Z3Prover/z3](https://github.com/Z3Prover/z3) | ~12.5k | SMT on **encoded** formulas only |
| **Kani** | model-checking / Amazon | [model-checking/kani](https://github.com/model-checking/kani) | ~3.3k | Model-check **Rust engine**, not Java beans |
| Iris / RustBelt | academic (Iris team) | papers + Coq | — | Language-level trust stories; Aria’26 agent+harness [2607.06341] |

### 2.6 Agent loop & CLI UX (enhancement)

| Piece | Lead | GitHub | Stars* | Transfer |
| --- | --- | --- | --- | --- |
| **SWE-agent** | Princeton / SWE-agent | [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) | ~20.0k | reason→act→verify→correct + ACI shape |
| **Cobra** | spf13 | [spf13/cobra](https://github.com/spf13/cobra) | ~44.4k | Go CLI chassis patterns |
| **Bubble Tea** | Charmbracelet | [charmbracelet/bubbletea](https://github.com/charmbracelet/bubbletea) | ~44.3k | TUI shape — Pilot UX |
| LanceDB | LanceDB | [lancedb/lancedb](https://github.com/lancedb/lancedb) | ~11.1k | Vectors — **RAG only**, never symbol SoR |

### 2.7 Science transfer (not tip)

Leaders: neuromorphic (Intel Loihi line), physical RC (photonic/soft-robot 2026 arXiv), Landauer/thermo (physics community).  
**Our locked transfers only** — see `11-science-transfer/locked-transfers/`.  
Papers pack: `research/papers-2026-may-aug/` (MAAD, observability, IMC, Landauer, PRC, Aria).

---

## 3. Mathematics that actually matters (honest)

| Math | Used for | MVP? | Abuse to refuse |
| --- | --- | --- | --- |
| **Graphs** (directed): nodes=beans/types/packages; edges=injects/imports/depends | Cycle detect, layer reachability | **Yes** | Pretending graph = running JVM |
| **Relations / Datalog-ish queries** | “Who injects X?”, lock queries | Pilot (DataScript) | Merge authority without deterministic engine |
| **Formal languages / parsing** (CFGs via tree-sitter) | CST extraction | **Yes** (via tools) | Hand-rolled parsers day one |
| **Type/symbol identity** (SCIP symbol strings) | Cross-file resolve | **Yes** | Embeddings cosine as identity |
| **SAT/SMT** (Z3) | Lock predicates as formulas | **No** (Phase 2+) | “Proved the Spring app” |
| **Model checking** (Kani) | Rust engine properties | When engine exists | Java Stage-0 |
| **Probability / concentration** | Flake language, eval variance | Sensors only | Probabilistic merge green |
| **Information theory / Landauer** | Cost/remeasure *language* | Metaphor | \(kT\ln 2\) CI floor |
| **Control / observability Gramians** | Sensor rate caps metaphor | Metaphor | Cover% PID |
| **Reservoir → linear readout** | climb/sensors → oracle readout analogy | Metaphor | Physical RC hardware |

**MVP math = graph algorithms + schemas + deterministic predicates.** Everything else is Pilot or metaphor.

---

## 4. Constraints (fixed for wave-1 unless ADR)

| ID | Constraint |
| --- | --- |
| C-LOCAL | Local-first; indexes derived on developer/CI machine |
| C-LOCKGIT | Locks live in git; do not sync Lance/SCIP blobs as team SoR |
| C-ORACLE1 | One deterministic gate/oracle writer at a time |
| C-UNK | Ambiguous DI → Unknown, never silent pick |
| C-RAG≠V | RAG/LLM text ∉ verify witnesses |
| C-WASM≠P | WASM = sandbox/trust-boundary engineering, not theorem |
| C-SCIP≠DI | SCIP ≠ Spring `@Primary`/`@Qualifier`/profiles runtime |
| C-NOCODE | No product codegen until DoR green |
| C-SCIENCE | Only locked E-DYN1 transfers enter product language |
| C-PLANT | Java 17/21 · Boot 3.2/3.3 envelope until reopened |

---

## 5. What implementation looks like (concrete, still Spec)

### Wave-0 — this repo (now)

Markdown under `00/`–`12/`: RE, QAS, constraints, ports, schemas as **design**.

### Wave-1 MVP (first valuable product)

**Ship:** CLI `fitness_check` / `verify` that:

1. Reads lock files + optional `index.scip`
2. Builds/updates **SQLite** registry (beans/edges) — DDL in information-model
3. Resolves injection sites → edge or **Unknown**
4. Runs cycle + layer LockCheck
5. Writes **receipt JSON** (proof tour v0: lock id, edge id, file:line)
6. Exit nonzero on Must violations

**Stack Pilot order:** external scip-java → Rust (or thin host) decode/resolve/check → SQLite → receipts.  
Go watch, bb graph, WASM guest, TS LSP = **not** MVP blockers.

### Wave-2

LSP squiggles (same LockCheck), lock sync via git only, proof-tour UI panel.

### Wave-3

Ghost prefetch, polyglot bell (explicit bridge facts / OpenAPI), optional Z3 on lock formulas, optional WASM sandbox packaging.

---

## 6. MVP phase order (logical build)

| Phase | Outcome | Exit criterion |
| --- | --- | --- |
| **P0 Spec** | Boundary, QAS, SoR matrix, ports, receipt schema, OQs closed | DoR green + human Approve |
| **P1 Index ingest** | Consume `index.scip` + annotation scan → SQLite | Query: list beans for type X |
| **P2 Resolve** | injection_point → bean \| Unknown | Multi-impl without qualifier → Unknown |
| **P3 Locks** | Package/layer/cycle rules on graph | Fixture plant fails controller→repo |
| **P4 Receipts** | Stable step IDs; CLI prints path | Missing witness → fail |
| **P5 ACI** | Agent/human same CLI | SWE-agent-style loop uses verify tool |
| **P6 LSP** | publishDiagnostics | Human edit same violation ID |
| **P7 Enrichment** | Go watch, bb queries, WASM package | Keep/drop per Spike |
| **P8 Proof+/polyglot** | Z3/Kani/cross-lang | Separate Approves |

---

## 7. Why these choices are good (and where they land today)

| Choice | Good because | Lands today | Gap to accomplish |
| --- | --- | --- | --- |
| Tool over SaaS | Privacy, offline, git locks | Vision draft in STATUS | OQ-01 Accept |
| Graph+locks before SMT/LLM | Deterministic Accept; high ROI | Described in research memos | DDL + lock IR + plants |
| SQLite derived registry | Hermetic, CTE-friendly, local | ADR-0002 Proposed | Schema file + migrations design |
| SCIP consume | Real symbol identity at scale | Named external | Plant indexing runbook |
| Packwerk pattern | Battle-tested modular monorepo UX | Research + ADR-0003 | Executable lock IR |
| Monorepo later | Version alignment | Folders `07/options` | No Cargo yet — correct |
| Refuse embeddings-as-SoR | Stars≠truth; LanceDB ≠ SCIP | Critique memos | Keep in constraints |
| Polyglot as Pilot lanes | Steal UX without tip thrash | nests/ legacy + options/ | OQ-08 wave-1 BC set |

---

## 8. Fluff to stop writing (rewrite rule)

| Fluff pattern | Rewrite to |
| --- | --- |
| “Use latest frameworks” | Name repo + version pin + Accept predicate |
| “AI-powered architecture” | Agent loop + **deterministic** verify tool |
| Bare “≤2s latency” | Six-part QAS with measure |
| “Proved via WASM” | trust-boundary + optional formal ticket |
| Nine-language monorepo ASCII | options/ + Pilot order table |
| Star-count as correctness | Adoption signal only; plants decide |

---

## 9. Bloom Create tickets

| ID | Acceptance |
| --- | --- |
| **ARCH-1** | This brief Approved or explicitly Draft-wave |
| **ARCH-2** | `01-vision/problem-frame/BOUNDARY.md` matches §0 |
| **ARCH-3** | SoR matrix file exists (`08-verification/sor-derived-matrix.md`) |
| **ARCH-4** | Ports stub + ICD list committed |
| **ARCH-5** | Receipt JSON Schema draft committed |
| **ARCH-6** | MVP phases mirrored in `12-delivery/waves/` |

**Implement still Refuse** until DoR green.
