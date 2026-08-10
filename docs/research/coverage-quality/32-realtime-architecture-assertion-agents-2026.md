---
title: Real-time architecture & logic assertion for coding agents (2026)
status: "legacy \u2014 needs review"
date: '2026-08-10'
claim_tiers: Unknown
related: []
last_reviewed: '2026-08-10'
freshness: tip-bound
---
# Real-time architecture & logic assertion for coding agents (2026)

**Date:** 2026-08-09  
**Product:** `doc-engine` / huntyyyyyy/spring-boot-doc-agent (Python CLI, deterministic gates)  
**Status:** RESEARCH COMPLETE — Spec-only epic **E-RT0** (do not implement in this pass)  
**Claim tiers:** `[Evidenced]` primary paper/docs/API · `[Confirmed]` this checkout · `[Unknown]` missing ID, blocked cartography, or open product choice  
**SoT siblings:** `se-quality-synthesis-2026-08-08.md` · `01-coverage-oracle-climb-solid.md` · `08-rust-test-runners-bottlenecks.md` · `modularity/20-tach-dependency-blueprint-2026.md` · `process/19-watch-stalker-agents-context-lean-2026.md` · `ci/17-codeql-signals-skip-fingerprint-2026.md` · `docs/design/rust-stack-fit-memo-2026-08-08.md`

---

## Verdict (one page)

| Question | Answer |
| --- | --- |
| Can we theoretically review agent code **in real time** and assert coverage **plus** dependency / system / code architecture, data access, mapping, schema, and logic — correcting hallucination / bad traversal as the agent moves? | **Partially yes — but not as one fused SoT.** STEM/OSS evidence supports **deterministic, incremental predicates at the tool/edit boundary** (tach, ast-grep, ruff, Semgrep MCP hooks, LTL/SMT tool-call gates, receipt grounding). Whole-repo Cover% 98.7, mutation adequacy, and schema/corpus hermeticity remain **gate-time oracles**, not microsecond monitors. |
| What is Rust’s real role vs theater? | **Embody Rust via existing wheels/CLIs** (ast-grep, ruff, tach, complexipy). **Refuse in-tree Rust rewrite** unless a profiled Stage-0 / I/O hotspot remains after those tools. cargo-\* / Clippy are **pattern sources** for Rust crates, not product deps. |
| Embody / Adopt / Refuse for *this* repo? | **Embody** oracle + path-cohesion + claims + tach cycles + structural search mandate + suite stalker *sensors*. **Adopt** (Spec-gated): incremental “edit-time” fitness pack (tach check / ruff / ast-grep / size / complexipy on touched paths), tool-receipt / deny-list harness for agent tools, optional lightweight LTL templates over *tool* traces — never over Cover%. **Refuse** LLM-as-judge as green, fuzzy/PID confidence, in-tree Rust, OPA/Guardrails as Cover% SoT, full AgentLTL/SMT stack as merge runtime without a narrow Spec, climb Cover% as floor proof. |
| Motivating failure | Local “green” (scoped climb / partial pre_pr) vs remote Cover% red (oracle cell) is already a **category error** this repo named (oracle ≠ climb). Real-time assertion must **not** invent a third SoT that looks like Cover% but measures something else. |

**Bottom line:** Real-time assertion is **theoretically sound** for *architecture edges, structural patterns, policy-permissive writes, and claim grounding*. It is **theoretically weak** as a substitute for whole-suite coverage, mutation discrimination, and Stage-0 corpus hermeticity. The correct product shape is a **layered envelope**: cheap incremental gates while the agent moves → `pre_pr` / quality-gates → CI oracle (`coverage.xml`, fail_under 98.7 on 3.11 only). Spec → Implement → Verify → Archive; one tip writer.

---

## Problem framing (local green / remote Cover% red as motivating failure)

### Failure shape `[Confirmed]`

Agents (and humans) routinely optimize the cheapest green signal:

