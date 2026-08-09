"""Mock Stage 3 — gap questions and interview answers."""

from __future__ import annotations

import os

from doc_engine.pipeline.mock_stage_constants import (
    _FALLBACK_CITATION_BUCKETS,
    DOC_BUCKETS,
)
from doc_engine.pipeline.mock_stage_io import _write_json

# Topics per document, drawn from doc-taxonomy.md's "Interview-worthy" notes —
# the categories that are structurally invisible to static analysis.
GAP_TOPICS = [
    ("integrations", "external-consumers", "Which external systems call this service, and who owns them?"),
    ("authorization", "unsecured-intent", "Is any unsecured endpoint deliberately public, or is that a gap?"),
    ("database", "write-ownership", "Which system is the authoritative writer for these tables?"),
    ("operations", "deploy-topology", "Where does this run, and what is the deploy cadence?"),
    ("known_limitations", "known-pain", "What breaks often enough that the team works around it?"),
    ("change_impact", "blast-radius", "What downstream consumer breaks first if this contract changes?"),
]

def _first_pool_citation(pool, buckets):
    """Return the first citation found across *buckets*, or None."""
    for bucket in buckets:
        rows = pool.get(bucket) or []
        if rows:
            return rows[0]
    return None


def _fallback_citation(pool, todos):
    """Any resolvable citation, else a TODO marker, else None."""
    citation = _first_pool_citation(pool, _FALLBACK_CITATION_BUCKETS)
    if citation is not None:
        return citation
    if todos:
        return (todos[0]["file"], todos[0]["line"], "TODO marker")
    return None


def _citation_for_topic(pool, blocks_file, fallback):
    """Prefer doc-bucket evidence; fall back to a repo-wide citation."""
    citation = _first_pool_citation(pool, DOC_BUCKETS.get(blocks_file) or [])
    return citation if citation is not None else fallback


def _build_gap_questions(pool, todos):
    """Build gap_questions.json rows anchored to resolvable evidence."""
    fallback = _fallback_citation(pool, todos)
    questions = []
    for blocks_file, topic, prompt in GAP_TOPICS:
        citation = _citation_for_topic(pool, blocks_file, fallback)
        if citation is None:
            continue
        relpath, line, _match = citation
        questions.append({
            "blocks_file": blocks_file,
            "topic": topic,
            "question": f"MOCK QUESTION (nobody was asked this): {prompt}",
            "evidence": f"{relpath.replace(os.sep, '/')}:{line}",
        })
    return questions


def _build_interview_answers(questions, today):
    """Record answered/skipped interview rows (every third is skipped)."""
    answers = []
    for index, question in enumerate(questions):
        skipped = (index % 3 == 2)
        answers.append({
            "id": f"{question['blocks_file']}.{question['topic']}",
            "question": question["question"],
            "status": "skipped" if skipped else "answered",
            "answer": None if skipped else (
                "MOCK ANSWER: no human was interviewed for this run; this string "
                "exists so run_manifest.py's answered/skipped counts and the "
                "[Confirmed] tag lane have something to read."
            ),
            "date": today,
        })
    return answers


def mock_gap_and_interview(out_dir, pool, todos, today, log):
    """gap_questions.json in agents/gap-analyzer.md's shape, then the
    interview_answers.json the orchestrating thread would record.

    validate_gap_analyzer_questions() enforces three things worth naming: the
    four required keys, blocks_file drawn from the fourteen, and contiguous
    grouping by blocks_file. `evidence` must carry a real resolvable path:line
    and must not be an elided `src/.../Thing.java` — that's the one point where
    the whole [Confirmed] lane is anchored to a real location, so the mock
    takes its citations from the same verified pool the docs use.
    """
    questions = _build_gap_questions(pool, todos)
    _write_json(os.path.join(out_dir, "gap_questions.json"), questions)
    log(
        f"  wrote gap_questions.json ({len(questions)} question(s), "
        f"grouped by blocks_file)"
    )

    # The interview itself is the one stage that structurally cannot be mocked
    # into something true: it's the orchestrating thread talking to a person.
    # So every answer is marked as a mock, and every third is a skip — because
    # SKILL.md is explicit that "asked, unanswered" must be recorded as a skip
    # rather than a blank, and a mock run should exercise that path too.
    answers = _build_interview_answers(questions, today)
    _write_json(os.path.join(out_dir, "interview_answers.json"), answers)
    answered = sum(1 for answer in answers if answer["status"] == "answered")
    log(
        f"  wrote interview_answers.json ({answered} answered, "
        f"{len(answers) - answered} skipped)"
    )
    return f"{len(questions)} gap question(s), {len(answers)} recorded answer(s)"

