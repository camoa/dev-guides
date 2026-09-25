---
description: Agentic recipes — goal-oriented, prescriptive capability deliveries that sequence existing guides and plays end to end, each with a verifier.
---

# Agentic Recipes

> Not to be confused with [Drupal core recipes](../drupal/recipes/index.md) (declarative `recipe.yml` config packages). An **agentic recipe** is the AI-native equivalent: a set of *agentic* steps carrying the reasoning, derivation, gating, and invocation a declarative format cannot. One recipe delivers **one named capability** end to end.

A recipe is **prescriptive, not descriptive**. "How X works in Drupal" is a guide; "how *we* do X, and what we refuse to do" is a recipe. A recipe **cites guides and plays, never duplicates them**, and is not a recipe at all unless it carries a name an agent can route to, the constraint it enforces, and a **verifier** that catches the agent when it drifts.

Recipes are published to a separate index, `agentic-recipes.txt` (not `llms.txt`), exposing only each recipe's routing block (`name` / `capability` / `description`). A caller matches a capability first, loads the recipe, and the recipe names the guides it needs.

## Routing table

| Capability | Recipe | When to use |
|---|---|---|
| `responsive-image-delivery` | [Responsive image wiring](drupal/responsive-image-wiring.md) | A Drupal site has named image use-cases (hero, card thumbnail, content inline) that must render as responsive images on image fields. |
| `drupal-seo-foundation` | [Drupal SEO foundation](drupal/drupal-seo-foundation.md) | A Drupal site needs its SEO/GEO foundation wired to an opinionated, verifier-gated contract — metatag per bundle, Schema.org/JSON-LD, sitemap, pathauto + redirect, robots. |
| `drupal-module-test-authoring` | [Drupal module test authoring](drupal/module-test-authoring.md) | A Drupal module needs tests written or extended: which kind each behaviour gets, written to the conventions current core and PHPUnit enforce, and proved by a run whose output was read. |
| `drupal-dependency-update` | [Drupal dependency update](drupal/dependency-update.md) | A Drupal site must update named packages, the whole site, or core along a version path, and reach a stable point with nothing pending and every moved package reported. |
| `pathauto-alias-pattern-configuration` | [Configure Pathauto alias pattern](drupal/configure-pathauto-alias-pattern.md) | A single bundle or vocabulary needs a clean URL-alias pattern via Pathauto, scoped with a selection-criteria condition — not a full SEO build. |
| `content-moderation-workflow-provisioning` | [Content moderation workflow](drupal/content-moderation-workflow.md) | A content type needs an editorial workflow via core content_moderation + workflows — states, transitions, and backfilling existing content. |
| `editorial-roles-permissions-provisioning` | [Editorial roles & permissions](drupal/editorial-roles-permissions.md) | A site needs its editorial content roles — a single content_editor or a two-tier author/editor split, granted per bundle, never via `is_admin`. |
| `content-type-field-provisioning` | [Provision content type fields](drupal/provision-content-type-fields.md) | A content type needs its fields defined — per-field storage decisions, shared storages, custom compound fields only where genuinely polymorphic. |
| `drupal-site-template-publishing` | [Site template publishing](drupal/site-template-publishing.md) | A working Drupal CMS site must become a standalone, marketplace-compliant site template, exported from a disposable scratch install. |
| `layout-builder-editorial-wiring` | [Wire Layout Builder for editorial use](drupal/wire-layout-builder-editorial.md) | A content type must be handed to editors to compose pages in Layout Builder — palette curation, repeating sections, and editor-UX hardening. |

## Authoring an agentic recipe

An agentic recipe is authored to the **same `recipe_schema_version 1.0.0` standard** as a process recipe — same validator (`scripts/validate_recipes.py`, run in CI over both recipe roots), same required sections. It differs only in **where it lives** and in **what `capability` means**.

**1. Location is the class.** Put the file at `docs/agentic-recipes/<domain>/<name>.md`. Anything under this root is an agentic (task) recipe and is published to `agentic-recipes.txt` — matched **by capability** during free task routing. (Process recipes live under `docs/process-recipes/` and are matched only by `(phase × framework)`.)

**2. Routing-first frontmatter** (first three keys, in order):

```yaml
name: drupal_seo_foundation        # globally unique, snake_case
capability: drupal-seo-foundation  # the CAPABILITY an agent routes to — not a lifecycle phase
description: Use when …            # single-line when-to-use trigger
```

Unlike a process recipe, `capability` is a free task capability; there is **no** `framework` / `recipe_class: process` routing pair.

**3. Required metadata:**

```yaml
label: Drupal SEO foundation
recipe_schema_version: 1.0.0
version: 0.2.1
```

Optional machine-readable dependencies — `requires_guides:` / `requires_plays:` — list guide/play slugs the `recipe-loader` resolves without parsing prose; each must resolve to a published `docs/<slug>.md` or `docs/<slug>/index.md` (CI fails the build on a dangling slug). Any other keys (`drupal_compatibility`, `requires_modules`, `escalation_policy`, …) are free-form — the validator ignores them.

**4. Required body sections** (the same nine as every recipe): `Goal`, `Opinion`, `Preconditions`, `Input contract`, `Sequence`, `Data flow`, `State-awareness contract`, `Verifier`, `References`.

**5. Reference, don't duplicate; don't bake in examples.** A recipe cites guides and plays for *mechanics* and carries only the prescriptive stance and the sequencing. The `## Input contract` is a **generic schema** the operator fills — do not bake operator-specific input values or worked examples into the body.

