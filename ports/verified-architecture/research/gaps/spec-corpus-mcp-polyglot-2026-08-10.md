---
title: Spec / corpus Model Context Protocol + polyglot language features — deep research
status: RESEARCH — FREEZE-aware; NOT product verify Model Context Protocol; NOT Implement Ready
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

**Banner.** This studies a **read-only Spec / corpus Model Context Protocol** that shrinks large language model
context and hallucination over the planning tree. It is **not** the product
`verify` / `resolve` / receipt server. Under FREEZE: research + optional Spike
only — do not schedule polyglot product Implement.

**User question (accepted):** Is there benefit to “training” on unfinished
contracts via tools (vs dumping the repo)? Can **Rust / WebAssembly / Go / other
lanes** already add features for that Spec surface — including ideas from the
polyglot portfolio (“last night” feature dump: WebAssembly LockCheck, Go watch, Ruby
locks, Clojure/bb, TS IDE, etc.)?

No literal “before bed” string in-repo; the matching backlog is the
**polyglot portfolio + Wave-3 enrichment + E-TOOL0 / tip-grounding Model Context Protocol** work
(`[Evidenced — ADR-0001/0004/0007/0009/0010`, `research/polyglot/*`,
`docs/research/process/25-tip-grounding-mcp-2026.md`, `48-complete-toolscape…`]).

---

## 0. Dual surfaces (do not conflate)

| Surface | Job | System of Record? |
| --- | --- | --- |
| **Planning Spec corpus** | Progressive disclosure for agents designing the engine | Spec docs / Decision Framework / FREEZE |
| **Verify engine Model Context Protocol** | Graph + locks + receipts over a *target* repo | Future product; Draft Interface Control Document only |

`BOUNDARY.md` already separates them. A Spec Model Context Protocol serves **surface 1**. Rust/WebAssembly
LockCheck belongs to **surface 2** (Wave-3 / Could) — useful later, wrong as
day-one Spec Model Context Protocol deps.

---

## 1. Why Spec Model Context Protocol can help (your inefficiency point)

| Mode | Cost | Hallucination mode |
| --- | --- | --- |
| Dump / re-parse whole port every turn | High tokens; contradictions (Adopt vs FREEZE) | Model invents “Chosen” as Accept |
| **Spec Model Context Protocol tools** return *one* STATUS / assumption / Interface Control Document slice | Low, auditable | Failures are `unknown_id` / path miss — visible |
| Product verify Model Context Protocol with fake greens | Medium | **False training** on unfinished oracles |

**Verdict:** unfinished **contracts as tools** = useful training; unfinished
**oracles as tools** = harmful. Spec Model Context Protocol is the former.

---

## 2. What already exists on the tip (parent repo)

| Artifact | State | Gap |
| --- | --- | --- |
| `adapters/mcp/server.py` | Read-only Stage-0 **pipeline run** query | Speaks protocol **`2024-11-05`** + `initialize` — **stale vs `2026-07-28`** `[Evidenced — server.py]` |
| E-GND0 tip-grounding Model Context Protocol memo | Spec Draft — tip probes, Refuse codegen tools | Not Implemented; depends other Approves |
| E-TOOL0 toolscape | Polyglot Pilot catalog for *this* monorepo | TOOL9: steal TS envelopes into **Python** host — no Node tip dep |
| TOOL10 | WebAssembly: bubblewrap first; Extism after fail | Tip sandboxing — not VA LockCheck |

**Implication:** you are not starting from zero — extend **tip / Spec grounding**,
do not invent a second verify stack. Upgrade path must pin **`2026-07-28`**
(stateless / handles) for any *new* server; legacy Stage-0 needs an explicit
compat Architecture Decision Record if kept.

---

## 3. Language feature map — Spec Model Context Protocol vs product verify

GitHub snapshot **2026-08-10** `[Evidenced]`: official software development kits — TypeScript ★~13k,
Python ★~24k, Go ★~5k, C# ★~4.5k, **Rust ★~3.8k** (active). Wasmtime ★~18.5k,
Extism ★~5.7k, wazero ★~6.3k.

