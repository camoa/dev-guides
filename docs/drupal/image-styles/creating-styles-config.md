---
description: Create an image style via YAML config
drupal_version: "11.x"
---

# Creating Image Styles via Config

## When to Use

> Use this when creating an image style via YAML config for version control, recipes, or distribution.

## Pattern

1. **Generate UUID for each effect**

   ```bash
   drush php-eval "echo \Drupal::service('uuid')->generate() . PHP_EOL;"
   # or: uuidgen | tr '[:upper:]' '[:lower:]'
   ```

2. **Create YAML file**

   ```yaml
   # config/install/image.style.hero_large.yml
   langcode: en
   status: true
   dependencies: { }
   name: hero_large
   label: 'Hero Large (1200x600)'
   effects:
     f4e8d9c0-1a2b-3c4d-5e6f-7a8b9c0d1e2f:
       uuid: f4e8d9c0-1a2b-3c4d-5e6f-7a8b9c0d1e2f
       id: image_scale_and_crop
       weight: 0
       data:
         width: 1200
         height: 600
         anchor: center-center
     a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d:
       uuid: a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d
       id: image_convert_avif
       weight: 1
       data:
         extension: webp
   ```

3. **Import config**

   ```bash
   drush config:import
   # or: drush config:import --partial --source=modules/custom/my_module/config/install
   ```

4. **Verify**

   ```bash
   drush config:get image.style.hero_large
   ```

## Decision

| At this step... | If... | Then... |
|---|---|---|
| UUID generation | Creating multiple effects | Generate a UUID for each, track in a text file |
| File location | Distributing in module/theme | Use `config/install/` for default config |
| File location | Site-specific active config | Use `config/sync/` and commit to git |
| Import | Config already exists | Use `--partial` to override, or delete existing first |

## Common Mistakes

- **Wrong**: Reusing UUIDs across effects → **Right**: Generate unique UUID per effect (only one effect executes, silent data loss)
- **Wrong**: Wrong file path for config → **Right**: Use config/install or config/sync as appropriate (config never imported, style missing)
- **Wrong**: Missing dependencies declaration → **Right**: Declare config dependencies (style imported but breaks on referenced style deletion)
- **Wrong**: Not clearing cache after import → **Right**: Run `drush cr` after import (old style cached, changes not visible)

## See Also

- [Image Style Config Schema](image-style-schema.md)
- [Core Image Effects](core-image-effects.md)
- [Config Export & Recipes](config-export-recipes.md)
- Reference: core/lib/Drupal/Core/Config/ConfigInstaller.php
