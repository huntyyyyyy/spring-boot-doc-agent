---
title: VA architecture method — ATAM QAS · constraints · tactics · ADR · formal boundaries
status: RESEARCH COMPLETE — methodology gate before Design/Pilot (amends RE + process/53)
date: '2026-08-10'
epic: VA
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
related:
  - docs/requirements/

  - research/adversarial/adversarial-ddia-solid-polyglot-2026-08-10.md
  - research/adversarial/re-master-adversarial-critique-2026-08-10.md
  - research/polyglot/pilot-mental-models-polyglot-lanes-2026-08-10.md
  - docs/adr/README.md

  - .cursor/rules/00-constitution.mdc
do_not:
  - Let budget adjectives (≤2s) influence Design without a six-part QAS
  - Confuse constraints with requirements
  - Treat C4/orchestra diagrams as living SoR without ADRs
  - Claim tip code is Coq/Isabelle-proved because Wasmtime exists
  - Skip ATAM tradeoff recording when choosing cache/async/WASM/SQLite
sources:
  web:
    - https://www.sei.cmu.edu/documents/629/2000_005_001_13706.pdf
    - https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
    - https://plv.mpi-sws.org/rustbelt/popl18/paper.pdf
    - https://verus-lang.github.io/verus/guide/
    - https://conrad-watt.github.io/papers/watt2021.pdf
    - https://iris-project.org/pdfs/2024-oopsla-iris-mswasm.pdf
    - https://github.com/WasmCert/WasmCert-Isabelle
  github:
    - https://github.com/verus-lang/verus
    - https://github.com/tlaplus/tlaplus
  arxiv_or_acm:
    - Wright CSP connectors (Allen/Garlan); Rapide posets; Darwin π-calculus
  mcp: https://mcp.deepwiki.com/mcp
last_reviewed: '2026-08-10'
---

# Architecture method for VA — QAS before Design

**User correction (accepted).** process/53 restored polyglot mental models but
still let **assumption-shaped NFRs** (“≤2s warm”) steer Pilot talk. That is not
architecture engineering. Before a non-functional need may influence Design:

1. Rewrite it as an **ATAM quality-attribute scenario** (six parts).  
2. Keep **constraints** in a separate ledger (what is fixed).  
3. Enumerate **tactics**, mark **sensitivity** and **tradeoff** points.  
4. Record the chosen tactic in a **Nygard ADR** (context/decision/status/consequences).  
5. Optionally check connector/protocol properties (ADL / TLA+) and treat
   Rust/WASM boundaries as **provable trust surfaces** only where the literature
   actually supports that claim.

This memo is the **methodology SoR**. It amends the RE package and blocks
Design influence from incomplete NFRs.

---

## 0. Bloom

| Level | Evidence |
| --- | --- |
| **1** | SEI ATAM TR; Nygard ADR; Wright/Rapide/Darwin survey; RustBelt; Verus; Watt/WasmCert; Iris-MSWasm |
| **2** | Map QAS → VA actors/artifacts (LockCheck, SCIP index, receipt, tip oracle) |
| **3** | Concrete QAS for Must NFRs; ADR path `docs/design/adr/` |
| **4** | Tactics vs tradeoffs (cache↔freshness, WASM↔latency, SQLite↔Datascript) |
| **5** | False claims: “Wasmtime ⇒ proved”; “C4 stays true without ADR” |
| **6** | ATAM-* / ADR-* / FML-* tickets — Design blocked until Must QAS exist |

---

## 1. Diagnosis — what we had wrong

| Artifact | Defect |
| --- | --- |
| `REQ-N-01` “≤2s resolve” | Adjective budget, not a scenario (no stimulus source/environment/measure method) |
| process/53 orchestra diagram | Useful cartography; **not** a decision record — goes stale without ADRs |
| “Pilot WASM for sandbox” | Tactic without tradeoff vs native LockCheck latency / fuel determinism |
| Formal buzzwords in RE-MASTER | Implementation fashion, not layered: ADL check ≠ Iris proof ≠ tip gate |

**Rule (hard).** An NFR that is not a completed QAS may appear only as
`status: incomplete-qas` and **must not** appear in Design `approved_decisions`
or Pilot Accept until rewritten.

---

## 2. Quality Attribute Scenario form `[Evidenced — SEI ATAM]`

Six components (stimulus source · stimulus · environment · artifact · response ·
response measure). Example shape from the user, specialized to VA:

### Template

| Field | Prompt |
| --- | --- |
| **ID** | `QAS-N-xx` (links to `REQ-N-*`) |
| **Quality** | performance / security / modifiability / availability / … |
| **Stimulus source** | Who/what triggers |
| **Stimulus** | Exact event |
| **Environment** | Load / mode / failure / peak |
| **Artifact** | Component that must respond |
| **Response** | Observable behavior |
| **Response measure** | Quantitative pass/fail + how measured |
| **Priority** | Must / Should (from MoSCoW) |

