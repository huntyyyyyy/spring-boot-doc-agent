# Rust (and Rust-core) quality toolscape — BFS then DFS (2026)

**Date:** 2026-08-09  
**Product:** `doc-engine` / huntyyyyyy/spring-boot-doc-agent (Python CLI, deterministic gates, coding-agent workflow)  
**Status:** RESEARCH COMPLETE — Spec-only epic **E-RUST0** (amend **E-RT0**; do not implement product code in this pass)  
**Claim tiers:** `[Evidenced]` primary paper/docs/API · `[Confirmed]` this checkout · `[Unknown]` missing ID, blocked cartography, or open product choice  
**Prior (too narrow):** [`32-realtime-architecture-assertion-agents-2026.md`](32-realtime-architecture-assertion-agents-2026.md)  
**SoT siblings:** `se-quality-synthesis-2026-08-08.md` · `docs/design/rust-stack-fit-memo-2026-08-08.md` · `08-rust-test-runners-bottlenecks.md` · `09-test-adequacy-vs-coverage-inflation-2026.md` · `modularity/20-tach-dependency-blueprint-2026.md` · `process/19-watch-stalker-agents-context-lean-2026.md`

**Star counts:** GitHub REST API, fetched **2026-08-09**, unless marked `[Unknown]`.

---

## Verdict (one page)

| Question | Answer |
| --- | --- |
| Does Rust improve architecture / quality / faults / assumptions / LLM witnesses for *this* repo? | **Yes — almost entirely as Embodied wheels/CLIs and as pattern libraries**, not as an in-tree rewrite. The winning Rust-core surface is already pinned: **ast-grep, ruff, tach, complexipy**. Adjacent Rust tools (uv, ty, pyrefly, py-spy, samply, maturin, cargo-\* patterns) expand **sensors and profiled helpers**, never a second Cover% SoT. |
| What did memo 32 miss? | It framed Rust as a footnote to “real-time architecture assertion.” It under-enumerated **fuzz/sanitizer analogs, mutation/differential coverage, SBFL, SBOM/supply-chain, profiling/debug, formal contracts, packaging, IDE/type-checkers beyond pyright, and metrics-beyond-Cover%**. It treated cargo-\* mostly as refuse theater without a **BFS catalog → DFS Embody/Adopt/Refuse** map. |
| Embody / Adopt / Refuse? | **Embody** existing Rust CLIs + oracle/claims/tach/ast-grep mandate. **Adopt** (Spec-gated): E-RT0 incremental fitness pack; tool receipts; pip-audit/OSV **sensors**; Hypothesis deepening; optional profiled maturin **bin**; ty/basedpyright Spike; py-spy/samply for stalker bottlenecks. **Refuse** in-tree Cargo workspace; WASM/wasmtime product runtime; Miri/ASan as Python merge gates; cargo-fuzz as product dep; LLM-as-judge / SemLoc as 98.7 SoT; oxc/biome as Python SoT; fuzzy/PID green. |
| Motivating failure | Local sensor green ≠ remote oracle 98.7. Expanding the toolscape must **widen deterministic envelopes**, not invent a third Cover%-shaped SoT. |

**Bottom line:** Treat Rust as a **capability marketplace of engines we consume**, mapped category-by-category. Memo 32’s E-RT0 remains valid for edit-time architecture + receipts; **E-RUST0** is the Spec-only amendment that inventories the rest of the marketplace and binds each item to existing gates (`pre_pr`, oracle, tach, ast-grep, ruff, claims, stalker, CodeQL, Semgrep) without softening constitution invariants. **Widened 2026-08-10:** polyglot BFS (WASM/Go/TS/PyO3/…) lives in [`process/39-polyglot-cli-toolkit-bfs-2026-08-10.md`](../process/39-polyglot-cli-toolkit-bfs-2026-08-10.md) as **E-POLY0** (amends this epic; does not replace Embody-wheels).

**Constitution (do not soften):** whole-repo Cover% **98.7** boolean SoT · climb ≠ oracle · complexipy ≤5 · LOC ≤225 · no `utils/` · descriptive names · refuse in-tree Rust unless profiled · Embody via wheels/CLIs OK · no LLM-as-judge SoT · no fuzzy/PID green · Spec → Implement → Verify → Archive.

---

## Gap vs memo 32

| Memo 32 covered well | Memo 32 under-covered / missed |
| --- | --- |
| Agent LTL/SMT / receipts / Spec Kit probing | Full **BFS categories** (fuzz, SBOM, debug, packaging, formal contracts, metrics-beyond-Cover%) |
| tach / ast-grep / ruff / complexipy Embody | **ty / pyrefly / basedpyright**, oxc/biome as *pattern* sources |
| Real-time vs gate-only table | **Differential coverage**, behavioural-gap metrics, SBFL/SemLoc as **sensors not SoT** |
| cargo-deny / Clippy refuse as product deps | **cargo-fuzz, AFL++, Miri, ASan/Atheris analogs**, cargo-geiger, cargo-show-asm **patterns** |
| maturin only as conditional Adopt | **py-spy / austin / samply** stalker profiling lane |
| WASM refuse one-liner | Explicit **wasmtime/wasmer refuse** + why category error for CLI gates |
| Fitness = tach check | **Nygard/Thoughtworks architectural fitness functions** as sensor vocabulary (not a product framework) |
| E-RT0 tickets | Need **E-RUST0** Spec tickets for supply-chain, fuzz, profiling, type-checker Spike, profiled helper gate |

