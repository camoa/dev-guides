---
description: Export image styles for version control and create distribution recipes with config dependencies and import strategies
---

# Config Export & Recipes

## When to Use

> Use this when you need to export image styles for version control or create a recipe to distribute image styles as reusable config.

## Steps - Config Export

### 1. Export specific image style

```bash
# View single style config
drush config:get image.style.large

# Full config export (includes all image styles)
drush config:export
```

### 2. Export for module/theme distribution

```bash
# Copy to module's config/install
cp config/sync/image.style.hero_large.yml modules/custom/my_module/config/install/

# Remove UUID from top of file (required for install config)
sed -i '1d' modules/custom/my_module/config/install/image.style.hero_large.yml
```

### 3. Export responsive image styles with dependencies

Responsive image styles depend on image styles. Export both:

```bash
# Export responsive style
drush config:export responsive_image.styles.hero

# Export all referenced image styles
drush config:export image.style.hero_small
drush config:export image.style.hero_medium
drush config:export image.style.hero_large
```

## Steps - Creating a Recipe

### 1. Create recipe directory structure

```
recipes/my_images/
├── recipe.yml
└── config/
    ├── image.style.hero_large.yml
    ├── image.style.hero_medium.yml
    └── responsive_image.styles.hero.yml
```

### 2. Create recipe.yml

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

### 3. Apply recipe

```bash
# Apply recipe to site
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

**Always declare dependencies** in responsive image style config:

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

- Exporting config with UUID for module distribution → Config import fails, UUID mismatch errors
- Not declaring dependencies in responsive image styles → Silent breakage when referenced style deleted
- Using `strict: true` in recipe meant for updates → Fails on existing sites, should use `strict: false`
- Forgetting to install responsive_image module in recipe → Config import fails, module not found
- Exporting only responsive style without image styles → Broken config, missing dependencies
- Not removing site-specific values from exported config → UUID conflicts, unexpected site references

## See Also

- [Creating Image Styles via Config](creating-styles-config.md)
- [Responsive Image Style Config](responsive-image-config.md)
- Reference: core/recipes/standard_responsive_images/recipe.yml
- Reference: https://www.drupal.org/docs/8/theming-drupal-8/including-default-image-styles-with-your-theme
