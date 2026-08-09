"""Structural Mermaid syntax checks for semantic-eval mechanical pre-pass."""

from __future__ import annotations

import re

SUBGRAPH_RE = re.compile(r"^\s*subgraph\b", re.MULTILINE)
END_RE = re.compile(r"^\s*end\s*$", re.MULTILINE)

# A "declared" node: an identifier immediately followed by a label in one of
# Mermaid's three bracket shapes (A["Label"], A(Label), A{Label}).
NODE_DECL_RE = re.compile(r"\b([A-Za-z_]\w*)\s*(?:\[[^\]]*\]|\([^)]*\)|\{[^}]*\})")

# An edge: two identifiers joined by an arrow (-->, --, -.->,  ==>, etc.),
# each optionally immediately followed by its own label, with an optional
# |edge label| between the arrow and the target. Deliberately permissive
# (not a full grammar) — this only needs the two endpoint identifiers.
EDGE_RE = re.compile(
    r"\b([A-Za-z_]\w*)\s*(?:\[[^\]]*\]|\([^)]*\)|\{[^}]*\})?"
    r"\s*(?:--+>|--+|-\.+->?|==+>?)\s*(?:\|[^|]*\|\s*)?"
    r"([A-Za-z_]\w*)\b"
)


def find_undefined_node_refs(mermaid_text):
    """Every node in this pipeline's diagrams is supposed to carry a real
    file/class label (agents/architect-segment.md rule 3 forbids inventing a
    'friendlier' label, and forbids a bare/unlabeled node in the first
    place) — so an identifier that shows up as an edge endpoint but never
    receives a label anywhere in the diagram is not "implicitly a valid
    unlabeled node" the way it would be in Mermaid generally; for this
    project's diagrams specifically it's the signature of a truncated or
    malformed diagram (a node whose label-bearing declaration got cut off,
    or an architect-merge dedup that dropped a label during stitching).
    Returns the sorted list of such identifiers, empty if none."""
    declared = {m.group(1) for m in NODE_DECL_RE.finditer(mermaid_text)}
    referenced = set()
    for m in EDGE_RE.finditer(mermaid_text):
        referenced.add(m.group(1))
        referenced.add(m.group(2))
    return sorted(referenced - declared)


def bracket_balance_findings(mermaid_text):
    findings = []
    for open_c, close_c, label in (
        ("[", "]", "square_brackets"),
        ("(", ")", "parentheses"),
        ("{", "}", "braces"),
    ):
        opens, closes = mermaid_text.count(open_c), mermaid_text.count(close_c)
        if opens != closes:
            findings.append({
                "type": f"unbalanced_{label}",
                "detail": f"{opens} '{open_c}' vs {closes} '{close_c}'",
            })
    return findings


def subgraph_quote_findings(mermaid_text):
    findings = []
    subgraph_count = len(SUBGRAPH_RE.findall(mermaid_text))
    end_count = len(END_RE.findall(mermaid_text))
    if subgraph_count != end_count:
        findings.append({
            "type": "unbalanced_subgraph_end",
            "detail": f"{subgraph_count} 'subgraph' vs {end_count} 'end'",
        })
    quote_count = mermaid_text.count('"')
    if quote_count % 2 != 0:
        findings.append({
            "type": "unbalanced_quotes",
            "detail": f"{quote_count} double-quote characters (odd count)",
        })
    return findings


def check_mermaid_syntax(mermaid_text):
    """Structural (not a full grammar/renderer) checks: bracket/paren/brace
    balance, subgraph/end balance, double-quote balance, and undefined node
    references (find_undefined_node_refs). Sufficient to catch the failure
    class this exists for (a doc-writer or architect subagent emitting a
    truncated or malformed diagram) without adding a Mermaid-parsing
    dependency this project doesn't otherwise need."""
    findings = bracket_balance_findings(mermaid_text)
    findings.extend(subgraph_quote_findings(mermaid_text))
    undefined_refs = find_undefined_node_refs(mermaid_text)
    if undefined_refs:
        findings.append({
            "type": "undefined_node_ref",
            "detail": (
                "referenced in an edge but never labeled anywhere in the diagram: "
                f"{undefined_refs}"
            ),
        })
    return findings


def extract_mermaid_block(text):
    """Pulls the first fenced ```mermaid ... ``` block out of a markdown
    file. Returns None if there isn't one."""
    m = re.search(r"```mermaid\s*\n(.*?)```", text, re.DOTALL)
    return m.group(1) if m else None
