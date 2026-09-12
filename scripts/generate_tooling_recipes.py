#!/usr/bin/env python3
"""Generate tooling-recipes.txt index and tooling-recipes.hash for dev-guides.

Tooling recipes are a THIRD class, separate from task (agentic) and process
recipes, and they get their own published index for the same reason those two
do: a caller resolving one already knows it wants a tool, and surfacing tool
installs during task routing would pollute context.

Without this index the published tooling recipes cannot be found at all. A
caller has no listing to search, so it reads whatever folders it has locally and
stops where a recipe would have to come from the catalog — not by decision, but
because nothing is there to read.

Routing is decided by LOCATION: every recipe under docs/tooling-recipes/** is a
tooling recipe. The task generator scans docs/agentic-recipes/ only and the
process generator scans docs/process-recipes/ only, so the three cannot leak
into each other.

Each line carries what a caller needs to resolve a recipe WITHOUT fetching the
body: `[tool=<tool> framework=<framework>]`. Two things, because there are two
lookups. The TOOL NAME, because that is how everything refers to a tooling
recipe — the tooling index says a recipe is named for its tool and whatever
needs the tool refers to it by that name — which serves a caller that already
knows which tool it wants. And the FRAMEWORK, because the same tool installs
differently per framework: phpunit on Drupal runs through Composer inside a
container, phpunit on a PHP CLI project does not. Search words match against the
description, which is what a caller does when it does not yet know the tool.

`tool` is the recipe's `capability` — the two coincide for a tooling recipe,
exactly as `phase` and `capability` coincide for a process recipe. The
per-recipe `(sha:XXXXXXXX)` gates the body cache as in the other two indexes.

Run after `mkdocs build` so site/ exists.
"""

import hashlib
import sys
from pathlib import Path

import yaml

SITE_BASE_URL = "https://camoa.github.io/dev-guides"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
RECIPES_DIR = DOCS_DIR / "tooling-recipes"
SITE_DIR = PROJECT_ROOT / "site"

# Domain key -> display name (mirrors generate_process_recipes.py).
DOMAIN_MAP = {
    "drupal": "Drupal",
    "css": "CSS",
    "js": "JavaScript",
    "nextjs": "Next.js",
    "wordpress": "WordPress",
    "design-systems": "Design Systems",
    "claude-code-plugins": "Claude Code Plugins",
    "go": "Go",
    "php-cli": "PHP CLI",
    "python-cli": "Python CLI",
}
DOMAIN_ORDER = [
    "Drupal", "PHP CLI", "Python CLI", "Go", "WordPress", "Next.js",
    "JavaScript", "CSS", "Design Systems", "Claude Code Plugins",
]

