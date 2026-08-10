---
title: Adversarial critique — verified-slice RE-MASTER-001 v0.5.1 (AI rough draft)
status: RESEARCH COMPLETE — critique of inbound RE draft (not Spec Approve)
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
  - docs/design/ddia-north-star/domains/01-data-flow-and-truth/concepts/system-of-record-vs-derived.md

  - .cursor/rules/00-constitution.mdc
do_not:
  - Treat RE-MASTER-001 as requirements SoR until rewritten implementation-free
  - Pin Phi-3 / any LLM identity into FR text (model choice will change)
  - Use LanceDB cosine similarity as Accept for exact symbol resolution
  - Claim FN=0 on Spring locks while excluding AOP/conditional DI
  - Adopt Kuzu multi-instance LB architecture without Spike (embedded SoR)
sources:
  web:
    - https://www.iso.org/standard/72089.html
    - https://www.iso.org/standard/94091.html
    - https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http
    - https://modelcontextprotocol.io/extensions/tasks/overview
    - https://blog.modelcontextprotocol.io/posts/2026-07-28/
    - https://www.sonarsource.com/resources/library/iso-iec-25010-explained/
  deepwiki_ask:
    - sourcegraph/scip-java · Spring DI / incomplete compile
    - bytecodealliance/wasmtime · WASI deny-by-default / WasiCtxBuilder
    - kuzudb/kuzu · embedded vs multi-instance LB
    - tree-sitter/tree-sitter · ERROR nodes · incremental
    - lancedb/lancedb · vector search vs exact symbols
    - sourcegraph/scip · exact navigation vs embeddings
  mcp: https://mcp.deepwiki.com/mcp
last_reviewed: '2026-08-10'
---

# Adversarial critique — RE-MASTER-001 v0.5.1

**Subject.** Inbound AI draft
[`verified-slice-re-master-v0.5.1-draft.md`](../inbound/verified-slice-re-master-v0.5.1-draft.md)
(truncated paste; FR-16 incomplete).  
**Stance.** Useful as a **stimulus corpus** for RE quality. **Not** the
requirements SoR for this repo. Authoritative RE draft remains
[`docs/requirements-2026-08-10.md`](../../design/docs/requirements-2026-08-10.md).

**One-line verdict.** High theatrical compliance (clause numbers, corpora IDs,
p95 budgets) wrapping **implementation-bound “requirements,” invented
priority math, vapor corpora, and several false technical claims** — including
conflating **verify** with **RAG+LLM suggest**, and using **LanceDB** where
**SCIP/exact graph** belongs. Model pin (Phi-3) must leave FR text entirely.

---

## 0. Bloom

| Level | Evidence |
| --- | --- |
| **1** | ISO 29148:2018 / DIS Ed3 pages; MCP 2026-07-28 Streamable HTTP + Tasks; DeepWiki Ask (scip-java, wasmtime, kuzu, tree-sitter, lancedb, scip) |
| **2** | Map draft BR/FR onto VA Layers + SoR\|derived + this tip’s claims/coverage |
| **3** | Show which Accept methods could run on corpus/OCS vs which need nonexistent VS-* corpora |
| **4** | Embody / Adopt / Refuse table vs constitution + va REQ-* |
| **5** | Adversarial false-green/red; FN=0 impossibility; Kuzu LB fail |
| **6** | Critique tickets CRM-* + RE rewrite rules — no Implement from this draft |

---

## 1. What the draft gets right (keep)