---

## BFS catalog (categories × tools)

Stars = GitHub `stargazers_count` on **2026-08-09**. Language column is primary GitHub language (Rust-core tools may still ship Python wheels). Stance is a **first-pass** Embody/Adopt/Refuse for *this* product; DFS sections refine the top eight.

### 1. Architecture / dependency fitness

| Tool / source | ★ | Core | What it enforces (compressed) | Stance |
| --- | --- | --- | --- | --- |
| [tach-org/tach](https://github.com/tach-org/tach) | 2786 | Rust | `depends_on`, interfaces, layers, **no cycles** | **Embody** (cycles); **Adopt** map (E-TACH0) |
| Thoughtworks / Ford–Parsons fitness functions | n/a | pattern | Objective architectural characteristic checks as continual verification | **Adopt pattern** (sensors ≠ Cover%) |
| [obi1kenobi/cargo-semver-checks](https://github.com/obi1kenobi/cargo-semver-checks) | 1667 | Rust | SemVer API breakage for crates | **Refuse dep**; **Adopt pattern** → façade poke |
| [EmbarkStudios/cargo-deny](https://github.com/EmbarkStudios/cargo-deny) | 2396 | Rust | License/ban/advisory/source lint | **Refuse dep**; supply-chain pattern → §7 |
| ArchUnit / pytestarch / grimp | vary | JVM/Py | Import/layer rules | **Refuse** dual-SoT with tach (see E-TACH0) |
| Nygard “release it” / fitness reviews | n/a | pattern | Operability as measurable fitness | **Adopt vocabulary** only |

### 2. Static quality / lint / complexity

| Tool / source | ★ | Core | What it enforces | Stance |
| --- | --- | --- | --- | --- |
| [astral-sh/ruff](https://github.com/astral-sh/ruff) | 49117 | Rust | Lint + format | **Embody** |
| [rohaquinlop/complexipy](https://github.com/rohaquinlop/complexipy) | 748 | Rust | Cognitive complexity | **Embody** ≤5 (pinned exception to ★ bar) |
| [rust-lang/rust-clippy](https://github.com/rust-lang/rust-clippy) | 13433 | Rust | Rust lints | **Refuse product dep**; lint-culture analogy |
| [oxc-project/oxc](https://github.com/oxc-project/oxc) | 22261 | Rust | JS/TS parser/linter/transformer | **Refuse** as Python SoT; speed/arch pattern only |
| [biomejs/biome](https://github.com/biomejs/biome) | 25539 | Rust | JS/TS lint+format | Same as oxc |
| Size ratchet (in-repo) | n/a | Python | LOC ≤225 | **Embody** `[Confirmed]` |
| [PyCQA/bandit](https://github.com/PyCQA/bandit) | 8201 | Python | Security lint | **Adopt sensor** optional; Semgrep/CodeQL already Stage-0/SAST |

### 3. Incremental / structural analysis

| Tool / source | ★ | Core | What it enforces | Stance |
| --- | --- | --- | --- | --- |
| [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) | 15456 | Rust | Structural search/lint/rewrite; CLI+LSP | **Embody** Stage-0 + citation mandate |
| [tree-sitter/tree-sitter](https://github.com/tree-sitter/tree-sitter) | 26589 | Rust | Incremental parsers | **Refuse replace** ast-grep; underlying grammar tech |
| [tree-sitter/py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter) | 1481 | C/bindings | Python bindings | **Refuse** dual structural SoT |
| [Instagram/LibCST](https://github.com/Instagram/LibCST) | 1934 | Python | Concrete syntax trees | **Defer**; not citation SoT |
| [semgrep/semgrep](https://github.com/semgrep/semgrep) | 16162 | OCaml | Pattern SAST | **Embody** Stage-0 backend |
| [github/codeql](https://github.com/github/codeql) | 9923 | CodeQL | QL scanning | **Embody** pack + E-CQL0 |

### 4. Runtime / faults / UB analogs

| Tool / source | ★ | Core | What it enforces | Stance |
| --- | --- | --- | --- | --- |
| [rust-lang/miri](https://github.com/rust-lang/miri) | 6481 | Rust | Interpreter detects UB in Rust | **Refuse product**; pattern = “fail closed on undefined” |
| [google/sanitizers](https://github.com/google/sanitizers) | 12443 | C | ASan/TSan/UBSan | **Refuse** as Python merge gate; relevant only if native ext |
| [google/atheris](https://github.com/google/atheris) | 1658 | Python | libFuzzer + optional ASan on C ext | **Adopt Spike** if native deps appear; else **Defer** |
| CPython / pytest exceptions | n/a | Python | Soft “faults” are exceptions/asserts | **Embody** suite + oracle |
| Hypothesis health checks | 8857 | Python | Flaky/invalid data detection | **Embody pattern** (E-QA3) |

### 5. Fuzz / property-based

| Tool / source | ★ | Core | What it enforces | Stance |
| --- | --- | --- | --- | --- |
| [HypothesisWorks/hypothesis](https://github.com/HypothesisWorks/hypothesis) | 8857 | Python | Property-based tests | **Embody** / deepen (E-QA3) |
| [rust-fuzz/cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz) | 1875 | Rust | libFuzzer cargo integration | **Refuse product dep**; pattern for harness shape |
| [AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus) | 6703 | C | Coverage-guided fuzzing | **Refuse product**; pattern only |
| [jwilk/python-afl](https://github.com/jwilk/python-afl) | 373 | Python | AFL for Python | **Refuse** (&lt;1k★ + niche) |
| [google/atheris](https://github.com/google/atheris) | 1658 | Python | Coverage-guided Python fuzz | **Adopt Spike** for parsers/fixtures |
| [schemathesis/schemathesis](https://github.com/schemathesis/schemathesis) | 3512 | Python | API schema property tests | **Refuse** (no HTTP product surface) |
| [google/oss-fuzz](https://github.com/google/oss-fuzz) | 12531 | Shell | Continuous fuzz service | **Refuse** until public fuzz targets exist |

### 6. Mutation / adequacy

| Tool / source | ★ | Core | What it enforces | Stance |
| --- | --- | --- | --- | --- |
| [boxed/mutmut](https://github.com/boxed/mutmut) | 1379 | Python | Mutation testing | **Adopt sensor** (already advisory `--full`) |
| in-repo `mutation_driver` | n/a | Python | Adequacy advisory | **Embody** `[Confirmed]` |
| Metamorphic / rule fixtures | n/a | Python | Stage-0 metamorphic corpus | **Embody** |
| PIT / operator zoo | n/a | JVM | Mutation operators | **Refuse** (constitution) |
| arXiv:2607.22880 (cov/mutation vs effectiveness) | n/a | paper | Context-dependent usefulness of cov/mutation | **Evidenced** — sensors ≠ SoT |

### 7. SBOM / supply-chain

| Tool / source | ★ | Core | What it enforces | Stance |
| --- | --- | --- | --- | --- |
| [rustsec/rustsec](https://github.com/rustsec/rustsec) (+ cargo-audit) | 1932 | Rust | Rust advisory DB + audit tooling | **Refuse product**; pattern → pip-audit/OSV |
| [geiger-rs/cargo-geiger](https://github.com/geiger-rs/cargo-geiger) | 1644 | Rust | `unsafe` usage tally | **Refuse**; no in-tree Rust |
| [pypa/pip-audit](https://github.com/pypa/pip-audit) | 1345 | Python | Audit pinned deps vs advisories | **Adopt sensor** Spec |
| [google/osv-scanner](https://github.com/google/osv-scanner) | 10791 | Go | OSV vuln scan | **Adopt sensor** optional |
| [anchore/syft](https://github.com/anchore/syft) / [grype](https://github.com/anchore/grype) | 9368 / 12706 | Go | SBOM + vuln | **Defer** (CLI app, not container image SoT) |
| [aquasecurity/trivy](https://github.com/aquasecurity/trivy) | 37323 | Go | Broad scanner | **Defer** / optional CI |
| [CycloneDX/cyclonedx-python](https://github.com/CycloneDX/cyclonedx-python) | 389 | Python | SBOM emit | **Unknown**/Defer (&lt;1k★) |
| requirements pin + claims | n/a | repo | Exact pins; PATH version gates | **Embody** `[Confirmed]` |

### 8. Debugging / observability / profiling

| Tool / source | ★ | Core | What it enforces | Stance |
| --- | --- | --- | --- | --- |
| [benfred/py-spy](https://github.com/benfred/py-spy) | 15424 | Rust | Sampling profiler (no code change) | **Adopt** local/stalker profiling |
| [mstange/samply](https://github.com/mstange/samply) | 4364 | Rust | Firefox Profiler–compatible sampler | **Adopt** optional (native/CLI) |
| [P403n1x87/austin](https://github.com/P403n1x87/austin) | 2211 | C | Frame sampler | **Defer** (py-spy preferred) |
| [flamegraph-rs/flamegraph](https://github.com/flamegraph-rs/flamegraph) | 5993 | Rust | Flamegraphs for Rust | **Refuse product**; pattern |
| [pacak/cargo-show-asm](https://github.com/pacak/cargo-show-asm) | 969 | Rust | Show asm/MIR/LLVM-IR | **Refuse** (&lt;1k★ + no Rust tree); pattern for “show generated form” |
| [rr-debugger/rr](https://github.com/rr-debugger/rr) | 10614 | C++ | Record/replay | **Defer** rare CI flake hunts |
| [RadareOrg/radare2](https://github.com/radareorg/radare2) | 24537 | C | Reverse engineering | **Refuse** for product workflow |
| Suite stalker sensors (E-RUN/E-STK) | n/a | Python | Timing/plateau ledger | **Embody** sensors `[Confirmed]` |
| [open-telemetry/opentelemetry-python](https://github.com/open-telemetry/opentelemetry-python) | 2580 | Python | Tracing SDK | **Defer**; not merge SoT |

### 9. Formal methods / contracts

| Tool / source | ★ | Core | What it enforces | Stance |
| --- | --- | --- | --- | --- |
| [Z3Prover/z3](https://github.com/Z3Prover/z3) | 12538 | C++ | SMT solver | **Adopt pattern** for *tool-call* gates only (E-RT0 Spike); **Refuse** merge-path Z3 without precision audit |
| AgentLTL / Agent-C / VIGIL (arXiv) | n/a | papers | LTL/SMT over tool traces | **Adopt Spike** (memo 32) |
| ToolGate [arXiv:2601.04688](https://arxiv.org/abs/2601.04688) | n/a | paper | Hoare contracts on tools | **Adopt pattern** for PreToolUse |
| [life4/deal](https://github.com/life4/deal) | 903 | Python | Design-by-contract | **Refuse** (&lt;1k★) as SoR; pattern OK |
| [Parquery/icontract](https://github.com/Parquery/icontract) | 411 | Python | Contracts | **Refuse** (&lt;1k★) |
| EG-VAR Lean sidecar [arXiv:2607.12650](https://arxiv.org/abs/2607.12650) | n/a | paper | Kernel-attested claims | **Refuse** as merge runtime; **Adopt** “abstain > fake Verified” ethic |

### 10. LLM / agent witnesses & receipts

| Tool / source | ★ | Core | What it enforces | Stance |
| --- | --- | --- | --- | --- |
| Tool Receipts / NabaOS [2603.10060](https://arxiv.org/abs/2603.10060) | n/a | paper | HMAC receipts; epistemic claim classes | **Adopt** (E-RT0) |
| ToolGate [2601.04688](https://arxiv.org/abs/2601.04688) | n/a | paper | Pre/postconditions on tools | **Adopt pattern** |
| EG-VAR [2607.12650](https://arxiv.org/abs/2607.12650) | n/a | paper | Lean-attested tool descent | **Refuse** full Lean stack; ethic OK |
| Reason Less, Verify More [2607.07405](https://arxiv.org/abs/2607.07405) | n/a | paper | Deterministic pre-exec gates; audit precision | **Embody principle** |
| Real-Time Detection/Repair [2608.02464](https://arxiv.org/abs/2608.02464) | n/a | paper | Deterministic verifiers &gt; LLM auditor | **Embody principle** |
| in-repo deny hooks + claims | n/a | Python | No Grep; no raw curl; claim predicates | **Embody** `[Confirmed]` |
| Guardrails / OPA | 7263 / 12086 | Py/Go | LLM I/O / Rego policy | **Refuse** as Cover%/arch SoT |

### 11. Metrics beyond Cover%

| Tool / source | ★ | Core | What it measures | Stance |
| --- | --- | --- | --- | --- |
| coverage.py + fail_under 98.7 | 3405 | Python | Line/branch Cover% | **Embody oracle** |
| Climb / gap-average / PathCohesion | n/a | Python | Sensors | **Embody**; ≠ floor |
| diff-cover ([Bachmann1234/diff_cover](https://github.com/Bachmann1234/diff_cover)) | 842 | Python | New-code coverage | **Embody** near-gate (★ bar exception — already in quality_gates) |
| Differential coverage ([riesentoaster/differential-coverage](https://github.com/riesentoaster/differential-coverage)) | 4 | Python | Relcov between approaches | **Refuse tool** (&lt;1k★); **Adopt concept** for climb-vs-oracle honesty |
| Behavioural gaps [arXiv:2606.10417](https://arxiv.org/abs/2606.10417) | n/a | paper | Untested expected behaviours | **Adopt sensor research**; refuse as 98.7 |
| SBFL classical + SemLoc [2603.29109](https://arxiv.org/abs/2603.29109) | n/a | paper | Suspiciousness / semantic spectra | **Adopt Spike** as debug sensor; **Refuse** merge SoT / LLM-judge floor |
| Metamorphic coverage [2508.16307](https://arxiv.org/html/2508.16307) | n/a | paper | MR adequacy lighter than mutation | **Adopt pattern** (already metamorphic fixtures) |
| complexipy / size / tach / claims | n/a | mixed | Complexity, LOC, deps, doc truth | **Embody** multi-metric envelope |

### 12. IDE / LSP real-time

| Tool / source | ★ | Core | What it enforces | Stance |
| --- | --- | --- | --- | --- |
| ast-grep LSP | (same) | Rust | Structural diagnostics in editor | **Embody** |
| ruff LSP / VS Code ext | 1663 (ext) | Rust | Lint-on-type | **Embody** |
| [microsoft/pyright](https://github.com/microsoft/pyright) | 15578 | TypeScript | Static types | **Spike** (memo 32 RT-S1) |
| [DetachHead/basedpyright](https://github.com/DetachHead/basedpyright) | 3523 | TypeScript | Strict pyright fork | **Spike** with pyright |
| [astral-sh/ty](https://github.com/astral-sh/ty) | 19433 | Python/Rust | Astral type checker (emerging) | **Spike** — watch maturity |
| [facebook/pyrefly](https://github.com/facebook/pyrefly) | 6864 | Rust | Meta type checker | **Spike** / Defer dual checkers |
| [python/mypy](https://github.com/python/mypy) | 20587 | Python | Gradual typing | **Defer** if pyright/ty chosen |

### 13. Packaging / wheels / native helpers

| Tool / source | ★ | Core | What it provides | Stance |
| --- | --- | --- | --- | --- |
| [PyO3/maturin](https://github.com/PyO3/maturin) | 5742 | Rust | Build wheels / bin bridges | **Adopt** only after profile; prefer **bin** |
| [PyO3/pyo3](https://github.com/PyO3/pyo3) | 16009 | Rust | Rust↔Python FFI | Same gate as maturin |
| [astral-sh/uv](https://github.com/astral-sh/uv) | 88542 | Rust | Fast resolver/installer | **Adopt optional** local DX; not Cover% SoT |
| [bytecodealliance/wasmtime](https://github.com/bytecodealliance/wasmtime) | 18495 | Rust | Wasm runtime | **Refuse** product runtime |
| [wasmerio/wasmer](https://github.com/wasmerio/wasmer) | 20946 | Rust | Wasm runtime | **Refuse** |
| [indygreg/PyOxidizer](https://github.com/indygreg/PyOxidizer) | 6141 | Rust | Freeze Python apps | **Refuse** (packaging theater) |
| Existing PyPI wheels (ruff, ast-grep-cli, …) | n/a | mixed | PATH pins | **Embody** |

---

## DFS — top 8 categories (deep)

Selection criterion: highest leverage for **Python CLI + coding-agent + existing gate graph**, not generic “Rust is cool.”

### DFS-1 — Architecture / dependency fitness

**Enforces:** Declared module edges, cycles, (future) layers/interfaces; architectural *characteristics* as objective checks (Thoughtworks fitness functions: “where’s the data and how do I get to it?” — usually 10–15 lines of script, not a platform).

**Fit to gates:**

| Gate | Fit |
| --- | --- |
| `tach.toml` / `tach check` in quality_gates | **Embody** cycles today; E-TACH0 for layers/`depends_on` |
| façade poke / public_surface | SemVer-checks **pattern** |
| pre_pr | Near-gate; RT pack candidate |
| oracle Cover% | Orthogonal — never substitute |

**Embody:** tach cycles; fitness-function *vocabulary* for claims/tach/size.  
**Adopt:** E-TACH0 map; incremental `tach check` in RT pack (E-RT0).  
**Refuse:** ArchUnit dual-SoT; `tach sync` as architecture Approve; mesh/Backstage “architecture platform.”

**Open Spec questions:** (1) Which BC layers become tach `layers` first? (2) Are fitness functions documented as sensors in CONTRIBUTING or only in research? (3) Does façade poke need a semver-break *sensor* name without claiming cargo-semver-checks?

---

### DFS-2 — Static quality (ruff / complexipy / size / JS-Rust linters as analogy)

**Enforces:** Style, bugclass lint, cognitive complexity ≤5, file LOC ≤225. oxc/biome show what a Rust-core monorepo linter looks like for *other* languages — useful as **existence proof**, not a dep.

**Fit:** `pre_pr` + `quality_gates` + CI. Already the wall-clock win from Rust.

**Embody:** ruff, complexipy, size ratchet.  
**Adopt:** none required for static lane beyond RT touched-path scoping.  
**Refuse:** Clippy/oxc/biome as product gates; raising complexipy/LOC ceilings.

**Open Spec:** Should touched-path complexipy fail the agent loop or only warn until whole-repo gate? (Prefer fail on touched files — still ≠ oracle.)

---

### DFS-3 — Incremental structural analysis (ast-grep vs tree-sitter)

**Enforces:** Structural pattern presence for Stage-0 signals and citation correctness. tree-sitter is the grammar substrate ecosystem; **ast-grep** is the productized structural search we pin. Dual SoT (LibCST + ast-grep + tree-sitter queries) would recreate the Grep-vs-structure failure mode CLAUDE.md forbids.

**Fit:** Stage-0 scanners, `rule_coverage`, claims citation discipline, LSP edit-time.

**Embody:** ast-grep CLI + YAML rules + grammar-care (zero match ≠ absence).  
**Adopt:** `ast-grep-py` only if profiled subprocess/JSON chunking dominates.  
**Refuse:** Replacing ast-grep with raw tree-sitter queries in-agent; text grep.

**Open Spec:** Which rule subset is safe for RT pack (fast, no Stage-0 corpus compile)?

---

### DFS-4 — LLM / agent witnesses & receipts

**Enforces:** Tool results actually happened; ordering/policy on tool streams; claims about paths/gates are grounded. Papers: NabaOS receipts, ToolGate Hoare contracts, AgentLTL, Reason-Less-Verify-More precision audit, EG-VAR abstention ethic (refuse full Lean).

**Fit:** Claude `PreToolUse` deny hooks (text-search, raw network) already **real-time**; `check_repo_claims.py` is near-gate; E-RT0 wants receipts composed with denies.

**Embody:** deny hooks + claims.  
**Adopt:** hash/HMAC receipts Spec; narrow LTL templates Spike; ToolGate-style preconditions for “edit CONSTRAINTS / fail_under.”  
**Refuse:** ZK proofs; LLM-as-judge green; Guardrails/OPA as Cover% SoT; Lean kernel in merge path.

**Open Spec:** Receipt store location (session artifact vs CI)? Forged “I ran pytest” fixture shape for harness tests?

---

### DFS-5 — Metrics beyond Cover% (mutation, differential, SBFL, behavioural gaps)

**Enforces / measures:** Discrimination power (mutation survivors), new-code floors (diff-cover), approach-vs-approach coverage (differential concept), suspiciousness for debug (SBFL/SemLoc), behavioural gaps vs docs (2606.10417).

**Critical honesty:** 2607.22880 — cov/mutation usefulness is **context-dependent**; when CUT may be buggy, Cover% is unreliable as bug-detection proof. SemLoc (2603.29109) beats SBFL on semantic faults but uses LLMs in the loop → **sensor / research only**, never fail_under substitute.

**Fit:** oracle XML SoT; climb sensors; `mutation_driver` advisory; adequacy_summary (E-QA); stalker findings.

**Embody:** 98.7 oracle; climb ≠ floor; advisory mutation/metamorphic.  
**Adopt:** document differential-coverage *concept* for climb-vs-oracle; optional SBFL Spike on failing oracle triage.  
**Refuse:** SemLoc/LLM-FL as merge SoT; riesentoaster tool (&lt;1k★); PIT zoo; climb as floor.

**Open Spec:** Does E-QA gain a “behavioural gap” Spike, or stay mutator+metamorphic only?

---

### DFS-6 — Fuzz / property (Hypothesis, Atheris, cargo-fuzz patterns)

**Enforces:** Input-space exploration; properties/invariants; for Atheris+ASan, memory bugs in **native** extensions.

**Fit:** E-QA3 Hypothesis spike; Stage-0 fixture parsers are the only plausible fuzz targets; no C-ext surface in doc-engine core today `[Confirmed]` pins are wheels/CLIs not in-tree `.so` product code.

**Embody:** Hypothesis as property pattern.  
**Adopt:** HypoFuzz/Atheris Spike **only** for pure parsers (signals JSON, claims predicates) with timeout budgets.  
**Refuse:** cargo-fuzz/AFL++ product deps; OSS-Fuzz onboarding without targets; python-afl (&lt;1k★).

**Open Spec:** Which pure function is the first Hypothesis property (fingerprint? claims predicate evaluation?)?

---

### DFS-7 — SBOM / supply-chain (cargo-deny/audit → pip-audit/OSV)

**Enforces:** Known advisories, license/ban policies, pin freshness. Rust’s cargo-deny/geiger/audit are **pattern donors**; Python equivalent is pip-audit + OSV + strict pins + PATH version gates (already for ast-grep/semgrep).

**Fit:** requirements pins; CI version gates; optional `pre_pr` advisory step; **not** oracle.

**Embody:** pin discipline + tool version gates.  
**Adopt:** `pip-audit` (or osv-scanner) as **non-blocking or warn-gate** Spec under E-RUST0; document cargo-deny ↔ pip-audit analogy.  
**Refuse:** cargo-deny/geiger as product gates; Trivy-everything dashboard as SoT; CycloneDX theater without consumer.

**Open Spec:** Fail CI on high severity, or advisory artifact only? Allowlist process for transitive noise?

---

### DFS-8 — Debugging / observability (py-spy, samply, stalker)

**Enforces:** Nothing about correctness — **explains** wall-clock and stalls. Memo 08 / E-RUN already refuse “Rust stalker product as oracle.” py-spy/samply are the missing **concrete profilers** memo 32 never named.

**Fit:** E-RUN plateau sensors; local diagnosis when pre_pr/oracle slow; agent “why is this stuck” cards.

**Embody:** stalker timing sensors.  
**Adopt:** documented py-spy (and optional samply) recipe in process docs / tool-quirks; link from E-RUN.  
**Refuse:** Always-on profiler in CI oracle cell; radare/gdb as agent defaults; cargo-show-asm without Rust tree.

**Open Spec:** Is py-spy a documented **human** recipe only, or an agent-invokable tool with receipt?

---

## Cross-cutting: packaging & type-checkers (BFS 12–13, short DFS)

| Item | Stance | Note |
| --- | --- | --- |
| maturin/pyo3 helper | **Adopt iff profiled** | Prefer standalone CLI bin; OCP behind scanner registry — rust-stack-fit Rank 2 |
| uv | **Adopt optional DX** | Does not replace CI oracle Python |
| wasmtime/wasmer | **Refuse** | Category error for gate CLI; constitution mesh/WASM refuse |
| ty / pyrefly / pyright / basedpyright | **Spike one** | Dual typecheckers = dual SoT pain; pick ≤1 near-gate |

---

## Proposed epic work

### A. Amend E-RT0 (keep; do not re-litigate)

Memo 32 tickets **RT0-1…RT0-8** and spikes RT-S1…S3 remain the Spec for **real-time architecture + receipts**. Amendments from this memo:

| ID | Change |
| --- | --- |
| **RT0-4** | Explicitly list **non-goals:** no pip-audit, no py-spy, no Hypothesis inside the RT pack (those move to E-RUST0) |
| **RT-S1** | Expand candidates: pyright **or** basedpyright **or** ty (single winner); pyrefly only if Spike exits Adopt |
| **RT0-1** | Must link **this file** + E-RUST0 as sibling Spec, not replace |

### B. New Spec-only epic **E-RUST0** — Rust/quality toolscape binding

**Epic goal:** Bind the BFS/DFS Rust-adjacent marketplace to Embody/Adopt/Refuse tickets with Acceptance, without implementing product code or softening 98.7 / complexipy / LOC.

**Invariants:** same constitution as E-RT0 · one tip writer · Spec → Implement → Verify → Archive · Implement epics only after Approve.

| ID | Title | Est | Acceptance |
| --- | --- | --- | --- |
| **RUST0-1** | Lock this memo as SoR toolscape | S | Human Approve; Explicit refuse list unchanged; links rust-stack-fit + memo 32 + synthesis |
| **RUST0-2** | Gate×category matrix | S | Table: each DFS category → `pre_pr` / oracle / tach / ast-grep / ruff / claims / stalker / CodeQL / Semgrep with RT / near-gate / gate-only / never |
| **RUST0-3** | Supply-chain sensor Spec | M | Spec for pip-audit or osv-scanner: advisory vs fail; pin allowlist; **must not** claim Cover%; cargo-deny cited as pattern only |
| **RUST0-4** | Profiling recipe Spec | S | Document py-spy (± samply) for suite stalls; ties E-RUN; agent invocation optional with receipt; never in oracle cell |
| **RUST0-5** | Property/fuzz boundary Spec | S | Hypothesis deepen targets list; Atheris only if native/parser Spike exits; refuse cargo-fuzz/AFL product deps |
| **RUST0-6** | Metrics-beyond-Cover% honesty Spec | M | One CONTRIBUTING/research paragraph: differential concept, behavioural gaps, SBFL/SemLoc = sensors; SemLoc ≠ fail_under; cite 2607.22880 + 2606.10417 |
| **RUST0-7** | Profiled native helper gate | S | Precondition checklist before any maturin/pyo3: profile artifact, bin-not-cdylib preference, LOC/CI matrix impact, OCP registry seam — matches rust-stack-fit |
| **RUST0-8** | Typechecker Spike charter | S | Single-candidate Spike (ty vs basedpyright vs pyright); exit Adopt/Defer/Refuse; refuse dual checkers |

**Spikes**

| Spike | Question | Exit |
| --- | --- | --- |
| RUST-S1 | pip-audit noise rate on current pins? | Adopt warn / Adopt fail-high / Defer |
| RUST-S2 | Does Stage-0 JSON/parser deserve Atheris? | Adopt harness / Refuse |
| RUST-S3 | py-spy on oracle plateau — actionable frames? | Recipe only / agent tool / Defer |
| RUST-S4 | ty maturity vs basedpyright for this tree? | One Adopt or all Defer |

**Exit (epic done):** E-RUST0 Spec Approved; no product Implement required; feed E-RT1 / E-QA3 / E-RUN / optional E-SUPPLY1 only after ticket Approves.

**Non-goals:** in-tree Rust; WASM runtime; replacing oracle; implementing monitors in this pass.

---

## Explicit refuse (do not schedule)

1. In-tree `Cargo.toml` / PyO3 rewrite of measure/gap/ratchets **without** profiled RUST0-7 gate.  
2. wasmtime / wasmer / PyOxidizer / mesh / ECS / Backstage as architecture or gate runtime.  
3. Miri, ASan/TSan, cargo-fuzz, AFL++, cargo-geiger, Clippy, cargo-deny as **product** merge gates.  
4. oxc / biome / SWC as Python quality SoT.  
5. Dual structural SoT (tree-sitter queries + ast-grep) or reclaiming Grep.  
6. SemLoc / LLM-as-judge / behavioural-gap LLM extraction as **98.7** proof.  
7. Fuzzy/PID confidence of green; climb/differential Cover% as floor.  
8. radare / ghidra / rr as default agent debugging (rr optional human-only Defer).  
9. deal/icontract (&lt;1k★) or Lean EG-VAR as mandatory runtime.  
10. OSS-Fuzz / schemathesis without an HTTP or native attack surface.  
11. Treating ★ counts alone as Adopt.  
12. Softening complexipy ≤5, LOC ≤225, or whole-repo fail_under 98.7.

---

## Sources

### GitHub API stars (2026-08-09) — selected

tach 2786 · ast-grep 15456 · ruff 49117 · uv 88542 · ty 19433 · complexipy 748 · pyright 15578 · basedpyright 3523 · pyrefly 6864 · semgrep 16162 · codeql 9923 · hypothesis 8857 · mutmut 1379 · cargo-deny 2396 · clippy 13433 · cargo-fuzz 1875 · AFL++ 6703 · miri 6481 · py-spy 15424 · austin 2211 · samply 4364 · cargo-geiger (geiger-rs) 1644 · rustsec/cargo-audit monorepo 1932 · wasmtime 18495 · wasmer 20946 · maturin 5742 · pyo3 16009 · tree-sitter 26589 · oxc 22261 · biome 25539 · radare2 24537 · atheris 1658 · pip-audit 1345 · osv-scanner 10791 · syft 9368 · grype 12706 · trivy 37323 · coveragepy 3405 · diff_cover 842 · bandit 8201 · pacak/cargo-show-asm 969 · life4/deal 903 · python-afl 373 · differential-coverage 4 · rr 10614 · Z3 12538 · OPA 12086 · guardrails 7263 · cargo-semver-checks 1667

### arXiv / papers (fetched or searched 2026-08-09)

- [2603.10060](https://arxiv.org/abs/2603.10060) Tool Receipts / NabaOS  
- [2601.04688](https://arxiv.org/abs/2601.04688) ToolGate  
- [2607.12650](https://arxiv.org/abs/2607.12650) EG-VAR  
- [2607.07405](https://arxiv.org/abs/2607.07405) Reason Less, Verify More  
- [2608.02464](https://arxiv.org/abs/2608.02464) Real-Time Detection and Repair  
- [2607.02599](https://arxiv.org/abs/2607.02599) AgentLTL  
- [2603.29109](https://arxiv.org/abs/2603.29109) SemLoc  
- [2606.10417](https://arxiv.org/abs/2606.10417) Behavioural gaps beyond coverage/mutation  
- [2607.22880](https://arxiv.org/abs/2607.22880) Coverage/mutation vs effectiveness (replication)  
- [2508.16307](https://arxiv.org/html/2508.16307) Metamorphic Coverage  
- [2506.03585](https://arxiv.org/html/2506.03585v1) LLM fault localization + SBFL context  
- Memo 32 corpus (Agent-C, Spec Kit Agents, VIGIL, …)  
- Thoughtworks: [Architectural fitness function](https://www.thoughtworks.com/radar/techniques/architectural-fitness-function); fitness-function-driven development / Architecture as code podcasts (2024–26 cartography)

### In-repo SoT

- `docs/design/rust-stack-fit-memo-2026-08-08.md`  
- `docs/research/coverage-quality/32-realtime-architecture-assertion-agents-2026.md`  
- `docs/research/coverage-quality/08-rust-test-runners-bottlenecks.md`  
- `docs/research/coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md`  
- `docs/research/se-quality-synthesis-2026-08-08.md`  
- `tach.toml`, `scripts/ci/pre_pr.py`, `src/doc_engine/ci/quality_gates.py`, `requirements*.txt`

### Unknown / blocked

- Whether Astral **ty** is merge-ready for this tree (maturity Spike).  
- LedgerMind primary arXiv ID unresolved in this pass (ToolGate + NabaOS + EG-VAR used instead).  
- Exact pip-audit fail rate on current lock — needs RUST-S1.  
- Whether any transitive wheel ships a fuzz-worthy native extension — needs inventory.  
- DeepWiki cartography not re-fetched for every BFS row (memo 32 DeepWiki for tach/ast-grep still valid).

---

## Parent-agent brief — what memo 32 missed

- Full **BFS categories** (fuzz, sanitizers/Miri analogs, SBOM, profiling, packaging, formal contracts, metrics-beyond-Cover%, oxc/biome, ty/pyrefly).  
- Concrete **profilers** (py-spy, samply, austin) vs abstract “stalker.”  
- **cargo-fuzz / AFL++ / Atheris / Hypothesis** boundary for a pure-Python CLI.  
- **Supply-chain** pattern transfer (cargo-deny/audit/geiger → pip-audit/OSV).  
- **Differential coverage + behavioural gaps + SBFL/SemLoc** as sensors with explicit SoT refuse.  
- **ToolGate / EG-VAR** beside NabaOS receipts.  
- **Architectural fitness functions** (Nygard/Thoughtworks) as sensor vocabulary.  
- **maturin profile gate** and **WASM refuse** spelled as tickets (E-RUST0), not one-liners.  
- Typechecker field beyond a single pyright Spike (**ty / pyrefly / basedpyright**).  
- Honest ★-dated catalog so Adopt/Refuse is evidence-bound, not vibes.
