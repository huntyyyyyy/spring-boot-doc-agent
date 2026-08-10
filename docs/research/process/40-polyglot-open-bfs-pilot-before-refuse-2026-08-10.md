---
title: Open polyglot BFS — pilot-before-refuse (Ruby · JVM · .NET · Elixir · Datalog · enterprise)
status: ACTIVE research — amends E-POLY0; Spec E-POLY0b DRAFT; no Implement
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python 3.10+ CLI doc-engine (Stage-0 · MCP · later RAG)
related:
  - docs/research/process/39-polyglot-cli-toolkit-bfs-2026-08-10.md
  - docs/research/coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md
  - docs/research/cold-bc-dimensional-mental-map-2026-08-10.md
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
  - docs/research/process/38-cli-dx-a11y-dual-sinks-2026-08-10.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
do_not:
  - treat Pilot as license to write coverage.xml / claims / cert SoT
  - use star counts as architecture proof
  - replace Python kernel with Ruby/JVM/.NET/Elixir/WASM
  - unattended AI merge; embedding citation SoT
  - Implement pilots without named Spike exit (keep/drop)
human_review_floor: true
spec_gate: DRAFT E-POLY0b (2026-08-10) — doctrine + pilot queue; amends E-POLY0
amends: E-POLY0 · E-RUST0
stars_as_of: 2026-08-10 (GitHub API)
arxiv_verified: 2026-08-10 (HTTP 200 sample)
doctrine: Pilot-before-Refuse (five buckets)
---

# Open polyglot BFS — throw it on the wall with scorecards (2026-08-10)

**Question.** Ruby (and the full open-source / enterprise language marketplace)
can enhance doc-engine too — right? What does a **larger, open-minded, parallel
BFS** look like if we **scope + pilot before dismissing**, instead of refuse-first?

**User frame (this pass).** Assumptions without tests are weak. Prefer putting
tools through **reversible pilots** with keep/drop exits. Unique language gems
and modern research can sit **on top of** the Python kernel. Constitution still
blocks category errors (mesh/ECS/Backstage-as-product; dual Cover% SoT) — those
are not “pilots,” they are wrong product shapes.

**Method.** Parallel BFS: (A) Ruby + dynamic langs · (B) JVM/.NET/FP/systems ·
(C) enterprise frameworks/research clusters. Stars + arXiv verified 2026-08-10.
Sibling: [`process/39-…`](39-polyglot-cli-toolkit-bfs-2026-08-10.md) (first pass).

---

## 0. Doctrine shift (E-POLY0 → E-POLY0b)

| Old (memo 39 tendency) | New (this memo) |
| --- | --- |
| Early **Refuse** for whole languages/runtimes | **Five buckets** — Pilot-now · Pilot-later · Pattern-only · Defer-with-revisit · Refuse-only-after-failed-pilot **or** clear category error |
| “Deps OK if cool” vs “Refuse WASM” tension | Deps OK as **sensors / sidecars / sinks**; tip SoT stays Python; every Pilot writes **keep/drop exit first** |
| Language fashion as architecture | ★ and DeepWiki = cartography; pilots = tests of assumptions |

### Five buckets

| Bucket | Meaning |
| --- | --- |
| **Pilot-now** | Small reversible Spike; dual-sink JSON; no oracle write |
| **Pilot-later** | Blocked on named Spec (FACT0 / QUERY0 / OAS0 / …) |
| **Pattern-only** | Steal design; no new runtime dep |
| **Defer-with-revisit** | Explicit trigger or date (e.g. “customer Rails target” / 2026-11-01) |
| **Refuse** | Failed pilot **or** category error (mesh/ECS/Backstage-as-product; Cover% in another language; embedding citation SoT; unattended AI merge) |

**Hard SoT (unchanged):** `coverage.xml` fail_under 98.7 · claims · cert fold · Stage-0 citation via ast-grep/CodeQL/Semgrep · human review floor.

---

## 1. One-page verdict

