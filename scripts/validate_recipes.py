#!/usr/bin/env python3
"""Validate agentic recipes under docs/agentic-recipes/.

A recipe is born-atomic (not partitioned), so it is authored directly to the
recipe-file-format-standard. This validator is the gate that keeps the catalog
honest. It checks, per recipe file:

  1. Frontmatter parses and is routing-first: the first three keys are
     exactly `name`, `capability`, `description`, in that order.
  2. Required metadata keys are present: `label`, `recipe_schema_version`,
     `version`.
  3. Required body sections are present (the 1.0.0 section set).
  4. Every cited guide/play slug resolves to a real file under docs/.
     An unresolved citation is a BLOCKER — it is also the signal that a
     referenced guide needs to be authored (the "auto-generate guides when
     needed" hook).

Exit code is non-zero if any recipe fails. Pure stdlib + PyYAML; safe to run
locally and in CI before `mkdocs build`.
"""

import re
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
RECIPES_DIR = DOCS_DIR / "agentic-recipes"

# First three frontmatter keys, in order (routing block).
ROUTING_KEYS = ["name", "capability", "description"]

# Metadata keys that must be present (order not enforced beyond routing-first).
REQUIRED_META_KEYS = ["label", "recipe_schema_version", "version"]

# Required body sections (## headings), per recipe_schema_version 1.0.0.
REQUIRED_SECTIONS = [
    "Goal",
    "Opinion",
    "Preconditions",
    "Input contract",
    "Sequence",
    "Data flow",
    "State-awareness contract",
    "Verifier",
    "References",
]

# A citation slug: lowercase path segments joined by '/', e.g.
# drupal/image-styles/image-overview or
# drupal/best-practices/camoa/responsive-image-sizing-per-context.
# Excludes dotted config keys (system.theme.default), globs (*.breakpoints.yml),
# and single-segment tokens.
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)+$")


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_yaml, body). Empty frontmatter if none present."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[3:end], text[end + 3:]
    return "", text


def ordered_keys(frontmatter_yaml: str) -> list[str]:
    """Top-level YAML keys in source order (comments and indented keys ignored)."""
    keys = []
    for line in frontmatter_yaml.splitlines():
        if not line or line[0] in " \t#-":
            continue
        m = re.match(r"^([A-Za-z0-9_]+):", line)
        if m:
            keys.append(m.group(1))
    return keys


def cited_slugs(body: str) -> set[str]:
    """All backtick-quoted path-like slugs in the body."""
    slugs = set()
    for token in re.findall(r"`([^`]+)`", body):
        token = token.strip()
        if SLUG_RE.match(token):
            slugs.add(token)
    return slugs


def slug_resolves(slug: str) -> bool:
    """A slug resolves if docs/<slug>.md or docs/<slug>/index.md exists."""
    return (DOCS_DIR / f"{slug}.md").is_file() or (
        DOCS_DIR / slug / "index.md"
    ).is_file()


def validate_recipe(path: Path) -> list[str]:
    """Return a list of human-readable errors for one recipe (empty = valid)."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm_yaml, body = split_frontmatter(text)

    if not fm_yaml.strip():
        return ["missing YAML frontmatter"]

    try:
        meta = yaml.safe_load(fm_yaml) or {}
    except yaml.YAMLError as exc:
        return [f"frontmatter YAML error: {exc}"]

    # 1. Routing-first: first three keys exactly name, capability, description.
    keys = ordered_keys(fm_yaml)
    if keys[:3] != ROUTING_KEYS:
        errors.append(
            f"routing block must be the first three keys {ROUTING_KEYS} in order; "
            f"found {keys[:3]}"
        )

    # 2. Required metadata present.
    for key in REQUIRED_META_KEYS:
        if not meta.get(key):
            errors.append(f"missing required frontmatter key: {key}")

    # `description` must be a single line (one-line trigger, not a paragraph).
    desc = str(meta.get("description", ""))
    if "\n" in desc.strip():
        errors.append("`description` must be a single line (when-to-use trigger)")

    # 3. Required body sections.
    headings = {h.strip() for h in re.findall(r"^##\s+(.+)$", body, re.MULTILINE)}
    for section in REQUIRED_SECTIONS:
        if section not in headings:
            errors.append(f"missing required section: ## {section}")

    # 4. Citations resolve.
    for slug in sorted(cited_slugs(body)):
        if not slug_resolves(slug):
            errors.append(
                f"cited guide/play does not resolve to a file: `{slug}` "
                f"(expected docs/{slug}.md or docs/{slug}/index.md)"
            )

    return errors


def main() -> int:
    if not RECIPES_DIR.is_dir():
        print(f"No recipes directory at {RECIPES_DIR} — nothing to validate.")
        return 0

    recipe_files = sorted(
        p for p in RECIPES_DIR.rglob("*.md") if p.name != "index.md"
    )
    if not recipe_files:
        print(f"No recipe files under {RECIPES_DIR} — nothing to validate.")
        return 0

    total_errors = 0
    for path in recipe_files:
        rel = path.relative_to(PROJECT_ROOT)
        errors = validate_recipe(path)
        if errors:
            total_errors += len(errors)
            print(f"\nFAIL  {rel}")
            for err in errors:
                print(f"        - {err}")
        else:
            print(f"OK    {rel}")

    print()
    if total_errors:
        print(f"Validation failed: {total_errors} error(s) across recipes.")
        return 1
    print(f"All {len(recipe_files)} recipe(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
