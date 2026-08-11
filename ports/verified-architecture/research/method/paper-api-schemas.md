---
title: Paper research API schemas — route and filter before full digests
status: ACTIVE
date: '2026-08-10'
audience: [agent, developer, architect]
claim_tiers: Evidenced / Confirmed / Unknown
sources:
  - https://info.arxiv.org/help/api/user-manual.html
  - https://api.semanticscholar.org/api-docs/
  - https://developers.openalex.org/llms.txt
  - https://developers.openalex.org/api-reference/work-types
---

> Mirror of parent `docs/research/method/paper-api-schemas.md` — parent wins on conflict.
> **Historical / evidence — not product SoT.** Routing catalog only.

# Paper research API schemas

Use these **schemas + field selects** to filter candidates **before** fetching HTML
or writing a full paper digest. Goal: lower token use, higher selection floor.
Fail-mode: start with full PDF/HTML for a broad search.

Primary method still: `docs/research/method/paper-digest-framework.md`.  
This file is the **call catalog** for Phase A routing.

Whole words preferred in memos; API field names stay as published.

---

## 0. Routing ladder (do this order)

```text
1) OpenAlex  — type + year + topic filters; select= tiny fields
2) Semantic Scholar — publicationTypes + year + tldr; fields= tiny
3) arXiv Atom — cat: + submittedDate; id_list for known ids (abstract only)
4) arXiv HTML — ONLY for shortlist that survived 1–3 (section map)
5) paper-digest skill — full digest + related walk + GitHub anti-bogus
```

**Never** start with full PDF/HTML for a broad search.  
**Never** request `abstract` + `citations` + `references` + `embedding` on search lists.

---

## 1. OpenAlex (best native “work type” key)

| Item | Value |
| --- | --- |
| Base | `https://api.openalex.org` |
| large language model index | `https://developers.openalex.org/llms.txt` |
| OpenAPI | `https://developers.openalex.org/api-reference/openapi.json` |
| Polite pool | always pass `mailto=<contact>` (and `api_key` when available) |

### 1.1 Entity endpoints (calls we use)

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/works` | Search/filter works |
| GET | `/works/{id}` | One work (OpenAlex `W…`, `doi:…`, arXiv DOI) |
| GET | `/topics` | Resolve topic names → ids (do **not** filter by display name) |
| GET | `/autocomplete/{entity}` | Typeahead → ids |

### 1.2 Query parameters (list endpoints)

| Param | Schema | Notes |
| --- | --- | --- |
| `filter` | `field:value` CSV AND; `\|` OR within one field; `!` NOT; ranges `2020-2024`; comparisons `cited_by_count:>10` | |
| `search` | string | Costlier than filter — avoid for bulk routing |
| `sort` | e.g. `cited_by_count:desc`, `publication_date:desc` | |
| `select` | CSV of **root** fields only | **Required for token control** |
| `per-page` / `per_page` | int ≤ 100 | Prefer 25 for scouting |
| `page` | int | Shallow paging |
| `cursor` | `*` then token | Deep paging |
| `group_by` | field | Counts (e.g. `type`) |
| `mailto` | email | Polite pool |

### 1.3 Work `type` values (filter key for paper-form)

Use `filter=type:preprint` etc. Map to our digest `primary_type` **after** reading — OpenAlex type ≠ theoretical/empirical.

| `type` | Typical use in our routing |
| --- | --- |
| `preprint` | Default arXiv-class candidates |
| `article` | Peer-reviewed research articles |
| `review` | Literature / systematic / meta — route to survey checklist |
| `conference-paper` | Venue papers |
| `dataset` / `data-paper` | Artifact/data — not architecture Method Must unless entity is data |
| `software` / `software-paper` | Code artifact / software descriptor |
| `report` | Technical reports |
| `dissertation` | Usually demote unless foundational |
| `editorial` / `letter` / `paratext` / `erratum` / `retraction` / `book-review` / `news`-like `other` | **Filter out** for Must-spine algorithm search (`type:!paratext` etc.) |

Full list: [work-types](https://developers.openalex.org/api-reference/work-types) `[Evidenced]`.

### 1.4 Scout `select` (minimal)

```text
select=id,doi,title,type,publication_year,cited_by_count,primary_topic
```

Optional next tier (still small):

```text
select=id,doi,title,type,publication_year,cited_by_count,authorships,open_access,primary_location
```

**Do not** `select` full inverted abstracts on list scouts.

### 1.5 Example filters

```text
# 2026 CS-ish preprints (then refine with search/topics)
/works?filter=publication_year:2026,type:preprint&sort=publication_date:desc&select=id,doi,title,type,publication_year&per-page=25&mailto=…

