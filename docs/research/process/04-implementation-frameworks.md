---
segment: 04
title: Implementation frameworks — Embody / Adopt / Refuse
wave: wave1-cov-climb-a
status: RESEARCH COMPLETE — sibling segment for synthesis; no code impl
research date: 2026-08-08
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI / agentic Spring-doc pipeline (doc-engine), not a K8s farm
related:
  - docs/research/archive/_wip-coverage-design-audit.md
  - docs/agentic-foundational-se-taxonomy-2026-08-08.md
  - docs/design/coverage-measure-modes-design-2026-08-08.md
  - docs/design/rust-stack-fit-memo-2026-08-08.md
awaiting_merge:
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
---

# Segment 04 — Implementation frameworks for this product

> Maps industry operationalization patterns onto **this** repo: a Python CLI
> (`doc_engine`, `stf`) with deterministic Stage-0 + quality gates, agentic doc
> stages, and single-writer path cohesion. Not a microservice platform.
> **No dual-mode / measure-mode implementation in this pass.**

**Claim tiers**

| Tier | Meaning |
| --- | --- |
| `[Evidenced]` | Primary paper, official docs, or named GitHub/DeepWiki page verified this session |
| `[Confirmed]` | Local seams / CONTRIBUTING / design memos agree with the claim |
| `[Unknown]` | ID missing, hype, unverified DeepWiki handle, or product choice still open |

**Stance vocabulary:** **Embody** = already true here · **Adopt** = take next (process/docs/gates) · **Refuse** = wrong shape for this product.

Cross-links: dual-mode decisions 1–16 in
[`docs/design/coverage-measure-modes-design-2026-08-08.md`](../design/coverage-measure-modes-design-2026-08-08.md);
taxonomy + decisions 17–24 draft in
[`docs/agentic-foundational-se-taxonomy-2026-08-08.md`](../agentic-foundational-se-taxonomy-2026-08-08.md).
This segment is the **framework SoT for merge**; de-dupe taxonomy §4 when synthesizing.

---

## 1. Source verification (do not trust labels blindly)

| Framework / label | Claimed source | What it actually is | Tier |
| --- | --- | --- | --- |
| Spec-Driven Development (process) | arXiv **2606.04967** | **Exists.** Macedo, *From Prompt to Process…* (2026). Six-dimension taxonomy (specification, context, roles, execution, validation, portability) over GitHub Spec Kit, OpenSpec, Spec Kitty, BMAD, GSD, Reversa. Convergence: persistent artifacts, contracts, human review beat isolated prompts. | `[Evidenced]` |
| GitHub Spec Kit | github/spec-kit | Open-source SDD toolkit (`/speckit.*` commands, constitution). Greenfield-leaning process kit — **not** a runtime dependency of doc-engine. | `[Evidenced]` |
| OpenSpec | Fission-AI/OpenSpec (via 2606.04967 + README lineage) | Lightweight brownfield-first SDD; delta markers (ADDED/MODIFIED/REMOVED) against living specs. Best *process* fit for this brownfield CLI. | `[Evidenced]` (paper + upstream existence) |
| Hexagonal / ports & adapters | Cockburn ports-and-adapters | Classic structural pattern: app core owns ports; adapters bind CLI/pytest/filesystem. | `[Evidenced]` |
| DDD bounded contexts | Evans / Vernon lineage (secondary here) | Strategic decomposition by language/use-case, not by technical layer. | `[Evidenced]` (classic) / mapping `[Confirmed]` |
| DOD / ECS | Mike Acton CppCon 2014; Unity ECS practice | Data layout / SoA for hot homogeneous transforms (games/sim). | `[Evidenced]` |
| Green AI / Green-Ops | arXiv **1907.10597** (Schwartz et al.) | Efficiency as first-class evaluation criterion; report cost/price tag. Carbon-aware *schedulers* are a later ops overlay, not this paper. | `[Evidenced]` (Green AI) / carbon schedulers `[Unknown]` value here |
| IDP / Golden Paths / Backstage | CNCF Backstage + platform-eng practice | Portal + templates + self-service. Golden *path* ≠ must install Backstage. | `[Evidenced]` (ecosystem) |
| GitOps | Argo CD / Flux pull-reconcile | Git as desired-state SoT for **clusters**. Analogy to ratchet/CONSTRAINTS commits only. | `[Evidenced]` |
| Service mesh | Istio/Linkerd class | East-west traffic, mTLS, retries for µsvc. | `[Evidenced]` as industry pattern / **Refuse** for product |
| Multi-agent orchestration | BMAD / Spec Kitty worktrees (via 2606.04967); Kleppmann dual-write | Parallel agents need isolation + single writer; unordered tip thrash = dual-write. | `[Evidenced]` / local cohesion `[Confirmed]` |
| LLM-as-Judge | DeepWiki langchain-ai/openevals | Verified DeepWiki page for judge evaluators; advisory pattern only. | `[Evidenced]` |
| RAG / enterprise FDE | DeepWiki “pierpaolo28” | **Not found** this campaign. Product already has Stage-0 + context packets. | `[Unknown]` (that handle) |
| WASM / Rust hot paths | Rust stack-fit memo | Pick-none default; profile before native. | `[Confirmed]` memo / `[Evidenced]` DeepWiki for consumed Rust CLIs (ast-grep, ruff) |

