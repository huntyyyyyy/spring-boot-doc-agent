"""Constants for run_manifest stage vocabulary and preflight mapping."""

from __future__ import annotations

# ML Metadata's Execution.last_known_state enum vocabulary, reused verbatim
# rather than inventing a bespoke one (see the research doc's design notes).
# "new" is accepted as a stage status for forward-compatibility but nothing
# in this module currently produces it.
STAGE_STATUSES = frozenset(
    {"new", "running", "complete", "failed", "cached", "canceled"}
)
END_STAGE_STATUSES = sorted(STAGE_STATUSES - {"new", "running"})

# capacity_preflight.py's stage_fanout dict uses a different, independently
# evolved key vocabulary — stage1_file_summarizer / stage2_architect_segment /
# stage2_architect_merge / stage3_gap_analyzer /
# stage3_software_architect_and_testing / stage4_doc_writer — which does not
# match this module's own stage names. This mapping lets finalize's
# --preflight-file tie-in diff predicted vs. actual fan-out.
# stage2_architect_segment and stage2_architect_merge both fold into this
# module's single combined "architect" stage (predicted counts are summed).
# stage3_gap_analyzer and stage3_software_architect_and_testing map to two
# *different* manifest stages (dispatched in the same turn but tracked
# separately).
PREFLIGHT_TO_MANIFEST_STAGE = {
    "stage1_file_summarizer": "file_summarize",
    "stage2_architect_segment": "architect",
    "stage2_architect_merge": "architect",
    "stage3_gap_analyzer": "gap_analysis_interview",
    "stage3_software_architect_and_testing": "architecture_testing_review",
    "stage4_doc_writer": "doc_writer",
}

_TAG_KEY_MAP = {
    "evidenced": "Evidenced",
    "confirmed": "Confirmed",
    "unknown": "Unknown",
    "per_existing_docs": "PerExistingDocs",
}
