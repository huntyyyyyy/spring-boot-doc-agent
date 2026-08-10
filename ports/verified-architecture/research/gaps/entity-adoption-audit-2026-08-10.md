---
title: Entity adoption audit — papers understood vs genuine GitHub algorithms
status: RESEARCH FAIL (honesty pass)
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
audience: [architect, principal-se, agent]
---

# Entity adoption audit (2026-08-10)

## Verdict (read this first)

Prior June–August readiness work **did not** meet the bar you asked for:

1. Enough **recent papers per entity** with **content understanding** (not title→todo).
2. Mapping each entity to **at least five genuine GitHub repositories** that
   implement the *algorithms*, after filtering star-bait / empty / scrapers.

This memo starts repairing that. It is **not** complete Bloom Create. It is the
honest sensor that Definition of Ready row **D0 = FAIL**.

Anti-bogus filter used (a repo must pass most):

| Check | Pass means |
| --- | --- |
| Identity | Canonical org or widely depended package — not a one-commit rename of a paper title |
| Maintenance | `pushed_at` in 2025–2026 (or explicit long-term support) and not archived |
| Substance | Real source tree + tests or Actions workflows (when API-visible) |
| Algorithm fit | Implements the *named algorithm class*, not “also mentions agents” |
| Reject | Awesome-list scrapers, 0-star profile stubs, unrelated homonyms (for example image-segmentation “EA-Graph”) |

GitHub metadata snapshot: **2026-08-10** via `gh api` `[Evidenced]`.

---

## Entity A — Artifact-anchored verification claim memory

### Paper content (understood)

| Paper | Published | What the algorithm actually does | What it does **not** prove |
| --- | --- | --- | --- |
| *EA-Graph: Artifact-Anchored Verification Memory for Coding Agents under Upstream Drift* (arXiv:2608.04278) | 2026-08-04 | Artifacts as nodes; claims anchored to content digests; evidence strength **independent of** freshness; withdrawal → `unaffected` / `affected` / **`unprovable`** (no guess) | Efficiency; repair quality; transfer beyond synthetic “worlds”; Sonnet contrasts often ceilinged |
| *Proof-or-Stop… Evidence-Gated Lifecycle Control* (arXiv:2607.14890) | 2026-07-16 | Lifecycle advances only on **fresh, source-bound, mechanically checkable** evidence; agent text is claim not state; receipts bind hashes | Semantic program correctness; host-neutral generality beyond evaluated family |
| *Taxonomy-Driven Analysis of Open-Source AI Risk Mitigation Tools* (arXiv:2608.07446) | 2026-08-07 | Maps 21 open-source tools → risk taxonomy; shows tooling skew to ops, weak governance | Does not implement claim memory |

### Genuine GitHub — **algorithm adopters**

| Result | Detail |
| --- | --- |
| **Exact EA-Graph algorithm** | **0 found.** Code search hits are arXiv scrapers or **unrelated** 2019 image-segmentation “EA-Graph”. `[Evidenced]` |
| **Proof-or-Stop named engine** | Paper claims open-source instantiation. Org `Proof-or-Stop` on GitHub contains only `Proof-or-Stop/.github` (0 stars, profile stub). No public engine repository resolvable under that org. `uncfreak1255-code/loopspine` (0 stars) is **not** accepted as genuine without provenance. **Gap.** |
| **Adjacent (digest-bound attestations — related class, not the same algorithm)** | See table below — **Adopt patterns**, do not pretend they *are* EA-Graph |

