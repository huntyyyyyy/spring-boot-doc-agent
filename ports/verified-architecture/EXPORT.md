# Export — create the standalone GitHub repository

**Port Ready:** CONDITIONAL (`STATUS.md` / `PORT_READY.md`) — research depth not
green. **Implement Ready:** no.

Cloud tokens often cannot `createRepository`. Create an empty private repo in the UI, then from **this folder as root**.

Do not export until Architecture Decision Record index and FREEZE status match
`STATUS.md`. Prefer tip work under the monorepo `ports/verified-architecture/`
until Definition of Ready improves.

**Hooks:** tip `.cursor/hooks.json` (including semantic-review inject/audit/stop)
does **not** automatically exist in a greenfield clone unless copied. Port Skills
under `.cursor/skills/` do export with this tree.
