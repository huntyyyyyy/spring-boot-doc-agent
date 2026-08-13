---
title: Quality backlog — Active tip + queues
status: ACTIVE — one stream at a time
date: 2026-08-10
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
ledger_archive: docs/research/archive/quality-backlog-ticket-ledger-2026-08-10.md
rule: Spec → Implement → Verify → Archive; no parallel SoT thrash
---

# Quality backlog

**How to read this file**

| Section | Meaning |
| --- | --- |
| **1. Active tip** | The only Implement stream right now |
| **2. Next after Active** | Ordered candidates — do not start in parallel |
| **3. Draft Specs (parked)** | Research exists; **no Implement** until Approve |
| **4. Conditional** | Only when a gate on touched files forces it |
| **5. Done** | Closed epics — do not reopen as “P0” |
| **6. Refuse** | Never schedule |

Ticket-level history (old P0–P38 tables): [`archive/quality-backlog-ticket-ledger-2026-08-10.md`](archive/quality-backlog-ticket-ledger-2026-08-10.md).

**Hard invariants:** `fail_under=98.7`, complexipy ≤5, size ≤225; no `utils/` grab-bag; one tip writer.

---

## 1. Active tip (NOW)

**Active:** land combined tip #119, then resume E-COH1

| Field | Value |
| --- | --- |
| **Stream** | Land combined tip **#119**, then resume **E-COH1** |
| **Branch / PR** | `cursor/repo-and-context-combined-83d2` → [`#119`](https://github.com/huntyyyyyy/spring-boot-doc-agent/pull/119) |
| **Why** | Research stack is ahead of Implement; E-COH1 was paused until this tip lands |
| **Already on tip (Done)** | **E-REPO1-A** (`semantic_eval` / `docs_site` nest + `-m` shims); folds of #113–#118; **E-MDC0** docs + `.cursor/rules` pack (`process/47`); **E-LOG0** session-log nest (≤225 LOC + `START__slug`) |
| **Do not do in this stream** | New research epics; Approve-all Drafts; E-CTX1 / E-DYN1 Implement; parallel tips; E-MDC0 must not block E-COH1 code |

**E-COH1 exit (when resumed):** CGQ3 Accept rows (Concern→Remedy→Depth→Witness) on reshape; `check_public_surface` hard; no mechanical LOC chops. Design: [`docs/design/concept-split-cohesion-design-2026-08-09.md`](../design/concept-split-cohesion-design-2026-08-09.md).

---

## 2. Next after Active (one at a time)

| Order | Epic | Action | Gate |
| --- | --- | --- | --- |
| A | **E-REPO1-B** | `pipeline`↔`scanning` cycle-break → further nests | After #119 merge; one-way edges + tach |
| B | **E-LEG** remainder | Ordered size offenders: TOOL4 → PIPE1 → QUERY1 → STF1 | After E-COH1 green slice |
| C | **E-OCS** operator | Live `run-plant.sh ocs` + OpenAPI join evidence | Operator checkout (not tip theater) |
| D | **E-UX2** | Claims / code_quality headline + `<details>` | Optional |
| E | **E-STK3** | Cycle-focus rotator / LLM ranker | Defer — not required for G1–G6 |

---

## 3. Draft Specs (parked — no Implement)

| Epic | Topic | Research entry |
| --- | --- | --- |
| **E-REPO0** | Full DDD structure packet (Wave 0/0.5 shipped; Spec still Draft) | `bounded-contexts/21–24` |
| **E-CTX0** | Agent context hygiene / algorithm-first masking | `process/26–28` |
| **E-DYN1** | Dynamics metaphor hygiene; physical substrates **Refuse** | `process/43` (+ 20/21/44/45) |
| **E-TACH0** | Tach layers / depends_on as architecture SoT | `bounded-contexts/20` |
| **E-SOL0** | Concern→remedy vocabulary | `process/23` |
| **E-GND0** | Tip-grounding MCP (demoted) | `process/25` |
| **E-AST0** | Tailored ast-grep packs Spec (vacuity Implement already Done) | `stage0/astgrep-tailored-packs-…` |
| **E-OAS0** | Operator/agent surface CLI+MCP+retrieval | `process/37` |
| **E-QUERY0 / E-CERT0 / E-FACT0** | Cold BC Spec seeds | cold-product + stage0 maps |
| **E-CPL0** | Control-plane closed-loop | `process/35` |
| **E-RT0 / E-RUST0 / E-POLY0 / E-LANG0** | RT assertion / Rust toolscape / polyglot | `process/32–33`, `39–41` |
| **E-LINT0** | Import resolution: keep ruff; add ty for unresolved top-of-file imports | `process/46` |
| **E-MDC0** | Optimized MDC DevEx (activation algebra; not mass `.md`→`.mdc`) — docs + `.cursor/rules` on #119 | `process/47` |
| **E-TOOL0** | Complete toolscape (agent + repo + developer) — full polyglot lanes (Rust/Go/Ruby/Clojure/Elixir/JVM/.NET/PHP/TS/WASM/…) Pilot-before-Refuse | `process/48` |
| **E-IK0** | Intent Kernel v3 — parked draft; **no Implement**. Unblock = D-00 + D-01 + five failing tests (`process/50`). Evidence record: `process/49`. | `process/50` |

Human Approve one Spec → then one Implement tip. Do not open sibling Drafts as Active.

---

## 4. Conditional (not the default “start here”)

| When | Do | Epic / note |
| --- | --- | --- |
| Size ratchet fails on a **touched** module | Thin toward ≤225 (vertical slice; no utils bag) | Legacy **P0** hygiene — not the product roadmap |
| Dual-mode / climb work touches measure code | Re-check oracle vs climb artifact **16-A** | Already shipped as E-CM*; only if regressing |

---

## 5. Done (do not reopen as Active)

Compact ledger. Detail: [archived ticket tables](archive/quality-backlog-ticket-ledger-2026-08-10.md).

| Epic | Outcome |
| --- | --- |
| **E-CM0–2** | Dual-mode Spec / Implement / process hygiene |
| **E-TEST0–1** | Domain markers + ABI shards |
| **E-CI0–1** | Thin `ci.yml` + reusable BCs |
| **E-RUN0–1** | Suite-stalking sensors (Spec + D1/D2/D17) |
| **E-QA0–2** | Adequacy Spec + sensors + Climb Archive checklist |
| **E-UX0–1** | Summary-first UX + step-summary |
| **E-KH0–1** | Kitchen Spec + `KitchenArtifacts` |
| **E-MOD0–3** | Pipeline/Stage-0 modularity waves |
| **E-FAC0 / E-RES0 / E-CUR0** | Façade poke + design-research + Cursor hooks |
| **E-LEG0 + E-SCAN1** | Legacy Spec + scanning/astgrep façade |
| **E-CQL0–1** | CodeQL fingerprint skip |
| **E-DOC0–1** | Research taxonomy + look-first map |
| **E-STK0–1** | Stalker Spec + G1–G6 sensors |
| **E-COH0** | Cohesion Spec Approve (Implement = E-COH1 Active) |
| **E-HOT0–1** | Post-merge gate repair Spec + Implement |
| **E-STACK0** | ≥10k★ stack rescope Spec |
| **E-CGQ0** | Codegen-quality dimensions Spec |
| **E-KNOB0–1** | Quality setpoints (no god file) |
| **E-HOOK0–2** | Pre-push + local gates + oracle remesure |
| **E-TEL0–2** | Telemetry ETL + path-parity G7–G10 |
| **E-SEL0–1** | Domain pytest select + fine ABI |
| **E-SEARCH0** | Allow ripgrep; prefer ast-grep for citations |
| **E-OCS0 + plant/remeasure** | Dual plant Spec + fail-closed plant + floors tooling |
| **E-AST1** | Vacuity pack hard in `pre_pr` |
| **E-REPO1-A** | First nest: `semantic_eval` + `docs_site` + shims |
| **E-LOG0** | Session-log nest: ≤225 LOC packs + `START__slug` names; stub kept |
| **P32 Harn/Nimbus/noprop** | Stance recorded — **Refuse** as product deps |

---

## 6. Explicit Refuse (do not schedule)

- Scoped Cover% or LLM-judge as 98.7 proof  
- PID / fuzzy “confidence of green” on oracle floor  
- Cross-worktree / cross-job `coverage combine` for oracle  
- Suite-wide pytest-xdist on the cov cell  
- `utils/` grab-bag; raise LOC/complexipy caps  
- Parallel tip thrash / sibling branches for the same stream  
- Physical tip substrates (DNA/RC/ionic/…) as product deps (**E-DYN1**)  
- MemGPT / viral ★ memory products as context SoT; token-prune of action grammar (**E-CTX0**)  
- Backstage / Spec Kit WorkflowEngine / Sonar as merge or runtime SoT  
- In-tree Rust/WASM-by-default without profiled Spec  
- Unattended AI merge; MCP `generate_code` tip writer  
- Chat-dump research SoT; DDIA-shaped nesting under `docs/research/`  

Full historical Never-list: see archive ledger § “Suggested next” snapshot.