| Repository | Stars / pushed | Why genuine | Algorithm utilized | Fit |
| --- | --- | --- | --- | --- |
| `in-toto/in-toto` | ~1026 / 2026-08-05 | Official supply-chain project; Actions present | Link steps to materials/products (attestations) | **Adopt** receipt shape ideas |
| `in-toto/attestation` | ~363 / 2026-08-04 | Spec sibling | Attestation vocabulary | **Adopt** |
| `sigstore/cosign` | ~6199 / 2026-08-10 | Sigstore; active | Sign/verify artifacts | **Adopt** signing, not claim withdrawal |
| `slsa-framework/slsa` | ~1907 / 2026-08-09 | Framework home | Provenance levels | **Adopt** freshness/provenance language |
| `sigstore/fulcio` | ~866 / 2026-08-10 | Certificate authority for Sigstore | Identity-bound signing | **Could** |
| `anchore/syft` | ~9374 / 2026-08-10 | SBOM generator; active | Content inventory digests | **Could** plant hashing |

**Genuine gap:** we elevated artifact-anchored claim memory to Must spine **without** five (or even one) field implementations of *that* withdrawal/`unprovable` machine. Adjacent attestation repos are necessary but **not sufficient**. Mark as **Pilot / invent under Spike**, not silent Adopt.

---

## Entity B — Stateful Tool-Enabled Agentic Deployment tool constraints

### Paper content (understood)

| Paper | Published | Algorithm | Limits |
| --- | --- | --- | --- |
| *Formal Verification of Agentic Systems over Operational Data* (arXiv:2608.03609) | 2026-08-04 | Formalises Stateful Tool-Enabled Agentic Deployments; First-Order Computation Tree Logic verify **undecidable**; equivariance under opaque-id rename; **canonical deployment wrapper** (graph-isomorphism-hard to compute) | No claim that wrapper is cheap or shipped; case study not a product library |
| *AgentLTL: Trace-Verification for Procedural Compliance* (arXiv:2607.02599) | 2026-07 | First-Order Linear Temporal Logic over typed tool-call traces; online harness block/warn; grounding catches entities not seen in prior tool results | Not opaque-id rename equivariance; paper code fails anti-bogus (anonymous / no Continuous Integration) |
| *CAGE: Certified Authorization under Typed-Return Uncertainty* (arXiv:2607.29190) | 2026-07 | Post-return authorization over binding faults + numerical drift neighborhoods | Complements pre-call equivariance; no product library found |
| *Verified Tool Calls under Non-Atomic Failures* (arXiv:2608.02645) | 2026-08 | Postcondition checks, verify-before-retry, idempotency keys for non-atomic tools | Orthogonal to First-Order Computation Tree Logic; adopt wrapper pattern |

### Genuine GitHub — **algorithm adopters**

| Result | Detail |
| --- | --- |
| **Equivariance wrapper / STEAD checker** | **0 public repos found** implementing the paper’s wrapper or First-Order Computation Tree Logic STEAD verify. Homonym / unrelated tool hosts do not count. |
| **Adjacent (typed tools / structured calls — partial)** | ≥5 genuine repos exist for *schemas and harnesses*, **none** for equivariance |

| Repository | Stars / pushed | Why genuine | Algorithm utilized | Fit |
| --- | --- | --- | --- | --- |
| `modelcontextprotocol/modelcontextprotocol` | ~8916 / 2026-08-10 | Spec org | Tool/resource protocol | **Adopt** wire shape |
| `modelcontextprotocol/python-sdk` | ~23968 / 2026-08-10 | Official SDK; many workflows | Typed server/client tools | **Adopt** ST-1-ish typing |
| `modelcontextprotocol/typescript-sdk` | ~13122 / 2026-08-10 | Official SDK | Same | **Adopt** |
| `openai/openai-agents-python` | ~28542 / 2026-08-10 | Vendor SDK; active | Agent proposes; tools execute | **Adopt** propose/decide split carefully |
| `567-labs/instructor` | ~13712 / 2026-08-09 | Structured outputs; Actions | Schema-constrained model outputs | **Adopt** for args, not equivariance |
| `guardrails-ai/guardrails` | ~7267 / 2026-08-05 | Runtime validators | Output/tool guards | **Could** |
| `NVIDIA-NeMo/Guardrails` | ~6907 / 2026-08-10 | Tool input/output rails | Block unsafe tool calls | **Could** |
| `openai/openai-guardrails-python` | ~227 / 2026-07-21 | Official OpenAI guardrails | Tool/output gates | **Could** |
| `Z3Prover/z3` | ~12542 / 2026-08-10 | Satisfiability Modulo Theories | Monitor/backends | **Could** Spike formal lane |
| `dottxt-ai/outlines` | ~15562 / 2026-08-07 | Constrained generation | Structured decoding | **Could** |
| `pydantic/pydantic` | ~28514 / 2026-08-10 | Validation substrate | Types as gates | **Embody** validation |