| Family | Yes, can enhance? | Best stick shape | Default bucket |
| --- | --- | --- | --- |
| **Ruby** | **Yes** | Asciidoctor sink · Brakeman/RuboCop SARIF · Packwerk · ruby-lsp/Sorbet **sensors** | **Pilot-now** (AsciiDoc + Rails SARIF) |
| **Elixir/Erlang** | **Yes** | Livebook review UX · OTP supervision **patterns** · Credo sensors | Pattern-only + Pilot-later |
| **PHP** | **Yes** (targets) | PHPStan levels as maturity UX · Composer provenance · Laravel packs | Pattern-now · Pilot-later targets |
| **JVM (beyond Spring-target)** | **Yes** | ArchUnit fitness vocab · Gradle Tooling API sidecar · SpotBugs/ErrorProne crosswalk | **Pilot-now** (ArchUnit patterns) |
| **.NET** | **Yes** (patterns / later targets) | Spectre.Console UX · Nuke DAG · Roslyn if .NET BC | Pattern-only · Pilot-later |
| **OCaml** | **Already yes** | Semgrep Embodied; Infer optional sensor | Embody-continue · Pilot-later Infer |
| **Datalog/Soufflé** | **Yes** | Fact-join Spike kin to CodeQL | Pilot-later (FACT0) |
| **Crystal / Perl / Nim / V / Odin / Carbon** | Niche | Pattern or Defer — pilot only if measured gap vs Rust wheels | Defer-with-revisit |
| **Swift / Dart / Julia / R** | Roadmap-gated | Target BC or offline metrics notebooks | Defer / Pilot-later |
| **Lua / Fennel** | **Yes** (targets / editor) | Kong plugin packs; Neovim review; **not** in-proc merge scripts | Pilot-later · Defer embed |
| **WASM / Extism** | **Yes as guest Spike** | After OS jail (bubblewrap) proven insufficient | Pilot-later · not by-default |
| **TS / Go / Rust wheels** | **Yes** (memo 39) | MCP · TUI patterns · Embodied engines | Embody / Adopt-pattern |

**“Throw everything and see what sticks”** = run the **top pilot queue** with exits — not merge fifteen runtimes into tip.

---

## 2. Master language marketplace (compressed)

Stars 2026-08-10. Detail scorecards live in research packets behind this synthesis.

### 2.1 Ruby & friends — **yes, Ruby can**

| Toolkit | ★ | Unique stick | Bucket |
| --- | ---: | --- | --- |
| Rails | 58681 | Target DSL / conventions | Pilot-later packs |
| RuboCop | 12897 | Lint SARIF sensor | **Pilot-now** |
| Brakeman | 7261 | Rails security SA | **Pilot-now** |
| Asciidoctor | 5202 | Enterprise AsciiDoc sink | **Pilot-now** |
| Sorbet / RBS / Tapioca | 3.8k / 2.2k / 0.9k | Gradual types / RBI | Pilot-later sensors |
| Shopify ruby-lsp / Packwerk | 2.0k / 1.9k | Rails meta + package boundaries | Pilot-later |
| Sidekiq / dry-rb / Hanami | 13.5k / … | Job topology / FP Ruby patterns | Pattern-only |
| Crystal | 20365 | Ruby-like native | Pattern-only · Defer host |
| mruby / ruby.wasm | 5.6k / 0.9k | Embed / WASM Ruby | Defer (guest Spike only w/ POLY0) |