# Exclude junk forms
/works?filter=publication_year:2026,type:!paratext,type:!erratum,type:!retraction&select=…

# DOI / arXiv DOI lookup
/works?filter=doi:https://doi.org/10.48550/arXiv.2608.04278&select=id,doi,title,type,publication_year,cited_by_count
```

Verified 2026-08-10: EA-Graph DOI resolves to `type: preprint`, `cited_by_count: 0` `[Evidenced]`.

### 1.6 Map OpenAlex `type` → digest routing

| OpenAlex | Prefer digest `primary_type` bias | Action |
| --- | --- | --- |
| `review` | literature-survey / systematic-review | Read protocol; rarely Must algorithm |
| `preprint` / `article` / `conference-paper` | empirical / formal-systems / systems-artifact (decide from sections) | Shortlist |
| `software` / `dataset` | systems-artifact / benchmark | GitHub/Zenodo path first |
| editorial/letter/paratext/… | — | Drop |

---

## 2. Semantic Scholar Academic Graph

| Item | Value |
| --- | --- |
| Base | `https://api.semanticscholar.org/graph/v1` |
| Docs | `https://api.semanticscholar.org/api-docs/` |
| Auth | Optional API key for higher rate limits; unauthenticated often **429** |

### 2.1 Endpoints we use

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/paper/search` | Relevance search (≤1000 ranked) |
| GET | `/paper/search/bulk` | Bulk / filter-heavy, weak relevance |
| GET | `/paper/search/match` | Single closest title match |
| GET | `/paper/{paper_id}` | One paper (`ARXIV:…`, DOI, S2 hash, `CorpusId:…`) |
| GET | `/paper/{id}/references` | Related walk (field-select!) |
| GET | `/paper/{id}/citations` | Influence (field-select!) |
| GET | `/paper/batch` | Many ids |
| GET | `/paper/autocomplete` | Typeahead |
| GET | `/snippet/search` | Passage search (optional) |
| GET | `/author/search`, `/author/{id}` | Author graph (rare) |

### 2.2 Shared query parameters

| Param | Schema | Notes |
| --- | --- | --- |
| `query` | string | Required on `/paper/search` |
| `fields` | CSV | **Default = only `paperId` + `title`** — always set explicitly |
| `offset` / `limit` | ints | Search limit ≤ 100 per page |
| `year` | `2024` or `2024-2026` | |
| `publicationDateOrYear` | date range | |
| `publicationTypes` | CSV enum (below) | **Closest S2 “paper form” key** |
| `fieldsOfStudy` | CSV | e.g. `Computer Science` |
| `venue` | CSV | |
| `minCitationCount` | int | |
| `openAccessPdf` | flag | Presence = require OA PDF |
| `sort` | bulk only: `citationCount:desc` etc. | |

### 2.3 `publicationTypes` enum (filter)

From Graph API docs `[Evidenced]`:

`Review`, `JournalArticle`, `CaseReport`, `ClinicalTrial`, `Conference`, `Dataset`, `Editorial`, `LettersAndComments`, `MetaAnalysis`, `News`, `Study`, `Book`, `BookSection`

Routing tips:

| Keep for Must algorithms | Usually drop / survey lane |
| --- | --- |
| `JournalArticle`, `Conference`, `Study` | `Review`, `MetaAnalysis` → survey checklist |
| `Dataset` when entity is data/benchmark | `Editorial`, `News`, `LettersAndComments` |

### 2.4 Scout `fields` (minimal)

```text
fields=paperId,externalIds,title,year,publicationTypes,tldr,citationCount,fieldsOfStudy
```

`tldr` is a **short** model summary — good for triage; **not** a section map and not Evidenced understanding.

Next tier (still before HTML):

```text
fields=paperId,externalIds,title,year,publicationTypes,tldr,abstract,citationCount,referenceCount,fieldsOfStudy,openAccessPdf
```

Related-walk tier (one paper):

```text
fields=title,year,externalIds
# on /references?fields=title,year,externalIds,publicationTypes
```

**Avoid on lists:** `embedding`, full `citations`/`references` trees, huge author details.

### 2.5 Paper id forms

`ARXIV:2608.04278`, `DOI:10.48550/arXiv.2608.04278`, CorpusId, S2 sha.

---

## 3. arXiv Atom API

| Item | Value |
| --- | --- |
| Endpoint | `GET https://export.arxiv.org/api/query` |
| Manual | `https://info.arxiv.org/help/api/user-manual.html` |
| Response | Atom 1.0 XML |
| Paper-type key | **None** — only subject `cat:` |

