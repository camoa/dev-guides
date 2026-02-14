---
description: Drupal Recipes compose reusable functionality into packages for shareable, tested configuration patterns
drupal_version: "11.x"
---

# Recipe System Overview

## When to Use

> Use Drupal Recipes (core since 10.3.0, May 2024) when you need shareable, tested configuration patterns that can be applied to any Drupal site. Use distributions for full site builds, config split for environment-specific config.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Full site with opinionated defaults from scratch | Distribution | Replaces entire installation profile, controls all config |
| Reusable configuration patterns to apply to existing sites | Recipe | Composable, shareable, can be applied post-install |
| Environment-specific config | Config Split | Manages config variations across environments |
| Historical install profile replacement | Recipe + custom code | Install profiles are deprecated, recipes are the modern replacement |

## Pattern

The five pillars of recipes: extensions, config, config actions, default content, and config checkpoints (rollback on failure).

```yaml
name: 'Content editor role'
description: 'Provides the Content editor role.'
type: 'User role'
install:
  - node
config:
  strict: false
  actions:
    user.role.content_editor:
      grantPermissions:
        - 'access administration pages'
```

RecipeRunner processes recipes in order: dependent recipes → install extensions → import config → apply config actions → import default content → trigger RecipeAppliedEvent. Config Checkpoint API creates snapshots before each step; on failure, config rolls back to pre-recipe state.

**Recipes are ephemeral** — once applied, the results become the site's responsibility. There is no "unapply" or managed state. The recipe itself is not tracked after application.

## Common Mistakes

- **Wrong**: Using install profiles for shareable functionality → **Right**: Install profiles are deprecated, use recipes
- **Wrong**: Hardcoding site-specific values → **Right**: Use the input system for environment-specific values
- **Wrong**: Treating recipes as migrations → **Right**: Recipes bootstrap sites, migrations transfer data
- **Wrong**: Applying recipes multiple times expecting updates → **Right**: Recipes are apply-once; config is permanent after application
- **Wrong**: Ignoring strict mode implications → **Right**: Strict mode validates existing config matches recipe expectations
- **Wrong**: Expecting recipes to contain custom code → **Right**: Recipes are declarative YAML only; use modules for custom logic
- **Wrong**: Expecting dynamic behavior → **Right**: No conditionals, loops, or runtime logic; static configuration only
- **Wrong**: Expecting upgrade paths → **Right**: Recipes have no update mechanism; version changes require manual migration

## See Also

- [Recipe YAML Schema](recipe-yaml-schema.md)
- Reference: `core/lib/Drupal/Core/Recipe/RecipeRunner.php`
- Reference: https://www.drupal.org/docs/extending-drupal/drupal-recipes
