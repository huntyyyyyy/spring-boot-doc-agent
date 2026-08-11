---
title: Shallow approvals deep-dive — classify, route, implementations, agent-codegen bites
status: RESEARCH PARTIAL
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
routing: docs/research/method/paper-api-schemas.md
mcp_primary: https://blog.modelcontextprotocol.io/posts/2026-07-28/
---

# Shallow approvals deep-dive (2026-08-10)

Entities we previously treated as “drafted enough” without lower-level schemas.
Method: OpenAlex/Semantic Scholar/arXiv **form filters** where useful; **industry
primary** for Model Context Protocol `2026-07-28`; prior entity-adoption audit for
GitHub anti-bogus. Whole words — `GLOSSARY.md`.

**Alarm:** Model Context Protocol **2026-07-28** made the protocol core **stateless**
(Streamable Hypertext Transfer Protocol headers, no session id, `server/discover`).
Our Interface Control Document still reads like a pre-stateless tool list. That is a
genuine requirements gap — not a polish item.

---

## Entity matrix (classify → route → status)

| Entity | Form class | Route used | Exact public algorithm? | Spec depth now | Confidence we understand enough to Implement |
| --- | --- | --- | --- | --- | --- |
| Model Context Protocol transport + tools | Industry specification + systems | Primary blog `2026-07-28` `[Evidenced]`; software development kits Adopt | Spec yes; our Interface Control Document no | **STALE** | **0.35** |
| Freshness-bound receipts | Empirical + systems (Proof-or-Stop); supply-chain adjacent | arXiv 2607.14890; in-toto/Witness | Engine pending; adjacent yes | Draft schema | **0.45** |
| Artifact-anchored claim memory | Empirical (EA-Graph) | Digest 2608.04278; Zenodo only | **0** product repos | Must intent / Pilot | **0.30** |
| Lock Intermediate Representation | Practice / systems | Packwerk / ArchUnit / dep-cruiser | Field yes | **No schema file** | **0.40** |
| Index freshness (Source Code Index Protocol) | Practice / systems | scip-* indexers | Indexers yes | Open question 06 empty | **0.35** |
| Harness propose/decide | Methodological + systems | Contracts / Aria papers; software development kits | Engines Unknown | Slogan only | **0.40** |
| Latency Quality Attribute Scenarios | Methodological (Architecture Tradeoff) | SEI six-tuple | N/A | Spike-blocked measures | **0.25** |
| C4 Context + Container | Methodological | C4 model | N/A | ASCII only | **0.50** (shape) / **0.20** (Accepted diagrams) |

---

## 1. Model Context Protocol — **2026-07-28 stateless** (missing requirements)

### What changed `[Evidenced — official MCP blog 2026-07-28]`

| Change | Model Context Protocol specification enhancement proposal / note | Implication for us |
| --- | --- | --- |
| No `initialize` / `initialized` handshake | Model Context Protocol SEP-2575 | Clients must send protocol version + client info on **every** request (`_meta`) |
| No `Mcp-Session-Id` | Model Context Protocol SEP-2567 | No sticky sessions; any instance may serve any call |
| Required headers on Streamable HTTP | Model Context Protocol SEP-2243 | `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name`; reject header/body mismatch |
| Optional `server/discover` | replaces handshake capability dump | Explicit discovery RPC |
| Application state = **explicit handles as tool args** | blog guidance | Aligns with typed `snapshot_id` / `lock_set_id` — **not** hidden transport session |
| List cache hints `ttlMs` / `cacheScope` | Model Context Protocol SEP-2549 | Tool catalog caching requirements |
| Multi Round-Trip Requests | Model Context Protocol SEP-2322 | Mid-tool elicitations without held stream |
| Auth hardening | RFC 9207 `iss`, CIMD over DCR | If remote Model Context Protocol ever ships |
| Roots / Sampling / Logging deprecated | Model Context Protocol SEP-2577 | Do not design new features on them |
| Legacy HTTP+SSE deprecated | 12-month window | Prefer Streamable HTTP `2026-07-28` |

Industry validators: Cloudflare Workers day-zero, Google / Microsoft / AWS commentary, FastMCP 4.0, Solo.io engineering notes `[Evidenced — vendor blogs]`.

