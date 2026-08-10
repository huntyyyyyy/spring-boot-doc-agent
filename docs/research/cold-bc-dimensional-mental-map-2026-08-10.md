---
title: Cold BC dimensional mental map — DDD · SOLID · patterns · CLI/a11y · RAG-later
status: ACTIVE principal research — Spec lattice DRAFT; no Implement without Approve
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine → later RAG/agent surface (structure-first SoT)
related:
  - docs/research/cold-bc-domain-subdomain-taxonomy-2026-08-10.md
  - docs/research/cold-product-bc-research-map-2026-08-10.md
  - docs/research/process/38-cli-dx-a11y-dual-sinks-2026-08-10.md
  - docs/research/process/39-polyglot-cli-toolkit-bfs-2026-08-10.md
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
  - docs/research/process/04-implementation-frameworks.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/stage0/d1-query-agent-retrieval-bc-research-2026-08-10.md
  - docs/research/stage0/d2-d3-certification-fact-stores-bc-research-2026-08-10.md
  - docs/research/stage0/d4-d5-d6-static-join-drift-cli-2026-08-10.md
  - docs/research/quality-backlog.md
do_not:
  - implement from this lattice without named Spec Approve
  - treat landing-pad repos as product deps by default
  - promote embeddings / rich / capacity / climb to merge or citation SoT
  - unattended AI merge; skip human review floor
  - invent utils/ grab-bags or single-letter mode flags
human_review_floor: true
invariants: fail_under 98.7 · complexipy ≤5 · LOC ≤225 · no utils/ · policy 16-A · cert never LWW
---

# Cold BC dimensional mental map (principal SE scope)

**Question.** Subdomains are necessary but not sufficient. What **dimensions**
must compose inside each subdomain so the domain ships without gaps, vacuous
greens, or SoT swaps — using modern GitHub/arXiv **landing pads**, scoped with
**DDD · TDD · OCP/DRY/SOLID · GoF patterns**, presented through **heavy but
honest CLI customization** (a11y + DX), while keeping a clean path for
doc-engine as a later **RAG/agent tool** (structure-first citations)?

**Method.** Taxonomy packets + dimensional lattice + CLI DX landing pads
(2026-08-10). Tiers: Evidenced / Confirmed / Unknown. Stars = landing-pad
signal, **not** architecture proof.

---

## 0. One-page verdict

| Stance | Choice |
| --- | --- |
| **Embody** | Cross-cutting lattice (Identity, Honesty, Budget, Isolation, Dual sink, Human floor, Fixture≠campaign, Derived≠LWW); structure-first Stage-0 as citation SoR; `dispatch_tool` library SoR; boolean setpoints; thin OCP presenters over one result object |
| **Adopt** | Ports/adapters + Strategy/Spec/Projection/Envelope; Typer thin grade façade; gh/ruff/clig.dev dual sinks; NO_COLOR / `--plain` / JSON receipt; oasdiff-class sensors; SLSA-/in-toto-*shaped* fields; finite OS×shell **campaign** matrix |
| **Refuse** | Embedding citation SoT; rich/emoji/progress-as-merge-proof; LWW cert; Artifactory OCS as CI SoT; capacity/climb/Recall@K as 98.7; MCP write/codegen; Textual-as-grade SoR; unattended AI merge; utils/; Spec Kit as runtime |

**Composition rule.** A subdomain Spec is incomplete until every cross-cutting
lattice row is marked **own / import / N/A-with-reason**, and every dimension
has: gap risk · DDD concept · SOLID bite · pattern · TDD shape · landing pad ·
RAG-later binding (SoT | sensor | adapter | refuse).

---

## 1. Mental map (how a principal SE scopes this)

```text
                    ┌─────────────────────────────────────────┐
                    │         HUMAN REVIEW FLOOR (SoT)         │
                    │   Spec Approve · operator Path B · merge │
                    └───────────────────┬─────────────────────┘
                                        │
         ┌──────────────────────────────┼──────────────────────────────┐
         ▼                              ▼                              ▼
   D3 Facts/KG                   D4 Static join                   D5 Drift/capacity
   (citation SoR)                (assert engine)                  (sensors)
         │                              │                              │
         └──────────────┬───────────────┴──────────────┬───────────────┘
                        ▼                              ▼
                 D2 Certification                 D1 Query/packet
                 (derived never LWW)              (typed retrieval)
                        │                              │
                        └──────────────┬───────────────┘
                                       ▼
                              D6 Operator CLI + MCP
                         dual sink · a11y · grade façade
                                       │
                                       ▼
                         RAG-later (sensor channel only)
                    rank/embed assist · never citation SoT
```

