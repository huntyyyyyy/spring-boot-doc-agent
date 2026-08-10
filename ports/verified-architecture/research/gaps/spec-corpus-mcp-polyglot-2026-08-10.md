---
title: Spec / corpus MCP + polyglot language features — deep research
status: RESEARCH — FREEZE-aware; NOT product verify MCP; NOT Implement Ready
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
related:
  - research/gaps/shallow-decisions-honesty-2026-08-10.md
  - 01-vision/problem-frame/BOUNDARY.md
  - docs/adr/adr-0004-native-then-wasm-lockcheck.md
  - docs/adr/adr-0007-rust-owns-engine.md
  - docs/adr/adr-0010-typescript-ide-mcp.md
  - ../../docs/research/process/25-tip-grounding-mcp-2026.md
  - ../../adapters/mcp/README.md
github_snapshot: '2026-08-10'
---

# Spec / corpus Model Context Protocol — deep research

**Banner.** This studies a **read-only Spec / corpus MCP** that shrinks LLM
context and hallucination over the planning tree. It is **not** the product
`verify` / `resolve` / receipt server. Under FREEZE: research + optional Spike
only — do not schedule polyglot product Implement.

**User question (accepted):** Is there benefit to “training” on unfinished
contracts via tools (vs dumping the repo)? Can **Rust / WASM / Go / other
lanes** already add features for that Spec surface — including ideas from the
polyglot portfolio (“last night” feature dump: WASM LockCheck, Go watch, Ruby
locks, Clojure/bb, TS IDE, etc.)?

No literal “before bed” string in-repo; the matching backlog is the
**polyglot portfolio + Wave-3 enrichment + E-TOOL0 / tip-grounding MCP** work
(`[Evidenced — ADR-0001/0004/0007/0009/0010`, `research/polyglot/*`,
`docs/research/process/25-tip-grounding-mcp-2026.md`, `48-complete-toolscape…`]).

---

## 0. Dual surfaces (do not conflate)

| Surface | Job | SoR? |
| --- | --- | --- |
| **Planning Spec corpus** | Progressive disclosure for agents designing the engine | Spec docs / Decision Framework / FREEZE |
| **Verify engine MCP** | Graph + locks + receipts over a *target* repo | Future product; Draft ICD only |

`BOUNDARY.md` already separates them. A Spec MCP serves **surface 1**. Rust/WASM
LockCheck belongs to **surface 2** (Wave-3 / Could) — useful later, wrong as
day-one Spec MCP deps.

---

## 1. Why Spec MCP can help (your inefficiency point)

| Mode | Cost | Hallucination mode |
| --- | --- | --- |
| Dump / re-parse whole port every turn | High tokens; contradictions (Adopt vs FREEZE) | Model invents “Chosen” as Accept |
| **Spec MCP tools** return *one* STATUS / assumption / ICD slice | Low, auditable | Failures are `unknown_id` / path miss — visible |
| Product verify MCP with fake greens | Medium | **False training** on unfinished oracles |

**Verdict:** unfinished **contracts as tools** = useful training; unfinished
**oracles as tools** = harmful. Spec MCP is the former.

---

## 2. What already exists on the tip (parent repo)

| Artifact | State | Gap |
| --- | --- | --- |
| `adapters/mcp/server.py` | Read-only Stage-0 **pipeline run** query | Speaks protocol **`2024-11-05`** + `initialize` — **stale vs `2026-07-28`** `[Evidenced — server.py]` |
| E-GND0 tip-grounding MCP memo | Spec Draft — tip probes, Refuse codegen tools | Not Implemented; depends other Approves |
| E-TOOL0 toolscape | Polyglot Pilot catalog for *this* monorepo | TOOL9: steal TS envelopes into **Python** host — no Node tip dep |
| TOOL10 | WASM: bubblewrap first; Extism after fail | Tip sandboxing — not VA LockCheck |

**Implication:** you are not starting from zero — extend **tip / Spec grounding**,
do not invent a second verify stack. Upgrade path must pin **`2026-07-28`**
(stateless / handles) for any *new* server; legacy Stage-0 needs an explicit
compat ADR if kept.

---

## 3. Language feature map — Spec MCP vs product verify