1. Scoped `pytest --cov=<package>` + fail_under → **looks like** 98.7 but is a *different predicate* than whole-repo oracle (`coverage_measure` / CONTRIBUTING / synthesis policy **16-A** / **17**).
2. `pre_pr --fast` / docs-path auto → ruff + claims only; **not** oracle.
3. Suite stalker / climb / gap-average / domain markers are **sensors** — rebuildable views, not floor proof.
4. Remote CI 3.11 cov cell then fails → “local was green” narrative.

That mismatch is the motivating failure for “assert more than coverage in real time”: if the agent only learns Cover%, it will game Cover%. If it also learns **dependency edges, public surfaces, size/complexity, structural citations, and tool-trace compliance**, local green can approach remote green *without* collapsing sensors into the oracle.

### What “real time” must mean here

| Sense | Feasible? | Evidence class |
| --- | --- | --- |
| Per tool-call / per edit batch (ms–s) | Yes for **deterministic** checkers | AgentLTL / Agent-C / SMT gates / tool receipts / tach / ruff / ast-grep LSP |
| Continuous Cover% floor while typing | No (honestly) | Whole-suite oracle cost; climb ≠ floor |
| Correct “bad traversal” (wrong files, hallucinated APIs) | Partially | Spec Kit Agents grounding hooks; receipt cross-check; structural search mandate |
| Correct semantic schema / data-access design mid-flight | Weak unless encoded as **executable contracts** | Stage-0 fixtures + schema validators are gate-shaped |

### Constitution anchors (do not soften)

- Whole-repo `fail_under=98.7` boolean SoT; climb sensors ≠ oracle; climb artifact path distinct (`coverage.climb.xml`).
- complexipy ≤5; LOC ≤225; no `utils/` grab-bag; descriptive names.
- Refuse in-tree Rust unless profiled; Embody Rust via wheels.
- No LLM-as-judge as SoT; no fuzzy/PID confidence of green.
- Spec → Implement → Verify → Archive.

---

## Evidence table (paper/repo | claim | tier | star/year if applicable)

Stars fetched via GitHub API on **2026-08-09** unless noted. Papers via arXiv abs/HTML/PDF same date.

### A. arXiv / formal methods (agent verification & architecture)

