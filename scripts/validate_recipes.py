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

import json
import re
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
RECIPES_DIR = DOCS_DIR / "agentic-recipes"          # task recipes
PROCESS_RECIPES_DIR = DOCS_DIR / "process-recipes"  # process recipes (location = class)

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

# `name` is a globally-unique identifier the navigator uses as a cache key
# (recipes.{<name>: …} in the navigator lockfile). snake_case only — a name with
# spaces, brackets, or hyphens would corrupt the delimiter-structured index line
# and could collide silently across recipes.
NAME_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")

# `capability` (the phase) and `framework` are routing tokens emitted into the
# process-recipes.txt line as `[phase=<capability> framework=<framework>]`. They
# must be single kebab/snake tokens with no spaces or brackets so the line stays
# deterministically parseable.
TOKEN_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

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


# `## Oracle files` is a CONSUMED contract as of 2026-09-01: the ai-dev-assistant
# test-motion guard reads the first ```json fence under that H2 and takes the
# `globs` off the row whose `type` is `test_delete`, instead of trusting a
# caller-supplied list. That makes three things load-bearing that used to be
# cosmetic — the fence must parse, the row keys must be the agreed set, and
# `test_delete` must appear exactly once so it is a stable selector.
ORACLE_H2 = "## Oracle files"
ORACLE_KEYS = {"type", "globs", "changes", "oracle_class", "severity"}
JSON_FENCE_RE = re.compile(r"```json\s*\n(.*?)\n```", re.S)


def validate_oracle_block(body: str) -> list[str]:
    """Check the `## Oracle files` JSON fence and its agreement with the table.

    Returns [] when the recipe has no oracle section — declaring none is a valid
    "no oracle configured" state, not an omission.
    """
    errors: list[str] = []
    idx = body.find(ORACLE_H2)
    if idx == -1:
        return errors

    # Bound the section at the next H2 so a later fence cannot be mistaken for it.
    rest = body[idx + len(ORACLE_H2):]
    nxt = re.search(r"^## ", rest, re.M)
    section = rest[: nxt.start()] if nxt else rest

    m = JSON_FENCE_RE.search(section)
    if not m:
        return ["`## Oracle files` has no ```json fence; the guard reads that fence"]

    try:
        rows = json.loads(m.group(1))
    except json.JSONDecodeError as exc:
        return [f"`## Oracle files` JSON does not parse: {exc}"]

    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        return ["`## Oracle files` JSON must be a top-level array of flat objects"]

    for i, row in enumerate(rows):
        if set(row) != ORACLE_KEYS:
            errors.append(
                f"oracle row {i} keys {sorted(row)} != the agreed set {sorted(ORACLE_KEYS)}"
            )
        globs = row.get("globs")
        if not isinstance(globs, list) or not globs or not all(isinstance(g, str) for g in globs):
            errors.append(f"oracle row {i} `globs` must be a non-empty list of strings")
        if row.get("severity") not in ("halt", "flag"):
            errors.append(f"oracle row {i} `severity` must be 'halt' or 'flag'; found {row.get('severity')!r}")
        changes = row.get("changes")
        if not isinstance(changes, list) or not set(changes) <= {"A", "M", "D"} or not changes:
            errors.append(f"oracle row {i} `changes` must be a non-empty subset of A/M/D")

    n_delete = sum(1 for r in rows if r.get("type") == "test_delete")
    if n_delete > 1:
        errors.append(
            f"`type: test_delete` appears {n_delete} times; the guard selects on it, "
            "so it must appear at most once per recipe"
        )

    # The markdown table above the fence and the fence itself state the same rules.
    # Nothing reconciled them before, so they could drift apart silently — the
    # table is what a person reads, the fence is what the guard applies.
    table_rows = [
        ln for ln in section.splitlines()
        if ln.startswith("|") and "|" in ln[1:] and not re.match(r"^\|[\s:|-]+\|$", ln)
    ]
    # drop the header row
    table_rows = [ln for ln in table_rows if "Oracle file" not in ln]
    if table_rows and len(table_rows) != len(rows):
        errors.append(
            f"`## Oracle files` table has {len(table_rows)} rule row(s) but the JSON fence "
            f"has {len(rows)}; the table a person reads and the rules the guard applies "
            "must not drift apart"
        )
    for i, row in enumerate(rows):
        sev = row.get("severity")
        if i < len(table_rows) and sev and sev not in table_rows[i]:
            errors.append(
                f"oracle row {i} severity {sev!r} does not appear in the matching table row; "
                "table and JSON disagree"
            )
    return errors


