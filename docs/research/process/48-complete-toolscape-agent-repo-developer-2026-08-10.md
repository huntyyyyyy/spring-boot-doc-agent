---
title: E-TOOL0 — Complete toolscape for agents, repo gates, and developers (2026-08-10)
status: RESEARCH COMPLETE — Spec Draft (no mass installs until Approve)
date: 2026-08-10
epic: E-TOOL0
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
related:
  - docs/research/process/22-stack-rescope-10k-star-bar-2026.md
  - docs/research/coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md
  - docs/research/process/39-polyglot-cli-toolkit-bfs-2026-08-10.md
  - docs/research/process/40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md
  - docs/research/process/41-language-excellence-domains-subdomains-2026-08-10.md
  - docs/research/process/46-lint-import-resolution-ruff-vs-ty-2026-08-10.md
  - docs/research/process/47-cursor-mdc-rules-devex-ai-repos-2026-08-10.md
  - adapters/claude/SEARCH.md
  - .cursor/rules/
sources:
  llms_txt:
    - https://docs.astral.sh/ruff/llms.txt
    - https://docs.astral.sh/ty/llms.txt
    - https://docs.astral.sh/uv/llms.txt
    - https://cursor.com/llms.txt
  deepwiki_ask:
    - astral-sh/ruff · astral-sh/uv · ast-grep/ast-grep · semgrep/semgrep
    - charmbracelet/bubbletea · spf13/cobra · hashicorp/go-plugin
    - ruby/ruby · babashka/babashka · clojure/clojure
    - TNG/ArchUnit · gradle/gradle · elixir-lang/elixir · livebook-dev/livebook
    - bytecodealliance/wasmtime · extism/extism
    - modelcontextprotocol/typescript-sdk
  mcp: https://mcp.deepwiki.com/mcp
---

# Principal memo: who installs what — agent · repo · developer

**Product:** `doc-engine` Python CLI + Cursor/Claude agent DevEx.  
**Question.** Beyond “LLM prompts,” what is the **complete toolscape** humans and
agents should download and run — **all polyglot lanes** (Rust wheels, Go, Ruby,
Clojure, Elixir, JVM, .NET, PHP, TS/MCP, WASM, Datalog, shells, …) — without
making polyglot the merge SoT?

**Method.** Fold Jul–Aug 2026 memos (22/33/39–41/46/47) + DeepWiki MCP Ask +
Astral/`cursor.com` `llms.txt` → Embody / Adopt / Pilot / Refuse by **audience**.
Depth scorecards remain in process/39–41; this memo is the **install / audience
SoR** that binds them.

---

## 0. One-page verdict

| Audience | Must have today `[Confirmed]` | Next Adopt / Pilot | Refuse |
| --- | --- | --- | --- |
| **Repo / CI** | `.venv`: ruff, pytest, complexipy, tach, ast-grep, semgrep; CodeQL; `pre_pr --auto`; claims | **ty** (E-LINT0); SARIF/SBOM sensors; Conftest optional | Mega-linter SoT; dual Cover%; Sonar floor |
| **Developer laptop** | Same venv + `gh` + ripgrep + LSP; `install_git_hooks` | `uv` Spike; dual-sink recipes (Nu/pwsh); named language sidecars only after Pilot | husky; tip rewrite in another language |
| **Cursor / Claude agent** | MDC + Skills + hooks; SEARCH; DeepWiki MCP; `llms.txt` | E-GND0 tip-probe; E-OAS0 sinks; MCP TS **patterns** in Python host | Raw curl/clone; Node as tip dep; alwaysApply bloat |

**Polyglot lanes (compressed):** Python kernel + Embodied **Rust wheels** stay SoT.
Every other family is **Pilot / Pattern / Defer** per E-POLY0b — never a second
`coverage.xml` writer. Full family table → §2.

---

## 0b. Bloom ladder

