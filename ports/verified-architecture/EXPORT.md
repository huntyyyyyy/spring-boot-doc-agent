# Export — create the standalone GitHub repository

**Port Ready:** CONDITIONAL (`STATUS.md` / `PORT_READY.md`) — research depth not
green. **Implement Ready:** no.

Cloud tokens often cannot `createRepository`. Create an empty private repo in the UI, then from **this folder as root**.

Do not export until Architecture Decision Record index and FREEZE status match
`STATUS.md`. Prefer tip work under the monorepo `ports/verified-architecture/`
until Definition of Ready improves.

## What this export is

| Mode | Allowed? | Bound |
| --- | --- | --- |
| Spec sandbox (more research / Accept prep) | **CONDITIONAL** | Wave-0 Port row in `SIGNOFF_LOG.md` should be signed or explicitly deferred |
| Product crates / daemons | **No** | Definition of Ready 0 PASS; D0 FAIL |

## Bootstrap after clone (Spec-only)

1. Read `AGENT_BOOTSTRAP.md` → `STATUS.md` → `GLOSSARY.md`.  
2. Treat `research/` as evidence packs — not Implement green.  
3. FREEZE deepen-only: receipt β/ρ, claim withdrawal, Model Context Protocol handle lifecycle.  
4. Do **not** invent parallel Interface Control Document paths under `docs/design/`.

## Tip hooks / Skills copy checklist

The port tree under this folder has Skills at `.cursor/skills/` (they export
with the tree). It does **not** ship tip `.cursor/hooks.json`.

If you need semantic-review inject / audit / stop (or tip Claude policy bridges)
in a greenfield clone:

| Copy from tip monorepo | Into standalone | Notes |
| --- | --- | --- |
| `.cursor/hooks.json` | `.cursor/hooks.json` | Adjust command paths if layout differs |
| `.cursor/hooks/inject_semantic_review.py` (+ audit/stop siblings) | same relative paths | Optional for Spec-only |
| Tip Claude policy bridges (if used) | as referenced by hooks | Pipe-exit / network deny are tip concerns |

**Fail-mode:** assuming a greenfield clone has tip inject/audit/stop without this
checklist — known export gap under FREEZE; not a soft-pass for Implement.

Port Skills under `.cursor/skills/` (including `semantic-adversarial-review`)
do export with this tree when present.
