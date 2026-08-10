# Export — create the standalone GitHub repository

Cloud tokens often cannot `createRepository`. Create an empty private repo in the UI, then:

```bash
cd /path/to/this/tree
git init
git add -A
git commit -m "Initial commit: verified architecture planning + RAG corpus"
git branch -M main
git remote add origin git@github.com:<org>/<repo>.git
git push -u origin main
```

Optional: attach this tree as a Cursor Cloud environment root so agents load `.cursor/rules/` and nest MDCs.
