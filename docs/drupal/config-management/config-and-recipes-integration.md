---
description: Distribute reusable configuration bundles with Recipes — modules, config, and content as a single installable unit.
---

# Config & Recipes Integration

## When to Use

When you need to distribute reusable configuration bundles (Recipes) that install modules, config, and content together as a single unit for features or starter kits.

## Recipes Overview

**Recipes** (Drupal 11+) are YAML-defined installation profiles that bundle:
- Modules to enable
- Configuration to import
- Content to create
- Dependencies on other recipes

Recipes replace Features module and installation profiles for distributing functionality.

## Recipe Structure

```
my_recipe/
├── recipe.yml              # Recipe definition
├── config/                 # Config to import
│   └── install/
│       ├── node.type.article.yml
│       └── views.view.articles.yml
└── content/                # Content to create (optional)
    └── node/
        └── article.yml
```

## Example: Recipe Definition

```yaml
# my_recipe/recipe.yml
name: 'Article Management'
description: 'Article content type with views'
type: 'Feature'
version: '1.0'

install:
  # Modules to enable
  - node
  - views
  - field
  - text

recipes:
  # Depend on other recipes
  - core/recipes/standard_media

config:
  # Config to import (from config/install/)
  import:
    node:
      - node.type.article
    views:
      - views.view.articles
    field:
      - field.storage.node.body
      - field.field.node.article.body

content:
  # Content to create (optional)
  node:
    - content/node/sample_article.yml
```

**Reference:** Core recipes at `/core/recipes/`

## Applying Recipes

```bash
# Apply recipe via Drush
drush recipe my_recipe

# Apply recipe from module
drush recipe modules/custom/mymodule/recipes/feature

# Apply core recipe
drush recipe core/recipes/article_with_summary
```

## Config in Recipes vs Config Management

**Config Management** — For ongoing site configuration
- Export: `drush cex`
- Import: `drush cim`
- Tracks changes between environments
- Version controlled

**Recipes** — For initial setup and feature distribution
- One-time application
- Bundles modules + config + content
- Reusable across sites
- Not for ongoing changes

## Creating Config for Recipes

1. **Build feature in dev site** — Create content types, views, fields via UI
2. **Export config** — `drush cex` to see what config was created
3. **Copy config to recipe** — Copy relevant files to `recipe/config/install/`
4. **Test recipe** — Apply to clean site: `drush recipe recipe_name`
5. **Refine dependencies** — Ensure all module dependencies listed
6. **Document usage** — Add README.md with instructions

## Example: Recipe with Config Dependencies

```yaml
# recipe.yml
name: 'Event Management'
install:
  - node
  - field
  - datetime

config:
  import:
    node:
      - node.type.event
    field:
      - field.storage.node.field_event_date
      - field.field.node.event.field_event_date
```

```yaml
# config/install/node.type.event.yml
type: event
name: Event
description: 'Events with date/time'
dependencies:
  module:
    - node
```

```yaml
# config/install/field.storage.node.field_event_date.yml
id: node.field_event_date
field_name: field_event_date
entity_type: node
type: datetime
settings:
  datetime_type: datetime
dependencies:
  module:
    - datetime
    - node
```

## Common Mistakes

- No module dependencies — Recipe installs config before modules enabled, fails
- Wrong config export list — Missing config, feature incomplete
- Hardcoded UUIDs — UUID conflicts when applied to existing sites
- No recipe dependencies — Assuming base config exists, breaks on clean install
- Recipes for ongoing changes — Use config management instead
- Not testing on clean site — Recipe works on dev site (config exists), fails elsewhere

## See Also

- [Config Installer](config-installer.md) — module install config
- [Config Dependencies](config-dependencies.md) — dependency management
- [Config Entities](config-entities.md) — config entity structure
- Reference: [Recipes Initiative](https://www.drupal.org/project/distributions_recipes)