| Keep | Why | Tier |
| --- | --- | --- |
| Separate **local** vs **org-wide** OpsCon | Matches VA local-first + optional daemon | Confirmed fit |
| Stakeholder SH-01…04 with **measurable proxies** | Better than nameless “users” | Adopt shape |
| BR-01 pre-push / IDE-time violation surfacing | Aligns REQ-F-05 / F-12 Should | Adopt intent |
| BR-03 auditable proof artefact | Aligns REQ-F-06 | Adopt intent |
| Explicit Spring Boot / Java LTS **version envelope** | Good scope fence (absent in va RE — add) | Adopt |
| MCP 2026-07-28 **Streamable HTTP** + `Mcp-Method`/`Mcp-Name` | Normative headers exist `[Evidenced — MCP transports]` | Adopt when Phase-2 MCP |
| Tasks as **extension** with `tasks/get` | SEP-2663 / ext-tasks `[Evidenced — MCP Tasks]` | Adopt pattern |
| NFR **reference hardware** concept | Needed for latency claims | Adopt (add Linux CI SKU) |
| WASM **deny-by-default** posture for untrusted eval | Aligns Wasmtime WASI `[Evidenced — DeepWiki wasmtime]` | Pilot Could |
| Documented **risk R-01 Spring Magic** | Same DI envelope gap as process/51 | Embody |

---

## 2. Category errors (fatal for 29148-shaped RE)

### 2.1 Implementation-bound FR text

29148 quality includes requirements that are **implementation-free** (need →
capability). The draft’s FR statements **are** the design:

| FR | Bound to (should be Design / Spike) |
| --- | --- |
| FR-02 | tree-sitter-java |
| FR-04 / FR-06 / FR-07 | LanceDB, Phi-3 Mini Q4_K_M, Ollama tag |
| FR-05 | scip-java |
| FR-08 | Wasmtime + concrete crate path |
| FR-13+ | Kuzu, Redis, OAuth 2.1+OIDC+PKCE |
| Scope | “common Rust core (MSRV 1.80)” |

**User note:** model choice **will change** — therefore FR-04/06/07 model
identity is already obsolete as a requirement. Remediation LLM must be an
**NFR/constraint slot** (“local inference provider meeting latency/RSS”) not a
pinned tag in FR.

### 2.2 Verify path polluted by RAG+LLM

OpsCon LOCAL MODE steps 4–5 put **RAG + Phi-3** on the critical path of
`fitness_check` (≤900 ms of the 2000 ms budget). That collapses:

| Concern | Correct layer (VA) | Draft |
| --- | --- | --- |
| Lock violation? | L2 LockCheck (deterministic) | Mixed with LLM |
| Remediation text | Optional suggest (sensor) | Mandatory FR-07 |
| Proof witness | Graph/lock IDs | Mentions ADR but LLM panel is core |

**Refuse:** LLM output as Accept for BR-01. Suggest may be Should/Could;
**verify Must not depend on it.**

### 2.3 LanceDB as “symbol index”

FR-04 Accept: symbol returns in top-10 with cosine ≥ 0.72.  
LanceDB is **vector/semantic** search `[Evidenced — DeepWiki lancedb]`.  
SCIP is **exact** defs/refs `[Evidenced — DeepWiki scip]`.  

Using embeddings as the primary index for lock checking is a **SoR category
error** (derived sensor treated as authority). Cosine thresholds are not
symbol identity.

### 2.4 Invented “priority derivation formula”

Header claims formula implements ISO 29148 §5.2 “necessary.” **Necessary** is a
**boolean quality characteristic** of a requirement statement, not a numeric
`(stakeholder_count × impact) / effort` score. The formula is **Unknown /
non-normative invention**. Nearly all FRs marked HIGH via it → MoSCoW theater.

### 2.5 Vapor corpora as Accept SoR

`VS-corpus-v1`, `VS-bench-v1`, `VS-eval-v1`, `VS-load-v1` are cited with
hand-labelled FN=0 / FP≤2.30% / MAP@10 ≥ 0.68. **None exist in this repo**
(`[Confirmed]` absent). Pass criteria referencing them are **unsatisfiable**.
Until corpora are created with methodology, Accept must bind to corpus/OCS /
fixture packs we already ship.

### 2.6 FN = 0 while excluding Spring Magic

FR-03 demands **zero false negatives** on architecture locks. R-01 simultaneously
excludes AOP proxies / weaving from AST scope. Those are not edge cases in Spring
codebases — they are common. FN=0 is **infeasible** under stated exclusions;
honest Accept is **soundness class + Unknown** (va REQ-F-02/F-07; ADV-3).

---

