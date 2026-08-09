---
segment: 02
title: Foundational vs Agentic SE taxonomy (2026)
branch: wave1-gates-untrusted-tree-hygiene
status: RESEARCH COMPLETE — segment SoT for taxonomy / layers / Embody·Adopt·Refuse
research date: 2026-08-08
claim tiers: Evidenced / Confirmed / Unknown
siblings:
  - docs/research/coverage-quality/01-coverage-oracle-climb-solid.md
  - docs/research/coverage-quality/03-scientific-dimensions-metrics.md
  - docs/research/process/04-implementation-frameworks.md
  - docs/research/process/05-dynamics-neuromorphic.md
related:
  - docs/design/coverage-measure-modes-design-2026-08-08.md
  - docs/agentic-foundational-se-taxonomy-2026-08-08.md
  - claude/research/s-stf-a-spec-kit-runners-adr-2026-08-08.md
  - claude/research/s-stf-b-openspec-deltas-adr-2026-08-08.md
do_not: implement dual-mode; own segment-03 scorecards or segment-04 framework catalog
---

# Segment 02 — Foundational vs Agentic SE taxonomy (2026)

Maps 2026 taxonomy cells onto **spring-boot-doc-agent**: a Python CLI / agentic Spring-doc
pipeline with deterministic gates (coverage measure, size ≤225, complexipy ≤5, mutation
taxonomies, claims checker). Not a K8s microservice farm. Dual-mode climb/oracle remains
**design-only**.

**Claim tiers**

| Tier | Meaning |
| --- | --- |
| `[Evidenced]` | Primary paper, official docs, or verified repo page supports the claim |
| `[Confirmed]` | Local seams in this repo agree (file/ADR/gate exists and matches) |
| `[Unknown]` | ID/source missing, label conflation, hype, or product choice still open |

**Out of scope for this segment:** four scientific-dimension scorecards → sibling **03**;
industry framework catalog (DDD/hexagonal/Backstage/…) → sibling **04**. A broader
principal memo at `docs/agentic-foundational-se-taxonomy-2026-08-08.md` may overlap; **this
file is SoT for taxonomy cells + synthesis layers + Embody/Adopt/Refuse** when merging.

---

## 1. Foundational vs Agentic (working definitions)

| Mode | What it is | What it is not (for this product) |
| --- | --- | --- |
| **Foundational SE** | Specs, contracts, review, reproducible gates, hermetic corpora, single-writer SoT | Standing up µsvc meshes, IDP portals, or “cartography as architecture” |
| **Agentic SE** | LLM/agent loops that plan, edit, and iterate with tool feedback | Ungated self-rewrite of CONSTRAINTS/baselines; LLM self-score as merge gate |

**Synthesis rule for this repo:** Agentic work is allowed only inside a **Foundational
envelope** — persistent artifacts + human review + deterministic Verify. That is the
practical reading of Spec-Driven Development process taxonomies (arXiv:2606.04967) and of
issue-resolution surveys that bind acceptance to validation/selection phases
(arXiv:2512.22256), not to model confidence alone.

---

## 2. Source verification (do not trust prompt tables blindly)

Fetched 2026-08-08 from arXiv abs pages unless noted.

