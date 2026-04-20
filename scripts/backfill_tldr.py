#!/usr/bin/env python3
"""Backfill `tldr:` frontmatter field across all atomic guides.

Extracts a 1-2 sentence summary from each guide's "When to Use" blockquote
plus its primary pattern indicator, and writes it to frontmatter.

Idempotent: skips guides that already have `tldr:` set.

Usage:
    python scripts/backfill_tldr.py [--dry-run] [--topic drupal/plus-suite]
"""

import argparse
import re
import sys
from pathlib import Path
from textwrap import shorten

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"

# Skip non-guide files (maintenance artifacts, planning docs, etc.)
SKIP_NAMES = {
    "sources-maintenance.md",
    "code-reference-map.md",
    "conclusion.md",
}
SKIP_DIRS = {"plans"}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
# Matches "When to Use", "When to Use This Section", or "When to Use This Guide":
#   ## When to Use\n\n> Some text...
#   ### When to Use This Section\n- bullet\n- bullet
# Stops at the next heading or double blank line.
WHEN_TO_USE_RE = re.compile(
    r"#{2,4}\s+When to Use(?:\s+This\s+(?:Section|Guide))?\s*\n+"
    r"(?:>\s*)?"                # optional blockquote marker
    r"(.+?)"
    r"(?=\n\n#{1,4}\s|\n\Z|\Z)",  # until next heading or EOF
    re.DOTALL | re.IGNORECASE,
)


def parse_frontmatter(content: str):
    """Return (frontmatter_text, body, has_frontmatter)."""
    m = FRONTMATTER_RE.match(content)
    if not m:
        return "", content, False
    return m.group(1), content[m.end():], True


def frontmatter_has_field(fm_text: str, field: str) -> bool:
    """Check if frontmatter already defines a field."""
    pattern = rf"^{re.escape(field)}\s*:"
    return bool(re.search(pattern, fm_text, re.MULTILINE))


def extract_description(fm_text: str) -> str:
    """Extract the description: value from frontmatter."""
    m = re.search(r"^description\s*:\s*(.+?)$", fm_text, re.MULTILINE)
    if not m:
        return ""
    val = m.group(1).strip()
    # Strip optional surrounding quotes.
    if (val.startswith('"') and val.endswith('"')) or (
        val.startswith("'") and val.endswith("'")
    ):
        val = val[1:-1]
    return val.strip()


def extract_when_to_use(body: str) -> str:
    """Pull the 'When to Use' text (blockquote, paragraph, or bullet list)."""
    m = WHEN_TO_USE_RE.search(body)
    if not m:
        return ""
    text = m.group(1).strip()
    # Strip blockquote continuation markers.
    text = re.sub(r"\n>\s*", " ", text)
    # Stop at the first double newline (end of first paragraph/list).
    text = text.split("\n\n")[0]
    # Strip leading bullet markers on each line ("- ", "* ", numbered).
    text = re.sub(r"^\s*(?:[-*•]|\d+\.)\s+", "", text, flags=re.MULTILINE)
    # Collapse all whitespace.
    text = re.sub(r"\s+", " ", text).strip()
    # Trim trailing artifacts.
    text = text.rstrip(" -—•")
    return text


def compose_tldr(when_to_use: str, max_chars: int = 240) -> str:
    """Produce a 1-2 sentence tldr from the 'When to Use' text.

    Strategy: take the first 1-2 sentences. If shorter than budget,
    keep as-is. If longer, truncate at sentence boundary.
    """
    if not when_to_use:
        return ""

    # Split into sentences (naive but good enough).
    sentences = re.split(r"(?<=[.!?])\s+", when_to_use)
    if not sentences:
        return ""

    # Take up to 2 sentences.
    candidate = " ".join(sentences[:2]).strip()

    # Trim trailing markdown-ish artifacts like bullet dashes.
    candidate = candidate.rstrip(" -—")

    if len(candidate) <= max_chars:
        return candidate

    # Too long — use shorten with word boundary.
    return shorten(candidate, width=max_chars, placeholder="…")