| Language / runtime | Spec / corpus Model Context Protocol (now–Spike) | Product verify Model Context Protocol (later) | Tier for Spec Model Context Protocol |
| --- | --- | --- | --- |
| **TypeScript** | Cursor/IDE stdio; Architecture Decision Record ADR-0010 Model Context Protocol presentation | Product Model Context Protocol presentation | **Working hypothesis (Draft)** for Spec host — independent of tip Python |
| Python | **Refuse** for this port (Spec host, ACI, oracle writer) | **Refuse** | **Refuse** |
| **Rust** | **Spike host** (Working hypothesis): schema validate, frontmatter index, corpus digest, stdio Model Context Protocol | Engine + wasmtime host (Architecture Decision Record ADR-0007) | **Working hypothesis (Draft)** for Spec Model Context Protocol |
| **WebAssembly / Wasmtime / Extism** | Optional **sandboxed markdown/schema reader** plugin (deny net) — niche | LockCheck guest (Architecture Decision Record ADR-0004); isolation ≠ proof | **Could** after thin Spec Model Context Protocol works; **Refuse** as Spec Model Context Protocol requirement |
| **Go** | `corpus_version` / fsnotify invalidate Spec snapshot handle | Watch/reindex chassis (Architecture Decision Record ADR-0009) | **Could** sidecar for handle freshness |
| **Ruby** | Weak for Spec Model Context Protocol | Packwerk lock DX (Architecture Decision Record ADR-0003) | **Park** for Spec Model Context Protocol |
| **Clojure / bb** | Weak; optional EDN query over *exported* Spec index | Graph brain sidecar | **Park** for Spec Model Context Protocol |
| **C / Zig** | N/A | Niche systems/WebAssembly | **Refuse** Spec Model Context Protocol |

### Can WebAssembly/Rust “already be added” for Spec Model Context Protocol?

**Rust — yes, as a library feature, not as the only server.** Official
`modelcontextprotocol/rust-sdk` is real and maintained. Best Spec uses early:
deterministic `material_digest`-style hash of the Spec tree; JSON Schema checks
against `icd/mcp/*.schema.json`; reject oversized payloads. That trains agents
on **schema_invalid** without fake verify.

**WebAssembly — yes as capability sandbox for *untrusted* Spec plugins, no as prover.**
Same honesty as Architecture Decision Record ADR-0004: fuel/epoch = engineering control. For Spec Model Context Protocol, a
WebAssembly guest that only parses Markdown/JSON under deny-FS-except-corpus is a
**Could** hardening — not needed to get hallucination reduction. Product
LockCheck-in-WebAssembly remains Wave-3 / PIL-WebAssembly — **do not** drag it into Spec Model Context Protocol
v0.

**Go — yes for corpus watch.** Mint `spec_snap_…` when FREEZE/STATUS/icd change;
agents pass handle — mirrors product `snapshot_open` *pattern* without being
verify. Excellent “train on unfinished contracts” without false-green receipts.

**Ruby / Clojure — not for Spec Model Context Protocol v0.** Keep for product lanes.

---

## 4. Architecture options (scored as sensors)

**Honesty correction (user challenge, accepted):** earlier “Python host” reasoning
was largely **self-referential** — tip already has `adapters/mcp` + TOOL9 “steal
TS into Python,” so the agent preferred Python. That is **not** an earned
product decision; it is tip convenience. Treat host language as **re-openable**.

| Option | Independent why (ignore tip accident) | Tip convenience | Verdict |
| --- | --- | --- | --- |
| **A. TypeScript stdio Spec Model Context Protocol** | Cursor/IDE Model Context Protocol ecosystem; Architecture Decision Record ADR-0010 names TS for Model Context Protocol *presentation* | Medium (new tip dep vs TOOL9) | **Could** facade only — not Spec corpus SoT if Rust serves index |
| **B. Python stdio Spec Model Context Protocol** | — | Tip accident only | **Refuse** (2026-08-11) — not Could |
| **C. Rust stdio Spec Model Context Protocol** | Official rust-sdk; digest/schema; matches engine lane (Architecture Decision Record ADR-0007); frontmatter index SoT | Low tip ergonomics today | **Working hypothesis (Draft) for Spike** — user course-correct 2026-08-10: build Rust here, not tip Python |
| **D. Rust core + thin TS facade** | Separation: Cursor presentation vs corpus digest | More moving parts | **Could** after Rust host proves tools |
| **E. WebAssembly as Spec Model Context Protocol host** | Wrong job — sandbox guest ≠ host; no earned realtime-server Spec | — | **Refuse** as host |
| **F. WebAssembly sandbox for agent-generated tool probes** | User idea: spin capability-limited guests to test agent tooling | Separate Spike | **Could** (not Spec Model Context Protocol v0) |
| **G. Full polyglot Spec Model Context Protocol day one** | Prestige | — | **Refuse** |
| **H. Product verify Model Context Protocol now** | — | — | **Refuse** until deepen-3 |