| Level | Evidence |
| --- | --- |
| **1 Remember** | Tool IDs + `llms.txt` + DeepWiki Ask (Astral, Charm, Babashka, ArchUnit, Livebook, wasmtime/Extism, MCP TS SDK) |
| **2 Understand** | Audiences ≠ one install list; languages ≠ tip kernels |
| **3 Apply** | Today `.venv`+`pre_pr`; pilots named with keep/drop from memo 40 §4 |
| **4 Analyze** | Embody wheels vs Adopt-pattern vs Pilot-before-Refuse |
| **5 Evaluate** | §6 adversarial |
| **6 Create** | TOOL0–TOOL12 — **Implement blocked until Approve** |

---

## 1. Problem classes

| Class | Failure | Owner |
| --- | --- | --- |
| **T1 Gate SoT** | Local green ≠ CI 98.7 | `pre_pr` / oracle |
| **T2 Citation** | Text hit as structural proof | ast-grep (+ CodeQL/Semgrep) |
| **T3 Import resolution** | Unused ≠ unresolved | ruff vs **ty** |
| **T4 Agent context** | Always-on essay / missing tools | MDC + SEARCH |
| **T5 Human DX** | Opaque CLI / no dual-sink | E-OAS0 / gh patterns |
| **T6 Polyglot envy** | Rewrite tip in $LANG | Pilot-before-Refuse |

---

## 2. Full language marketplace (audience SoR)

Doctrine: five buckets from [`40`](40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md).
Excellence maps: [`41`](41-language-excellence-domains-subdomains-2026-08-10.md).
Rust engine marketplace: [`33`](../coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md).

### 2.0 Already Embodied (do not re-debate)

| Stick | Family | Role |
| --- | --- | --- |
| **ruff · complexipy · tach · ast-grep** | Rust wheels | Lint / cognitive / cycles / citation |
| **semgrep** | OCaml engine | Stage-0 / FP twin |
| **pytest · coverage adapter** | Python | Tests + oracle fold |
| **CodeQL** | CodeQL | Signals pack (CI) |
| **ripgrep allowed** | Rust binary | Prose inventory (E-SEARCH0) |
| **MDC + Skills + hooks** | Cursor | Agent activation (E-MDC0) |

### 2.1 Rust (beyond Embodied wheels)

| Stick | Bucket | Notes |
| --- | --- | --- |
| **uv** | Spike / Adopt-installer | Fast venv + `tool install` `[Evidenced — DeepWiki/llms]` |
| **ty** | Adopt after E-LINT0 Approve | `unresolved-import` |
| **maturin / PyO3 profiled bin** | Pilot-now if measured | Never unprofiled in-tree Cargo |
| **difftastic / delta** | Pilot-now review sink | Optional human DX |
| **cargo-\* / Miri / Clippy as deps** | **Refuse** | Pattern/culture only |
| **In-tree Cargo workspace** | **Refuse** | Constitution |

### 2.2 Go

| Stick | Bucket | Notes |
| --- | --- | --- |
| **cobra / gh `--json`** | Pattern | Dual-sink CLI contracts |
| **Bubble Tea / Lip Gloss / glow** | Pattern → Pilot TUI | Elm-MVU; Python-hosted `[Evidenced — DeepWiki]` |
| **go-plugin** | Pattern → Pilot | Sensor ABI shape |
| **Syft / Trivy** | Pilot-now | SBOM/vuln SARIF — never Cover% SoT |
| **OPA / Conftest** | Pattern → Pilot-later | Policy packets over grade JSON |
| **Prometheus / OTel Collector** | Pattern / Pilot-later | Sensors only |
| **Istio/Linkerd/mesh product** | **Refuse** | Category error |
| **Go tip rewrite** | **Refuse** | |

### 2.3 Ruby

| Stick | Bucket | Notes |
| --- | --- | --- |
| **Asciidoctor** | Pilot-now | Doc sink beside MkDocs |
| **RuboCop / Brakeman SARIF** | Pilot-now | Rails *targets* |
| **Packwerk ↔ tach** | Pilot-later | Boundary vocab |
| **Sorbet / ruby-lsp** | Pilot-later | Read-only sensors |
| **Bundler/Rake** | Sidecar only | If Ruby helper exists |
| **Ruby tip kernel** | **Refuse** | |

### 2.4 Clojure

