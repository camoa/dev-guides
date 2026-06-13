#!/usr/bin/env python3
"""Generate llms.txt index and llms.hash for dev-guides.

Reads partition-manifest.json, extracts topic metadata (title, description,
guide count), writes site/llms.txt index pointing to topic index pages,
and generates site/llms.hash for cache freshness.

Run after `mkdocs build` so site/ exists.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

SITE_BASE_URL = "https://camoa.github.io/dev-guides"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SITE_DIR = PROJECT_ROOT / "site"
MANIFEST_PATH = PROJECT_ROOT / "partition-manifest.json"
TEMPLATE_PATH = PROJECT_ROOT / "llms.txt.template"

# Category display names derived from topic key prefixes
CATEGORY_MAP = {
    "drupal": "Drupal",
    "css": "CSS",
    "js": "JavaScript",
    "media": "Media",
    "design-systems": "Design Systems",
    "nextjs": "Next.js",
    "development": "Development Practices",
    "ai-tooling": "AI Tooling",
    "decoupled": "Decoupled",
    "testing": "Testing",
    "performance": "Performance",
    "accessibility": "Accessibility",
}

# Preferred category display order. This is an ORDERING HINT, not a gate:
# categories not listed here are still emitted (appended alphabetically). Add a
# category here only to control where it appears.
CATEGORY_ORDER = [
    "Drupal",
    "CSS",
    "JavaScript",
    "Media",
    "Design Systems",
    "Next.js",
    "Development Practices",
    "Performance",
    "Accessibility",
    "AI Tooling",
    "Decoupled",
    "Testing",
]


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter delimited by --- from markdown content."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[end + 3:].lstrip("\n")
    return content


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter using yaml.safe_load."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            try:
                meta = yaml.safe_load(content[3:end])
                return meta if isinstance(meta, dict) else {}
            except yaml.YAMLError:
                return {}
    return {}


def extract_h1(content: str) -> str:
    """Extract the first H1 heading from markdown content."""
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_summary(content: str) -> str:
    """Extract a one-line summary from frontmatter description or first paragraph."""
    meta = extract_frontmatter(content)
    if meta.get("description"):
        return meta["description"]
    # Fall back to first non-empty line after H1
    stripped = strip_frontmatter(content)
    for line in stripped.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            # Clean markdown formatting
            line = re.sub(r"[>\|]", "", line).strip()
            if line:
                return line[:120]
    return ""



def get_category(key: str) -> str:
    """Get display category from topic key prefix.

    Falls back to a prettified prefix (e.g. 'web-components' -> 'Web Components')
    for categories not explicitly mapped, so new categories get a sane name.
    """
    prefix = key.split("/")[0]
    return CATEGORY_MAP.get(prefix, prefix.replace("-", " ").title())


def order_categories(present: list[str]) -> list[str]:
    """Order categories by CATEGORY_ORDER, then append any others alphabetically.

    CATEGORY_ORDER is a ranking hint, NOT a gate: every category present in the
    data is returned, so newly added categories are never silently dropped from
    the index. Unranked categories trigger a stderr note suggesting they be
    added to CATEGORY_ORDER for custom placement.
    """
    present_set = set(present)
    ranked = [c for c in CATEGORY_ORDER if c in present_set]
    unranked = sorted(c for c in present_set if c not in CATEGORY_ORDER)
    for c in unranked:
        print(
            f"  NOTE: category '{c}' not in CATEGORY_ORDER — appended at end; "
            f"add it to CATEGORY_ORDER to control placement.",
            file=sys.stderr,
        )
    return ranked + unranked


def extract_topic_metadata(topic_key: str, guide_count: int) -> dict | None:
    """Extract topic metadata from docs directory. Returns metadata dict or None."""
    topic_dir = DOCS_DIR / topic_key
    if not topic_dir.is_dir():
        print(f"  WARNING: Directory not found: {topic_dir}", file=sys.stderr)
        return None

    # Count .md files (excluding index.md)
    md_files = [f for f in topic_dir.glob("*.md") if f.name != "index.md"]
    if not md_files:
        print(f"  WARNING: No .md files in {topic_dir}", file=sys.stderr)
        return None

    # Read index.md for topic title and description
    index_file = topic_dir / "index.md"
    index_content = ""
    if index_file.exists():
        index_content = index_file.read_text(encoding="utf-8")

    topic_title = extract_h1(index_content) or topic_key.split("/")[-1].replace("-", " ").title()
    topic_desc = extract_summary(index_content) or f"Decision guides for {topic_title}"
    actual_count = len(md_files)

    print(f"  {topic_key} — {actual_count} guides")

    return {
        "topic_key": topic_key,
        "title": topic_title,
        "description": topic_desc,
        "guide_count": actual_count,
        "category": get_category(topic_key),
    }


def build_index(topics: list[dict]) -> str:
    """Build the llms.txt index content."""
    # Group by category
    categories: dict[str, list[dict]] = {}
    for t in topics:
        cat = t["category"]
        categories.setdefault(cat, []).append(t)

    # Every present category, in preferred order then alphabetical (no drops).
    ordered_cats = order_categories(list(categories.keys()))

    # Check for template
    if TEMPLATE_PATH.exists():
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
        # Simple template rendering
        sections = []
        for cat_name in ordered_cats:
            section_lines = [f"## {cat_name}\n"]
            for t in sorted(categories[cat_name], key=lambda x: x["title"]):
                url = f"{SITE_BASE_URL}/{t['topic_key']}/"
                desc = t["description"][:100]
                section_lines.append(
                    f"- [{t['title']}]({url}): {t['guide_count']} guides — {desc}"
                )
            sections.append("\n".join(section_lines))

        topic_sections = "\n\n".join(sections)
        result = template.replace("{{ topic_sections }}", topic_sections)
        total_guides = sum(t["guide_count"] for t in topics)
        result = result.replace("{{ total_guides }}", str(total_guides))
        result = result.replace("{{ topic_count }}", str(len(topics)))
        return result

    # Fallback: generate without template
    lines = ["# Dev Guides\n"]
    total_guides = sum(t["guide_count"] for t in topics)
    lines.append(
        f"> AI-friendly atomic decision guides for Drupal, CSS, JavaScript, "
        f"design systems, and Next.js development. {total_guides} guides across "
        f"{len(topics)} topics. Each topic link below points to a topic index "
        f"with a routing table to individual guides.\n"
    )

    for cat_name in ordered_cats:
        lines.append(f"## {cat_name}\n")
        for t in sorted(categories[cat_name], key=lambda x: x["title"]):
            url = f"{SITE_BASE_URL}/{t['topic_key']}/"
            desc = t["description"][:100]
            lines.append(f"- [{t['title']}]({url}): {t['guide_count']} guides — {desc}")
        lines.append("")

    return "\n".join(lines)


GUIDE_MANIFEST_NAME = "guide-index.json"


def build_guide_manifests(topics: list[dict]) -> int:
    """Emit a per-topic guide manifest giving each guide BODY a content hash.

    `llms.txt` is per-topic, so a guide body edit that doesn't move a topic's
    count/description is invisible to `llms.hash` — the navigator has no way to
    know a cached guide went stale without re-fetching it. This manifest is the
    per-guide equivalent of the recipe index's per-line `(sha:...)`: a small
    `{ "<filename>.md": "<sha256>" }` map the navigator reads (once per topic it
    routes into) to decide, WITHOUT fetching the body, whether its cached copy is
    current. `index.md` is included so the routing table is cacheable too.

    The sha256 is over the raw file bytes — the exact content the navigator pulls
    from `raw.githubusercontent.com/.../docs/<topic>/<file>.md` — so the hashes
    match byte-for-byte. Written to `site/<topic>/guide-index.json`, served beside
    the topic page (gated by the per-file sha, never the global `llms.hash`).

    Returns the total number of files hashed across all topics.
    """
    total = 0
    for t in topics:
        topic_key = t["topic_key"]
        md_files = sorted((DOCS_DIR / topic_key).glob("*.md"))
        if not md_files:
            continue
        manifest = {
            f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in md_files
        }
        out_dir = SITE_DIR / topic_key
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / GUIDE_MANIFEST_NAME).write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        total += len(manifest)
    return total


def build_llms_hash(llms_content: str) -> None:
    """Generate llms.hash — SHA-256 of llms.txt for cache freshness."""
    content_hash = hashlib.sha256(llms_content.encode("utf-8")).hexdigest()
    output_path = SITE_DIR / "llms.hash"
    output_path.write_text(content_hash, encoding="utf-8")
    print(f"\nHash: {output_path} ({content_hash[:16]}...)")


def main():
    if not MANIFEST_PATH.exists():
        print(f"ERROR: {MANIFEST_PATH} not found", file=sys.stderr)
        sys.exit(1)

    if not SITE_DIR.exists():
        print(f"ERROR: {SITE_DIR} not found. Run 'mkdocs build' first.", file=sys.stderr)
        sys.exit(1)

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    print(f"Found {len(manifest)} topics in manifest\n")

    topics = []
    for topic_key, meta in manifest.items():
        result = extract_topic_metadata(topic_key, meta.get("guides_extracted", 0))
        if result:
            topics.append(result)

    # Generate llms.txt index
    index_content = build_index(topics)
    index_path = SITE_DIR / "llms.txt"
    index_path.write_text(index_content, encoding="utf-8")

    total_guides = sum(t["guide_count"] for t in topics)

    # Generate llms.hash for cache freshness
    build_llms_hash(index_content)

    # Generate per-topic guide manifests (per-guide body shas for the navigator).
    files_hashed = build_guide_manifests(topics)

    print(f"\nDone!")
    print(f"  Topics: {len(topics)}")
    print(f"  Total guides: {total_guides}")
    print(f"  Index: {index_path}")
    print(f"  Guide manifests: {len(topics)} × {GUIDE_MANIFEST_NAME} ({files_hashed} files hashed)")


if __name__ == "__main__":
    main()
