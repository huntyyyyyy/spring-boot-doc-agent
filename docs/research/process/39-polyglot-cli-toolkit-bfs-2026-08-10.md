---
title: Polyglot CLI toolkit BFS — Rust · WASM · Go · TS · PyO3 (Bloom Create)
status: ACTIVE research — Spec epic E-POLY0 DRAFT; amends E-RUST0; no Implement
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
product: Python 3.10+ CLI doc-engine (Stage-0 · MCP · later RAG)
related:
- docs/research/coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md
- docs/research/coverage-quality/32-realtime-architecture-assertion-agents-2026.md
- docs/design/rust-stack-fit-memo-2026-08-08.md
- docs/research/process/04-implementation-frameworks.md
- docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
- docs/research/process/38-cli-dx-a11y-dual-sinks-2026-08-10.md
- docs/research/process/40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md
- docs/research/cold-bc-dimensional-mental-map-2026-08-10.md
- docs/research/se-quality-synthesis-2026-08-08.md
- docs/research/quality-backlog.md
do_not:
- treat polyglot / WASM / Rust rewrite as merge or Cover% SoT
- add in-tree Cargo / wasmtime-by-default without profiled Spec Approve
- replace Python oracle/claims with another language runtime
- unattended AI merge; embedding citation SoT
- Implement helpers from this BFS alone
human_review_floor: true
spec_gate: DRAFT E-POLY0 (2026-08-10) — POLY0-1–POLY0-10 pending Approve
amends: E-RUST0
stars_as_of: 2026-08-10 (GitHub API)
arxiv_verified: 2026-08-10 (HTTP 200)
last_reviewed: '2026-08-10'
---

# Polyglot CLI toolkit BFS (2026-08-10)

**Question.** Beyond “Python-only,” which **languages and toolkits** (Rust, WASM,
Go, TS/Node, PyO3, …) could **enhance** doc-engine’s total CLI functionality —
LLM usage, MCP usage, developer usage, accessibility, and meta-understanding up
to Bloom **Create** — without making polyglot the merge SoT?

**User frame (this pass).** Dependencies are acceptable **when** arXiv / GitHub /
DeepWiki show powerful, healthy implementations — as **landing pads** and
**profiled helpers**, not as fashion. Constitution still binds: no WASM-by-default
without profiled Spec, no dual Cover% SoT, Python remains kernel.

**Doctrine update (same day):** Refuse-first softened to **Pilot-before-Refuse**
in [`process/40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md`](40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md)
(E-POLY0b) — includes **Ruby**, JVM/.NET/Elixir/PHP/Datalog, enterprise clusters,
and ranked pilots with keep/drop exits. This memo 39 remains the Rust/WASM/Go/TS/PyO3
first-pass inventory.

**Method.** BFS across languages + enhancement clusters; GitHub stars/push +
arXiv HTTP 200 + DeepWiki Evaluate/Create. Prior: E-RUST0 memo 33 (Rust quality
marketplace). This memo **widens the marketplace** to polyglot CLI/MCP/LLM.

---

## 0. One-page verdict

| Stance | Choice |
| --- | --- |
| **Embody** | Python kernel + oracle/claims; **Rust via pinned wheels/CLIs** (ast-grep, ruff, tach, complexipy); tree-sitter substrate *inside* those tools; dual sinks / NO_COLOR; thin MCP host |
| **Adopt-pattern** | TS MCP SDK envelopes; Charm Bubble Tea / ratatui Elm-MVU; clap help semantics; gh `--json`/`--jq`; hashicorp go-plugin / WASI capability *shapes*; LSP/SCIP as understanding **sensors** |
| **Spike (profiled Spec)** | maturin/PyO3 **helper bin** for measured hotspots; Extism/WASI guest plugins; bubblewrap/Landlock for agent tool isolation; Deno sidecar if TS MCP servers adopted; official MCP SDK pin |
| **Explicit Defer** | Zig; Lua/Rhai user scripting; Bun/Deno as dual kernel; full wasmtime/wasmer product host |
| **Refuse** (category error — no pilot theater) | Dual Cover%/claims SoT in another language; mesh/ECS/Backstage-as-product; embedding citation SoT; unattended AI merge |
| **Pilot-before-Refuse** | See E-POLY0b / process/40 for Ruby+full marketplace + keep/drop exits |