| Stick | Bucket | Notes |
| --- | --- | --- |
| **Malli / Spec / Schema** | Pattern → Pilot-later | Contract registries |
| **DataScript / XTDB** | Pilot-later | FACT0 as-of facts |
| **Babashka** | Pilot-later ops | Binary *shape*; not merge interpreter `[Evidenced — DeepWiki]` |
| **Clerk / CIDER** | Pattern | Moldable review → marimo kin |
| **rewrite-clj as citation SoT** | **Refuse** | ast-grep remains citation SoT |
| **Clojure/SCI tip kernel** | **Refuse** | |

### 2.5 Elixir / Erlang

| Stick | Bucket | Notes |
| --- | --- | --- |
| **OTP supervision patterns** | Pattern | MCP/tool restart budgets `[Evidenced — DeepWiki]` |
| **Livebook sidecar** | Pilot-later | Operator notebooks; not tip SoT |
| **Credo** | Pilot-later sensor | If Elixir targets appear |
| **Elixir tip runtime** | **Refuse** | |

### 2.6 JVM (beyond Spring-as-scan-target)

| Stick | Bucket | Notes |
| --- | --- | --- |
| **ArchUnit fitness vocabulary** | Pilot-now | Pattern → Stage-0/tach docs `[Evidenced — DeepWiki]` |
| **Gradle Tooling API** | Pilot-now/later | Read-only capacity/drift receipt |
| **ErrorProne / SpotBugs / Detekt / Infer** | Pilot-later | Bug corpora / FP crosswalk |
| **JVM rewrite of tip** | **Refuse** | Spring remains *scan target*, not host |

### 2.7 .NET

| Stick | Bucket | Notes |
| --- | --- | --- |
| **Spectre.Console UX** | Pattern | CLI presentation culture |
| **Nuke DAG** | Pattern | Build orchestration shapes |
| **Roslyn analyzers** | Pilot-later | Only if .NET BC Spec’d |
| **.NET tip kernel** | **Refuse** | |

### 2.8 PHP / Lua / Fennel

| Stick | Bucket | Notes |
| --- | --- | --- |
| **PHPStan levels** | Pattern-now | Maturity/honesty UX in docs |
| **Composer provenance** | Pattern | Lockfile hygiene analogy |
| **Laravel / Kong Lua packs** | Pilot-later | Target BC only |
| **Neovim Lua review** | Defer / Pilot-later | Editor floor — not in-proc merge |
| **PHP/Lua tip kernel** | **Refuse** | |

### 2.9 TypeScript / Node (MCP & DX)

| Stick | Bucket | Notes |
| --- | --- | --- |
| **MCP TS SDK envelopes** | Pattern | Reimplement concepts in Python host `[Evidenced — DeepWiki]` |
| **Node as tip dependency** | **Refuse** | No husky / no required Node for gates |
| **jscpd (existing npm pin)** | Embody-continue | Quality gate only as already pinned |

### 2.10 WASM / Extism

| Stick | Bucket | Notes |
| --- | --- | --- |
| **bubblewrap / Landlock first** | Pilot-now | OS jail before WASM guests |
| **Extism / wasmtime guests** | Pilot-later | After bwrap insufficient `[Evidenced — DeepWiki]` |
| **WASM tip SoT / Cover%** | **Refuse** | Guest platform only (LANG0) |
| **“Wasm = secure” theater** | **Refuse** | |

### 2.11 OCaml / Datalog / FP extras

| Stick | Bucket | Notes |
| --- | --- | --- |
| **Semgrep** | Embody-continue | Already pinned |
| **Infer** | Pilot-later | Optional sensor |
| **Soufflé / Formulog** | Pilot-later | FACT0 fact-join Spike |
| **Haskell QuickCheck culture** | Pattern | Deepen Hypothesis — not new runtime |

### 2.12 Shells / notebooks / supply-chain / policy

