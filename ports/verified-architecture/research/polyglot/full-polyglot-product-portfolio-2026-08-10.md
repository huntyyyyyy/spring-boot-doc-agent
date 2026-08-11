---
title: VA / E-POLY — Full polyglot product portfolio (Rust · WebAssembly · SQLite · Go · Ruby · Clojure · TS · C · Zig)
status: RESEARCH COMPLETE — Spec Draft PRODUCT STANCE; **amended 2026-08-11 — Refuse Python runtime**
date: '2026-08-10'
last_reviewed: '2026-08-11'
epic: VA
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
related:
  - docs/requirements/
  - docs/adr/README.md
  - docs/adr/adr-0001-polyglot-first-product.md
  - research/polyglot/
  - research/mdc-devex/
  - research/polyglot/pilot-mental-models-polyglot-lanes-2026-08-10.md
  - research/atam-formal/atam-qas-adr-formal-boundaries-2026-08-10.md
do_not:
  - Revive Python ACI / Spec host / tip convenience for this port
  - Water this down to “Python tip + optional demos”
  - Dual-write coverage.xml from two languages without cutover Architecture Decision Record
  - Skip Quality Attribute Scenario/Architecture Decision Record gates from process/54 when picking toolkits
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
---

# Full polyglot product portfolio — user stance locked

**Historical / evidence — not product SoT.** Older layout / PyO3-transition
sections below are evidence of prior framing only.

**Directive (2026-08-11).** **Refuse Python** as Spec host, ACI nest, oracle
writer, or default PyO3 bridge for this port (Architecture Decision Record
ADR-0001 amended). Follow ADR-0001 + `portfolio-summary.md` + nest 08 tombstone.
**Rust** Spec host; WebAssembly **Could** (sandbox, not proof).

**Directive (2026-08-10).** The product is **not** “Python with cool sidecars.”
It is a **polyglot local-first verified architecture engine** that **fully uses**:

**Rust · WebAssembly (+ Rust/WebAssembly toolkits) · SQLite · Go · Ruby · Clojure ·
TypeScript · C (when necessary) · Zig (when it earns a seat).** **Not Python.**

Earlier agent framing that demoted languages to Pattern-only or kept a Python
Must/peer is **amended**. process/53 lanes stay as *mental models*; this memo
is the **product identity**. process/54 Quality Attribute Scenario/Architecture Decision Record/formal gates still bind — full
polyglot does **not** mean vibes or dual Cover%.

---

## 0. Bloom

| Level | Evidence |
| --- | --- |
| **1** | Logos from process/41 + toolkit list §3 |
| **2** | Each language owns a *first-class* bounded context, not a demo folder |
| **3** | Monorepo layout + build matrix + Pilot order |
| **4** | Transitional oracle writer vs cutover; Zig/C when earned |
| **5** | Adversarial: supply-chain, dual Source of Truth, formal overclaim |
| **6** | POLY-FULL tickets + Architecture Decision Record ADR-0001 |

---

## 1. One-page verdict

| Question | Answer |
| --- | --- |
| Is the product polyglot? | **Yes — by design** |
| Where does it live? | **This monorepo** (not a greenfield abandon of corpus/OCS) |
| Can Rust own the engine? | **Yes** — first-class `crates/` / engine bounded context |
| WebAssembly? | **Yes** — guests + hosts + WIT/component model + Extism/wazero as needed |
| Ruby / Clojure? | **Yes** — real lock DSL / graph brain bounded contexts, not “pattern essays” |
| Go? | **Yes** — daemon/chassis bounded context |
| SQLite? | **Yes** — registry System of Record-derived (Architecture Decision Record ADR-001) |
| Python / TS? | **Yes** — ACI, gates, IDE/Model Context Protocol/Language Server Protocol as needed |
| C / Zig? | **Yes when needed** — grammars, amalgamation, systems/WebAssembly niches |
| Merge oracle today? | **Single writer** until **cutover Architecture Decision Record** (may move; not forever-Python) |

---

## 2. Bounded contexts by language (first-class)

