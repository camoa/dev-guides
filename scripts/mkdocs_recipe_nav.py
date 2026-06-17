"""mkdocs build hook: auto-generate the recipe nav sections from disk.

The "Process Recipes" and "Agentic Recipes" sections of the left-hand nav are
built from the recipe files on disk at build time, so a new recipe — or a whole
new framework/domain folder — appears in the menu automatically. No manual
`mkdocs.yml` edit, and the menu can never drift out of sync with what is
published (the bug this replaces: 4 of 6 Drupal process recipes were missing
from the nav because each had to be added by hand).

Single source of truth = the files under `docs/<section>/`. Per recipe:
  - the nav title is the recipe's `label` frontmatter (falls back to `name`,
    then the filename),
  - recipes are grouped by `framework` (falls back to the folder name) and
    ordered by lifecycle phase (`capability`); unknown phases sort last by label.

This mirrors generate_process_recipes.py (which builds the machine-readable
index) so the human nav and the orchestrator index stay aligned.

Wired via `hooks:` in mkdocs.yml. mkdocs calls on_config() after the raw config
is loaded but before the Navigation object is built, so mutating config["nav"]
here is picked up when mkdocs materializes the menu.
"""

from pathlib import Path

import yaml

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

# Nav section title -> docs/ subdirectory that backs it.
RECIPE_SECTIONS = [
    ("Process Recipes", "process-recipes"),
    ("Agentic Recipes", "agentic-recipes"),
]

# Framework/domain folder -> display name for its sub-section. Unknown folders
# fall back to a title-cased token, so a new framework needs no edit here.
FRAMEWORK_TITLES = {
    "drupal": "Drupal",
    "claude-code-plugins": "Claude Code Plugins",
    "nextjs": "Next.js",
    "css": "CSS",
    "js": "JavaScript",
    "wordpress": "WordPress",
    "design-systems": "Design Systems",
}
# Sub-section order; frameworks not listed are appended alphabetically.
FRAMEWORK_ORDER = ["drupal", "wordpress", "nextjs", "claude-code-plugins"]

# Lifecycle phase order (a process recipe's `capability`); unknown/absent phases
# sort after the known ones, then alphabetically by label.
PHASE_ORDER = [
    "research",
    "design",
    "implement",
    "review",
    "e2e-setup",
    "visual-regression",
]


def _framework_title(folder: str) -> str:
    return FRAMEWORK_TITLES.get(folder, folder.replace("-", " ").title())


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    try:
        meta = yaml.safe_load(text[3:end])
    except yaml.YAMLError:
        return {}
    return meta if isinstance(meta, dict) else {}


def _sort_key(recipe: dict) -> tuple:
    """Order by lifecycle phase when present, else after, by label."""
    capability = recipe["capability"]
    if capability in PHASE_ORDER:
        return (0, PHASE_ORDER.index(capability), "")
    return (1, 0, recipe["label"].lower())


def _build_section(subdir: str) -> list:
    """Return the nav list for one recipe section, index page first."""
    section_dir = DOCS_DIR / subdir
    items: list = []

    index_md = section_dir / "index.md"
    if index_md.is_file():
        items.append(f"{subdir}/index.md")

    if not section_dir.is_dir():
        return items

    by_framework: dict[str, list] = {}
    for md in sorted(section_dir.rglob("*.md")):
        if md.name == "index.md":
            continue
        meta = _frontmatter(md)
        framework = meta.get("framework") or md.parent.name
        by_framework.setdefault(framework, []).append(
            {
                "label": str(meta.get("label") or meta.get("name") or md.stem),
                "capability": str(meta.get("capability") or ""),
                "path": md.relative_to(DOCS_DIR).as_posix(),
            }
        )

    ordered = FRAMEWORK_ORDER + sorted(
        f for f in by_framework if f not in FRAMEWORK_ORDER
    )
    for framework in ordered:
        recipes = by_framework.get(framework)
        if not recipes:
            continue
        recipes.sort(key=_sort_key)
        sub_nav = [{r["label"]: r["path"]} for r in recipes]
        items.append({_framework_title(framework): sub_nav})

    return items


def _replace_section(nav, title: str, subtree: list) -> bool:
    """Replace the value of the nav entry whose key == title. Returns True if found."""
    if not isinstance(nav, list):
        return False
    for entry in nav:
        if not isinstance(entry, dict):
            continue
        for key, value in list(entry.items()):
            if key == title:
                entry[key] = subtree
                return True
            if _replace_section(value, title, subtree):
                return True
    return False


def on_config(config):
    nav = config.get("nav")
    if not nav:
        return config
    for title, subdir in RECIPE_SECTIONS:
        subtree = _build_section(subdir)
        if subtree:
            _replace_section(nav, title, subtree)
    return config