### Implementations (genuine)

| Repository / artifact | Role | Fit |
| --- | --- | --- |
| `modelcontextprotocol/modelcontextprotocol` | Spec | **Adopt** version pin `2026-07-28` |
| `modelcontextprotocol/python-sdk` / `typescript-sdk` | Tier-1 software development kits updated | **Adopt** |
| `PrefectHQ/fastmcp` | Framework targeting new spec | **Could** |
| Official blog + Model Context Protocol specification enhancement proposal pages | Normative intent | **Embody** |

### Agent-codegen bites (rubber-stamped then fail)

1. Generating servers that still do `initialize` + session cookies — **breaks** under load-balanced `2026-07-28` clients.  
2. Hiding `snapshot_id` in “session middleware” instead of tool args — model cannot thread state; Stateful Tool-Enabled Agentic Deployment/handle story collapses.  
3. Omitting `Mcp-Method` / `Mcp-Name` headers — gateways cannot route; servers must reject mismatch.  
4. Treating `tools/list` as immortal — ignore `ttlMs` → stale tool catalogs in agent prompts.  
5. Free-text entity names in tool JSON Schema — hallucinated ids (ST-1); agents happily invent bean names.  
6. Assuming bidirectional SSE forever — deprecated path.

### Missing requirements (add to Interface Control Document / open questions)

- [ ] Normative protocol version: **`2026-07-28`** (local command-line interface may still speak stdio; remote must speak Streamable HTTP headers).  
- [ ] Tool args that are handles: `snapshot_id`, `lock_set_id`, `claim_id` — **minted by tools**, never invented by the model.  
- [ ] Reject codes: header mismatch; unknown handle; stale material digest; llm witness.  
- [ ] `tools/list` cache policy (`ttlMs` / `cacheScope`) for agent hosts.  
- [ ] Explicit **non-goals**: Roots/Sampling/Logging; protocol-level sessions.  
- [ ] Effect checkpoints per tool (DynamicMCPBench family — code still Unknown).

---

## 2. Freshness-bound receipts

| Classify | Empirical / systems-artifact (Proof-or-Stop); adjacent supply-chain |
| Route | arXiv 2607.14890; in-toto Witness, SLSA verifier |
| Exact engine | **Unknown / pending** (`Proof-or-Stop` org not released) |

### Lower-level fields we under-specified

Draft `receipt.schema.json` has `material_digest` / `policy_digest` but not yet:

- Canonical **tree hash algorithm** (what files? ignore noise?) — Proof-or-Stop β(E): `materialHash`, `headHash`, story/policy/command-set hashes  
- **Receipt identity ρ(E)** on executed steps: `cmd`, `args`, `cwd`, `exit`, `outputDigest`  
- **`step_id` stability** across re-runs (open question 05)  
- Binding of receipt to **protocol version** / tool handle set  
- Tamper classes we claim to reject (Proof-or-Stop lists 18 — we have none enumerated)  
- Mapping to in-toto Statement subject/predicate (even if minimum viable product unsigned)

**Do not** rename Supply-chain Levels for Software Artifacts provenance as Proof-or-Stop — compose them.

### Implementations

`in-toto/witness`, `in-toto/in-toto`, `slsa-framework/slsa-verifier`, `sigstore/cosign` — **Adopt patterns**, Refuse as mandatory merge Source of Truth.

### Agent-codegen bites

1. Agents write `result: "pass"` without recomputing digests.  
2. Embedding “large language model explanation” into `witness` — our schema forbids it; models still try.  
3. Reusing yesterday’s receipt after an edit (stale `material_digest`).  
4. Unstable `step_id` strings → flaky Accept tests and useless audits.

---

## 3. Artifact-anchored claim memory

| Classify | Empirical (synthetic plants) |
| Exact impl | **0** public products; Zenodo study only |
| Verdict | **Pilot / invent** — not industry Adopt |

### Agent-codegen bites

1. Collapsing claims into chat memory / mem0 — paper explicitly fights this.  
2. On digest mismatch, **guessing** a new bean instead of `unprovable`.  
3. Treating evidence strength as freshness.  
4. Skipping withdrawal after file edits because “tests still pass.”

