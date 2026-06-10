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

## See also

- File-format standard: `recipe_schema_version 1.0.0` — routing-first frontmatter, fixed body section set, verifier required.
- [Drupal best-practice plays](../drupal/best-practices/camoa/index.md) — the prescriptive stances recipes cite as sources.