**Read order for Spec work:** lattice (§2) → domain dimensions (§3) → CLI/a11y
layer (§4) → RAG boundary (§5) → pattern/TDD catalog (§6) → epic tickets (§7).

Detail tables for every subdomain live below; arXiv/repo inventories remain in
[`cold-bc-domain-subdomain-taxonomy-2026-08-10.md`](cold-bc-domain-subdomain-taxonomy-2026-08-10.md)
and domain packets. CLI landing pads:
[`process/38-cli-dx-a11y-dual-sinks-2026-08-10.md`](process/38-cli-dx-a11y-dual-sinks-2026-08-10.md).

---

## 2. Cross-cutting dimension lattice

| Dimension | Gap / vacuity if missing | DDD | SOLID | Patterns | TDD shape | Landing pad | RAG-later |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Identity** | Wrong citations; fingerprint churn | Value object / Aggregate | **L** | Value Object, Spec | Property + hermetic fixture | claim-symbol ADR `[Confirmed]`; SCIP | **SoT**; **refuse** embed-id |
| **Honesty labels** | Vacuous certified; mock-as-live | VO + domain stamp | **I** | Spec, Strategy | Contract | OPA *shape* (~12k★); arXiv 2409.05014 | Labels **SoT**; scores **sensor** |
| **Budget / caps** | Silent truncation; unbounded dumps | Envelope VO | **S** | Builder, Envelope | Property + metamorphic | LLMLingua 2310.05736; Aider RepoMap | **sensor**; **refuse** as Cover% |
| **Isolation boundary** | Confused deputy; write MCP | Anti-corruption + Port | **D** | Port/Adapter, Facade | Contract deny matrix | MCP 2601.17549; FastMCP ~27k★ | Shell **adapter**; **refuse** write |
| **Dual sink** | Pipe-masked exits; unparseable CI | Emit domain service | **O** | Facade, Projection | Contract schema+exit | gh CLI ~46k★; ruff ~49k★; clig.dev | **adapter**; not Cover% SoT |
| **Human review floor** | Unattended AI merge | Approve Aggregate | **S** | Spec, CoR | Refuse-path characterization | 2603.02512; LangGraph HITL *pattern* | Approve **SoT**; **refuse** unattended |
| **Fixture ≠ campaign** | OCS becomes CI SoT | Plant Aggregate | **L** | Strategy, Repository | Hermetic CI + campaign char. | E-OCS0 `[Confirmed]`; CodeQL ~10k★ | Fixture **SoT**; campaign **sensor** |
| **Derived ≠ LWW** | Dual-write cert/climb | Projection over SoR | **O** | Projection (CQRS analogy) | Metamorphic recompute | ESAA 2602.23193; in-toto | Projection **sensor**; **refuse** LWW |

---

## 3. Subdomain dimensions (compose or leave gaps)

*Each subdomain: 5–6 dimensions. Full SOLID/pattern/TDD rows in research packets
when Spec opens; here = principal scope checklist.*

### D1.1 Packets / compaction → domain D1

| Dimension | Vacuity if missing | DDD / SOLID / pattern | Landing pad | RAG-later |
| --- | --- | --- | --- | --- |
| Packet kind registry | Opaque dumps | Aggregate + Spec · **O** · Strategy | A-RAG 2602.03442; CodeGraph ~66k★ | kinds **SoT** |
| Compaction honesty | Silent loss as “complete” | TruncationReport VO · **S** · Envelope | LLMLingua family | **sensor** |
| Nested envelope caps | Section starvation | Composite + Envelope · **I** | tip envelope `[Confirmed]` | **adapter** |
| Structure-first selection | Dump/embed fills gap | FactReader Port · **D** · Strategy | Graph-RAG 2601.08773; tree-sitter | structure **SoT** |
| Fail-closed partial | Empty≡success | Result type · **L** | Logical RAG 2605.27123 | presence **SoT** |
| Provider seam | God builder | Port/Adapter · **D** | `dispatch_tool` `[Confirmed]` | library **SoT** |

### D1.2 MCP isolation

