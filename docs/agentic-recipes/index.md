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

**6. Every `## Verifier` check must declare its runnability — the consumer fail-closes on a check it cannot run.** The `ai-dev-assistant` plugin (v5.12.0+) runs each adopted recipe's `## Verifier` as a **hard-block review gate** and treats any check it *cannot* run as **unresolved → fail-closed HALT**, never a silent "skipped → pass". So a check that is ambiguously specified or depends on something the `## Input contract` doesn't provide will spuriously block a review. Classify every check as one of:

- **`config-assert`** — reads config/state via `drush` / file reads; deterministic, no served site needed.
- **`live-site`** — fetches a served page and asserts on the response/DOM; needs a served site. Its absence is a *correct* fail-close, not a recipe defect — say so explicitly so the consumer treats a no-site environment as expected.
- **`self-fixture`** — needs a state change to observe, so the check **creates and cleans up its own fixture** (e.g. create a node, regenerate its alias, assert the 301, delete it). Prefer this over assuming an operator-supplied fixture: a check that depends on a node/entity the input contract doesn't identify is non-deterministic and will fail-close.

Never write a blanket "manual / does not ship an executable verifier" line that implies the checks can't be run automatically — **"ships no script" ≠ "not runnable"**. Each check is a method the consumer runs.

## See also

- File-format standard: `recipe_schema_version 1.0.0` — routing-first frontmatter, fixed body section set, verifier required.
- Machine-readable dependencies (**optional**): a recipe body may declare `requires_guides:` and `requires_plays:` — lists of guide/play slugs (e.g. `drupal/image-styles/image-overview`) the recipe-loader resolves **without parsing prose**. Each slug must resolve to a published guide/play (`docs/<slug>.md` or `docs/<slug>/index.md`); `scripts/validate_recipes.py` (run in CI) fails the build on a dangling slug. A recipe that omits them still matches — its aspects fall through to residual guide-search. These keys live in the **recipe body** (fetched raw on match), not the routing index.
- [Drupal best-practice plays](../drupal/best-practices/camoa/index.md) — the prescriptive stances recipes cite as sources.
