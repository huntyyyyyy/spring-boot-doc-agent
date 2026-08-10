# DOMAIN_MAP — product bounded contexts (orientation SoT)

**Audience:** humans and agents in **other chats / days / forks**. Read this before
renaming packages or inventing a new top-level taxonomy.

**Status:** Wave 0 orientation shipped (2026-08-10). Wave 0.5 nest: research domain
`docs/research/modularity/` → **`docs/research/bounded-contexts/`** (ubiquitous language).
**Not** a license for mass `git mv` of `src/`. Physical BC moves follow
[`docs/research/bounded-contexts/24-ddd-repo-structure-landing-gaps-2026.md`](docs/research/bounded-contexts/24-ddd-repo-structure-landing-gaps-2026.md).

**Machine inventory:** [`docs/design/tools_bc_inventory.json`](docs/design/tools_bc_inventory.json)
(CI: every `src/doc_engine/tools/*.py` must appear; orphans fail).

---

## 1. Ubiquitous language (product, not “folders”)

**doc-engine** turns a Spring Boot codebase into a **certified fourteen-view doc set**.

| Phrase | Meaning |
| --- | --- |
| **Stage-0 evidence** | Deterministic scan facts (signals, drift, gap) — no LLM required |
| **Path B / generative** | Optional LLM stages that *author* views from Stage-0 + query packets |
| **Fourteen views** | Fixed product surface (architecture, constraints, …) — not arbitrary markdown |
| **Certification fold** | Derived gate bundle (`certification.json`) over citations / validators |
| **Bounded context** | One cohesive product capability with a one-way dependency edge |
| **Composition root** | Thin CLI / adapter that *wires* BCs — must not own domain rules |
| **SoR vs derived vs sensor** | Oracle boolean / rebuildable fold / advisory-only (policy 16-A) |

One-line product: portable Stage-0 scan + optional generative Path B → fourteen-file
Spring docs with certification gates.

| Layer | Path | May enter customer `pip install` wheel? |
| --- | --- | --- |
| Kernel + product tools | `src/doc_engine/`, `src/stf/` | **Yes** |
| Adapters (Claude / Cursor / GH / MCP) | `adapters/` | Plugin/Action packs — not the wheel guts |
| Meta quality (claims, ratchets, rule coverage) | `scripts/` | **No** |
| Research / design SoT | `docs/research/`, `docs/design/` | No |
| Agent policy bridges | `.cursor/`, `.claude/`, `CLAUDE.md`, `AGENTS.md` | No |

Detail: [`docs/product-architecture.md`](docs/product-architecture.md).

---

## 2. Truth classes (policy 16-A / DDIA)

When touching coverage, certification, or sensors, name the class:

| Class | Meaning | Examples |
| --- | --- | --- |
| **SoR** | Authoritative boolean / oracle | `coverage.xml` (fail_under 98.7), size/claims baselines, Stage-0 facts when dual-emitted |
| **Derived** | Rebuildable fold/view | `certification.json`, climb `coverage.climb.xml`, gap-average, DDIA INDEX |
| **Sensor** | Advisory signal — never floor proof | adequacy, suite timing, stalker ledger, semantic-eval |
| **Product** | Runtime pipeline / CLI | `pipeline/`, `scanning/`, most `tools/` |
| **Meta** | This repo’s self-check | `scripts/ci/check_repo_claims.py`, rule coverage |
| **Adapter** | Generative / host entry | `adapters/claude/skills/`, Action |

**Refuse:** dual-writing climb into oracle `coverage.xml`; treating sensors as merge SoT.

---

## 3. Target bounded contexts (destination — not all folders exist yet)

Nest by **product capability**, not by “layer” or “type of file.” Today’s
`tools/` flat bag is a **staging area** tagged by inventory → future home under the
BC that owns the verb.

| BC | Owns (product verb) | Today’s primary paths |
| --- | --- | --- |
| `scanning` | Extract Stage-0 evidence from the Spring tree | `src/doc_engine/scanning/`, tools → `scanning` |
| `partition_capacity` | Slice the repo into groups that fit context budgets | tools → `partition_capacity` |
| `pipeline` | Run the stage graph and persist artifacts under ACL | `src/doc_engine/pipeline/` |
| `compliance_gates` | Fold citations/validators into certification | tools → `compliance_gates` |
| `query` | Build context packets for generative stages | `src/doc_engine/query/` |
| `ci_sensors` | Measure / climb coverage (product-adjacent) | `src/doc_engine/ci/` |
| `stf` | Semantic tests against the doc set | `src/stf/` |
| `cli` | Thin composition root | `src/doc_engine/cli*.py`, `cli.py` |
| `meta` | Repo claims / ratchets / rule coverage | `scripts/` |
| `adapters` | Host-specific generative + CI entry | `adapters/` |