| Dimension | Vacuity if missing | Pattern bite | Landing pad | RAG-later |
| --- | --- | --- | --- | --- |
| Server-derived root | Confused deputy | Anti-corruption · **D** | 2601.17549; S-STF-E | boundary **SoT** |
| Tool ⊆ library | Write/codegen invent | Facade · **I** | FastMCP; MCP python-sdk Defer | MCP **adapter** |
| Stdio hygiene | Protocol corruption | Adapter · **S** | FastMCP stderr doctrine | **adapter** |
| Write/codegen deny | Unattended mutation | Spec deny · **S** | MCP servers (read only) | **refuse** |
| Capability ≠ authz | List-as-authorization | Spec · **I** | 2604.05969 | authz **SoT** |

### D1.3 Rank / freshness

| Dimension | Vacuity if missing | Pattern bite | Landing pad | RAG-later |
| --- | --- | --- | --- | --- |
| Rank as sensor | Similarity = citation | Strategy · **S** | FRESCO 2604.14227; Graphiti ~30k★ | **sensor**; **refuse** SoT |
| Freshness labels | Stale as live | Projection stamp · **O** | Codebase-Memory 2603.27277 | label **SoT** |
| Lexical before embed | Embed-first Stage-0 | Strategy chain · **D** | 2605.27123; Continue | structure **SoT** |
| Recall@K honesty | Sold as Cover% | Spec tag · **I** | synthesis metrics | **sensor**; **refuse** floor |
| Deterministic tie-break | Flaky agent context | Strategy · **L** | tip rank | **adapter** |

### D2.1–D2.3 Certification (compressed)

| Sub | Must-have dimensions | Landing pads | RAG-later |
| --- | --- | --- | --- |
| D2.1 | SoR inventory · full-refresh default · projection hash · disposable cert · verify≠existence | ESAA 2602.23193; DBSP 2203.16684; tip B2.5 | facts **SoT**; cert **sensor** |
| D2.2 | builder/executor id · subject+digest · typed predicates · human floor on signing · mock/live honesty | SLSA 2409.05014; in-toto; Cosign *shape* | fields **SoT**; Cosign merge **refuse**/Defer |
| D2.3 | phase-pure fold · AND of hard gates · vacuous-true refuse · LLM-judge absent · LOC/complexipy | OPA shape; 2511.20313; tip fold | boolean fold **SoT** |

### D3.1–D3.3 Facts / KG (compressed)

| Sub | Must-have dimensions | Landing pads | RAG-later |
| --- | --- | --- | --- |
| D3.1 | Stage-0 citation SoR · zero≠absence · dual-emit · grammar ports · rule↔fixture coverage | ast-grep ~15k★; tree-sitter; rule_coverage | facts **SoT** |
| D3.2 | hash rebuild · incr≡full · PathCohesion refuse · Spike-before-store · partial-scope label | 2308.09660; OpenIVM 2404.16486 | full extract **SoT**; incr **adapter** |
| D3.3 | structure citation default · hybrid sensor-only · typed edges · LLM-KG refuse · identity continuity | 2601.08773; 2509.16112; claim-symbol ADR | structure **SoT**; embed **refuse** citation |

### D4.1–D4.3 Static join (compressed)

| Sub | Must-have dimensions | Landing pads | RAG-later |
| --- | --- | --- | --- |
| D4.1 | backend ports · one assertion consumer · pack versioning · complementary≠competing · closed rule_id | Semgrep ~16k★; CodeQL; QLCoder refuse-as-SoT | packs **SoT**; backends **adapter** |
| D4.2 | join keys · audited OpenAPI · wire≠oracle · oasdiff sensor · human floors · path:line | AutoOAS 2410.23873; oasdiff ~1.3k★ elegant | keys/floors **SoT**; LLM OAS **refuse** |
| D4.3 | plant profile · Artifactory refuse CI SoT · same engine · fingerprint skip honesty · campaign≠Cover% | E-OCS0; PreciseBugCollector 2309.06229 | fixture **SoT**; OCS **sensor** |

### D5.1–D5.3 Drift / capacity (compressed)

| Sub | Must-have dimensions | Landing pads | RAG-later |
| --- | --- | --- | --- |
| D5.1 | drift-as-sensor · break taxonomy · Spec↔impl ports · plant-before-threshold · human floor | oasdiff; 2008.12808; 2311.08175 | **sensor** |
| D5.2 | preflight≠floor · estimator ports · budget coupling · refuse PID green · plant baseline | capacity_preflight; 2308.09660 | **sensor**; **refuse** 98.7 |
| D5.3 | proxy labeling · boolean setpoints · threshold=Spec event · climb path 16-A · refuse LLM-judge floor | Goodhart 1803.04585; synthesis | setpoints **SoT** |