---

## 2. Master stance table (Embody / Adopt / Refuse)

| Framework | Dimension | Stance | Mapping to this Python CLI |
| --- | --- | --- | --- |
| **DDD bounded contexts** | Structural | **Embody / deepen** | Concept modules: `coverage_measure`, `coverage_path_cohesion`, `coverage_gap_average`, `quality_gates` — **no utils mega-layer**. Oracle vs climb = two *use cases* in one measure BC (shared PathCohesion kernel), not two top-level packages. |
| **Hexagonal / ports & adapters** | Structural | **Adopt for measure modes** | Today: `MeasureRun`, `PathCohesionGuard`, gate checkout. Next (design-only): strategy/protocol for measure modes; pytest-cov argv builder as adapter; CLI thin. Scanner registry already port-like. |
| **Semantic / vertical slicing** | Structural | **Embody** | Prefer `doc_engine.ci.*` vertical features over type-layered `models/` / `services/` / `utils/`. Keep climb/oracle in `ci`, not a new horizontal layer. |
| **DOD / ECS** | Computational | **Refuse** | Fits game/sim SoA hot loops; poor fit for CLI gate orchestration, AST/signal object graphs, and PathCohesion. |
| **WASM / Rust–Zig in-tree hot paths** | Computational | **Refuse by default** | Cross-link Rust memo: consume pinned Rust CLIs (ast-grep, ruff, complexipy); no in-tree PyO3/WASM rewrite unless profiled bottleneck + human approve. |
| **Green-Ops / carbon-aware CI** | Computational | **Optional later** | Cov-only-on-3.11 already cuts matrix waste `[Confirmed]`. Climb scoping = local time/energy accelerator, **not** floor. Carbon schedulers = Adopt-next only if free; never block oracle correctness. |
| **Platform eng / IDP / Backstage / Golden Paths** | Architectural | **Embody without Backstage** | Golden path = documented CLI: `doc-engine coverage-measure`, `quality-gates`, `check_repo_claims`. Refuse standing up Backstage/IDP portal for this repo. |
| **GitOps (Argo / Flux)** | Architectural | **Partial analogy only** | Git is SoT for baselines, ratchets, CONSTRAINTS. We are **not** deploying clusters. Refuse Argo/Flux as product dependency. |
| **Service mesh** | Architectural | **Refuse** | Irrelevant product infra for a Python CLI. Mesh/ECS theater does not buy citation correctness or coverage floors. |
| **SDD / OpenSpec closed loop** | Agentic | **Adopt (process)** | One stream: Spec (memo/decision) → Implement → Verify (oracle + gates). Prefer OpenSpec-style *delta* against living CONTRIBUTING / design memos over mandatory Spec Kit install. |
| **Multi-agent orchestration** | Agentic | **Refuse unordered parallel tip** | MAO only with single-writer worktree + PathCohesion + deterministic verify. Parallel agents editing same SoT = dual-write (Kleppmann). Spec Kitty-style worktree isolation is the *shape* to copy, not BMAD agent-count theater. |
| **RAG-optimized context / semantic index** | Agentic | **Embody partial / careful adopt** | Stage-0 signals + context packets already structure retrieval. Refuse replacing deterministic scans with opaque embedding SoT; optional index as accelerator only. |

---

## 3. Structural frameworks — DDD, Hexagonal, vertical slicing

### 3.1 DDD bounded contexts — Embody / deepen

**Evidence:** Evans/Vernon strategic design (classic); local module naming `[Confirmed]`.

| Already true | Deepen next (design) | Refuse |
| --- | --- | --- |
| Coverage / gates live under `doc_engine.ci` with concept names | Name oracle vs climb as use cases sharing PathCohesion + wipe | Splitting into `oracle/` and `climb/` top-level packages |
| Scanning vs pipeline vs query are separable contexts | Keep anti-corruption at Stage-0 → doc-writer packet boundary | Ubiquitous-language theater without gate semantics |

**Product rule:** Bounded context ≠ microservice. One installable CLI can host several contexts.

### 3.2 Hexagonal ports & adapters — Adopt for measure modes

**Evidence:** Cockburn ports-and-adapters `[Evidenced]`; scanner registry already OCP/port-like `[Confirmed]` (Rust memo / Stage-0).

