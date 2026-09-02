---
description: Publish recipes as Composer packages for distribution and versioning
tldr: "Use Composer packaging when you need to distribute recipes with version management and dependency resolution."
drupal_version: "11.x"
---

# Composer Integration & Publishing

## When to Use

> Use Composer packaging when you need to distribute recipes with version management and dependency resolution.

Publish recipes as Composer packages for distribution and versioning.

## Steps: Package, Publish and Install a Recipe

1. **Create composer.json** — Declare recipe package type
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

2. **Configure installer-paths** — Recipe installer places recipes correctly
   ```json
   {
     "extra": {
       "installer-paths": {
         "recipes/{$name}": ["type:drupal-recipe"]
       }
     }
   }
   ```

3. **Publish to repository** — Push to Packagist or private repo
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   # Submit to packagist.org or add to private repositories
   ```

4. **Install via Composer** — Require recipe in project
   ```bash
   composer require myorg/my-recipe
   # Installs to recipes/my-recipe/
   ```

5. **Apply installed recipe** — Use Drush or core script
   ```bash
   drush recipe recipes/my-recipe
   ```

## Decision Points: Dependencies, Versioning and Distribution

| At this step... | If... | Then... |
|---|---|---|
| Recipe needs contrib modules | Dependencies outside core | Add to `require` in composer.json |
| Recipe version matters | Semantic versioning needed | Use Git tags; Composer handles versions |
| Recipe is organization-internal | Not public | Use private Packagist or artifact repository |
| Recipe installer missing | Custom Composer setup | Ensure `drupal-recipe` type has installer configured |

## Common Mistakes

- Forgetting `type: drupal-recipe` → Composer treats as library; doesn't install to recipes directory
- Not declaring module dependencies → Modules must be installed before recipe applies; declare in composer.json
- Hardcoding version constraints → Use caret/tilde ranges for flexibility; `^10.3 || ^11` for Drupal 11 compatibility
- Assuming recipes update → Recipes are apply-once; version bumps don't re-apply; communicate to users
- Not testing clean install → Always test recipe on vanilla Drupal before publishing

## See Also

- Previous: ← [Default Content - Importing](default-content-importing.md)
- Next: [Recipe Tooling](recipe-tooling.md) →
- Reference: https://www.drupal.org/docs/extending-drupal/drupal-recipes
