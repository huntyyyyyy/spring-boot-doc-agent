---
title: VA Pilot depth — mental models · histories · polyglot implementation lanes
status: RESEARCH COMPLETE — Pilot research gate (before Design Spec / Implement)
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
  - research/polyglot/

  - research/mdc-devex/
  - docs/design/ddia-north-star/domains/01-data-flow-and-truth/concepts/system-of-record-vs-derived.md

do_not:
  - Flatten Pilot to “Python only” and drop Packwerk/bb/Go/SQLite/WASM lanes
  - Treat SCIP transmission as Spring DI resolve
  - Use LanceDB/Kuzu as symbol or multi-writer SoR in v1 Pilot
  - Dual-write coverage.xml from any sidecar
  - Implement without Spike keep/drop exits per lane
sources:
  github:
    - https://github.com/Shopify/packwerk
    - https://github.com/scip-code/scip/blob/main/docs/DESIGN.md
    - https://github.com/sourcegraph/scip-java
    - https://github.com/tonsky/datascript
    - https://github.com/babashka/babashka
    - https://github.com/spf13/cobra
    - https://github.com/extism/extism
  web:
    - https://docs.wasmtime.dev/examples-interrupting-wasm.html
    - https://docs.wasmtime.dev/api/wasmtime/struct.Config.html
    - https://sourcegraph.com/blog/announcing-scip
  deepwiki_ask:
    - Shopify/packwerk · package.yml · todo · mental model
    - babashka/babashka · SCI · datascript feature
    - tonsky/datascript · EAV · Datalog · vs SQLite/Neo4j
    - spf13/cobra · command lifecycle
    - sourcegraph/scip-java · index.scip · SemanticDB
    - extism/extism · vs Wasmtime PDK
  mcp: https://mcp.deepwiki.com/mcp
last_reviewed: '2026-08-10'
---

# VA Pilot depth — why these pieces exist, and how we pilot them *rich*

**Problem this memo fixes.** Prior chat compressed the Pilot to “thin Python
slice.” That was correct for **Must verify** (graph + locks + receipt) but
**wrong** as product framing: the distinctive VA feature set is a
**polyglot orchestra** (Packwerk-shaped locks, SQLite registry, Babashka graph
brain, Go watch chassis, WASM sandbox) *on top of* the Python tip — doctrine
already in process/40–41/48/51. Adopt-lists without history and mental models
are not enough to Design or Implement.

**Gate.** More research *of this depth* was the missing step. This memo is the
**Pilot research SoR**. Design Spec (VA-1 / ADV-1…3) cites it. Implement still
needs RE Approve + one Active-tip reorder.

---

## 0. Bloom

| Level | Evidence |
| --- | --- |
| **1** | Packwerk README; SCIP DESIGN.md; scip-java index path; Datascript EAV; bb SCI; Cobra hooks; Wasmtime fuel/epoch; Extism PDK |
| **2** | Map each tool to Layers L1/L1b/L2 + SoR\|derived + tip vs sidecar |
| **3** | Concrete Spike commands on corpus/OCS; module seams ≤225; keep/drop |
| **4** | Why not Neo4j/Kuzu/LanceDB-as-symbols; Extism vs Wasmtime; bb vs JVM Clojure |
| **5** | False green/red per lane; FN≠0 Packwerk honesty; SCI limits |
| **6** | PIL-* Spike tickets — rich multi-lane Pilot, not flatten |

---

## 1. Master mental model — orchestra, not monolith

```text
                 ┌─────────────────────────────────────┐
  Policy SoR     │  locks/*.yml  ·  .mdc  ·  claims     │  (git)
  (L2 intent)    └──────────────┬──────────────────────┘
                                │ Packwerk-shaped IR
                                ▼
  Verify path    ┌─────────────────────────────────────┐
  (Must)         │ LockCheck  →  cycle/layer  → receipt │
                 └──────────────┬──────────────────────┘
                                │ edges from
                                ▼
  Wire graph     ┌─────────────────────────────────────┐
  (L1b derived)  │ SQLite bean/dep registry + resolve  │
                 │   Unknown > wrong                    │
                 └──────────────┬──────────────────────┘
                                │ symbols from
                                ▼
  Where          ┌──────────────┴──────────────┐
  (L1)           │ SCIP index.scip (transmit)  │← scip-java
                 │ tree-sitter / ast-grep fast │
                 └─────────────────────────────┘

  Sidecar brains (Pilot — enrich, never Cover% SoT)
  · bb + Datascript  — Datalog ask over EDN export of graph
  · Go Cobra daemon  — watch → reindex → notify ACI
  · WASM/Extism      — sandboxed LockCheck guest (parity w/ native)
  · Python tip       — ACI, claims, coverage.xml writer, orchestration
```

