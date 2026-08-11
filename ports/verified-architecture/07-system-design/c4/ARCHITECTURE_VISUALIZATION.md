---
title: Architecture visualization — Draft system design (not Implement-ready)
status: DRAFT — shape sensor only
date: '2026-08-11'
accepted: false
look_first:
  - ../ARCHITECTURE_BRIEF.md
  - C4-BRIEF-CONFIDENCE.md
  - ../../08-verification/VERIFY_STACK.md
  - ../../08-verification/sor-derived-matrix.md
  - ../../01-vision/problem-frame/BOUNDARY.md
  - ../../docs/adr/adr-0004-native-then-wasm-lockcheck.md
  - ../../docs/adr/adr-0011-mcp-protocol-and-tool-surface.md
freeze_class: sensor
doc_role: architecture-diagram
---

# Architecture visualization (Draft)

**Banner:** Definition of Ready has **zero** PASS rows. These diagrams are
**shape confidence**, not permission to open product crates. Scores and boxes
do not equal Implement readiness (~0.15).

Whole words — root `GLOSSARY.md`. Companion ASCII: `C4-BRIEF-CONFIDENCE.md`.
Poster: `verified-architecture-system-design-draft.png`.

---

## 1. Context — who talks to what

```mermaid
flowchart LR
  subgraph People["People and agents"]
    Dev["Developer / coding agent<br/>proposes only"]
  end

  subgraph Target["Target git repository"]
    Src["Sources"]
    Locks["Policy locks in git<br/>System of Record"]
    Scip["index.scip<br/>Index System of Record"]
  end

  subgraph Product["Verified Architecture product local"]
    Engine["Rust engine<br/>decide + write oracles"]
    Present["TypeScript presentation<br/>Model Context Protocol / IDE"]
  end

  Host["Optional IDE / remote host<br/>Model Context Protocol 2026-07-28"]

  Dev -->|command-line or tools| Present
  Dev -->|command-line or tools| Engine
  Host -->|Streamable HTTP session-free| Present
  Present -->|typed tool calls| Engine
  Engine -->|read| Src
  Engine -->|read| Locks
  Engine -->|read| Scip
  Engine -->|write derived only| Engine
```

**Out of minimum viable product:** org SaaS / Backstage mesh. **Refuse:** Python
as engine or specification-corpus host.

---

## 2. Containers — Wave-1 vs later Could

Solid boxes = Wave-1 **intent** (still Pilot / Draft). Dashed = Could / refused.

```mermaid
flowchart TB
  User["Operator / developer / continuous integration"]

  subgraph Wave1["Wave-1 intent"]
    Eng["Engine — Rust<br/>decode · resolve · LockCheck · receipts · claim memory"]
    Reg[("Registry — SQLite<br/>derived graph")]
    Ide["IDE presentation — TypeScript<br/>diagnostics + Model Context Protocol UI"]
    SpecMcp["Specification corpus server — Rust<br/>read-only Spike — not verify oracle"]
  end

  subgraph CouldLater["Could / later waves"]
    Wasm["LockCheck guest — WebAssembly<br/>Wave-3 parity with native"]
    Go["Watch / reindex chassis — Go"]
    Ruby["Lock authoring DX — Ruby"]
    Clj["Graph query brain — Clojure"]
  end

  Plant["Target repo + indexer<br/>sources · locks · index.scip"]

  User --> Ide
  User --> Eng
  User --> SpecMcp
  Ide --> Eng
  Eng --> Reg
  Eng --> Plant
  Eng -.->|optional later| Wasm
  Go -.->|triggers only| Eng
  Ruby -.->|lock Intermediate Representation| Eng
  Eng -.->|export| Clj

  style Wasm stroke-dasharray: 5 5
  style Go stroke-dasharray: 5 5
  style Ruby stroke-dasharray: 5 5
  style Clj stroke-dasharray: 5 5
```

---

## 3. Inside the engine — verify pipeline

Corrected “Agent operating-system” flow: global map → local truth → **native**
spine → atomic write. WebAssembly is not the spine.

