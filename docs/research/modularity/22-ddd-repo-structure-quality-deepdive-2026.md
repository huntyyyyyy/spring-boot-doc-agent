---
title: E-REPO0 deep — classify → quality research → modern + unusual layouts
status: DRAFT Spec companion to modularity/21 — pending Approve of REPO1–REPO16
research date: 2026-08-10
research_window: 2024-11-01 → 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI modular monolith (`doc_engine` + `stf`) + meta CI + agent adapters
parent: docs/research/modularity/21-ddd-repository-structure-options-2026.md
related:
  - docs/research/modularity/23-ddd-repo-structure-capability-backcast-2026.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/process/04-implementation-frameworks.md
  - docs/research/modularity/20-tach-dependency-blueprint-2026.md
  - docs/design/ddia-north-star/domains/01-data-flow-and-truth/
  - docs/design/ddia-north-star/domains/05-maintainability-and-change/
  - docs/product-architecture.md
do_not:
  - treat LLM architecture recovery (ArchAgent) as merge SoT
  - adopt polylith-cli / Pants / Hive frameworks as runtime deps under ≥1k★ bar without Spike
  - weaken fail_under 98.7, complexipy ≤5, LOC ≤225, PathCohesion, policy 16-A
  - big-bang filesystem rewrite before PairSmell-style inventory + Spec Approve
spec_gate: DRAFT E-REPO0 companion (2026-08-10) — expands REPO decisions; Approve with 21
gh_sor_bar: "≥1000★ and pushed_at within research_window (prefer Releases/docs); pattern-only below bar"
---

# Deep research: classify → quality → unusual value

**Why this companion exists.** Memo 21 listed six *familiar* layouts and ranked A+F.
That under-scoped the problem: it treated “shallow folders” as a naming/taste issue
instead of a **quality multi-axis** issue, and it under-sampled **unusual** setups that
look wrong at first glance but buy properties this product uniquely needs
(SoR vs derived, agent DX, pipeline DAG, brick assembly of CLI+plugin+Action).

**Method (skill bar):** classify → route through quality research (arXiv + GH primary +
local SoT) → map modern *and* unusual concepts → Embody / Adopt / Refuse / Defer for
*this* CLI — never fashion.

---

## 0. One-page verdict (revised)

| Question | Answer |
| --- | --- |
| What is actually wrong? | Not “too few directory levels.” It is **failed scream test**, **InCol grab-bags**, **shallow modules with wide surfaces**, **product/meta dual-runtime collocation**, and **structure that does not encode SoR vs derived**. `[Confirmed]` + `[Evidenced]` PairSmell / Ousterhout / DDIA |
| Is A+F still right? | **As the default Implement spine — yes**, but incomplete. Add **O (deep packs)**, **N (logical overlay)**, and **selectively G/J/K/H-pattern**. |
| Unusual ideas worth real weight? | **J** SoR/derived/sensor tree · **H-pattern** Polylith brick assembly (CLI / plugin / Action as projects) · **K** stage-DAG folders for pipeline tools · **M** agent-context packs · **I** Hive mini-hexagon per BC |
| What stays refuse? | ArchAgent/LLM recovery as SoT · Pants/Polylith *deps* without Spike (&lt;1k★ or wrong weight) · layer-first top · colocated bang · mesh/Backstage |
| Quality gate before any `git mv`? | **REPO-S3:** PairSmell-style InSep/InCol inventory (import graph + co-change + name clusters) → cut list; then façades; then moves. |

---

## 1. Classification framework (problem is multi-axis)

### 1.1 Axes (route each to a quality SoT)

