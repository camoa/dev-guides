#!/usr/bin/env python3
"""Generate process-recipes.txt index and process-recipes.hash for dev-guides.

Process recipes are a SEPARATE class from task (agentic) recipes, and they get a
SEPARATE published index for a deliberate reason: they are resolved by an
orchestrator at a lifecycle phase, keyed by (phase × framework) — never matched
by capability during free task work, where they would pollute context. Keeping
them in their own index (and their own docs/ root) means a task-routing caller
never even sees them.

Routing is decided by LOCATION: every recipe under docs/process-recipes/** is a
process recipe. This is robust by construction — the task generator
(generate_recipes.py) scans docs/agentic-recipes/ only, so a process recipe
cannot leak into the task index. (`recipe_class: process` in the frontmatter is
self-documenting; the directory is the source of truth.)

This is the process-catalog counterpart to generate_recipes.py. Recipes are
born-atomic — no partition step, no manifest. It scans docs/process-recipes/**
directly, reading each recipe's routing block, and emits one line per recipe
grouped by domain (the first path segment under process-recipes/, e.g. `drupal`).

Each line carries the resolution key the orchestrator matches on WITHOUT fetching
the body: `[phase=<phase> framework=<framework>]`, where `phase` is the recipe's
`capability` (the two coincide for a process recipe — the capability IS the
lifecycle phase). The per-recipe `(sha:XXXXXXXX)` gates the body cache exactly as
in the task index.

Run after `mkdocs build` so site/ exists.
"""

import hashlib
import sys
from pathlib import Path

import yaml

SITE_BASE_URL = "https://camoa.github.io/dev-guides"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
RECIPES_DIR = DOCS_DIR / "process-recipes"
SITE_DIR = PROJECT_ROOT / "site"

# Domain key -> display name (mirrors generate_recipes.py).
DOMAIN_MAP = {
    "drupal": "Drupal",
    "css": "CSS",
    "js": "JavaScript",
    "nextjs": "Next.js",
    "wordpress": "WordPress",
    "design-systems": "Design Systems",
}
DOMAIN_ORDER = ["Drupal", "WordPress", "Next.js", "JavaScript", "CSS", "Design Systems"]

HEADER = (
    "# Dev Process Recipes\n\n"
    "> Framework-specific drivers for one phase of the development lifecycle. A "
    "process recipe is resolved by an ORCHESTRATOR, keyed by (phase × framework), "
    "at a lifecycle moment — NOT matched by capability during free task work. This "
    "index is separate from both llms.txt (guides) and agentic-recipes.txt (task "
    "recipes); do not surface these during normal task routing.\n>\n"
    "> Each line: `- <name> [phase=<phase> framework=<framework>] (sha:XXXXXXXX): "
    "<when-to-use> — <site-url>`. Match on (phase, framework); a single phase may "
    "resolve one recipe per listed framework. Fetch the body as RAW markdown via "
    "curl (never WebFetch), derived from the site-url. The `(sha:XXXXXXXX)` is a "
    "per-recipe content hash: cache the body once keyed by name, re-fetch only when "
    "the sha differs.\n\n"
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
    """First path segment under process-recipes/ → display domain."""
    rel = path.relative_to(RECIPES_DIR)
    key = rel.parts[0] if len(rel.parts) > 1 else "general"
    return DOMAIN_MAP.get(key, key.title())


def recipe_url(path: Path) -> str:
    """GitHub Pages URL for a recipe page (mkdocs directory-style URL).

    The navigator derives the raw body URL from this: site-url
    `…/process-recipes/drupal/e2e-setup-atk/` →
    raw `…/main/docs/process-recipes/drupal/e2e-setup-atk.md`.
    """
    rel = path.relative_to(DOCS_DIR).with_suffix("")
    return f"{SITE_BASE_URL}/{rel.as_posix()}/"


def collect_recipes() -> list[dict]:
    """Scan docs/process-recipes/** and return routing metadata per recipe.

    `phase` is the recipe's `capability` (they coincide for a process recipe).
    `framework` is required — it is the second half of the resolution key. A file
    missing name / capability / framework is skipped with a warning (it cannot be
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
        sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8]
        recipes.append(
            {
                "name": name,
                "phase": capability,
                "framework": framework,
                "description": " ".join(str(description).split()),
                "sha": sha,
                "domain": domain_of(path),
                "url": recipe_url(path),
            }
        )
        print(f"  {name} [phase={capability} framework={framework}] (sha:{sha}) — {domain_of(path)}")
    return recipes


def build_index(recipes: list[dict]) -> str:
    """Render process-recipes.txt: one routing line per recipe, grouped by domain."""
    by_domain: dict[str, list[dict]] = {}
    for r in recipes:
        by_domain.setdefault(r["domain"], []).append(r)

    ordered = DOMAIN_ORDER + [d for d in sorted(by_domain) if d not in DOMAIN_ORDER]

    sections = []
    for domain in ordered:
        if domain not in by_domain:
            continue
        lines = [f"## {domain}\n"]
        for r in sorted(by_domain[domain], key=lambda x: (x["phase"], x["framework"], x["name"])):
            lines.append(
                f"- {r['name']} [phase={r['phase']} framework={r['framework']}] "
                f"(sha:{r['sha']}): {r['description']} — {r['url']}"
            )
        sections.append("\n".join(lines))

    return HEADER.format(recipe_sections="\n\n".join(sections))


def main() -> int:
    if not RECIPES_DIR.is_dir():
        print(f"No process-recipes directory at {RECIPES_DIR} — nothing to generate.")
        return 0
    if not SITE_DIR.exists():
        print(f"ERROR: {SITE_DIR} not found. Run 'mkdocs build' first.", file=sys.stderr)
        return 1

    recipes = collect_recipes()
    index_content = build_index(recipes)

    index_path = SITE_DIR / "process-recipes.txt"
    index_path.write_text(index_content, encoding="utf-8")

    content_hash = hashlib.sha256(index_content.encode("utf-8")).hexdigest()
    (SITE_DIR / "process-recipes.hash").write_text(content_hash, encoding="utf-8")

    print(f"\nDone!")
    print(f"  Process recipes: {len(recipes)}")
    print(f"  Index: {index_path}")
    print(f"  Hash:  {content_hash[:16]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
