---
title: Paper digest framework — type keys, sections, references, related walks
status: ACTIVE
date: '2026-08-10'
audience: [agent, developer, architect]
claim_tiers: Evidenced / Confirmed / Unknown
---

# Paper digest framework

Use this **before** promoting a paper into Must spine, Definition of Ready,
or Embody/Adopt/Refuse. Title-skim is not enough.

Whole words — root `GLOSSARY.md`.

## Hard truth about arXiv “keys”

The arXiv Atom application programming interface exposes **subject categories**
(for example `cs.SE`, `cs.AI`) plus abstract, authors, comment, journal
reference, digital object identifier — **not** a controlled vocabulary for
*theoretical / empirical / systematic review*.

| Field (API) | Use for |
| --- | --- |
| `arxiv:primary_category` + `category` | Domain filter / query (`cat:cs.SE`) |
| `summary` | Abstract only |
| `comment` | Page/figure hints; sometimes “survey” |
| HTML (`arxiv.org/html/<id>`) or PDF | **Sections**: methods, results, discussion, references |
| References in HTML | Related-paper walk (prefer cited works over “similar title” search) |

**Paper type is a classification we assign** after reading abstract + section
map. Mark it `[Inferred]` unless the paper explicitly self-labels (for example
“systematic literature review”).

Sources: [arXiv API user manual](https://info.arxiv.org/help/api/user-manual.html)
`[Evidenced]`.

---

## Paper-type keys (closed set — pick one primary, optional secondary)

| Key | Means | Typical sections that carry the claim |
| --- | --- | --- |
| **theoretical** | Definitions, theorems, undecidability, complexity | Definitions, theorems, proofs, discussion of assumptions |
| **formal-systems** | Semantics + model of a deployed system class | Formal model, properties, case study |
| **empirical** | Measured outcomes on tasks/plants/models | Methods, results, threats to validity |
| **benchmark** | Dataset/framework/scoring protocol as contribution | Corpus construction, metrics, leaderboard |
| **systems-artifact** | Ships runnable tool/harness as primary claim | Design, implementation, evaluation |
| **methodological** | Process/method for others to apply (not a product) | Protocol steps, worked example |
| **analytic** | Conceptual analysis / taxonomy / framework without new measure | Framework tables, case reasoning |
| **literature-survey** | Narrative review of a field | Related work as body; synthesis |
| **systematic-review** | Protocol-driven evidence synthesis (Kitchenham-class) | Search protocol, inclusion, synthesis |
| **position / vision** | Argument for a direction | Motivation, agenda; thin methods |

A paper may be **formal-systems + empirical** (secondary). Record both.

---

## Section map (always fill)

Prefer HTML when available (`https://arxiv.org/html/<id>`). If only PDF,
note `[Unknown section offsets]`.

| Slot | Look for headings like… | Extract (short) |
| --- | --- | --- |
| **Abstract** | Atom `summary` | Problem, method, result bounds in authors’ words |
| **Introduction / problem** | Introduction, Problem | What fails today |
| **Related work** | Related Work | Closest prior; what they claim differs |
| **Methods / model** | Method, Model, Approach, Formalization | Algorithm / definitions / protocol |
| **Results / findings** | Evaluation, Experiments, Results | Numbers + conditions; ceiling effects |
| **Analysis / discussion** | Discussion, Threats, Ablation | What measures got wrong; limits |
| **Conclusions** | Conclusion, Future Work | Authors’ own scope claim |
| **References** | References | Seed list for related walk (next section) |

Copy **quotes sparingly**; prefer paraphrase with `[Evidenced — arXiv:ID §n]`.

---

## Methodical understanding checklist (by primary type)

### If theoretical / formal-systems

1. State the **objects** and **relations** (tuple / state / transition).
2. State what is **proven** vs **assumed**.
3. State **decidability / complexity** if present.
4. List **non-preserved** structure when transferring to our product (isomorphism test).
5. Ask: do we need the full checker, or only a **constraint** implied by the proof?

### If empirical / benchmark / systems-artifact

1. What is the **plant** (synthetic worlds, live servers, self-hosted corpus)?
2. What is the **measure** (paired tests, pass^k, false-DONE rate)?
3. What would **false-green** our Definition of Ready if we over-generalize?
4. Is there a **public artifact** (repository)? Apply anti-bogus filter.
5. Separately score **algorithm novelty** vs **engineering packaging**.

### If methodological / analytic / systematic-review / literature-survey

1. Extract the **protocol or taxonomy** we can re-run.
2. Do **not** treat prose recommendations as merge System of Record.
3. Prefer using them to **structure Spikes** and Quality Attribute Scenarios.

### If position / vision

1. Tag claims **Unknown** until backed by another type.
2. Useful for problem framing only.

---

## Related-paper walk (references → next digests)

Do **not** stop at one paper. From References + Related Work:

1. Pick up to **5** cited works that share the *algorithm class* (not just “agents”).
2. Prefer newer (2024–2026) or foundational (definition of the algorithm).
3. For each: Atom metadata → classify type → section map → one-paragraph understanding.
4. Optional: Semantic Scholar / OpenAlex citation graph when rate limits allow; if
   rate-limited, stay on arXiv HTML references `[Unknown — external graph]`.
5. Stop when either (a) five genuine GitHub algorithm adopters exist, or
   (b) you can honestly write **Pilot / invent** with eyes open.

---

## Digest file convention

```text
research/papers-2026-may-aug/digests/<arxiv-id>-<short-slug>.md
```

Frontmatter required:

```yaml
arxiv: '2608.04278'
title: '…'
primary_type: empirical   # from closed set above
secondary_types: [systems-artifact]
arxiv_categories: [cs.SE, cs.AI]
sections_source: html     # html | pdf | abstract-only
related_walk: []          # arxiv ids digested next
github_adopters_status: none | adjacent | exact
claim_tiers: Evidenced / Confirmed / Unknown
```

Body: use `PAPER_DIGEST_TEMPLATE.md` in this folder.

---

## Gate (Definition of Ready D0)

A Must-spine paper is not “researched” until:

1. Type key assigned `[Inferred]` or self-labeled  
2. Section map filled (not abstract-only)  
3. Type-appropriate checklist answered  
4. Related walk started (≥1 follow-on digest or explicit “no algorithmic kin”)  
5. GitHub anti-bogus table for the algorithm class  

Until then: keep D0 **FAIL**.