**Invariant.** One tip writer for merge floors. Sidecars are **sensors /
query / chassis / sandbox**. That is the unique richness — not a second kernel.

**Correction to earlier advice.** “Stay in this repo + thin Pilot” meant:
don’t greenfield GitHub; don’t tip-rewrite Rust. It did **not** mean delete the
Ruby/Clojure/Go/SQLite/WASM lanes from the Pilot *plan*.

---

## 2. Histories & mental models (why each piece looks like that)

### 2.1 Packwerk → lock package IR `[Evidenced — Shopify Packwerk]`

**History.** Shopify’s modular-monolith pain: Ruby has no package boundary
enforcement; Sandi Metz: *knowing who you are raises cost of change*. Packwerk
= static constant-reference checker over Zeitwerk packages.

**Mental model to copy (not tip Ruby):**

| Concept | Meaning | Our lock IR analogue |
| --- | --- | --- |
| `package.yml` | Package manifest | `locks/<pkg>.yml` or FM on package dir |
| `enforce_dependencies` | Declared edges only | `may_depend_on: [services]` |
| Privacy / public API | Only public constants importable | `public:` paths / stereotypes |
| `package_todo.yml` | Bankruptcy / gradual enforce | `locks/todo.yml` — old violations parked |
| Acyclic validator | Dep graph must be DAG | Cycle check on virtual graph |
| Prefer FN over FP | Dynamic Ruby → miss some refs | Same honesty for Spring Magic |

**Limitation we inherit.** Packwerk ignores method calls/objects; we ignore
runtime DI we cannot see → **Unknown**, not silent green.

**Pilot deliverable.** YAML schema + checker against corpus controller→repo;
**no** `gem install packwerk` as tip dep — **Adopt pattern** only. Optional
read of Rust `packs` later as Pattern.

### 2.2 SCIP → transmission, not storage `[Evidenced — SCIP DESIGN]`

**History.** LSIF’s opaque numeric IDs made incrementality and debugging hard.
SCIP = Protobuf with **human-readable symbol strings**; designed as
**transmission** from indexer → consumer, **not** a query DB.

**Mental model:**

| Layer | Role |
| --- | --- |
| scip-java | Produce `index.scip` via SemanticDB during compile |
| SCIP file | Portable defs/refs/impls blob |
| Consumer | **Must** build a query store (SQLite, etc.) |

`scip expt-convert` → SQLite is **experimental debug** (opaque occurrence
blobs) `[Evidenced — scip CLI]`. Our Pilot may **inspire** schema but should
own a **bean/dep-shaped** SQLite (or parallel tables), not treat expt-convert
as production SoR.

**scip-java path `[Evidenced — DeepWiki scip-java]`:**

- `scip-java index` auto-detects Gradle/Maven → SemanticDB → `index.scip`  
- Incomplete compile can still yield partial index unless `strictCompilation`  
- Spring DI / AOP still **not** in SCIP → L1b resolve is *our* job  

### 2.3 SQLite → derived operational registry `[Confirmed fit]`

**Why SQLite here (not Neo4j/Kuzu/LanceDB):**

| Store | Fit for Pilot | Why |
| --- | --- | --- |
| **SQLite** | **Yes — registry SoR-derived** | Single-file, local, SQL join for beans/edges, tip-friendly, matches “rebuild from SCIP+scan” |
| Datascript | **Yes — query sidecar** | Ephemeral Datalog over exported EDN; not durable merge SoR |
| Kuzu | **No for LB org-wide** | Embedded; multi-instance RW fails (process/52) |
| LanceDB | **No for symbols** | Vector sensor; not exact identity |
| Neo4j | **Defer** | Server tax; overkill for corpus Pilot |

**Mental model.** SQLite holds **facts we assert** after resolve:

```text
beans(id, type_symbol, impl_symbol, stereotype, qualifiers_json, …)
edges(from_symbol, to_symbol, kind, confidence, reason_code)
index_meta(scip_sha, tree_sha, built_at)
```

`confidence` / `reason_code` encode Unknown taxonomy. Rebuild = delete DB +
re-run pipeline (DDIA derived).

