---
description: Package and distribute reusable configuration with Drupal Recipes for composable, version-controlled config distribution across sites.
---

# Recipes for Reusable Config

## When to Use

When you want to package and distribute reusable configuration setups (content types, fields, views, modules) across multiple Drupal sites or projects. Recipes are Drupal 11's successor to installation profiles and features.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Reusable config across multiple sites | Recipe | Composable, distributable, version-controlled |
| One-time site setup | Installation profile or manual config | Recipes are for reusable patterns |
| Configuration for a specific site | Standard config management | Recipes are for distribution, not site-specific config |
| Modular config bundles | Multiple composable recipes | Recipes can depend on other recipes |

## Pattern

```yaml
# recipes/my_content_type/recipe.yml
name: Article Content Type
description: Adds Article content type with common fields
type: Recipe
recipes:
  - core/recipes/article_tags
install:
  - node
  - field
  - text
  - image
config:
  import:
    node_type:
      - node.type.article
    field_config:
      - field.field.node.article.body
      - field.field.node.article.field_image
    field_storage:
      - field.storage.node.body
      - field.storage.node.field_image
```

```yaml
# recipes/my_content_type/config/node.type.article.yml
langcode: en
status: true
dependencies: {  }
name: Article
type: article
description: 'Use articles for time-sensitive content like news and blog posts.'
help: ''
new_revision: true
preview_mode: 1
display_submitted: true
```

## Applying Recipes

```bash
# Apply recipe to existing site
php core/scripts/drupal recipe recipes/my_content_type

# Via Composer (for distributed recipes)
composer require myorg/my-recipe
php core/scripts/drupal recipe vendor/myorg/my-recipe
```

Reference: `core/recipes/`, Drupal Recipes documentation at drupal.org/docs/extending-drupal/drupal-recipes

## Modular Recipe Composition

```yaml
# recipes/my_site_starter/recipe.yml
name: My Site Starter
description: Complete site setup with all content types and config
type: Recipe
recipes:
  - myorg/article_content_type
  - myorg/page_content_type
  - myorg/custom_blocks
  - myorg/site_branding
install:
  - admin_toolbar
  - pathauto
config:
  import:
    pathauto:
      - pathauto.pattern.article
```

## Common Mistakes

- **Creating recipes for site-specific config** — Recipes are for reusable patterns; use standard config management for site-specific settings
- **Not making recipes modular** — Keep recipes focused; compose larger setups from smaller recipes
- **Duplicating config across recipes** — Extract shared config into its own recipe, reference from others
- **Not version controlling recipes** — Recipes should be in version control like any other code
- **Forgetting dependencies** — Declare module dependencies in `install:` section

## See Also

- [Config Split and Environments](config-split-environments.md)
- [Drush and CLI Reuse](drush-cli-reuse.md)
- Reference: [Drupal Recipes | Drupal.org](https://www.drupal.org/docs/extending-drupal/drupal-recipes)
- Reference: [Cooking up irresistible Drupal websites with Recipes | Specbee](https://www.specbee.com/blogs/cooking-irresistible-drupal-websites-with-recipes)
