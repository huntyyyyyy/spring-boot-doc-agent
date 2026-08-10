---
title: E-LIE0 — Local-first verified architecture agent (Layers of Truth)
status: RESEARCH COMPLETE — Spec Draft (no kernel rewrite until Approve)
date: 2026-08-10
epic: E-LIE0
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
related:
  - docs/research/process/48-complete-toolscape-agent-repo-developer-2026-08-10.md
  - docs/research/process/40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md
  - docs/research/process/49-markdown-frontmatter-metadata-schemas-2026-08-10.md
  - docs/research/process/51-e-lie0-adversarial-ddia-solid-polyglot-slate-2026-08-10.md
  - docs/research/process/52-verified-slice-re-master-adversarial-critique-2026-08-10.md
  - docs/design/e-lie0-requirements-2026-08-10.md
  - docs/research/inbound/verified-slice-re-master-v0.5.1-draft.md
  - docs/research/stage0/d1-query-agent-retrieval-bc-research-2026-08-10.md
  - docs/research/stage0/d2-d3-certification-fact-stores-bc-research-2026-08-10.md
  - docs/research/quality-backlog.md
  - .cursor/rules/se-quality-constitution.mdc
do_not:
  - Dual-write coverage.xml from a second kernel
  - Claim SCIP alone resolves Spring @Primary/@Qualifier/profiles
  - Equate WASM with mathematical proof (Z3/Kani are proof; WASM is sandbox)
  - Mass Cargo/Go/Clojure tip rewrite without Pilot keep/drop
  - Treat Duck.ai chat as Evidenced SoT — inspiration only
  - Treat this memo as SRS — cite docs/design/e-lie0-requirements-*.md for REQ-*

sources:
  github:
    - https://github.com/sourcegraph/scip-java
    - https://github.com/scip-code/scip
    - https://github.com/tree-sitter/tree-sitter
    - https://github.com/princeton-nlp/SWE-agent
    - https://github.com/Z3Prover/z3
    - https://github.com/model-checking/kani
  deepwiki_ask:
    - github/docs · quarto-dev/quarto-cli (prior sessions; FM/locks patterns)
  web:
    - duck.ai Gemma transcript 2026-08-10 (inspiration — Unknown tier)
  mcp: https://mcp.deepwiki.com/mcp
---

# E-LIE0 — Local-first verified Spring / architecture agent

**Product today:** Python `doc-engine` + Stage-0 ast-grep + claims/MDC + gates.  
**Ambition:** glue **SCIP → local SCM → graph verify → (optional) SMT**, with
Python (then Rust hot paths) as ACI — more precise than chat-only agents, more
flexible than a pure verifier.

**Method note.** Shape inspired by a Duck.ai / Gemma exploration
(`[Unknown — chat]`); corrected against this repo’s constitution and prior
polyglot memos. **No Refuse-by-default** — Pilot-before-cutover.

---

## 0. One-page verdict

| Layer | Question | Tools | Merge SoT? |
| --- | --- | --- | --- |
| **L1 Where** | Where is it? What shape? Who refs it? | ast-grep (fast) · tree-sitter · **SCIP** | Index SoR (sensor) |
| **L1b Wire** | Which bean binds here? | Annotation registry + SCIP types + **Spring resolve** | Graph SoR (sensor→gate) |
| **L2 How** | Is this change allowed? | `.mdc` / locks · claims · E-MD0 FM | **Policy SoT** |
| **L3 Proof** | Can we refute a property? | Z3 / Kani (Rust) · CodeQL queries | Optional proof SoR |
| **Sandbox** | Where does untrusted check run? | **WASM** (validator harness) | Not a prover |

**v1 Accept (pragmatic):** virtual Spring/dep **graph** + lock checks + proof-tour
receipts. **Defer** full Z3 bean “proofs.” Keep Python tip until Explicit cutover.

**Requirements SoR:**
[`docs/design/e-lie0-requirements-2026-08-10.md`](../../design/e-lie0-requirements-2026-08-10.md)
(StRS / MoSCoW SRS / RTM). Tours below are product sketches; **Must** capabilities
are only those tagged Must in the RE package (`REQ-F-01…09`, `REQ-N-01…03/05/06`).

---

## 0b. Bloom ladder

| Level | Evidence |
| --- | --- |
| **1 Remember** | scip-java, tree-sitter, SWE-agent ACI, Z3, Kani, LanceDB, Glean-as-pattern |
| **2 Understand** | Spring DI ≠ Java symbols; WASM ≠ SMT; sg is fast path inside L1 |
| **3 Apply** | Pilot: `scip-java index` on kitchen/OCS → SQLite registry → cycle/layer gate |
| **4 Analyze** | Embody wheels/sg; Pilot Rust analyzer + SCIP; Pattern SWE-agent loop; Defer Z3 |
| **5 Evaluate** | §6 adversarial |
| **6 Create** | LIE0 tickets below — Implement blocked until Approve |

---

## 1. Layers of Truth (pyramid)

### L1 — Where (navigation / retrieval)

- **ast-grep:** high-speed filter, Stage-0 fire, lock patterns that are pure shape.  
- **tree-sitter:** CST for large Java; prune to semantic summaries (methods + annotations).  
- **SCIP:** defs/refs/impls across huge trees — “exactly where is this symbol?”

**If removed:** agent is blind / keyword-RAG only.

### L1b — Wire (virtual Spring graph) `[Confirmed gap today]`

sg finds `@Service` / `@Autowired`; it does **not** answer “bean for
`UserService` is `UserServiceImpl` under these qualifiers.”

Static model (not a JVM):