## 3. Standards header — scored

| Claim | Assessment | Tier |
| --- | --- | --- |
| 29148:2018 Ed2 published; confirmed 2024; stage 90.92 | Matches ISO page | Evidenced |
| DIS Ed3 stage 40.00 registered 2026-07-13 | Matches ISO 94091 | Evidenced |
| Ed3 no force until 60.60 | Correct process reading | Evidenced |
| Exact clause map (§5.2 nine chars, §9.3 StRS…) | Plausible; **not verified** against paid text in-session | Unknown |
| ISO 25010:2023 nine chars; Safety new; Usability→Interaction; Scalability under Flexibility | Matches secondary explainers | Evidenced (secondary) |
| MCP 2026-07-28 Streamable HTTP; `Mcp-Method`/`Mcp-Name` required | Primary transports page | Evidenced |
| Protocol-level sessions removed in 2026-07-28 | Spec notes removal | Evidenced |
| Tasks / `tasks/get` | Extension `io.modelcontextprotocol/tasks`, not core | Evidenced — draft underspecifies negotiation |
| “Stateless ⇒ no Set-Cookie” as BR-04 sole proof | Insufficient (OAuth cookies, affinity, task store) | Critique fail |
| INCOSE SE Handbook 5.0 cited | Name-drop only; no mapped practices | Unknown / theater |

---

## 4. Technical claim audits

### 4.1 tree-sitter “error-node-free CST” (FR-02)

**Fail.** Tree-sitter inserts `ERROR` / `MISSING` under recovery; grammar gaps
can yield errors even on intended-valid sources
`[Evidenced — DeepWiki tree-sitter]`. Accept must be: parse usable tree;
measure error-node rate; not “zero error nodes forever.”

### 4.2 scip-java “Risk: None” (FR-05)

**Fail.** Incomplete compile → partial SemanticDB; Spring DI richness
(`@Conditional`, AOP, SpEL) not SCIP’s job
`[Evidenced — DeepWiki scip-java]` + process/51. Risk register must list stale
index + Unknown.

### 4.3 Wasmtime “six Config DENY flags” + crate path (FR-08)

**Partial.** Deny-by-default WASI via `WasiCtxBuilder` is real
`[Evidenced — DeepWiki wasmtime]`. Clocks are **not** a simple six-boolean
`Config` DENY list as written; network is address-policy nuanced;  
`/crates/sandbox/src/lib.rs` is **vapor** relative to this monorepo
`[Confirmed]`. Rewrite as capability policy NFR + Design adapter.

### 4.4 Kuzu behind round-robin LB (FR-14 / BR-04)

**Fail.** Kuzu is **embedded**; RW single `Database` per path; not a shared
multi-writer graph for sticky-free LB `[Evidenced — DeepWiki kuzu]`.  
`traversal_id` + Redis might externalize state — then **Kuzu is not the shared
plane**. Architecture contradiction with “plain round-robin, no per-instance
config.”

### 4.5 MCP Tasks status enum (FR-15)

Draft: `pending | running | complete | failed`.  
Extension uses task lifecycle including `completed` / `failed` / `cancelled` /
`input_required` (+ polling / `tasks/update`) `[Evidenced — MCP Tasks]`.  
Status strings and **server-directed** task creation (client declares extension;
server decides) are mis-specified. Also: Tasks docs note `Mcp-Name` = `taskId`
for routing — tension with “no affinity” unless durable shared task store.

### 4.6 Proof tour SHA-1 (FR-09)

Git may use SHA-256 object IDs. “40-char lowercase hex SHA-1” is brittle.
ADR regex `ADR-[A-Z]+-\d{3}` / `RULE-\d{4}` may not match this repo’s epic/REQ
IDs. **Every** `fitness_check` requiring violated rule + ADR even on **clean**
passes is underspecified (null fields forbidden).

### 4.7 BR-01 vs `git push`

“Result delivered before `git push` completes” is not a controllable Accept
without a mandatory pre-push hook and defined failure mode. Prefer: IDE
diagnostic on save / explicit `fitness_check` / optional hook (this tip already
has hook epic history).

