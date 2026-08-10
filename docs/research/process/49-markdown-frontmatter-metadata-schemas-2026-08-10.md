---
title: E-MD0 — Markdown frontmatter metadata schemas (research → closed CI)
status: IMPLEMENTING — closed schema + CI on tip (corpus C)
date: '2026-08-10'
epic: E-MD0
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
bloom_mcp:
- deepwiki_ask_question
- llms_txt
related:
- docs/research/process/48-complete-toolscape-agent-repo-developer-2026-08-10.md
- docs/research/process/47-cursor-mdc-rules-devex-ai-repos-2026-08-10.md
- docs/research/process/26-agent-context-markdown-bloat-2026.md
- docs/research/README.md
- scripts/ci/check_repo_claims.py
- docs/design/ddia-north-star/_build_catalog.py
- .cursor/skills/principal-se-research-epic/SKILL.md
do_not:
- Force bloom_mcp onto DDIA pages, session-log packs, or root CLAUDE/AGENTS
- Paste GitHub Docs carousels/spotlight/ms.* translation keys
- Grow check_repo_claims.py further — sibling modules only (≤225 LOC)
- Treat stars_as_of / arxiv_verified as merge SoT
- Second Cover% or fuzzy confidence from metadata completeness
sources:
  llms_txt:
  - https://docs.devin.ai/llms.txt
  - https://citation-file-format.github.io/1.2.0/schema.json
  deepwiki_ask:
  - github/docs · frontmatter AJV + gray-matter + pages.ts CI
  - quarto-dev/quarto-cli · scholarly FM + listing auto-fields
  - huggingface/huggingface_hub · RepoCard.validate → /api/validate-yaml enums
  - blacksmithgu/obsidian-dataview · tags/aliases list normalize + file.mtime
  github:
  - https://github.com/github/docs/blob/main/src/frame/lib/frontmatter.ts
  - https://github.com/github/docs/blob/main/src/frame/lib/read-frontmatter.ts
  mcp: https://mcp.deepwiki.com/mcp
last_reviewed: '2026-08-10'
---

# Principal memo: repo-wide markdown metadata (E-MD0)

**Product:** `doc-engine` agent + research SoR — markdown is the primary
look-first surface.  
**Question.** What closed key/value dimensions should every `*.md` kind carry,
which external schemas to Embody/Adopt/Refuse, and which low-level validators
maximize agent *use* of those files (not just compliance theater)?

**Locked scope:** corpus **C** (repo-wide `*.md`) · Active order: research →
design → Implement **before** E-COH1 · #119 already merged.

---

## 0. One-page verdict

| Kind | Embody | Adopt | Refuse |
| --- | --- | --- | --- |
| Research / design epic memos | Closed allowlist + required `title`/`status`/`date`/`claim_tiers`/`related`; Bloom keys when `bloom_gate` set | Typed `sources{}`; `last_reviewed`; `superseded_by`; ≤8 `related` | Free-key FM; space-keys (`claim tiers`) |
| DDIA north-star | Keep catalog required set | `aliases` optional | bloom_mcp mandatory |
| Steering prompts | Existing `status`+`verify:` claims | — | Bloom |
| Session-log packs | Packer-owned / exempt from research schema | Optional `kind: session_log_pack` | Full Bloom bar |
| Root SoT (`CLAUDE`/`AGENTS`/…) | Keep `derived:` HTML blocks as SoT | Thin optional YAML **only if** it helps indexers — default **no** | Duplicate counts in YAML |
| Skills / agents | Keep `name`/`description`/`tools` | Optional `related` | Research Bloom |

**CI pattern to Embody:** GitHub Docs — `additionalProperties: false` + parse →
validate → fail test (`src/frame/tests/pages.ts`) `[Evidenced — DeepWiki
github/docs]`.

---

## 0b. Bloom ladder

