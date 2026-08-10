---
title: Paper digest framework — type keys, sections, references, related walks
status: ACTIVE
date: '2026-08-10'
audience: [agent, developer, architect]
claim_tiers: Evidenced / Confirmed / Unknown
---

# Paper digest framework (project Source of Truth)

Canonical method for **principal-se-research-epic** Phase A. Title-skim is not
research. Greenfield planning trees may mirror this file; if they diverge, **this
path wins** for the parent repo.

## Hard truth about arXiv “keys”

The arXiv Atom application programming interface exposes **subject categories**
(for example `cs.SE`, `cs.AI`) plus abstract, authors, comment, journal
reference, digital object identifier — **not** a controlled vocabulary for
theoretical / empirical / systematic review.

| Field (API) | Use for |
| --- | --- |
| `arxiv:primary_category` + `category` | Domain filter / query (`cat:cs.SE`) |
| `summary` | Abstract only |
| `comment` | Page/figure hints; sometimes “survey” |
| HTML (`arxiv.org/html/<id>`) or PDF | **Sections**: methods, results, discussion, references |
| References in HTML | Related-paper walk (prefer cited works over “similar title” search) |

**Paper type is a classification we assign** after reading abstract + section
map. Mark it `[Inferred]` unless the paper explicitly self-labels.

Source: [arXiv API user manual](https://info.arxiv.org/help/api/user-manual.html)
`[Evidenced]`.

---

## Paper-type keys (closed set)

| Key | Means | Typical claim-bearing sections |
| --- | --- | --- |
| **theoretical** | Definitions, theorems, undecidability, complexity | Definitions, theorems, proofs, assumptions |
| **formal-systems** | Semantics + model of a deployed system class | Formal model, properties, case study |
| **empirical** | Measured outcomes on tasks/plants/models | Methods, results, threats to validity |
| **benchmark** | Dataset/framework/scoring protocol as contribution | Corpus construction, metrics, leaderboard |
| **systems-artifact** | Ships runnable tool/harness as primary claim | Design, implementation, evaluation |
| **methodological** | Process/method for others to apply | Protocol steps, worked example |
| **analytic** | Taxonomy / framework without new measure | Framework tables, case reasoning |
| **literature-survey** | Narrative review | Related work as body |
| **systematic-review** | Protocol-driven evidence synthesis | Search protocol, inclusion, synthesis |
| **position** | Vision / agenda | Motivation; thin methods |

Primary + optional secondary. Record both.

---

## Section map (always fill)

Prefer `https://arxiv.org/html/<id>`. If only PDF: `[Unknown section offsets]`.

| Slot | Look for | Extract |
| --- | --- | --- |
| Abstract | Atom `summary` | Problem, method, result bounds |
| Introduction / problem | Introduction, Problem | What fails today |
| Related work | Related Work | Closest prior; claimed difference |
| Methods / model | Method, Model, Approach, Formalization | Algorithm / definitions / protocol |
| Results / findings | Evaluation, Experiments, Results | Numbers + conditions; ceilings |
| Analysis / discussion | Discussion, Threats, Ablation | Limits; what measures got wrong |
| Conclusions | Conclusion, Future Work | Authors’ own scope claim |
| References | References | Seeds for related walk |

Paraphrase with `[Evidenced — arXiv:ID §n]`; quote sparingly.

---

## Type-specific understanding checklist

### theoretical / formal-systems

1. Objects and relations (tuple / state / transition).  
2. Proven vs assumed.  
3. Decidability / complexity if present.  
4. Non-preserved structure on transfer (isomorphism I1–I5).  
5. Full checker needed, or only an implied **constraint**?

### empirical / benchmark / systems-artifact

1. Plant (synthetic, live, self-hosted).  
2. Measure (paired tests, pass^k, false-DONE, …).  
3. What would **false-green** Definition of Ready / merge gates?  
4. Public artifact? Apply **anti-bogus** (below).  
5. Algorithm novelty vs engineering packaging.

### methodological / analytic / systematic-review / literature-survey

1. Extract re-runnable protocol or taxonomy.  
2. Prose recommendations ≠ merge System of Record.  
3. Use to structure Spikes and Quality Attribute Scenarios.

### position

1. Tag claims Unknown until another type backs them.  
2. Framing only.

---

## Related-paper walk

From References + Related Work:

1. Up to **5** cited works in the *same algorithm class*.  
2. Prefer 2024–2026 or foundational definitions.  
3. Atom → type → section map → short understanding per kin.  
4. Semantic Scholar / OpenAlex optional; on rate-limit stay on HTML refs.  
5. Stop when ≥5 **exact** genuine GitHub algorithm adopters exist, or honest
   **Pilot / invent** is written.

---

## GitHub anti-bogus filter

A repository **passes** only if most hold:

| Check | Pass means |
| --- | --- |
| Identity | Canonical org or widely depended package — not a paper-title rename |
| Maintenance | Recent push (≈2025–2026) or explicit long-term support; not archived |
| Substance | Real source + tests or Actions (when API-visible) |
| Algorithm fit | Implements the **named algorithm class** |
| Reject | Awesome scrapers, 0-star profile stubs, homonyms, anonymous 0-CI paper dumps |

Always separate **exact** vs **adjacent** adopters. Adjacent ≥5 does **not**
authorize “Must Adopt” for an exact algorithm that has zero public implementations.

---

## Digest file convention (parent repo)

```text
docs/research/papers/digests/<arxiv-id>-<short-slug>.md
```

Greenfield / port trees may use `research/papers-*/digests/` with the same
frontmatter and template (`PAPER_DIGEST_TEMPLATE.md` beside this file).

```yaml
arxiv: '2608.04278'
title: '…'
primary_type: empirical
secondary_types: [systems-artifact]
arxiv_categories: [cs.SE, cs.AI]
sections_source: html
related_walk: []
github_adopters_status: none | adjacent | exact
claim_tiers: Evidenced / Confirmed / Unknown
```

## Research-complete gate

A paper is not “researched” for Must / Spec / Embody-Adopt-Refuse until:

1. Type key assigned (`[Inferred]` or self-labeled)  
2. Section map filled (**not** abstract-only)  
3. Type checklist answered  
4. Related walk started (≥1 follow-on digest or explicit no algorithmic kin)  
5. GitHub anti-bogus table (exact vs adjacent)  

Until then: keep research depth **FAIL** / Unknown — do not soft-pass Port Ready.