### D6.1–D6.2 Operator CLI (compressed) + heavy DX

| Sub | Must-have dimensions | Landing pads | RAG-later |
| --- | --- | --- | --- |
| D6.1 | stable codes · path:line+hint · exit honesty · dual sink · fail-closed · no megacli | Ruff; Typer ~20k★; pytest; NoFAQ 1608.08219 | codes/exit **SoT** |
| D6.2 | finite matrix · quoting honesty · refuse universal emulator · campaign≠merge · thin CI adapter · Spec to expand cells | GHA; flaky-build 2602.02307; OAS16 | campaign **sensor** |

---

## 4. CLI customization layer (beautiful · accessible · honest)

**Goal.** The CLI is the **principal operator display** for all domains — not a
thin afterthought — while remaining scriptable for agents/RAG later.

### 4.1 Presenter architecture (OCP / DRY)

```text
GradeReport / QueryEnvelope / CertView   ← one immutable result (domain)
        │
        ├── HeadlinePresenter      (L0: PASS/FAIL · exit · next action)
        ├── PlainPresenter         (--plain / NO_COLOR / screen-reader)
        ├── JsonReceiptPresenter   (--json / --receipt PATH)  ← agent/RAG twin
        └── RichTtyPresenter       (optional TTY only; never CI SoT)
```

**Embody:** one engine → many presenters (ruff `full|json|github` pattern
`[Evidenced]`). **Refuse:** rich tables / emoji status / spinner-without-JSONL
as merge proof. Detail: process/38.

### 4.2 Accessibility dimensions

| Axis | Embody | Adopt | Refuse |
| --- | --- | --- | --- |
| Color | `NO_COLOR`; `TERM=dumb` | `FORCE_COLOR`; gh-style accessible palette | Truecolor-only status |
| Motion | No animation in non-TTY | `DOC_ENGINE_SPINNER_DISABLED` | Spinner as sole channel |
| Structure | Semantic lines + JSON | `--plain` kills box-drawing | Box art as only receipt |
| Disclosure | L0 default | `--verbose` L1/L2 | Dump-everything default |
| Exit | Stable taxonomy | Remediation next-commands | Pipe-masked zero |
| LLM copy | — | Optional explain **sensor** | LLM text as gate truth (2409.18661) |

### 4.3 Landing pads (DX)

Typer · Click · Rich (TTY) · prompt_toolkit (interactive doctor only) · httpie
selectivity · **gh** `--json`/`NO_COLOR`/`GH_ACCESSIBLE_*` · clig.dev · Ruff
multi-format · pytest progressive disclosure · Charm bubbletea/lipgloss
(**pattern only**) · simonw/llm plugin envelopes (**Adopt** discipline;
**Refuse** LLM citation). **Refuse** Textual-as-grade; archived vercel/pkg.

arXiv: 2012.10206 (CLI customization) · 2210.11630 / 2409.18661 (error messages)
· 2607.17598 (progressive disclosure for agents) · 2606.03854 (agent-native CLI).

---

## 5. RAG-later boundary (doc-engine as retrieval tool)

When Stage-0 + packet + MCP grow into a RAG-shaped product:

| Layer | Role | Must stay true |
| --- | --- | --- |
| Stage-0 facts + typed edges | **Citation SoT** | Deterministic extract; path:line; zero≠absent |
| `context_packet` / query kinds | **Retrieval surface SoT** | Caps + freshness + truncation honesty |
| Rank / hybrid / embeddings | **Sensor only** | Never cite by nearest-neighbor alone |
| MCP / CLI presenters | **Adapters** | Same library SoR; dual sinks |
| Certification / Cover% / claims | **Orthogonal SoT** | RAG quality ≠ fail_under 98.7 |
| Human review | **Merge SoT** | Agents propose; humans Approve |

**Progressive disclosure maps to RAG** (2607.17598): L0 tool descriptions → L1
packet → L2 full-signal — without smuggling embedding chunks into Evidenced
citations. **CLI-Anything** (2606.03854) supports agent-native CLI over brittle
GUI — reinforces MCP+grade dual surface, not unattended merge.

---

## 6. Pattern & TDD catalog (how we build dimensions)

### 6.1 Creational