GitHub snapshot **2026-08-10** `[Evidenced]`: official SDKs — TypeScript ★~13k,
Python ★~24k, Go ★~5k, C# ★~4.5k, **Rust ★~3.8k** (active). Wasmtime ★~18.5k,
Extism ★~5.7k, wazero ★~6.3k.

| Language / runtime | Spec / corpus MCP (now–Spike) | Product verify MCP (later) | Tier for Spec MCP |
| --- | --- | --- | --- |
| **TypeScript** | Cursor/IDE stdio host ergonomics; ADR-0010 presentation | Product MCP presentation | **Could** host shell; TOOL9 preferred Python tip |
| **Python** | Natural tip host (existing adapter + ICD JSON Schema validate with draft schemas) | Peer ACI only | **Pilot / Adopt pattern** for Spec MCP v0 |
| **Rust** | Fast path: schema validate, frontmatter index, content-addressed corpus digest | Engine + wasmtime host (ADR-0007) | **Could** library behind Python/TS; **Refuse** day-one polyglot host |
| **WASM / Wasmtime / Extism** | Optional **sandboxed markdown/schema reader** plugin (deny net) — niche | LockCheck guest (ADR-0004); isolation ≠ proof | **Could** after thin Spec MCP works; **Refuse** as Spec MCP requirement |
| **Go** | `corpus_version` / fsnotify invalidate Spec snapshot handle | Watch/reindex chassis (ADR-0009) | **Could** sidecar for handle freshness |
| **Ruby** | Weak for Spec MCP | Packwerk lock DX (ADR-0003) | **Park** for Spec MCP |
| **Clojure / bb** | Weak; optional EDN query over *exported* Spec index | Graph brain sidecar | **Park** for Spec MCP |
| **C / Zig** | N/A | Niche systems/WASM | **Refuse** Spec MCP |

### Can WASM/Rust “already be added” for Spec MCP?

**Rust — yes, as a library feature, not as the only server.** Official
`modelcontextprotocol/rust-sdk` is real and maintained. Best Spec uses early:
deterministic `material_digest`-style hash of the Spec tree; JSON Schema checks
against `icd/mcp/*.schema.json`; reject oversized payloads. That trains agents
on **schema_invalid** without fake verify.

**WASM — yes as capability sandbox for *untrusted* Spec plugins, no as prover.**
Same honesty as ADR-0004: fuel/epoch = engineering control. For Spec MCP, a
WASM guest that only parses Markdown/JSON under deny-FS-except-corpus is a
**Could** hardening — not needed to get hallucination reduction. Product
LockCheck-in-WASM remains Wave-3 / PIL-WASM — **do not** drag it into Spec MCP
v0.

**Go — yes for corpus watch.** Mint `spec_snap_…` when FREEZE/STATUS/icd change;
agents pass handle — mirrors product `snapshot_open` *pattern* without being
verify. Excellent “train on unfinished contracts” without false-green receipts.

**Ruby / Clojure — not for Spec MCP v0.** Keep for product lanes.

---

## 4. Architecture options (scored as sensors)

| Option | Why | What | Who | How | When | Where | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **A. Thin Python Spec MCP** (extend tip pattern) | 2 | 2 | 2 | 2 | 2 | 2 | **Working hypothesis** for Spike |
| B. Thin TypeScript-only Spec MCP | 2 | 1 | 1 | 2 | 2 | 1 | **Could** (Cursor stdio ergonomics); peer lean — fights TOOL9 “no Node tip dep” unless facade-only |
| C. Rust core + thin TS/Python facade | 2 | 2 | 1 | 1 | 1 | 1 | **Could** after A proves tools |
| D. WASM guest readers day one | 1 | 1 | 0 | 0 | 0 | 0 | **Refuse** v0 |
| E. Full polyglot Spec MCP (all lanes) | 0 | 0 | 0 | 0 | 0 | 0 | **Refuse** (FREEZE + shallow risk) |
| F. Product verify MCP now | 0 | 0 | 0 | 0 | 0 | 0 | **Refuse** until deepen-3 |

### Suggested tool set (Spec MCP v0 — read-only)

