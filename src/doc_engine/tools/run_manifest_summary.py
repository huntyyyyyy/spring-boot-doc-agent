"""Human-readable summary formatting for run_manifest."""

from __future__ import annotations


def _format_stage_line(stage):
    dur = stage.get("duration_ms")
    dur_str = f"{dur / 1000:.1f}s" if dur is not None else "?"
    fanout_str = (
        f", fanout={stage['actual_fanout']}"
        if stage.get("actual_fanout") is not None
        else ""
    )
    error_str = f" — {stage['error']}" if stage.get("error") else ""
    return f"  - {stage['name']}: {stage['status']} ({dur_str}{fanout_str}){error_str}"


def _format_tag_totals(tag_counts):
    totals = {"Evidenced": 0, "Confirmed": 0, "Unknown": 0, "PerExistingDocs": 0}
    for counts in tag_counts.values():
        for key in totals:
            totals[key] += counts.get(key, 0)
    return (
        f"  evidence tags across {len(tag_counts)} file(s): "
        f"Evidenced={totals['Evidenced']}, Confirmed={totals['Confirmed']}, "
        f"Unknown={totals['Unknown']}, PerExistingDocs={totals['PerExistingDocs']}"
    )


def _fanout_compare_line(stage_name, predicted, stages):
    actual = sum(
        s.get("actual_fanout") or 0 for s in stages if s["name"] == stage_name
    )
    return f"  fanout[{stage_name}]: predicted={predicted}, actual={actual}"


def _format_preflight_lines(preflight, stages):
    lines = []
    unmapped = preflight["unmapped_preflight_keys"]
    if unmapped:
        lines.append(
            f"  capacity_preflight: {len(unmapped)} unmapped stage key(s): {unmapped}"
        )
    predicted = preflight["predicted_fanout_by_manifest_stage"]
    lines.extend(
        _fanout_compare_line(name, value, stages) for name, value in predicted.items()
    )
    return lines


def _summary_timestamp_line(manifest):
    ts_start, ts_end = manifest.get("timestamp_start"), manifest.get("timestamp_end")
    if not (ts_start and ts_end):
        return None
    return f"  total: {ts_start} -> {ts_end}"


def _summary_interview_line(interview):
    if not interview:
        return None
    return (
        f"  interview: asked={interview['asked']} answered={interview['answered']} "
        f"skipped={interview['skipped']}"
    )


def _summary_optional_sections(manifest, stages):
    """Build optional summary lines (timestamps, tags, interview, preflight)."""
    lines = []
    ts_line = _summary_timestamp_line(manifest)
    if ts_line:
        lines.append(ts_line)
    tag_counts = manifest.get("evidence_tag_counts") or {}
    if tag_counts:
        lines.append(_format_tag_totals(tag_counts))
    interview_line = _summary_interview_line(manifest.get("interview"))
    if interview_line:
        lines.append(interview_line)
    preflight = manifest.get("capacity_preflight")
    if preflight:
        lines.extend(_format_preflight_lines(preflight, stages))
    return lines


def format_summary(manifest):
    stages = manifest.get("stages", [])
    lines = [
        f"run_manifest: run_id={manifest.get('run_id')} status={manifest.get('status')}"
    ]
    lines.extend(_format_stage_line(s) for s in stages)
    lines.extend(_summary_optional_sections(manifest, stages))
    return "\n".join(lines)