```mermaid
flowchart TB
  Intent["Global intent<br/>question or proposed change"]

  SCIP["Source Code Index Protocol<br/>global candidate map"]
  Local["Structural search / parse<br/>local truth on shortlisted files"]
  Graph["Derived registry graph"]
  Lock["Native Rust LockCheck<br/>policy System of Record"]
  Claim["Claim memory<br/>anchors · freshness · unprovable"]
  Receipt["Receipt writer<br/>freshness bindings · no model text as witness"]
  Write["Rust atomic / hash-guarded effects<br/>derived store or accepted mutation path"]

  WasmOpt["WebAssembly LockCheck guest<br/>Could Wave-3 only"]

  Intent --> SCIP
  SCIP --> Local
  Local --> Graph
  Graph --> Lock
  Lock --> Claim
  Claim --> Receipt
  Receipt --> Write
  Lock -.-> WasmOpt
```

| Step | Job | Fail-mode if skipped or inverted |
| --- | --- | --- |
| Index map | Scale lookup | Structural search over the whole tree every turn |
| Local truth | Citation-grade check of current bytes | Trust stale index alone |
| Native LockCheck | Policy decide | Putting WebAssembly here as Must spine |
| Claim memory | Survive upstream edits | Stale “green” docs/answers |
| Receipt | Grounding gap toward zero | Model prose as proof |
| Atomic write | Engine owns effects | Model writes oracles / free shell |

---

## 4. Dual Model Context Protocol surfaces

Do not merge these into one mega-tool list.

```mermaid
flowchart LR
  Agent["Coding agent / host"]

  subgraph SurfaceA["Surface A — product verify Draft"]
    A1["snapshot_open"]
    A2["verify · resolve"]
    A3["claim_withdraw · locks_list"]
    RustA["Rust engine effects"]
    A1 --> RustA
    A2 --> RustA
    A3 --> RustA
  end

  subgraph SurfaceB["Surface B — specification corpus Spike"]
    B1["spec_status · spec_gap · …"]
    RustB["Rust read-only host"]
    B1 --> RustB
  end

  TS["TypeScript presentation only"]

  Agent --> TS
  TS --> SurfaceA
  Agent --> SurfaceB
```

Wire pin: Model Context Protocol **2026-07-28** (session-free; handles as
arguments). Tool *semantics* remain Pilot invent until Accept.

---

## 5. System of Record versus derived

```mermaid
flowchart TB
  subgraph SoR["Systems of Record"]
    Sources["Target sources — developers"]
    Policy["Locks / pack manifests — architects via git"]
    Index["index.scip — indexer job"]
  end

  subgraph Derived["Derived — Rust engine only"]
    Reg2["SQLite registry / graph"]
    Claims["Claim store"]
    Rcpt["Proof-carrying receipts"]
  end

  subgraph NeverVerify["Never verify witnesses"]
    Rag["Retrieval embeddings / assist text"]
    Llm["Model remediation prose"]
  end

  Sources --> Reg2
  Index --> Reg2
  Policy --> Reg2
  Reg2 --> Claims
  Reg2 --> Rcpt
  Rag -.->|forbidden edge| Rcpt
  Llm -.->|forbidden edge| Rcpt
```

---

## 6. Stakeholder grounded-doc pressure (not Accepted)

Discovery metrics (index lag, stale fragments, grounding gap) reinforce Fresh +
claims. A thin filesystem tool stack (read / ripgrep / tree / apply-diff / wiki)
is **Could adapter** until open question on product boundary is Accepted — it
does **not** replace the diagram in §3.

```mermaid
flowchart LR
  Pain["Brownfield stale docs<br/>authors gone"]
  Gap["Grounding gap → 0"]
  Spine["§3 verify spine"]
  Fs["Filesystem / wiki tools<br/>Could only"]

  Pain --> Gap
  Gap --> Spine
  Fs -.->|not Wave-1 replacement| Spine
```

---

## 7. How to read this pack

| Document | Use |
| --- | --- |
| This file | Mermaid overview |
| `C4-BRIEF-CONFIDENCE.md` | ASCII + shape confidence scores |
| `ARCHITECTURE_BRIEF.md` | Decisions table + topology prose |
| `docs/c4/02-containers.md` | Polyglot container C4 |
| `VERIFY_STACK.md` | Four Must-intent legs |
| `STATUS.md` | FREEZE + Implement Refuse |

**Human still owns:** product-boundary Accept (Q1–Q4 in stakeholder discovery
memo) and Wave-0 signoff. Diagrams do not close those.
