---
title: Language excellence domains → subdomains (Rust · Go · Ruby · Clojure · WASM)
status: ACTIVE deep research — amends E-POLY0b; Spec E-LANG0 DRAFT; no Implement
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine (Stage-0 · MCP · later RAG)
related:
  - docs/research/process/39-polyglot-cli-toolkit-bfs-2026-08-10.md
  - docs/research/process/40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md
  - docs/research/coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md
  - docs/research/cold-bc-dimensional-mental-map-2026-08-10.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
do_not:
  - treat logo ★ as architecture proof
  - replace Python Cover%/claims SoT with any language runtime
  - Implement without Pilot keep/drop exits
  - unattended AI merge; embedding citation SoT
  - mesh/ECS/Backstage-as-product theater
human_review_floor: true
doctrine: Pilot-before-Refuse (five buckets)
spec_gate: DRAFT E-LANG0 (2026-08-10) — depth map; amends E-POLY0b
stars_as_of: 2026-08-10 (GitHub API)
arxiv_verified: 2026-08-10 (HTTP 200 sample)
---

# Language excellence: domains → subdomains → logo exemplars

**Question.** For languages that excel in SE/architecture tooling — **Rust, Go,
Ruby, Clojure, WASM** — what **domains** and **common subdomains** matter, and
what are the **excellent logos** (flagship repos + research) to pilot from?

**Method.** Deep DFS per language (not shallow BFS laundry lists). Stars + push
via GitHub API 2026-08-10. arXiv HTTP 200 verified for cited IDs. Doctrine:
Pilot-before-Refuse ([process/40](40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md)).

**One-page verdict**

| Language | Excels at | Best stick on doc-engine |
| --- | --- | --- |
| **Rust** | Correctness engines · ultra-fast CLI/lint · structural search · Wasm *producer* · Cargo supply-chain | **Embody** wheels; Pilot maturin bins; Pattern clap/Miri |
| **Go** | Cloud CLIs · RPC plugins · Charm TUI · policy/control-plane · release/SBOM agents | **Pattern** CLI/TUI/plugin; Pilot Syft/Trivy sensors |
| **Ruby** | Rails SA/security · AsciiDoc · gradual types/LSP · Packwerk · job topology | **Pilot-now** Asciidoctor + Brakeman/RuboCop |
| **Clojure** | REPL/data-as-program · EDN/Transit · Spec/Malli · EAV/time facts · Babashka · rewrite-clj | **Pattern** contracts/facts; Pilot-later FACT0/bb |
| **WASM** | Portable sandboxed guests · polyglot PDK · capability WASI · signed portable modules | **Pattern** capability worlds; Pilot-later Extism after bwrap |

Kernel SoT stays Python. Logos are landing pads for pilots — not tip rewrites.

---

## 0. Cross-language logo wall (iconic SE tooling)

| Rust | ★ | Go | ★ | Ruby | ★ | Clojure | ★ | WASM | ★ |
| --- | ---: | --- | ---: | --- | ---: | --- | ---: | --- | ---: |
| rust-lang/rust | 115k | kubernetes | 124k | rails/rails | 59k | clojure/clojure | 11k | wasmer | 21k |
| ripgrep | 67k | cobra | 44k | Sidekiq | 14k | DataScript | 5.8k | wasmtime | 18k |
| ruff | 49k | bubbletea | 44k | RuboCop | 13k | Babashka | 4.6k | pyodide | 15k |
| tree-sitter | 27k | Prometheus | 66k | Brakeman | 7.3k | CIDER | 3.7k | WasmEdge | 11k |
| ast-grep | 15k | gh (cli/cli) | 46k | Asciidoctor | 5.2k | XTDB | 3.0k | wasm-bindgen | 9.1k |
| rust-analyzer | 17k | Terraform | 49k | Sorbet | 3.8k | clj-kondo | 1.8k | Spin | 6.5k |
| Clippy | 13k | OPA | 12k | ruby-lsp | 2.0k | Malli | 1.8k | Extism | 5.7k |
| wasmtime | 18k | go-plugin | 6.1k | Packwerk | 1.9k | core.async | 2.0k | component-model | 1.4k |
| tokio | 33k | goreleaser | 16k | YARD | 2.0k | Component | 2.2k | wazero | 6.3k |
| cargo | 15k | Helm | 30k | Thor | 5.3k | Clerk | 2.1k | javy | 2.7k |