HEADER = (
    "# Dev Tooling Recipes\n\n"
    "> One tool, one framework, one document: what the tool is, how to install "
    "it, and how to run it. A tooling recipe is resolved when something needs a "
    "tool on disk — by tool name and framework when the caller knows which tool "
    "it wants, or by search words when it does not. This index is separate from "
    "llms.txt (guides), agentic-recipes.txt (task recipes) and "
    "process-recipes.txt (lifecycle drivers); do not surface these during normal "
    "task routing.\n>\n"
    "> Each line: `- <name> [tool=<tool> framework=<framework>] (sha:XXXXXXXX): "
    "<when-to-use> — <site-url>`. Match on (tool, framework); the same tool name "
    "resolves to a different recipe per framework, because the install differs. "
    "Fetch the body as RAW markdown via curl (never WebFetch), derived from the "
    "site-url. The `(sha:XXXXXXXX)` is a per-recipe content hash: cache the body "
    "once keyed by name, re-fetch only when the sha differs.\n>\n"
    "> Under `## Install`, every fenced block tagged `sh` holds commands, one per "
    "line, read in order; a block tagged anything else is read, not run. Under "
    "`## Run`, exactly one block is tagged `sh` and it holds one command. Running "
    "that command is also the check for whether the tool is present.\n\n"
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
    """First path segment under tooling-recipes/ → display domain."""
    rel = path.relative_to(RECIPES_DIR)
    key = rel.parts[0] if len(rel.parts) > 1 else "general"
    return DOMAIN_MAP.get(key, key.title())


def recipe_url(path: Path) -> str:
    """GitHub Pages URL for a recipe page (mkdocs directory-style URL).

    The navigator derives the raw body URL from this: site-url
    `…/tooling-recipes/drupal/phpcs/` →
    raw `…/main/docs/tooling-recipes/drupal/phpcs.md`.
    """
    rel = path.relative_to(DOCS_DIR).with_suffix("")
    return f"{SITE_BASE_URL}/{rel.as_posix()}/"


def collect_recipes() -> list[dict]:
    """Scan docs/tooling-recipes/** and return routing metadata per recipe.

    `tool` is the recipe's `capability` (they coincide for a tooling recipe).
    `framework` is required — it is the second half of the resolution key, and
    the reason the same tool name can appear more than once. A file missing
    name / capability / framework is skipped with a warning (it cannot be
    routed to).
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
        framework = meta.get("framework")
        if not (name and capability and description and framework):
            print(
                f"  WARNING: skipping {path.relative_to(PROJECT_ROOT)} "
                f"(needs name/capability/description/framework)",
                file=sys.stderr,
            )
            continue
        # Hash the raw on-disk bytes — the exact content a consumer pulls from
        # raw.githubusercontent.com and re-hashes to verify the blob. read_text()
        # above normalizes newlines for frontmatter parsing, so it must NOT be the
        # hash input or a CRLF/BOM file would fail that integrity check.
        sha = hashlib.sha256(path.read_bytes()).hexdigest()[:8]
        recipes.append(
            {
                "name": name,
                "tool": capability,
                "framework": framework,
                "description": " ".join(str(description).split()),
                "sha": sha,
                "domain": domain_of(path),
                "url": recipe_url(path),
            }
        )
        print(f"  {name} [tool={capability} framework={framework}] (sha:{sha}) — {domain_of(path)}")
    return recipes


def build_index(recipes: list[dict]) -> str:
    """Render tooling-recipes.txt: one routing line per recipe, grouped by domain."""
    by_domain: dict[str, list[dict]] = {}
    for r in recipes:
        by_domain.setdefault(r["domain"], []).append(r)

    ordered = DOMAIN_ORDER + [d for d in sorted(by_domain) if d not in DOMAIN_ORDER]

    sections = []
    for domain in ordered:
        if domain not in by_domain:
            continue
        lines = [f"## {domain}\n"]
        for r in sorted(by_domain[domain], key=lambda x: (x["tool"], x["framework"], x["name"])):
            lines.append(
                f"- {r['name']} [tool={r['tool']} framework={r['framework']}] "
                f"(sha:{r['sha']}): {r['description']} — {r['url']}"
            )
        sections.append("\n".join(lines))

    return HEADER.format(recipe_sections="\n\n".join(sections))


def main() -> int:
    if not RECIPES_DIR.is_dir():
        print(f"No tooling-recipes directory at {RECIPES_DIR} — nothing to generate.")
        return 0
    if not SITE_DIR.exists():
        print(f"ERROR: {SITE_DIR} not found. Run 'mkdocs build' first.", file=sys.stderr)
        return 1

    recipes = collect_recipes()
    index_content = build_index(recipes)

    index_path = SITE_DIR / "tooling-recipes.txt"
    index_path.write_text(index_content, encoding="utf-8")

    content_hash = hashlib.sha256(index_content.encode("utf-8")).hexdigest()
    (SITE_DIR / "tooling-recipes.hash").write_text(content_hash, encoding="utf-8")

    print(f"\nDone!")
    print(f"  Tooling recipes: {len(recipes)}")
    print(f"  Index: {index_path}")
    print(f"  Hash:  {content_hash[:16]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