**6. Every `## Verifier` check must declare its runnability — the consumer fail-closes on a check it cannot run.** The `aida` plugin (6.0.0-beta.26) runs each `verifier:` entry of the covering recipe as the work order's own proof, and reads any entry it *cannot* run as **unknown → fail-closed**, never a silent "skipped → pass". So a check that is ambiguously specified or depends on something the `## Input contract` doesn't provide will spuriously block the build. Classify every check as one of:

- **`config-assert`** — reads config/state via `drush` / file reads; deterministic, no served site needed.
- **`live-site`** — fetches a served page and asserts on the response/DOM; needs a served site. Its absence is a *correct* fail-close, not a recipe defect — say so explicitly so the consumer treats a no-site environment as expected.
- **`self-fixture`** — needs a state change to observe, so the check **creates and cleans up its own fixture** (e.g. create a node, regenerate its alias, assert the 301, delete it). Prefer this over assuming an operator-supplied fixture: a check that depends on a node/entity the input contract doesn't identify is non-deterministic and will fail-close.

Never write a blanket "manual / does not ship an executable verifier" line that implies the checks can't be run automatically — **"ships no script" ≠ "not runnable"**. Each check is an entry of the `verifier:` block (rule 7).

**7. `## Verifier` is one `verifier:` block, and nothing outside it is a check.** Consumer: `aida` 6.0.0-beta.26. Each entry carries four keys:

- `id` — lowercase and hyphenated, unique in the recipe.
- `kind` — `config-assert`, `live-site` or `self-fixture`, rule 6's three kinds.
- `run` — one command, run from the project root. AIDA reads the block line by line, not as YAML: the value is the rest of the key's own line, with one pair of outer quotes removed from `run` and `pass` only; `id` and `kind` keep any quotes, so leave them unquoted. So write `run` and `pass` on one line, with no `#` comment and no block scalar (`>-`, `|`). It is split on spaces and never run through a shell. It carries none of `` ` $ ; & | < > ( ) \ " ' ``, and no tab or newline.
- `pass` — `exit 0`, `stdout empty` or `stdout contains <literal>`. A non-zero exit fails the entry whatever `pass` says. `stdout empty` and `stdout contains` read standard output only.

A placeholder is a whole token, never part of one. `{field}` or `{a.b}` names an `## Input contract` field by its dotted path. A list field runs the entry once per item. AIDA multiplies the line by the first placeholder in it that has more than one value; any other list placeholder in that line takes its first item. An empty list, or an absent bare field, reads unknown — never a pass. `{a.b:json}` passes the field's whole value as one JSON token, and `null` when the field is absent; give every optional field the `:json` form. Nothing substitutes inside a token, and nothing substitutes inside a `stdout contains` literal.

AIDA also supplies three placeholders that no `## Input contract` field names: `{paths}` and `{file}` give the files the work order owns, one argument each, and `{dirs}` gives their folders. `drupal/module-test-authoring.md` uses `{paths}`. An order that owns no file gets no argument at all, and the entry still runs. So a script called with `{paths}` must print a violation when it receives no file; otherwise `stdout empty` passes falsely.

A check that needs more than one command ships a script in `## Files`: a fenced block ```` ```<lang> .aida/<recipe-slug>/<file> ```` under that heading. AIDA writes it into the worktree only for the verify run, and removes it after. Never commit it. Never gitignore it. It is written without the execute bit, so `run` calls it through an interpreter — `bash .aida/<slug>/verify.sh …` or `ddev drush php:script /var/www/html/.aida/<slug>/verify.php -- …`. Keep the recipe's frontmatter `name:` stable across versions: AIDA recognises an earlier version of a shipped file by that name. A recipe that ships `## Files` must not check `git status` cleanliness — its own script is untracked during the run. The same holds across recipes: AIDA writes the files of every recipe an order cites before any entry runs. So one order must not cite both `drupal/dependency-update.md`, whose `all-committed` entry checks `git status`, and a recipe that ships `## Files`. A target file that already exists with the same bytes is kept, and not removed after the run. If it exists with different content, AIDA replaces it only when it matches an earlier version of the recipe that this machine's navigator store holds. Otherwise AIDA stops the whole build step at exit 3; no entry gets a verdict.

The site must be running before the verify run. `ddev drush` and `ddev exec` both start a stopped DDEV project, and DDEV prints its start-up text on standard output. That text fails every `stdout empty` entry (fail-closed, never a false pass). A recipe's note that `ddev drush` keeps messages on standard error holds for Drush, not for DDEV's start-up.

Text after the block is a note for readers. Write it as bullets, never as a numbered list: a numbered item under `## Verifier` is read as a model-judged check. `drupal/dependency-update.md` is the model.

AIDA documents this contract at `aida/skills/implement/references/build.md`, "Record the attempt", and `aida/skills/design/SKILL.md`, "Carry the proof from its source" (camoa-skills).

## See also

- File-format standard: `recipe_schema_version 1.0.0` — routing-first frontmatter, fixed body section set, verifier required.
- Machine-readable dependencies (**optional**): a recipe body may declare `requires_guides:` and `requires_plays:` — lists of guide/play slugs (e.g. `drupal/image-styles/image-overview`) the recipe-loader resolves **without parsing prose**. Each slug must resolve to a published guide/play (`docs/<slug>.md` or `docs/<slug>/index.md`); `scripts/validate_recipes.py` (run in CI) fails the build on a dangling slug. A recipe that omits them still matches — its aspects fall through to residual guide-search. These keys live in the **recipe body** (fetched raw on match), not the routing index.
- [Drupal best-practice plays](../drupal/best-practices/camoa/index.md) — the prescriptive stances recipes cite as sources.