| Source | Claim (compressed) | Tier | Year / notes |
| --- | --- | --- | --- |
| [arXiv:2607.02599](https://arxiv.org/abs/2607.02599) AgentLTL | FO-LTL over tool traces; **judge-free** compliance score; offline scoring + **online** pre-execution gating; grounding constraints can flag unsupported recall | `[Evidenced]` | 2026 |
| [arXiv:2603.20449](https://arxiv.org/abs/2603.20449) Winston et al. | Encode tool-use policies as SMT-LIB; Z3 checks planned tool calls **before** execution; reduces policy violations on τ-bench | `[Evidenced]` | 2026 |
| [arXiv:2512.23738](https://arxiv.org/abs/2512.23738) Agent-C | Temporal DSL → FOL/SMT; enforce ordering/invariants on tool-call streams; constrained generation on violation (HTML convert failed; PDF abstract retrieved via search + PDF fetch) | `[Evidenced]` (PDF) / HTML `[Unknown]` | 2025–26 |
| [arXiv:2607.07405](https://arxiv.org/abs/2607.07405) Reason Less, Verify More | Silent wrong-state failures when tools are policy-permissive; **deterministic pre-execution gates** lift success; gate **precision must be audited** | `[Evidenced]` | 2026 |
| [arXiv:2603.10060](https://arxiv.org/abs/2603.10060) Tool Receipts / NabaOS | HMAC-signed tool receipts; epistemic claim classification; detects fabricated tool refs / count lies with &lt;15 ms overhead — **not** ZK | `[Evidenced]` | 2026 |
| [arXiv:2608.02464](https://arxiv.org/abs/2608.02464) Real-Time Detection and Repair | Telemetry monitors (ESN etc.) + **deterministic verifiers** (recompute totals, shape-check tool results); LLM-auditor every step is costlier/weaker; repair via rollback | `[Evidenced]` | 2026 |
| [arXiv:2604.05278](https://arxiv.org/abs/2604.05278) Spec Kit Agents | SDD stages + **read-only probing** + validation hooks reduce context blindness (hallucinated APIs / arch violations); LLM-judge quality metric used in eval — **do not adopt as merge SoT** | `[Evidenced]` | 2026 |
| [arXiv:2604.10800](https://arxiv.org/abs/2604.10800) Verify Before You Fix | No repair without **execution-grounded** confirmation; plan–execute–verify; disabling validation ↑ unnecessary repairs | `[Evidenced]` | 2026 |
| [arXiv:2603.20356](https://arxiv.org/abs/2603.20356) Agentproof | Static + runtime checks on **agent workflow graphs** (not Python import graphs); DFA temporal policies | `[Evidenced]` | 2026 — map carefully (framework graphs ≠ doc-engine modules) |
| [arXiv:2604.11767](https://arxiv.org/abs/2604.11767) λ_A | Typed calculus for agent composition; lint structural incompleteness; YAML+AST beats YAML-only | `[Evidenced]` | 2026 — pattern for config+code entanglement |
| [arXiv:2605.16198](https://arxiv.org/abs/2605.16198) Formal Methods Meet LLMs | LTL progression monitors; residual formulas for intervention/re-prompt | `[Evidenced]` | 2026 |
| [arXiv:2606.26524](https://arxiv.org/abs/2606.26524) VIGIL | Runtime enforcement of skill behavioral specs via SMT over finite traces | `[Evidenced]` | 2026 |
| [arXiv:2607.26110](https://arxiv.org/abs/2607.26110) Architecture lit review | Continuous architectural governance / multi-view monitoring themes (2024–25 synthesis) | `[Evidenced]` | 2026 — secondary survey |
| [arXiv:2605.09059](https://arxiv.org/abs/2605.09059) Evaluating LLM-Generated Code | Correctness benchmarks miss production readiness; human review complements automation | `[Evidenced]` | 2026 — supports layered Verify, not real-time Cover% |
| [arXiv:2602.22302](https://arxiv.org/html/2602.22302) Agent Behavioral Contracts | Runtime contracts / AgentAssert; soft+hard constraints (HTML) | `[Evidenced]` | 2026 |
| CoverUp [2403.16218](https://arxiv.org/abs/2403.16218) / ChaCo [2601.10942](https://arxiv.org/abs/2601.10942) | Climb-shaped iteration vs patch coverage — **already** embodied in dual-mode design | `[Evidenced]` | cited in synthesis |

### B. GitHub / OSS enforcers (what they actually enforce)

| Repo | ★ (2026-08-09) | What it actually enforces (primary README/docs) | Fit for *this* product |
| --- | --- | --- | --- |
| [tach-org/tach](https://github.com/tach-org/tach) | **2786** | Declared `depends_on`, public interfaces, **no cycles**, layers; `tach check` CI; Rust core, Python CLI; no runtime impact | **Embody** (cycles already in `tach.toml`); **Adopt** finer map under E-TACH0 |
| [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) | **15456** | Structural AST search/lint/rewrite; CLI + LSP (IDE real-time) + py bindings | **Embody** Stage-0 + citation mandate |
| [astral-sh/ruff](https://github.com/astral-sh/ruff) | **49117** | Extremely fast lint+format (Rust) | **Embody** `pre_pr` / CI |
| [rohaquinlop/complexipy](https://github.com/rohaquinlop/complexipy) | **748** | Cognitive complexity analysis (Rust) | **Embody** ≤5 ratchet (&lt;1k★ but already pinned — bar exception because Confirmed gate) |
| [microsoft/pyright](https://microsoft/pyright) | **15578** | Static type checker | **Adopt selectively** / Spike — not Cover% SoT |
| [semgrep/semgrep](https://github.com/semgrep/semgrep) | **16162** | Pattern SAST / guardrails; IDE + pre-commit + CI; MCP hooks for coding agents | **Embody** Stage-0 backend + rule_coverage |
| [github/codeql](https://github.com/github/codeql) | **9923** | QL libraries / code scanning | **Embody** pack + change/fingerprint Spec (E-CQL0) |
| [HypothesisWorks/hypothesis](https://github.com/HypothesisWorks/hypothesis) | **8857** | Property-based testing | **Embody** pattern for generative tests; not architecture SoT |
| [boxed/mutmut](https://github.com/boxed/mutmut) | **1379** | Mutation testing | **Adopt as sensor** / advisory — refuse as 98.7 substitute |
| [sixty-north/cosmic-ray](https://github.com/sixty-north/cosmic-ray) | **647** | Mutation testing | **Refuse as implement SoR** (&lt;1k★); pattern OK |
| [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | **12086** | General policy engine (Rego) | **Refuse as core** for Python CLI Cover%; **Adopt pattern** for tool-call policy encoding if Spec wants Rego≠Z3 |
| [guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails) | **7263** | LLM I/O validators + structured generation | **Refuse as Cover%/arch SoT**; optional prose/IO Spike |
| [obi1kenobi/cargo-semver-checks](https://github.com/obi1kenobi/cargo-semver-checks) | **1667** | SemVer API breakage for Rust crates | **Refuse product dep**; **Adopt pattern** → public_surface / façade poke |
| [EmbarkStudios/cargo-deny](https://github.com/EmbarkStudios/cargo-deny) | **2396** | License/ban/advisory/source lint for Cargo deps | **Refuse product dep**; supply-chain pattern only |
| [rust-lang/rust-clippy](https://github.com/rust-lang/rust-clippy) | **13433** | Rust lints | **Refuse product dep**; lint-culture analogy to ruff |
| coveragepy | **3405** | Coverage measurement | **Embody** oracle XML pipeline |
| “neuri” / Neuri guardrails | — | No clear primary matching agent-architecture enforcer in search results | `[Unknown]` — do not cite as SoR |

### C. DeepWiki (cartography only)

| Page | Useful cartography? | Tier |
| --- | --- | --- |
| [deepwiki.com/gauge-sh/tach](https://deepwiki.com/gauge-sh/tach) (indexed Apr 2025) | Hybrid Py/Rust; dependency pipeline; check/interfaces/layers/test selection | `[Evidenced]` cartography |
| [deepwiki.com/ast-grep/ast-grep](https://deepwiki.com/ast-grep/ast-grep) (indexed Aug 2026) | Core engine + CLI/LSP/NAPI/py; rule YAML | `[Evidenced]` cartography |
| Other DeepWiki targets | Not required for this memo | — |

### D. Confirmed local gate map (this repo)

| Gate / seam | Role today | Real-time? | Tier |
| --- | --- | --- | --- |
| `coverage_measure` oracle → `coverage.xml` + fail_under 98.7 (3.11) | **Floor SoT** | Gate only | `[Confirmed]` |
| Climb / gap-average / PathCohesion | Sensors / cohesion wipe | Climb can be scoped; **≠ floor** | `[Confirmed]` |
| `scripts/ci/pre_pr.py` | Local orchestrator: ruff, claims, code quality, domain markers, façade poke, rule_coverage, pytest; `--full` mutators advisory; `--actions-outage` CodeQL | Near-gate, not per-keystroke | `[Confirmed]` |
| `doc_engine.ci.quality_gates` | complexipy, size, tach cycles, diff-cover new-code, duplication | PR/local gate | `[Confirmed]` |
| `tach.toml` | **Cycles only** today (`forbid_circular_dependencies`); free cross-imports | Fast enough for edit-time | `[Confirmed]` |
| `check_repo_claims.py` | Steering/`derived`/CONSTRAINTS predicates | Fast; edit-time capable | `[Confirmed]` |
| Suite stalker sensors (E-RUN / E-STK) | Timing/plateau telemetry; findings ledger | Sensors ≠ SoT | `[Confirmed]` |
| CodeQL signals + E-CQL0 fingerprint Spec | Pack compile/runtime; skip when inputs unchanged | Gate; not agent-loop | `[Confirmed]` |
| `mutation_driver` / mutate.py | Adequacy advisory in `--full` | Gate/advisory | `[Confirmed]` |
| Public surface / façade poke (`check_facade_poke_surface.py`, E-COH0) | Characterization attrs / façade contract direction | Near-gate; tach `[[interfaces]]` still Spec-draft | `[Confirmed]` |
| Hooks deny text-search / raw network | Agent tool policy at PreToolUse | **Already real-time** for Claude Code | `[Confirmed]` |

---

## Rust: Embody vs Adopt vs Refuse

### Embody (already the win)

| Artifact | Why Rust matters | Theater risk if misused |
| --- | --- | --- |
| **ast-grep** | Structural citations; Stage-0 SoT; LSP = true edit-time | Replacing with text grep “for speed” |
| **ruff** | Lint/format wall-clock | Claiming ruff green ⇒ architecture OK |
| **tach** | Dependency fitness; Rust parser/`ruff_python_ast` class stack | `tach sync` as silent architecture Approve |
| **complexipy** | Cognitive complexity ≤5 | Raising ceiling to land features |

Aligned with `docs/design/rust-stack-fit-memo-2026-08-08.md`: consume owned Rust products as PATH/wheels; do not dual-toolchain the monorepo.

### Adopt (conditional / Spec-gated)

| Item | When |
| --- | --- |
| `ast-grep-py` in-process | Only if profiled subprocess/JSON chunking dominates Stage-0 |
| maturin **bin** helper (walk/hash) | Only after profile; prefer CLI over cdylib |
| cargo-semver-checks **pattern** | Inform public_surface / façade poke Accept criteria — not a Cargo workspace |
| Semgrep MCP / IDE hooks | Edit-time SAST for agents — keep hermetic CE rules for CI SoR |

### Refuse (theater)

| Item | Why |
| --- | --- |
| In-tree `Cargo.toml` / rewrite of measure/gap/ratchets | No profiled ROI; CI matrix + LOC culture tax (`rust-stack-fit`) |
| cargo-deny / Clippy as product gates | Wrong ecosystem; supply-chain already Python-pinned |
| “Rust stalker” product bundle as oracle replacement | E-RUN0 / research 08 |
| WASM/mesh/ECS “for architecture assertion” | Category error for this CLI |
| Claiming Rust ⇒ real-time Cover% | Coverage instrumentation remains CPython/`coverage.py` |

**Verdict line:** Rust’s real role is **high-performance deterministic analysis engines we already pin**. Theater is **rewriting the product in Rust** or treating Rust linters as proof of architectural correctness.

---

## What can be asserted in real time vs only at gate

### Real-time capable (ms–few seconds; agent-loop / IDE / PreToolUse)

| Dimension | Mechanism | Honesty bound |
| --- | --- | --- |
| Dependency architecture (imports, cycles, declared edges) | `tach check` (+ future `depends_on` / interfaces) | Declares **intended** modular monolith edges — not runtime topology |
| Code architecture / structural patterns | ast-grep rules + LSP; Semgrep patterns | Pattern presence ≠ semantic correctness; zero match ≠ absence without grammar care |
| Style / bugclass lint | ruff | Not system architecture |
| Cognitive complexity / size on touched files | complexipy + size ratchet scoped | Scoped size ≠ whole-repo offender map unless aggregated |
| Tool-call policy / ordering | LTL/SMT gates, deny hooks (text-search, raw network) | Enforces **procedure**, not Cover% |
| Hallucinated tool results / fabricated citations | Tool receipts; claims checker on paths; refuse Grep | Receipts ground *claims about tools*; not design quality |
| Bad traversal (wrong paths) | Spec Kit–style probing hooks; PathCohesion on measure writes | Still needs human Spec for “allowed write set” |
| Public surface poke | façade characterization script | Characterization ≠ full API semver |

### Gate-only (or batch) — do not pretend real-time

| Dimension | Why gate-only |
| --- | --- |
| Whole-repo Cover% vs 98.7 | Full suite + cohesive `coverage.xml`; CI 3.11 only |
| New-code diff-cover floor | Needs compare-ref + oracle XML |
| Mutation / metamorphic adequacy | Expensive; advisory `mutation_driver` |
| Stage-0 rule corpus + CodeQL pack compile/runtime | Fingerprint skip OK; still evaluation-time SoR |
| Schema / data-access / mapping “designs” | Require hermetic fixtures + validators + human Spec; encode as contracts before real-time |
| System architecture (product category) | Strategic refuse list — not a linter |

### Mapping: user wish-list → repo stance

| Wish | Real-time? | Embody / Adopt / Refuse |
| --- | --- | --- |
| Coverage | Gate (oracle); climb sensor only | Embody dual-mode discipline |
| Dependency architecture | Yes (tach) | Embody cycles; Adopt map |
| System architecture | Mostly Spec/docs | Refuse mesh theater |
| Code architecture | Partial (ast-grep/ruff/size) | Embody |
| Data access / mapping / schema | Gate + contracts | Adopt executable schemas; Refuse LLM schema SoT |
| Logic checks | Partial (SMT/LTL/tests) | Adopt narrow gates; Refuse LLM-judge |
| Correct hallucination mid-move | Partial (receipts, structural search, probing) | Adopt receipts+hooks; Refuse ZK theater |

---

## Proposed epic E-RT0 (Spec-only) — tickets with Acceptance; do NOT implement

**Epic goal:** Specify a **layered real-time assertion envelope** for coding agents on this repo that asserts dependency/code architecture and tool-trace honesty **without** creating a fake Cover% SoT or in-tree Rust.

**Invariants:** fail_under 98.7 · complexipy ≤5 · LOC ≤225 · no utils · policy 16-A · LLM-judge ≠ SoT · one tip writer · Spec → Implement → Verify → Archive.

| ID | Title | Est | Acceptance |
| --- | --- | --- | --- |
| **RT0-1** | Spec memo lock (this file + backlog pointer) | S | Human Approve of E-RT0 scope; Explicit refuse list unchanged; link synthesis + rust-stack-fit |
| **RT0-2** | Inventory: edit-time vs gate predicates | S | Table of every existing gate classified RT / near-gate / gate-only with command + wall-clock class; no new SoT names colliding with `coverage.xml` |
| **RT0-3** | Agent harness Spec: tool receipts + deny composition | M | Spec for HMAC-or-hash receipts on tool results (inspired by 2603.10060) composed with existing deny hooks; Accept: forged “I ran pytest” claims fail closed in harness tests (design-level fixtures) |
| **RT0-4** | Incremental fitness pack Spec | M | Spec for `touched-path` pack: ruff + tach check + complexipy + size + ast-grep rule subset; **must not** set fail_under; banner “sensor ≠ oracle” |
| **RT0-5** | Architecture conformance Spec (tach interfaces) | M | Depends on E-TACH0 Approve; Accept criteria for `[[interfaces]]` / public_surface vs façade poke; refuse `tach sync` auto-Approve |
| **RT0-6** | Optional LTL template Spike | S | Spike: 3–7 safety templates over **agent tool traces** (must_precede claims-check before CONSTRAINTS edit; never_after force-push; etc.); exit: keep/defer; **no** Z3 in merge path unless precision audit plan |
| **RT0-7** | Schema/data-access assertion boundary | S | Document which Stage-0 / artifact validators are gate-only; list any contract that could become edit-time without LLM-judge |
| **RT0-8** | Local↔remote parity note | S | Extend process docs: which RT pack greens still require oracle before push; tie to pre_pr modes + E-CQL0 asymmetry |

**Spikes**

| Spike | Question | Exit |
| --- | --- | --- |
| RT-S1 | Does pyright earn a near-gate slot under ★ bar + LOC culture? | Adopt/Defer/Refuse with measure |
| RT-S2 | AgentLTL vs hand templates vs OPA Rego for *tool* policy? | One encoding; refuse dual engines |
| RT-S3 | Semgrep MCP hooks vs existing Claude PreToolUse — overlap? | Single deny story |

**Exit (epic done):** E-RT0 Spec Approved; no implement code required; E-RT1 Implement may be scheduled only after RT0-1–RT0-5 Approve and E-TACH0/E-COH dependencies clear.

**Non-goals:** implementing monitors; weakening 98.7; in-tree Rust; replacing stalker sensors with LLM chat.

---

## Explicit refuse list

1. Scoped Cover% / climb / gap-average / domain meeting-rate as proof of whole-repo **98.7**.
2. LLM-as-judge, PID/fuzzy “confidence of green,” or statistical monitors as **merge SoT**.
3. In-tree Rust / Cargo workspace / Clippy / cargo-deny / cargo-semver-checks as product gates.
4. OPA, Guardrails Hub, or Agentproof workflow-graph tools as substitutes for tach + oracle.
5. Full AgentLTL/SMT stack as mandatory runtime without precision audit + Spec (2607.07405).
6. ZK proofs for interactive coding agents (2603.10060 argues receipts win on cost).
7. Dual import-linter + tach without LEG-S1; `tach sync` as architecture Approve.
8. Ungated agent rewrite of CONSTRAINTS / fail_under / baselines.
9. Cross-worktree `coverage combine`; cov cell on every Python version.
10. Mesh / ECS / Backstage / WASM-by-default / Spec Kit WorkflowEngine as mandatory runtime.
11. Treating DeepWiki cartography or ★ counts alone as Adopt.
12. “neuri” (unresolved primary) as cited enforcer.

---

## Sources

### arXiv (fetched 2026-08-09)

- https://arxiv.org/abs/2604.05278 — Spec Kit Agents  
- https://arxiv.org/abs/2605.09059 — Evaluating LLM-Generated Code  
- https://arxiv.org/abs/2607.26110 — Software design/architecture lit review  
- https://arxiv.org/abs/2608.02464 — Real-Time Detection and Repair of LLM Agent Failures  
- https://arxiv.org/abs/2607.02599 — AgentLTL  
- https://arxiv.org/abs/2607.07405 — Reason Less, Verify More  
- https://arxiv.org/abs/2603.10060 — Tool Receipts / NabaOS  
- https://arxiv.org/abs/2603.20449 — Solver-Aided Policy Compliance  
- https://arxiv.org/abs/2604.10800 — Verify Before You Fix  
- https://arxiv.org/abs/2603.20356 — Agentproof  
- https://arxiv.org/abs/2604.11767 — λ_A  
- https://arxiv.org/abs/2605.16198 — Formal Methods Meet LLMs  
- https://arxiv.org/abs/2606.26524 — VIGIL  
- https://arxiv.org/abs/2512.23738 — Agent-C (PDF; HTML conversion failed)  
- https://arxiv.org/html/2602.22302 — Agent Behavioral Contracts  
- Prior synthesis IDs: 2403.16218, 2601.10942, 2606.04967, 2512.22256  

### GitHub API / primary READMEs (stars 2026-08-09)

- tach-org/tach (2786), ast-grep/ast-grep (15456), astral-sh/ruff (49117), microsoft/pyright (15578), semgrep/semgrep (16162), github/codeql (9923), HypothesisWorks/hypothesis (8857), boxed/mutmut (1379), sixty-north/cosmic-ray (647), open-policy-agent/opa (12086), guardrails-ai/guardrails (7263), obi1kenobi/cargo-semver-checks (1667), EmbarkStudios/cargo-deny (2396), rust-lang/rust-clippy (13433), coveragepy/coveragepy (3405), rohaquinlop/complexipy (748)  

### DeepWiki

- https://deepwiki.com/gauge-sh/tach  
- https://deepwiki.com/ast-grep/ast-grep  

### In-repo SoT

- `docs/research/se-quality-synthesis-2026-08-08.md`  
- `docs/research/coverage-quality/01-coverage-oracle-climb-solid.md`  
- `docs/research/coverage-quality/08-rust-test-runners-bottlenecks.md`  
- `docs/research/modularity/20-tach-dependency-blueprint-2026.md`  
- `docs/design/rust-stack-fit-memo-2026-08-08.md`  
- `docs/design/concept-split-cohesion-design-2026-08-09.md`  
- `docs/research/process/19-watch-stalker-agents-context-lean-2026.md`  
- `docs/research/ci/17-codeql-signals-skip-fingerprint-2026.md`  
- `scripts/ci/pre_pr.py`, `src/doc_engine/ci/quality_gates.py`, `tach.toml`  

### Unknown / blocked

- Agent-C HTML abs page conversion failure (PDF used).  
- “neuri” product identity unresolved.  
- Whether pyright / Rego / full AgentLTL belong in E-RT1 — open product choice (Spikes RT-S1/S2).  
