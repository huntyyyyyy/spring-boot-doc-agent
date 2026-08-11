---
name: whole-words-prose
description: >-
  Expand every acronym and short label to a full phrase in user-facing chat and
  in ports/verified-architecture Markdown. Use whenever writing STATUS, BOUNDARY,
  Architecture Decision Records, research memos, discovery answers, reviews, or
  any reply that would otherwise say MCP, DoR, ADR, Spec, SoT, JIT, OS, FS, PoS,
  STEAD, ICD, QAS, or similar bare shorts.
---

# Skill: Whole-words prose (no bare acronyms)

**Authority:** `ports/verified-architecture/GLOSSARY.md` (phrase table).  
**Companion:** Skill `predicate-prose` (anti-tautology). This skill is about
*labels*; that skill is about *empty predicates*.

## Hard rule for user-facing chat

Write the **full phrase**. Do not use a bare acronym as the only form of a
term in a sentence the human must decide on.

| Wrong (bare) | Right (whole words) |
| --- | --- |
| MCP server | Model Context Protocol server |
| DoR FAIL | Definition of Ready still has zero PASS rows |
| OQ-01 | open question on product boundary |
| ADR-0011 | Architecture Decision Record on protocol pin and tool surfaces |
| Spec export | specification-tree export |
| SoT / SoR | source of truth / system of record |
| JIT disk | just-in-time disk read (no background index) |
| β/ρ | Proof-or-Stop freshness binding and command receipt identity |
| FS/wiki stack | filesystem read/write tools plus wiki page writers |

Allowed exceptions (only these):

1. Inside backticks / fenced code / file paths (`icd/mcp-tools.md`).  
2. **Once** after the full phrase in the same paragraph:  
   `Architecture Decision Record ADR-0001`.  
3. Choice tokens the human must type back (`Q1-DOC`) — expand the meaning in
   the same bullet, not only the token.

## Three checks before you send

1. **Acronym scan:** If a token is mostly capitals and ≤6 letters, expand it
   unless it is in the exception list above.  
2. **Cold-reader test:** Could a teammate who never opened this repo understand
   the sentence without a glossary? If no, expand.  
3. **Decision test:** For human gates, each option must name a concrete day-90
   outcome — not “verify spine vs brownfield MCP.”

## Ban these reply shapes

- Headers like “What lands / Hard contradiction / Also refuse” with only jargon
  chips underneath.  
- “Embody X / Refuse Y / Adopt Z” without one plain sentence of *what changes*.  
- Stacking five acronyms in one bullet.

## Forced rewrite shape

`Full phrase — what it does — bound (path or number) — what fails if ignored`

Example:  
“Grounding gap — count of model claims minus verifiable source-file citations —
target near zero on a fixed question set — if nonzero, the server is guessing.”

## When editing the port tree

Same rule as chat. Prefer updating `GLOSSARY.md` when a new short label appears
more than twice. Do not invent a parallel glossary under `docs/`.