| Axis | Symptom here | Quality research SoT | Good structure signal |
| --- | --- | --- | --- |
| **Scream / intent** | Root `ls` screams “Python packaging + agent tooling,” not “document Spring repos” | Screaming architecture / VSA primers `[Evidenced]` | Top names = capabilities |
| **Modular relation** | `tools/` collocates scan + cert + partition + docs helpers | PairSmell **InCol** (inapt collocated); TSE’26 follow-on `[Evidenced]` arXiv:2411.01012 / IEEE TSE 2026 | Pairs that co-change stay together; unrelated pairs split |
| **Module depth** | Many small façade-ish files beside 63-sibling bags; wide import surfaces | Ousterhout deep modules `[Evidenced]` | Narrow public surface, deep impl |
| **Truth class** | Oracle, climb, gap, claims, ratchets live as *scripts vs packages* without a truth taxonomy in the tree | DDIA SoR vs derived; policy **16-A** `[Confirmed]` | Physical or logical zones: SoR / derived / sensor |
| **Runtime class** | Customer wheel vs meta CI vs generative adapters share one flat root | product-architecture dual-runtime `[Confirmed]` | Explicit product / meta / policy zones |
| **Change unit** | Feature work jumps `tools/` ↔ `pipeline/` ↔ `tests/doc_engine` filename prefixes | Vertical slice / Bogard VSA `[Evidenced]` | Slice = unit of change |
| **Fitness** | tach only cycles; no interfaces | tach / Packwerk pattern; E-TACH0 `[Confirmed]`/`[Evidenced]` | Declared deps + public expose |
| **Agent context** | Agents must load CLAUDE + adapters + skills + src + scripts to act | Polylith “DX for humans and agents” `[Evidenced]` docs; E-STK context-lean `[Confirmed]` | Packets sized to one BC + its skills/tests |
| **Pipeline identity** | Product *is* a stage graph, but folders are library-shaped | Tilburg-style stage dirs; orun/synix DAG/CAS analogies `[Evidenced]` (pattern) | Stages as first-class folders *or* registry SoR |

### 1.2 Smell inventory (this tip) `[Confirmed]`

| ID | Smell | Evidence | PairSmell lens |
| --- | --- | --- | --- |
| S1 | Root scream fail | 27 mixed top entries; no `document-spring` / `stage0` at root | — |
| S2 | `tools/` InCol | 62 modules; heuristic clusters ≈ scan 18 / partition 28 / gates 10 / misc | **InCol** candidate |
| S3 | Test InSep risk | 208 flat `test_*.py`; cohesion via prefixes only | **InSep** vs production packages |
| S4 | Shallow wide surface | CLI/tools re-export sprawl; deep imports tolerated until tach interfaces | Depth fail |
| S5 | Truth collocation | Oracle floor scripts beside climb sensors; product tools beside meta claims | SoR/derived blur |
| S6 | Dual-runtime blur | `adapters/` + `skills/` + `scripts/` + `src/` peers | Intentional BCs, bad packaging |

**Heuristic tools clusters (not yet PairSmell-rated):** scan_stage0≈18, partition_edges≈28, gates_cert≈10, docs_site≈2, misc≈4. `[Confirmed]` tip measurement — treat as **spike input**, not cut list.

### 1.3 Category errors (expanded)

| Error | Why |
| --- | --- |
| Depth theater | More folders ≠ better MR |
| LLM recovery as Spec | ArchAgent `[Evidenced]` arXiv:2601.13007 = **sensor**; synthesis decision **20** refuses LLM-judge as fail_under; same class for merge architecture |
| Copying Polylith/Pants wholesale | python-polylith ≈**550★** — below this repo’s ≥1k★ implement bar → pattern Spike only |
| Ignoring dual-runtime | “One DDD tree” that mixes wheel + claims + hooks recreates InCol at root |
| Temporal-only split | Stage folders *alone* without BC language recreates Ousterhout temporal decomposition smell |

---

## 2. Quality research routing (primary)

### 2.1 Modular relation quality — PairSmell

| Claim | Tier | Source |
| --- | --- | --- |
| Inapt **separated** pairs (InSep) associate with **~190% more co-changes** than proper separations | `[Evidenced]` | arXiv:2411.01012 |
| Inapt **collocated** pairs (InCol) associate with **~35% fewer co-changes** than proper collocates (entities that should not share a module) | `[Evidenced]` | same |
| Pair characteristics (deps, shared terms, fields) predict smells | `[Evidenced]` | IEEE TSE 2026 follow-on (doi 10.1109/tse.2026.3704291) |