| Pattern | Where it bites | DRY/OCP note |
| --- | --- | --- |
| **Builder** | Envelope/packet/cert from SoR only | One construction path; no hand-edit CTOR |
| **Abstract Factory** | Defer store/SDK until Spike | Avoid premature SoR |
| **Factory Method** | Presenter selection by sink/TTY | OCP for new sinks |

### 6.2 Structural

| Pattern | Where it bites |
| --- | --- |
| **Port / Adapter** (hexagonal) | Scanners, MCP transport, shell matrix, Spec/Impl readers |
| **Facade** | Thin `doc-engine grade`; MCP over `dispatch_tool` |
| **Anti-Corruption** | LLM-judge, Artifactory, embeddings, SARIF-as-oracle |
| **Composite / Envelope** | Nested caps; attestation statement shape |
| **Bridge** | Transport-agnostic query core |

### 6.3 Behavioral

| Pattern | Where it bites |
| --- | --- |
| **Strategy** | Rank, backends, plant profiles, presenters |
| **Specification** | Gate predicates, deny lists, join floors, honesty |
| **Template Method** | Fold / drift plant-before-threshold |
| **Projection** | Cert / climb derived views |
| **Chain of Responsibility** | Human review before merge/write |
| **Observer (light)** | Hash-triggered reindex — careful of over-coupling |

### 6.4 TDD shapes (non-vacuous)

| Shape | Use for |
| --- | --- |
| **Hermetic fixture** | SoT extract, join keys, rule_coverage |
| **Contract** | Ports, deny matrix, label enums, exit codes, schemas |
| **Metamorphic** | incr≡full; tighter budget ⇒ labeled subset; recompute≡prior |
| **Property** | Caps; stable rank seed; fingerprint stability |
| **Characterization** | Before threshold rewrite; phase-split fold; shell matrix |
| **Refuse tests** | Embedding-as-citation; vacuous certified; pipe-mask; rich-as-CI |

**DRY:** one result object, many presenters; one assertion engine, many plants;
one identity VO, many consumers. **TDD:** red on honesty lies first.

---

## 7. Spec tickets (dimensional — DRAFT)

*Do not Implement until Approve. Est omitted (agent-time, not calendar).*

| ID | Title | Acceptance (sketch) |
| --- | --- | --- |
| **DIM0** | Lattice coverage checklist in each epic Spec | Every subdomain lists own/import/N/A for §2 rows |
| **Q0-D** | D1.1–D1.3 dimensions locked in E-QUERY0 | Packet kinds, caps, MCP deny, freshness enums Spec’d |
| **C0-D** | D2 dimensions locked in E-CERT0 | SoR→projection inventory; mock/live; vacuous refuse |
| **F0-D** | D3 dimensions in E-FACT0 | Extract SoR; incr≡full; embed refuse path |
| **J0-D** | D4 dimensions in E-CQLJ0 | Join keys; one engine; plant profiles |
| **T4-D** | D5 dimensions in E-TOOL4 | Proxy labels; capacity≠Cover%; plant-before-threshold |
| **OAS-D** | D6 + CLI presenter ports in E-OAS0 | GradeReport; Headline/Plain/Json/RichTty; a11y envs; finite matrix |
| **RAG-B** | RAG-later boundary ADR | SoT/sensor/adapter/refuse table frozen before any embed feature |

---

## 8. Adversarial checklist

- [ ] Any dimension without a **SOLID bite** (vacuous row)? Rewrite or drop.
- [ ] Two **SoT** bindings for one concern? Dual-write — refuse.
- [ ] **Sensor** without refuse-to-floor path? Gap.
- [ ] **Adapter** owning identity/thresholds? Leak — move to domain.
- [ ] CLI beauty without JSON twin / `--plain` / `NO_COLOR`? a11y gap.
- [ ] RAG plan that cites embeddings? Constitution violation.
- [ ] Landing pad treated as must-pin dep without Spike + ≥10k★ bar? Process gap.
- [ ] Spec Approve skipped for “obvious” dimension? Human floor violation.

---

## 9. Exit

This memo is the **principal mental map** for scoping cold BCs dimensionally.
It does **not** Approve Implement. Next: human Approve of epic Specs
(QUERY0 → CERT0 → FACT0 → CQLJ0 → TOOL4 → OAS0) with **DIM0** lattice coverage
checked in each. Sibling SoTs: taxonomy · domain packets · process/37 · process/38 ·
synthesis decisions 1–31.
