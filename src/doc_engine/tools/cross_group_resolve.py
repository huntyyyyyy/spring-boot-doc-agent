"""Parse package/import reference rows for cross-group edge join."""

from __future__ import annotations

import collections
import re
from typing import Dict, List, Set, Tuple

PACKAGE_RE = re.compile(r"^package\s+([\w.]+)\s*;")
IMPORT_RE = re.compile(r"^import\s+(static\s+)?([\w.*]+)\s*;")


def type_stem_from_path(path: str) -> str:
    return path.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0]


def index_package_declaration(
    path: str,
    package_name: str,
    decl_files: Dict[str, Set[str]],
    stem_index: Dict[Tuple[str, str], str],
) -> None:
    decl_files[package_name].add(path)
    stem_index[(package_name, type_stem_from_path(path))] = path


def ingest_reference_row(
    row: dict,
    decl_files: Dict[str, Set[str]],
    stem_index: Dict[Tuple[str, str], str],
    imports: Dict[str, List[Tuple[str, bool]]],
) -> None:
    path = row.get("file")
    text = (row.get("match") or "").strip()
    if not path:
        return
    package_match = PACKAGE_RE.match(text)
    if package_match:
        index_package_declaration(
            path, package_match.group(1), decl_files, stem_index
        )
        return
    import_match = IMPORT_RE.match(text)
    if import_match:
        imports[path].append(
            (import_match.group(2), bool(import_match.group(1)))
        )


def parse_references(references: List[dict]):
    """Split the `references` bucket into the two indexes the join needs.

    Returns (decl_files, stem_index, imports):
      decl_files[package]        -> set of files declaring it
      stem_index[(package, Type)]-> the file whose name is Type.java
      imports[file]              -> list of (qualified_name, is_static)
    """
    decl_files: Dict[str, Set[str]] = collections.defaultdict(set)
    stem_index: Dict[Tuple[str, str], str] = {}
    imports: Dict[str, List[Tuple[str, bool]]] = collections.defaultdict(list)
    for row in references:
        ingest_reference_row(row, decl_files, stem_index, imports)
    return decl_files, stem_index, imports


def resolve_wildcard_import(qualified: str, decl_files) -> Tuple[List[str], str]:
    package_name = qualified[:-2]
    targets = sorted(decl_files.get(package_name, ()))
    return targets, ("package-fanout" if targets else "unresolved")


def resolve_type_import(qualified: str, decl_files, stem_index) -> Tuple[List[str], str]:
    name = qualified
    while "." in name:
        package_name, stem = name.rsplit(".", 1)
        hit = stem_index.get((package_name, stem))
        if hit is not None:
            return [hit], "exact"
        if package_name in decl_files:
            return sorted(decl_files[package_name]), "package-fanout"
        name = package_name  # shorten and retry: static member / nested class
    return [], "unresolved"


def resolve_targets(qualified: str, decl_files, stem_index) -> Tuple[List[str], str]:
    """Resolve one imported qualified name to the file(s) that declare it.

    Returns (target_files, confidence) where confidence is one of:
      "exact"           — resolved to a single declaring file by type name
      "package-fanout"  — resolved only to a package; every file in it is a
                          candidate (wildcard imports, or a type whose file
                          name doesn't match the type name)
      "unresolved"      — nothing in this repo declares it (third-party)

    Static-member and nested-class imports are handled by shortening the
    name one component at a time: `import static com.x.Foo.BAR` first tries
    (com.x.Foo, BAR), fails, then tries (com.x, Foo) and resolves. Without
    this loop those imports resolve to nothing and vanish silently, which is
    the single easiest way to under-report the cut.
    """
    if qualified.endswith(".*"):
        return resolve_wildcard_import(qualified, decl_files)
    return resolve_type_import(qualified, decl_files, stem_index)


def build_membership(groups: List[dict]) -> Dict[str, Set[int]]:
    """file -> set of group ids. A set, not a scalar: the grouping is a
    cover with ~10% overlap, so a file can legitimately belong to two."""
    memb: Dict[str, Set[int]] = collections.defaultdict(set)
    for group in groups:
        for path in group["files"]:
            memb[path].add(group["id"])
    return memb


def is_cut(memb: Dict[str, Set[int]], u: str, v: str) -> bool:
    """True iff no single group contains both endpoints — the correct
    predicate for a cover. `owner(u) != owner(v)` is not well defined."""
    return not (memb.get(u, set()) & memb.get(v, set()))
