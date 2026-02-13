---
description: Content type YAML configuration for exportable content types
drupal_version: "11.x"
---

# Content Type Configuration

## When to Use

When creating content types via configuration management (YAML files) for deployment across environments, or when exporting existing content types for version control.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Simple content type | YAML configuration | Exportable, version controlled, no code required |
| Dynamic content types | Programmatic creation | Can be created/modified by site builders at runtime |
| Custom content entity | Custom bundle entity class | Full control over behavior and validation |

## Pattern

Content type definition in `config/install/node.type.article.yml`:

```yaml
langcode: en
status: true
dependencies:
  module:
    - menu_ui
third_party_settings:
  menu_ui:
    available_menus: [main]
    parent: 'main:'
name: 'Article'
type: article
description: 'Time-sensitive content like news or blog posts.'
help: null
new_revision: true        # Enable revisions by default
preview_mode: 1           # Optional preview
display_submitted: true   # Show author/date
```

Install via `drush config:import` or module installation. Dependencies ensure menu_ui is installed first.

Reference: `/core/modules/node/config/install/node.type.article.yml`

## Common Mistakes

- **Wrong**: Forgetting module dependencies → **Right**: Results in broken config imports when required modules aren't installed
- **Wrong**: Using underscores in machine names → **Right**: Use lowercase letters and hyphens only for consistency
- **Wrong**: Missing help text → **Right**: Content creators need guidance; add description and help fields
- **Wrong**: Enabling features without dependencies → **Right**: Check third_party_settings requirements before enabling

## See Also

- [Entity Architecture Fundamentals](entity-architecture-fundamentals.md)
- [Bundle Entity Implementation](bundle-entity-implementation.md) for programmatic creation
- Reference: [Content type configuration schema](https://git.drupalcode.org/project/drupal/-/blob/11.x/core/modules/node/config/schema/node.schema.yml)
