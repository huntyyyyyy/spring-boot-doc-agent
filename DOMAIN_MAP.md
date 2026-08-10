# DOMAIN_MAP — where this monorepo is headed

**Audience:** humans and agents in **other chats / days / forks**. Read this before
renaming packages or inventing a new top-level taxonomy.

**Status:** Wave 0 orientation shipped (2026-08-10). **Not** a license for mass
`git mv`. Physical BC moves follow [`docs/research/modularity/24-ddd-repo-structure-landing-gaps-2026.md`](docs/research/modularity/24-ddd-repo-structure-landing-gaps-2026.md).

**Machine inventory:** [`docs/design/tools_bc_inventory.json`](docs/design/tools_bc_inventory.json)
(CI: every `src/doc_engine/tools/*.py` must appear; orphans fail).

---

## 1. Product in one line

**doc-engine** = portable Stage-0 scan + optional generative Path B that writes a
fixed fourteen-file Spring doc set with `certification.json` gates.

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

| BC | Owns | Today’s primary paths |
| --- | --- | --- |
| `scanning` | Stage-0 signals, scanners, drift, gap_probe | `src/doc_engine/scanning/`, tools tagged `scanning` in inventory |
| `partition_capacity` | Groups, edges, capacity preflight | tools tagged `partition_capacity` |
| `pipeline` | Stage graph, runner, artifacts ACL | `src/doc_engine/pipeline/` |
| `compliance_gates` | Certification fold, citation/gates/validators | tools tagged `compliance_gates` |
| `query` | Context packet / query surface | `src/doc_engine/query/` |
| `ci_sensors` | Coverage measure / climb (product-adjacent) | `src/doc_engine/ci/` |
| `stf` | Semantic test framework | `src/stf/` |
| `cli` | Thin composition root | `src/doc_engine/cli*.py`, `cli.py` |
| `meta` | Repo claims / ratchets / rule coverage | `scripts/` |
| `adapters` | Host-specific generative + CI entry | `adapters/` |

**Stable invoke:** `python -m doc_engine.tools.<mod>` and `doc-engine …` stay green across
moves (shim/façade) unless a deprecation Spec says otherwise.

---

## 4. Task order (other sessions: do not invent a parallel tip)

1. **Active tip:** E-COH1 cohesion reshape (see [`docs/research/quality-backlog.md`](docs/research/quality-backlog.md)).
2. Wave 0 (this map + inventory) — **shipped**.
3. Cycle-break `pipeline`↔`scanning` → then E-TACH layers / interfaces.
4. One `tools/` cluster move + shim — not big-bang dissolve.
5. H1 product evidence: Stage-4 mid-size measure, live Path B, semantic-eval once.
6. H3 (RBAC / multi-repo / HttpLLM) only after explicit product Spec — **no prep folders**.

Full possibilities + landing gaps: research packet **21–24** under `docs/research/modularity/`.

---

## 5. Scrapped / refuse (do not revive as “structure”)

| Item | Why |
| --- | --- |
| `scripts/verify_llms_docs.py` (deleted — refuse revival) | RCE defect — `path_absent` in CI |
| Unary `entity_table_map` as SoR | Replaced by facts ledger direction |
| Packaging mega-PR restart | STATUS: paused complete enough for pilots |
| Layer-first top `domain/application/infra` | Wrong ubiquitous language (E-MOD M4) |
| Multi-package workspace bang | Hostile to one-wheel install until H3 multi-repo Spec |
| ArchAgent / LLM architecture recovery as merge SoT | Sensor only |
| Unattended fleet / Backstage / mesh | Explicit non-goals |

---

## 6. How agents should use this file

1. Open **this map** + [`docs/research/quality-backlog.md`](docs/research/quality-backlog.md) Active row.
2. If changing `tools/`, update **`docs/design/tools_bc_inventory.json` in the same commit**.
3. Do **not** mass-rename for “LLM clarity” — update this map and refuse table instead.
4. Research look-first remains [`docs/research/README.md`](docs/research/README.md) (different map: research domains, not code BCs).