| Port (conversation) | Adapter candidates | Notes |
| --- | --- | --- |
| Measure strategy | `OracleMeasure` / `ClimbMeasure` (design) | Shared PathCohesion; diverge on argv scope + fail_under policy |
| Coverage report I/O | XML reader / gap-average view | Climb must not promote to oracle SoT (DDIA) |
| Gate checkout | `gate_tools` filesystem | Keep CLI as driving adapter only |

**Refuse:** Hexagonal folder ceremony (`domain/application/infrastructure` trees) that fights vertical modules and size ≤225.

### 3.3 Semantic / vertical slicing — Embody

Prefer feature slices (`ci/coverage_*`, `ci/quality_*`) over horizontal type layers. Vertical slicing keeps change locality for agent edits and PathCohesion.

**Refuse:** Reintroducing `utils.py` catch-alls or a parallel `services/` layer for climb.

---

## 4. Computational frameworks — DOD/ECS, WASM, Green-Ops

### 4.1 DOD / ECS — Refuse (theater)

**Evidence:** Acton CppCon 2014; Unity ECS — SoA / contiguous component streams for hot transforms `[Evidenced]`.

| When DOD pays | Why not here |
| --- | --- |
| Large homogeneous numeric scans, SIMD/GPU, game ticks | Stage-0 is AST/signal/object-graph + subprocess CLIs |
| Cache-friendly batch transforms | Gate orchestration is control-flow + XML policy, not entity ticks |

**Refuse:** Rewriting `Finding` / signal graphs as ECS components “for performance” without a profiled kernel. Aligns with segment-05 SoA refuse (coordinator draft).

### 4.2 WASM / Rust–Zig hot paths — Refuse by default

**Evidence:** [`docs/design/rust-stack-fit-memo-2026-08-08.md`](../design/rust-stack-fit-memo-2026-08-08.md) — pick-none 30 days; wins already via pinned Rust CLIs `[Confirmed]`.

| Embody | Adopt only if | Refuse |
| --- | --- | --- |
| Consume `ast-grep-cli`, `ruff`, `complexipy` | Profiled Stage-0 bottleneck + human approve + seam-bound helper | In-tree WASM of `coverage_measure` / PyO3 by default |

### 4.3 Green-Ops — Optional later; prefer cheap wins first

**Evidence:** Green AI arXiv:1907.10597 — efficiency as criterion, report cost `[Evidenced]`.

| Already green-ish `[Confirmed]` | Adopt-next (cheap) | Refuse |
| --- | --- | --- |
| Cov cell Python 3.11-only | Document climb as energy/time accelerator | Blocking merges on carbon APIs before oracle/climb split |
| Hermetic fixtures over live client corpora | Optional carbon-aware scheduling if free | Treating Green-Ops dashboards as coverage SoT |

---

## 5. Architectural / operational — IDP, GitOps, mesh

### 5.1 IDP / Golden Paths — Embody without Backstage

**Evidence:** Backstage + golden-path practice is real platform engineering `[Evidenced]`. For a single-product CLI repo, the portal is overhead.

| Golden path here `[Confirmed]` | Refuse |
| --- | --- |
| `doc-engine coverage-measure` | Backstage software catalog for this repo |
| `doc-engine quality-gates` | Crossplane / ApplicationSet scaffolding |
| `python scripts/ci/check_repo_claims.py` | Ticket-queue “platform team” for merges |

**Adopt:** CONTRIBUTING Oracle vs Climb table (when dual-mode design approved) so the golden path documents both modes without conflating floors.

### 5.2 GitOps — Analogy only

Git already holds ratchet baselines, CONSTRAINTS, and claims. That is **source-of-truth discipline**, not Argo reconciliation.

| Analogy | Literal GitOps (Refuse) |
| --- | --- |
| Desired gate state lives in git; CI enforces | Flux/Argo controllers as product deps |
| Drift detected by claims checker / CI | Cluster self-heal loops |

### 5.3 Service mesh — Refuse

No east-west traffic plane. Adding Istio/Linkerd vocabulary to a CLI gate stack is **mesh theater** — refuse alongside ECS theater (decision 22 in taxonomy draft).

---

## 6. Agentic frameworks — SDD, multi-agent orchestration, RAG

### 6.1 Spec-Driven Development — Adopt (lightweight process)

**Evidence:** arXiv:2606.04967 process taxonomy; github/spec-kit; OpenSpec brownfield deltas `[Evidenced]`.

**One-stream loop for wave1 / P-items**

1. **Spec** — written decision bullets in design/research memos; human approve.
2. **Implement** — single stream on tip; no parallel SoT forks.
3. **Verify** — deterministic gates (oracle or scoped climb for WIP only) + complexipy + size + claims; remesure oracle before PR.
4. **Archive** — update living CONTRIBUTING / CONSTRAINTS; session-log only if steering assumptions move.

