# Export — create the standalone GitHub repository

**Port Ready:** yes (`PORT_READY.md`). Implement Ready: no.

Cloud tokens often cannot `createRepository`. Create an empty private repo in the UI, then from **this folder as root**:

```bash
cd /path/to/ports/verified-architecture   # or the exported copy
git init
git add -A
git commit -m "Initial commit: verified architecture Spec + RAG corpus (Port Ready)"
git branch -M main
git remote add origin git@github.com:<org>/<repo>.git
git push -u origin main
```

Point Cursor/Cloud agent root at that repo. First message: paste from
`HOW_TO_PRIME_AGENTS.md`.