### Worked Must rewrites (draft — replace old NFR influence)

#### QAS-N-01 — warm resolve latency

| Field | Value |
| --- | --- |
| **Stimulus source** | Agent operator (A-OP) or CLI `va resolve` |
| **Stimulus** | Request binding for one injection site / type |
| **Environment** | Local laptop; **warm** registry+SCIP already loaded; corpus-scale tree; swap=0 |
| **Artifact** | `WiringResolver` + SQLite registry |
| **Response** | Return impl symbol **or** `Unknown` + reason_code |
| **Response measure** | Wall p95 ≤ *T* ms over *N*≥30 calls on VS-corpus harness; record *T* from Spike (do not invent *T* in Design until measured). Fail if any silent pick under multi-candidate. |

#### QAS-N-02 — lock check on save path

| Field | Value |
| --- | --- |
| **Stimulus source** | Developer save / `fitness_check` |
| **Stimulus** | One changed Java file’s outbound edges |
| **Environment** | Warm locks+graph; peak = 10 concurrent checks on same machine |
| **Artifact** | `LockCheck` (native first) |
| **Response** | Violation report or clean; receipt emitted |
| **Response measure** | p95 ≤ *U* ms (Spike-measured); receipt schema valid 100%; zero missing witness IDs |

#### QAS-N-05 — local-first privacy

| Field | Value |
| --- | --- |
| **Stimulus source** | Default Pilot config |
| **Stimulus** | Full Must verify path (index→resolve→lock→receipt) |
| **Environment** | Offline network namespace / egress deny |
| **Artifact** | Python ACI + registry + LockCheck |
| **Response** | Completes without outbound sockets |
| **Response measure** | Packet capture / deny-net harness: 0 egress; exit 0 |

#### QAS-N-06 — determinism

| Field | Value |
| --- | --- |
| **Stimulus source** | CI |
| **Stimulus** | Re-run verify twice on same `(tree_sha, locks_version, scip_sha)` |
| **Environment** | Clean worktree; same binary digests |
| **Artifact** | Full Must spine |
| **Response** | Identical resolve outcomes + receipt witness sets (modulo timestamp field if separated) |
| **Response measure** | Byte-identical canonical JSON (timestamp stripped) across 2 runs × 5 fixtures |

