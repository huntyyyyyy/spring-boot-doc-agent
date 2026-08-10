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

These are **genuine** DDD nests or removals. Wave 0.5 ships the **map rename**;
physical collapse still needs cycle-break / equality-gate Spec where noted.

| Candidate | Nest into | Why it can go / nest | Blocker |
| --- | --- | --- | --- |
| Research domain name `modularity/` | **`bounded-contexts/`** | Folder said process, not product meaning | **Done** (this tip) |
| Flat `src/doc_engine/tools/*.py` | Home BC packages per inventory | Tools are verbs of BCs, not a BC | Cycle `pipeline`↔`scanning`; 118 tests on `doc_engine.tools`; keep `-m` shim |
| Dual `skills/` ↔ `adapters/claude/skills/` | Single adapter SoT (+ mirror gate) | Two trees teach the wrong root | Equality CI; retire Spec before delete |
| Layer-shaped tips (`domain/`/`application/`) | Refuse — use BC verbs | Wrong ubiquitous language (E-MOD M4) | Already refuse |
| H3 prep folders (RBAC / multi-repo / HttpLLM) | Nowhere until product Spec | Speculative structure is debt | Explicit product Spec |
| `scripts/verify_llms_docs.py` (deleted — refuse revival) | Tombstone only | RCE — do not revive | `path_absent` |
| Research memos past ~12/domain | Synthesis / archive (DOC1) | Depth theater ≠ DDD | Reshape, do not deepen past 2 levels |

**Do dissolve when the blocker clears** — do not wait for “a big restructure day.”
One BC cluster + shim per tip is the aggressive unit; big-bang `git mv` is not.

---

## 5. Task order (other sessions: do not invent a parallel tip)

1. **Active tip:** E-COH1 cohesion reshape (see [`docs/research/quality-backlog.md`](docs/research/quality-backlog.md)).
2. Wave 0 (map + inventory) — **shipped**; Wave 0.5 (`bounded-contexts/` rename + this map) — **this tip**.
3. Cycle-break `pipeline`↔`scanning` → then E-TACH layers / interfaces.
4. One `tools/` cluster move into its BC + shim — **aggressive unit**, not dissolve-all.
5. H1 product evidence: Stage-4 mid-size measure, live Path B, semantic-eval once.
6. H3 (RBAC / multi-repo / HttpLLM) only after explicit product Spec — **no prep folders**.

Full possibilities + landing gaps: research packet **21–24** under `docs/research/bounded-contexts/`.

---

## 6. Scrapped / refuse (do not revive as “structure”)

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

## 7. How agents should use this file

1. Open **this map** + [`docs/research/quality-backlog.md`](docs/research/quality-backlog.md) Active row.
2. If changing `tools/`, update **`docs/design/tools_bc_inventory.json` in the same commit**.
3. Prefer **nesting a tool into its BC** over adding another top-level noun folder.
4. Do **not** mass-rename for “LLM clarity” — update this map and refuse table; one cluster + shim when cycles allow.
5. Research look-first remains [`docs/research/README.md`](docs/research/README.md) (research domains, not code BCs).
