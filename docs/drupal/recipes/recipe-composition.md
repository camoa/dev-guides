---
description: Compose granular recipes into complex functionality by declaring dependencies in the recipes key
tldr: "Use recipe composition when you need to build complex functionality from granular, reusable recipe building blocks."
drupal_version: "11.x"
---

# Recipe Composition & Dependencies

## When to Use

> Use recipe composition when you need to build complex functionality from granular, reusable recipe building blocks.

Compose granular recipes into complex functionality by declaring dependencies in the `recipes:` key.

## Steps: Declare and Resolve Dependencies

1. **List dependencies** — Order matters; dependencies apply first
   ```yaml
   name: 'Standard'
   recipes:
     - basic_block_type
     - article_content_type
     - page_content_type
   ```

2. **Dependency resolution** — RecipeConfigurator loads recipes recursively
   - Each recipe's dependencies apply before the recipe itself
   - Recipes applied in dependency-first order (graph sorting)
   - Duplicate recipes in graph apply only once

3. **Override patterns** — Later recipes override earlier config
   ```yaml
   recipes:
     - base_role       # Creates role with minimal permissions
     - enhanced_role   # Adds more permissions to same role
   ```

## Decision Points: Ordering and Circular Dependencies

| At this step... | If... | Then... |
|---|---|---|
| Ordering recipes | Recipes are independent | Order doesn't matter; list logically |
| Ordering recipes | Recipe B modifies Recipe A's config | List A before B; B's actions override |
| Handling circular deps | Recipe A needs B, B needs A | Validation prevents this; refactor into A → C ← B pattern |
| Recipe not found | Dependency path incorrect | Recipes resolved relative to parent recipe's directory or Composer |

## Common Mistakes

- Assuming recipe order doesn't matter → Config actions from later recipes override earlier ones
- Creating circular dependencies → Validation catches this but error is cryptic; design for directed acyclic graph
- Depending on unpublished recipes → Recipes must be discoverable via filesystem or Composer
- Listing same recipe twice → Deduplicated automatically but signals design issue
- Not understanding dependency depth → Dependencies are recursive; A→B→C means C applies before B before A

## See Also

- Previous: ← [Creating Your First Recipe](creating-first-recipe.md)
- Next: [Extension Installation](extension-installation.md) →
- Reference: `core/lib/Drupal/Core/Recipe/RecipeConfigurator.php`
