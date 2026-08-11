---
title: E-LIE0 / E-POLY — Full polyglot product portfolio (Rust · WASM · SQLite · Go · Ruby · Clojure · TS · C · Zig)
status: RESEARCH COMPLETE — Spec Draft PRODUCT STANCE (user-directed; amends “sidecar-only” framing)
date: '2026-08-10'
epic: E-LIE0
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
related:
  - docs/design/e-lie0-requirements-2026-08-10.md
  - docs/design/adr/README.md
  - docs/design/adr/adr-006-polyglot-first-monorepo.md
  - docs/research/process/40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md
  - docs/research/process/41-language-excellence-domains-subdomains-2026-08-10.md
  - docs/research/process/48-complete-toolscape-agent-repo-developer-2026-08-10.md
  - docs/research/process/50-local-first-verified-architecture-agent-2026-08-10.md
  - docs/research/process/53-e-lie0-pilot-mental-models-polyglot-lanes-2026-08-10.md
  - docs/research/process/54-e-lie0-atam-qas-adr-formal-boundaries-2026-08-10.md
  - docs/research/quality-backlog.md
do_not:
  - Water this down to “Python tip + optional demos”
  - Dual-write coverage.xml from two languages without cutover ADR
  - Skip QAS/ADR gates from process/54 when picking toolkits
  - Equate “full polyglot” with unproven formal claims on every crate
sources:
  github:
    - https://github.com/bytecodealliance/wasmtime
    - https://github.com/bytecodealliance/wit-bindgen
    - https://github.com/extism/extism
    - https://github.com/Shopify/packwerk
    - https://github.com/alexevanczuk/packs
    - https://github.com/babashka/babashka
    - https://github.com/tonsky/datascript
    - https://github.com/spf13/cobra
    - https://github.com/tetratelabs/wazero
    - https://github.com/ziglang/zig
    - https://github.com/verus-lang/verus
  web:
    - https://component-model.bytecodealliance.org/
  mcp: https://mcp.deepwiki.com/mcp
last_reviewed: '2026-08-10'
---

# Full polyglot product portfolio — user stance locked

**Directive (2026-08-10).** The product is **not** “Python with cool sidecars.”
It is a **polyglot local-first verified architecture engine** that **fully uses**:

**Rust · WASM (+ Rust/WASM toolkits) · SQLite · Go · Ruby · Clojure · Python ·
TypeScript (as needed) · C (when necessary) · Zig (when it earns a seat).**

Earlier agent framing that demoted languages to Pattern-only or “optional after
Python Must” is **amended**. process/53 lanes stay as *mental models*; this memo
is the **product identity**. process/54 QAS/ADR/formal gates still bind — full
polyglot does **not** mean vibes or dual Cover%.

---

## 0. Bloom

| Level | Evidence |
| --- | --- |
| **1** | Logos from process/41 + toolkit list §3 |
| **2** | Each language owns a *first-class* BC, not a demo folder |
| **3** | Monorepo layout + build matrix + Pilot order |
| **4** | Transitional oracle writer vs cutover; Zig/C when earned |
| **5** | Adversarial: supply-chain, dual SoT, formal overclaim |
| **6** | POLY-FULL tickets + ADR-006 |

---

## 1. One-page verdict

| Question | Answer |
| --- | --- |
| Is the product polyglot? | **Yes — by design** |
| Where does it live? | **This monorepo** (not a greenfield abandon of kitchen/OCS) |
| Can Rust own the engine? | **Yes** — first-class `crates/` / engine BC |
| WASM? | **Yes** — guests + hosts + WIT/component model + Extism/wazero as needed |
| Ruby / Clojure? | **Yes** — real lock DSL / graph brain BCs, not “pattern essays” |
| Go? | **Yes** — daemon/chassis BC |
| SQLite? | **Yes** — registry SoR-derived (ADR-001) |
| Python / TS? | **Yes** — ACI, gates, IDE/MCP/LSP as needed |
| C / Zig? | **Yes when needed** — grammars, amalgamation, systems/WASM niches |
| Merge oracle today? | **Single writer** until **cutover ADR** (may move; not forever-Python) |

---

## 2. Bounded contexts by language (first-class)

```text
crates/lie0-*          Rust     engine: parse, SCIP decode, resolve, lock IR, receipts
                       + host for WASM; optional Verus/Kani on pure cores
wasm/ / guests/        WASM     LockCheck & untrusted packs (capability boundary)
go/lie0d/              Go       watch / reindex / plugin chassis (Cobra)
ruby/locks/            Ruby     Packwerk-compatible or Packwerk-shaped DSL tooling
                               (packs Rust impl may assist — still Ruby UX)
clj/ / bb/             Clojure  Datascript/XTDB-style graph REPL & query services
sqlite/                SQL      schema + migrations (owned; accessed via rusqlite etc.)
src/doc_engine/        Python   transitional ACI, Stage-0, claims, coverage writer
extensions/ / mcp/     TS       IDE panel, LSP client glue, MCP Streamable HTTP UI
native/ / c/           C        tree-sitter grammars, sqlite amalgamation, FFI edges
zig/ (opt)             Zig      alternate WASM/systems toolkit when Spike keeps it
```

**Doctrine.** Languages are **peers with roles**, not guests of Python. Python is
the **current** oracle/ACI host, not the product ceiling.

---

## 3. Toolkit portfolio (intentional, not laundry)

### 3.1 Rust (engine + hosts)

