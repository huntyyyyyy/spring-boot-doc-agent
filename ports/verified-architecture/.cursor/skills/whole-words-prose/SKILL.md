---
name: whole-words-prose
description: >-
  Expand every acronym and short label to a full phrase in user-facing chat and
  in ports/verified-architecture Markdown. Use for STATUS, BOUNDARY, Architecture
  Decision Records, research memos, discovery answers, and reviews — never leave
  MCP, DoR, ADR, Spec, SoT, JIT, PoS, STEAD, ICD bare in prose the human must act on.
---

# Skill: Whole-words prose (no bare acronyms)

**Authority:** root `GLOSSARY.md` in this port.  
**Companion:** Skill `predicate-prose`. Tip mirror: `.cursor/skills/whole-words-prose/`.

## Hard rule

Full phrases in user-facing chat and new/edited port Markdown. Bare acronyms
allowed only in paths/code fences, or once after the full phrase
(`Architecture Decision Record ADR-0001`), or as typed choice tokens that are
expanded in the same bullet (`Q1-DOC` = documentation-first day-90 ask).

## Three checks

1. Capitals-heavy ≤6-letter token → expand.  
2. Cold teammate understands without glossary → else expand.  
3. Human gates name concrete outcomes, not slogan pairs.

## Ban

Jargon chip headers (“what lands / hard contradiction”) without plain sentences;
Embody/Refuse/Adopt without saying what work changes; acronym stacks.

## Shape

`Full phrase — what it does — bound — fail-mode`