```text
crates/va-*          Rust     engine: parse, SCIP decode, resolve, lock IR, receipts
                       + host for WASM; optional Verus/Kani on pure cores
wasm/ / guests/        WASM     LockCheck & untrusted packs (capability boundary)
go/lie0d/              Go       watch / reindex / plugin chassis (Cobra)
ruby/locks/            Ruby     Packwerk-compatible or Packwerk-shaped DSL tooling
                               (packs Rust impl may assist — still Ruby UX)
clj/ / bb/             Clojure  Datascript/XTDB-style graph REPL & query services
sqlite/                SQL      schema + migrations (owned; accessed via rusqlite etc.)
src/product/        Python   transitional ACI, Stage-0, claims, coverage writer
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
| clap or equivalent | Engine command-line interface |
| tokio | Async where earned |
| PyO3 / maturin | Bridge to Python ACI during transition |
| wasmtime (host) | Embed WebAssembly guests |
| wit-bindgen / component model | Typed WebAssembly interfaces |
| Miri / Clippy / rust-analyzer | Dev quality |
| Kani / Verus | Pilot-later on pure resolve/lock cores (process/54 FML) |

### 3.2 WebAssembly (+ multi-host toolkits)

| Toolkit | Role |
| --- | --- |
| wasmtime | Primary host (fuel/epoch) |
| Extism | Multi-lang PDK plugins if useful |
| wazero | Go-side WebAssembly host (daemon sandboxes) |
| wit / component model | Capability interfaces |
| wasm-bindgen / javy (opt) | JS/TS guest experiments |
| Wasmer / WasmEdge | Spike only if wasmtime gaps |

### 3.3 SQLite

| Piece | Role |
| --- | --- |
| SQLite engine | Derived bean/edge registry |
| SQL migrations | Versioned schema |
| rusqlite / Go database/sql / Python sqlite3 | Language bindings — **one schema System of Record** |

### 3.4 Go

| Toolkit | Role |
| --- | --- |
| Cobra | `lie0d` command-line interface/daemon |
| fsnotify | Watch → reindex |
| go-plugin / hashicorp | Optional language sidecars |
| wazero | In-process WebAssembly from Go |

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
| optional ACI peer | Orchestration, Stage-0, claims |
| pytest / pre_pr / coverage | **Current** merge oracle writer |
| PyO3 consumers | Call Rust engine |

### 3.8 TypeScript

| Toolkit | Role |
| --- | --- |
| Language Server Protocol / VS Code or Cursor extension | Red squiggle + verification panel |
| Model Context Protocol TS software development kit patterns | Org-wide / IDE Model Context Protocol clients |
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
| Alternate WebAssembly/systems toolkit | Simpler cross-compile / C-interop story |
| Native helpers | When Spike shows better fit than C/Rust for a shim |

**Keep/drop rule.** Zig/C enter via Spike with Quality Attribute Scenario; they are **in the portfolio**,
not forbidden — but not cargo-culted onto the tip without Accept.

---

## 4. Constraints that still bind (not anti-polyglot)

| ID | Constraint |
| --- | --- |
| CON-ORACLE | Exactly **one** merge writer for `coverage.xml` / claims at a time |
| CON-Quality Attribute Scenario | non-functional requirements → Architecture Tradeoff Analysis Method Quality Attribute Scenario before Design (process/54) |
| CON-Architecture Decision Record | Language bounded context additions need Architecture Decision Record (see Architecture Decision Record ADR-0001) |
| CON-SIZE | New modules respect LOC/complexipy culture (cohesive crates OK) |
| CON-PLANT | Kitchen/OCS remain Accept plants |

Polyglot **is** the product. These constraints keep it shippable.

---

## 5. Cutover roadmap (oracle)

| Phase | Oracle writer | Engine |
| --- | --- | --- |
| **Now** | Python | Spikes: Rust crates + Go daemon + Ruby locks + bb + WebAssembly guest |
| **Pilot green** | Python | Rust engine called via PyO3/command-line interface; parity tests |
| **Cutover (Approve)** | New Architecture Decision Record supersedes Architecture Decision Record ADR-005 | Rust (or designated) writes oracle **or** Python remains thin façade over Rust |

User intent: **do not stall** Rust/WebAssembly/Go/Ruby/Clojure waiting for eternal
Python ownership ideology.

---

## 6. Create — POLY-FULL tickets

| ID | Ticket | Acceptance |
| --- | --- | --- |
| **PF-0** | Architecture Decision Record ADR-0001 Accepted (product = polyglot monorepo) | Stakeholder Accept |
| **PF-1** | Cargo workspace skeleton `crates/va-*` | Builds in CI job (non-oracle) |
| **PF-2** | Go `lie0d` Cobra skeleton + watch Spike | Stamp file updates |
| **PF-3** | Ruby lock package project (Packwerk-shaped or Packwerk) | controller→repo demo |
| **PF-4** | Clojure/bb Datascript REPL on EDN export | 3 queries = SQL goldens |
| **PF-5** | WebAssembly LockCheck guest + wasmtime host | Parity vs native |
| **PF-6** | SQLite schema crate + rusqlite | Migrations + corpus load |
| **PF-7** | TS extension Spike (diagnostics panel) | One lock visible in IDE |
| **PF-8** | C/Zig Spike backlog | Only when PF-1/5 need ABI/grammar |
| **PF-9** | CI matrix: rust / go / ruby / bb / wasm **without** dual Cover% | Separate jobs; oracle still single |

---

## 7. Status

**Product stance:** full polyglot — **locked per user direction**.  
**Method stance:** Quality Attribute Scenario + Architecture Decision Record + honest formal boundaries (process/54) — **unchanged**.  
**Implement:** still behind RE Approve + Active tip reorder; PF-* are the Pilot
shape once Active.