**Key reframe vs “deps don’t matter”:** deps are fine for **Embodied engines we
already consume** and for **Spec-gated helpers** with Acceptances. They are
**not** a license to dual-write Cover%, citations, or certification into another
runtime. Polyglot complexity is itself a risk `[Evidenced]` PolyDebug 2502.20537,
MEnvAgent 2601.22859.

---

## 1. Mental map — language → Bloom Create

```text
Bloom Create (author new tools / packets / packs / presenters)
        ▲
        │  MCP tool authorship (TS patterns + Python host)
        │  Stage-0 rule Create (ast-grep / CodeQL packs)
        │  Presenter Create (Headline/Plain/JSON/RichTty)
        │  Profiled native helper Create (PyO3 bin — Spike)
        │  Sandboxed guest Create (WASM/Extism — Spike only)
Understand / Evaluate  ←── DeepWiki + LSP/SCIP sensors + fixtures
Apply / Analyze        ←── Stage-0 facts, joins, drift sensors
Remember / Understand  ←── Python CLI + Embodied Rust CLIs
────────────────────────────────────────────────────────────
KERNEL SoT (never leave Python): coverage.xml · claims · cert fold · plant
ENGINES (consume): Rust wheels · Semgrep · CodeQL · tree-sitter-under-hood
ADAPTERS: MCP · Typer grade · optional TTY · optional sandbox
GUESTS (Spike): WASM PDK / subprocess plugins — never merge authority
```

---

## 2. BFS by language / runtime

Stars · push from GitHub API **2026-08-10**.

| Language | Toolkit clusters (examples) | CLI / MCP / LLM / a11y / meta | Bloom Create unlock | Stance |
| --- | --- | --- | --- | --- |
| **Rust** | ast-grep ★15k · ruff ★49k · tach · complexipy · clap ★17k · tree-sitter ★27k · maturin ★5.7k · ripgrep | Engines behind gates; weak MCP host; strong agent-callable bins; clap help culture; DeepWiki clap/tree-sitter | New Stage-0 rules / sensors without second language SoT | **Embody** wheels · **Refuse** in-tree Cargo |
| **WASM/WASI** | wasmtime ★18k · wasmer ★21k · WasmEdge ★11k · WASI · extism ★5.7k · spin ★6.5k · component-model | Plugin/sandbox story; SpecBox-class MCP coupling `[Evidenced]`; no a11y win; DeepWiki Engine/Store/Component | User-authored sandboxed plugins — only if Spec’d marketplace | **Defer** · **Refuse** product/merge runtime |
| **Go** | cobra ★44k · bubbletea ★44k · lipgloss · huh · go-plugin · OPA ★12k | Best TUI patterns; go-plugin RPC; OPA weight wrong; DeepWiki MVU | Better HITL review TUIs (Python-hosted) | **Adopt-pattern** · **Refuse** Go rewrite |
| **Zig** | zig ★43k | Systems DIY; near-zero MCP/Stage-0 ecosystem | Unlikely unique helper vs Rust wheels | **Explicit Defer** |
| **C/C++ (via existing)** | tree-sitter C core · LLVM · pybind11 · Cython · zstd | Already inside Embodied tools | New grammars consumed by tools — not in-tree C | **Embody** indirect · **Refuse** new in-tree C |
| **TypeScript/Node** | typescript-sdk ★13k · MCP servers ★89k · TS ★110k · esbuild · oxc | **Strongest MCP ecosystem**; LLM SDKs; editor WASM bridge ≠ terminal a11y | Author MCP tools exposing Stage-0 + grade | **Adopt-pattern** · optional sidecar Spike |
| **Lua / Rhai** | lua · mlua · rhai ★5.6k · starlark | Embeddable scripting; high unattended-merge risk | Safe user extensions only after Spec’d deny surface | **Explicit Defer** |
| **Java/Kotlin** | Spring Boot ★81k · Framework · Kotlin | **Target** analysis language, not host | Richer Spring fixtures/packs for doc Create | **Embody** target · **Refuse** host JVM |
| **PyO3 / maturin** | PyO3 ★16k · maturin · uv · tokenizers | Profiled `.so`/bin helpers; host stays Python | Profiled bin for measured hotspot | **Spike-profiled-helper** |
| **Deno / Bun** | Deno ★108k · Bun ★95k | Permissioned JS runtimes for MCP sidecars | Permissioned TS MCP host — not dual kernel | **Explicit Defer** (sidecar if TS MCP) |