def inject_tldr(fm_text: str, tldr: str) -> str:
    """Insert `tldr: "<text>"` into frontmatter after `description:` if present,
    else at the top. Escapes any embedded double quotes.
    """
    escaped = tldr.replace("\\", "\\\\").replace('"', '\\"')
    new_line = f'tldr: "{escaped}"'

    # Try to place after `description:` line (common convention).
    desc_pattern = re.compile(r"^(description\s*:.*)$", re.MULTILINE)
    m = desc_pattern.search(fm_text)
    if m:
        return fm_text[: m.end()] + "\n" + new_line + fm_text[m.end():]

    # Otherwise prepend.
    return new_line + "\n" + fm_text


def looks_like_table_or_code(text: str) -> bool:
    """Detect content that's clearly markdown table or code — not a prose summary."""
    # Markdown table separators.
    if "|---" in text or "| ---" in text:
        return True
    # Many pipe characters → table row.
    if text.count("|") >= 3:
        return True
    # Starts with table cell.
    if text.lstrip().startswith("|"):
        return True
    return False


def process_file(path: Path, dry_run: bool = False) -> str:
    """Process one guide file. Returns status string."""
    content = path.read_text(encoding="utf-8")
    fm_text, body, has_fm = parse_frontmatter(content)

    # If no frontmatter, the body is the entire file.
    if not has_fm:
        body = content
        fm_text = ""

    if has_fm and frontmatter_has_field(fm_text, "tldr"):
        return "already-has-tldr"

    # Primary source: "When to Use" section. Reject if it's a markdown table
    # or code block (happens when the section opens with a decision table).
    when_to_use = extract_when_to_use(body)
    if when_to_use and looks_like_table_or_code(when_to_use):
        when_to_use = ""  # force fallback

    # Fallback: description: from frontmatter.
    if not when_to_use and has_fm:
        when_to_use = extract_description(fm_text)

    if not when_to_use:
        return "no-source"

    tldr = compose_tldr(when_to_use)
    if not tldr:
        return "empty-tldr"

    new_fm = inject_tldr(fm_text, tldr)
    new_content = f"---\n{new_fm}\n---\n{body}"

    if dry_run:
        prefix = "would-create-fm" if not has_fm else "would-write"
        return f"{prefix}: {tldr[:80]}"

    path.write_text(new_content, encoding="utf-8")
    prefix = "created-fm" if not has_fm else "wrote"
    return f"{prefix}: {tldr[:80]}"


def main():
    parser = argparse.ArgumentParser(description="Backfill tldr: across guides")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files")
    parser.add_argument(
        "--topic",
        help="Only process this topic (e.g., drupal/plus-suite)",
    )
    parser.add_argument(
        "--sample",
        type=int,
        help="Print N sample tldr values (with --dry-run)",
    )
    args = parser.parse_args()

    if args.topic:
        target = DOCS_DIR / args.topic
        if not target.is_dir():
            print(f"ERROR: topic not found: {target}", file=sys.stderr)
            sys.exit(1)
        files = sorted(target.rglob("*.md"))
    else:
        files = sorted(DOCS_DIR.rglob("*.md"))

    # Exclude topic index.md files — those have guide-meta, not atomic guides.
    files = [f for f in files if f.name != "index.md"]
    # Exclude maintenance artifacts and planning docs.
    files = [
        f for f in files
        if f.name not in SKIP_NAMES
        and not any(part in SKIP_DIRS for part in f.parts)
    ]

    counts = {}
    samples = []

    for f in files:
        result = process_file(f, dry_run=args.dry_run)
        # Bucket the status (strip the sample text after ": ").
        bucket = result.split(":")[0]
        counts[bucket] = counts.get(bucket, 0) + 1
        if args.sample and len(samples) < args.sample and bucket.startswith(
            ("wrote", "would-write", "created-fm", "would-create-fm")
        ):
            samples.append((f.relative_to(PROJECT_ROOT), result))

    print("\nSummary:")
    for k, v in counts.items():
        if v:
            print(f"  {k}: {v}")
    print(f"  total processed: {len(files)}")

    if samples:
        print("\nSamples:")
        for path, result in samples:
            print(f"  {path}")
            print(f"    {result}")


if __name__ == "__main__":
    main()
