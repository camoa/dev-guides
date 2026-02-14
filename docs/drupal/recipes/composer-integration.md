---
description: Publish recipes as Composer packages for distribution and versioning
drupal_version: "11.x"
---

# Composer Integration & Publishing

## When to Use

> Use Composer packaging when you need to distribute recipes with version management and dependency resolution.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Recipe needs contrib modules | Add to `require` | Dependencies outside core |
| Recipe version matters | Use Git tags | Semantic versioning via Composer |
| Recipe is organization-internal | Private Packagist or artifact | Not public distribution |
| Recipe installer missing | Configure `drupal-recipe` type | Ensures installation to recipes directory |

## Pattern

Create composer.json (declare recipe package type):

```json
{
  "name": "myorg/my-recipe",
  "type": "drupal-recipe",
  "description": "My reusable recipe",
  "require": {
    "drupal/core": "^10.3 || ^11"
  }
}
```

Configure installer-paths:

```json
{
  "extra": {
    "installer-paths": {
      "recipes/{$name}": ["type:drupal-recipe"]
    }
  }
}
```

Publish to repository:

```bash
git tag v1.0.0
git push origin v1.0.0
# Submit to packagist.org or add to private repositories
```

Install via Composer:

```bash
composer require myorg/my-recipe
# Installs to recipes/my-recipe/
```

Apply installed recipe:

```bash
drush recipe recipes/my-recipe
```

## Common Mistakes

- **Wrong**: Forgetting `type: drupal-recipe` → **Right**: Composer treats as library; doesn't install to recipes directory
- **Wrong**: Not declaring module dependencies → **Right**: Modules must be installed before recipe applies; declare in composer.json
- **Wrong**: Hardcoding version constraints → **Right**: Use caret/tilde ranges for flexibility; `^10.3 || ^11` for Drupal 11 compatibility
- **Wrong**: Assuming recipes update → **Right**: Recipes are apply-once; version bumps don't re-apply; communicate to users
- **Wrong**: Not testing clean install → **Right**: Always test recipe on vanilla Drupal before publishing

## See Also

- [Default Content - Importing](default-content-importing.md)
- [Recipe Tooling](recipe-tooling.md)
- Reference: https://www.drupal.org/docs/extending-drupal/drupal-recipes