**Incomplete → complete:** until Spike fills *T*/*U*, mark measure as
`MEASURE-TBD` and **forbid** Design claiming a numeric SLA.

---

## 3. Constraints ≠ requirements `[Evidenced — ATAM / RE practice]`

| Kind | Meaning | VA examples |
| --- | --- | --- |
| **Requirement** | Stakeholder-valued capability/quality (can MoSCoW) | QAS-N-01 latency scenario |
| **Constraint** | Fixed for this wave; not traded casually | Python tip writes `coverage.xml`; no dual Cover%; Java 17/21 · Boot 3.2/3.3 envelope; local-first default; constitution complexipy/LOC |

Constraints live in RE **§Constraints** (new). Changing a constraint needs an
ADR + explicit risk, not a quiet Design edit.

---

## 4. Tactics → sensitivity → tradeoff `[Evidenced — SEI ATAM]`

For each QAS, list **candidate tactics**, then mark:

- **Sensitivity point** — decision that strongly affects one quality  
- **Tradeoff point** — same decision moves two qualities in opposite directions  

### VA starter tradeoff table (must be ADR’d when chosen)

| Decision knob | Helps | Hurts | Class |
| --- | --- | --- | --- |
| Aggressive graph/SCIP cache | QAS latency | Freshness / stale false-green | **Tradeoff** |
| WASM LockCheck guest | Capability isolation | Latency; host/guest drift risk | **Tradeoff** |
| SQLite as registry SoR-derived | Deterministic SQL verify | Less flexible ad-hoc graph ask | Sensitivity (modifiability of queries) |
| Export EDN + bb Datascript | Query richness | Dual-view drift unless goldens | **Tradeoff** |
| Async Go watch reindex | Perceived freshness | Consistency windows; stamp races | **Tradeoff** |
| Unknown hard-fail (strict) | Safety / honesty | Availability of “green” under ambiguity | **Tradeoff** |
| Embeddings / RAG on verify path | Suggest UX | Truthfulness (Refuse for Must) | Category error |

**ATAM output we will keep:** not a slide deck — a short **utility tree** of
prioritized QAS + this table + risks. Diagrams illustrate; **ADRs decide**.

---

## 5. Architecture Decision Records `[Evidenced — Nygard]`

**Format.** Context / Decision / Status / Consequences (one decision each).  
**Location.** `docs/design/adr/adr-NNN-<slug>.md` (see README).  
**Rule.** Any Design choice that affects structure, NFRs, deps, interfaces, or
construction technique **requires** an ADR before Implement. C4 / orchestra
diagrams cite ADR IDs; without them they are **non-SoR sketches**.

Seed ADRs (proposed, not Accepted):

| ID | Decision theme |
| --- | --- |
| ADR-001 | SQLite (not LanceDB/Kuzu) as Pilot registry |
| ADR-002 | Packwerk-shaped lock IR (pattern, not tip Ruby) |
| ADR-003 | Native LockCheck before WASM; WASM = trust-boundary Pilot |
| ADR-004 | bb+Datascript as query sidecar with SQL goldens |
| ADR-005 | Python remains coverage/claims writer |

---

## 6. Architectural analysis languages & model checking

### 6.1 Classical ADLs `[Evidenced — Wright / Rapide / Darwin literature]`

| ADL | Semantics | Check |
| --- | --- | --- |
| **Wright** | CSP connectors/ports | Deadlock-freedom; port↔role compatibility (FDR-style) |
| **Rapide** | Partially ordered event sets | Simulation / trace constraint checks (sampling, not all paths) |
| **Darwin** | π-calculus | Dynamic reconfiguration structure |

**Stance for this repo.** Full Wright/Rapide toolchains are research-era /
heavy — **Pattern**, not tip dep. **Adopt the properties**: name connectors
(Index→Registry, Registry→Resolve, Resolve→LockCheck, LockCheck→Receipt) and
state compatibility obligations in Design. Optionally encode 1–2 protocols in
**TLA+** / PlusCal and run **TLC** for deadlock / invariant violations on the
watch→reindex→verify stamp protocol (state-explosion risk → keep models tiny).

### 6.2 TLA+ `[Evidenced — TLA+ practice]`

**Pilot use.** Spec the Go watch stamp + ACI stale-refuse protocol; prove
“no verify Accept on stale digest.” Not for Spring DI itself.

---

## 7. Verified boundaries (implementation trust surfaces)

Honest layering — what literature actually gives us:

| Layer | Claim | Evidence | Our use |
| --- | --- | --- | --- |
| **Safe Rust** | Ownership prevents UB / data races *in the model* | RustBelt (Iris/Coq) `[Evidenced]` | **Trust language**; not automatic proof of *our* crates |
| **Unsafe encapsulation** | Library must meet semantic VC | RustBelt library proofs | Unsafe in LockCheck/host → review + optional Verus |
| **Functional correctness** | Spec ↔ code | Verus (SMT); RefinedRust (foundational) `[Evidenced]` | **Pilot later** on tiny pure resolve/lock IR core — not whole tip |
| **WASM type soundness** | Spec mechanised; soundness proved | Watt → WasmCert-Isabelle/Coq `[Evidenced]` | Trust **language** boundary |
| **Capability safety** | Module can’t escape except granted caps | Iris-MSWasm (MSWasm) `[Evidenced]` | **Design meaning** of WASM LockCheck: deny FS/net; fuel/epoch host limits; **do not** claim Iris proof of our guest unless we invest FML Spike |
| **Host sandbox config** | Deny-by-default WASI + fuel | Wasmtime Config docs | **Confirmed engineering** control for Pilot |

**Architecture diagram rule.** A WASM box may be labeled
`trust-boundary (capability-sandbox)` citing this memo + ADR-003. It may
**not** be labeled `proved` unless an FML ticket lands machine-checked
artifacts in-tree.

---

## 8. Create — methodology tickets

| ID | Ticket | Acceptance |
| --- | --- | --- |
| **ATAM-1** | Rewrite all Must `REQ-N-*` as QAS-N-* six-part | No Must NFR without measure method; MEASURE-TBD allowed only pre-Spike |
| **ATAM-2** | Constraints ledger in RE (separate from REQ) | Table committed; constitution rows linked |
| **ATAM-3** | Utility tree + tradeoff table for VA | Sensitivity/tradeoff points named |
| **ADR-0** | ADR folder + template + ADR-001…005 proposed | Nygard sections present |
| **ADL-1** | Connector contract list (ports/roles) | Compatibility obligations in Design Spec |
| **TLA-1** | Optional TLC model for watch/stamp freshness | Tiny model; invariant “no Accept on stale” or drop |
| **FML-1** | Stance memo: RustBelt/Verus/Watt/Iris-MSWasm → Pilot scope | This §7; no false “proved” labels |
| **FML-2** | Spike: Verus on pure lock-IR evaluator (≤225 LOC core) | keep/drop |
| **GATE** | Design may use only QAS-complete Must NFRs + Accepted/Proposed ADRs | Checklist in Design Spec |

---

## 9. Status

Methodology research **Complete**. Prior Pilot talk that used raw latency
adjectives is **superseded** for Design influence. Next: land ATAM-1…3 + ADR-0
in the RE/ADR tree, then Design Spec.