| Tool | Returns | Trains |
| --- | --- | --- |
| `spec_status` | `STATUS.md` structured fields + FREEZE flag | Don’t Implement |
| `spec_assumption` | A-LOCAL…A-DEPTH from honesty memo | Explicit assumptions |
| `spec_icd` | Named ICD / schema path contents (size-capped) | Contracts not vibes |
| `spec_decision` | One Decision Matrix section | Working hypothesis ≠ Accept |
| `spec_gap` | G-* / deepen-3 queue | Focus |
| `spec_snapshot_open` (optional Go-backed) | `spec_snap_…` + corpus digest | Handle discipline without verify |

**Minefields:** any tool that writes; `verify`/`resolve`; narrative “research PASS”.

### Contract stamps (required on every tool result)

| Field | Why |
| --- | --- |
| `doc_status` | `DRAFT` / `SUPERSEDED` / … — blocks Draft-as-Accepted |
| `freeze_active` | boolean from STATUS FREEZE |
| `accepted` | always `false` until human Accept recorded |
| `corpus_version` | digest or `spec_snap_…` — cache invalidation |

Prefer **Resources** for corpus slices (URI + `ttlMs` / `cacheScope`) and **Tools**
for typed getters. Go reminting a handle does **not** fix clients that cache
long-TTL resource bodies across a FREEZE demotion — advertise short `ttlMs` or
`listChanged`.

Exact public products with these `spec_*` tool names = **0** → **Pilot invent**
host pattern; do not read “Adopt pattern” as Adopt of tool semantics.

---

## 5. Training benefit vs false-green (direct answer)

| Benefit | Real? |
| --- | --- |
| Less repo-wide parse / fewer contradiction hallucinations | **Yes** if tools are the SoR path for tip agents |
| Practice `2026-07-28` handles / reject classes | **Yes** on Spec snapshot handles |
| Practice Rust/WASM LockCheck | **No** via Spec MCP — wrong surface |
| “Warm up” product verify | **Risky** — only after deepen-3; stub rejects OK, pass receipts **Refuse** |

---

## 6. Spike charter (optional — not scheduled as Must)

| ID | SPIKE-SPEC-MCP-0 |
| --- | --- |
| Goal | Read-only Spec MCP over `ports/verified-architecture` (+ honesty FREEZE) |
| Host | Python stdio; pin protocol story (`2026-07-28` or explicit legacy ADR) |
| Exit keep | Tip agent answers FREEZE/deepen-3 via tools without opening >N files; FX-SPEC-01 forged handle rejects |
| Exit drop | If tools just wrap `cat` with no size/deny discipline |
| Out of scope | Rust engine, WASM LockCheck, Go product watch, Ruby/Clojure |
| Follow-ons (Could) | Rust schema crate; Go corpus watch; WASM sandboxed reader |

Align with E-GND0: **Refuse** codegen / write tools on this server.

---

## 7. Agent-codegen bites

1. Building product `packages/mcp-server` “to help Spec” → FREEZE violation.  
2. Labeling WASM Spec reader “proved.”  
3. Keeping `initialize` / `2024-11-05` while claiming `2026-07-28`.  
4. Polyglot day-one Spec MCP (Ruby+bb+WASM+Go) as prestige theater.  
5. Spec tools that return entire `ARCHITECTURE_BRIEF` (defeats the point).

---

## 8. Bloom

| Level | Evidence |
| --- | --- |
| 1 | SDK stars; adapters/mcp; ADR-0004/7/9/10; E-GND0; E-TOOL0 TOOL9/10 |
| 2 | Dual surfaces; language map |
| 3 | SPIKE-SPEC-MCP-0 |
| 4 | Options A–F; Refuse polyglot/product now |
| 5 | Training vs false-green; FREEZE |
| 6 | This memo + Spike charter — **not** Spec Approve; Implement Refuse for product |

---

## 9. One-line recommendation

**Yes — a thin read-only Spec MCP is the right place to “train” without
repo-dump hallucination; add Rust (schema/digest) and maybe Go (corpus
snapshot) as libraries/sidecars after Python v0 works. Keep WASM LockCheck and
full polyglot for the product verify surface later — do not bolt them onto Spec
MCP day one.**
