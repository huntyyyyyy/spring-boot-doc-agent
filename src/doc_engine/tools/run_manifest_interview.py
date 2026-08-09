"""Interview-answers parsing for run_manifest finalize."""

from __future__ import annotations

import json
import sys

from doc_engine.core.jsonio import load_json as _read_json


def _empty_interview():
    return {"asked": 0, "answered": 0, "skipped": 0, "questions": []}


def _tally_interview_entry(entry, questions):
    """Append one interview entry; return answered/skipped deltas (0 or 1)."""
    if not isinstance(entry, dict) or "id" not in entry or "status" not in entry:
        print(
            f"warning: interview file entry missing required 'id'/'status' keys, "
            f"skipping: {entry!r}",
            file=sys.stderr,
        )
        return 0, 0
    status = entry["status"]
    answered = 1 if status == "answered" else 0
    skipped = 1 if status == "skipped" else 0
    if status not in ("answered", "skipped"):
        print(
            f"warning: interview entry {entry.get('id')!r} has unrecognized "
            f"status {status!r}",
            file=sys.stderr,
        )
    questions.append({"id": entry["id"], "status": status})
    return answered, skipped


def parse_interview_file(path):
    """Parse interview_answers.json; malformed input → zeros + stderr."""
    empty = _empty_interview()
    try:
        data = _read_json(path)
    except (OSError, json.JSONDecodeError) as e:
        print(
            f"warning: could not read/parse interview file '{path}': {e}",
            file=sys.stderr,
        )
        return empty
    if not isinstance(data, list):
        print(
            f"warning: interview file '{path}' is not a JSON list as documented "
            f"in SKILL.md Stage 3, recording zeros",
            file=sys.stderr,
        )
        return empty

    questions, answered, skipped = [], 0, 0
    for entry in data:
        a, s = _tally_interview_entry(entry, questions)
        answered += a
        skipped += s
    return {
        "asked": len(questions),
        "answered": answered,
        "skipped": skipped,
        "questions": questions,
    }
