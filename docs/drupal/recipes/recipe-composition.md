---
description: Compose granular recipes into complex functionality by declaring dependencies in the recipes key
drupal_version: "11.x"
---

# Recipe Composition & Dependencies

## When to Use

> Use recipe composition when you need to build complex functionality from granular, reusable recipe building blocks.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Recipes are independent | Order doesn't matter | List logically for readability |
| Recipe B modifies Recipe A's config | List A before B | B's actions override A's config |
| Recipe A needs B, B needs A | Refactor into A → C ← B | Validation prevents circular dependencies |
| Dependency path incorrect | Use correct machine name or path | Recipes resolved relative to parent or Composer |

## Pattern

List dependencies in order:

```yaml
name: 'Standard'
recipes:
  - basic_block_type
  - article_content_type
  - page_content_type
```

Override pattern - later recipes override earlier config:

```yaml
recipes:
  - base_role       # Creates role with minimal permissions
  - enhanced_role   # Adds more permissions to same role
```

Dependency resolution:
- Each recipe's dependencies apply before the recipe itself
- Recipes applied in dependency-first order (graph sorting)
- Duplicate recipes in graph apply only once

## Common Mistakes

- **Wrong**: Assuming recipe order doesn't matter → **Right**: Config actions from later recipes override earlier ones
- **Wrong**: Creating circular dependencies → **Right**: Validation catches this; design for directed acyclic graph
- **Wrong**: Depending on unpublished recipes → **Right**: Recipes must be discoverable via filesystem or Composer
- **Wrong**: Listing same recipe twice → **Right**: Deduplicated automatically but signals design issue
- **Wrong**: Not understanding dependency depth → **Right**: Dependencies are recursive; A→B→C means C applies before B before A

## See Also

- [Creating Your First Recipe](creating-first-recipe.md)
- [Extension Installation](extension-installation.md)
- Reference: `core/lib/Drupal/Core/Recipe/RecipeConfigurator.php`
