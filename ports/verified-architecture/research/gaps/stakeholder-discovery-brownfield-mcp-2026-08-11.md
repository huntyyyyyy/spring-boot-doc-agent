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

## Plain-language summary (for humans — no jargon chips)

You told us three things that matter:

1. **Who hurts:** engineers on brownfield repos whose docs are stale and whose
   original authors are gone. Agents burn money hunting context.
2. **What “good” looks like in ~90 days:** answers and generated docs stay tied
   to files that still exist; measure how long after a save/pull the search/index
   is current; measure how often retrieved snippets cite dead code; measure
   **grounding gap** (model claims minus citations you can open in the repo) and
   drive that toward zero.
3. **How you want the server built:** session-free Model Context Protocol; tools
   that always answer from today’s disk; edits only if a content hash still
   matches; optional wiki writers; no “memory” inside the server process.

What we already agree with, in plain words:

- The industry Model Context Protocol pin that drops transport sessions is the
  right wire. We already chose that.
- “Do not answer without a citation to current code” is the same intent as our
  freshness-bound receipts and claim memory. That intent stays.
- Hash-checked edits are a sound guard against overwriting someone else’s save.

What we will not silently treat as the product yet:

- Replacing the whole product with only “read file / ripgrep / tree / apply
  diff / run shell / write wiki.” That is a thin filesystem agent adapter. It
  does not by itself evaluate architecture locks or emit proof-carrying receipts.
- Saying “never keep any derived index” while also requiring index-lag and
  embedding-freshness metrics. Those metrics need a derived index (or an honest
  drop of those metrics).
- Shipping unrestricted shell execution or wiki writes that are not tied back to
  current file digests — that recreates stale documentation.

The decision questions in §6 ask you which day-90 job is primary, what “fresh”
means after a pull, what the server may mutate, and which metric fails the
review. Answer those; do not re-litigate slogans.

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

## 6. Human gate — answer these (not A/B slogans)

Each question is closed-choice. Your answer changes **which Wave-1 tools we
Spec**, **which 90-day metrics are Must**, and **what agents are forbidden to
build**. Tautology check: if deleting the option label leaves no difference in
allowed work, the question failed — these do not.

### Q1 — What does a coworker or agent ask this product on day 90?

Pick **one** primary job (secondary jobs can be Could later):

| Choice | Example ask that must succeed | Example ask we may refuse or defer |
| --- | --- | --- |
| **Q1-LOCK** | “Will merging this PR break our layer locks / DI graph? Show the receipt.” | “Write me a wiki page summarizing the billing module.” |
| **Q1-DOC** | “What does the billing module do, with citations to files that still exist at HEAD?” | “Is `controller → repository` allowed under lock set L?” |
| **Q1-BOTH** | Both asks must succeed in the same MVP window | Neither may be “nice to have” |

**If Q1-LOCK:** Eyes/Hands/Wiki stay out of Wave-1 ICD.  
**If Q1-DOC:** graph/LockCheck is not the MVP headline; amend BOUNDARY one-liner.  
**If Q1-BOTH:** say so explicitly — schedule cost rises (two Accept surfaces).

### Q2 — When code changes, what must update before we call the answer “fresh”?

Pick **one**:

| Choice | What must be true after `git pull` / save | What we stop claiming |
| --- | --- | --- |
| **Q2-JIT** | Next `read_file` / `search_code` / `get_structure` sees disk; no background indexer required for MVP | Drop as Must: index lag, embedding freshness, event-queue throughput, symbol-coverage-of-generated-docs |
| **Q2-INDEX** | A derived index/doc inventory updates; we measure lag (commit/save → index ready) and stale-fragment rate | Drop the slogan “no derived state / database is always a liability” |
| **Q2-HYBRID** | Reads may be JIT, but **generated wiki/answers** only ship if bound to digests + a Fresh check (index or content-hash set) | “Wiki write without Fresh” and “pure OS wrapper with no rebuildable derived artifacts” |

### Q3 — Who is allowed to mutate the repo through this Model Context Protocol server?

Pick **one**:

| Choice | Allowed mutations | Forbidden in MVP |
| --- | --- | --- |
| **Q3-READ** | None (answers + maybe write receipts/claims outside target tree, or only under a verify out-dir) | `apply_diff`, `execute_command`, `write_wiki_page` as agent tools |
| **Q3-HASHED** | `apply_diff` only with matching `expected_hash`; wiki pages only with content digest + secondary validate | Open `execute_command`; free wiki rewrite of MAP as truth |
| **Q3-SHELL** | Hash-guarded edits **and** an allowlisted command runner that records ρ (cmd/args/cwd/exit/output digest) | Unrestricted shell; commands without receipts |

### Q4 — What is the create metric we will fail a release on?

Pick **one primary** (others can be sensors):

| Choice | Fail the 90-day review if… |
| --- | --- |
| **Q4-GAP** | Mean grounding gap (AI claims − verifiable code citations) is not near zero on a fixed question set |
| **Q4-STALE** | Stale fragment rate on retrieved chunks exceeds an agreed threshold after pulls |
| **Q4-LOCK** | LockCheck false-green / false-red on the plant suite exceeds threshold |
| **Q4-LAG** | Index lag p95 after large pull exceeds agreed seconds |

You already named **grounding gap** as the create metric — confirm **Q4-GAP** or override.

### How to answer

Reply with four tokens, e.g. `Q1-DOC Q2-HYBRID Q3-HASHED Q4-GAP`, plus any
one-line amend to the BOUNDARY sentence. That is enough to close or redirect
open question OQ-01 in `SIGNOFF_LOG.md`.

### Agent after your answer

| Your pattern | Agent may | Agent must not |
| --- | --- | --- |
| Q1-LOCK + Q2-* | Keep FREEZE deepen on β/ρ / claims / handles | Add Eyes/Hands/Wiki to Wave-1 schemas |
| Q1-DOC + Q2-JIT | Draft a **Could** FS-MCP ICD separate from verify | Claim verify LockCheck is MVP; claim index-lag metrics |
| Q1-DOC + Q2-INDEX/HYBRID | Amend BOUNDARY; Spike derived index + Fresh plants | Ship crates before Definition of Ready |
| Q3-SHELL | Charter allowlist + ρ Spike only | Unrestricted `execute_command` as Adopt |

---

## 7. Bottom line

Stakeholder pain and **grounding gap ≈ 0** reinforce Proof-or-Stop / claim
memory / Fresh — they do **not** auto-Authorize a seven-tool OS wrapper as the
verify product.

**Stateless Model Context Protocol wire:** already Adopted.  
**Application shape:** waiting on Q1–Q4 above.  
**Implement:** still **Refuse**.