### Missing requirements

Withdrawal API sequencing; rebuild-from-receipts rules; plant fixtures FX-claim-*; Spike exit before Must Implement.

**Paper detail agents flatten:** leaf/sub-path anchors (not file-only); evidence lattice independent of freshness; `unprovable` terminal without destroying last verified artifact; OPS vs ANCH completeness check. Evidence enum in draft schema (`weak|strong`) is **under-specified** vs paper `unknown|partial|proven`.

---

## 4. Lock Intermediate Representation

| Classify | Practice systems (Packwerk primary docs; adjacent ArchUnit / dependency-cruiser / tach / import-linter) |
| Exact Packwerk Intermediate Representation | **2** strong (`Shopify/packwerk`, `alexevanczuk/packs`); polyglot lock class **≥5** |
| Our gap | **No `lock-ir.schema.json`** (open question 04) |

Fidelity limits to bind into every receipt: constant-reference edges only; no method-call / dynamic require / initializer graph; clean todo ≠ isolatable boot. Privacy enforcement removed in Packwerk 3.0 — do not encode as core Intermediate Representation.

### Agent-codegen bites

1. Inventing lock dialects per language in the same monorepo.  
2. Encoding **method-call** edges Packwerk never saw → false red.  
3. Growing `package_todo` forever via agent `update-todo` (debt becomes the green path).  
4. Letting the model rewrite policy System of Record without human Approve.  
5. Stopping at static clean while runtime NameError / initializer edges remain.  
6. Placing files by token similarity to “fix” violations.

### Missing requirements

Language-agnostic JSON Schema (package node, allowed edges, violation kinds, content-stable todo fingerprint); strict vs gradual modes; forbid silent agent `update-todo`; edge-fidelity matrix on receipts; stale-todo garbage-collection gate; adapter mapping rules (open question 04).

---

## 5. Index freshness (Source Code Index Protocol)

| Classify | Practice systems (`scip-code/scip` + language indexers) |
| Exact indexers | scip-java / scip-typescript / scip-python / src-cli **Adopt** |
| Industry model | Full rebuild + **commit-bound** upload; nearest-upload soft stale is for humans browsing — **Refuse** as Must verify |
| Our gap | Freshness **budgets** Unknown (open question 06) |

### Agent-codegen bites

1. Verify against **stale** `index.scip` while sources changed.  
2. Mixing indexer versions across languages → ghost symbols.  
3. Claiming Spring Dependency Injection resolve from Source Code Index Protocol alone (stereotype Unknown).  
4. Treating nearest-commit / search fallback as precise resolve.  
5. Assuming fine-grained incremental invalidation exists (practice is full reindex).

### Missing requirements

Budget fields: `tree_sha`, `index_sha`, `indexer_name`/`version`, `built_at`, `max_commit_distance`, `stale_policy`; reject codes `index_missing` / `index_stale` / `nearest_upload_exceeds_budget` / `search_fallback_forbidden`; Must verify = exact commit index or rebuild; bind `scip_sha` into receipts (mismatch → `unprovable`).

---

## 6. Harness propose / decide

| Classify | Methodological + systems (arXiv:2607.08028 Contracts; 2607.20972 Delivery) |
| Exact engines | Prompts→Contracts / cue-anchor / Aria public code **0** → Pilot invent |
| Adjacent | openai-agents, instructor, pydantic-ai, SWE-agent, guardrails — **Adopt propose/decide pattern only** |

### Agent-codegen bites

1. “The agent decided verify passed” in the same process that proposes.  
2. Prompt-only “be careful with ids” instead of code-owned schema checks.  
3. Cue/memory products that **store** but do not **deliver** at lifecycle points (~0 voluntary memory ops under compaction).  
4. Bolt-on guardrails that over-refuse or miss composition-boundary checks.  
5. Agent-authored `update-todo` / claim write without harness decision record.

### Missing requirements

Normative propose/decide split; versioned contract artifacts + fault-injection rejects; cue-anchor Intermediate Representation + delivery receipts; compaction/resume re-inject cues (conversation summary ≠ System of Record); effect checkpoints on mutating tools.