### 3.1 Query parameters

| Param | Required | Schema |
| --- | --- | --- |
| `search_query` | no* | Lucene-like fielded query |
| `id_list` | no* | Comma-separated arXiv ids (prefer for known ids) |
| `start` | no | 0-based offset |
| `max_results` | no | Page size (keep small, e.g. 10–25) |
| `sortBy` | no | `relevance` \| `lastUpdatedDate` \| `submittedDate` |
| `sortOrder` | no | `ascending` \| `descending` |

\*At least one of `search_query` / `id_list`.

### 3.2 `search_query` field prefixes

| Prefix | Field |
| --- | --- |
| `ti` | Title |
| `au` | Author |
| `abs` | Abstract |
| `co` | Comment |
| `jr` | Journal reference |
| `cat` | Subject category (`cs.SE`, `cs.AI`, …) |
| `rn` | Report number |
| `all` | All of the above |

Boolean: `AND`, `OR`, `ANDNOT`. Grouping: `%28` `%29`. Phrases: `%22…%22`. Spaces: `+`.

Date: `submittedDate:[YYYYMMDDHHMM+TO+YYYYMMDDHHMM]` (GMT).

Example:

```text
search_query=cat:cs.SE+AND+submittedDate:[202606010000+TO+202608102359]
&sortBy=submittedDate&sortOrder=descending&max_results=25
```

### 3.3 Atom entry fields (response schema)

| Element | Content |
| --- | --- |
| `title` | Title |
| `id` | `http://arxiv.org/abs/…` |
| `published` | Version-1 submit time |
| `updated` | Retrieved version submit time |
| `summary` | **Abstract only** |
| `author/name` | Authors |
| `link` | abs / pdf / doi |
| `category@term` | Categories (arXiv / ACM / MSC) |
| `arxiv:primary_category@term` | Primary subject |
| `arxiv:comment` | Author comment |
| `arxiv:journal_ref` | Journal ref |
| `arxiv:doi` | DOI if provided |

Feed also has OpenSearch `totalResults`, `startIndex`, `itemsPerPage`.

### 3.4 HTML follow-on (not Atom)

`https://arxiv.org/html/<id>` — section map for digest. Only after scout filters.

---

## 4. Crossref / Zenodo (secondary)

| API | When | Minimal call |
| --- | --- | --- |
| Crossref Works | DOI metadata / type | `https://api.crossref.org/works/{doi}` |
| Zenodo | Study artifacts when GitHub absent | Record DOI API (e.g. EA-Graph Zenodo) |

Use after OpenAlex/S2 point at a DOI with no GitHub.

---

## 5. Token budget policy (agents)

| Stage | Max payload habit |
| --- | --- |
| Scout list | titles + type/year/ids/`tldr` only (≤25 rows) |
| Shortlist (≤8) | + abstract OR OpenAlex type confirmation |
| Digest (≤3 Must) | HTML section map + checklist |
| Related walk | reference titles/years/ids first; HTML only for chosen kin |

If Semantic Scholar returns **429**, fall back to OpenAlex + arXiv Atom; do not spin.

---

## 6. Consistency floor (selection)

A candidate may enter a Must-spine shortlist only if:

1. Survived form filters (OpenAlex `type` and/or S2 `publicationTypes`) appropriate to the entity  
2. In the time window (`publication_year` / `submittedDate` / `year`)  
3. Atom or S2 abstract/`tldr` shows **algorithm-class** fit (not “also mentions agents”)  
4. Then — and only then — full digest + GitHub anti-bogus  

Document dropped candidates in one line: `dropped: <id> reason=type:review|off-window|no-algorithm-fit`.
