"""Pure adaptive grouping with overlap (ArchAgent-style token budgets)."""

from __future__ import annotations

import math


def _should_skip_carry_candidate(
    relpath: str,
    tokens: int,
    *,
    carried: int,
    overlap_budget: float,
    max_tokens: int,
    carried_in_paths,
) -> str | None:
    """Return 'break', 'continue', or None to accept the candidate."""
    if carried >= overlap_budget:
        return "break"
    if relpath in carried_in_paths:
        return "continue"
    if carried + tokens >= max_tokens:
        return "break"
    return None


def _carry_forward_overlap(closed_group, closed_tokens, overlap_ratio, max_tokens, carried_in_paths=frozenset()):
    """Build ~overlap_ratio worth of trailing tokens from a just-closed
    group to seed the next one. Files that entered the closed group only
    via overlap from the prior group are not re-carried — that prevents
    overlap cascading into three or more consecutive groups."""
    overlap_budget = closed_tokens * overlap_ratio
    carry, carried = [], 0
    for relpath, tokens in reversed(closed_group):
        decision = _should_skip_carry_candidate(
            relpath,
            tokens,
            carried=carried,
            overlap_budget=overlap_budget,
            max_tokens=max_tokens,
            carried_in_paths=carried_in_paths,
        )
        if decision == "break":
            break
        if decision == "continue":
            continue
        carry.append((relpath, tokens))
        carried += tokens
    carry.reverse()
    return carry, carried


def _should_close_group(
    current,
    current_tokens,
    candidate_tokens,
    *,
    is_last_group_being_filled: bool,
    max_tokens: int,
    target_per_group: float,
) -> bool:
    would_exceed_hard_cap = bool(current) and (current_tokens + candidate_tokens > max_tokens)
    would_exceed_soft_target = (
        bool(current)
        and not is_last_group_being_filled
        and current_tokens >= target_per_group
    )
    return would_exceed_hard_cap or would_exceed_soft_target


def _guard_zero_progress_carry(
    carry,
    carried,
    current_tokens,
    candidate_tokens,
    *,
    groups_closed_so_far: int,
    num_groups: int,
    max_tokens: int,
    target_per_group: float,
):
    """Clear carry when it would re-trigger the same close decision forever."""
    if carried != current_tokens:
        return carry, carried
    re_triggers_hard_cap = carried + candidate_tokens > max_tokens
    re_triggers_soft_target = (
        groups_closed_so_far != num_groups - 1 and carried >= target_per_group
    )
    if re_triggers_hard_cap or re_triggers_soft_target:
        return [], 0
    return carry, carried


def _close_group_and_seed_next(
    groups,
    current,
    current_tokens,
    candidate_tokens,
    *,
    overlap_ratio,
    max_tokens,
    carried_in_paths,
    num_groups,
    target_per_group,
):
    groups.append(current)
    carry, carried = _carry_forward_overlap(
        current, current_tokens, overlap_ratio, max_tokens, carried_in_paths,
    )
    carry, carried = _guard_zero_progress_carry(
        carry,
        carried,
        current_tokens,
        candidate_tokens,
        groups_closed_so_far=len(groups),
        num_groups=num_groups,
        max_tokens=max_tokens,
        target_per_group=target_per_group,
    )
    return list(carry), carried, frozenset(path for path, _ in carry)


def _step_group_assignment(
    file_tokens,
    index,
    *,
    groups,
    current,
    current_tokens,
    carried_in_paths,
    num_groups,
    max_tokens,
    overlap_ratio,
    target_per_group,
):
    """Advance one file into the current group, or close and re-evaluate."""
    relpath, tokens = file_tokens[index]
    is_last_group_being_filled = len(groups) == num_groups - 1
    if _should_close_group(
        current,
        current_tokens,
        tokens,
        is_last_group_being_filled=is_last_group_being_filled,
        max_tokens=max_tokens,
        target_per_group=target_per_group,
    ):
        current, current_tokens, carried_in_paths = _close_group_and_seed_next(
            groups,
            current,
            current_tokens,
            tokens,
            overlap_ratio=overlap_ratio,
            max_tokens=max_tokens,
            carried_in_paths=carried_in_paths,
            num_groups=num_groups,
            target_per_group=target_per_group,
        )
        return index, current, current_tokens, carried_in_paths
    current.append((relpath, tokens))
    return index + 1, current, current_tokens + tokens, carried_in_paths


def build_groups(file_tokens, max_tokens, overlap_ratio):
    """file_tokens: list of (relpath, tokens) in DFS order.
    Returns list of groups: each a list of (relpath, tokens).

    Check-before-append ("strict"): a candidate file is only added to the
    current group if doing so would not exceed max_tokens (unless the
    current group is still empty, in which case the file is added
    regardless — a single file larger than max_tokens has nowhere else to
    go; groups are atomic at the file level, so "a group containing that
    file is at least that file's size" is an unavoidable floor, not a bug).
    This bounds every group's total to at most max_tokens, except a group
    forced to open with a single oversized file — versus the previous
    check-after-append behavior's max_tokens + (whatever file closed the
    group) bound. Verified by direct execution against five scenarios plus
    an overlap-duplication regression and a deliberate infinite-loop
    trigger case — see the module's accompanying handoff notes / commit
    message for the exact scenarios and output, so nobody has to re-derive
    this from scratch if it's questioned later.
    """
    total_tokens = sum(tokens for _, tokens in file_tokens)
    if total_tokens == 0 or not file_tokens:
        return []

    num_groups = max(1, math.ceil(total_tokens / max_tokens))
    target_per_group = total_tokens / num_groups

    groups = []
    current = []
    current_tokens = 0
    carried_in_paths: frozenset[str] = frozenset()
    index = 0
    file_count = len(file_tokens)

    while index < file_count:
        index, current, current_tokens, carried_in_paths = _step_group_assignment(
            file_tokens,
            index,
            groups=groups,
            current=current,
            current_tokens=current_tokens,
            carried_in_paths=carried_in_paths,
            num_groups=num_groups,
            max_tokens=max_tokens,
            overlap_ratio=overlap_ratio,
            target_per_group=target_per_group,
        )

    if current:
        groups.append(current)

    return groups