| Level | Evidence |
| --- | --- |
| **1 Remember** | GitHub Docs `frontmatter.ts` / `read-frontmatter.ts`; CFF 1.2 schema keys; Quarto listing fields; HF `validate-yaml`; Dataview tags/aliases; in-repo `parse_frontmatter` + DDIA `_build_catalog` |
| **2 Understand** | File *kinds* need different closed worlds; research FM is richer than claims list-parser; root SoT already has `derived:` SoR |
| **3 Apply** | Sibling `scripts/ci/md_frontmatter_*.py` + `check_md_frontmatter.py` wired like claims; `--fix` renames; PyYAML OK (already dep) for nested `sources` |
| **4 Analyze** | Embody Docs closed-schema; Adopt DataCite relationTypes as optional typed related; Refuse HF remote validate API as SoT; Refuse growing 1863-LOC claims file |
| **5 Evaluate** | §6 adversarial — false-green if exempt globs too wide; false-red if Bloom required on every README |
| **6 Create** | MD0-1…MD0-8 tickets below → Design Spec → Implement |

---

## 1. Problem classes (this product)

1. **Open keys** — research memos invent keys; CI never fails unknown ones.  
2. **Naming drift** — `claim tiers` (57) vs `claim_tiers` (14); `research date` vs `date`.  
3. **Unvalidated Bloom** — README rule 6 / skill frontmatter hint; ~3 files carry `bloom_gate`.  
4. **Staleness** — no `last_reviewed` / tip-bound freshness; agents re-read dead memos.  
5. **Parser fragmentation** — three FM parsers (`check_repo_claims`, `check_llms_coverage`, DDIA builder) with different nesting power.  
6. **Corpus C heterogeneity** — one schema cannot fit session-log packs and process/48.

---

## 2. External schemas (low-level, not theory)

### 2.1 GitHub Docs `[Evidenced — DeepWiki + primary]`

- Schema: required `title`,`versions`; **`additionalProperties: false`**.  
- Pipeline: gray-matter parse → AJV `validateJson` → map `instancePath` to
  `property: 'versions.ftp'` → CI test `every page has valid frontmatter`.  
- Deprecated keys stay in schema with `deprecated: true` (translation lag) —
  **Adopt** for our rename window (`claim tiers` allowed only under `--fix`
  warn, then hard-fail).

### 2.2 CITATION.cff 1.2 `[Evidenced — schema.json]`

- Required: `cff-version`, `message`, `title`, `authors`.  
- Useful optional: `doi`, `identifiers`, `keywords`, `license`,
  `repository-code`, `references`, `date-released`, `commit`.  
- Root **`additionalProperties: false`**.  
- **Adopt** closed-world + identifier list shape into `sources.github` /
  `sources.arxiv`; **Refuse** requiring CFF file per memo.

### 2.3 CodeMeta / schema.org `[Evidenced — codemeta terms]`

- `citation`, `relatedLink`, `isPartOf`, `identifier`, `keywords`,
  `dateModified`, `referencePublication`.  
- **Adopt** as conceptual dimensions inside `related` / `sources`; **Refuse**
  mandating `codemeta.json` per markdown file.

### 2.4 Quarto `[Evidenced — DeepWiki quarto-cli]`

- Scholarly: `title`, `author`, `date`, `date-modified`, `citation`,
  `categories`.  
- Listings auto-derive `file-modified`, `word-count`, `reading-time`.  
- **Adopt** `last_reviewed` + generated `_index` (not hand word-counts).  
- **Refuse** `execute:` and Quarto project chrome.

### 2.5 DataCite 4.x `[Evidenced — schema docs]`

- Typed dates (`Created`/`Updated`/`Issued`/…).  
- `relationType` enum: `Cites`, `IsSupplementedBy`, `Obsoletes`, `IsPartOf`, …  
- **Adopt** optional typed related: `{path, relation}` for supersession edges.  
- **Refuse** full DataCite XML/JSON-LD export as tip SoT.

### 2.6 Hugging Face cards `[Evidenced — DeepWiki huggingface_hub]`

- `RepoCard.validate()` → Hub `/api/validate-yaml`; enum-closed `license`,
  `task_categories`, `tags`.  