### 2.4 Babashka + Datascript → graph brain `[Evidenced — bb / Datascript]`

**History.** bb = native SCI Clojure for scripts (fast start, not long JVM
services). Datascript = immutable EAV + Datalog; “a little data,” ephemeral,
schema-on-read — born for client-side graphs, not multi-TB warehouses.

**Mental model:**

| Piece | Job |
| --- | --- |
| Python/SQLite | Authoritative derived registry |
| Export EDN | Snapshot of beans/edges for query |
| bb + Datascript | Ad-hoc architecture questions: “who depends on X?”, recursive rules |
| Full JVM Clojure / Noumenon | Defer / Watch |

bb can enable Datascript via feature flag at build time
`[Evidenced — DeepWiki babashka]`. Pilot may use a **published bb binary with
datascript** or thin EDN + `bb` script depending on available binary — Spike
records which.

**Unique value.** Interactive architecture REPL without standing up Neo4j —
this is a real differentiator vs “just another linter.”

### 2.5 Go + Cobra → chassis daemon `[Evidenced — Cobra]`

**History.** Cobra = kubectl-shaped command trees: root, persistent flags,
`PreRun`→`Run`→`PostRun`, completions, plugin naming.

**Mental model for us:**

| Command | Role |
| --- | --- |
| `va-daemon index` | One-shot / CI index |
| `va-daemon watch` | fsnotify → reindex dirty set → touch stamp / notify |
| `va-daemon serve-mcp` | Later Phase-2 |

Cobra itself is **not** a daemon framework — `Run` holds the loop; supervision
is OS/`systemd`/dev script. That is fine for Pilot.

**Unique value.** Local freshness without IDE coupling; Observer for L1
invalidation — research slate item, not fashion.

### 2.6 WASM / Extism → sandbox, not prover `[Evidenced — Wasmtime / Extism]`

**History.** Wasmtime: capability-safe embedder; **fuel** = deterministic
trap; **epoch** = low-overhead wall interrupt
`[Evidenced — Wasmtime Config / interrupting docs]`. Fuel/epoch do **not**
cancel blocking host/WASI — so LockCheck guest should be **pure** (bytes in →
violation JSON out), no FS/net.

**Extism** = higher-level plugin host on Wasmtime: PDKs (Rust/JS/Go/…),
timeouts, memory limits, host functions `[Evidenced — DeepWiki Extism]`.

| Choice | Pilot stance |
| --- | --- |
| Pure LockCheck in WASM | **Pilot** after native LockCheck green |
| Extism vs raw Wasmtime | Spike: Extism if multi-lang PDK wanted; Wasmtime if Rust-only guest |
| “WASM proves Spring” | **Refuse** (process/50) |

**Unique value.** Untrusted lock packs / agent-authored checks without host
escape — compliance story without equating sandbox to proof.

### 2.7 Python tip — why it stays `[Confirmed]`

Claims, `coverage.xml`, Stage-0 ast-grep, corpus harness, agent ACI already
live here. Constitution: one oracle writer. Polyglot **enhances**; it does not
replace.

---

## 3. End-to-end Pilot dataflow (implementation-level)

```text
corpus / OCS Spring tree
    │
    ├─(1)─ ast-grep Stage-0 stereotypes          [Embody — already tip]
    ├─(2)─ scip-java index → index.scip          [PIL-SCIP]
    ├─(3)─ decode SCIP + merge stereotypes
    │         → SQLite registry                  [PIL-SQL]
    ├─(4)─ WiringResolver → edges | Unknown      [PIL-RES]
    ├─(5)─ Lock IR (Packwerk-shaped) evaluate    [PIL-LOCK]
    │         optional: same IR in WASM guest    [PIL-WASM]
    ├─(6)─ proof-tour JSON receipt               [PIL-RCPT]
    ├─(7)─ export EDN → bb Datascript queries    [PIL-BB]
    └─(8)─ optional: Go watch reindex            [PIL-GO]
```

**Verify Must path** = steps 2–6 (deterministic).  
**Rich lanes** = 7–8 (+ WASM parity).  
**Not on Must path** = RAG, Phi-*, LanceDB, org Kuzu MCP.

---

## 4. Proposed module seams (≤225 LOC culture)

