---
title: Release scan — Harn 0.10.69 · Nimbus 0.2.1 · noprop 0.0.4
status: RESEARCH COMPLETE — Spec-only stance (no impl tip)
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine (Embody Rust as wheels/CLIs, not in-tree runtime)
related:
- docs/research/coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md
- docs/research/process/22-stack-rescope-10k-star-bar-2026.md
- docs/research/stage0/astgrep-tailored-packs-fixture-ocs-2026.md
- docs/research/ci/36-ocs-dual-plant-profile-2026.md
do_not:
- add Harn/Nimbus/noprop as product deps or in-tree Cargo workspace
- replace Hypothesis / ast-grep / vacuous / client-identifier denylist
- treat ★≪10k pre-1.0 agent languages as merge SoT
spec_gate: none required — Refuse / pattern-only; no epic until a product gap opens
last_reviewed: '2026-08-10'
---

# Principal memo: Harn / Nimbus / noprop release burst (2026-08-10)

## 0. One-page verdict

| Bundle | What it is | Stance for *this* product |
| --- | --- | --- |
| **Harn 0.10.69** (`harn-kernel`, `tree-sitter-harn`, `harn-ir`, `harn-fmt`, `harn-terminal`, `harn-session-store`, `harn-sqlite`, `harn-opcode-macros`, `harn-secret-catalog`, …) | Pre-1.0 **pipeline language for AI agent orchestration** (Rust host); deterministic replay + capability contracts; tree-sitter grammar for `.harn` | **Refuse** product runtime / deps / Stage-0 language. **Adopt pattern only:** receipt + capability-fail-closed vocabulary (aligns E-CPL0 *semantics*, not Harn tip). |
| **Nimbus 0.2.1** (`nimbus-vault`, `nimbus-cli`, `nimbus-tui`, `nimbus-core`, `nimbus-creator`) | Pluggable **object-tree vault** sync (fs / HTTP / shell / nested vault) | **Refuse** plant/SoT. OCS dual plant already uses Path + gitignored pointer + Artifactory fail-closed. |
| **noprop 0.0.4** | Imperative Rust PBT; no deps/macros; caller-supplied seeds | **Refuse** dep (★0, `v0.0.x`, Rust-only). **Embody** Hypothesis; **Adopt pattern:** explicit seeds / no implicit I/O. |

**Bottom line:** Interesting adjacent Rust marketplace — **zero Embody crates** for doc-engine tip. Keep building **ast-grep + vacuous + Hypothesis**; do not open an epic to absorb Harn or Nimbus.

**Constitution:** fail_under **98.7** · complexipy **≤5** · LOC **≤225** · Embody Rust via pinned wheels/CLIs · refuse in-tree Rust unless profiled · ≥10k★ bar for stack *Adopt* (STACK0) with documented pin exceptions (complexipy, vacuous).

---

## 1. Evidence

### Evidenced

