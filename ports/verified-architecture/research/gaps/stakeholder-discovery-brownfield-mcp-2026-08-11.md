---
title: Stakeholder discovery — brownfield repo MCP + metrics + stateless stack
status: RESEARCH — stakeholder Working hypothesis (not Accept; not Implement)
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
audience: [architect, stakeholder, agent]
freeze_class: sensor
look_first:
  - 01-vision/problem-frame/BOUNDARY.md
  - 04-constraints/open-questions/OQ-01.md
  - docs/adr/adr-0011-mcp-protocol-and-tool-surface.md
  - research/gaps/shallow-decisions-honesty-2026-08-10.md
  - research/gaps/deepen-receipt-beta-rho-2026-08-11.md
accepted: false
implements: discovery Block A + proposed thin OS MCP stack
---

# Stakeholder discovery (2026-08-11)

**Source:** human stakeholder answers (who / pain / 90-day metrics / preferred
stateless Model Context Protocol tool stack). This memo is **evidence**, not
Definition of Ready PASS and not a new Wave-1 tool list under FREEZE.

**Banner:** Implement = **Refuse**. Definition of Ready **D0 FAIL**. Do not
promote this stack into `icd/mcp-tools.md` without human Accept of open question
OQ-01 (boundary) and an explicit Embody/Adopt/Refuse pass that survives the
adversarial section below.

Whole words — root `GLOSSARY.md`.

---

## 1. Who `[Evidenced — stakeholder]`

Primary users: **software engineers and other technical people with access to a
repository** (agents + coworkers). Not org SaaS knowledge-graph tenants as MVP.

## 2. Pain `[Evidenced — stakeholder]`

| Pressure | Stakeholder wording (compressed) |
| --- | --- |
| Stale documentation | Docs routinely drift; expensive to trust |
| Brownfield Spec-driven design | Company drive to Spec-driven design on brownfield |
| Lost domain owners | Original implementers gone; questions have no living expert |
| AI cost / needle-in-haystack | Agents burn tokens hunting context without a correct, current map |
| Desired shape | Repository exposes a Model Context Protocol server that answers what agents/coworkers need, **correctly**, and **adjusts when code changes** |

## 3. Success metrics (≈90 days) `[Evidenced — stakeholder]`

Named sensors. None are Implement green by themselves; each needs a plant +
owner + fail-mode before Definition of Ready Accept.

| Metric | Stakeholder definition | Maps onto port entities (Hypothesis) | Tier |
| --- | --- | --- | --- |
| **Index lag** | Time from `git commit` / file save → Model Context Protocol index/embeddings updated | Derived index freshness; open question OQ-06; not “no index forever” | Stakeholder Must-pressure |
| **Stale fragment rate** | % retrieved chunks whose code signatures no longer exist at `HEAD` | Claim freshness / Proof-or-Stop Fresh; receipt digests | Aligns with FREEZE β/ρ |
| **Event processing throughput** | File-change events queued vs processed / sec under large install or pull | Indexer / watcher capacity Quality Attribute Scenario (N-01/N-02 still Spike-blocked) | Needs QAS plant |
| **Symbol coverage ratio** | % public functions / classes / API endpoints with up-to-date server-generated doc entry | Doc inventory vs SCIP/CST symbols — **Pilot invent** scorer | Adjacent to DynamicMCPBench-style effect checks |
| **Doc↔code divergence** | How often generated docs fail a secondary validation pass | EA-Graph dispositions `affected` / `unprovable`; dual-pass Accept | Aligns with claim memory |
| **Structural depth** | DeepWiki-style stub pages / deep pages | Spec corpus quality sensor (not verify SoR) | Could / Spec surface |
| **Answer accuracy / citation precision** | Answers cite verifiable sources | Receipt witnesses; refuse `llm_text` | Aligns with ICD receipt |
| **Context window efficiency** | Used tokens / relevant tokens (10k pull for 5 lines = noisy) | Retrieval policy; Spec `spec_lookup` vs dump-all | Design pressure |
| **Retrieval recall (first hit)** | Exact file found on first attempt vs follow-up search | Resolve / search plant | Needs plant |
| **Grounding gap (CREATE)** | `(AI claims) − (verifiable source-code citations)` → target **≈ 0** | Proof-or-Stop Admissible + claim anchors; “guessing” = fail closed | **Embody intent** into Must-spine |

**If** grounding gap is the create metric, **then** a server that answers or
writes docs without a 1:1 map to current repo state is **not** a research/doc
tool — it is guessing `[Evidenced — stakeholder]`. That sentence is already the
port’s receipt / claim-memory fail-mode in different words.

---