**Papers:** LspFuzz/Sorbet [2510.00532](https://arxiv.org/abs/2510.00532) · gradual typing [2007.12630](https://arxiv.org/abs/2007.12630) · YASA polyglot taint [2601.17390](https://arxiv.org/abs/2601.17390).

### 2.2 Elixir / PHP / Lua

| Family | Unique stick | Bucket |
| --- | --- | --- |
| Elixir Livebook ★5.8k + OTP | Operator notebooks; supervision for agent tools | Pattern-only OTP · Pilot-later Livebook sidecar |
| PHPStan ★14k · Composer ★29k · Laravel ★35k | Level/baseline maturity UX; PHP target Stage-0 | Pattern-now levels · Pilot-later targets |
| Kong ★44k · OpenResty · Neovim | Gateway Lua plugins; editor review floor | Pilot-later target · Defer in-proc scripts |

**Papers:** Erlang scale [1704.07234](https://arxiv.org/abs/1704.07234) · PHP taint [2410.12351](https://arxiv.org/abs/2410.12351).

### 2.3 JVM / .NET / FP / Datalog

| Family | Unique stick | Bucket |
| --- | --- | --- |
| ArchUnit ★3.8k | Fitness-as-rules vocabulary for Spring | **Pilot-now** (pattern→Stage-0) |
| Gradle Tooling API | Live project model / deps without full build | Pilot-later sidecar |
| ErrorProne / SpotBugs / Detekt / Infer | Bug corpora / FP crosswalk | Pilot-later |
| Roslyn ★20.6k · Spectre.Console ★11.6k · Nuke | Analyzer Create · CLI UX · build DAG | Pattern-now · Pilot-later .NET BC |
| Semgrep (OCaml) | **Already Embodied** | Embody-continue |
| Soufflé ★1.1k · Formulog line | Declarative fact joins / provenance | Pilot-later FACT0 |
| Haskell QuickCheck / Liquid | Property + contract culture | Pattern-only → Hypothesis deepen |
| SwiftLint / SourceKit · Flutter DevTools | Apple targets · stalker UX | Defer / Pattern |
| Julia / R | Offline metrics / RAG eval notebooks | Pilot-later |
| Nushell ★40k · PowerShell ★55k | Structured operator views | **Pilot-now** recipes |

**Papers:** PolyDebug [2502.20537](https://arxiv.org/abs/2502.20537) · Formulog [2009.08361](https://arxiv.org/abs/2009.08361) · fitness functions [2509.10085](https://arxiv.org/abs/2509.10085) · Ant Group analysis [2401.01571](https://arxiv.org/abs/2401.01571) · FlowLog [2511.00865](https://arxiv.org/abs/2511.00865).

---

## 3. Enterprise / research clusters (on top of languages)

| Cluster | Landing pads | Bucket |
| --- | --- | --- |
| Plugin ABI | Python entry_points · go-plugin shape · Extism · Java SPI | **Pilot-now** entry_points · Pattern go-plugin · Pilot-later Extism |
| Understanding engines | LSP · SCIP · Serena · Metals · ruby-lsp | Pilot-later sensors (never citation SoT) |
| Build intelligence | Gradle now · Bazel/Nx/Pants Defer-with-revisit | Pilot-now Gradle sensor |
| Policy | Conftest/Rego offline · Cedar shape · Refuse Gatekeeper/Kyverno tip | Pilot-now Conftest |
| Supply chain | Syft · CycloneDX · Grype later · Cosign Defer | Pilot-now SBOM export |
| Literate review | marimo / Jupyter · Livebook UX pattern | Pilot-now marimo |
| Observability | OTel as **sensor only** (Refuse as tip SoT) | Pilot-now optional spans |
| Sandbox | bubblewrap/Landlock first · WASM guest later · Refuse Firecracker tip | Pilot-now bwrap |

---

## 4. Top pilots ranked (unique value × reversibility)

| # | Pilot | Bucket | Keep if | Drop if |
| ---: | --- | --- | --- | --- |
| 1 | `entry_points` for scanners/presenters/packs | Pilot-now | ≥2 hermetic packs load | importlib tax > benefit |
| 2 | **Asciidoctor** (Ruby or asciidoctor.js) presenter sink | Pilot-now | Reviewers use AsciiDoc output | Unused / dep brittle |
| 3 | **Brakeman + RuboCop SARIF** → sensor findings | Pilot-now | Rails kitchen fixture useful | No Rails targets in roadmap |
| 4 | **ArchUnit → Stage-0/tach fitness vocabulary** | Pilot-now | Clearer Spring boundary docs/tests | Duplicates tach without gain |
| 5 | Gradle Tooling API read-only capacity/drift receipt | Pilot-now/later | Kitchen uses receipt | Flake/cost high |
| 6 | Syft/CycloneDX SBOM export on cert | Pilot-now | Labeled compliance used | Unused |
| 7 | Conftest/Rego over grade JSON | Pilot-now | Clarifies CONSTRAINTS packs | Duplicates `check_repo_claims` |
| 8 | marimo/Jupyter human review notebooks | Pilot-now | Humans actually open them | Ignored |
| 9 | bubblewrap (± Landlock) for agent tools | Pilot-now | Blocks real escape class | Hooks already enough |
| 10 | OTel spans → stalker ETL only | Pilot-now | p95 Stage-0 visible | Noise by 2026-10-01 |
| 11 | Nu/pwsh dual-sink operator recipes | Pilot-now | Docs stop pipe-exit footguns | — |
| 12 | PHPStan levels → honesty/maturity **pattern** | Pattern → Pilot | UX adopted in docs | — |
| 13 | OTP supervision → MCP process **pattern** | Pattern | Restart budgets documented | — |
| 14 | SCIP/ruby-lsp/Sorbet read-only sensors | Pilot-later | Enrich packets w/ labels | Citation temptation |
| 15 | Livebook runbook sidecar | Pilot-later | Ops UX win | Erlang install tax |
| 16 | Soufflé 5-relation fact Spike | Pilot-later | Clearer joins than Python | CodeQL enough |
| 17 | Extism guest plugin | Pilot-later | OS jail insufficient | entry_points+subprocess enough |
| 18 | Packwerk / Kong Lua / Laravel packs | Pilot-later | Target BC Spec’d | Spring Stage-0 starved |

**Not in queue (category error — Refuse without pilot theater):** mesh · ECS product rewrite · Backstage-as-runtime · Cover% in Ruby/JVM/WASM · Firecracker/Kata tip · unattended AI merge.

---

## 5. Bloom Create unlocked by open BFS

| Create lane | Language/toolkit fuel |
| --- | --- |
| Doc sinks | Asciidoctor · ExDoc patterns · marimo review |
| Target packs | Rails SARIF · Laravel · Kong Lua · Swift later |
| Fitness vocabulary | ArchUnit · Packwerk · tach Embody |
| Fact engines | CodeQL deepen · Soufflé Spike · SCIP sensors |
| Agent surface | entry_points · MCP TS patterns · Cedar/Rego envelopes · bwrap |
| Operator UX | Spectre/Bubble Tea patterns · Livebook UX · Nu/pwsh |
| Profiled helpers | PyO3 bin (memo 39) after measure |

---

## 6. Spec amendments **E-POLY0b** (DRAFT)

| ID | Decision |
| --- | --- |
| **POLY0b-1** | Adopt five-bucket doctrine (Pilot-before-Refuse) |
| **POLY0b-2** | Ruby is in-scope for Pilot-now sinks/sensors (AsciiDoc, Rails SARIF) |
| **POLY0b-3** | Every Pilot Spec must list keep/drop exit + SoT non-goals |
| **POLY0b-4** | Category-error Refuse list remains (mesh/ECS/Backstage/dual Cover%) |
| **POLY0b-5** | Top-11 Pilot-now items eligible for Spike tickets after Approve |
| **POLY0b-6** | Pilot-later items gated on FACT0/QUERY0/OAS0/target-BC Specs |
| **POLY0b-7** | WASM/Extism remains Pilot-later — after bubblewrap Pilot result |
| **POLY0b-8** | Memo 39 Embody (Python + Rust wheels) unchanged |

**Exit:** Approve POLY0b-1–8 → open Spike PRs one-at-a-time (not fifteen parallel tip thrash). Failed Spike → bucket **Refuse** or **Defer-with-revisit**, documented.

---

## 7. Adversarial checklist

- [ ] Is “open-minded” being used to skip keep/drop exits?
- [ ] Is a Ruby/JVM/Elixir runtime writing oracle/claims/cert?
- [ ] Are we starving Spring Stage-0 for Rails fashion?
- [ ] Did WASM Pilot wait for OS-jail result?
- [ ] Are sensors honesty-labeled vs SoT?
- [ ] Is star count architecture proof? (No)
- [ ] Polyglot cost acknowledged (PolyDebug / MEnvAgent)?

---

## 8. Exit

Yes — **Ruby can**, and so can Elixir, PHP, JVM tooling, .NET UX, Datalog, notebooks, policy packs, SBOM, and sandboxes — as **pilots and patterns on top of** the Python kernel. This memo replaces refuse-first with **pilot-before-refuse**, inventories the marketplace, and ranks experiments. **No Implement** until Spike Specs with exits. Sibling: process/39 · dimensional map · E-RUST0.
