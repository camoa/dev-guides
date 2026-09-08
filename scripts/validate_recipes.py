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
TOOLING_RECIPES_DIR = DOCS_DIR / "tooling-recipes"  # tooling recipes (location = class)

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

# A tooling recipe says what a tool is, how to install it, and how to run it.
# Three headings, deliberately: Run is also the check, so there is no verifier
# section, and an install step that needs something absent fails with that
# thing's own message, so there is no preconditions section. Grow this list when
# a real recipe needs more, with that recipe as the reason.
TOOLING_REQUIRED_SECTIONS = ["Goal", "Install", "Run"]

SECTIONS_BY_KIND = {
    "task": REQUIRED_SECTIONS,
    "process": REQUIRED_SECTIONS,
    "tooling": TOOLING_REQUIRED_SECTIONS,
}

# A tooling recipe is read by a machine as well as by a person: something resolves
# the recipe and runs what it finds. Reading by position — "the first fence under
# Install" — truncates a two-step install silently, which is how the first pair of
# live recipes ran `composer config` without its `composer require` and reported
# success. So the info string is the contract: `sh` means run this block, any other
# label means read it. Nothing below inspects what a block says, so nothing guesses.
TOOLING_COMMAND_TAG = "sh"
FENCE_LINE_RE = re.compile(r"^\s*```(.*)$")

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


def section_lines(body: str, heading: str, line_offset: int) -> list[tuple[int, str]] | None:
    """Lines of one `## <heading>` section, bounded at the next H2.

    Each entry is (file line number, text) so an error can name where to look.
    Returns None when the heading is absent — a missing section is already
    reported by the required-sections check, and reporting it twice reads as two
    problems.
    """
    lines = body.splitlines()
    heading_re = re.compile(r"^##\s+" + re.escape(heading) + r"\s*$")
    start = next((i + 1 for i, ln in enumerate(lines) if heading_re.match(ln)), None)
    if start is None:
        return None
    out: list[tuple[int, str]] = []
    for i in range(start, len(lines)):
        if lines[i].startswith("## "):
            break
        out.append((line_offset + i + 1, lines[i]))
    return out


def fenced_blocks(section: list[tuple[int, str]]) -> list[tuple[int, str, list[str]]]:
    """(opening line number, info string, content lines) per fence in a section.

    The info string is stripped, so `sh` and `sh ` are the same tag — a trailing
    space is invisible in an editor, and a correctly tagged block must not be
    skipped for one.
    """
    blocks: list[tuple[int, str, list[str]]] = []
    open_at: tuple[int, str] | None = None
    content: list[str] = []
    for lineno, line in section:
        m = FENCE_LINE_RE.match(line)
        if not m:
            if open_at is not None:
                content.append(line)
            continue
        if open_at is None:
            open_at = (lineno, m.group(1).strip())
            content = []
        else:
            blocks.append((open_at[0], open_at[1], content))
            open_at = None
    if open_at is not None:  # unclosed fence; report what was opened
        blocks.append((open_at[0], open_at[1], content))
    return blocks


def tooling_fence_errors(body: str, line_offset: int) -> list[str]:
    """Check the fence labels under `## Install` and `## Run` of a tooling recipe."""
    errors: list[str] = []
    for heading in ("Install", "Run"):
        section = section_lines(body, heading, line_offset)
        if section is None:
            continue
        blocks = fenced_blocks(section)
        for lineno, info, _ in blocks:
            if not info:
                errors.append(
                    f"line {lineno}: fenced block under `## {heading}` carries no info "
                    f"string; tag it `{TOOLING_COMMAND_TAG}` to have it run, or anything "
                    "else (`text`) to have it read"
                )
        commands = [b for b in blocks if b[1] == TOOLING_COMMAND_TAG]
        if heading == "Install" and not commands:
            errors.append(
                f"`## Install` carries no block tagged `{TOOLING_COMMAND_TAG}`; the "
                "commands that add the tool go in tagged blocks, read in order"
            )
        if heading == "Run":
            if len(commands) != 1:
                errors.append(
                    f"`## Run` carries {len(commands)} blocks tagged "
                    f"`{TOOLING_COMMAND_TAG}`; exactly one is the command to run — tag a "
                    "worked example `text` so it is read rather than executed"
                )
            for lineno, _, content in commands:
                # One command, so a reader cannot take the first line, drop the
                # rest, and report a success nobody got.
                body_lines = [ln for ln in content if ln.strip()]
                if len(body_lines) != 1:
                    errors.append(
                        f"line {lineno}: the `{TOOLING_COMMAND_TAG}` block under `## Run` "
                        f"holds {len(body_lines)} commands; Run is one command"
                    )
    return errors