def validate_recipe(path: Path, is_process: bool = False) -> list[str]:
    """Return a list of human-readable errors for one recipe (empty = valid).

    `is_process` is set for recipes under docs/process-recipes/ — they get the
    extra process-routing-key checks (section 6). Location is the source of truth
    for the class, not the frontmatter flag.
    """
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

    # 1b. Routing-token formats. `name` is a navigator cache key and `capability`
    #     is emitted into the index line — both must be clean single tokens (no
    #     spaces/brackets) so the line parses deterministically and names can't
    #     collide via whitespace differences.
    name = meta.get("name")
    if name is not None and not (isinstance(name, str) and NAME_RE.match(name)):
        errors.append(
            f"`name` must be snake_case matching {NAME_RE.pattern} "
            f"(lowercase letters, digits, underscores); found {name!r}"
        )
    capability = meta.get("capability")
    if capability is not None and not (
        isinstance(capability, str) and TOKEN_RE.match(capability)
    ):
        errors.append(
            f"`capability` must be a single token matching {TOKEN_RE.pattern} "
            f"(lowercase letters, digits, hyphens); found {capability!r}"
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

    # 5. Machine-readable `requires_*` frontmatter slugs resolve.
    #    Honors the contract recipe-loader relies on (degrade-paths.md:14 — dev-guides CI owns dangling
    #    requires_* slugs). OPTIONAL keys: checked only WHEN PRESENT, so older recipes with no machine
    #    deps stay valid and the degraded fall-through path remains supported.
    for key in ("requires_guides", "requires_plays"):
        decl = meta.get(key)
        if decl is None:
            continue
        if not isinstance(decl, list):
            errors.append(
                f"`{key}` must be a list of guide/play slugs (got {type(decl).__name__})"
            )
            continue
        for slug in decl:
            if not isinstance(slug, str) or not slug_resolves(slug):
                errors.append(
                    f"`{key}` slug does not resolve to a file: `{slug}` "
                    f"(expected docs/{slug}.md or docs/{slug}/index.md)"
                )

    # 6. Process-recipe routing keys (only for recipes under docs/process-recipes/).
    #    Routing is keyed by (phase × framework); `capability` IS the phase, so no
    #    separate applies_to_phase is required. When present, applies_to_phase must
    #    equal capability (catches divergence). The recipe_class flag is documentary
    #    but enforced so the file self-declares its class.
    if is_process:
        if meta.get("recipe_class") != "process":
            errors.append(
                f"process recipe must declare `recipe_class: process` "
                f"(found {meta.get('recipe_class')!r})"
            )
        framework = meta.get("framework")
        if not framework or not isinstance(framework, str):
            errors.append("process recipe must carry a `framework` routing key (string)")
        elif not TOKEN_RE.match(framework):
            errors.append(
                f"`framework` must be a single token matching {TOKEN_RE.pattern} "
                f"(lowercase letters, digits, hyphens); found {framework!r}"
            )
        atp = meta.get("applies_to_phase")
        if atp is not None and str(atp) != str(meta.get("capability", "")):
            errors.append(
                f"`applies_to_phase` is redundant for a process recipe and, when "
                f"present, must equal `capability` ({meta.get('capability')!r}); "
                f"found {atp!r}"
            )
    else:
        # Task recipes MAY optionally declare `framework` to override the
        # path-derived routing token generate_recipes.py emits on the index line
        # (`[<capability> framework=<token>]`). Optional — checked only when
        # present, so every existing recipe stays valid — but when present it must
        # be token-shaped, or the emitted line stops parsing for every consumer.
        fw = meta.get("framework")
        if fw is not None and not (isinstance(fw, str) and TOKEN_RE.match(fw)):
            errors.append(
                f"`framework` must be a single token matching {TOKEN_RE.pattern} "
                f"(lowercase letters, digits, hyphens); found {fw!r}"
            )
        if meta.get("recipe_class") == "process":
            errors.append(
                "`recipe_class: process` is only valid under docs/process-recipes/; "
                "move this file there so it routes to the process index, not the task index"
            )

    if is_process:
        errors.extend(validate_oracle_block(body))

    return errors


def main() -> int:
    # Scan both recipe roots. Location decides the class: docs/agentic-recipes/ →
    # task recipes; docs/process-recipes/ → process recipes (extra section-6 checks).
    roots = [(RECIPES_DIR, False), (PROCESS_RECIPES_DIR, True)]
    recipe_files: list[tuple[Path, bool]] = []
    for root, is_process in roots:
        if not root.is_dir():
            continue
        recipe_files.extend(
            (p, is_process)
            for p in sorted(root.rglob("*.md"))
            if p.name != "index.md"
        )

    if not recipe_files:
        print(
            "No recipe files under docs/agentic-recipes/ or docs/process-recipes/ "
            "— nothing to validate."
        )
        return 0

    total_errors = 0
    # name -> list of files declaring it, accumulated across BOTH roots. The
    # navigator keys its body cache by `name`; two recipes sharing a name would
    # silently collide there, so a duplicate is a global BLOCKER, not a per-file
    # one.
    names_seen: dict[str, list[Path]] = {}
    for path, is_process in recipe_files:
        rel = path.relative_to(PROJECT_ROOT)
        kind = "process" if is_process else "task"
        errors = validate_recipe(path, is_process=is_process)

        fm_yaml, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        try:
            meta = yaml.safe_load(fm_yaml) or {}
        except yaml.YAMLError:
            meta = {}
        name = meta.get("name")
        if isinstance(name, str) and name:
            names_seen.setdefault(name, []).append(rel)

        if errors:
            total_errors += len(errors)
            print(f"\nFAIL  [{kind}] {rel}")
            for err in errors:
                print(f"        - {err}")
        else:
            print(f"OK    [{kind}] {rel}")

    # Cross-file: `name` must be globally unique across both recipe roots.
    duplicates = {n: paths for n, paths in names_seen.items() if len(paths) > 1}
    if duplicates:
        for name, paths in sorted(duplicates.items()):
            total_errors += 1
            locations = ", ".join(str(p) for p in sorted(paths))
            print(
                f"\nFAIL  [global] duplicate recipe name {name!r} "
                f"(navigator cache key collision): {locations}"
            )

    print()
    if total_errors:
        print(f"Validation failed: {total_errors} error(s) across recipes.")
        return 1
    print(f"All {len(recipe_files)} recipe(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