| User label | Claimed ID / handle | What it actually is | Tier |
| --- | --- | --- | --- |
| Spec-Driven Development / OpenSpec | arXiv **2606.04967** | **Exists.** Macedo, *From Prompt to Process: a Process Taxonomy…* (2026). Compares GitHub Spec Kit, OpenSpec, Spec Kitty, BMAD, GSD, Reversa. Six-dimension process taxonomy: specification, context, roles, execution, validation, portability. Thesis: persistent artifacts + contracts + human review beat isolated prompts. | `[Evidenced]` |
| Self-evolving scaffolds | arXiv **2608.03392** | **Exists.** Zhou et al., *Self-Evolving Coding Agents* survey. Object-centered evolution taxonomy; companion Awesome list. Warns on feedback reliability, safety, maintainability, cost, generalization. **Not** a SICA/SIFT/Gödel-Machines primary — those names are not the paper’s title objects. Gödel Machines = classical Schmidhuber; treat SICA/SIFT as `[Unknown]` unless separately cited. | `[Evidenced]` (survey) / `[Unknown]` (SICA/SIFT labels) |
| Issue resolution workflow | arXiv **2512.22256** | **Exists.** Jiang, Lo, Liu, *Agentic Software Issue Resolution…* (242-study survey). Logical phases ≈ repo preprocessing → localization → repair → patch validation → patch selection (not a branded “Analysis→Planning→Coding→Testing→Verification” product pipeline). | `[Evidenced]` |
| Log smell taxonomy | arXiv **2412.09284** | **Exists.** Saarimäki, Shin, Bianculli, *Towards a Taxonomy of Software Log Smells*. Nine smells + facets + tool mapping. | `[Evidenced]` |
| MSR-LM taxonomy | arXiv **2604.00787** | **Exists.** Romero-Arjona et al., *The Rise of Language Models in Mining Software Repositories* (177 papers). LM-in-MSR taxonomy (classification/generation/extraction/detection, …). | `[Evidenced]` |
| System cartography | GitHub Thesirix | **Weak secondary.** Profile README mindmap (microservices, EDA, serverless, CQRS). Not peer-reviewed cartography. Vocabulary checklist only. | `[Confirmed]` exists / `[Evidenced]` as formal SoT = **no** |
| LLM-as-Judge / “crupig” / CoderEval | DeepWiki crupig | **crupig not found.** Closest verified DeepWiki: [langchain-ai/openevals LLM-as-Judge](https://deepwiki.com/langchain-ai/openevals/2.1-llm-as-judge-evaluators). CoderEval is a separate code-eval benchmark lineage; do not conflate with openevals. | `[Unknown]` (crupig) / `[Evidenced]` (openevals pattern) |
| FDE / enterprise RAG | DeepWiki pierpaolo28 | **pierpaolo28 not found** for FDE. Unrelated RAG DeepWiki hits do not establish Forward Deployment Engineering. FDE **does** exist as industry practice (Palantir lineage; 2025–2026 hiring/playbooks; Wikipedia *Forward Deployed Engineer*) — but that DeepWiki page is not a primary cite. | `[Unknown]` (named DeepWiki) / `[Evidenced]` (FDE as industry role, secondary) |
| Local SDD practice | STF ADRs | Spec Kit WorkflowEngine **refused**; OpenSpec-style deltas **accepted** for review remediation. | `[Confirmed]` — `claude/research/s-stf-a-spec-kit-runners-adr-2026-08-08.md`, `…/s-stf-b-openspec-deltas-adr-2026-08-08.md` |

---

## 3. Taxonomy cells → Embody / Adopt / Refuse

**Legend**

| Stance | Meaning |
| --- | --- |
| **Embody** | Already true in product shape or gates |
| **Adopt** | Take next (process / docs / gates) without changing product category |
| **Refuse** | Wrong shape for this product (or ungated form is unsafe) |

| Cell | Synthesis layer | Stance | Mapping to spring-boot-doc-agent |
| --- | --- | --- | --- |
| System cartography (µsvc / EDA / serverless / CQRS) | Strategic / Foundational | **Refuse as product infra**; **Embody analogies** | Ship a **monolithic installable CLI** (`doc_engine`, `stf`), not service meshes. CQRS-like *read* of coverage XML vs *write* of measure is conceptual only (oracle write → gap/climb derived reads). Thesirix mindmap = vocabulary, not architecture target. |
| Spec-Driven Development (Spec Kit / OpenSpec / Spec Kitty) | Probabilistic → Strategic | **Adopt (lightweight)** | arXiv:2606.04967: persistent artifacts, contracts, human review. Fit: one-stream Spec → Implement → Verify against CONTRIBUTING / CONSTRAINTS / design memos. **Do not** install Spec Kit WorkflowEngine as mandatory runtime — already decided in S-STF-A. Prefer OpenSpec-style *deltas* (S-STF-B) over greenfield Spec-Kit install. |
| Self-evolving scaffolds | Probabilistic | **Refuse (ungated)** | arXiv:2608.03392: evolution of memory/skills/tools is research-real and risk-laden. Agents must **not** rewrite CONSTRAINTS, coverage baselines, or `fail_under` without human review + `check_repo_claims` / ratchet discipline. |
| Issue resolution workflow | Probabilistic | **Embody (partial)** | Pipeline agents already Plan-Act against Stage-0 + gates. Adopt explicit Analysis→Plan→Code→Test→Verify **for climb batches**, with Verify = oracle / diff-cover / complexipy / size / claims — **not** LLM self-score. Align phases to Jiang et al.’s validation/selection, not a marketing funnel name. |
| Log smell taxonomy | Deterministic / Quality | **Adopt selectively** | Useful for ops/doc logging hygiene; **not** a coverage-floor substitute. Do not invent parallel “log smell CI” until a real incident seeds a mutator (repo mutation policy). Unlabeled metrics (climb Cover% mistaken for floor) are an adjacent smell class — banner + distinct artifact policy. |
| LLM-as-Judge | Probabilistic | **Refuse as SoT** | Optional advisory for doc prose / qualitative claims (steering `01` / semantic-pipeline-eval skill). **Never** substitute for `fail_under`, complexipy, size, claims, PathCohesion. |
| Forward Deployment / enterprise RAG | Strategic | **Unknown / refuse-as-core** | No verified pierpaolo28 DeepWiki page. Product already does structured Stage-0 + context packets — not an enterprise RAG platform or customer-embedded FDE services org. Optional analogy: human-in-the-loop clarification questions before fourteen-doc emit. |
| MSR-LM taxonomy | Probabilistic / Data | **Embody (partial)** | Stage-0 signal scan + hermetic fixtures ≈ MSR extraction with deterministic backends (ast-grep / CodeQL / filesystem). Keep hermetic corpora; refuse client-dirname corpora (already policy). LM classifiers as SoT for Stage-0 hits = **Refuse**. |

---

## 4. Deterministic vs Probabilistic vs Strategic layers

How this product should *use* taxonomy cells — not a claim that the papers use these three names.

| Layer | Role here | Examples we trust | Failure mode if confused |
| --- | --- | --- | --- |
| **Deterministic** | Hard gates / SoT / SLO-like floor | Oracle Cover% / `fail_under`, complexipy ≤5, LOC ≤225, PathCohesion, `check_repo_claims`, mutation kill, hermetic Stage-0 fixtures | Softening floor with “judge says good enough” |
| **Probabilistic** | Agent feedback / targeting / drafts | Climb scoped Cover%, gap-average inventory, LLM patch proposals, LLM-as-judge advisory, semantic-pipeline-eval | Promoting climb Cover% or judge score to repo floor |
| **Strategic** | Process / sequencing / product shape | One-stream SDD queue, golden-path `doc-engine quality-gates`, human approve before CONSTRAINTS evolution, OpenSpec deltas for remediation | Parallel tip thrash; multi-stream SoT edits; Spec Kit as mandatory runtime |

### 4.1 Oracle vs climb placement (taxonomy implication)

```text
DETERMINISTIC (SoT / SLO)              PROBABILISTIC (feedback)
─────────────────────────              ────────────────────────
mode=oracle full suite                 mode=climb scoped --cov
fail_under / certified floor           Cover% / missing for scope
PathCohesionGuard                      guides next edit batch
CI 3.11 cov cell                       never claims repo floor
coverage.xml (authoritative)           gap-average (derived view)
diff-cover new-code gate               LLM plan / patch proposals
complexipy / size / claims             LLM-as-judge (advisory only)
```

**Agentic maintenance angle** (arXiv:2512.22256): Verification/selection must bind to
deterministic oracles. Climb is the cheap inner-loop sensor; final acceptance remains
whole-repo oracle.

**Quality-health angle** (adjacent to arXiv:2412.09284): Wrong severity/destination of a
signal is a smell. Banner + distinct climb artifact policy mitigate “unlabeled Cover%”
confusion (see coverage-measure design decisions 11, 16).

### 4.2 Foundational envelope for agentic loops

```text
Strategic: Spec (memo/decision) ──► Implement (single stream)
                                      │
                                      ▼
Probabilistic: agent Plan-Act / climb feedback
                                      │
                                      ▼
Deterministic: Verify (oracle + complexipy + size + claims + PathCohesion)
                                      │
                                      ▼
Strategic: archive / update living docs (CONTRIBUTING; session-log only if steering moves)
```

Refuse: multi-stream “implement while spec still open”; agents auto-advancing P-levels
without Verify; ungated self-evolution of ratchets.

---

## 5. Decisions owned by this segment (taxonomy / layers)

These bind agents and design approval. Framework-catalog refuses that are not taxonomy
cells belong primarily to sibling **04**; listed here only where they protect layer
binding.

| # | Decision | Layer |
| --- | --- | --- |
| **17** | Agents treat `mode=oracle` as the only coverage SoT/SLO; `mode=climb` is tool feedback / verification-loop metric only. Climb exit codes ≠ floor proof. | Deterministic vs Probabilistic |
| **19** | No ungated self-evolution: agents must not rewrite CONSTRAINTS, coverage baselines, or `fail_under` without human review + claims/ratchet discipline. | Refuse self-evolving scaffolds |
| **20** | LLM-as-judge is not `fail_under`: probabilistic judges may advise docs/tests; deterministic Cover%/complexipy/size/claims remain hard gates. | Refuse judge-as-SoT |
| **21** | SDD one-stream: Spec → Implement → Verify for each P-item; no parallel tip thrash on SoT files. Prefer OpenSpec-style deltas; refuse Spec Kit WorkflowEngine as runtime (S-STF-A). | Adopt lightweight SDD |

**Cross-links (not owned here):** dual-mode decisions **1–16** live in
`docs/design/coverage-measure-modes-design-2026-08-08.md`. Bounded-context / hexagonal /
framework refuse list (**18**, **22–24**) → sibling **04** (and the broader principal memo
until 04 lands).

---

## 6. Segment verdict

| Question | Answer |
| --- | --- |
| Are the claimed arXiv IDs real for the labeled topics? | **Yes** for 2606.04967, 2608.03392, 2512.22256, 2412.09284, 2604.00787 — all `[Evidenced]` after abs fetch. |
| Are DeepWiki “crupig” / “pierpaolo28” usable SoTs? | **No** — `[Unknown]`; use openevals for judge pattern; treat FDE as industry practice only. |
| What should this product Embody now? | Partial issue-resolution loops; hermetic MSR-like Stage-0; CLI (not mesh) product shape; OpenSpec deltas already accepted. |
| What to Adopt next (process)? | Lightweight one-stream SDD; selective log-smell hygiene; explicit Verify = deterministic gates for climb batches. |
| What to Refuse? | Ungated self-evolution; LLM-judge / climb Cover% as SoT; Spec Kit as mandatory runtime; µsvc/EDA/serverless as product infra; FDE/enterprise RAG as core. |

**Safe to treat this segment as taxonomy SoT for merge?** Yes — after coordinator merges with
siblings 01/03/04/05.  
**Code implementation in this pass?** No.

---

## 7. References (primary anchors)

- Macedo, *From Prompt to Process…*, [arXiv:2606.04967](https://arxiv.org/abs/2606.04967)
- Zhou et al., *Self-Evolving Coding Agents*, [arXiv:2608.03392](https://arxiv.org/abs/2608.03392)
- Jiang, Lo, Liu, *Agentic Software Issue Resolution…*, [arXiv:2512.22256](https://arxiv.org/abs/2512.22256)
- Saarimäki et al., *Towards a Taxonomy of Software Log Smells*, [arXiv:2412.09284](https://arxiv.org/abs/2412.09284)
- Romero-Arjona et al., *The Rise of Language Models in Mining Software Repositories*, [arXiv:2604.00787](https://arxiv.org/abs/2604.00787)
- DeepWiki: [langchain-ai/openevals LLM-as-Judge](https://deepwiki.com/langchain-ai/openevals/2.1-llm-as-judge-evaluators)
- Wikipedia / industry secondary: Forward Deployed Engineer (role practice — not pierpaolo28)
- Local: S-STF-A Spec Kit runners ADR; S-STF-B OpenSpec deltas ADR; CONTRIBUTING gates; coverage-measure design memo decisions 1–16