---

## 3. Enhancement clusters (LLM · MCP · developer)

### 3.1 MCP (beyond Python)

| Repo | ★ | Push | Stance | Create unlock |
| --- | ---: | --- | --- | --- |
| modelcontextprotocol/typescript-sdk | 13109 | 2026-08-10 | Adopt-pattern | Typed dual-surface registry |
| modelcontextprotocol/servers | 89383 | 2026-08-10 | Adopt-pattern | Read-only catalog discipline |
| modelcontextprotocol/python-sdk | 23954 | 2026-08-07 | Spike pin (Q0-9) | Official schema |
| mark3labs/mcp-go / go-sdk / rust-sdk | 4–9k | active | Spike interop fixtures | Conformance matrix |
| oraios/serena | 27790 | 2026-08-09 | Adopt-pattern | LSP-as-tools (sensor) |
| PrefectHQ/fastmcp | 27142 | 2026-08-10 | Refuse second megastack | Keep thin adapter |

### 3.2 WASM plugins / hosts

| Repo | ★ | Stance | Create unlock |
| --- | ---: | --- | --- |
| wasmtime / wasmer | ~18–21k | Refuse product dep; Spike guest only under Spec | Capability guest port |
| extism/extism | 5710 | Spike PDK ergonomics | Versioned plugin ABI + deny-by-default |
| wazero / hashicorp/go-plugin | ~6k | Adopt-pattern | Subprocess plugin > in-proc WASM for tip |
| WASI / Shopify Functions pattern | — | Adopt capability *shape* | Guest = pure fn; host owns I/O |

Papers: eWAPA 2409.10252 · Twine 2103.15860 · Not So Fast 1901.09056 · Gobi 1912.02285 · WASM security 2407.12297 · SpecBox 2607.23933 · MVVM agents 2410.15894 · CapSeal 2604.16762.

### 3.3 Terminal UX meta

| Repo | ★ | Stance |
| --- | ---: | --- |
| bubbletea / ratatui | 44k / 22k | Adopt-pattern (testable model→view) |
| textual | 37k | Refuse as grade/MCP SoR |
| rich | 57k | Embody optional TTY; Refuse CI SoT |
| typer | 20k | Embody thin grade façade |

### 3.4 Structured output for agents

| Repo | ★ | Stance |
| --- | ---: | --- |
| jq / yq / nushell / fx / dasel | 8–40k | Adopt-pattern views; Refuse shelling as SoR |
| jsonschema | ~5k | Embody receipt schemas |
| outlines | 16k | Refuse as citation/gate SoT |
| gh CLI | 46k | Embody `--json` + `--jq` dual sinks |

### 3.5 Sandbox / isolation

| Repo | ★ | Stance |
| --- | ---: | --- |
| bubblewrap | 8.3k | Spike Linux tool-subprocess jail |
| firecracker / gvisor / kata | 19–36k | Refuse tip deps (ops tax) |
| Landlock | small★ | Spike capability FS jail pattern |
| WASM sandbox | — | Refuse-by-default; Spike only with Spec |

Papers: container escape 2603.02277 · WASM container attack surface 2509.11242 · Crab C/R 2604.28138 (if cited elsewhere).

### 3.6 Meta-understanding (toward Create)

| Repo | ★ | Stance | Create unlock |
| --- | ---: | --- | --- |
| tree-sitter / ast-grep / semgrep / codeql | 10–27k | Embody | Structural / QL rule Create |
| language-server-protocol / rust-analyzer / pyright | 13–17k | Spike sensors | Xref/type facts channel |
| scip-code/scip | ~0.7k elegant | Spike | Index export — not tip SoR |

Papers: Codebase-Memory MCP 2603.27277 · DL for code intel 2401.00288 · LSP families 2509.15150 · polyglot programs 2602.00303.

---

## 4. DeepWiki Evaluate → Create (cartography only)