| Stick | Bucket | Notes |
| --- | --- | --- |
| **Nushell / PowerShell recipes** | Pilot-now | Dual-sink operator docs; pipe-exit hygiene |
| **marimo / Jupyter** | Pilot-now | Human review notebooks |
| **Syft / CycloneDX / Grype** | Pilot-now / later | SBOM sensors |
| **Conftest / Rego** | Pilot-now | Over grade JSON — not Gatekeeper tip |
| **OTel spans** | Pilot-now optional | Stalker ETL only — never tip SoT |
| **Backstage / mesh / ECS product** | **Refuse** | Category error |

### 2.13 Niche / roadmap-gated (Defer)

Crystal, Perl, Nim, V, Odin, Carbon, Swift, Dart, Julia, R, mruby/ruby.wasm —
**Defer-with-revisit** unless a named target BC or measured gap vs Rust wheels
appears. Stars alone never Adopt.

---

## 3. Install matrix (who downloads what)

### 3.1 Every developer + CI (today)

Activate `.venv` from `requirements.txt` + `requirements-dev.txt`; install git
hooks; use system/user **ripgrep** + **gh**. Do not invent a second lockfile SoT.

### 3.2 Agent runtime (today)

Cursor project rules (MDC), Skills, `.cursor/hooks.json`, DeepWiki MCP URL,
SEARCH playbook. No separate “agent-only” pip world.

### 3.3 Optional after Approve (not default bootstrap)

| Install | Gate |
| --- | --- |
| `ty` in `pre_pr` | E-LINT0 Approve |
| Ruby toolchain for Asciidoctor/RuboCop job | TOOL4 Spike keep |
| Go helper binaries (Syft/Trivy) | TOOL5/SBOM Spike keep |
| Extism guest | after bubblewrap Pilot |
| Babashka / Livebook / Soufflé | named Pilot-later Spec |

---

## 4. Create — epic tickets

| ID | Acceptance |
| --- | --- |
| **TOOL0** | This memo (full marketplace §2) + backlog Draft |
| **TOOL1** | `docs/process/toolscape.md` thin pointer index → audiences × Embody |
| **TOOL2** | Wire **ty** per E-LINT0 |
| **TOOL3** | CONTRIBUTING laptop bootstrap (`uv`/`venv`/`gh`/`rg`) — no husky |
| **TOOL4** | Ruby Pilot-now (Asciidoctor **or** RuboCop/Brakeman SARIF) keep/drop |
| **TOOL5** | Go pattern landing: dual-sink CLI + Syft/Trivy sensor Spike |
| **TOOL6** | Clojure pattern → FACT0/contracts; Babashka only if ops Spike |
| **TOOL7** | JVM: ArchUnit vocabulary → Stage-0/tach docs Spike |
| **TOOL8** | Elixir: OTP supervision pattern doc for MCP tools; Livebook deferred |
| **TOOL9** | TS MCP: steal envelopes into Python host — **no** Node tip dep |
| **TOOL10** | WASM: bubblewrap Pilot-now; Extism only after fail |
| **TOOL11** | Shells/notebooks: Nu/pwsh recipes + marimo review Spike |
| **TOOL12** | Policy/SBOM: Conftest + CycloneDX export labeled sensors |

**Refuse until Approve:** mass polyglot toolchains on tip; replacing Python
oracle; mega-linter; mesh/Backstage/ECS product theater.

---

## 5. Adversarial

| Risk | Mitigation |
| --- | --- |
| “Complete” → install everything | Audience matrix + Pilot exits (memo 40 §4) |
| Starving Spring Stage-0 for Rails/WASM fashion | Pilot queue ranks; Stage-0 stays Active priority |
| ty / SARIF false-red | venv pin; sensors honesty-labeled |
| Node/Elixir/Ruby as silent tip deps | Explicit Refuse rows |
| WASM before OS jail | TOOL10 ordering |
| DeepWiki as Spec proof | Primary `llms.txt` for merge-critical |

---

## 6. Pointers

| Need | Open |
| --- | --- |
| Search | `adapters/claude/SEARCH.md` |
| Polyglot BFS | process/39–41 |
| Stack ★ bar | process/22 |
| Rust toolscape | coverage-quality/33 |
| MDC | process/47 + `.cursor/rules/` |
| Active tip | `docs/research/quality-backlog.md` |