### Independent decision vectors (host language)

| Vector | Fair content |
| --- | --- |
| **Why** | Cut dump/hallucination with typed Spec tools — not to bless tip Python |
| **What** | Read-only tools + stamps; `2026-07-28` or explicit legacy Architecture Decision Record; size caps |
| **Who** | Tip agents + human; maintainers must not be trapped by agent-written stack |
| **How** | stdio into Cursor `mcp.json`; optional later Rust digest crate |
| **When** | Optional Spike after/in parallel with deepen-3 — not Must |
| **Where** | New package under tip or port `packages/spec-mcp/` — **not** `packages/mcp-server` verify |

**Rejected reasoning:** “Choose Python because this session/adapters already used Python.”


| Tool | Returns | Trains |
| --- | --- | --- |
| `spec_status` | `STATUS.md` structured fields + FREEZE flag | Don’t Implement |
| `spec_assumption` | A-LOCAL…A-DEPTH from honesty memo | Explicit assumptions |
| `spec_icd` | Named Interface Control Document / schema path contents (size-capped) | Contracts not vibes |
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
| Less repo-wide parse / fewer contradiction hallucinations | **Yes** if tools are the System of Record path for tip agents |
| Practice `2026-07-28` handles / reject classes | **Yes** on Spec snapshot handles |
| Practice Rust/WebAssembly LockCheck | **No** via Spec Model Context Protocol — wrong surface |
| “Warm up” product verify | **Risky** — only after deepen-3; stub rejects OK, pass receipts **Refuse** |

---

## 6. Spike charter (optional — not scheduled as Must)

| ID | SPIKE-SPEC-Model Context Protocol-0 |
| --- | --- |
| Goal | Read-only Spec Model Context Protocol over `ports/verified-architecture` (+ honesty FREEZE) |
| Host | **Rust** stdio only (`SPIKE-SPEC-MCP-0`); pin `2026-07-28`; **Refuse** Python |
| Exit keep | Tip agent answers FREEZE/deepen-3 via tools without opening >N files; FX-SPEC-01 forged handle rejects |
| Exit drop | If tools just wrap `cat` with no size/deny discipline |
| Out of scope | Product verify tools; Python host/ACI; WebAssembly as Spec host |
| Follow-ons (Could) | Thin TypeScript facade for Cursor wiring; Go corpus watch; WebAssembly sandboxed reader guest |

Align with E-GND0: **Refuse** codegen / write tools on this server.

---

## 7. Agent-codegen bites

1. Building product `packages/mcp-server` “to help Spec” → FREEZE violation.  
2. Labeling WebAssembly Spec reader “proved.”  
3. Keeping `initialize` / `2024-11-05` while claiming `2026-07-28`.  
4. Polyglot day-one Spec Model Context Protocol (Ruby+bb+WebAssembly+Go) as prestige theater.  
5. Spec tools that return entire `ARCHITECTURE_BRIEF` (defeats the point).

---

## 8. Bloom

| Level | Evidence |
| --- | --- |
| 1 | software development kit stars; adapters/mcp; Architecture Decision Record ADR-0004/7/9/10; E-GND0; E-TOOL0 TOOL9/10 |
| 2 | Dual surfaces; language map |
| 3 | SPIKE-SPEC-Model Context Protocol-0 |
| 4 | Options A–F; Refuse polyglot/product now |
| 5 | Training vs false-green; FREEZE |
| 6 | This memo + Spike charter — **not** Spec Approve; Implement Refuse for product |

---

## 9. One-line recommendation

**Yes — a thin read-only Spec Model Context Protocol can train contracts without repo-dump
hallucination.** Host language is **re-opened**: do not pick Python because the
agent already wrote Python; prefer an independent score (TypeScript presentation
vs Rust engine DNA). WebAssembly is **not** the Spec host — it remains a **Could**
sandbox for agent-generated tool probes / later LockCheck. Product verify Model Context Protocol
stays Refuse until deepen-3.