---

## 1. Rust — domains & subdomains

### R1 Systems correctness & memory safety
| Subdomain | Logos | Research | Pilot |
| --- | --- | --- | --- |
| Ownership / UB (Miri, Stacked Borrows) | miri ★6.5k · rust | [Stacked Borrows](https://plv.mpi-sws.org/rustbelt/stacked-borrows/) · [2404.11671](https://arxiv.org/abs/2404.11671) | Pattern |
| Bounded verify (Kani) | kani ★3.3k | [Kani book](https://model-checking.github.io/kani/) · Oxide [1903.00982](https://arxiv.org/abs/1903.00982) | Defer→Pilot if native |
| Proof-oriented (Verus/Prusti) | verus ★2.8k · prusti ★1.8k | Verus [2303.05491](https://arxiv.org/abs/2303.05491) | Pattern (claim tiers) |
| Fuzz adjacency | cargo-fuzz ★1.9k | Fuzzing survey [1812.00140](https://arxiv.org/abs/1812.00140) | Pilot-later fixtures |

### R2 High-perf CLI / linters / formatters
| Subdomain | Logos | Research | Pilot |
| --- | --- | --- | --- |
| Repo-scale lint engines | **ruff** ★49k · biome ★26k · oxc ★22k · Clippy ★13k | Clippy book · [1806.02693](https://arxiv.org/abs/1806.02693) | **Embody** ruff |
| Agent-callable search CLIs | ripgrep ★67k · fd ★44k · bat ★60k | [2601.23254](https://arxiv.org/abs/2601.23254) | Pattern (ast-grep SoT) |
| Diff / review binaries | difftastic ★26k · delta ★32k | — | Pilot-now review sink |
| CLI framework culture | clap ★17k · ratatui ★22k | clap docs | Pattern→Typer |

### R3 Structural search / parsers
| Subdomain | Logos | Research | Pilot |
| --- | --- | --- | --- |
| Incremental grammars | **tree-sitter** ★27k · helix ★46k | [2603.27277](https://arxiv.org/abs/2603.27277) | Embody under ast-grep |
| Structural search/codemod | **ast-grep** ★15k · comby ★2.7k | ast-grep docs | **Embody** |
| Semantic index | rust-analyzer ★17k · SCIP ★0.7k | rustc-dev-guide | Pilot-later sensors |
| Architecture fitness | tach ★2.8k · cargo-semver-checks ★1.7k | — | Embody tach |

### R4 WASM as producer · R5 Async · R6 Supply-chain · R7 PDKs
- **R4:** wasmtime ★18k · wasmer ★21k · wit-bindgen · Extism — [2311.14246](https://arxiv.org/abs/2311.14246) · Pilot-later guests  
- **R5:** tokio ★33k · tracing ★6.8k · vector ★22k — Pattern spans  
- **R6:** cargo-deny ★2.4k · **PyO3** ★16k · maturin ★5.7k · uv ★89k — SoK [2406.10109](https://arxiv.org/abs/2406.10109) · Pilot maturin if profiled  
- **R7:** embassy ★9.7k — Defer (no product need)

**Bloom Create (Rust):** Stage-0 packs · fitness sensors · profiled bins · capability guest sketches.

---

## 2. Go — domains & subdomains

### G1 Cloud-native CLIs & operators
| Subdomain | Logos | Pilot |
| --- | --- | --- |
| CLI frameworks & flagship CLIs | cobra ★44k · **gh** ★46k · urfave/cli ★24k | Pattern `--json`/`--jq` |
| Operator / controller SDKs | kubebuilder ★9.3k · controller-runtime ★2.9k | Pattern reconcile (E-CPL0 kin) |
| Cluster UX / GitOps | k9s ★34k · Helm ★30k · Argo CD ★24k · Flux ★8.3k | Pattern progressive disclosure |

### G2 Plugin architectures
| Subdomain | Logos | Pilot |
| --- | --- | --- |
| Subprocess RPC plugins | **go-plugin** ★6.1k · Terraform ★49k · yamux | **Pilot-now** sensor ABI shape |
| gRPC boundaries | grpc-go ★23k | Pattern contracts |

### G3 Terminal UX (Charm)
| Subdomain | Logos | Pilot |
| --- | --- | --- |
| Elm-MVU TUI | **bubbletea** ★44k · huh ★7.1k · tview ★14k | **Pilot-now** pattern→Python TUI |
| Style / markdown TTY | lipgloss ★12k · glow ★27k | Pilot-now presenters |
| Tape demos | vhs ★21k | Pilot-later CLI fixtures |

### G4 Policy · G5 Observability · G6 Release · G7 Mesh (pattern only)
- **G4:** OPA ★12k · Conftest ★3.2k · Kyverno ★8k — Pattern/Pilot-later sensor ([2603.15799](https://arxiv.org/abs/2603.15799))  
- **G5:** Prometheus ★66k · OTel Collector ★7.4k — Pattern metrics; Pilot-later export  
- **G6:** goreleaser ★16k · Trivy ★37k · **Syft** ★9.4k · cosign ★6.2k — **Pilot-now** SBOM/vuln sensors  
- **G7:** Istio/Linkerd/Cilium — Pattern only; **Refuse** mesh-as-product ([2207.00592](https://arxiv.org/abs/2207.00592))

**Bloom Create (Go):** HITL TUI · versioned plugins · SBOM sensors · admission-metaphor gates.

---

## 3. Ruby — domains & subdomains

### Logos (excellence)
Rails ★59k · RuboCop ★13k · Brakeman ★7.3k · Sidekiq ★14k · Asciidoctor ★5.2k · Sorbet ★3.8k · RBS ★2.2k · ruby-lsp ★2.0k · Packwerk ★1.9k · YARD ★2.0k · Thor ★5.3k

| Domain | Key subdomains | Exemplars | Research | Pilot |
| --- | --- | --- | --- | --- |
| **R1 Rails SA/security** | Rails taint SA · lint cops · parser AST | Brakeman · RuboCop · rubocop-rails | YASA [2601.17390](https://arxiv.org/abs/2601.17390) | **Pilot-now** SARIF |
| **R2 DX CLIs** | Thor generators · Lefthook · Scientist | Thor · Shopify/cli · Scientist ★7.7k | — | Pattern |
| **R3 Gradual types/LSP** | Sorbet · RBS · ruby-lsp | Sorbet · Tapioca · ruby-lsp | [2007.12630](https://arxiv.org/abs/2007.12630) · LspFuzz [2510.00532](https://arxiv.org/abs/2510.00532) | Pilot-later sensors |
| **R4 Docs/publishing** | AsciiDoc · YARD | **Asciidoctor** · YARD | AsciiDoc Spec | **Pilot-now** sink |
| **R5 Modular monolith** | Packwerk · Zeitwerk | Packwerk · Zeitwerk | [2401.11867](https://arxiv.org/abs/2401.11867) | Pilot-later (~tach) |
| **R6 Job topology** | Sidekiq / Puma split | Sidekiq · Puma | — | Pattern |
| **R7 Meta-aware tooling** | DSL/macro SA | RuboCop · Sorbet · YARD | [1711.09281](https://arxiv.org/abs/1711.09281) | Pattern→Stage-0 packs |

**Bloom Create (Ruby):** AsciiDoc Create · Rails finding packs · package-boundary fitness · typed claim assists.

---

## 4. Clojure — domains & subdomains

### Logos (excellence)
Clojure ★11k · DataScript ★5.8k · Babashka ★4.6k · CIDER ★3.7k · XTDB ★3.0k · clj-kondo ★1.8k · Malli ★1.8k · Schema ★2.5k · Component ★2.2k · Clerk ★2.1k · core.async ★2.0k · rewrite-clj ★0.7k · SCI ★1.4k · Transit ★1.9k

| Domain | Key subdomains | Exemplars | Research | Pilot |
| --- | --- | --- | --- | --- |
| **C1 REPL / interactive** | nREPL+CIDER · Clerk notebooks · tools.namespace | CIDER · Clerk · tools.namespace | Hickey talks | Pattern → marimo kin |
| **C2 EDN / Transit / immutability** | EDN envelopes · Transit wire · persistent colls | edn · transit · clojure | [2003.07395](https://arxiv.org/abs/2003.07395) | Pilot-later dual-sink |
| **C3 Contracts** | Malli/Spec/Schema · Typed Clojure | Malli · Schema · spec.alpha | [1812.03571](https://arxiv.org/abs/1812.03571) · [1909.08965](https://arxiv.org/abs/1909.08965) | Pattern→Pilot-later contracts |
| **C4 Fact/time models** | EAV/Datalog · bitemporal · Pathom | DataScript · XTDB · Datalevin | Formulog [2009.08361](https://arxiv.org/abs/2009.08361) | Pilot-later FACT0 |
| **C5 Language tooling** | clj-kondo · clojure-lsp · style guides | clj-kondo · clojure-lsp | [2605.24049](https://arxiv.org/abs/2605.24049) | Pilot-later if targets |
| **C6 Concurrent architecture** | CSP · Component/Integrant · re-frame | core.async · Component · re-frame | Discourje [2407.00540](https://arxiv.org/abs/2407.00540) | Pattern |
| **C7 Babashka CLIs** | Native scripts · SCI · Joker | **Babashka** · SCI · Joker | SCI docs | Pilot-later ops sidecar |
| **C8 Code-as-data** | rewrite-clj · grasp · SCI DSLs | rewrite-clj · edamame · grasp | [1905.09950](https://arxiv.org/abs/1905.09950) | Pattern (ast-grep SoT) |

**Bloom Create (Clojure):** Contract registries · as-of fact audits · bb ops recipes · moldable review notebooks · macro-aware pack patterns.

**Refuse:** Clojure tip kernel · SCI as merge authority.

---

## 5. WASM — domains & subdomains (platform excellence)

### Logos
wasmer ★21k · wasmtime ★18k · pyodide ★15k · WasmEdge ★11k · wasm-bindgen ★9.1k · workerd ★8.6k · wasm3 ★8.0k · Spin ★6.5k · Extism ★5.7k · wazero ★6.3k · component-model ★1.4k · wit-bindgen ★1.4k · javy ★2.7k · vscode-wasm ★0.5k · cosign ★6.2k (attest)

| Domain | Key subdomains | Why WASM excels | Pilot |
| --- | --- | --- | --- |
| **1 Portable plugins/PDKs** | In-proc PDK · deny-by-default ABI · vs go-plugin | Cross-lang guest; SFI sandbox | Pilot-later Extism after bwrap |
| **2 Polyglot guests** | Language PDKs · WIT · Javy/ruby.wasm | One host, many guest langs | Defer until demand |
| **3 Edge/serverless** | Spin/workerd cold-start · runwasi | Tiny images / fast start | **Pattern only** (not tip) |
| **4 Browser/editor** | vscode-wasm · bindgen · pyodide | Extension sandbox | Pattern/Defer |
| **5 Capability WASI/CM** | WIT worlds · WASI 0.2 · confused-deputy notes | Least privilege imports | Pattern design language |
| **6 Portable libs** | One artifact many OS · RLBox | Replace `.so` matrix pain | Pilot-later if measured |
| **7 Agent isolation** | Untrusted tool bodies · CapSeal · fuel limits | Import-gated LLM tools | Pilot-later after OS jail |
| **8 Attestation** | OCI+cosign · provenance | Signed portable modules | Pilot-later with guests |

**Papers:** Gobi [1912.02285](https://arxiv.org/abs/1912.02285) · Not So Fast [1901.09056](https://arxiv.org/abs/1901.09056) · Twine [2103.15860](https://arxiv.org/abs/2103.15860) · Wasm security [2407.12297](https://arxiv.org/abs/2407.12297) · SpecBox [2607.23933](https://arxiv.org/abs/2607.23933) · CapSeal [2604.16762](https://arxiv.org/abs/2604.16762) · eWAPA [2409.10252](https://arxiv.org/abs/2409.10252).

**Where WASM does *not* excel:** tip SoT · I/O-heavy tools · first isolation layer · “Wasm = secure” theater · a11y/TUI.

---

## 6. Unified pilot scoreboard (depth → action)

| # | Pilot | From excellence of | Bucket |
| ---: | --- | --- | --- |
| 1 | Keep Embodied Rust wheels (ast-grep, ruff, tach, complexipy) | Rust R2/R3 | Embody |
| 2 | Asciidoctor sink | Ruby R4 | **Pilot-now** |
| 3 | Brakeman/RuboCop SARIF | Ruby R1 | **Pilot-now** |
| 4 | Charm/Bubble Tea → dual-sink TUI patterns | Go G3 | **Pilot-now** |
| 5 | go-plugin shape for language sensors | Go G2 | **Pilot-now** |
| 6 | Syft/Trivy SARIF sensors | Go G6 | **Pilot-now** |
| 7 | clap/gh CLI contract polish | Rust R2 · Go G1 | Pattern |
| 8 | Malli/Spec → closed contract registry | Clojure C3 | Pattern→Pilot-later |
| 9 | DataScript/XTDB patterns → FACT0 | Clojure C4 | Pilot-later |
| 10 | Profiled maturin bin | Rust R6 | Pilot-now if profiled |
| 11 | bubblewrap then Extism guest | WASM 7→1 | Pilot-now → Pilot-later |
| 12 | Packwerk ↔ tach vocabulary | Ruby R5 | Pilot-later |
| 13 | Babashka ops scripts | Clojure C7 | Pilot-later |
| 14 | OPA/Conftest policy packets | Go G4 | Pilot-later |
| 15 | Mesh/operator as product | Go G7 | **Refuse** (category) |

---

## 7. Spec **E-LANG0** (DRAFT)

| ID | Decision |
| --- | --- |
| **LANG0-1** | Excellence maps (this memo) are Spec SoR for *where* each language is allowed to contribute |
| **LANG0-2** | Logo tables are landing pads — ★ ≠ architecture proof |
| **LANG0-3** | Subdomain pilots inherit POLY0b five buckets + keep/drop exits |
| **LANG0-4** | Clojure added as first-class excellence language (was under-covered in memo 40) |
| **LANG0-5** | WASM scoped as **guest platform** domains only — not tip rewrite |
| **LANG0-6** | Approve unlocks Pilot-now rows 2–7 only (one tip stream) |

---

## 8. Adversarial checklist

- [ ] Depth used to justify tip polyglot kernel? → Refuse  
- [ ] Logo project without keep/drop? → incomplete Spec  
- [ ] Clojure/Ruby/WASM writing oracle? → Refuse  
- [ ] Mesh papers used as product justification? → Refuse  
- [ ] WASM Pilot before bwrap result? → out of order  

---

## 9. Exit

Deep excellence maps landed for **Rust · Go · Ruby · Clojure · WASM**: domains → subdomains → logo exemplars → pilot buckets. Amends E-POLY0b. **No Implement** until E-LANG0 / Spike Specs. Siblings: process/39–40 · E-RUST0 · dimensional map.