## 4. Preferred “stateless” Model Context Protocol stack `[Evidenced — stakeholder]`

### 4.1 Pure-function rule

Given the **same disk state**, a tool always returns the same result. LLM holds
conversation state; server does not.

### 4.2 Proposed tools

| Stack | Tool | Stakeholder contract |
| --- | --- | --- |
| Read (Eyes) | `read_file(path)` | Raw text + current SHA-256 of file |
| Read | `search_code(query)` | Wrap `rg`; lines + snippets |
| Read | `get_structure(depth)` | Directory tree; **hit disk every time** |
| Write (Hands) | `apply_diff(path, diff, expected_hash)` | Apply only if hash matches; else `State Drift Detected` |
| Write | `execute_command(cmd)` | Shell (e.g. `npm test`); stdout/stderr |
| Wiki | `write_wiki_page(title, content)` | Markdown under `/docs` or `/wiki` |
| Wiki | `update_index()` | Scan repo; rewrite `README.md` / `MAP.md` on disk |

### 4.3 Loop

Observe (`get_structure` / `read_file`) → capture hash → plan unified diff →
`apply_diff` with `expected_hash` → on drift, re-read.

### 4.4 “Real-time without a database”

- No in-memory file-tree cache; every structure/search is JIT disk.  
- Optional `.mcp_state` file in-repo for agent work-set (git-versioned).  
- Thesis: server is a thin disposable OS wrapper; delete/reinstall loses nothing
  that is not already on disk.

### 4.5 Goal → tool mapping (stakeholder)

| Goal | Path |
| --- | --- |
| Code for me | `apply_diff` + hash guard |
| Answer questions | `rg` → `read_file` → LLM synthesize |
| Create docs | read code → Markdown → `write_wiki_page` |
| Real-time | no internal server session store |

---

## 5. Adversarial adjudication (principal-SE)

### 5.1 What already aligns (Embody / true Adopt)

| Stakeholder claim | Port / industry SoT | Verdict |
| --- | --- | --- |
| Protocol should be session-free | Model Context Protocol **`2026-07-28`** pin (ADR-0011); SEP-2567/2575 | **true Adopt** of *wire* — already decided `[Evidenced — MCP blog 2026-07-28]` |
| “Same disk → same tool result” for **reads** | Deterministic engine + JIT freshness | **Embody** for read/search/structure |
| `expected_hash` / State Drift on write | Handle digests + Proof-or-Stop Fresh / `apply` optimistic concurrency | **Embody pattern** — maps to FREEZE β/ρ + handle bind; **not** a license to replace `verify`/`claim_withdraw` |
| Grounding gap ≈ 0 | Receipt witnesses forbid `llm_text`; claims need anchors; Prefer Unknown | **Embody intent** — this is the create metric for the *verify* spine |
| Stale fragment rate | Claim freshness ⊥ evidence; material digests | **Embody** sensor into D10 / D10b plants |
| Dual users: humans + agents | BOUNDARY already | **Confirmed** fit |

Industry Spec quote (compressed): dropping protocol sessions does **not** force
application statefulness away — mint **handles** and pass them as args
`[Evidenced — MCP blog “Stateless protocol, stateful applications”]`. Stakeholder
“no server memory” is **stricter** than the Spec requires.

### 5.2 Category errors / contradictions (Refuse or demote)

| Finding | Why it bites | Verdict |
| --- | --- | --- |
| **Thin OS MCP ≠ verified-architecture engine** | BOUNDARY one-liner is graph + locks + receipts + claim memory. A seven-tool filesystem/wiki MCP does **not** satisfy that sentence. Collapsing surfaces → open question OQ-02 class fail | **Refuse** replacing Surface A with Eyes/Hands/Wiki |
| **“No cache / no DB” vs index-lag metrics** | Index lag, embeddings update, event queue throughput, symbol coverage of *generated* docs all require a **derived index or doc store**. Pure JIT `rg` cannot measure those 90-day metrics | **Contradiction** — pick: (A) JIT-only read MCP **or** (B) derived index with Fresh/lag sensors. Not both as one slogan |
| **`execute_command` as first-class Model Context Protocol tool** | Unrestricted shell is not a pure function over disk in the *effect* sense; STEAD ST-5 / harness “model proposes, kernel decides”; DynamicMCPBench minefields | **Refuse** as Wave-1 Must; Could behind allowlist + receipt ρ later |
| **`write_wiki_page` without Fresh/anchors** | Recreates the stakeholder’s own stale-doc pain unless every page binds content digests + secondary validation | **Pilot / Hypothesis** only with doc↔code divergence plant; not free write |
| **`update_index()` rewriting MAP on every call** | Side-effecting “index” without receipt / claim disposition is a second SoR | **Refuse** silent MAP rewrite as verify truth; Spec corpus index = separate surface |
| **`search_code` = `rg` only** | Citation correctness for structure needs ast-grep / SCIP where grammar exists (tip SoT soft-prefer); keyword-only retrieval raises grounding gap | **Adjacent** — allow `rg` for inventory; do not claim structural resolve |
| **`.mcp_state` as global agent work-set** | Hidden coordination file can become a session store by another name | **Hypothesis** — if used, treat as ordinary git artifact with hash binds; not transport session |
| **Gold-standard “delete server, zero data lost”** | True for Eyes/Hands/Wiki-on-disk. **False** for claim memory, receipt history, and any derived registry unless those also live as rebuildable derived artifacts with wipe/rebuild honesty (ICD-REG) | **Demote slogan** — disposable *process*, not disposable *verify artifacts* without rebuild rules |
| **FREEZE** | New Wave-1 tools / Decision Matrices forbidden without override | Stakeholder stack stays **Working hypothesis** — do **not** edit `mcp-tools.md` tool table from this memo alone |