### 4.8 Document integrity

FR-04 duplicated mid-paste; FR-16 truncated; NFRs referenced (NFR-01a…04) but
not present in the paste; `/docs/rtm.csv` auto-generation claimed, absent;
epics T1–T5 / Phase 2 undefined in-repo.

---

## 5. Stakeholder / OpsCon gaps vs this product

| Gap | Draft | Needed here |
| --- | --- | --- |
| Tip / CI coverage SoR | Missing | A-CI: no dual `coverage.xml` (constitution) |
| Agent operator vs IDE developer | Collapsed into SH-01 | A-OP vs A-DEV (va) |
| Target-repo owner cost | Weak | Index rebuild / Unknown > wrong |
| Validation vs verification | Collapsed into proof tour | Architect validates lock *intent*; tool verifies |
| Social graph / people nodes | Org-wide KG | Out of scope for v1 Must (Could) |

---

## 6. Constitution / VA collision matrix

| Draft thrust | Stance |
| --- | --- |
| Rust MSRV core as *requirement* | **Refuse** as REQ — Pilot only after hotspot (process/50) |
| WASM-by-default for all lock eval | **Refuse** default; **Could** sandbox (REQ-F-16) |
| Phi-3 / Ollama on verify path | **Refuse** as Must; model-agnostic Should for remediation |
| LanceDB symbol SoR | **Refuse** |
| Org-wide Kuzu+Lance MCP Phase 2 | **Park** — Spike; not RE SoR |
| Backstage deferred | Aligns constitution Refuse as merge SoT |
| FN=0 Spring locks | **Refuse** — use Unknown taxonomy |
| VS-* corpora Accept | **Replace** with corpus/OCS + labeled fixtures when built |
| Priority formula | **Refuse** — use MoSCoW + RTM |

---

## 7. Embody / Adopt / Refuse (rewrite rules)

**Embody into va RE (next amend):**

1. Version envelope: Java 17/21 · Spring Boot 3.2/3.3 (or explicit R-03).  
2. Stakeholder measurable proxies (SH-style).  
3. Proof artefact mandatory field *set* as NFR/schema (implementation-free).  
4. Reference hardware + **CI Linux** SKU for NFR.  
5. MCP header/Tasks **Design constraints** when org-wide tool ships.

**Adopt (Design / Spike, not FR):**

- tree-sitter summaries; scip-java index; Wasmtime guest; Packwerk-like lock IR.  
- LSP diagnostics shape (FR-10 intent) as Should.  
- Async task polling pattern for long tools.

**Refuse (do not copy into SoR):**

- Model identity in FR.  
- Embedding cosine as symbol Accept.  
- FN=0 under Spring exclusions.  
- Fake priority formula & vapor VS-* thresholds.  
- Kuzu multi-instance LB as stated.  
- LLM on Must verify path.  
- Concrete crate paths as Pass Criterion Inspection targets.

---

## 8. Create — critique tickets (CRM-*)

| ID | Ticket | Acceptance |
| --- | --- | --- |
| **CRM-1** | Park inbound draft under `docs/research/inbound/` | Path exists; status DRAFT-AI; not Design SoR |
| **CRM-2** | Amend va RE: version envelope + SH proxies + model-agnostic remediation | REQ rows updated; Phi-* absent from FR |
| **CRM-3** | Split verify vs suggest in OpsCon | Must verify = graph+locks+receipt; LLM = Could/Should |
| **CRM-4** | Replace FN=0 with Unknown/soundness class Accept | Matches ADV-3 |
| **CRM-5** | Spike note: Kuzu embedded vs shared graph SoR | Keep/drop for BR-04 |
| **CRM-6** | Do **not** Implement from RE-MASTER-001 | Tip stays E-COH1 / RE Approve gate |

---

## 9. Status

Critique **Complete**. RE-MASTER-001 is a **rough AI draft** — keep as critique
fuel; **rewrite** before stakeholder Approve. VA RE package remains the
working SoR until a human-approved merge of Adopt items.