def validate_recipe(path: Path, kind: str = "task") -> list[str]:
    """Return a list of human-readable errors for one recipe (empty = valid).

    `kind` is derived from the directory: docs/agentic-recipes/ -> "task",
    docs/process-recipes/ -> "process", docs/tooling-recipes/ -> "tooling".
    Location is the source of truth for the class, not the frontmatter flag —
    the flag is enforced so the file self-declares, and rejected outside its own
    root so a misfiled recipe cannot route to the wrong index.
    """
    is_process = kind == "process"
    is_tooling = kind == "tooling"
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
    for section in SECTIONS_BY_KIND[kind]:
        if section not in headings:
            errors.append(f"missing required section: ## {section}")

    # 3b. Tooling recipes: the fences under Install and Run say what they are.
    if is_tooling:
        errors.extend(tooling_fence_errors(body, text[: len(text) - len(body)].count("\n")))

    # 4. Citations resolve.
    #    Skipped for tooling recipes: a tooling recipe cites no guide by design —
    #    it names packages and commands — and a package name is character-for-
    #    character indistinguishable from a guide slug (`drupal/coder`,
    #    `phpstan/phpstan`). Running this check there reports every package as a
    #    dangling citation.
    for slug in sorted(() if is_tooling else cited_slugs(body)):
        if not slug_resolves(slug):
            errors.append(
                f"cited guide/play does not resolve to a file: `{slug}` "
                f"(expected docs/{slug}.md or docs/{slug}/index.md)"
            )

    # 4b. `requires_tooling` names resolve to a tooling recipe for THIS framework.
    #     A process recipe knows which tools its method needs; the caller only knows
    #     it wants a standards check, not that a Drupal standards check means phpcs.
    #     The tool name is the whole contract, so a name that resolves to nothing has
    #     to fail here — at publish — rather than on the machine of whoever runs it.
    #     Resolution is per framework on purpose: the same tool installs differently
    #     per stack, which is why phpunit is two recipes and not one.
    #     OPTIONAL, checked only when present, so a recipe whose framework has no
    #     tooling recipes yet stays valid.
    decl = meta.get("requires_tooling")
    if decl is not None:
        if not isinstance(decl, list):
            errors.append(
                f"`requires_tooling` must be a list of tool names (got {type(decl).__name__})"
            )
        else:
            fw = meta.get("framework")
            for tool in decl:
                if not isinstance(tool, str) or not TOKEN_RE.match(tool):
                    errors.append(
                        f"`requires_tooling` entry must be a single lowercase token naming a "
                        f"tool (got {tool!r})"
                    )
                    continue
                if not fw:
                    errors.append(
                        f"`requires_tooling` names `{tool}` but the recipe declares no "
                        "`framework`; a tool resolves per framework, so it cannot be checked"
                    )
                    continue
                if not (TOOLING_RECIPES_DIR / str(fw) / f"{tool}.md").is_file():
                    errors.append(
                        f"`requires_tooling` names `{tool}`, which has no tooling recipe for "
                        f"framework `{fw}` (expected docs/tooling-recipes/{fw}/{tool}.md)"
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
    elif is_tooling:
        # 6b. Tooling-recipe routing keys. Routing is keyed by (tool x framework);
        #     `capability` carries the tool name, which is unambiguous because the
        #     directory already fixed the class before anything reads it. The
        #     recipe_class flag is enforced so the file self-declares.
        if meta.get("recipe_class") != "tooling":
            errors.append(
                f"tooling recipe must declare `recipe_class: tooling` "
                f"(found {meta.get('recipe_class')!r})"
            )
        framework = meta.get("framework")
        if not framework or not isinstance(framework, str):
            errors.append("tooling recipe must carry a `framework` routing key (string)")
        elif not TOKEN_RE.match(framework):
            errors.append(
                f"`framework` must be a single token matching {TOKEN_RE.pattern} "
                f"(lowercase letters, digits, hyphens); found {framework!r}"
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
        declared = meta.get("recipe_class")
        if declared in ("process", "tooling"):
            root = "process-recipes" if declared == "process" else "tooling-recipes"
            errors.append(
                f"`recipe_class: {declared}` is only valid under docs/{root}/; "
                f"move this file there so it routes to the {declared} index, "
                "not the task index"
            )

    if is_process:
        errors.extend(validate_oracle_block(body))

    return errors


def main() -> int:
    # Scan both recipe roots. Location decides the class: docs/agentic-recipes/ →
    # task recipes; docs/process-recipes/ → process recipes (extra section-6 checks).
    roots = [
        (RECIPES_DIR, "task"),
        (PROCESS_RECIPES_DIR, "process"),
        (TOOLING_RECIPES_DIR, "tooling"),
    ]
    recipe_files: list[tuple[Path, str]] = []
    for root, kind in roots:
        if not root.is_dir():
            continue
        recipe_files.extend(
            (p, kind)
            for p in sorted(root.rglob("*.md"))
            if p.name != "index.md"
        )

    if not recipe_files:
        print(
            "No recipe files under docs/agentic-recipes/, docs/process-recipes/ "
            "or docs/tooling-recipes/ — nothing to validate."
        )
        return 0

    total_errors = 0
    # name -> list of files declaring it, accumulated across BOTH roots. The
    # navigator keys its body cache by `name`; two recipes sharing a name would
    # silently collide there, so a duplicate is a global BLOCKER, not a per-file
    # one.
    names_seen: dict[str, list[Path]] = {}
    for path, kind in recipe_files:
        rel = path.relative_to(PROJECT_ROOT)
        errors = validate_recipe(path, kind=kind)

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
