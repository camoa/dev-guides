---
description: Step-by-step workflow for creating image styles via YAML config with UUID generation, file placement, and import verification
---

# Creating Image Styles via Config

## When to Use

> Use this when you need to create an image style via YAML config for version control, recipes, or distribution.

## Steps

### 1. Generate UUID for each effect

```bash
# Using Drush
drush php-eval "echo \Drupal::service('uuid')->generate() . PHP_EOL;"

# Using uuidgen (Linux)
uuidgen | tr '[:upper:]' '[:lower:]'
```

### 2. Create YAML file

At `config/install/image.style.{machine_name}.yml` (for new modules/themes) or `config/sync/image.style.{machine_name}.yml` (for active config)

```yaml
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

### 3. Import config

```bash
# Full config import
drush config:import

# Single config import
drush config:import --partial --source=modules/custom/my_module/config/install
```

### 4. Verify image style

```bash
# List all image styles
drush config:get image.style

# Get specific style
drush config:get image.style.hero_large
```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Step 1 (UUID generation) | You're creating multiple effects | Generate a UUID for each effect, track in a text file |
| Step 2 (File location) | Distributing in module/theme | Use `config/install/` for default config |
| Step 2 (File location) | Site-specific active config | Use `config/sync/` and commit to git |
| Step 3 (Import) | Config already exists | Use `--partial` to override, or delete existing first |

## Common Mistakes

- Reusing UUIDs across effects → Only one effect executes, silent data loss
- Wrong file path for config → Config never imported, style missing
- Missing dependencies declaration → Style imported but breaks on referenced style deletion
- Not clearing cache after import → Old style cached, changes not visible
- Importing config with UUID key at top → Should be removed for install config, kept for sync config

## See Also

- [Image Style Config Schema](image-style-schema.md)
- [Core Image Effects](core-image-effects.md)
- [Config Export & Recipes](config-export-recipes.md)
- Reference: core/lib/Drupal/Core/Config/ConfigInstaller.php
