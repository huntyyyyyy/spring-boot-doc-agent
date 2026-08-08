"""Incident-seeded gate-mutator definitions (catalog only; not the harness).

Standing rule: new entries must name a real near-miss / incident class
(check F, rule-form loss, size ratchet, network deny, derived-count drift,
…). Refuse “add ROR because PIT has it.” See CONTRIBUTING.md
“Mutation-scope taxonomies” and “Incident-seeded gate mutators only.”

Loaded by ``mutator_registry.load_registry``; ``mutate.py`` does not own this
list. Formatting perturbations and assertion-engine mutants stay elsewhere.
"""
from __future__ import annotations

from mutator import Mutator


def definitions() -> tuple[Mutator, ...]:
    """Closed catalog of gate mutators. Extend only with an incident seed."""
    return (
        # --- structural: located by ast-grep, immune to reformatting ---------
        Mutator(
            "secret-heuristic-stops-unquoting",
            "src/doc_engine/scanning/support/_secret_heuristics.py", "python",
            "PLACEHOLDER_VALUE_RE.match(_unquote($V))",
            "PLACEHOLDER_VALUE_RE.match($V)",
            "test_secret_heuristics.py",
            'quoted "${X}" was reported as a literal credential on a real '
            "build script"),
        Mutator(
            "build-file-guard-loosened",
            "src/doc_engine/scanning/_scanner_filesystem.py", "python",
            'name.endswith(".gradle.kts")', 'ext == ".kts"',
            "test_spring_signal_scan.py",
            "a bare .kts is any Kotlin script; treating it as a build file puts "
            "arbitrary Kotlin into operations.md"),
        Mutator(
            "relation-permits-everything", "scripts/ratchets/set_delta.py",
            "python",
            "return lambda member, direction: False",
            "return lambda member, direction: True",
            "test_set_delta.py",
            "a relation that permits everything makes every metamorphic "
            "assertion pass while checking nothing"),
        Mutator(
            "query-limit-ceiling-removed",
            "src/doc_engine/query/envelope.py", "python",
            "cap = max(0, min(cap, max_limit))",
            "cap = max(0, cap)",
            "test_query_artifacts.py",
            "agents rely on hard --limit clamp; removing it dumps unbounded "
            "evidence into context (DDIA backpressure)"),
        Mutator(
            "context-packet-budget-trim-disabled",
            "src/doc_engine/query/rank.py", "python",
            "tokens_used + cost <= budget",
            "True",
            "test_context_packet.py",
            "context_packet budgetTokens must trim primaryContext; disabling "
            "the guard dumps unbounded packets"),
        Mutator(
            "freshness-mismatch-always-fresh",
            "src/doc_engine/query/freshness.py", "python",
            "return (FreshnessLabel.FRESH_INDEXED if actual == expected "
            "else FreshnessLabel.STALE)",
            "return FreshnessLabel.FRESH_INDEXED",
            "test_context_packet.py",
            "signature mismatch must label stale; always-fresh hides drift"),

        # --- literal: see Mutator's docstring for why each cannot be ---------
        # --- structural, and RegistryAnchorsTest for what guards them --------
        Mutator(
            "agent-regains-grep", "adapters/claude/agents/gap-analyzer.md", "",
            "tools: Read, Glob, Write", "tools: Read, Grep, Glob, Write",
            "test_check_repo_claims.py",
            "all five agents declared Grep until 0ee4033; check F exists to "
            "stop it coming back"),
        Mutator(
            "rule-loses-its-args-form",
            "src/doc_engine/scanning/resources/spring_ast_grep_rules.yml", "",
            '    - pattern: "@JoinColumn($$$ARGS)"\n', "",
            "test_rule_coverage.py",
            "a marker pattern and an argument-bearing one are disjoint node "
            "shapes; dropping one silently halves a rule"),
        Mutator(
            "derived-count-edited", "CLAUDE.md", "",
            "<!-- derived: predicate_count -->7<!-- /derived -->",
            "<!-- derived: predicate_count -->6<!-- /derived -->",
            "test_check_repo_claims.py",
            'CLAUDE.md read "Three forms" for two windows after a fourth and '
            "fifth landed"),
        Mutator(
            "prompt-contract-drifts",
            "adapters/claude/agents/file-summarizer.md", "",
            "test, other —", "test, other, scheduler —",
            "test_prompt_contracts.py",
            "the validators held hand-copied duplicates of this list with "
            "nothing reading them back"),
    )
