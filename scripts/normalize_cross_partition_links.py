#!/usr/bin/env python3
"""Rewrite stale cross-partition anchor links in the published docs.

When a comprehensive source guide is partitioned into atomic files, its internal
cross-references — written as same-page anchors like `[Source Plugins](#source-plugins)`
— become broken: the target section now lives in a SIBLING file, so the `#anchor`
points at an id that no longer exists on the page. `mkdocs build --strict` aborts
on these. This script repoints such links at the sibling file that actually owns
the heading.

Matching is separator-insensitive (compares lowercased alphanumeric "cores") so it
survives the slug drift between the hand-authored link (`#best-practices--anti-patterns`)
and the real heading ("Best Practices & Anti-Patterns") and filename
(`best-practices-and-anti-patterns.md`). Heading parsing and link rewriting are both
fence-aware, so `#anchor`-looking text and `# comment` lines inside code blocks are
left untouched.

A link is rewritten only when:
  - its anchor does NOT resolve to a heading on its own page, AND
  - exactly one sibling file in the same directory owns a heading with that core.
Ambiguous or unresolved anchors are reported and left as-is (never guessed).

Idempotent. Run as an authoring/post-partition step (e.g. inside /create-guide,
after the partitioner) so corrected links are committed to docs/.

Usage:
    python scripts/normalize_cross_partition_links.py [--dry-run] [--topic drupal/ui-patterns]
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"

FENCE_RE = re.compile(r"^(\s*)(```+|~~~+)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
# A pure same-page anchor link: ](#slug) — optionally with a "title".
ANCHOR_LINK_RE = re.compile(r"\]\(#([A-Za-z0-9][\w-]*)\s*(\"[^\"]*\")?\)")


def core(text: str) -> str:
    """Separator-insensitive identity: lowercased alphanumerics only."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def mkdocs_slug(text: str) -> str:
    """Replicate python-markdown's default slugify (toc extension)."""
    value = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


def iter_content_lines(text: str):
    """Yield (line, in_fence) for each line, tracking code-fence state."""
    in_fence = False
    fence_marker = ""
    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\n")
        m = FENCE_RE.match(stripped)
        if m:
            marker = m.group(2)
            if not in_fence:
                in_fence = True
                fence_marker = marker[0] * 3  # ``` or ~~~
            elif marker[0] * 3 == fence_marker:
                in_fence = False
                fence_marker = ""
            yield line, True  # the fence line itself is "in fence"
            continue
        yield line, in_fence


def parse_headings(text: str):
    """Return list of (core, mkdocs_slug, is_first) for headings outside fences."""
    headings = []
    first = True
    for line, in_fence in iter_content_lines(text):
        if in_fence:
            continue
        m = HEADING_RE.match(line.rstrip("\n"))
        if m:
            title = m.group(2).strip()
            if not title:
                continue
            headings.append((core(title), mkdocs_slug(title), first))
            first = False
    return headings


def build_dir_index(md_files: list[Path]) -> dict:
    """Map heading-core -> list of (filename, mkdocs_slug, is_first) across siblings."""
    index: dict[str, list] = {}
    for path in md_files:
        for c, slug, is_first in parse_headings(path.read_text(encoding="utf-8")):
            index.setdefault(c, []).append((path.name, slug, is_first))
    return index


def rewrite_file(path: Path, dir_index: dict, own_cores: set, dry_run: bool):
    """Rewrite cross-partition anchors in one file. Returns (changes, unresolved)."""
    text = path.read_text(encoding="utf-8")
    changes: list[tuple[str, str]] = []
    unresolved: list[str] = []
    out_lines = []

    for line, in_fence in iter_content_lines(text):
        if in_fence:
            out_lines.append(line)
            continue

        def repl(m: re.Match) -> str:
            anchor = m.group(1)
            title = m.group(2) or ""
            c = core(anchor)
            if c in own_cores:
                return m.group(0)  # valid same-page anchor
            targets = dir_index.get(c, [])
            # Don't repoint to a heading that lives in THIS file only.
            external = [t for t in targets if t[0] != path.name]
            if len(external) == 1:
                fname, slug, is_first = external[0]
                new_target = fname if is_first else f"{fname}#{slug}"
                suffix = f" {title}" if title else ""
                changes.append((f"#{anchor}", new_target))
                return f"]({new_target}{suffix})"
            if not external:
                unresolved.append(f"#{anchor} (no sibling owns it)")
            else:
                unresolved.append(f"#{anchor} (ambiguous: {[t[0] for t in external]})")
            return m.group(0)

        out_lines.append(ANCHOR_LINK_RE.sub(repl, line))

    if changes and not dry_run:
        path.write_text("".join(out_lines), encoding="utf-8")
    return changes, unresolved


def process_dir(dir_path: Path, dry_run: bool):
    md_files = sorted(p for p in dir_path.glob("*.md"))
    if len(md_files) < 2:
        return 0, 0
    dir_index = build_dir_index(md_files)
    total_changes = 0
    total_unresolved = 0
    for path in md_files:
        own_cores = {c for c, _, _ in parse_headings(path.read_text(encoding="utf-8"))}
        changes, unresolved = rewrite_file(path, dir_index, own_cores, dry_run)
        if changes:
            total_changes += len(changes)
            verb = "would rewrite" if dry_run else "rewrote"
            print(f"  {verb} {len(changes)} in {path.relative_to(PROJECT_ROOT)}:")
            for old, new in changes:
                print(f"      {old} -> {new}")
        if unresolved:
            total_unresolved += len(unresolved)
            print(f"  UNRESOLVED in {path.relative_to(PROJECT_ROOT)}:")
            for u in unresolved:
                print(f"      {u}")
    return total_changes, total_unresolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report, don't write")
    parser.add_argument("--topic", help="Only this topic dir (e.g. drupal/ui-patterns)")
    args = parser.parse_args()

    if args.topic:
        dirs = [DOCS_DIR / args.topic]
    else:
        dirs = sorted({p.parent for p in DOCS_DIR.rglob("*.md")})

    changed = unresolved = 0
    for d in dirs:
        if not d.is_dir():
            print(f"  WARNING: {d} not found", file=sys.stderr)
            continue
        c, u = process_dir(d, args.dry_run)
        changed += c
        unresolved += u

    print(f"\n{'Would rewrite' if args.dry_run else 'Rewrote'} {changed} link(s); "
          f"{unresolved} unresolved.")
    return 0


if __name__ == "__main__":
    main()
