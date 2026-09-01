#!/usr/bin/env python3
"""Add a Summary column to each topic's index.md routing table.

For each topic index.md:
1. Find the "I need to... | Guide" Markdown table
2. For each row, resolve the target guide .md link
3. Read that guide's `tldr:` frontmatter
4. Rewrite the table as "I need to... | Guide | Summary"

Idempotent: if the table already has 3+ columns, skip.

Usage:
    python scripts/add_tldr_to_routing_tables.py [--dry-run] [--topic drupal/plus-suite]
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"

# Match the routing table header (2 or 3 columns). Variants observed:
#   | I need to... | Guide |
#   | Task         | Guide |
#   | Goal         | Go To |
#   | I need to... | Guide | Summary |   (already processed)
HEADER_RE = re.compile(
    r"^\|\s*(?:I need to\.\.\.|Task|Goal|When you need to\.\.\.|Topic)\s*"
    r"\|\s*(?:Guide|Go To|Link)\s*"
    r"(?:\|\s*Summary\s*)?"  # optional Summary column (already processed)
    r"\|\s*$",
    re.MULTILINE | re.IGNORECASE,
)

# Match a link like [Name](filename.md) or [Name](./filename.md)
LINK_RE = re.compile(r"\[([^\]]+)\]\(\.?\/?([a-z0-9\-_/]+\.md)\)", re.IGNORECASE)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def read_tldr(guide_path: Path) -> str:
    """Load `tldr:` from a guide's frontmatter. Returns empty string on failure."""
    if not guide_path.exists():
        return ""
    content = guide_path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(content)
    if not m:
        return ""
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return ""
    if not isinstance(fm, dict):
        return ""
    return str(fm.get("tldr", "")).strip()


def process_index(index_path: Path, dry_run: bool = False, refresh: bool = False) -> str:
    """Add a Summary column to the routing table in a topic's index.md.

    With refresh=True, a table that already has a Summary column is rewritten so
    every Summary cell is the target guide's `tldr:` verbatim. A hand-edited or
    paraphrased Summary drifts from the guide it describes and the navigator
    pre-filters on it, so a stale cell routes on text no guide actually says.
    """
    content = index_path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)

    # Find the routing table header.
    header_idx = None
    for i, line in enumerate(lines):
        if HEADER_RE.match(line.rstrip("\n")):
            header_idx = i
            break
    if header_idx is None:
        return "no-routing-table"

    # Separator line is header_idx + 1, rows start at header_idx + 2.
    if header_idx + 2 >= len(lines):
        return "malformed-table"

    separator_line = lines[header_idx + 1].rstrip("\n")
    # Count pipes in the separator — already 3 columns = already processed.
    col_count = separator_line.count("|") - 1  # leading/trailing pipes
    already = col_count >= 3
    if already and not refresh:
        return "already-has-summary"

    # Rebuild the header and separator.
    new_header = "| I need to... | Guide | Summary |\n"
    new_separator = "|-------------|-------|---------|\n"

    # Process rows.
    topic_dir = index_path.parent
    new_rows = []
    row_idx = header_idx + 2
    while row_idx < len(lines):
        row = lines[row_idx].rstrip("\n")
        # Blank line = end of table.
        if not row.strip():
            break
        # Non-table line = end of table.
        if not row.lstrip().startswith("|"):
            break
        # Must be a table row.
        match = LINK_RE.search(row)
        if not match:
            # Row without a link — append as-is with empty summary column.
            new_rows.append(row.rstrip(" |") + " | |\n")
            row_idx += 1
            continue

        link_path = match.group(2)
        guide_path = topic_dir / link_path
        tldr = read_tldr(guide_path)
        # Escape pipe chars in tldr for table safety.
        tldr_safe = tldr.replace("|", "\\|")

        # Insert the Summary column just before the trailing pipe. When refreshing an
        # already-3-column table, drop the existing Summary cell first so the value is
        # replaced rather than appended as a fourth column.
        new_row = row.rstrip()
        if already:
            # Split on UNESCAPED pipes only. A routing row legitimately contains `\|`
            # inside a cell (Twig filter names such as `\|t`, `\|without`); splitting on
            # those would tear the row apart and drop its guide link.
            cells = re.split(r"(?<!\\)\|", new_row.strip().strip("|"))
            if len(cells) >= 3:
                new_row = "|" + "|".join(cells[:2]) + "|"
        if new_row.endswith("|"):
            new_row = new_row[:-1].rstrip() + f" | {tldr_safe} |\n"
        else:
            new_row = new_row + f" | {tldr_safe} |\n"
        new_rows.append(new_row)
        row_idx += 1

    # Reassemble the file.
    new_lines = (
        lines[: header_idx]
        + [new_header, new_separator]
        + new_rows
        + lines[row_idx:]
    )
    new_content = "".join(new_lines)

    if new_content == content:
        return "no-change"

    if dry_run:
        return f"would-update: {len(new_rows)} rows"

    index_path.write_text(new_content, encoding="utf-8")
    return f"updated: {len(new_rows)} rows"


def main():
    parser = argparse.ArgumentParser(description="Add Summary column to routing tables")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files")
    parser.add_argument(
        "--topic", help="Only process this topic (e.g., drupal/plus-suite)"
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Also rewrite tables that already have a Summary column, restoring each "
        "cell to the target guide's tldr verbatim",
    )
    args = parser.parse_args()

    if args.topic:
        targets = [DOCS_DIR / args.topic / "index.md"]
    else:
        # All topic index.md files (2 levels deep: docs/<category>/<topic>/index.md)
        targets = sorted(DOCS_DIR.glob("*/*/index.md"))

    counts = {}
    samples = []
    for index_path in targets:
        if not index_path.exists():
            continue
        result = process_index(index_path, dry_run=args.dry_run, refresh=args.refresh)
        bucket = result.split(":")[0]
        counts[bucket] = counts.get(bucket, 0) + 1
        if bucket in ("updated", "would-update") and len(samples) < 3:
            samples.append((index_path.relative_to(PROJECT_ROOT), result))

    print("Summary:")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    print(f"  total: {sum(counts.values())}")

    if samples:
        print("\nSample updates:")
        for path, result in samples:
            print(f"  {path} — {result}")


if __name__ == "__main__":
    main()
