---
category: Stack-fit research — Rust vs Python doc-engine / Stage-0 / gates
status: research complete; recommendation = no in-tree Rust for 30 days
date: '2026-08-08'
claim_tiers: Evidenced / Confirmed / Unknown
title: 'Principal SE memo: Should Rust improve `spring-boot-doc-agent`?'
related: []
last_reviewed: '2026-08-10'
---

# Principal SE memo: Should Rust improve `spring-boot-doc-agent`?

**Verdict:** For the next 30 days, **do not add in-tree Rust**. This product already buys most of the Rust wins that matter via **pinned external binaries** (`ast-grep-cli`, `ruff`, `complexipy`). In-tree PyO3/maturin would mainly tax the CI matrix, contributor surface, and cohesion rules without proven CI-minute ROI. Profile Stage-0 on a real Spring tree first; only then consider a **tiny, seam-bound** native helper—and prefer a **standalone CLI** over an extension module.

---

## Context (this repo)

| Fact | Evidence |
|------|----------|
| No in-repo `Cargo.toml` / `.rs` | Confirmed by workspace search |
| Stage-0 structural scan shells to **ast-grep** (chunked argv; Windows CreateProcess 206 mitigation) | `_scanner_astgrep.py` |
| Runtime pins: `ast-grep-cli`, `semgrep`; meta: `ruff`, `complexipy`, npm `jscpd` | `requirements.txt`, `requirements-dev.txt` |
| Scanner OCP registry already exists (`filesystem` / `ast-grep` / `codeql`) | `_scanner_registry.py` |
| CI: Ubuntu Python **3.10–3.12**; expensive hermetic steps pinned to **3.11** | CI workflow pattern (repo briefing) |
| Gap-average = Cobertura `xml.etree` policy report, not a throughput kernel | `coverage_gap_average.py` |

**Claim tiers used below:** **Evidenced** = primary source / this repo; **Confirmed** = well-supported secondary synthesis; **Unknown** = would need a profile or experiment.

---

## 1. Where Rust helps *this* product (ranked)

ROI axes: **CI minutes**, **correctness**, **maintenance**. Generic “Rust is fast” is not a ranking criterion.

### Rank 1 — Already captured: consume Rust CLIs (keep / deepen)