- **Adopt** *local* enum allowlists (status, kind, bloom_gate).  
- **Refuse** remote Hub validate as CI dependency.

### 2.7 Obsidian / Dataview `[Evidenced — DeepWiki dataview]`

- Plural list keys (`tags`/`aliases`); implicit `file.mtime` / outlinks.  
- **Adopt** list-only multi-values + `aliases` for renames.  
- **Refuse** inline `[key:: value]` as SoT (FM only).

---

## 3. In-repo baseline `[Confirmed]`

| Mechanism | Role |
| --- | --- |
| `check_repo_claims.parse_frontmatter` | Scalar+list; status/`verify:` only for steering |
| DDIA `_build_catalog.py` | Required `id`,`kind`,`completeness`,`last_refined`; closed `catalog.schema.json` |
| process/48 exemplar | Gold bar: `sources`, `bloom_*`, `claim_tiers`, `do_not`, `related` |
| `derived:` HTML blocks | Root SoT counts — orthogonal to YAML |

---

## 4. Closed key registry (Embody for epic memos)

**Required:** `title`, `status`, `date` (ISO), `claim_tiers`, `related` (list ≤8
preferred).  
**When `bloom_gate: required-through-create`:** non-empty `bloom_mcp`,
`sources` with ≥1 of `llms_txt`|`deepwiki_ask`|`github`|`arxiv`.  
**Optional high-ROI:** `epic`, `do_not`, `spec_gate`, `last_reviewed`,
`freshness` (`evergreen`|`quarterly`|`tip-bound`), `superseded_by`, `aliases`,
sensor stamps (`stars_as_of`, …).  
**Deprecated aliases (fix→fail):** `claim tiers`→`claim_tiers`,
`research date`→`date`.

Root / packs / skills: see §0 table — **kind schemas**, not one god schema.

---

## 5. Low-level heuristics (maximize *use*)

1. Agent sees `status` + `do_not` in first screenful → cheap refuse.  
2. Typed `sources` → replay DeepWiki/llms without body archaeology.  
3. `related` path-exists gate → no dead look-first.  
4. Generated `docs/research/_frontmatter_index.yaml` (Quarto listing analogue)
   → query without opening 127 bodies.  
5. `--fix` for mechanical renames; human pass for staleness prose.  
6. Bidirectional related as **advisory** first (DataCite one-way relations
   exist).

---

## 6. Adversarial

| Failure | Mitigation |
| --- | --- |
| False-green: broad exempt globs | Explicit kind map + tests per kind |
| False-red: Bloom on every README | README/`archive/` soft or exempt |
| Parser can't read nested `sources` | PyYAML in sibling module |
| claims.py LOC explosion | Never edit into 1863 file — siblings ≤225 |
| Metadata Completeness% as Cover% | Refuse — boolean schema only |

---

## 7. Create — epic tickets

| ID | Ticket | Acceptance |
| --- | --- | --- |
| **MD0-1** | Design Spec `docs/design/md-frontmatter-metadata-design-2026-08-10.md` | Kind matrix finalized; root = derived-only |
| **MD0-2** | `md_frontmatter_kinds.py` registries | Path→kind; allowlists; deprecated map |
| **MD0-3** | `md_frontmatter_validate.py` | Validate one doc; path-exists related |
| **MD0-4** | `check_md_frontmatter.py` CLI | Walk corpus; `--fix`; exit≠0 on hard |
| **MD0-5** | Wire into `pre_pr` / claims companion | Hard gate on tip |
| **MD0-6** | Tests `tests/ci/test_md_frontmatter*.py` | domain_ci_meta; fix+fail cases |
| **MD0-7** | Normalize pass corpus C | Renames; add missing required on epic memos; index file |
| **MD0-8** | Backlog + README rule | Active tip E-MD0; process pointer |

**Implement blocked until Design Spec exists on tip** (this memo = research SoR).

---

## 8. Status

Research **Complete** through Bloom Create. Next: Design Spec (MD0-1), then
Implement MD0-2…8 on `cursor/e-md0-frontmatter-metadata-61f3`.