| Toolkit | Role |
| --- | --- |
| rustc / Cargo workspace | Engine monorepo |
| tree-sitter (+ java grammar) | CST summaries |
| scip / protobuf crates | Decode `index.scip` |
| rusqlite | Registry access |
| clap or equivalent | Engine CLI |
| tokio | Async where earned |
| PyO3 / maturin | Bridge to Python ACI during transition |
| wasmtime (host) | Embed WASM guests |
| wit-bindgen / component model | Typed WASM interfaces |
| Miri / Clippy / rust-analyzer | Dev quality |
| Kani / Verus | Pilot-later on pure resolve/lock cores (process/54 FML) |

### 3.2 WASM (+ multi-host toolkits)

| Toolkit | Role |
| --- | --- |
| wasmtime | Primary host (fuel/epoch) |
| Extism | Multi-lang PDK plugins if useful |
| wazero | Go-side WASM host (daemon sandboxes) |
| wit / component model | Capability interfaces |
| wasm-bindgen / javy (opt) | JS/TS guest experiments |
| Wasmer / WasmEdge | Spike only if wasmtime gaps |

### 3.3 SQLite

| Piece | Role |
| --- | --- |
| SQLite engine | Derived bean/edge registry |
| SQL migrations | Versioned schema |
| rusqlite / Go database/sql / Python sqlite3 | Language bindings — **one schema SoR** |

### 3.4 Go

| Toolkit | Role |
| --- | --- |
| Cobra | `lie0d` CLI/daemon |
| fsnotify | Watch → reindex |
| go-plugin / hashicorp | Optional language sidecars |
| wazero | In-process WASM from Go |

### 3.5 Ruby

| Toolkit | Role |
| --- | --- |
| Packwerk and/or packwerk-extensions | Real package boundary UX |
| packs (Rust impl of Packwerk) | Fast checker option — Spike |
| Thor / RuboCop (opt) | Lock repo DX |

### 3.6 Clojure

| Toolkit | Role |
| --- | --- |
| Babashka + Datascript | Fast script graph REPL |
| Full Clojure JVM (when long-running) | Persistent query service if Spike keeps |
| Malli / Spec | Contract on EDN exports |
| Noumenon / XTDB | Watch / Pattern — not required for v1 green |

### 3.7 Python

| Toolkit | Role |
| --- | --- |
| doc-engine ACI | Orchestration, Stage-0, claims |
| pytest / pre_pr / coverage | **Current** merge oracle writer |
| PyO3 consumers | Call Rust engine |

### 3.8 TypeScript

| Toolkit | Role |
| --- | --- |
| LSP / VS Code or Cursor extension | Red squiggle + verification panel |
| MCP TS SDK patterns | Org-wide / IDE MCP clients |
| Node only as **extension host**, not tip Cover% writer |

### 3.9 C (when crazy is required)

| Use | Why C |
| --- | --- |
| tree-sitter grammar / parser cores | Ecosystem reality |
| SQLite amalgamation / custom VFS | Extreme embed control |
| FFI shims | When Rust/Zig/Go need a stable C ABI |

### 3.10 Zig (earned seat)

| Use | Why Zig |
| --- | --- |
| Alternate WASM/systems toolkit | Simpler cross-compile / C-interop story |
| Native helpers | When Spike shows better fit than C/Rust for a shim |

**Keep/drop rule.** Zig/C enter via Spike with QAS; they are **in the portfolio**,
not forbidden — but not cargo-culted onto the tip without Accept.

---

## 4. Constraints that still bind (not anti-polyglot)

| ID | Constraint |
| --- | --- |
| CON-ORACLE | Exactly **one** merge writer for `coverage.xml` / claims at a time |
| CON-QAS | NFRs → ATAM QAS before Design (process/54) |
| CON-ADR | Language BC additions need ADR (see ADR-006) |
| CON-SIZE | New modules respect LOC/complexipy culture (cohesive crates OK) |
| CON-PLANT | Kitchen/OCS remain Accept plants |

Polyglot **is** the product. These constraints keep it shippable.

---

## 5. Cutover roadmap (oracle)

| Phase | Oracle writer | Engine |
| --- | --- | --- |
| **Now** | Python | Spikes: Rust crates + Go daemon + Ruby locks + bb + WASM guest |
| **Pilot green** | Python | Rust engine called via PyO3/CLI; parity tests |
| **Cutover (Approve)** | New ADR supersedes ADR-005 | Rust (or designated) writes oracle **or** Python remains thin façade over Rust |

User intent: **do not stall** Rust/WASM/Go/Ruby/Clojure waiting for eternal
Python ownership ideology.

---

## 6. Create — POLY-FULL tickets

| ID | Ticket | Acceptance |
| --- | --- | --- |
| **PF-0** | ADR-006 Accepted (product = polyglot monorepo) | Stakeholder Accept |
| **PF-1** | Cargo workspace skeleton `crates/lie0-*` | Builds in CI job (non-oracle) |
| **PF-2** | Go `lie0d` Cobra skeleton + watch Spike | Stamp file updates |
| **PF-3** | Ruby lock package project (Packwerk-shaped or Packwerk) | controller→repo demo |
| **PF-4** | Clojure/bb Datascript REPL on EDN export | 3 queries = SQL goldens |
| **PF-5** | WASM LockCheck guest + wasmtime host | Parity vs native |
| **PF-6** | SQLite schema crate + rusqlite | Migrations + kitchen load |
| **PF-7** | TS extension Spike (diagnostics panel) | One lock visible in IDE |
| **PF-8** | C/Zig Spike backlog | Only when PF-1/5 need ABI/grammar |
| **PF-9** | CI matrix: rust / go / ruby / bb / wasm **without** dual Cover% | Separate jobs; oracle still single |

---

## 7. Status

**Product stance:** full polyglot — **locked per user direction**.  
**Method stance:** QAS + ADR + honest formal boundaries (process/54) — **unchanged**.  
**Implement:** still behind RE Approve + Active tip reorder; PF-* are the Pilot
shape once Active.