| Opportunity | Expected ROI | Why it fits |
|-------------|--------------|-------------|
| Keep **ast-grep** as Stage-0 SoT; pin + PATH discipline | **CI:** high (already paid); **correctness:** high (structural search mandate); **maint:** medium | Rust AST engine without dual-toolchain ownership. [Evidenced] DeepWiki: shared core + CLI/`ast-grep-py` UIs ([ast-grep overview](https://deepwiki.com/ast-grep/ast-grep), [Python integration](https://deepwiki.com/ast-grep/ast-grep/8-python-integration)); PyPI `ast-grep-cli` pin in-repo. |
| Keep **ruff** / **complexipy** as meta gates | **CI:** medium–high vs flake8 era; **maint:** high | Ruff is a Rust toolchain shipped as wheels/binaries ([architecture](https://deepwiki.com/astral-sh/ruff/1.1-architecture-overview); [v0.4 parser post](https://astral.sh/blog/ruff-v0.4.0) — >2× parser, 20–40% end-to-end). [Evidenced] |
| Optional: evaluate **`ast-grep-py`** only if subprocess/JSON chunking dominates | **CI:** Unknown until profiled; **maint:** risk ↑ (second package + ABI) | Official PyO3 bindings exist ([API guide](https://ast-grep.github.io/guide/api-usage/py-api.html)). Could cut argv chunking + JSON round-trips. [Confirmed] existence; **Unknown** net win vs CLI for *our* rule-file scan. |

**Pattern match:** Ruff/Polars/ast-grep succeed as **owned Rust products** with Python as a thin façade—not as drive-by FFI inside an unrelated Python app ([Polars PyO3 layer](https://deepwiki.com/pola-rs/polars/3-python-rust-interface)).

### Rank 2 — Conditional: in-process / native helper for Stage-0 *Python* residue

Only if profiling shows Python dominating wall clock **after** ast-grep returns:

| Seam | ROI if hot | Notes |
|------|------------|-------|
| Filesystem walk + SHA256 inventory (`core/walk.py`) | Medium CI on large target repos | Pure walk/hash is a classic Rust CLI win (ripgrep-class I/O). Prefer **bin** binding via maturin over cdylib. [Confirmed] pattern (maturin `bin` bridge — [maturin DeepWiki](https://deepwiki.com/PyO3/maturin)). |
| Merge/dedupe of partial signal bags + extract post-JSON | Low–medium | Small data volumes vs tree-sitter work; JSON→dict in Python is rarely the bottleneck. **Unknown** without profile. |
| Register a `rust-scan` / `native-walk` behind `_scanner_registry` | Correctness/maint: good if Protocol-stable | Matches existing OCP seam; do **not** put Rust inside LLM stages. [Evidenced] repo architecture. |

### Rank 3 — Poor ROI for *this* product (often suggested, skip)

| Idea | Why low ROI here |
|------|------------------|
| Rewrite **coverage.xml / gap-average** in Rust | Cobertura for this package is modest; work is policy (floor, weighted climb), not GB-scale XML. Gate time ≪ pytest collection/execution. |
| Rewrite **size ratchet / LOC AST** in Rust | Already adjacent to **ruff**/Python `ast`; correctness must match baseline JSON; dual impl risks false ratchet churn. |
| Accelerate **mutate sandbox** via Rust | Cost is tree copy + **pytest suite per mutant**, not parsing. |
| Replace **jscpd**/npm with Rust clone-detector | Orthogonal; already a native binary path via `gate_tools.py`. |
| Rust for **pytest-cov wall clock** | Coverage instrumentation is CPython/`coverage.py` domain; Rust does not replace suite structure. |

---

## 2. Where Rust is a poor fit

| Area | Reason |
|------|--------|
| Generative stages 1–4, adapters, interview, certification | Latency/quality dominated by LLM + policy, not CPU loops. |
| `doc_engine` / `stf` orchestration, registries, config trust | Needs readable Python for OCP/DDIA operability; FFI dilutes debugging. |
| Most quality-gate *policy* (diff-cover thresholds, claim predicates, Sonar) | I/O + subprocess + human-readable fail messages. |
| Semgrep / CodeQL backends | Already foreign runtimes; adding Rust between them adds seams without owning their engines. |
| “Rewrite the monorepo in Rust” | arXiv work on polyglot/monorepo pain stresses **CI rebuild scope and dual tooling**, not free performance ([Runnable Directories, arXiv:2512.03815](https://arxiv.org/html/2512.03815)). Migration papers ([RustMap](https://arxiv.org/pdf/2503.17741), etc.) target C→Rust safety, not Python CLI product kernels. |

---

## 3. Adoption patterns that match our principles

Align with port/adapter + small cohesive units + operability:

1. **Prefer maturin `bin` over `cdylib` first**  
   Same distribution story as `ruff` / `ast-grep-cli`: installable tool on `PATH`, invoked from `gate_tools`-style resolvers. Avoids GIL/ABI fretting for batch CI. [Evidenced] [maturin bindings table](https://deepwiki.com/PyO3/maturin); [distribution / manylinux](https://www.maturin.rs/distribution.html).

2. **If PyO3, treat it as an adapter, not a grab-bag `ffi/`**  
   Stable DTO in → stable DTO out; Python owns registries/OCP. Mirror Polars: thin Python wrapper, Rust core, no logic sprawl in the binding layer ([Polars interface](https://deepwiki.com/pola-rs/polars/3-python-rust-interface)). PyO3’s model is explicitly two-way bridge with GIL/`'py` lifetimes ([PyO3 DeepWiki](https://deepwiki.com/PyO3/pyo3)).

3. **One crate per concept; no `utils` in Rust either**  
   Size/complexipy culture applies: small crates, named seams (`walk_hash`, `merge_signals`), not a kitchen-sink `doc_engine_native`.

4. **abi3 / wheel matrix as a product cost**  
   PyO3 supports abi3 and multi-interpreter packaging ([PyO3](https://deepwiki.com/PyO3/pyo3)); maturin still requires **manylinux/zig + Windows + macOS** build graph for publishable wheels ([maturin distribution](https://www.maturin.rs/distribution.html)). That fights our already-slow CI and Windows-local gate story.

5. **FFI boundary risk is real in research terms**  
   [SafeFFI (arXiv:2510.20688)](https://ar5iv.labs.arxiv.org/html/2510.20688): memory-safety bugs concentrate at safe/unsafe and **mixed-language** boundaries. For us: keep unsafe/FFI surface tiny; prefer process isolation (CLI) over in-process extension until proven necessary.

6. **Do not re-implement tree-sitter/Java grammars**  
   Charon/LiteRSan-class papers show how expensive *owning* analysis infra is ([Charon](https://arxiv.org/html/2410.18042)). We should **buy** ast-grep, not fork it.

---

## 4. Concrete proposal options

### A. Pick-none (default) — **recommended**

Leave architecture as: Python orchestration + pinned Rust/native CLIs. Continue PATH-shadow discipline (`CONSTRAINTS` runtime note on `cargo`/`npm` vs pip pins).

**Wins already banked:** structural scan, lint, complexity—without Cargo in-tree.

### B. Spike one seam (only after A’s profiling gate)

**30-day spike criteria (all must hold):**

1. Profile `spring_signal_scan` on a mid/large real Spring repo (not only fixtures).  
2. Show **≥20–30%** of Stage-0 wall clock in Python walk/merge/extract (not ast-grep subprocess, not CodeQL).  
3. Prototype as **optional CLI** behind scanner Protocol; hermetic fixture parity unchanged; **no** coverage/size gate weakening.

**Preferred spike target:** walk+hash or ast-grep JSON post-process—not gap-average/size.

**Alternative spike (lower risk than own crate):** trial `ast-grep-py` vs `ast-grep-cli` for the same ruleset; measure wall clock + Windows argv issues. Still a dependency/ABI decision—not free.

### C. Strategic (explicitly defer)

In-tree Rust workspace + maturin wheels for Win+Linux × 3.10–3.12, published or CI-built. Matches Ruff/Polars *scale*, not this repo’s staffing or CI budget. Revisit only if Stage-0 becomes a product SLA bottleneck on customer-sized monorepos **and** B succeeds.

| Option | CI minutes | Correctness | Maintenance |
|--------|------------|-------------|-------------|
| A pick-none | Best near-term | Unchanged | Best |
| B one seam | Possible small win | Must prove parity | Dual toolchain tax |
| C strategic | Likely **worse** CI until mature | High if owned well | High ongoing |

---

## 5. Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **CI matrix × wheels** (manylinux, Windows, abi3, 3.10–3.12) | High | Prefer `bin`; or consume upstream wheels only |
| Contributor barrier (Rust + Python + npm + CodeQL) | High | Keep Cargo out of critical path for contributors |
| Debugging across FFI / process | Medium | CLI + JSON schemas; golden fixtures |
| `ffi/` junk diluting LOC/modularity / complexipy narrative | High | Forbid grab-bag; one named crate; size ratchet applies to generated? Prefer not to generate Python wrappers sprawl |
| PATH dual installs (pip pin vs `cargo install`) | Already lived | Keep pin-verify in CI |
| Subtle semantic drift vs Python size/coverage parsers | High if rewritten | Don’t rewrite ratchet parsers without byte-identical fixtures |

---

## 6. Recommendation (next 30 days)

**Default: Option A — pick-none.**

1. **Do not** add Rust crates, PyO3 modules, or maturin CI jobs.  
2. **Do** spend any performance budget on **profiling** Stage-0 + mutate (Python `cProfile`/timing around walk, ast-grep chunks, merge)—evidence before FFI.  
3. **Do** keep buying Rust via pins (`ast-grep-cli`, `ruff`, `complexipy`); treat that as the intentional architecture.  
4. **Reopen Option B** only if profiling shows a hot **Python** seam with clear CI-minute payoff; spike as a **CLI behind the scanner registry**, not a coverage/size rewrite.  
5. **Never** weaken coverage/size/complexipy gates to “make room” for a native experiment.

---

## Key citations

| Source | URL | Use |
|--------|-----|-----|
| PyO3 architecture | https://deepwiki.com/PyO3/pyo3 | Extension vs embed; GIL/abi3 |
| maturin overview + distribution | https://deepwiki.com/PyO3/maturin · https://www.maturin.rs/distribution.html | `bin`/`pyo3`, manylinux, generate-ci |
| Ruff architecture + parser rewrite | https://deepwiki.com/astral-sh/ruff/1.1-architecture-overview · https://astral.sh/blog/ruff-v0.4.0 | When Rust rewrite pays (owned toolchain) |
| ast-grep core + Python PyO3 | https://deepwiki.com/ast-grep/ast-grep · https://deepwiki.com/ast-grep/ast-grep/8-python-integration · https://ast-grep.github.io/guide/api-usage/py-api.html | CLI vs `ast-grep-py` |
| Polars PyO3 layering | https://deepwiki.com/pola-rs/polars/3-python-rust-interface | Adapter boundary pattern |
| SafeFFI (mixed-language boundary) | https://ar5iv.labs.arxiv.org/html/2510.20688 | FFI risk |
| Polyglot/monorepo CI cost framing | https://arxiv.org/html/2512.03815 | Dual-toolchain operability |
| Charon (cost of owning analysis infra) | https://arxiv.org/html/2410.18042 | Don’t re-build scanners |

**Unknown that would change the recommendation:** measured Stage-0 breakdown on a real multi-module Spring repo showing Python walk/merge ≫ ast-grep. Until that number exists, in-tree Rust is speculation.
