"""Shared vocabulary and evidence maps for mock generative stages."""

from __future__ import annotations

from doc_engine.tools.doc_tag_utils import VALID_DOC_FILES

# The em dash the tag grammar requires, spelled as an escape rather than a
# literal so a copy/paste through a lossy encoding can't silently downgrade it
# to a hyphen — which is the exact malformed-tag case doc_tag_utils.py's
# find_malformed_tags() exists to catch, and would make this script's own
# output fail the gate it is trying to demonstrate.
EM = "—"

# Stage names run_manifest.py records. Source of truth for the vocabulary:
# skills/document-spring-repo/SKILL.md's concurrency contract, which names
# exactly these six and requires one start/end pair each, from the
# orchestrating thread only.
STAGE_SIGNAL_SCAN = "signal_scan"
STAGE_PARTITION = "partition"
STAGE_FILE_SUMMARIZE = "file_summarize"
STAGE_ARCHITECT = "architect"
STAGE_GAP_INTERVIEW = "gap_analysis_interview"
STAGE_DOC_WRITER = "doc_writer"

# The fourteen output files, in the taxonomy's own order. VALID_DOC_FILES is a
# frozenset (unordered), and a fan-out of fourteen reads better in a log when
# it comes out in a stable, documented order — so the order lives here and is
# checked against the imported set at import time rather than duplicating the
# set itself.
DOC_ORDER = [
    "readme", "architecture", "integrations", "authorization", "database",
    "operations", "observability", "troubleshooting", "configuration",
    "change_impact", "glossary", "local_development", "testing",
    "known_limitations",
]
assert set(DOC_ORDER) == set(VALID_DOC_FILES), (
    "DOC_ORDER has drifted from doc_tag_utils.VALID_DOC_FILES"
)

# Which signal-scan evidence buckets feed which document. Mirrors
# spring_signal_scan.py's own docstring mapping ("Output buckets map directly
# to documentation categories") plus doc-taxonomy.md, and is used here only to
# pick plausible citations for the mock docs.
DOC_BUCKETS = {
    "readme": ["api_surface", "persistence"],
    "architecture": ["api_surface", "persistence", "messaging"],
    "integrations": ["api_surface", "outbound_clients", "messaging"],
    "authorization": ["security"],
    "database": ["persistence", "raw_queries"],
    "operations": ["deployment", "configuration"],
    "observability": ["observability"],
    "troubleshooting": ["error_handling", "observability"],
    "configuration": ["configuration"],
    "change_impact": ["references", "api_surface"],
    "glossary": ["persistence", "api_surface"],
    "local_development": ["deployment", "configuration"],
    "testing": ["testing"],
    "known_limitations": [],
}

# How an evidence bucket's match reads as a sentence. Keeps the mock prose from
# being fourteen copies of one line, and — more usefully — makes each claim
# name the concrete artifact it cites, which is what citation_coverage.py's
# missing-tag heuristic looks for.
BUCKET_PHRASING = {
    "api_surface": "`{file}` contributes to the HTTP API surface (`{match}`)",
    "outbound_clients": "`{file}` calls out to another service (`{match}`)",
    "messaging": "`{file}` participates in asynchronous messaging (`{match}`)",
    "persistence": "`{file}` maps application state to storage (`{match}`)",
    "raw_queries": "`{file}` issues a hand-written query (`{match}`)",
    "security": "`{file}` carries an access-control annotation (`{match}`)",
    "configuration": "`{file}` supplies externalized configuration (`{match}`)",
    "error_handling": "`{file}` handles or translates errors (`{match}`)",
    "observability": "`{file}` emits operational signal (`{match}`)",
    "deployment": "`{file}` is part of how this service is built or deployed (`{match}`)",
    "testing": "`{file}` is exercised by the test suite (`{match}`)",
    "references": "`{file}` depends on another file in this repo (`{match}`)",
}

SPRING_ROLE_BY_BUCKET = {
    "api_surface": "controller",
    "persistence": "repository",
    "raw_queries": "repository",
    "security": "security",
    "configuration": "config",
    "messaging": "messaging-producer",
    "testing": "test",
}

_FALLBACK_CITATION_BUCKETS = (
    "api_surface",
    "security",
    "persistence",
    "configuration",
    "deployment",
    "observability",
    "references",
)

_ARCHITECTURE_BUCKETS = (
    "api_surface",
    "security",
    "persistence",
    "raw_queries",
    "messaging",
    "outbound_clients",
)
