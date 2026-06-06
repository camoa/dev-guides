#!/usr/bin/env python3
"""Generate agentic-recipes.txt index and agentic-recipes.hash for dev-guides.

This is the recipe-catalog counterpart to generate_llms.py. It is deliberately
SEPARATE from llms.txt: recipes publish their own lean index so the guides index
never grows by a recipe, and a caller (e.g. the dev-guides-navigator's recipe
mode) fetches it independently.

Recipes are born-atomic — there is no partition step and no manifest. This
scans docs/agentic-recipes/** directly, reading each recipe's routing block
(name / capability / description), and emits one line per recipe grouped by
domain (the first path segment under agentic-recipes/, e.g. `drupal`).

Run after `mkdocs build` so site/ exists.
"""

import hashlib
import re
import sys
from pathlib import Path

import yaml

SITE_BASE_URL = "https://camoa.github.io/dev-guides"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
RECIPES_DIR = DOCS_DIR / "agentic-recipes"
SITE_DIR = PROJECT_ROOT / "site"

# Domain key -> display name (mirrors generate_llms.py CATEGORY_MAP).
DOMAIN_MAP = {
    "drupal": "Drupal",
    "css": "CSS",
    "js": "JavaScript",
    "nextjs": "Next.js",
    "design-systems": "Design Systems",
}
DOMAIN_ORDER = ["Drupal", "CSS", "JavaScript", "Next.js", "Design Systems"]

HEADER = (
    "# Dev Agentic Recipes\n\n"
    "> Goal-oriented, prescriptive capability deliveries. Each recipe sequences "
    "existing guides and plays end to end and carries a verifier. Match a "
    "capability below, then fetch the recipe (raw markdown via curl, never "
    "WebFetch) — it names the guides it needs. This index is separate from "
    "llms.txt (the guides index).\n>\n"
    "> Each line carries `(sha:XXXXXXXX)` — a per-recipe content hash. Cache the "
    "recipe body once on first fetch keyed by name; on later need, re-fetch only "
    "if the line's sha differs from your cached sha. The body need not be "
    "re-downloaded while the sha is unchanged.\n\n"
    "{recipe_sections}\n"
)


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter as a dict."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            try:
                meta = yaml.safe_load(content[3:end])
                return meta if isinstance(meta, dict) else {}
            except yaml.YAMLError:
                return {}
    return {}


def domain_of(path: Path) -> str:
    """First path segment under agentic-recipes/ → display domain."""
    rel = path.relative_to(RECIPES_DIR)
    key = rel.parts[0] if len(rel.parts) > 1 else "general"
    return DOMAIN_MAP.get(key, key.title())


def recipe_url(path: Path) -> str:
    """GitHub Pages URL for a recipe page (mkdocs directory-style URL)."""
    rel = path.relative_to(DOCS_DIR).with_suffix("")
    return f"{SITE_BASE_URL}/{rel.as_posix()}/"


def collect_recipes() -> list[dict]:
    """Scan docs/agentic-recipes/** and return routing metadata per recipe.

    Each recipe carries a per-recipe content hash (sha256 of the full file)
    so a caller's body cache can be invalidated per-recipe — without fetching
    the body — even when the routing block (and thus the global index hash) is
    unchanged. The global agentic-recipes.hash gates the index cache; this
    per-recipe sha gates each downloaded-once body cache.
    """
    recipes = []
    for path in sorted(RECIPES_DIR.rglob("*.md")):
        if path.name == "index.md":
            continue
        raw = path.read_text(encoding="utf-8")
        meta = extract_frontmatter(raw)
        name = meta.get("name")
        capability = meta.get("capability")
        description = meta.get("description")
        if not (name and capability and description):
            print(
                f"  WARNING: skipping {path.relative_to(PROJECT_ROOT)} "
                f"(missing name/capability/description)",
                file=sys.stderr,
            )
            continue
        sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8]
        recipes.append(
            {
                "name": name,
                "capability": capability,
                "description": " ".join(str(description).split()),
                "sha": sha,
                "domain": domain_of(path),
                "url": recipe_url(path),
            }
        )
        print(f"  {name} [{capability}] (sha:{sha}) — {domain_of(path)}")
    return recipes


def build_index(recipes: list[dict]) -> str:
    """Render agentic-recipes.txt: one routing line per recipe, grouped by domain."""
    by_domain: dict[str, list[dict]] = {}
    for r in recipes:
        by_domain.setdefault(r["domain"], []).append(r)

    ordered = DOMAIN_ORDER + [d for d in sorted(by_domain) if d not in DOMAIN_ORDER]

    sections = []
    for domain in ordered:
        if domain not in by_domain:
            continue
        lines = [f"## {domain}\n"]
        for r in sorted(by_domain[domain], key=lambda x: x["name"]):
            lines.append(
                f"- {r['name']} [{r['capability']}] (sha:{r['sha']}): "
                f"{r['description']} — {r['url']}"
            )
        sections.append("\n".join(lines))

    return HEADER.format(recipe_sections="\n\n".join(sections))


def main() -> int:
    if not RECIPES_DIR.is_dir():
        print(f"No recipes directory at {RECIPES_DIR} — nothing to generate.")
        return 0
    if not SITE_DIR.exists():
        print(f"ERROR: {SITE_DIR} not found. Run 'mkdocs build' first.", file=sys.stderr)
        return 1

    recipes = collect_recipes()
    index_content = build_index(recipes)

    index_path = SITE_DIR / "agentic-recipes.txt"
    index_path.write_text(index_content, encoding="utf-8")

    content_hash = hashlib.sha256(index_content.encode("utf-8")).hexdigest()
    (SITE_DIR / "agentic-recipes.hash").write_text(content_hash, encoding="utf-8")

    print(f"\nDone!")
    print(f"  Recipes: {len(recipes)}")
    print(f"  Index: {index_path}")
    print(f"  Hash:  {content_hash[:16]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
