---
title: Anti-tautology Spec prose — predication and information gain
status: RESEARCH — Adopt for ports/verified-architecture writing + Skill
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
related:
  - ../mdc-devex/cursor-mdc-activation-algebra.md
  - ../../.cursor/skills/predicate-prose/SKILL.md
  - ../../docs/standards/adr-standard.md
  - ../../STATUS.md
do_not:
  - Confuse progressive disclosure (load less) with tautology (say nothing)
  - Delete structure folders solely to look non-tautological
  - Soft-pass Definition of Ready by rewriting slogans
last_reviewed: '2026-08-11'
doc_role: gap
freeze_class: deepen
look_first:
  - ../../STATUS.md
  - ../../.cursor/skills/predicate-prose/SKILL.md
mcp_tools:
  - spec_gap
accepted: false
corpus_version: '2026-08-11'
sources:
  primary_docs:
    - https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
  arxiv:
    - '2607.17598'
  web:
    - https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
---

# Anti-tautology for Spec corpora

**Product question.** Port Markdown is consuming agent tokens while reducing
uncertainty by ~0. How do we implement the user's three principles so files
*predicate attributes* instead of restating names?

## 0. User principles → engineering tests

| Principle | Failure mode in this port | Pass test |
| --- | --- | --- |
| **Logical** (A→B, not A→A) | “Rust owns the engine” when the title is already “Rust owns engine” | After deleting the subject noun, a **new** consequence remains |
| **Semantic** (predication) | “Polyglot-first means languages are peers” (synonym circle) | Sentence assigns a measurable attribute, bound, or fail-mode |
| **Epistemological** (information gain) | “Implement Ready: NO” repeated without *what blocks* | Cold agent’s next action set shrinks |

**Embody** these three tests as Skill `predicate-prose`. Progressive disclosure
(`[Evidenced — Agent Skills / arXiv 2607.17598]`) solves *when* to load; it does
**not** fix *what* the loaded text asserts.

## 1. External practices to steal (not rename)

| Source | Steal | Refuse |
| --- | --- | --- |
| Nygard ADR `[Evidenced — Fowler/Cognitect]` | Context = forces; Decision = choice; Consequences = **trade-offs including negatives** | Extra sections that restate Decision |
| ADR “consequences most neglected” `[Confirmed — industry practice]` | One sentence: what gets harder | Benefit-only sales pitches |
| Agent Skills progressive disclosure `[Evidenced]` | Lean always-on; depth on demand | Dumping synonym essays into alwaysApply |
| Claim tiers (in-repo) | Unknown stays Unknown | “Research complete” slogans |

## 2. Port-specific tautology shapes (observed)

1. **Title echo** — body repeats Architecture Decision Record title.  
2. **Folder label echo** — README = folder name + “see PRECODE_MAP”.  
3. **Policy echo** — FREEZE / Refuse Python restated without *which file changes*.  
4. **Synonym stack** — complex≈complicated; polyglot≈many languages; corpus≈collection of docs.  
5. **Excluded-middle filler** — “may or may not Accept” with no Accept criterion.

## 3. Implementation (Adopt)

| Layer | Mechanism |
| --- | --- |
| Skill (Spec prose) | `predicate-prose` — rewrite protocol + detection checklist |
| Skill (chat reviews) | `semantic-adversarial-review` (port + tip) — if→then spine |
| Hooks (tip root) | `inject_semantic_review` → `audit_semantic_review_response` → `stop_semantic_review_rewrite` — regex density sensor for Support/Refuse stamps vs if→then; **not** a formal semantics engine |
| Always-on | One constitution line: refuse synonym-only sentences |
| Wave rewrite | STATUS, BOOTSTRAP, ADRs, nest READMEs, Spike — not all research digests at once |
| Frontmatter | `look_first` already forces edges; body must add attributes those edges cannot carry |

**Honesty on the hook:** the detector Embody’s *epistemological* test only as a
cheap sensor (stamp count vs if→then count). It does not implement Montague /
situation semantics. Theory lives in this memo + Skills; hooks refuse the
obvious scoreboard failure mode.

## 3b. Why indexes use backticks more than markdown links

If a catalog’s job is Retrieval-Augmented Generation chunk routing and agent
`Read` by path, then a backtick path is the operable handle. Markdown links
help humans click; they are not required for `look_first` / `related` edges
(those are YAML). Mixed docs (ADR index with `[0007](…)` vs `research/INDEX.md`
with `` `path` ``) are a **progressive-disclosure / audience split**, not proof
that missing links mean missing files. Fail-mode: treating an unlinked catalog
row as “file absent.”

## 4. Forced sentence shape (Create)

Prefer:

`Subject | attribute | numeric or path bound | fail-mode if violated`

Example replace:

- Tautology: “SQLite is the derived registry.”  
- Predicate: “SQLite holds rebuildable bean/edge rows written only by the Rust
  engine; a second writer fails Architecture Decision Record ADR-0006.”

## 5. Bloom

| Level | Evidence |
| --- | --- |
| 1 | User three principles; Nygard ADR; Skills progressive disclosure; in-port tautology shapes |
| 2 | Disclosure ≠ predication |
| 3 | Skill + rewritten STATUS/constitution |
| 4 | Embody tests; Adopt Nygard consequences; Refuse mass research rewrite as day-one |
| 5 | False-green: prettier synonyms; false-red: deleting stubs that correctly say “empty” |
| 6 | Skill + Wave-0 file rewrite |

## 6. Exit

Skill exists; STATUS and constitution pass the three tests; ADR index points at
the skill; cold-start invokes it before editing.