| Claim | Source |
| --- | --- |
| Harn = agent-orchestration language; pre-1.0; deterministic replay; capability-safe; MCP/ACP/A2A | [harnlang.com](https://harnlang.com/) |
| `harn-kernel` = portable compiler + deterministic execution leaf (no FS/net/clock authority in-kernel) | [docs.rs/harn-kernel](https://docs.rs/harn-kernel/latest/harn_kernel/) |
| `tree-sitter-harn` = editor/structural grammar for Harn source | [crates.io/tree-sitter-harn](https://crates.io/crates/tree-sitter-harn), editor docs |
| `harn-secret-catalog` = shared high-confidence secret pattern catalog for redaction/scan | [crates.io/harn-secret-catalog](https://crates.io/crates/harn-secret-catalog) |
| `noprop` = Rust PBT, no deps/macros/unsafe, caller-supplied seeds; API unstable `v0.0.x` | [github.com/sile/noprop](https://github.com/sile/noprop) |
| `nimbus-vault` = `Origin` trait over fs/HTTP/command/vault; `vault.toml` | [crates.io/nimbus-vault](https://crates.io/crates/nimbus-vault), PeachGB/nimbus |

### Stars / maturity (GitHub REST + crates.io, 2026-08-10)

| Project | ★ | Notes |
| --- | --- | --- |
| burin-labs/harn | **17** | Active push same day as 0.10.69; far below STACK0 bar |
| sile/noprop | **0** | Early |
| PeachGB/nimbus | **0** | Early; CLI/TUI recently labeled working vs stub in older README |
| tree-sitter-harn dl | ~8.3k | Grammar downloads ≠ product adoption for *our* Python CLI |
| noprop / nimbus-vault dl | dozens | Not a pin exception candidate |

### Confirmed (this tip)

| Fact | Where |
| --- | --- |
| Structural SoT = ast-grep (Java/Python) + Semgrep + CodeQL; citation mandate | CLAUDE.md, E-SCAN1, E-AST0 |
| Python vacuity = ast-grep rules ∪ `vacuous~=0.1.2` ∪ empty telemetry | `doc_engine.ci.vacuity` |
| PBT = Hypothesis (Embody) | E-RUST0 / synthesis |
| Client identifiers = denylist gate, not Harn secret catalog | `check_no_client_identifiers` |
| OCS plant = fixture SoR + Path pointer; Artifactory fail-closed | E-OCS0 |

### Unknown

| Item | Why |
| --- | --- |
| Whether `harn-secret-catalog` patterns are language-agnostic enough to extract without Harn runtime | Not fetched as data dump this pass |
| DeepWiki cartography | MCP unavailable |

---

## 2. Category mapping (vs open work)

| Open concern | Tempting crate | Better existing vehicle | Decision |
| --- | --- | --- | --- |
| Agent orchestration language | Harn kernel/CLI | Cursor/Claude adapters + `pre_pr` receipts | **Refuse** rewrite |
| Deterministic replay / receipts | Harn session-store | E-CPL0 Proof-or-Stop *semantics*; telemetry ledger | **Adopt pattern**; no Harn dep |
| Secret redaction catalog | harn-secret-catalog | Client-identifier denylist + CONSTRAINTS | **Refuse** dep; optional future sensor Spike only if denylist gaps are Evidenced |
| Structural search | tree-sitter-harn | ast-grep (Java/Python we actually ship) | **Refuse** (wrong language) |
| CFG / invariant analysis | harn-ir | complexipy + tach + CodeQL | **Refuse** |
| Pseudo-TTY / VT capture | harn-terminal | Not a gate need | **Refuse** |
| Multi-origin artifact sync | nimbus-vault | `local-runs/` + plant_profile + expectations JSON | **Refuse** now; Defer if Spec names multi-origin campaign store |
| Property testing | noprop | Hypothesis | **Refuse** dep; **Adopt** seed/repro pattern |

---

## 3. Adversarial checklist

- [ ] “New Rust release day” ≠ product need (category error vs E-RUST0 BFS)
- [ ] tree-sitter-* downloads mistaken for ★ bar / Embody eligibility
- [ ] Harn deterministic kernel sold as Cover% or vacuity SoT
- [ ] Nimbus vault soft-greens OCS without Artifactory (reopens E-OCS0 refuse)
- [ ] noprop displaces Hypothesis in Python tests via “no deps” aesthetic
- [ ] In-tree Cargo to “just try” Harn — constitution refuse

---

## 4. Epic

**None.** No Spec gate. If a later gap appears (e.g. shared secret-pattern SoR beyond denylist), open a **Spike** with exit criterion “extract patterns without Harn runtime” — not “depend on harn-secret-catalog.”

---

## Invariants

fail_under **98.7** · complexipy **≤5** · LOC **≤225** · Embody ast-grep/ruff/tach/complexipy/vacuous wheels · refuse in-tree Rust · STACK0 ★ bar · Spec → Implement → Verify → Archive
