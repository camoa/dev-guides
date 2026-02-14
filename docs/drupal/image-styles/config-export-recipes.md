---
description: Export image styles or create a recipe
drupal_version: "11.x"
---

# Config Export & Recipes

## When to Use

> Use this when exporting image styles for version control or creating a recipe to distribute image styles as reusable config.

## Pattern - Config Export

1. **Export specific image style**

   ```bash
   drush config:export image.style.large --destination=/tmp/config
   # or all: drush config:export --destination=config/sync
   ```

2. **Export for module/theme distribution**

   ```bash
   cp config/sync/image.style.hero_large.yml modules/custom/my_module/config/install/
   sed -i '1d' modules/custom/my_module/config/install/image.style.hero_large.yml  # Remove UUID
   ```

3. **Export responsive image styles with dependencies**

   ```bash
   drush config:export responsive_image.styles.hero
   drush config:export image.style.hero_small
   drush config:export image.style.hero_medium
   drush config:export image.style.hero_large
   ```

## Pattern - Creating a Recipe

1. **Create recipe directory structure**

   ```
   recipes/my_images/
   ├── recipe.yml
   └── config/
       ├── image.style.hero_large.yml
       ├── image.style.hero_medium.yml
       └── responsive_image.styles.hero.yml
   ```

2. **Create recipe.yml**

   ```yaml
   name: 'Hero Image Styles'
   description: 'Provides hero image styles and responsive variants.'
   type: 'Image styles'
   install:
     - responsive_image
   config:
     strict: false
     import:
       image: '*'
       responsive_image: '*'
   ```

3. **Apply recipe**

   ```bash
   drush recipe recipes/my_images
   ```

## Recipe Config Options

| Option | Value | Description |
|---|---|---|
| `strict: true` | Conflict error | Fails if config already exists |
| `strict: false` | Override | Updates existing config, safer for updates |
| `import: image: '*'` | All image styles | Imports all image.style.* from config/ |
| `import: image: 'hero_*'` | Prefix match | Imports only matching config |

## Config Dependencies

Always declare dependencies in responsive image style config:

```yaml
# responsive_image.styles.hero.yml
dependencies:
  config:
    - image.style.hero_small
    - image.style.hero_medium
    - image.style.hero_large
  module:
    - responsive_image
```

## Common Mistakes

- **Wrong**: Exporting config with UUID for module distribution → **Right**: Remove UUID line from install config (config import fails, UUID mismatch errors)
- **Wrong**: Not declaring dependencies in responsive image styles → **Right**: Declare all config dependencies (silent breakage when referenced style deleted)
- **Wrong**: Using `strict: true` in recipe meant for updates → **Right**: Use `strict: false` for updates (fails on existing sites)
- **Wrong**: Forgetting to install responsive_image module in recipe → **Right**: Add to install list (config import fails, module not found)
- **Wrong**: Exporting only responsive style without image styles → **Right**: Export all dependencies (broken config, missing dependencies)

## See Also

- [Creating Image Styles via Config](creating-styles-config.md)
- [Responsive Image Style Config](responsive-image-config.md)
- Reference: core/recipes/standard_responsive_images/recipe.yml
- Reference: https://www.drupal.org/docs/8/theming-drupal-8/including-default-image-styles-with-your-theme