**Embody for this tip:** before mass moves, score candidate cuts with **import edges + shared name tokens + co-change** (lightweight PairSmell), not vibes.  
**Refuse:** treating ArchUnit-style tools as optional theater while ignoring measured MR.

### 2.2 Architecture recovery — ArchAgent

| Claim | Tier | Source |
| --- | --- | --- |
| LLM + static analysis can recover business-aligned views; dependency context lifts F1 | `[Evidenced]` | arXiv:2601.13007 |
| Fit as merge SoT here | **Refuse** | Non-deterministic; conflicts E-CM decision **20** / E-TACH6 (human Approves blueprint) |

**Adopt as Spike sensor only:** draft BC hypotheses for REPO-S3; human + tach Approve.

### 2.3 Depth vs fan-out — Ousterhout

Deep module = simple interface, rich implementation. Shallow = interface ≈ implementation.  
**Adopt:** BC packs expose **narrow façades** (CLI subcommands, `tools` entrypoints, tach `expose`); hide `lib/`/`internal/`.  
**Refuse:** proliferating 1:1 wrapper packages (“classitis” at package scale).

### 2.4 Maintainability / truth — DDIA + local synthesis

| Claim | Tier |
| --- | --- |
| SoR vs derived must not dual-write | `[Confirmed]` north-star domain 01 + policy 16-A |
| Evolvability prefers clear change units | `[Confirmed]` domain 05 |
| Vertical / concept slices; no utils | `[Confirmed]` E-MOD M4; segment 04 |

### 2.5 Modular monolith industry — survey + Hive + Modulith

| Claim | Tier | Source |
| --- | --- | --- |
| Modules with explicit APIs; extract-later optional | `[Evidenced]` | arXiv:2401.11867 |
| Spring Modulith: application modules + encapsulation + verification | `[Evidenced]` | Spring Modulith docs (pattern only) |
| Hive: **one BC = one mini-hexagon** (ports/adapters/domain per module) | `[Evidenced]` | industry pattern write-ups 2025–26 |

### 2.6 Unusual-but-active Python structuring — Polylith

