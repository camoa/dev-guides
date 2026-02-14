---
description: Follow this workflow to create a minimal working recipe from scratch
drupal_version: "11.x"
---

# Creating Your First Recipe

## When to Use

> Follow this workflow to create a minimal working recipe from scratch.

## Decision

| At this step | Choose | Why |
|--------------|--------|-----|
| Adding configuration - simple and static | Use `config/` directory | For config files that don't need dynamic updates |
| Adding configuration - needs dynamic updates | Use `config.actions` | For config actions that merge with existing config |
| Choosing strict mode - setting up new functionality | Use `strict: false` | Allows existing config, flexible application |
| Choosing strict mode - enforcing specific config state | Use `strict: true` or array | Validates config matches expectations |

## Pattern

Create recipe directory:

```bash
mkdir -p recipes/my_recipe
```

Write minimal recipe.yml:

```yaml
name: 'My Recipe'
description: 'Example recipe.'
type: 'Feature'
install:
  - node
config:
  strict: false
```

Add configuration (optional):

```bash
mkdir -p recipes/my_recipe/config
drush config:export --destination=recipes/my_recipe/config
```

Apply the recipe:

```bash
# Drush (recommended)
drush recipe recipes/my_recipe

# Core script (no Drush)
php core/scripts/drupal recipe recipes/my_recipe
```

## Common Mistakes

- **Wrong**: Applying recipe before installing required modules → **Right**: Use `install:` key to declare dependencies
- **Wrong**: Putting recipe.yml in wrong location → **Right**: Must be in recipe root directory, not subdirectory
- **Wrong**: Using `config:` key without understanding strict mode → **Right**: Defaults to `strict: true` in current core (may change)
- **Wrong**: Not testing recipe on clean install → **Right**: Recipes should be idempotent but are designed for apply-once
- **Wrong**: Forgetting composer.json for published recipes → **Right**: Recipes distributed via Composer need `type: drupal-recipe`

## See Also

- [Recipe YAML Schema](recipe-yaml-schema.md)
- [Recipe Composition & Dependencies](recipe-composition.md)
- Reference: https://project.pages.drupalcode.org/distributions_recipes/recipe.html