### 5.3 Boundary pressure (open question OQ-01)

Stakeholder product sentence (reconstructed):

> A **local Model Context Protocol server over a brownfield git repository** that
> keeps **answers and generated documentation grounded in current code**
> (grounding gap ≈ 0), with **measurable freshness** when the tree changes.

Current BOUNDARY sentence centers **locks + Dependency Injection graph +
proof-carrying receipts**. These are **compatible goals** only if:

1. Eyes/Hands remain a **thin presentation / agent FS adapter** (Could), and  
2. Wiki/docs generation is **downstream of** claim/receipt Fresh (Must-intent), and  
3. Derived indexes (if any) are **explicit derived SoR** with lag + stale-fragment
   sensors — not “we have no state because we deleted Redis.”

**If** the human Accepts the stakeholder sentence as the product, **then** amend
BOUNDARY + reopen Architecture Decision Record ADR-0011 Surface A tool list.  
**If** the human keeps graph/locks/receipts as the product, **then** treat
Eyes/Hands/Wiki as **Could / adjacent IDE skills**, not Wave-1 Must.

Until that Accept: open question **OQ-01 remains SPIKE**; `blocks_code: true`.

### 5.4 Bloom (this memo only)

| Level | Evidence |
| --- | --- |
| 1 Remember | Stakeholder who/pain/metrics/tool names; MCP `2026-07-28` blog |
| 2 Understand | Grounding gap ↔ PoS/EA-Graph; JIT vs index-lag contradiction |
| 3 Apply | No crates; pointers to digests + FREEZE deepen rows |
| 4 Analyze | Embody wire + hash-guard; Refuse shell Must + surface collapse |
| 5 Evaluate | Research-depth still FAIL; D0 FAIL; boundary Accept pending |
| 6 Create | **This memo + OQ-01/BOUNDARY pointers only** — not epic codegen |

DeepWiki Ask / llms.txt on competitor FS-MCP servers: **not run this session**
(no DeepWiki Model Context Protocol tool in environment) → `[Unknown]`.

---

## 6. Ordered next (human + agent)

| Who | Action | Exit |
| --- | --- | --- |
| **Human** | Choose BOUNDARY: (A) verify spine primary, FS/wiki Could; or (B) brownfield grounded-doc MCP primary | Sign/amend OQ-01 in `SIGNOFF_LOG.md` |
| **Human** | Resolve JIT-only vs derived-index (metrics need index) | One sentence in BOUNDARY or open question OQ-06 |
| **Agent (FREEZE)** | Keep deepen β/ρ / withdrawal / handles — they serve grounding gap + stale fragments | Digests + Spikes already pointed |
| **Agent** | Do **not** add Eyes/Hands/Wiki to `icd/mcp/*.schema.json` until OQ-01 Accept | FREEZE holds |
| **Later Spike** | Allowlisted command runner with ρ receipt; wiki page schema with `content_digest` + secondary validate | Charter only after boundary Accept |

---

## 7. Bottom line

Stakeholder pain and **grounding gap ≈ 0** are the strongest create signals yet —
they **reinforce** Proof-or-Stop / claim-memory / Fresh, not a soft-pass to ship
a seven-tool OS wrapper.

**Stateless Model Context Protocol wire:** already Adopted.  
**Stateless application = pure disk tools only:** Working hypothesis that
**contradicts** the stakeholder’s own index/embedding/lag metrics unless a
derived index is admitted.  
**Implement:** still **Refuse**.