**Genuine gap:** ST-1…5 in our Interface Control Document are **design constraints inspired by a paper with no field library**. Treating them as “Adopt from industry” was wrong. Correct tier: **Embody warning + Pilot wrapper Spike**. Reject anonymous AgentLTL / 2★ Agent-C dumps as merge evidence.

---

## Entity C — Graph + architectural locks

### Understanding

Package/layer boundary enforcement: declare allowed dependencies; fail on illegal edges. Classic algorithm is graph reachability / import extraction + policy check — mature, unlike Entities A/B.

Recent papers are thinner here; foundational practice dominates. June–August 2026 agent papers do not replace Packwerk-class checkers.

### Genuine GitHub (≥5) — **pass filter**

| Repository | Stars / pushed | Algorithm | Fit |
| --- | --- | --- | --- |
| `Shopify/packwerk` | ~1901 / 2026-07-27 | Ruby package boundary checker | **Adopt** lock Intermediate Representation ideas |
| `alexevanczuk/packs` | ~97 / 2026-02-24 | Rust reimplementation of Packwerk | **Adopt** / Pilot engine language |
| `sverweij/dependency-cruiser` | ~7052 / 2026-08-10 | JS/TS dependency rules + CI | **Adopt** |
| `TNG/ArchUnit` | ~3794 / 2026-08-10 | Java architecture unit tests | **Adopt** plant patterns |
| `nrwl/nx` | ~29210 / 2026-08-10 | Module boundaries in monorepos | **Adopt** selectively |
| `bazelbuild/bazel` | ~25699 / 2026-08-10 | Visibility / target graph | **Could** (heavy) |
| `tach-org/tach` | ~2.8k / 2026-06 (CI present) | Python modular dependency enforce | **Adopt** Python lane |
| `seddonym/import-linter` | ~1.1k / 2026-08-10 | Import contracts over graph | **Adopt** receipt-oriented peer |
| `fe3dback/go-arch-lint` | ~528 / 2026-08 | Go architecture rules | **Adopt** Go lane |

**Status:** this entity **can** meet the ≥5 genuine-repo bar. Our gap is **lock Intermediate Representation language** (open question 04), not “does the world ship graph locks.”

**Fidelity gaps (do not soft-pass):** Packwerk-class tools often miss method-call edges; Bazel is build visibility not source refs; ArchUnit needs compiled classes; Spring `@Primary` / `@Qualifier` is **not** solved by this layer. `[Evidenced — follow-on from graph-lock research agent]`

---

## Entity D — Source Code Index Protocol / code intelligence

### Understanding

Language tools emit a stable index (formerly Language Server Index Format lineage → Source Code Index Protocol) so cross-language resolve does not depend on one IDE. Algorithm: extract symbols/refs → binary index → consumers query.

### Genuine GitHub (≥5)

| Repository | Stars / pushed | Fit |
| --- | --- | --- |
| `scip-code/scip` | ~721 / 2026-08-10 | **Adopt** index System of Record |
| `scip-code/scip-java` | ~131 / 2026-08-10 | **Adopt** Java lane |
| `sourcegraph/scip-typescript` | ~106 / 2026-08-10 | **Adopt** TypeScript lane |
| `sourcegraph/scip-python` | ~97 / 2026-08-07 | **Adopt** Python lane |
| `microsoft/language-server-protocol` | ~12977 / 2026-08-10 | **Adopt** protocol lineage (interactive — not offline index) |
| `sourcegraph/scip-clang` | ~91 / 2026-08-08 | **Adopt** C/C++ lane when needed |
| `microsoft/lsif-node` | ~198 / 2026-06 | **Refuse** greenfield — Language Server Index Format superseded by Source Code Index Protocol |

