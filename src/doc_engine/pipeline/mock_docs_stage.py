"""Mock Stage 4 — fourteen taxonomy documents with well-formed tags."""

from __future__ import annotations

import os

from doc_engine.pipeline.mock_citations import (
    confirmed_tag,
    evidenced,
    per_existing_docs_tag,
    pick,
    unknown_tag,
)
from doc_engine.pipeline.mock_stage_constants import (
    BUCKET_PHRASING,
    DOC_BUCKETS,
    DOC_ORDER,
)
from doc_engine.pipeline.mock_stage_io import _write_text

DOC_INTRO = (
    "> **MOCK DOCUMENT.** Written by `python -m doc_engine.pipeline.local_runner`, not by a\n"
    "> `doc-writer` subagent. The evidence tags below are real and resolvable\n"
    "> — they cite lines this run's own signal scan actually found — but the\n"
    "> prose is templated and this file documents nothing. It exists so the\n"
    "> Stage 4 gate and the citation checks have real input.\n"
)

def _append_known_limitations(body, todos, tag_totals):
    """Append TODO/FIXME candidate bullets for known_limitations.md."""
    body.append("## TODO/FIXME candidates (candidates, not facts)")
    body.append("")
    if not todos:
        body.append(
            f"- No TODO/FIXME/XXX/HACK markers were found in this repo. "
            f"Whether that reflects a clean codebase or markers tracked "
            f"elsewhere is {unknown_tag()}."
        )
        tag_totals["unknown"] += 1
        return
    for hit in todos[:15]:
        body.append(
            f"- `{hit['file']}` carries a `{hit['marker']}` marker "
            f"{evidenced(hit['file'], hit['line'])}."
        )
        tag_totals["evidenced"] += 1


def _append_evidenced_claims(body, pool, doc_name, tag_totals):
    """Append evidenced claim bullets for a non-known_limitations doc."""
    picks = pick(pool, DOC_BUCKETS.get(doc_name) or [], 8)
    body.append("## Evidenced claims")
    body.append("")
    if not picks:
        body.append(
            f"- No deterministic signal-scan evidence mapped to this "
            f"document for this repo, so its content is "
            f"{unknown_tag()}."
        )
        tag_totals["unknown"] += 1
        return
    for bucket, (relpath, line, match) in picks:
        template = BUCKET_PHRASING.get(bucket, "`{file}` matched `{match}`")
        sentence = template.format(file=relpath, match=match)
        body.append(f"- {sentence} {evidenced(relpath, line)}.")
        tag_totals["evidenced"] += 1


def _append_interview_section(body, confirmed_ids, today, tag_totals):
    """Append interview-dependent claims shared by every mock doc."""
    body += ["", "## Interview-dependent claims", ""]
    if confirmed_ids:
        body.append(
            f"- Ownership and operational context for this service were "
            f"recorded in the interview {confirmed_tag(today)}."
        )
        tag_totals["confirmed"] += 1
    body.append(f"- Anything not covered above is {unknown_tag()}.")
    tag_totals["unknown"] += 1


def _append_existing_docs_section(body, existing_readme, tag_totals):
    """Optionally note a pre-existing README under Per existing docs."""
    if not existing_readme:
        return
    body += [
        "",
        "## Pre-existing documentation",
        "",
        f"- The repo's own overview was read but not verified against code "
        f"{per_existing_docs_tag(existing_readme)}.",
    ]
    tag_totals["per_existing_docs"] += 1


def _build_one_doc_body(name, pool, todos, confirmed_ids, today, existing_readme, tag_totals):
    """Assemble markdown lines for one taxonomy document."""
    body = [f"# {name.replace('_', ' ').title()}", "", DOC_INTRO, ""]
    if name == "known_limitations":
        _append_known_limitations(body, todos, tag_totals)
    else:
        _append_evidenced_claims(body, pool, name, tag_totals)
    if name == "architecture":
        body += [
            "",
            "## Merged diagram",
            "",
            "See `architecture_merged.md` in the run directory; a real run "
            "inlines it here along with its Discrepancies section.",
        ]
    _append_interview_section(body, confirmed_ids, today, tag_totals)
    _append_existing_docs_section(body, existing_readme, tag_totals)
    body.append("")
    return body


def mock_docs(docs_dir, pool, todos, answers, today, existing_readme, log):
    """One file per taxonomy name, each carrying only well-formed tags.

    check_pipeline_output.py gates three things here: all fourteen names
    present, no writer straying outside docs/, and every [Evidenced] citation
    resolving. The first is why this iterates DOC_ORDER rather than counting to
    fourteen — two writers handed the same path produce fourteen writes with
    one name duplicated and another missing, which a count check passes.
    """
    os.makedirs(docs_dir, exist_ok=True)
    confirmed_ids = [answer["id"] for answer in answers if answer["status"] == "answered"]
    written = []
    tag_totals = {"evidenced": 0, "confirmed": 0, "unknown": 0, "per_existing_docs": 0}

    for name in DOC_ORDER:
        body = _build_one_doc_body(
            name, pool, todos, confirmed_ids, today, existing_readme, tag_totals
        )
        path = os.path.join(docs_dir, f"{name}.md")
        _write_text(path, "\n".join(body))
        written.append(path)

    log(f"  wrote {len(written)} file(s) into {docs_dir}")
    log(f"  tag totals across all fourteen: {tag_totals}")
    return f"{len(written)} docs, tags={tag_totals}"

