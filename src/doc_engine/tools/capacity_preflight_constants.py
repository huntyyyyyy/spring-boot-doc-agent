"""Constants for capacity preflight Stage-0 / L2b reports."""

from __future__ import annotations

from doc_engine.tools.doc_tag_utils import VALID_DOC_FILES

STAGE3_FIXED_FANOUT = 1   # gap-analyzer, always exactly one dispatch
STAGE3_ARCH_TEST_REVIEW_FANOUT = 1  # software-architect-and-testing, always one
# SoR: taxonomy file set — not a magic literal that can drift from doc-writer.
STAGE4_FIXED_FANOUT = len(VALID_DOC_FILES)

# Wire version for capacity_preflight_report.json (slice-5 thin operator schema).
# Bump only on breaking changes; additive fields keep the same version per
# rel-schema-outlives-writers. Stamped on both Stage-0 compute_preflight and
# L2b compute_stage4_calibration return paths.
CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION = 1

# Pipeline SoR: doc_writer input_artifacts in doc_engine.pipeline.stages —
# what Stage-4 actually receives once those artifacts exist. Stage-0 proxy
# can only include a subset.
STAGE4_PROXY_INCLUDED = (
    "group_est_tokens_proxy_for_summaries",
    "spring_signals_optional",
)
STAGE4_PROXY_OMITTED = (
    "interview_answers",
    "architecture_merge_beyond_summary_proxy",
    "stage4_return_payloads",
)

# L2b measured mode: SoR = on-disk Stage-4 inputs. Returns stay omitted.
STAGE4_MEASURED_ALWAYS_OMITTED = (
    "stage4_return_payloads",
)