| Concept module | Responsibility | Lang |
| --- | --- | --- |
| `va.index_port` | Load/validate `index.scip` digest | Py |
| `va.symbol_fact` | Normalized symbol DTO | Py |
| `va.registry_sql` | SQLite schema + writers | Py |
| `va.wiring_resolve` | Multi-candidate → Unknown | Py |
| `va.lock_ir` | Parse Packwerk-shaped YAML | Py |
| `va.lock_check` | Evaluate IR vs edges | Py |
| `va.receipt` | Proof-tour schema emit/validate | Py |
| `va.edn_export` | Registry → EDN for bb | Py |
| `scripts/va/graph_repl.bb` | Datascript queries | bb |
| `cmd/lie0d/` (optional tree) | Cobra watch daemon | Go |
| `crates/lie0_lock_guest/` (optional) | WASM LockCheck | Rust→wasm |

No `utils/`. Ports first (ADV-2). Optional trees are **Pilot worktrees /
`pilots/`** gitignored from oracle if needed — never dual Cover%.

---

## 5. Research still open (honest Unknowns) — before/during Spikes

| ID | Question | Close by |
| --- | --- | --- |
| U-1 | Kitchen/OCS: does `scip-java index` complete? Partial? | PIL-SCIP receipt |
| U-2 | Stereotype vocabulary map: sg rules ↔ registry columns | PIL-SQL design note |
| U-3 | Lock IR v0 fields exact schema | PIL-LOCK + Packwerk mirror table |
| U-4 | bb binary: datascript included or pod? | PIL-BB keep/drop |
| U-5 | Extism vs Wasmtime for first guest | PIL-WASM Spike |
| U-6 | Go daemon: in-repo `cmd/` vs sibling repo | Prefer in-repo `pilots/lie0d` first |
| U-7 | SCIP→SQLite: custom schema vs expt-convert inspect | Prefer custom bean schema |
| U-8 | ADV-1 SoR matrix paper | Write in Design Spec |

These are **Spike exits**, not reasons to freeze.

---

## 6. Create — Pilot lane tickets (PIL-*)

Prereq: human **Approve** RE Must + Active tip = VA Pilot (or dedicated
Pilot branch after COH1). Each lane has **keep/drop**.

| ID | Lane | Work | Acceptance | Keep/drop |
| --- | --- | --- | --- | --- |
| **PIL-SCIP** | SCIP | `scip-java index` on corpus | `index.scip` + stats receipt; note partial/strict | Drop only if unusable on plants |
| **PIL-SQL** | SQLite | Schema + load symbols/stereotypes | Query bean-ish rows; rebuild script | Keep if rebuild < documented budget |
| **PIL-RES** | Resolve | WiringResolver + Unknown | Multi-impl fixture → Unknown; single → impl | Keep if Unknown rate explained |
| **PIL-LOCK** | Packwerk IR | YAML packages + cycle/layer | controller→repo red; todo file optional | Keep if IR executable (not prose) |
| **PIL-RCPT** | Receipt | JSON schema proof tour | Missing witness ID → fail | Keep |
| **PIL-BB** | bb+Datascript | EDN export + 3 Datalog queries | Queries match SQL goldens | Drop if bb/datascript friction > value |
| **PIL-GO** | Cobra watch | Reindex on file change | Stamp updates; ACI reads stamp | Drop if watch unreliable |
| **PIL-WASM** | Sandbox | Native vs guest LockCheck parity | Same violations; fuel trap test | Drop if parity cost > benefit |

Order: **SCIP → SQL → RES → LOCK → RCPT** (Must spine), then **BB ∥ GO ∥ WASM**
(rich lanes in parallel Spikes).

---

## 7. Adversarial (lane-aware)

| Attack | Lane | Control |
| --- | --- | --- |
| SCIP sold as DI | RES | Unknown taxonomy tests |
| Todo file hides forever | LOCK | Strict mode / bankruptcy report |
| bb answers ≠ SQLite | BB | Golden parity tests |
| Daemon stale stamp | GO | Digest in stamp; verify refuses stale |
| WASM/native drift | WASM | Property parity suite |
| Sidecar writes Cover% | all | Constitution + CI deny |

---

## 8. Status / how this unblocks the Pilot

| Artifact | Role |
| --- | --- |
| process/50 | Vision / Layers |
| process/51 | Adversarial + slate |
| process/52 | RE-MASTER critique |
| **process/53 (this)** | **Mental models + implementation Pilot lanes** |
| docs/requirements | REQ SoR |

**Still before code:** RE Approve · ADV-1…3 paper · tip reorder to VA.  
**Then:** execute PIL-* in this repo — **rich**, not flattened.