**Stable invoke:** `python -m doc_engine.tools.<mod>` and `doc-engine …` stay green across
moves (shim/façade) unless a deprecation Spec says otherwise.

---

## 4. Nest / collapse candidates (aggressive — map first, delete only with Spec)

| Candidate | Nest into / action | Why | Real blocker |
| --- | --- | --- | --- |
| Research domain `modularity/` | **`bounded-contexts/`** | Process jargon ≠ product BC language | **Done** (Wave 0.5) |
| **First tools nest:** `semantic_eval_*` | `doc_engine.semantic_eval` + tools shims | Sensor; no G-CYCLE edge | **Done** (E-REPO1-A) |
| `docs_site` (`build_docs_site`) | `doc_engine.docs_site` + shim | Tiny; pruned dead `_find_mkdocs_yml` | **Done** (E-REPO1-A) |
| `doc_tag_utils` | shared vocab (tools) | Mis-tagged as docs_site | `shared_vocab_rehome` later |
| E-MOD2 façades (`capacity_preflight`, `partition_repo`, …) | `partition_capacity` | Already concept-split — **not** retired | Large (~19 mods) |
| Scanning / compliance tools | `scanning` / `compliance_gates` | Sit on pipeline↔scanning edges | **Cycle-break** + ports |
| Dual `skills/` ↔ `adapters/claude/skills/` | Delete root mirror after retire Spec | Adapter SoT; root legacy alias | Equality CI — **not this tip** |
| Thin `scripts/` product aliases | Gone | Already phased | **Done** (STATUS) |
| `scripts/verify_llms_docs.py` | Tombstone | RCE (deleted — refuse revival) | `path_absent` |

**Correction:** Wave 0 stamped every inventory row `stay_until_cycle_break`. That was too blunt.
Cycle-break gates **scan/gate-adjacent** packages and tach layers — not every tools cluster.

**Not phased out:** E-MOD2/E-MOD3 product tools (`capacity_preflight`, `run_manifest`, …). Those were LOC/façade waves, not retirements.

**Do dissolve when the blocker clears** — one BC cluster + shim per tip; big-bang `git mv` is not.

---

## 5. Task order

**Active tip / next / Draft Specs:** always read
[`docs/research/quality-backlog.md`](docs/research/quality-backlog.md) — do not
fork a parallel tip from this map. Wave 0/0.5 orientation and **E-REPO1-A** first
nest are **Done**. Resume cohesion (**E-COH1**) and further nests only as the
backlog Active/Next rows say.

Full possibilities + landing gaps: research packet **21–24** under
`docs/research/bounded-contexts/`.

---

## 6. Scrapped / refused (do not revive as “structure”)

| Item | Why |
| --- | --- |
| `scripts/verify_llms_docs.py` (deleted — refuse revival) | RCE defect — `path_absent` in CI |
| Unary `entity_table_map` as SoR | Replaced by facts ledger direction |
| Packaging mega-PR restart | STATUS: paused complete enough for pilots |
| Layer-first top `domain/application/infra` | Wrong ubiquitous language (E-MOD M4) |
| Multi-package workspace bang | Hostile to one-wheel install until H3 multi-repo Spec |
| ArchAgent / LLM architecture recovery as merge SoT | Sensor only |
| Unattended fleet / Backstage / mesh | Explicit non-goals |
| Folder name “modularity” as research domain | Renamed — process jargon, not product BC language |

---

## 7. How to use this file

1. Open **this map** + backlog Active row (not a second policy essay).
2. If changing `tools/`, update **`docs/design/tools_bc_inventory.json` in the same commit**.
3. Prefer nesting a tool into its BC; one cluster + shim when cycles allow.
4. Do **not** mass-rename for “LLM clarity.”
5. Research look-first: [`docs/research/README.md`](docs/research/README.md).
6. Cursor path lenses for code/CI/research live under `.cursor/rules/` (MDC globs) — this file is the **human BC map**, not a duplicate rule pack.