| Repo | Evaluate | Create for doc-engine |
| --- | --- | --- |
| wasmtime / wasmer | Engine/Store/Component/WASI | Plugin host only after process isolation fails Spec |
| PyO3 | GIL, modules, smart pointers | Profiled **bin** under E-RUST0/POLY0 gate |
| clap | Builder/derive/ArgAction | Better Typer/help/completion patterns |
| bubbletea | Elm/MVU terminal | Review-floor TUI presenters; Python kernel |
| tree-sitter | Incremental parse + queries | Understand ast-grep substrate; refuse dual SoT |
| vscode-wasm | Component Model in editor | Editor sandbox ≠ CI oracle |
| extism | PDK + host functions | Cleanest plugin API — still Defer default |
| deno | Permissioned CLI | Permissioned TS MCP sidecar if needed |
| typescript-sdk | Tools/resources/prompts | Primary agent-surface Create lane |

---

## 5. How this binds the dimensional lattice

| Lattice row | Polyglot implication |
| --- | --- |
| Identity | SCIP/LSP may **sensor**-enrich ids; Stage-0/ast-grep remain SoT |
| Honesty labels | Native helpers must stamp builder/executor like cert honesty |
| Budget/caps | WASM/plugin guests inherit envelope caps — no unbounded guest I/O |
| Isolation | Prefer OS/process (bubblewrap) before WASM; MCP write still Refuse |
| Dual sink | Any Go/Rust helper bin must emit JSON twin + respect NO_COLOR |
| Human floor | Plugin Create ≠ merge authority |
| Fixture≠campaign | Polyglot envs (MEnvAgent) are campaign — not CI SoT |
| Derived≠LWW | No second cert writer in Rust/WASM |

---

## 6. Spec epic **E-POLY0** (DRAFT — amends E-RUST0)

| ID | Decision / ticket | Acceptance (sketch) |
| --- | --- | --- |
| **POLY0-1** | Python remains product kernel + Cover%/claims SoT | CONTRIBUTING + tests refuse polyglot oracle |
| **POLY0-2** | Embody Rust wheels list frozen (ast-grep, ruff, tach, complexipy) | Pins match requirements; E-RUST0 still binds |
| **POLY0-3** | WASM/wasmtime/wasmer **Refuse** as default runtime | Claims/docs; no dep without Spike exit |
| **POLY0-4** | Profiled helper gate: measure → Spec → prefer **maturin bin** over in-proc `.so` | Spike exit criterion documented |
| **POLY0-5** | MCP: thin Python host; Adopt TS envelope patterns; FastMCP megastack Refuse | Q0-4/Q0-9 alignment |
| **POLY0-6** | TUI: Adopt Bubble Tea/ratatui patterns; Textual Refuse as grade SoR | OAS-D presenters |
| **POLY0-7** | Agent structured I/O: Embody schema’d dual sinks; jq/yq views only | GradeReport JSON schema |
| **POLY0-8** | Sandbox Spike: bubblewrap/Landlock optional port — never merge SoT | Spec + Linux-first; Windows Path B |
| **POLY0-9** | Understanding sensors: LSP/SCIP Explicit Defer until FACT0/QUERY0 Approve | No citation via LSP alone |
| **POLY0-10** | Bloom Create lanes named: (a) Stage-0 packs (b) MCP tools (c) presenters (d) profiled bin (e) guest plugin | Each lane has human floor + Refuse list |

**Exit:** E-POLY0 Approve → unlocks only named Spikes; E-RUST1 / helper Implement still one tip stream after profile evidence.

**Non-goals:** Zig kernel · Lua scripting v1 · Firecracker · OPA runtime · Backstage · replacing E-RUST0 inventory.

---

## 7. Adversarial checklist

- [ ] Is “deps are fine” being used to sneak a second Cover% SoT?
- [ ] Is WASM justified by a measured isolation gap OS process can’t cover?
- [ ] Does every Create lane preserve human review floor?
- [ ] Are star counts treated as architecture proof? (Refuse)
- [ ] Does DeepWiki prose get cited as Stage-0 evidence? (Refuse)
- [ ] Is FastMCP / Textual / Go rewrite solving a real Spec gap?
- [ ] Has E-RUST0 already Embodied the Rust value we need for gates?

---

## 8. Exit

BFS complete: languages inventoried, enhancement clusters mapped, Bloom Create
lanes named, Spec **E-POLY0** drafted. **No Implement.** Sibling SoTs: memo 33
(E-RUST0) · process/37–38 · dimensional mental map · synthesis 1–31.

**Practical next Create energy (still Spec-first):** MCP tool surface + dual-sink
presenters + Stage-0 pack authorship — mostly **Python + Embodied Rust CLIs** —
before any WASM/PyO3 adventure.