---

## 7. Latency Quality Attribute Scenarios

| Classify | Methodological (Architecture Tradeoff six-tuple; Kazman et al.) |
| Exact Architecture Tradeoff Analysis Method latency engines | **0** — Embody method + Spike plant |
| Status | N-01/N-02 drafted; **response measures empty** (`threshold_status != measured`) |

### Agent-codegen bites

1. Agents invent “p95 &lt; 200ms” with no plant.  
2. Optimizing the wrong path (cold index rebuild vs warm resolve).  
3. Making latency Must → forces premature language/runtime choice.  
4. Measuring mean of three hand runs; mixing cold rebuild into warm budget.  
5. large language model-written Architecture Tradeoff prose as latency System of Record.

### Missing requirements

Six-part scenario + `measure_method` + `spike_id` + `threshold_status`; separate budgets (index rebuild vs warm resolve vs lock-check-on-save); Ban Design influence until Spike fills **T**; CI replay of p95 within tolerance — **or** demote latency from Must until Spike exits.

---

## 8. C4 Context + Container

| Status | ASCII topology in Architecture Brief; no `07-system-design/c4/` Accepted set |

### Agent-codegen bites

1. Generating a fifth microservice because the diagram was vague.  
2. Putting Retrieval-Augmented Generation inside the verify container.  
3. Drawing SaaS multi-tenant boxes against the local-command-line interface decision.

### Missing requirements

Accepted Context (users, target repo, engine, optional Model Context Protocol host) + Container (command-line interface, registry SQLite, index files, lock files, Model Context Protocol server process) with **trust boundaries**.

---

## Cross-cutting: what “users accept” that bites AI codegen

| Rubber-stamp | Later failure mode |
| --- | --- |
| Draft JSON Schema without fixtures | Agents fill required fields with nonsense that still validates |
| Must spine without exact adopters | Agents copy paper prose into production APIs |
| Model Context Protocol tool list without transport version | Broken clients after `2026-07-28` |
| “Source Code Index Protocol solves Dependency Injection” | Silent wrong resolves |
| Latency adjectives | Premature optimization / false Definition of Ready green |
| Port Ready = research done | Agents Implement on FAIL Definition of Ready |

---

## Newest industry advancement we under-weighted

**Model Context Protocol specification `2026-07-28` (28 July 2026)** — not an arXiv paper; **normative industry primary**. Stateless core + Streamable HTTP header routing + explicit state handles. Our product remains local-first, but any Model Context Protocol surface **must** gather requirements against this revision or we intentionally ship a legacy dialect with a migration plan.

Also still thin: DynamicMCPBench public code; Proof-or-Stop public engine; EA-Graph product code.

---

## Spec gap IDs (actionable)

| Gap | Entity | Missing | Blocks |
| --- | --- | --- | --- |
| G-R1 | Receipts | β/ρ fields Draft in schema + Decision Matrix; canon ls-tree Spike remains | D10 / open question 05 |
| G-R2 | Receipts | Tamper classes named in matrix; plants not yet executable | Verification and Validation |
| G-E1 | Claim memory | Evidence enum + DISP vs claim disposition + completeness | D10b / Quality Attribute Scenario QAS-N-07 |
| G-E2 | Claim memory | Pilot invent Spike (0 public impls) | Honest Must |
| G-M1 | Model Context Protocol | Per-tool schemas + `snapshot_open` Draft; Accept pending | D7 / D10c |
| G-M2 | Model Context Protocol | FX-Model Context Protocol TaskSpecs Draft; Tier-1 scorer + replay world pending | Implement |
| G-C1 | C4 | Accept Context+Container with minimum viable product subset | D8 |
| G-L1 | Lock Intermediate Representation | `lock-ir.schema.json` Draft + Decision Matrix; adapter map open | open question 04 |
| G-I1 | Index freshness | Budget fields + exact-commit Must policy | open question 06 |
| G-H1 | Harness | Propose/decide Interface Control Document + cue-delivery schema (Pilot) | D7 / Must spine |
| G-Q1 | Latency Quality Attribute Scenarios | Measure schema wired to receipts; Spike **T** or demote | D3 / N-01/N-02 |