**Status:** ≥5 genuine. Gap is **freshness budgets** (open question 06), not missing indexers. Source Code Index Protocol is transmission of facts, **not** architecture policy and **not** Spring Dependency Injection resolve.

---

## Entity E — Contracts / harness (agent proposes, harness decides)

### Papers

| Paper | Understanding |
| --- | --- |
| *From Prompts to Contracts…* (arXiv:2607.08028) | Code-owned checks beat prompt hope; contracts survive model swap |
| *Harnessing Code Agents for Automatic Software Verification* / Aria (arXiv:2607.06341) | Agent + harness; kernel/trust in harness |
| *Delivery, Not Storage: Cue-Anchored Working Memory…* (arXiv:2607.20972) | Working memory as **harness delivery**, not chat storage |

### Genuine GitHub (≥5) — harness / contract-adjacent

| Repository | Stars / pushed | Fit |
| --- | --- | --- |
| `microsoft/agent-framework` | ~12717 / 2026-08-10 | Cited by Proof-or-Stop; orchestration — **Adopt carefully** |
| `langchain-ai/langgraph` | ~39384 / 2026-08-10 | Graph-shaped agent control — **Could** (not our System of Record) |
| `openai/openai-agents-python` | ~28542 / 2026-08-10 | **Adopt** patterns |
| `google/adk-python` | ~21067 / 2026-08-10 | **Could** |
| `stanfordnlp/dspy` | ~37037 / 2026-08-10 | Programmatic pipelines — **Could** |
| `567-labs/instructor` + `guardrails-ai/guardrails` | (above) | **Adopt** contract checks |
| `pydantic/pydantic-ai` | ~19196 / 2026-08-10 | Schema-as-contract agents — **Adopt** patterns |
| `SWE-agent/SWE-agent` | ~20038 / 2026-08-10 | Coding-agent harness — **Could** |
| `OpenHands/OpenHands` | ~83640 / 2026-08-10 | Full coding harness — **Could** (heavy) |
| `openai/codex` | ~105146 / 2026-08-10 | Host hooks/compaction plane — **Could** for cue delivery |

**Gap:** cue-anchored *delivery* as first-class harness property still thinly productized; paper-linked `swapnanil/vectr` fails stars floor (~2★). Official Prompts→Contracts and Aria / Harness Hook Language public engines **Unknown** (not found). Do not Promote mem0 as verify claim store.

---

## Entity F — Model Context Protocol + effect-scored tool benches

### Papers

| Paper | Understanding |
| --- | --- |
| *DynamicMCPBench…* (arXiv:2607.20531) | Trace-grounded, effect-scored tasks over live Model Context Protocol servers |
| *HyperTool…* (arXiv:2606.13663) | Beyond step-wise tool calls; composition — keep primitive schemas first |

### Genuine GitHub (≥5)

| Repository | Stars / pushed | Fit |
| --- | --- | --- |
| `modelcontextprotocol/python-sdk` | ~23968 / 2026-08-10 | **Adopt** official Software Development Kit |
| `modelcontextprotocol/servers` | ~89406 / 2026-08-10 | **Adopt** reference servers (hygiene eyes open) |
| `modelcontextprotocol/typescript-sdk` | ~13122 / 2026-08-10 | **Adopt** |
| `PrefectHQ/fastmcp` | ~27160 / 2026-08-10 | **Adopt** high-adoption server framework |
| `microsoft/mcp` | ~3553 / 2026-08-10 | **Could** |
| `docker/mcp-gateway` | ~1524 / 2026-08-06 | **Could** fleet surface control |
| `SalesforceAIResearch/MCP-Universe` | ~593 / 2026-06-23 | **Adopt** execution-based evaluators (closest open effect/outcome pattern) |
| `mcp-use/mcp-use` | ~10472 / 2026-08-10 | **Could** |