1. Annotation scan → bean registry (SQLite)  
2. Injection sites → SCIP **requested type**  
3. Resolve (Rust/Python): impls ∩ stereotypes ∩ `@Primary`/`@Qualifier`/`@Bean`  
4. Edges → **virtual dependency graph** (Unknown when ambiguous)

SCIP is **substrate**; Spring resolve is **extra**.

### L2 — How (intent / policy)

Locks / `.mdc`: e.g. controllers call services, not repositories. Same rules for
**AI and humans** (LSP red squiggle). Git is lock SoR; engines sync locks, **not**
the vector/SCIP blob.

### L3 — Proof (optional)

- **Z3:** counterexamples on **encoded** FOL (business invariants).  
- **Kani:** model-check **Rust** engine code.  
- **CodeQL:** query-as-existence proof for vuln/pattern classes.  

WASM runs the **translator/validator** in a sandbox; it does **not** prove beans.

### Synergy loop

`Discovery (sg/SCIP)` → `Reason (LLM)` → `Act (ACI/edit)` →  
`Verify (graph + locks [+ SMT])` → `Correct` → **Proof tour** receipt.

---

## 2. Bells (product tours)

| Tour | Intent |
| --- | --- |
| **Proof tour** | Clickable steps: lock → graph edge → snippet → formula |
| **Ghost prefetch** | Cursor predicts files; preload AST/SCIP/locks; Cmd+K feels instant |
| **Red squiggle** | LSP runs same locks on human typing |
| **Lock sync** | `.mdc` in git; teammates’ engines refresh rules only |
| **Polyglot bell** | Cross-lang SCIP/bridges (Java API ↔ TS fetch); “what breaks FE?” |

---

## 3. Moats (pillar gap)

| Pillar | Has | Lacks |
| --- | --- | --- |
| Sourcegraph/SCIP | Index | Local-first agent + locks loop |
| SWE-agent / Devin-likes | Reason→act loop | Local SCM + formal/structural locks |
| CodeQL / Kani / Z3 | Proof/query | Agent + Spring graph ACI |
| Ollama / LanceDB | Local model/vectors | AST/SCIP truth |

**Glue:** local SCIP/SCM + virtual Spring graph + living locks + explainable verify
(+ optional SMT). Working name: **local-first verified architecture agent**.

---

## 4. Repo shape (target — not tip thrash)

Inspired by local-intelligence-engine sketches; map onto **this** monorepo later:

| Dir | Role | Language |
| --- | --- | --- |
| `core-engine/` / `java-analyzer` | Parse, registry, resolve, graph checks | Rust Pilot |
| `wasm-runtime/` | Sandboxed validator | Rust→WASM |
| `ai-orchestrator/` | CLI/ACI/MCP/RAG | **Python tip today** |
| `specs/` / `.cursor/rules` | Locks | MDC + schemas |
| `plugins/` | Optional Go daemon / Clojure graph | Pilot |

Python remains `coverage.xml` / claims writer until **named cutover Approve**.

---

## 5. Embody / Pilot / Defer

| Item | Stance |
| --- | --- |
| Keep Stage-0 ast-grep + Python tip | **Embody** |
| scip-java → SQLite registry + resolve + cycle/layer gate | **Pilot now** |
| Proof-tour JSON receipts | **Pilot now** |
| PyO3 / Rust crate for hot parse | **Pilot** after hotspot measure |
| WASM validator harness | **Pilot** with graph checks (not SMT) |
| LSP red squiggles | **Pilot later** |
| Ghost prefetch + LanceDB | **Pilot later** |
| Z3 business FOL | **Defer** until locks are formulas |
| Kani on Rust engine | **Defer** until Rust owns hot path |
| Replace tip kernel with Rust daemon | **Approve-gated cutover only** |

---

## 6. Adversarial

| Failure | Mitigation |
| --- | --- |
| SCIP sold as Spring DI | L1b resolve + Unknown |
| WASM sold as proof | Docs + gate naming |
| Dual Cover% | Constitution; one oracle path |
| Hallucinated “verified” | Proof tour requires witness IDs or fail |
| Index sync via git | Locks only; rebuild SCIP locally |

---

## 7. Create — tickets (Approve before Implement)

Prereq: RE package Approve (`REQ-*`) + ADV-1…3 from process/51. Each ticket
traces to RTM rows in the RE file.

| ID | Ticket | REQ trace | Acceptance |
| --- | --- | --- | --- |
| **LIE0-1** | Design Spec seam map (modules ≤225) | F-01…09, F-19 | Ports: Index, Registry, Resolve, LockCheck, Receipt |
| **LIE0-2** | Spike: scip-java on kitchen/OCS | F-10, N-04 | `index.scip` + symbol counts receipt |
| **LIE0-3** | Bean registry + ctor/`@Autowired` resolve | F-01, F-02, F-07 | Query: bean for type X → impl or Unknown |
| **LIE0-4** | Cycle + layer-lock check | F-03…05, F-11 | Catches controller→repo / A→B→A before merge |
| **LIE0-5** | Proof-tour schema | F-06, F-13 | Steps clickable in markdown/JSON |
| **LIE0-6** | Optional WASM wrap of LockCheck | F-16 Could | Same Accept as in-process |
| **LIE0-7** | LSP squiggle Spike | F-12 Should | One lock live in editor |
| **LIE0-8** | Polyglot bell Spike | F-15 Could | One Java↔TS bridge via OpenAPI or dual SCIP |

---

## 8. Status

Research **Complete** through Bloom Create (Spec Draft) + **RE draft**.  
**Do not** start Cargo monorepo or tip kernel swap until RE **Approve**,
ADV-1…3, Design Spec Approve, and Active tip allows (after E-COH1 / reorder).