| Prefer | Avoid |
| --- | --- |
| OpenSpec-style deltas vs living docs | Mandatory Spec Kit install as runtime |
| Human review on contracts | Trusting generated specs without verify |
| Worktree isolation when parallelizing *features* | Multi-stream edits to `fail_under` / baselines |

**Refuse:** Multi-stream “implement while spec still open,” or agents auto-advancing P-levels without verify.

### 6.2 Multi-agent orchestration — Refuse unordered tip; allow gated parallelism

**Evidence:** 2606.04967 notes worktree isolation (Spec Kitty); Kleppmann dual-write / DDIA SoR vs derived; local `PathCohesionGuard` `[Confirmed]`.

| Allowed | Refused |
| --- | --- |
| Parallel research segments writing **disjoint** files (this campaign) | Two agents rewriting `coverage_measure.py` on one tip |
| Feature worktrees with PathCohesion + verify before merge | BMAD-scale agent-count theater without gates |
| Climb batches as Plan-Act-Verify with deterministic Verify | LLM self-score as merge gate |

### 6.3 RAG / semantic context — Embody partial

| Already true | Careful adopt | Refuse |
| --- | --- | --- |
| Stage-0 structured signals + context packets | Optional semantic index as *accelerator* | Embedding store as citation / coverage SoT |
| ast-grep structural search mandate | Packet freshness metrics (advisory) | Enterprise RAG platform / unverified FDE DeepWiki as core |

**LLM-as-Judge:** DeepWiki openevals pattern `[Evidenced]` — advisory for doc prose only; **never** substitute for `fail_under`, complexipy, size, claims (align taxonomy decision 20).

---

## 7. Decisions this segment locks for synthesis

Reconcile with taxonomy 17–24; numbers stable for merge:

| # | Decision | Stance |
| --- | --- | --- |
| 18 | Oracle and climb share PathCohesion + wipe; diverge via hexagonal strategies — not ECS, not a second top-level BC package | Embody / Adopt |
| 21 | SDD one-stream Spec → Implement → Verify per P-item | Adopt |
| 22 | Framework refuse list for measure work: **DOD/ECS**, **service mesh**, Backstage-required IDP, GitOps controllers, WASM/Rust hot paths (unless profiled exception) | Refuse |
| 23 | Green-Ops: keep cov-only-3.11; carbon-aware CI optional; prefer climb scoping for local energy/time | Optional / Embody cheap wins |
| — | Golden path = CLI + CONTRIBUTING, not Backstage | Embody |
| — | MAO only with single-writer + PathCohesion + deterministic verify | Refuse unordered |

---

## 8. Verdict for dual-mode / wave1

**Safe to treat frameworks as settled for design approval:** Yes — Embody DDD + vertical slices; Adopt hexagonal strategies + lightweight SDD; **Refuse mesh/ECS/Backstage/GitOps-controller/WASM-default theater**.

**Not this segment’s job:** Implement `MeasureMode` / climb. That waits on synthesis merge + human approve of decisions 1–24 (or explicit subset including 13–17, 19–21, 22).

**Handoff to coordinator:** Merge this file with siblings 01–03 and 05 into `docs/research/se-quality-synthesis-2026-08-08.md`; de-dupe taxonomy memo §4.

---

## 9. References

### arXiv / papers
- Macedo, *From Prompt to Process…*, [arXiv:2606.04967](https://arxiv.org/abs/2606.04967)
- Schwartz et al., *Green AI*, [arXiv:1907.10597](https://arxiv.org/abs/1907.10597)
- Jiang, Lo, Liu, *Agentic Software Issue Resolution…*, [arXiv:2512.22256](https://arxiv.org/abs/2512.22256) (Verify phase binding)
- Zhou et al., *Self-Evolving Coding Agents*, [arXiv:2608.03392](https://arxiv.org/abs/2608.03392) (ungated evolution refuse)

### GitHub / DeepWiki
- [github/spec-kit](https://github.com/github/spec-kit)
- OpenSpec / BMAD / Spec Kitty — via 2606.04967 primary assessment + upstream READMEs
- [DeepWiki: langchain-ai/openevals LLM-as-Judge](https://deepwiki.com/langchain-ai/openevals/2.1-llm-as-judge-evaluators)
- DeepWiki ast-grep / ruff (consumed Rust CLIs) — see Rust stack-fit memo

### Classics / practice
- Alistair Cockburn, ports and adapters (hexagonal architecture)
- Mike Acton, *Data-Oriented Design and C++* (CppCon 2014)
- CNCF Backstage; Argo CD / Flux GitOps (refuse as product deps)
- Kleppmann, dual writes / DDIA Part III (SoR vs derived)
- Local: `MeasureRun`, `PathCohesionGuard`, `quality_gates`, CONTRIBUTING gates `[Confirmed]`