**Gap:** DynamicMCPBench and HyperTool (arXiv) public code **Unknown** / unpublished; reject `toolprint/hypertool-mcp` as name-collision. Our Verification and Validation plan still has no effect-checkpoint harness.

---

## Cross-cutting honesty table

| Must-spine entity | Papers understood? | ≥5 genuine algorithm repos? | Prior corpus claim | Corrected claim |
| --- | --- | --- | --- | --- |
| Graph + locks | Adequate (practice-heavy) | **Yes** | Must | Must **Adopt** field patterns; still need lock Intermediate Representation Accept |
| Artifact-anchored claims | Partial (1 core paper) | **No (0 exact)** | Must Adopt | **Must intent / Pilot invent** — D0 FAIL |
| Stateful Tool-Enabled Agentic Deployment constraints | Partial (1 core paper) | **No (0 exact wrapper)** | Must Adopt | **Embody warning + Spike** — D0 FAIL |
| Freshness-bound receipts | Partial | Adjacent yes; named engine **missing** | Must | Must **shape** from attestations; Proof-or-Stop engine **Unknown** |
| Harness propose/decide | Partial | Yes (adjacent) | Must | Must process; pick one harness pattern via Spike |
| Source Code Index Protocol | Yes | Yes | Assumed | Confirmed Adopt candidates |
| Model Context Protocol tools | Partial | Yes | Draft Interface Control Document | Adopt SDKs; still need typed-id Spike |

---

## Entity G — Architecture Tradeoff Analysis Method + multi-agent drafting

| Paper / method | Understanding |
| --- | --- |
| *Bridging Requirements and Architecture…* (arXiv:2606.01385) | Multi-agent drafting loop (Analyst / Modeler / Designer / Evaluator); emits Architecture Tradeoff Analysis Method-*style* prose — **not** deterministic lock receipts |
| SEI Architecture Tradeoff Analysis Method (Kazman et al.) | Utility tree + Quality Attribute Scenario six-tuple + sensitivity/tradeoff/risk — workshop method |

| Repository | Signal | Fit |
| --- | --- | --- |
| `RuiyinL/MAAD` | ~7 stars; **no runnable agent framework** in tree (artifact dump) | **Refuse** product dependency; schema inspiration only |
| `FoundationAgents/MetaGPT`, `OpenBMB/ChatDev`, large orchestrators | Huge / active | **Refuse** as architecture verify System of Record |
| `architecture-decision-record/architecture-decision-record` | ~16k / active | **Adopt** decision templates beside Quality Attribute Scenarios |
| Pedagogical Architecture Tradeoff Analysis Method sims | Near-zero / teaching | **Refuse** production command-line interface |

**Genuine gap:** no maintained open-source engine that deterministically scores architecture against code the way graph locks do. Drafting agents ≠ verify.

---

## What this means for Definition of Ready

1. Row **D0 FAIL** until each Must entity either (a) lists ≥5 genuine algorithm repos with Embody/Adopt/Refuse, or (b) is explicitly **Pilot/Unknown** with Spike charter — no silent upgrade.
2. **Port Ready P3** (research informing readiness) must be **PARTIAL/FAIL**, not PASS.
3. Elevating July–August papers into Must spine without adoption audit created **false confidence** — your alarm is correct.

## Next research work (not optional)

1. Locate or accept-as-missing Proof-or-Stop public engine; if missing, demote citations to paper-only `[Evidenced abstract]`.
2. DeepWiki Ask + primary docs on Packwerk / SCIP / in-toto for Bloom Apply in *our* ports.
3. Spike charters: claim-store Pilot; equivariance wrap Pilot; receipt freshness keys.
4. Per-entity folders under `research/entities/` with paper digests ≥1 page each (no title-only rows).