| Claim | Tier | Source |
| --- | --- | --- |
| Workspace = `bases/` + `components/` + `projects/` + `development/`; bricks share; projects assemble deployables | `[Evidenced]` | [python-polylith docs](https://davidvujic.github.io/python-polylith-docs/) |
| Explicit agent DX (“all context in one place”) | `[Evidenced]` | same |
| GitHub ★ | ≈550 — **below ≥1k★ implement bar** | `[Evidenced]` 2026-08-10 |
| Stance | **Pattern Adopt / tool Defer–Refuse as SoR** | matches E-TACH gh bar |

### 2.7 Screaming + VSA

Top-level folders name **what the system does**; framework lives one level down.  
`[Evidenced]` Bogard VSA lineage + modern screaming primers.  
**Local fail:** root screams packaging.

### 2.8 Pipeline / CAS analogies (unusual transfer)

Tilburg Science Hub: `src/<stage>/` + `gen/<stage>/{input,temp,output}`.  
Orun/synix: plan DAG + content-addressed artifacts.  
**Transfer carefully:** this product’s *runtime* already writes `--out-dir` artifacts (good); *source* tree is not stage-shaped (gap). Pattern Adopt for **tools/pipeline layout**, not for inventing a local CAS store.

---

## 3. Catalog: modern + unusual layouts (value-first)

Memo 21 covered **A–F**. Below **G–P** add modern refinements and **unusual** setups. Each answers: *what unique property does this buy that A+F alone does not?*

### G — Screaming capability root (modern)

```
document-spring/          # or keep product/ but rename for scream
  stage0-scan/
  partition-and-capacity/
  certify-and-gates/
  query/
  cli/
meta-quality/
  claims/
  coverage-oracle/
  ratchets/
agent-policy/
  adapters/
docs/
```

| Unique value | `ls` teaches the product in 5 seconds |
| Stance | **Adopt names** into DOMAIN_MAP / eventual root zones; physical rename **Defer** (claims blast) |
| Odd? | Mild — still “just folders,” but scream is the point |

### H — Polylith brick workspace (unusual)

```
bases/
  doc_engine_cli/
  github_action/
  claude_plugin/          # generative base only
components/
  scanning/
  pipeline/
  compliance/
  query/
  stf_graph/
projects/
  doc-engine-wheel/
  marketplace-plugin/
development/              # one venv for all bricks
```

| Unique value | **Same components, three deployables** (wheel / Action / plugin) without library-publish tax; agent sees one development project |
| Stance | **Adopt pattern** (base vs component vs project) · **Defer/Refuse** `polylith-cli` dep (&lt;1k★) · compose with setuptools extras / tach instead |
| Odd? | Yes — looks “not Python src layout.” Value: matches *this* monorepo’s real deployable multiplicity |

### I — Hive: BC = mini-hexagon (unusual nesting)

```
src/doc_engine/scanning/
  domain/
  application/
  ports/
  adapters/          # CodeQL, ast-grep, fs
  tests/             # optional colocation later
```

| Unique value | Extraction-ready BC; ports stay local — aligns E-MOD hexagonal without global `domain/` bag |
| Stance | **Adopt inside BCs that already hurt** (scanning, tools clusters) · **Refuse** as only top-level taxonomy |
| Odd? | Nested hexagons feel heavy; earned when a BC has real ports |

### J — Truth-class tree: SoR / derived / sensor (unusual, product-native)

```
truth/
  sor/                 # coverage.xml writers, size/claims baselines, certification SoR paths
  derived/             # climb XML policy 16-A, gap-average, INDEX/COMPLETENESS builders
  sensors/             # adequacy, suite timing, stalker ledger writers
product/
  pipeline/ scanning/ query/ …
meta/
  scripts/ci/ …
```

| Unique value | **Encodes policy 16-A and DDIA dual-write refusal in the filesystem** — agents cannot “accidentally” put climb next to oracle without crossing a named boundary |
| Stance | **Adopt as logical + CODEOWNERS zones immediately**; physical **Spike (REPO-S4)** |
| Odd? | Very — most repos never name “truth.” Here truth *is* the product quality spine |

### K — Stage-DAG source layout (unusual for libraries; natural for this CLI)

```
stages/
  s0_signals/
  s1_partition/
  s2_capacity/
  s3_generative_ports/   # interfaces only; adapters elsewhere
  s4_gates_cert/
registry/
  stage_specs.py         # build_stage_specs SoT (already conceptual)
```

| Unique value | Structure matches `build_stage_specs()` ubiquitous language; reduces temporal InSep between stage code and docs |
| Stance | **Adopt for dissolving `tools/` partition/scan clusters** · keep registry SoT in code (not YAML WorkflowEngine) |
| Odd? | Feels like a data-science repo; correct because doc-engine *is* a pipeline |

### L — Package-by-volatility / SDP (modern classic)

Stable deep core (`core`, schemas, artifact DTOs) at bottom; volatile adapters (`adapters/`, scanner backends) at edges; deps point inward.

| Unique value | Change blast radius visible; complements tach layers |
| Stance | **Embody** via E-TACH layers (ui/commands/core analogues: cli / bcs / core) |
| Odd? | No — but often skipped when people only redraw BC folders |

### M — Agent-context packs (unusual)

```
packs/
  stage0/
    src/…  tests/…  skills/document-spring-repo/  fixtures/
  certification/
    src/…  tests/…  skills/citation-coverage/
  meta-claims/
    scripts/ci/check_repo_claims.py  tests/support/repo_claims/
```

| Unique value | One pack ≈ one agent session context (E-STK lean); skills stop floating detached from code |
| Stance | **Adopt as overlay/map**; physical colocation **Defer** until E-TEST markers stable |
| Odd? | Breaks “skills live only under adapters.” Value: agent load time + fewer wrong tools |

### N — Logical structure overlay (unusual: *don’t move files*)

Keep filesystem; make **catalog + tach + markers + CODEOWNERS** the architecture SoR (already started with DDIA `catalog.json` and research domain map).

| Unique value | Near-zero churn; enforces intent now; PathCohesion-safe |
| Stance | **Embody/Adopt first wave** (DOMAIN_MAP, BC markers, tach interfaces) |
| Odd? | “Structure without folders” feels fake — but this repo already treats claims predicates and catalogs as SoR |

### O — Deep-module packs (modern refinement of A+F)

```
scanning/
  facade.py              # public entrypoints only (root files)
  lib/                   # all impl; subfolders private by rule
  tach.domain.toml
```

| Unique value | Operationalizes Ousterhout at package scale; fewer, deeper BCs beat many shallow files |
| Stance | **Adopt** with tach `[[interfaces]]` |
| Odd? | Mild — forbids casual deep imports |

### P — Mirror the DDIA north-star domains into product code (unusual)

```
src/doc_engine/
  data_flow_and_truth/     # artifacts, certification views
  encoding_and_evolution/  # schemas
  integrity_and_verification/  # gates, claims hooks product-side
  …
```

| Unique value | Design catalog ↔ code isomorphism; reviewers cite same `id`s |
| Stance | **Spike / likely Refuse as primary** — DDIA domains ≠ Spring-doc ubiquitous language; keep as *citation layer*, not package names |
| Odd? | Extremely — high poetry, weak product language |

---

## 4. Crosswalk: quality property → best unusual lever

| Needed property | Prefer | Avoid |
| --- | --- | --- |
| Agent finds Stage-0 fast | **G** scream names + **M** packs | Deeper `src/doc_engine/tools/` |
| Can’t dual-write climb into oracle | **J** truth zones + policy 16-A | “everything under ci/” |
| Three deployables share logic | **H-pattern** bases/components/projects | Publishing internal libs early |
| Extract scanner backends later | **I** mini-hexagon inside scanning | Global infrastructure package |
| Pipeline literacy | **K** stage folders for tools dissolution | Random verb-named scripts |
| Low move risk | **N** overlay first | Bang D from memo 21 |
| Narrow APIs | **O** deep packs + tach expose | Barrel `__init__` re-exports all |
| Measured cuts | PairSmell inventory (**REPO-S3**) | ArchAgent merge |

---

## 5. Revised ranking for *this* product

### Wave 0 — Spec Approve (no moves)
1. Lock **REPO1–REPO16** (below).  
2. **N** DOMAIN_MAP + truth-class labels on existing paths.  
3. Start **REPO-S3** InCol/InSep inventory on `tools/` + `tests/doc_engine`.

### Wave 1 — Structure that earns gates
4. **O + F + A**: deep BC packs + tach interfaces; dissolve `tools/` using **K** stage language where clusters match stages.  
5. **L** layers in tach (E-TACH1).  
6. **G** capability names in map (and only later root).

### Wave 2 — Unusual value (selective)
7. **J** physical truth zones if overlay proves insufficient (Spike REPO-S4).  
8. **H-pattern** project assembly for wheel vs plugin vs Action (without polylith-cli).  
9. **I** mini-hexagon only in BCs with real ports (scanning).  
10. **M** pack overlays linking skills↔BC.

### Stay off Active tip
- **P** DDIA-named packages as primary.  
- **C/D/E** from memo 21 (workspace bang, colocated bang, layer-first top).  
- ArchAgent / polylith-cli / Pants as merge SoR.

---

## 6. Spec decisions (expand REPO1–REPO8 → REPO16)

| ID | Decision | Stance |
| --- | --- | --- |
| **REPO1–8** | As memo 21 (BC-first; A+F; markers before test moves; …) | keep |
| **REPO9** | Treat structure work as **quality** (MR, depth, truth class), not aesthetics | **Embody** |
| **REPO10** | Require **PairSmell-style inventory** before mass `git mv` (REPO-S3) | **Adopt** |
| **REPO11** | Encode **SoR / derived / sensor** as named zones (logical first; physical Spike) | **Adopt** |
| **REPO12** | Adopt **Polylith pattern** (base/component/project) for deployable multiplicity; refuse polylith-cli as SoR until ≥1k★ *and* Spike | **Adopt pattern / Defer tool** |
| **REPO13** | Prefer **deep packs (O)** over many shallow modules when splitting LOC debt | **Adopt** (align E-COH) |
| **REPO14** | **Hive mini-hexagon** allowed *inside* a BC; refuse as repo-wide top taxonomy | **Adopt scoped** |
| **REPO15** | Stage-DAG (**K**) is a valid dissolution language for `tools/` when clusters match pipeline stages | **Adopt** |
| **REPO16** | LLM architecture recovery = **sensor only**; human + tach Approve blueprint | **Embody refuse-as-SoT** |

---

## 7. Spikes (exit criteria)

| ID | Question | Exit |
| --- | --- | --- |
| **REPO-S3** | Which `tools/` pairs are InCol vs proper collocate (imports + shared tokens + co-change 90d)? | Cut table with Embody/Defer per cluster |
| **REPO-S4** | Does logical truth zoning fail in practice (agents still dual-write paths)? | go/no-go physical **J** |
| **REPO-S5** | Can wheel + Action + plugin be expressed as three “projects” over shared components without polylith-cli? | sketch pyproject/extras + tach map |
| **REPO-S1/S2** | (from 21) root move cost; tools clusters | unchanged |

---

## 8. Adversarial checklist

- [ ] Does “unusual” become novelty theater? — Only keep options with a **named quality property** in §4.  
- [ ] Does J create a fourth parallel SoT beside CONTRIBUTING/claims/tach? — Zones must *point at* existing SoR files, not fork them.  
- [ ] Does K fight BC language? — Stages nest *under* BCs or dissolve into BCs named by stage; no second taxonomy forever.  
- [ ] Does H-pattern force microservices? — **No**; projects are assemble-time, one process fine.  
- [ ] Does PairSmell inventory license infinite analysis? — Time-box S3; unlabeled remains serial (E-TEST).  
- [ ] Does agent-pack colocation violate plugin marketplace packaging? — Keep generative skills under adapter contract; packs are **maps** first.

---

## 9. Epic delta (fresh-chat)

### E-REPO0 Amend
Approve **REPO9–REPO16** with REPO1–8.

### E-REPO1 Implement (revised order)
| ID | Title | Acceptance |
| --- | --- | --- |
| REPO1-0 | DOMAIN_MAP + truth-class labels (N+J logical) | paths classified SoR/derived/sensor/product/meta |
| REPO1-1 | REPO-S3 inventory committed | InCol/InSep table for `tools/` |
| REPO1-2 | First deep pack + tach interface (O+F) | deep import fails CI |
| REPO1-3 | Dissolve one tools cluster via K or BC name | tools top-level count ↓; façade stable |
| REPO1-4 | Markers aligned to same BC/stage names | E-TEST green |

**Invariants:** constitution; one tip; no ArchAgent SoT; no polylith-cli without Spike exit.

---

## 10. Relation to memo 21

| Memo 21 | This companion |
| --- | --- |
| Six familiar options A–F | Adds G–P + quality classification |
| Ranked A+F | Keeps A+F as spine; adds O/N/J/K/H-pattern/I/M |
| REPO1–8 | Adds REPO9–16 + S3–S5 |

Human Approve should treat **21 + 22 + 23** as one Spec packet for E-REPO0.
Capability-backed pros/cons and horizon fits live in memo 23.
