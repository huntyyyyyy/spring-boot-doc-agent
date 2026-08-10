---
title: OpenAlex / Semantic Scholar / arXiv — field-select cheatsheet
status: ACTIVE
date: '2026-08-10'
---

# Field-select cheatsheet (copy into tool calls)

Full schemas: `paper-api-schemas.md`.

## OpenAlex scout

```
GET https://api.openalex.org/works
  ?filter=publication_year:2026,type:preprint|article|conference-paper
  &select=id,doi,title,type,publication_year,cited_by_count,primary_topic
  &sort=publication_date:desc
  &per-page=25
  &mailto=YOUR_EMAIL
```

Drop: `type:paratext`, `erratum`, `retraction`, `editorial`, `letter`.

## Semantic Scholar scout

```
GET https://api.semanticscholar.org/graph/v1/paper/search
  ?query=YOUR_ENTITY_TERMS
  &year=2026-
  &publicationTypes=JournalArticle,Conference,Study
  &fields=paperId,externalIds,title,year,publicationTypes,tldr,citationCount,fieldsOfStudy
  &limit=20
```

Survey lane: `publicationTypes=Review,MetaAnalysis` (separate pass).

## arXiv Atom scout

```
GET https://export.arxiv.org/api/query
  ?search_query=cat:cs.SE+AND+submittedDate:[202606010000+TO+202608102359]
  &sortBy=submittedDate&sortOrder=descending
  &max_results=25
```

Known id: `?id_list=2608.04278` (abstract only).

## Only after shortlist

```
GET https://arxiv.org/html/<id>     # section map
GET …/paper/ARXIV:<id>/references?fields=title,year,externalIds,publicationTypes
```
